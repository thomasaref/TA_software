# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:07:30 2016

@author: thomasaref
"""

from enaml.application import Application, schedule, deferred_call, ScheduledTask
from threading import Thread

from time import sleep

from atom.api import Atom, Bool, Int, Float, Unicode, Property, Typed, observe, Value, Event, ContainerList
from enaml import imports
with imports():
    from test_thread_e import Main
from contextlib import contextmanager

def safe_setattr(obj, name, value):
    if Application.instance() is None:
        return setattr(obj, name, value)
    deferred_call(setattr, obj, name, value)

def safe_getattr(obj, name, default=None):
    if Application.instance() is None:
        return getattr(obj, name, default)
    return schedule(getattr, args=(obj, name, default))

#from taref.core.atom_extension import set_tag, get_tag

from Queue import Queue, Empty

class Test(Atom):
    a=Unicode("bb")
    busy=Bool(False)
    abort=Bool(False)
    progress=Int(0)
    b=Unicode()
    thread=Typed(Thread)
    queue=Value() #Typed(Queue)
    done=Event()
    timeout=1.0
    thread_list=ContainerList()

    def _default_queue(self):
        return Queue(1)

    @property
    def view_window(self):
        return Main(obj=self)


#    @contextmanager
#    def busy_context(self):
#        safe_setattr(self, "busy", True)
#        yield
#        safe_setattr(self, "progress", 0)
#        safe_setattr(self, "abort", False)
#        safe_setattr(self, "busy", False)

    def loop(self, start, stop=None, step=1, _q=None):
        """an assisting generator for looping with
        abort and progress. Use like range"""
        if stop is None:
            stop=start
            start=0
        for n in range(start, stop, step):
            if self.abort:
                break
            safe_setattr(self, "progress", int((n+1.0)*step/(stop-start)*100.0))
            yield n
        yield n

    def queue_put(self, result):
        if self.thread is not None:
            self.queue.put(result, timeout=self.timeout)
        return result

    def runner(self, code, *args, **kwargs):
        try:
            return self.queue_put(code(*args, **kwargs))
        except Exception as e:
            self.queue_put(e)
        finally:
            self.done()

    def run_loop(self):
        for n in self.loop(3):
            for m in self.loop(2):
                print n, m
                sleep(0.2)
        return "yo {0} {1}".format(m, n)

    def _observe_abort(self, change):
        if self.abort:
            if self.busy:
                print "abort detected"

    def _observe_done(self, change):
        self.stop_thread()

    def stop_thread(self):
        print "stopping thread: "+ self.thread.name
        if self.thread is not None:
            try:
                value=self.queue.get(timeout=self.timeout)
                if isinstance(value, Exception):
                    raise value
                setattr(self, self.thread.name, value)
            finally:
                if self.thread_list!=[]:
                    self.start_thread()
                else:
                    self.busy=False
                    self.thread=None
                    self.abort=False

    #def _observe_thread_list(self, change):
    #    print change
        #if change.get("operation", None)=="append":
        #    print self.thread_list[0].is_alive()
        #    print change["item"]



    def start_thread(self):
        self.busy=True
        self.thread=self.thread_list.pop(0)
        print "starting thread: "+self.thread.name
        self.thread.start()

    def add_thread(self, name, code, *args, **kwargs):
        thread = Thread(target=self.runner, args=(code,)+args, kwargs=kwargs)#, args=(self.loop_step, 10))
        thread.name=name
        self.thread_list.append(thread)
        if self.thread is None:
            self.start_thread()
        #set_tag(self, "thread", param=name)
        #self.thread.start()
        #self.busy=True

    #def _observe_busy(self, change):
    #    print change
        #if self.st is not None:
        #    print self.st.result()

    #def _observe_b(self, change):
    #    print change
        #if self.st is not None:
        #    print self.st.result()

    #def _observe_a(self, change):
    #    if change["type"]=="update":
    #        self.busy=True
    #        if Application.instance() is not None:
    #            self.st=schedule(self.run_loop, args=(), kwargs={})
    #        else:
    #            self.run_loop()


t=Test()
#print t.run_loop()
#t.add_thread('a', t.run_loop)
#t.add_thread('b', t.run_loop)
#print t.a
#print t.b
#while t.busy:
#    pass
#print t.a
#print t.b
#print t.thread_list
#t.add_thread('b')
#print t.thread_list
#t.thread_list.pop(0)
if 0:
    t.do_it_now()
    while True:
        result=t.watch_thread()
        #print result
        if result is not None:
            break
        #sleep(0.01)
    print result
#safe_setattr(t, "a", "3")
#print t.a

from taref.core.shower import shower
shower(t)
    #def cocall(code, *args, **kwargs):
#    if Application.instance is None:
#        return code(*args, **kwargs)
#    else: