# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
#from taref.core.log import log_debug
from atom.api import Unicode, ContainerList
from taref.core.backbone import Backbone
from taref.core.atom_extension import private_property, set_log, reset_properties
from collections import OrderedDict
from taref.core.shower import shower

class Operative(Backbone):
    """Adds functionality for auto showing to Backbone"""
    name=Unicode().tag(private=True, desc="name of agent. This name will be modified to be unique, if necessary")
    desc=Unicode().tag(private=True, desc="optional description of agent")

    base_name="operative"

    def show(self, *args, **kwargs):
        shower(*((self,)+args), **kwargs)

    @classmethod
    def run_all(cls):
        """runs all functions added in run_func_dict". Can be included in cls_run_funcs"""
        for func in cls.run_func_dict.values():
            if func!=cls.run_all:
                func()

    agent_dict=OrderedDict()
    abort=False

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