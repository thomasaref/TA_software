# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 21:59:45 2016

@author: zebra
"""

from taref.instruments.instrument import Instrument
from atom.api import Float, Unicode
from taref.core.atom_extension import tag_Callable, set_tag, get_tag, log_func, make_instancemethod#, safe_setattr
from time import sleep#, time
from taref.core.extra_setup import thread_callable

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

    @reader
    def reader(self):
        return self.command

    @writer
    def writer(self, write_str):
        """default writer does nothing"""
        pass #print write_str

    @asker
    def asker(self, ask_str):
        """default asker returns attr specified by ask_str"""
        return getattr(self, ask_str)

    @thread_callable()
    def example_loop(self):
        #self.do_it_busy(self.do_example_loop)
        print "starting loop"
        for n in self.loop(10):
            for m in self.loop(5):
                print n, m
                sleep(0.5)

    def extra_setup(self, param, typer):
        """extends extra_setup to set response get_cmd to self.reader
        and autoset set_cmd and get_cmd for params with get_str and set_str"""
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

    def __init__(self, **kwargs):
        """init adds reader, writer and asker as instance methods"""
        super(String_Instrument, self).__init__(**kwargs)
        make_instancemethod(self, self.reader)
        make_instancemethod(self, self.writer)
        make_instancemethod(self, self.asker)

    @thread_callable(sub=True, desc="function for test page which sends a commands, waits and gets a response")
    def command_response(self):
        if get_tag(self, "command", "do", False):
            self.do_send("command")
        if get_tag(self, "resp_delay", "do", False):
            self.wait_loop(self.resp_delay)
        if get_tag(self, "response", "do", False):
            self.do_receive("response")

    command=Unicode().tag(sub=True, set_str="{command}", send_now=False, do=True)
    resp_delay=Float(0.0).tag(sub=True, desc="delay in seconds", do=True)
    response=Unicode().tag(sub=True, get_str="command", spec="multiline", do=True)

if __name__=="__main__":
    a=String_Instrument()
    a.boot()
    a.command="blah"
    a.receive("response")

    #print dir(a.get_member("command_response"))
    #print dir(a.get_member("command_response").validate_mode[0].Callable)

    #print a.get_member("command_response").validate_mode[0]#(20)#'Callable']
    a.show()
    #from taref.core.shower import shower
    #shower(a)