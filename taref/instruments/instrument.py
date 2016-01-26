# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 17:25:53 2015

@author: thomasaref
"""

from atom.api import Bool, Value, List, Enum, Callable
from taref.core.agent import Agent
from taref.core.log import log_info, log_warning, log_debug#, make_log_file
from taref.core.atom_extension import private_property, set_tag, get_tag, get_type, get_inv, log_func, tag_Callable, get_all_tags
from taref.core.save_file import Save_HDF5

class InstrumentError(Exception):
    pass

def get_value_check(obj, name, value):
        """coerces and checks value when getting. For Enum this allows the inverse mapping.
        For List, this calls the get_value_check for the respective parameter in the List"""
        value=obj.coercer(name, value)
        if get_type(obj, name) is Enum:
            return get_inv(obj, name, value)
        elif get_type(obj, name) is List:
            for key, item in value.iteritems():
                temp=get_tag(obj, key, 'send_now', obj.send_now)
                set_tag(obj, key, send_now=False)
                setattr(obj, key, get_value_check(obj, key, item))
                set_tag(obj, key, send_now=temp)
            return value.keys()
        return value

class booter(tag_Callable):
    default_kwargs=dict(desc="the boot function for the instrument", private=True, booter=True)

class closer(tag_Callable):
    default_kwargs=dict(desc="the close function for the instrument", private=True, closer=True)

class Instrument(Agent):
    """Instrument class. Provides functionality for running instruments"""
    base_name="instrument"
    busy=False
    saving=False
    abort=False
    progress=0
    save_file=Save_HDF5()
    view="instrument"

    @classmethod
    def run_measurement(cls):
        log_info("Measurement started")
        cls.run()
        log_info("Measurement finished")

    @classmethod
    def run(cls):
        pass

    @private_property
    def progress(self):
        return self.int_progress

    session=Value().tag(private=True, desc="a link to the session of the instrument. useful particularly for dll-based instruments")
    status=Enum( "Closed", "Active").tag(private=True, desc="a description of if the instrument is active or not, i.e. has been booted")
    send_now=Bool(True).tag(private=True, desc="when true, changing a value automatically sends it to the instrument if a send_cmd exists for that value")

    def show(self):
        """saves data and closes instruments if it crashes"""
        from taref.core.shower import shower
        try:
            shower(self)
        finally:
            self.close_all()
            if self.saving:
                self.save_file.flush_buffers()

    @classmethod
    def boot_all(cls):
        for instr in cls.agent_dict.values():
            if instr.status=='Closed':
                instr.boot()

    @classmethod
    def close_all(cls):
        for instr in cls.agent_dict.values():
            if instr.status=='Active':
                instr.close()

    @private_property
    def cls_run_funcs(self):
        """class or static methods to include in run_func_dict on initialization. Can be overwritten in child classes"""
        return [self.boot_all, self.close_all, self.run_measurement, self.run]

    def boot(self,  **kwargs):
        """Boot the instrument using booter function if it exists"""
        log_info("BOOTED: {0}".format(self.name))
        self.status="Active"
        booter=get_all_tags(self, "booter", True)
        if booter!=[]:
            getattr(self, booter[0])(self, **kwargs)

    def close(self,  **kwargs):
        """Close the instrument using closer function if it exists"""
        log_info("CLOSED: {0}".format(self.name))
        self.status="Closed"
        closer=get_all_tags(self, "closer", True)
        if closer!=[]:
            getattr(self, closer[0])(self, **kwargs)

    def _observe_send_now(self, change):
        """if instrument send_now changes, change all send_now tags of parameters"""
        if change['type']!='create':
            self.set_all_tags(send_now=self.send_now)

    @private_property
    def view_window2(self):
        from enaml import imports
        with imports():
            from instrument_e import InstrMain
        return InstrMain(instrin=self)

    def receive_log(self, name):
        """Log for receiving. can be overwritten in child classes for customization of message"""
        label=get_tag(self, name, 'label', name)
        log_info("RECEIVE: {instr} {label}".format(instr=self.name, label=label))

    def receive(self, name, **kwargs):
        """performs receive of parameter name i.e. executing associated get_cmd with value checking"""
        get_cmd=get_tag(self, name, 'get_cmd')
        if get_cmd!=None and self.status=='Active':
            if not hasattr(get_cmd, "pname"):
                get_cmd=log_func(get_cmd, name)
                set_tag(self, name, get_cmd=get_cmd)
            self.receive_log(name)
            Instrument.busy=True
            value=get_cmd(self, **kwargs)
            Instrument.busy=False
            temp=get_tag(self, name, 'send_now', self.send_now)
            set_tag(self, name, send_now=False)
            value=get_value_check(self, name, value)
            setattr(self, name, value)
            set_tag(self, name, send_now=temp)
        else:
            log_warning("WARNING: get_cmd doesn't exist or instrument not active")

    def send_log(self, name):
        """Log for sending. can be overwritten in child classes to allow customization of message"""
        label=get_tag(self, name, 'label', name)
        log_info("SEND: {instr} {label}".format(instr=self.name, label=label))

    def send(self, name, value=None, **kwargs):
        """performs send of parameter name i.e. executing associated set_cmd. If value is specified, parameter is set to value
        kwargs allows additional parameters required by set_cmd to be fed in."""
        set_cmd=get_tag(self, name, 'set_cmd')
        if set_cmd!=None and self.status=='Active':
            if not hasattr(set_cmd, "pname"):
                set_cmd=log_func(set_cmd)
                set_tag(self, name, set_cmd=set_cmd)
            Instrument.busy=True
            temp=get_tag(self, name, 'send_now', self.send_now)
            set_tag(self, name, send_now=False)
            if value!=None:
                setattr(self, name, value)
            self.send_log(name)
            set_cmd(self, **kwargs)
            set_tag(self, name, send_now=temp)
            Instrument.busy=False
        else:
            log_warning("WARNING: set_cmd doesn't exist or instrument not active")



    def __setattr__(self, name, value):
        """extends __setattr__ to add automatic sending if tag send_now is true.
        This is preferable to using observing since it is called everytime the parameter value is set,
        not just when it changes."""
        super(Instrument, self).__setattr__( name, value)
        if name in self.all_params:
            if get_tag(self, name, 'send_now', self.send_now):
                if get_tag(self, name, 'set_cmd')!=None and self.status=='Active':
                    self.send(name)

if __name__=="__main__":
    a=Instrument(name='blah')
    b=Instrument(name="bob")
    a.boot()
    #a.boss.saving=False
    a.show()
