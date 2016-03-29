# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:07:30 2016

@author: thomasaref
"""

from enaml.application import Application, schedule, deferred_call
from threading import Thread

def code_caller(topdog, code, *args, **kwargs):
    result=code(*args, **kwargs)
    try:
        deferred_call(setattr, topdog, 'busy', False)
        deferred_call(setattr, topdog, 'progress', 0)
        deferred_call(setattr, topdog, 'abort', False)
    except RuntimeError:
        topdog.busy=False
        topdog.progress=0
        topdog.abort=False
    return result

def do_it_if_needed(topdog, code, *args, **kwargs):
    if not topdog.busy:
        topdog.busy = True
        thread = Thread(target=code_caller, args=(topdog, code)+args, kwargs=kwargs)
        thread.start()

def safe_setattr(obj, name, value):
    if Application.instance() is None:
        return setattr(obj, name, value)
    deferred_call(setattr, obj, name, value)

def safe_getattr(obj, name, default=None):
    if Application.instance() is None:
        return getattr(obj, name, default)
    return schedule(getattr, args=(obj, name, default))
    
from atom.api import Atom, Float, Unicode, Property
from enaml import imports
with imports():
    from test_thread_e import Main
from time import sleep
    
class Test(Atom):
    a=Unicode()
    _busy=False
    _abort=False
    _prog=0
    
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
        
    def run_loop(self):

        for n in range(11):
            if self.abort:
                break
            self.prog=n*10
            print n
            sleep(0.5)
        self.busy=False
        self.abort=False
        self.prog=0
        
    def _observe_a(self, change):
        self.busy=True
        if Application.instance() is not None:
            thread = Thread(target=self.run_loop, args=(), kwargs={})
            thread.start()
        else:
            self.run_loop()

t=Test()
print t.a
#safe_setattr(t, "a", "3")
#print t.a

from taref.core.shower import shower
shower(t)
    #def cocall(code, *args, **kwargs):
#    if Application.instance is None:
#        return code(*args, **kwargs)
#    else: