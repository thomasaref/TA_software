# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from atom.api import Unicode, ContainerList
#from taref.core.chief import Chief
from taref.core.backbone import Backbone, private_property
#from taref.core.log import log_debug
from collections import OrderedDict
from taref.core.shower import shower


def func_dict(*funcs):
    #return OrderedDict(zip([func.func_name for func in funcs], [func for func in funcs]))

    return OrderedDict(zip([func.__func__.func_name for func in funcs], [func.__func__ for func in funcs]))

class SubAgent(Backbone):
    """Adds chief functionality to Backbone"""
    name=Unicode().tag(private=True, desc="name of agent. This name will be modified to be unique, if necessary")
    desc=Unicode().tag(private=True, desc="optional description of agent")

    def show(self):
        shower(self)
        #self.chief.show()

    base_name="subagent"
#    @private_property
#    def base_name(self):
#        return "subagent"

    @classmethod
    def run_all(cls):
        """runs all functions added in run_func_dict". Can be included in cls_run_funcs"""
        for func in cls.run_func_dict.values():
            if func!=cls.run_all:
                func()

    agent_dict=OrderedDict()
    abort=False

#    @property
#    def agents(self):
#        """returns list of agents"""
#        return self.agent_dict.values()
#
#    @private_property
#    def agent_names(self):
#        """returns list of agent names"""
#        return self.agent_dict.keys()
#    @private_property
#    def chief(self):
#        """gets chief of agent. can be overwritten in children classes"""
#        return chief

    #chief=Chief()

    #@property
    #def abort(self):
    #    """shortcut to chief's abort control"""
    #    return self.chief.abort

    run_func_dict=OrderedDict()

    def add_func(self, *funcs):
        """adds functions to run_func_dict. functions should be a classmethod, a staticmethod or a separate take no arguments function"""
        for func in funcs:
            self.run_func_dict[func.func_name]=func

    @property
    def cls_run_funcs(self):
        """class functions to include in run_func_dict on initialization. Can be overwritten in child classes"""
        return []

#    @private_property
#    def run_funcs(self):
#        return self.run_func_dict.values()
#
#    @private_property
#    def run_func_names(self):
#        return self.run_func_dict.keys()
    #def add_func(self, func):
    #    self.chief.add_func(func)

    #def full_run(self):
    #    self.chief.full_run()

    @classmethod
    def activated(cls):
        """what to do when window is activated"""
        pass

    def __init__(self, **kwargs):
        """extends Backbone __init__ to add agent to boss's agent list
        and give unique default name."""
        super(SubAgent, self).__init__(**kwargs)
        agent_name=self.name
        if agent_name=="":
            agent_name=self.base_name
        if agent_name in self.agent_dict:
            agent_name="{name}__{num}".format(name=agent_name, num=len(self.agent_dict))
        self.name=agent_name
        self.agent_dict[self.name]=self
        self.add_func(*self.cls_run_funcs)

class Spy(SubAgent):
    """Spies uses observers to log all changes to params"""
    def log_changes(self, change):
        """a simple logger for all changes"""
        if change["type"]!="create":
            self.set_log(change["name"], change["value"])
        if change["type"]=="update":
            self.reset_properties()

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        super(Spy, self).extra_setup(param, typer)
        self.observe(param, self.log_changes)

    @private_property
    def base_name(self):
        return "spy"


class Agent(SubAgent):
    """Agents use setattr to log changes to params"""
    def __setattr__(self, name, value):
        """uses __setattr__ to log changes except for observers on ContainerList"""
        super(Agent, self).__setattr__(name, value)
        if name in self.all_params:
            self.set_log(name, value)
            self.reset_properties()

    def extra_setup(self, param, typer):
        """adds observer for ContainerLists to catch changes not covered by setattr.
        extra_setup goes from Spy, not Agent to not add observers"""
        super(Agent, self).extra_setup(param, typer)
        if typer in (ContainerList,): #Dict update does not generate event so not included
            self.observe(param, self.log_changes)

    def log_changes(self, change):
        """a simple logger for all changes"""
        if change["type"] not in ("create", "update"):
            self.set_log(change["name"], change["value"])
            self.reset_properties()

    @private_property
    def base_name(self):
        return "agent"

