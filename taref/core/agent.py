# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from taref.core.log import log_debug
from atom.api import Unicode, ContainerList, Float, Bool, Int, Typed, Instance, Event, Property, ReadOnly
from taref.core.backbone import Backbone
from taref.core.atom_extension import set_log, check_initialized, set_tag, defaulter
from taref.core.property import private_property, reset_properties
from taref.core.threadsafe import safe_setattr
from taref.core.universal import name_generator
from collections import OrderedDict
from taref.core.shower import shower
from time import time, sleep
#from enaml.application import Application
from threading import Thread
from Queue import Queue#, Empty
from numpy import linspace

class AgentError(Exception):
    """An Error for use by Operatives, Agents and Spies"""
    pass



#def name_generator(name, indict, suffix="{name}__{num}"):
#    """checks indict to see if name is in it and generates a new name based on length of indict if it is"""
#    if name in indict:
#        name="{name}__{num}".format(name=name, num=len(indict))
#    return name

class Operative(Backbone):
    """Adds functionality for auto showing to Backbone"""
    name=ReadOnly().tag(private=True, desc="Name of agent. This name will be modified to be unique, if necessary", initialized=False)

    #def _default_name(self):
    #    return self.base_name
    #def _observe_name(self, change):
    #    check_initialized(self, change)

    desc=Unicode().tag(private=True, desc="Optional description of agent")

    saving=False
    save_file=None

    base_name="operative"

    @classmethod
    def process_kwargs(cls, kwargs):
        agent=kwargs.pop(cls.base_name, None)
        if agent is None:
            return cls()
        return agent

    timeout=Float(1).tag(sub=True, desc="Timeout in seconds")

    @private_property
    def abort_timeout(self):
        return 1.0

    busy=Bool(False).tag(private=True, desc="A private Bool that represents if the agent is busy")
    progress=Int(0).tag(private=True, desc="A private Int that represents progress from 0 to 100")
    abort=Bool(False).tag(private=True, desc="A private Bool that signifies the agent wants to abort")

    thread=Typed(Thread).tag(private=True, desc="A private Typed that links to the current thread")
    queue=Instance(Queue).tag(private=True, desc="A private Instance that links to the agent's Queue")
    done=Event().tag(private=True, desc="A private Event that signifies a thread is done")
    thread_list=ContainerList().tag(private=True, desc="A private ContainerList that has the list of threads")

    def _default_queue(self):
        """queue of length one"""
        return Queue(1)

    def lins(self, start, stop, nsteps):
        """A utility generator for looping with abort and progress. Use like linspace"""
        n=start
        for n in linspace(start, stop, nsteps):
            if self.abort:
                break
            safe_setattr(self, "progress", int((n-start)/(stop-start)*100))
            yield n
        yield n

    def loop(self, start, stop=None, step=1):
        """a utility generator for looping with abort and progress. Use like range"""
        if stop is None:
            stop=start
            start=0
        n=start
        for n in range(start, stop, step):
            if self.abort:
                break
            safe_setattr(self, "progress", int((n+1.0)*step/(stop-start)*100.0))
            yield n
        yield n

    def queue_put(self, result):
        """adds result to queue if thread is active and returns result. blocks for self.timeout seconds"""
        if self.thread is not None:
            self.queue.put(result, timeout=self.abort_timeout)
        return result

    def thread_run(self, code, *args, **kwargs):
        """assisting function for running threads that passes exceptions and activates done event when finished"""
        try:
            return self.queue_put(code(*args, **kwargs))
        except Exception as e:
            self.queue_put(e)
        finally:
            self.done()

    def _observe_done(self, change):
        self.stop_thread()

    def stop_thread(self):
        """function for stopping a thread. if there are more threads in thread_list, it activates the next one.
        otherwise sets thread, abort, and busy to false"""
        print "stopping thread: "+ self.thread.name
        if self.thread is not None:
            try:
                value=self.queue.get(timeout=self.abort_timeout)
                if isinstance(value, Exception):
                    raise value
                if hasattr(self, self.thread.name):
                    setattr(self, self.thread.name, value)
            finally:
                if self.thread_list!=[]:
                    self.start_thread()
                else:
                    self.busy=False
                    self.thread=None
                    self.abort=False

    def start_thread(self):
        """starts first thread in thread_list and sets busy to true"""
        self.busy=True
        self.thread=self.thread_list.pop(0)
        print "starting thread: "+self.thread.name
        self.thread.start()

    def add_thread(self, name, code, *args, **kwargs):
        """adds a thread to thread_list and starts it if none are running"""
        thread = Thread(target=self.thread_run, args=(code,)+args, kwargs=kwargs)#, args=(self.loop_step, 10))
        thread.name=name
        self.thread_list.append(thread)
        if self.thread is None:
            self.start_thread()

    def _observe_abort(self, change):
        """observer for abort, logs abort"""
        if self.abort:
            if self.busy:
                log_debug("ABORTED: {0}".format(self.name))
        else:
            self.abort=False

    @classmethod
    def abort_all(cls):
        """attempts to abort all instruments"""
        for instr in cls.agent_dict.values():
            instr.abort=True

    def show(self, *args, **kwargs):
        """shortcut to shower which defaults to shower(self)"""
        shower(*((self,)+args), **kwargs)

    @classmethod
    def clean_up(cls):
        """Default class clean up aborts all processes and flushes class file buffer if saving"""
        cls.abort_all()
        if cls.saving:
            if hasattr(cls, "save_file"):
                cls.save_file.flush_buffers()

    @classmethod
    def run_all(cls):
        """Runs all functions added in run_func_dict". Can be included in cls_run_funcs"""
        for func in cls.run_func_dict.values():
            if func!=cls.run_all:
                func()

    @private_property
    def plots(self):
        """Dictionary of plots determined by base_name of agent being 'plot'"""
        return OrderedDict([(name, agent) for (name, agent) in self.agent_dict.iteritems() if agent.base_name=="plot"])

    @classmethod
    def get_agents(cls, *AgentTypes):
        """returns an OrderedDict of all agents in agent_dict of a particular AgentTypes.
        AgentType defaults to just type of self if no args are passed"""
        if AgentTypes is ():
            AgentTypes=(cls,) #(type(cls),)
        return OrderedDict([(name, agent) for (name, agent) in cls.agent_dict.iteritems()
                              if any(isinstance(agent, s) for s in AgentTypes)])

    agent_dict=OrderedDict()

    run_func_dict=OrderedDict()

    def add_func(self, *funcs):
        """Adds functions to run_func_dict. functions should be a classmethod, a staticmethod
        or a separate function that takes no arguments"""
        for func in funcs:
            self.run_func_dict[func.func_name]=func

    @private_property
    def cls_run_funcs(self):
        """class or static methods to include in run_func_dict on initialization. Can be overwritten in child classes"""
        return []

    @classmethod
    def activated(cls):
        """Function that runs when window is activated."""
        pass

    def __init__(self, **kwargs):
        """extends Backbone __init__ to add agent to boss's agent list
        and give unique default name."""
        agent_name=defaulter(self, "name", kwargs)
        agent_name=name_generator(agent_name, Operative.agent_dict, self.base_name)
        #if agent_name in Operative.agent_dict:
        #    agent_name="{name}__{num}".format(name=agent_name, num=len(Operative.agent_dict))
        self.name=agent_name
        Operative.agent_dict[self.name]=self
        #set_tag(self, "name", initialized=False)
        super(Operative, self).__init__(**kwargs)
        #set_tag(self, "name", initialized=True)
        self.add_func(*self.cls_run_funcs)


