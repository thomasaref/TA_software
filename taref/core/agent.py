# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from atom.api import Unicode, ContainerList
from taref.core.chief import chief
from taref.core.backbone import Backbone, private_property
#from taref.core.log import log_debug

class SubAgent(Backbone):
    """Adds chief functionality to Backbone"""
    name=Unicode().tag(private=True, desc="name of agent. This name will be modified to be unique, if necessary")
    desc=Unicode().tag(private=True, desc="optional description of agent")

    def show(self):
        self.chief.show()

    @private_property
    def base_name(self):
        return "subagent"

    @private_property
    def chief(self):
        """gets chief of agent. can be overwritten in children classes"""
        return chief

    @property
    def abort(self):
        """shortcut to chief's abort control"""
        return self.chief.abort

#    @property #remove?
#    def default_list(self):
#        return []

    def __init__(self, **kwargs):
        """extends Backbone __init__ to add agent to boss's agent list
        and give unique default name."""
        super(SubAgent, self).__init__(**kwargs)
        agent_name=self.name
        if agent_name=="":
            agent_name=self.base_name
        if agent_name in self.chief.agent_dict:
            agent_name="{name}__{num}".format(name=agent_name, num=len(self.chief.agent_dict))
        self.name=agent_name
        self.chief.agent_dict[self.name]=self

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

