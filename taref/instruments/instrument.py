# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 17:25:53 2015

@author: thomasaref
"""

from atom.api import Bool, Enum, Float
from taref.core.agent import Agent
from taref.core.log import log_info#, log_warning, log_debug#, make_log_file
from taref.core.atom_extension import (private_property, set_tag, get_tag, log_func, tag_Callable, set_all_tags,
                                       make_instancemethod, get_value_check, safe_setattr, safe_log_debug, safe_set_tag)
from taref.filer.save_file import Save_HDF5
from contextlib import contextmanager
from time import sleep
from taref.core.shower import shower
#from enaml.application import Application, deferred_call

from enaml import imports
with imports():
    from taref.instruments.instrument_e import ControlView, InstrumentView

class InstrumentError(Exception):
    pass

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
    saving=False
    save_file=Save_HDF5()

    timeout=Float(1).tag(sub=True, desc="timeout in seconds")

    def wait_loop(self, delay):
        names=[thread.name for thread in self.thread_list if "wait_loop" in thread.name]
        self.add_thread("wait_loop {}".format(len(names)), self.do_wait_loop, delay)

    def do_wait_loop(self, delay):
        """uses self.loop to provide updating delay in increments of 100 ms"""
        for n in self.loop(int(delay/0.1)):
            sleep(0.1)
                            
    @classmethod
    def run_measurement(cls):
        """shortcut method for running all measurements defined in run_func_dict"""
        log_info("Measurement started")
        for func in cls.run_func_dict.values():
            func()
        log_info("Measurement finished")

    status=Enum( "Closed", "Active").tag(private=True, desc="a description of if the instrument is active or not, i.e. has been booted")
    send_now=Bool(True).tag(private=True, desc="when true, changing a value automatically sends it to the instrument if a send_cmd exists for that value")

    @classmethod
    def clean_up(cls):
        """extends clean_up to close all instruments"""
        super(Instrument, cls).clean_up()
        cls.close_all()

    @classmethod
    def boot_all(cls):
        log_info("Booting all instruments")
        for instr in cls.get_agents(Instrument).values():
            instr.boot()
        log_info("All instruments successfully booted")

    @classmethod
    def close_all(cls):
        """attempts to close all instruments, then raises any errors that occurred"""
        cls.abort_all()
        log_info("Closing all instruments")
        for name, instr in cls.get_agents(Instrument).iteritems():
            instr.close()
        log_info("All instruments successfully closed")

    @booter
    def booter(self):
        """default booter does nothing. can be overwritten"""
        pass

    @closer
    def closer(self):
        """defualt closer does nothing. can be overwritten"""
        pass

    def preboot(self):
        """actions before boot. default is to do nothing. can be overwritten in child classes"""
        pass

    def boot(self,  **kwargs):
        """Boot the instrument using booter function if it exists"""
        if self.busy:
            raise InstrumentError("Trying to boot while busy")
        if self.status=="Closed":
            self.status="Active"
            self.preboot()
            self.booter(**kwargs)
            self.postboot()

    def postboot(self):
        """allows extra setup after instrument is booted. can be overwritten in child classes. default is to do nothing"""
        pass

    def _observe_status(self, change):
        """observer for status. logs booting and closing"""
        if change["type"]!="create":
            if self.status=="Active":
                log_info("BOOTED: {0}".format(self.name))
            elif self.status=="Closed":
                log_info("CLOSED: {0}".format(self.name))

    def close(self,  **kwargs):
        """Close the instrument"""
        if self.status=="Active":
            if self.busy:
                self.abort=True #safe_setattr(self, "abort", True)
            self.status="Closed" #safe_setattr(self, "status", "Closed")
            self.pre_close()
            self.closer(**kwargs)
            self.post_close()

    def pre_close(self):
        """allows extra action pre closing. default is to do nothing"""
        pass

    def post_close(self):
        """allows extra actions post closing. default is to log closing"""
        pass

    def _observe_send_now(self, change):
        """if instrument send_now changes, change all send_now tags of parameters"""
        print change
        if change['type']!='create':
            set_all_tags(self, send_now=self.send_now, n=0)

    @private_property
    def view_window(self):
        return InstrumentView(instr=self)

    @private_property
    def view(self):
        from taref.instruments.instrument_e import InstrLooper
        return InstrLooper

    chief_window=ControlView(name="instr_control", title="Instrument Control")

    def receive_log(self, name):
        """Log for receiving. can be overwritten in child classes for customization of message"""
        label=get_tag(self, name, 'label', name)
        print "RECEIVE: {instr} {label}".format(instr=self.name, label=label)

    def receive(self, name):
        self.add_thread("receive "+name, self.do_receive, name)

    def do_receive(self, name, **kwargs):
        """performs receive of parameter name i.e. executing associated get_cmd with value checking"""
        get_cmd=get_tag(self, name, 'get_cmd')
        if self.status=="Active":
            if get_cmd!=None:
                if not hasattr(get_cmd, "pname"):
                    get_cmd=log_func(get_cmd, name)
                    set_tag(self, name, get_cmd=get_cmd)
                self.receive_log(name)
                value=get_cmd(self, **kwargs)
                if isinstance(value, dict):
                    self.nosend_safeset(**value)
                    return value[name]
                else:
                    self.nosend_safeset(**{name:value})
                    return value
#                #safe_log(value)
#                with self.nosend_context(name):
#                    value=type(getattr(self, name))(value)
#                    value=get_value_check(self, name, value)
#                    safe_setattr(self, name, value)
                #return value
            else:
                print "WARNING: {instr} {name} get_cmd doesn't exist".format(instr=self.name, name=name)
        else:
            print "WARNING: Instrument {instr} not active".format(instr=self.name)

    @contextmanager
    def nosend_context(self, name):
        """context that temporarily turns off auto sending for it's duration"""
        temp=get_tag(self, name, 'send_now', self.send_now)
        safe_set_tag(self, name, send_now=False)
        yield
        safe_set_tag(self, name, send_now=temp)
    
    def nosend_safeset(self, **kwargs):
        for key, value in kwargs.iteritems():
            with self.nosend_context(key):
                value=get_value_check(self, key, value)
                safe_setattr(self, key, value)
                
    def send_log(self, name):
        """Log for sending. can be overwritten in child classes to allow customization of message"""
        label=get_tag(self, name, 'label', name)
        print "SEND: {instr} {label}".format(instr=self.name, label=label)

    def send(self, **kwargs):
        keys=kwargs.keys()
        if len(keys)!=1:
            raise InstrumentError("send takes argument of form param=value")
        name=keys[0]
        self.add_thread("send "+name, self.do_send, name, kwargs[name])

    def do_send(self, name, value=None, **kwargs):
        """performs send of parameter name i.e. executing associated set_cmd. If value is specified, parameter is set to value
        kwargs allows additional parameters required by set_cmd to be fed in."""
        if self.status=="Active":
            set_cmd=get_tag(self, name, 'set_cmd')
            if set_cmd!=None:
                if not hasattr(set_cmd, "pname"):
                    set_cmd=log_func(set_cmd, name)
                    set_tag(self, name, set_cmd=set_cmd)
                with self.nosend_context(name):
                    if value is not None:
                        safe_setattr(self, name, value)
                    self.send_log(name)
                    value=set_cmd(self, **kwargs)
            else:
                print "WARNING: {instr} {name} set_cmd doesn't exist".format(instr=self.name, name=name)
        else:
            print "WARNING: Instrument {instr} not active".format(instr=self.name)


    def __setattr__(self, name, value):
        """extends __setattr__ to add automatic sending if tag send_now is true.
        This is preferable to using observing since it is called everytime the parameter value is set,
        not just when it changes."""
        super(Instrument, self).__setattr__( name, value)
        if name in self.all_params:
            if get_tag(self, name, 'send_now', self.send_now):
                if get_tag(self, name, 'set_cmd')!=None:
                    self.send(**{name:value})

    def __init__(self, **kwargs):
        """init adds booter and closer as instance methods"""
        super(Instrument, self).__init__(**kwargs)
        make_instancemethod(self, self.booter)
        make_instancemethod(self, self.closer)


if __name__=="__main__":
    a=Instrument(name='blah')
    b=Instrument(name="bob")
    shower(a)
    #a.boot()
    #def run():
    #    print a, type(a)
    #a.add_func(run)
    #a.boss.saving=False
    #a.show()
