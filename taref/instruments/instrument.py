# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 17:25:53 2015

@author: thomasaref
"""

from atom.api import Bool, Value, List, Enum
from taref.core.backbone import private_property, tagged_callable
from taref.core.agent import Agent
from taref.core.log import log_info, log_warning#, make_log_file


class InstrumentError(Exception):
    pass

def boot_func(func, **kwargs):
    """decorator function for booter function in instrument"""
    if "desc" not in kwargs:
        kwargs["desc"]="the boot function for the instrument"
    if "private" not in kwargs:
        kwargs["private"]=True
    return tagged_callable(**kwargs)(func)

def close_func(func, **kwargs):
    """decorator function for closer function in instrument"""
    if "desc" not in kwargs:
        kwargs["desc"]="the close function for the instrument"
    if "private" not in kwargs:
        kwargs["private"]=True
    return tagged_callable(**kwargs)(func)

class Instrument(Agent):
    """Instrument class. Provides functionality for running instruments"""
    session=Value().tag(private=True, desc="a link to the session of the instrument. useful particularly for dll-based instruments")
    status=Enum( "Closed", "Active").tag(private=True, desc="a description of if the instrument is active or not, i.e. has been booted")
    send_now=Bool(True).tag(private=True, desc="when true, changing a value automatically sends it to the instrument if a send_cmd exists for that value")

    def boot(self,  **kwargs):
        """Boot the instrument using booter function if it exists"""
        log_info("BOOTED: {0}".format(self.name))
        self.status="Active"
        if "booter" in self.members():
            self.booter(self, **kwargs)

    def close(self,  **kwargs):
        """Close the instrument using closer function if it exists"""
        log_info("CLOSED: {0}".format(self.name))
        self.status="Closed"
        if "closer" in self.members():
            self.closer(self, **kwargs)

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
        label=self.get_tag(name, 'label', name)
        log_info("RECEIVE: {instr} {label}".format(instr=self.name, label=label))

    def receive(self, name, **kwargs):
        """performs receive of parameter name i.e. executing associated get_cmd with value checking"""
        get_cmd=self.func2log(name, 'get_cmd')
        if get_cmd!=None and self.status=='Active':
            self.receive_log(name)
            #self.busy=True
            value=get_cmd(self, **kwargs)
            #self.busy=False
            temp=self.get_tag(name, 'send_now', self.send_now)
            self.set_tag(name, send_now=False)
            value=self.get_value_check(name, value)
            setattr(self, name, value)
            self.set_tag(name, send_now=temp)
        else:
            log_warning("WARNING: get_cmd doesn't exist or instrument not active")

    def send_log(self, name):
        """Log for sending. can be overwritten in child classes to allow customization of message"""
        label=self.get_tag(name, 'label', name)
        log_info("SEND: {instr} {label}".format(instr=self.name, label=label))

    def send(self, name, value=None, **kwargs):
        """performs send of parameter name i.e. executing associated set_cmd. If value is specified, parameter is set to value
        kwargs allows additional parameters required by set_cmd to be fed in."""
        set_cmd=self.func2log(name, 'set_cmd')
        if set_cmd!=None and self.status=='Active':
            #self.busy=True
            temp=self.get_tag(name, 'send_now', self.send_now)
            self.set_tag(name, send_now=False)
            if value!=None:
                setattr(self, name, value)
            self.send_log(name)
            set_cmd(self, **kwargs)
            self.set_tag(name, send_now=temp)
            #self.busy=False
        else:
            log_warning("WARNING: set_cmd doesn't exist or instrument not active")

    def get_value_check(self, name, value):
        """coerces and checks value when getting. For Enum this allows the inverse mapping.
        For List, this calls the get_value_check for the respective parameter in the List"""
        value=self.coercer(name, value)
        if self.get_type(name)==Enum:
            self.gen_inv_map(self, name)
            return self.get_tag(name, 'inv_map')[value]
        elif self.get_type(name)==List:
            for key, item in value.iteritems():
                temp=self.get_tag(key, 'send_now', self.send_now)
                self.set_tag(key, send_now=False)
                setattr(self, key, self.get_value_check(key, item))
                self.set_tag(key, send_now=temp)
            return value.keys()
        return value

    def __setattr__(self, name, value):
        """extends __setattr__ to add automatic sending if tag send_now is true.
        This is preferable to using observing since it is called everytime the parameter value is set,
        not just when it changes."""
        super(Instrument, self).__setattr__( name, value)
        if name in self.all_params:
            if self.get_tag(name, 'send_now', self.send_now)==True:
                if self.get_tag(name, 'set_cmd')!=None and self.status=='Active':
                    self.send(name)
    @private_property
    def chief(self):
        from taref.instruments.instrument_chief import instrument_chief #boss is imported to make it a singleton (all instruments have the same boss)
        #inboss.make_boss()
        return instrument_chief

#    def __init__(self, **kwargs):
#        """extends __init__ of Slave to make booter and closer into logged functions"""
#        super(Instrument, self).__init__(**kwargs)
#        if not isinstance(self.booter, log):
#            self.booter=log(self.booter)
#        if not isinstance(self.closer, log):
#            self.closer=log(self.closer)

if __name__=="__main__":
    a=Instrument(name='blah')
    b=Instrument(name="bob")
    a.boot()
    #a.boss.saving=False
    #a.show()
