# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:07:30 2016

@author: thomasaref
"""

from enaml.application import Application, schedule, deferred_call, ScheduledTask
from threading import Thread

from time import sleep

from atom.api import Atom, Bool, Int, Float, Unicode, Property, Typed
from enaml import imports
with imports():
    from test_thread_e import Main
from contextlib import contextmanager
#def code_caller(topdog, code, *args, **kwargs):
#    result=code(*args, **kwargs)
#    try:
#        deferred_call(setattr, topdog, 'busy', False)
#        deferred_call(setattr, topdog, 'progress', 0)
#        deferred_call(setattr, topdog, 'abort', False)
#    except RuntimeError:
#        topdog.busy=False
#        topdog.progress=0
#        topdog.abort=False
#    return result
#
#def do_it_if_needed(topdog, code, *args, **kwargs):
#    if not topdog.busy:
#        topdog.busy = True
#        thread = Thread(target=code_caller, args=(topdog, code)+args, kwargs=kwargs)
#        thread.start()
#
def safe_setattr(obj, name, value):
    if Application.instance() is None:
        return setattr(obj, name, value)
    deferred_call(setattr, obj, name, value)

def safe_getattr(obj, name, default=None):
    if Application.instance() is None:
        return getattr(obj, name, default)
    return schedule(getattr, args=(obj, name, default))
    
class Test(Atom):
    a=Unicode()
    _busy=False
    _abort=False
    _prog=0
    b=Unicode()
    
    @Property
    def busy(self):
        return self._busy

    @busy.setter
    def set_busy(self, value):
        type(self)._busy=value
        self.get_member("busy").reset(self)

    @Property
    def prog(self):
        return self._prog

    @prog.setter
    def set_prog(self, value):
        type(self)._prog=value
        self.get_member("prog").reset(self)
 
    @Property
    def abort(self):
        return self._abort
    
    @abort.setter
    def set_abort(self, value):
        type(self)._abort=value
        self.get_member("abort").reset(self)
        
    @property
    def view_window(self):
        return Main(obj=self)

    st=Typed(ScheduledTask).tag(private=True)        

    def loop(self, start, stop=None, step=1):
        """an assisting generator for looping with
        abort and progress. Use like range"""
        try:
            if stop is None:
                stop=start
                start=0
            for n in range(start, stop, step):
                if self.abort:
                    break
                self.prog=int((n+1.0)*step/(stop-start)*100.0)
                yield n
        finally:
            safe_setattr(self, "prog", 0)
            safe_setattr(self, "abort", False)
            safe_setattr(self, "busy", False)
            
    def run_loop(self):
        for n in self.loop(10):
            for m in self.loop(5):
                print n, m
                sleep(0.5)
                
            
#    def loop_step(self, n):
#        with run_loop
#        print n
#        sleep(0.5)
        
    def _observe_busy(self, change):
        print change
        #if self.st is not None:
        #    print self.st.result()

    def _observe_b(self, change):
        print change
        #if self.st is not None:
        #    print self.st.result()
        
    def _observe_a(self, change):
        if change["type"]=="update":
            self.busy=True
            if Application.instance() is not None:
                self.st=schedule(self.run_loop, args=(), kwargs={})
            else:
                self.run_loop()

    def do_it_if_needed(self):
        if not self.busy:
            self.busy = True
            thread = Thread(target=self.run_loop)#, args=(self.loop_step, 10))
            thread.daemon = True
            thread.start()

t=Test()
#print t.a
#safe_setattr(t, "a", "3")
#print t.a

from taref.core.shower import shower
shower(t)
    #def cocall(code, *args, **kwargs):
#    if Application.instance is None:
#        return code(*args, **kwargs)
#    else: