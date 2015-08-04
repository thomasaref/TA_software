# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from atom.api import Atom, Unicode, Bool, Enum, List, Float, Int, ContainerList, Callable, Range, FloatRange
from a_Backbone import (get_all_params, get_type, get_reserved_names, get_all_main_params, get_map, 
                        lowhigh_check, set_log, get_tag, set_tag, unit_dict, log_func)
from a_Chief import chief

class Backbone(Atom):
    main_params=List().tag(private=True, desc="main parameters: allows control over what is displayed and in what order")

    def get_metadata(self, name):
        """returns the metadata of a member if it exists and sets it to a blank dictionary if it does not"""
        member=self.get_member(name)
        if member.metadata is None:
            member.metadata={}
        return member.metadata

    def set_tag(self, name, **kwargs):
        """sets the tag of a member using Atom's built in tag functionality"""
        member=self.get_member(name)
        member.tag(**kwargs)

    def set_all_tags(self, **kwargs):
        """set all parameters tags using keyword arguments"""
        for param in get_all_params(self):
            self.set_tag(param, **kwargs)

    def get_tag(self, name, key, none_value=None):
        """returns the tag key of a member name an returns none_value if it does not exist"""
        metadata=self.get_metadata(name)
        return metadata.get(key, none_value)

    def get_all_tags(self, key, key_value=None, none_value=None, search_list=None):
        """returns a list of names of parameters with a certain key_value"""
        if search_list is None:
            search_list=self.members()
        if key_value==None:
            return [x for x in search_list if none_value!=self.get_tag(x, key, none_value)]
        return [x for x in search_list if key_value==self.get_tag(x, key, none_value)]

    def get_type(self, name):
        """returns type of member with given name, with possible override via tag typer"""
        typer=type(self.get_member(name))
        return self.get_tag(name, "typer", typer)

    @property
    def reserved_names(self):
       """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
       return self.get_all_tags("private", True)

    @property
    def all_params(self):
        """all members that are not tagged as private, i.e. not in reserved_names and will behave as agents"""
        return self.get_all_tags(key="private", key_value=False, none_value=False)
    
    @property
    def all_main_params(self):
        """all members in all_params that are not tagged as sub.
        Convenience function for more easily custom defining main_params in child classes"""
        return self.get_all_tags('sub', False, False, self.all_params)

    def _default_main_params(self):
        """defaults to all members in all_params that are not tagged as sub.
        Can be overwritten to allow some minimal custom layout control,
        e.g. order of presentation and which members are shown. Use get_all_main_params to get a list of
        all members that could be in main_params"""
        return self.all_main_params

class SubAgent(Atom):
    name=Unicode().tag(private=True, desc="name of agent. A default will be provided if none is given")
    desc=Unicode().tag(private=True, desc="optional description of agent")
    main_params=List().tag(private=True, desc="main parameters: allows control over what is displayed and in what order")

    def _default_main_params(self):
        """defaults to all members in all_params that are not tagged as sub.
        Can be overwritten to allow some minimal custom layout control,
        e.g. order of presentation and which members are shown. Use get_all_main_params to get a list of
        all members that could be in main_params"""
        return get_all_main_params(self)
        
    def show(self):
        self.chief.show()

    def extra_setup(self, param, typer):
        """do nothing function to allow custom setup extension in subclasses"""
        pass

    def get_map(self, name, item=None, none_map={}):
        return get_map(self, name=name, item=item, none_map=none_map)

    @property
    def base_name(self):
        return "subagent"#, basenum=len(self.chief.agents))
    
    @property
    def chief(self):
        """gets chief of agent. can be overwritten in children classes"""
        return chief

    @property
    def abort(self):
        """shortcut to chief's abort control"""
        return self.chief.abort
        
    def __init__(self, **kwargs):
        """extends __init__ to set boss, add agent to boss's agent list and give unique default name.
        does some extra setup for particular types"""
        #self.boss.make_boss()
        super(SubAgent, self).__init__(**kwargs)
        if "name" not in kwargs:
            self.name="{basename}__{basenum}".format(basename=self.base_name, basenum=len(self.chief.agents))
        self.chief.agents.append(self)
        for param in get_all_params(self):
            typer=get_type(self, param)
            if typer in [Range, FloatRange]:
                """autosets low/high tags for Range and FloatRange"""
                set_tag(self, param, low=self.get_member(param).validate_mode[1][0], high=self.get_member(param).validate_mode[1][1])
            if typer in [Int, Float, Range, FloatRange]:
                """autosets units for Ints and Floats"""
                if get_tag(self, param, "unit", False) and (get_tag(self, param, "unit_factor") is None):
                    unit=get_tag(self, param, "unit", "")[0]
                    if unit in unit_dict:
                        unit_factor=get_tag(self, param, "unit_factor", unit_dict[unit])
                        set_tag(self, param, unit_factor=unit_factor)
            elif typer==Callable:
                """autosets Callables to be logged"""
                func=getattr(self, param)
                setattr(self, param, log_func(func))
            self.extra_setup(param, typer)
 
class Spy(SubAgent):
    """uses observers to log all changes"""
    def __setattr__(self, name, value):
        """setattr performs low/high check"""
        if name in get_all_params(self):
            value=lowhigh_check(self, name, value)            
        super(Spy, self).__setattr__(name, value)

    def log_changes(self, change):
        """a simple logger for all changes"""
        set_log(self, change["name"], change["value"])

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        self.observe(param, self.log_changes)
        
class Agent(Spy):
    """Agents use setattr rather than observers to log all changes"""
    def __setattr__(self, name, value):
        """uses __setattr__ to log changes except for ContainerList"""
        log_it=False
        if name in get_all_params(self):
            log_it=True
            value=lowhigh_check(self, name, value)            
        super(Agent, self).__setattr__(name, value)
        if log_it:
            set_log(self, name, value)

    def extra_setup(self, param, typer):
        """adds observer for ContainerLists to catch changes not covered by setattr"""
        if typer==ContainerList:
            self.observe(param, self.log_changes)



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


