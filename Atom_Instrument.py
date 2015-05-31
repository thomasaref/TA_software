# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 17:25:53 2015

@author: thomasaref
"""

from atom.api import Unicode, Bool, Value, Callable, List, Enum
from Atom_InstrumentBoss import instrumentboss as inboss #boss is imported to make it a singleton (all instruments have the same boss)
from Atom_Base import Base, log

import enaml
from enaml.qt.qt_application import QtApplication
from LOG_functions import log_info, log_warning, make_log_file

class InstrumentError(Exception):
    pass

def boot_func(instr):
    """default do nothing boot_func to allow definition of booter"""
    pass

def close_func(instr):
    """default do nothing close func to allow definition of closer"""
    pass

class Instrument(Base):
    """Base instrument class. Provides almost all functionality"""
    session=Value().tag(private=True)
    busy=Bool(False).tag(private=True)
    status=Enum( "Closed", "Active").tag(private=True)
    plot_x=Unicode().tag(private=True) #remove?
    send_now=Bool(True).tag(private=True)

    booter=Callable(boot_func).tag(private=True)
    closer=Callable(close_func).tag(private=True)

    #def _default_reserved_names(self):
    #    """reserved names not to perform standard logging and display operations on. Updates Slave's definition"""
    #    return Instrument.members().keys()

    def boot(self,  **kwargs):
        """Boot the instrument"""
        log_info("BOOT: {0}".format(self.name))
        self.status="Active"
        self.booter(self, **kwargs)

    def close(self,  **kwargs):
        """Close the instrument"""
        log_info("CLOSE: {0}".format(self.name))
        self.status="Closed"
        self.closer(self, **kwargs)

    def _observe_send_now(self, change):
        """if instrument send_now changes, change all send_now tags of parameters"""
        if change['type']!='create':
            self.set_all_tags(send_now=self.send_now)

    def show(self):
        """stand alone for showing instrument. Shows a modified boss view that has the instrument as a dockpane"""
        with enaml.imports():
            from enaml_Instrument import InstrMain as InstrMain
            #from enaml_Base import AutoInstrView as InstrMain
        try:
            app = QtApplication()
            view = InstrMain(instrin=self, boss=self.boss)
            view.show()
            app.start()
        finally:
            self.boss.close_all()

    def receive_log(self, name):
        """Log for receiving. can be overwritten in child classes for customization of message"""
        label=self.get_tag(name, 'label', name)
        log_info("RECEIVE: {instr} {label}".format(
                       instr=self.name, label=label))

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
        log_info("SEND: {instr} {label}".format(
                       instr=self.name, label=label))

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
            inv_map=self.get_tag(name, 'inv_map')
            if inv_map==None:
                mapping=self.get_tag(name, 'mapping')
                self.set_tag(name, inv_map={v:k for k, v in mapping.iteritems()})
                inv_map=self.get_tag(name, 'inv_map')
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

    def _default_boss(self):
        inboss.make_boss()
        return inboss

    def __init__(self, **kwargs):
        """extends __init__ of Slave to make booter and closer into logged functions"""
        super(Instrument, self).__init__(**kwargs)
        if not isinstance(self.booter, log):
            self.booter=log(self.booter)
        if not isinstance(self.closer, log):
            self.closer=log(self.closer)

if __name__=="__main__":
    a=Instrument(name='blah')
    b=Instrument(name="bob")
    a.boss.saving=False
    a.show()
