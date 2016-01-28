# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 17:25:53 2015

@author: thomasaref
"""

from atom.api import Bool, Value, List, Enum, Callable
from taref.core.agent import Agent
from taref.core.log import log_info, log_warning, log_debug#, make_log_file
from taref.core.atom_extension import private_property, set_tag, get_tag, get_type, get_inv, log_func, tag_Callable, get_all_tags, set_all_tags, make_instancemethod
from taref.core.save_file import Save_HDF5

class InstrumentError(Exception):
    pass

def get_value_check(obj, name, value):
        """coerces and checks value when getting. For Enum this allows the inverse mapping.
        For List, this calls the get_value_check for the respective parameter in the List"""
        if get_type(obj, name) is Enum:
            return get_inv(obj, name, value)
#        elif get_type(obj, name) is List:
#            for key, item in value.iteritems():
#                temp=get_tag(obj, key, 'send_now', obj.send_now)
#                set_tag(obj, key, send_now=False)
#                setattr(obj, key, get_value_check(obj, key, item))
#                set_tag(obj, key, send_now=temp)
#            return value.keys()
        return value

class tag_booter(tag_Callable):
    default_kwargs=dict(desc="the boot function for the instrument", private=True)

def booter(func):
    return tag_booter()(func)

class tag_closer(tag_Callable):
    default_kwargs=dict(desc="the close function for the instrument", private=True)

def closer(func):
    return tag_closer()(func)

class Instrument(Agent):
    """Instrument class. Provides functionality for running instruments"""
    base_name="instrument"
    busy=False
    saving=False
    abort=False
    int_progress=0
    save_file=Save_HDF5()

    @classmethod
    def run_measurement(cls):
        log_info("Measurement started")
        for func in cls.run_func_dict.values():
            func()
        log_info("Measurement finished")

    @private_property
    def progress(self):
        return self.int_progress

    session=Value().tag(private=True, desc="a link to the session of the instrument. useful particularly for dll-based instruments")
    status=Enum( "Closed", "Active").tag(private=True, desc="a description of if the instrument is active or not, i.e. has been booted")
    send_now=Bool(True).tag(private=True, desc="when true, changing a value automatically sends it to the instrument if a send_cmd exists for that value")

#    def show(self, *args, **kwargs):
#        instr_show(*((self,)+args), **kwargs)

    @classmethod
    def show(cls, *args, **kwargs):
        from taref.core.shower import shower
        from enaml import imports
        with imports():
            from taref.instruments.instrument_e import ControlView
        kwargs.update(dict(chief_view=ControlView, chief_cls=cls, name="instr_control", title="Instrument Control"))
        try:
            shower(*args, **kwargs)
        finally:
            Instrument.close_all()
            if Instrument.saving:
                Instrument.save_file.flush_buffers()


    @classmethod
    def boot_all(cls):
        for instr in cls.agent_dict.values():
            instr.boot()

    @classmethod
    def close_all(cls):
        for instr in cls.agent_dict.values():
            instr.close()

    @booter
    def booter(self):
        pass

    @closer
    def closer(self):
        pass

    def boot(self,  **kwargs):
        """Boot the instrument using booter function if it exists"""
        if self.status=="Closed":
            log_info("BOOTED: {0}".format(self.name))
            self.status="Active"
            self.booter(**kwargs)

    def close(self,  **kwargs):
        """Close the instrument using closer function if it exists"""
        if self.status=="Active":
            log_info("CLOSED: {0}".format(self.name))
            self.status="Closed"
            self.closer(**kwargs)

    @private_property
    def close_name(self):
        close_list=get_all_tags(self, "closer", True)
        return close_list[0] if close_list!=[] else ""

    def _observe_send_now(self, change):
        """if instrument send_now changes, change all send_now tags of parameters"""
        if change['type']!='create':
            set_all_tags(self, send_now=self.send_now)

    @private_property
    def view_window(self):
        from enaml import imports
        with imports():
            from taref.instruments.instrument_e import InstrumentView
        return InstrumentView(instr=self)

    @private_property
    def view(self):
        from taref.instruments.instrument_e import InstrLooper
        return InstrLooper

    def receive_log(self, name):
        """Log for receiving. can be overwritten in child classes for customization of message"""
        label=get_tag(self, name, 'label', name)
        log_info("RECEIVE: {instr} {label}".format(instr=self.name, label=label))

    def receive(self, name, **kwargs):
        """performs receive of parameter name i.e. executing associated get_cmd with value checking"""
        get_cmd=get_tag(self, name, 'get_cmd')
        if self.status=="Active":
            if get_cmd!=None:
                if not hasattr(get_cmd, "pname"):
                    get_cmd=log_func(get_cmd, name)
                    set_tag(self, name, get_cmd=get_cmd)
                self.receive_log(name)
                Instrument.busy=True
                value=get_cmd(self, **kwargs)
                log_debug(value)
                Instrument.busy=False
                temp=get_tag(self, name, 'send_now', self.send_now)
                set_tag(self, name, send_now=False)
                value=get_value_check(self, name, value)

                setattr(self, name, value)
                set_tag(self, name, send_now=temp)
            else:
                log_warning("WARNING: {instr} {name} get_cmd doesn't exist".format(instr=self.name, name=name))
        else:
            log_warning("WARNING: Instrument {instr} not active".format(instr=self.name))

    def send_log(self, name):
        """Log for sending. can be overwritten in child classes to allow customization of message"""
        label=get_tag(self, name, 'label', name)
        log_info("SEND: {instr} {label}".format(instr=self.name, label=label))

    def send(self, name, value=None, **kwargs):
        """performs send of parameter name i.e. executing associated set_cmd. If value is specified, parameter is set to value
        kwargs allows additional parameters required by set_cmd to be fed in."""
        set_cmd=get_tag(self, name, 'set_cmd')
        if self.status=="Active":
            if set_cmd!=None and self.status=='Active':
                if not hasattr(set_cmd, "pname"):
                    set_cmd=log_func(set_cmd, name)
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
                log_warning("WARNING: {instr} {name} set_cmd doesn't exist".format(instr=self.name, name=name))
        else:
            log_warning("WARNING: Instrument {instr} not active".format(instr=self.name))


    def __setattr__(self, name, value):
        """extends __setattr__ to add automatic sending if tag send_now is true.
        This is preferable to using observing since it is called everytime the parameter value is set,
        not just when it changes."""
        super(Instrument, self).__setattr__( name, value)
        if name in self.all_params:
            if get_tag(self, name, 'send_now', self.send_now):
                if get_tag(self, name, 'set_cmd')!=None:
                    self.send(name)

    def __init__(self, **kwargs):
        super(Instrument, self).__init__(**kwargs)
        make_instancemethod(self, self.booter)
        make_instancemethod(self, self.closer)

if __name__=="__main__":
    a=Instrument(name='blah')
    b=Instrument(name="bob")
    a.boot()
    def run():
        print a, type(a)
    a.add_func(run)
    #a.boss.saving=False
    a.show()
