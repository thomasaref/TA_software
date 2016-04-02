# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from taref.core.log import log_debug
from atom.api import Unicode, ContainerList, Float, Bool, Int
from taref.core.backbone import Backbone
from taref.core.atom_extension import private_property, set_log, reset_properties, safe_setattr, safe_run, busy_run, tag_Callable
from collections import OrderedDict
from taref.core.shower import shower
from time import time, sleep
from enaml.application import Application
from threading import Thread

class AgentError(Exception):
    pass

class Operative(Backbone):
    """Adds functionality for auto showing to Backbone"""
    name=Unicode().tag(private=True, desc="name of agent. This name will be modified to be unique, if necessary")
    desc=Unicode().tag(private=True, desc="optional description of agent")

    saving=False
    save_file=None

    base_name="operative"

    timeout=Float(1).tag(sub=True, desc="timeout in seconds")

    @private_property
    def abort_timeout(self):
        return 600

    busy=Bool(False).tag(private=True)
    progress=Int().tag(private=True)
    abort=Bool(False).tag(private=True)

    def _observe_abort(self, change):
        """observer for abort, logs and does abort"""
        if self.abort:
            if self.busy:
                log_debug("ABORTED: {0}".format(self.name))
                self.do_it_now(self.do_abort)
            else:
                self.abort=False

    def do_abort(self):
        """thread for performing abort with timeout"""
        #safe_setattr(self, "abort", True)
        tstart=time()
        for n in range(self.abort_timeout):
            if time()>tstart+self.timeout:
                raise AgentError("Timeout while attempting to abort!")
            if not self.busy:
                break
            sleep(0.1)
        #safe_setattr(self, "abort", False)


    @classmethod
    def abort_all(cls):
        """attempts to abort all instruments, then raises any errors that occurred"""
        for instr in cls.agent_dict.values():
            instr.abort=True

    def safe_run(self, code, *args, **kwargs):
        with safe_run(self):
            code(*args, **kwargs)

    def busy_run(self, code, *args, **kwargs):
        with busy_run(self):
            code(*args, **kwargs)

    def loop(self, start, stop=None, step=1):
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

    def do_it_now(self, code, *args, **kwargs):
        if Application.instance() is None:
            self.safe_run(code, *args, **kwargs)
        else:
            thread = Thread(target=self.safe_run, args=(code,)+args, kwargs=kwargs)
            thread.start()

    def do_it_busy(self, code, *args, **kwargs):
        if Application.instance() is None:
            self.busy_run(code, *args, **kwargs)
        else:
            thread = Thread(target=self.busy_run, args=(code,)+args, kwargs=kwargs)
            thread.start()

    def show(self, *args, **kwargs):
        """shortcut to shower which defaults to shower(self)"""
        shower(*((self,)+args), **kwargs)

    @classmethod
    def clean_up(cls):
        """default class clean up aborts all processes and flushes class file buffer if saving"""
        cls.abort_all()
        if cls.saving:
            if hasattr(cls, "save_file"):
                cls.save_file.flush_buffers()

    @classmethod
    def run_all(cls):
        """runs all functions added in run_func_dict". Can be included in cls_run_funcs"""
        for func in cls.run_func_dict.values():
            if func!=cls.run_all:
                func()

    @private_property
    def plots(self):
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
        """adds functions to run_func_dict. functions should be a classmethod, a staticmethod
        or a separate function that takes no arguments"""
        for func in funcs:
            self.run_func_dict[func.func_name]=func

    @private_property
    def cls_run_funcs(self):
        """class or static methods to include in run_func_dict on initialization. Can be overwritten in child classes"""
        return []

    @classmethod
    def activated(cls):
        """function that runs when window is activated"""
        pass

    def __init__(self, **kwargs):
        """extends Backbone __init__ to add agent to boss's agent list
        and give unique default name."""
        super(Operative, self).__init__(**kwargs)
        agent_name=self.name
        if agent_name=="":
            agent_name=self.base_name
        if agent_name in Operative.agent_dict:
            agent_name="{name}__{num}".format(name=agent_name, num=len(Operative.agent_dict))
        self.name=agent_name
        Operative.agent_dict[self.name]=self
        self.add_func(*self.cls_run_funcs)


class Spy(Operative):
    """Spies uses observers to log all changes to params"""
    base_name="spy"

    def log_changes(self, change):
        """a simple logger for all changes and to reset properties"""
        if change["type"]!="create":
            set_log(self, change["name"], change["value"])
        if change["type"]=="update":
            reset_properties(self)

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        super(Spy, self).extra_setup(param, typer)
        self.observe(param, self.log_changes)

class Agent(Operative):
    """Agents use primarily setattr to log changes to params"""
    base_name="agent"

    def __setattr__(self, name, value):
        """uses __setattr__ to log changes and reset properties"""
        super(Agent, self).__setattr__(name, value)
        if name in self.all_params:
            set_log(self, name, value)
            reset_properties(self)

    def extra_setup(self, param, typer):
        """adds observer for ContainerLists to catch changes not covered by setattr.
        extra_setup goes from Spy, not Agent to not add observers"""
        super(Agent, self).extra_setup(param, typer)
        if typer in (ContainerList,): #Dict update does not generate event so not included
            self.observe(param, self.log_changes)

    def log_changes(self, change):
        """a simple logger for changes not of type create or update that also resets properties"""
        if change["type"] not in ("create", "update"):
            set_log(self, change["name"], change["value"])
            reset_properties(self)

if __name__=="__main__":
    a=Agent()
    print Agent, type(a), type(a)==Agent