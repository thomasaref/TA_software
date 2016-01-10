# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from atom.api import Unicode, Enum, Float, Int, ContainerList, Callable
from taref.core.chief import chief
from taref.core.backbone import Backbone, private_property
from taref.core.log import log_debug
   
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

    @property #remove?
    def default_list(self):
        return []
        
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
            log_debug("log changes")
            self.set_log(change["name"], change["value"])
        if change["type"]=="update":
            self.reset_properties()
            #self.do_update(change["name"])

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        super(Spy, self).extra_setup(param, typer)
        self.observe(param, self.log_changes)

    @property
    def base_name(self):
        return "spy"


class Agent(Spy):
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
        super(Spy, self).extra_setup(param, typer)
        if typer==ContainerList:
            self.observe(param, self.log_changes)

    @property
    def base_name(self):
        return "agent"


if __name__=="__main__":
    from a_Backbone import run_func, log_func
    c=SubAgent()
    print c.view, c.main_params, c.base_name, c.all_params, c.all_main_params, c.reserved_names

    class tSpy(Spy):
        a=Float().tag(unit="A", unit_factor=10.0, label="Current", no_spacer=True, show_value=True)
        b=Unicode()
        c=Unicode().tag( no_spacer=True, spec="multiline")
        d=Int().tag(unit="A", unit_factor=10, label="Current",show_value=True)
        e=Enum("arg")

        @Callable
        def g(self):
            print self
            print "ran g"

    d=tSpy()
    d.a=4.3
    d.a=3.2
    #d.g(d)

    #run_func(d, "g")
    d.show()#show(d)
#    class test(object):
#        b=4
#        c=2
#
#        #@property
#        def f(self):
#            return 7
#        f.metadata=dict(mapping={7:1})
#
#
#    a=test()
#    print members(a)
#    print get_member(a, "c")
#    print get_metadata(a, "c")
#    metadata=get_metadata(a, "c")
#    metadata.update(money="power", foo="bar")
#    print get_metadata(a, "c")
#    print get_tag(a, "c", "h", True)
#    print get_map(a, "c", {2:3})
#    print get_map(a, "f")
#
#    print list_recursion([[["a", "d"],[ 1,2]], "b", "c"])
#
#    from atom.api import Int, observe, Coerced, Typed, Instance
#
#    class test(Atom):
#        a=Int().tag(money="time")
#        b=Int()
#        #c=Coerced(float, coercer=int)
#        c=Instance(float, ())
##        Instance
#
#        def _observe_a(self, change):
#            print change
#
#        def _observe_b(self, change):
#            print change
#
#        @observe('a')
#        @updater
#        def update_b(self, change):
#            self.b=self.a+1
#
#        @observe('b')
#        @updater
#        def update_a(self, change):
#            self.a=self.b+1

    #a=test()
    #print get_metadata(a, "a")
    #Coerced type get_member.validate_mode[1][1]
    #print get_member(a, "c").validate_mode
    #print
    #a.a=4
    #a.a=9
    #a.b=3


