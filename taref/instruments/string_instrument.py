# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 21:59:45 2016

@author: zebra
"""

from taref.instruments.instrument import Instrument
from atom.api import Float, Unicode
from taref.core.atom_extension import tag_Callable, set_tag, get_tag, log_func

class tag_writer(tag_Callable):
    default_kwargs=dict(desc="the boot function for the instrument", private=True)

def writer(func):
    return tag_writer()(func)

class tag_reader(tag_Callable):
    default_kwargs=dict(desc="the boot function for the instrument", private=True)

def reader(func):
    return tag_reader()(func)

class tag_asker(tag_Callable):
    default_kwargs=dict(desc="the boot function for the instrument", private=True)

def asker(func):
    return tag_asker()(func)

def new_ask_it(name, form_str, log_prefix=""):
    """get pass function. used as place holder."""
    def new_ask(instr, **kwargs):
        return instr.asker(form_str.format(**kwargs))
    new_ask=log_func(new_ask, name)
    new_ask.log_message=log_prefix+"ASK: {0} {1}: "+name
    return new_ask
    
def new_write_it(name, form_str, log_prefix=""):
    """send pass function. used as place holder"""
    def new_write(instr, **kwargs):
        instr.writer(form_str.format(**kwargs))
    new_write=log_func(new_write, name)
    new_write.log_message=log_prefix+"WRITE: {0} {1}: "+name
    new_write.run_params.append(name)
    return new_write
    
class String_Instrument(Instrument):
    """Instrument with string based communication"""
    base_name="String_Instrument"
    
    log_prefix="PASS "
    
#    @writer
#    def writer(self, write_str):
#        self.session.write(write_str)
#    
#    @asker        
#    def asker(self, ask_str):
#        return self.session.ask(ask_str)

    #@asker
    #def asker(self, ask_str):
    #    self.writer(ask_str)
    #    self.reader()

#    @private_property
#    def view_window(self):
#        from enaml import imports
#        with imports():
#            from taref.instruments.instrument_e import GPIB_InstrumentView
#        return GPIB_InstrumentView(instr=self)
        
    @reader
    def reader(self):
        return self.command
        
    @writer
    def writer(self, write_str):
        name, value=write_str.split("=")
        setattr(self, write_str)
        
    @asker
    def asker(self, ask_str):
        return getattr(self, ask_str)

    def extra_setup(self, param, typer):
        set_tag(self, "response", get_cmd=self.reader)
        write_string=get_tag(self, param, 'set_str')
        if write_string!=None:
            do=get_tag(self, param, "do", False)
            set_tag(self, param, set_cmd=new_write_it(param, write_string, self.log_prefix), do=do)
        ask_string=get_tag(self, param, 'get_str')
        if ask_string!=None:
            do=get_tag(self, param, "do", False)
            set_tag(self, param, get_cmd=new_ask_it(param, ask_string, self.log_prefix), do=do)
        super(String_Instrument, self).extra_setup(param, typer)  
        
    @tag_Callable(sub=True, desc="function for test page which sends a commands, waits and gets a response")
    def command_response(self):
        if get_tag(self, "command", "do", False):
            self.send("command")
        if get_tag(self, "resp_delay", "do", False):
            sleep(self.resp_delay)
        if get_tag(self, "response", "do", False):
            self.receive("response")

    command=Unicode().tag(sub=True, set_str="{command}", send_now=False, do=True)
    resp_delay=Float(0.0).tag(sub=True, unit2="s", desc="delay between command and response", do=True)
    response=Unicode().tag(sub=True, spec="multiline", do=True)  
    
if __name__=="__main__":
    a=String_Instrument()
    #a.boot()
    #a.command="blah"
    #a.receive("response")
    from taref.core.shower import shower
    shower(a)