class Spy(Operative):
    """Spies uses observers to log all changes to params"""
    base_name="spy"

    def log_changes(self, change):
        """A simple logger for all changes and to reset properties"""
        if change["type"]!="create":
            set_log(self, change["name"], change["value"])
        if change["type"]=="update":
            reset_properties(self)

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        super(Spy, self).extra_setup(param, typer)
        self.observe(param, self.log_changes)

class Agent(Operative):
    """Agents uses primarily setattr to log changes to params"""
    base_name="agent"

    def __setattr__(self, name, value):
        """Uses __setattr__ to log changes and reset properties"""
        super(Agent, self).__setattr__(name, value)
        if name in self.all_params:
            set_log(self, name, value)
            reset_properties(self)

    def extra_setup(self, param, typer):
        """Adds observer for ContainerLists to catch changes not covered by setattr."""
        super(Agent, self).extra_setup(param, typer)
        if typer in (ContainerList,): #Dict update does not generate event so not included
            self.observe(param, self.log_changes)

    def log_changes(self, change):
        """A simple logger for changes not of type create or update that also resets properties"""
        if change["type"] not in ("create", "update"):
            set_log(self, change["name"], change["value"])
            reset_properties(self)

if __name__=="__main__":
    a=Agent(name="bob")
    b=Agent(name="bob", desc="blah")
    print b.desc
    print a.name, b.name
    print a.agent_dict
    #b.name="yoya"
    print Agent, type(a), type(a)==Agent
    b.show()