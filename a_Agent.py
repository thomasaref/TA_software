# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from atom.api import Atom, Unicode, Bool, Enum, List, Float, Int, ContainerList, Callable, Range, FloatRange
from a_Backbone import (get_all_params, get_type, get_reserved_names, get_all_main_params, get_map, set_all_tags, 
                        lowhigh_check, set_log, get_tag, set_tag, unit_dict, log_func)
from a_Chief import boss

from enaml import imports

class aAtom(Atom):
    name=Unicode()

    @property       
    def viewprop(self):
        with imports():
            from e_UserTemps import TextEditorWindow
        return TextEditorWindow
        

class sAgent(Atom):
    name=Unicode().tag(private=True, desc="name of agent. A default will be provided if none is given")

    def show(self):
        self.chief.show()

    def extra_setup(self, param, typer):
        """do nothing function to allow custom setup extension in subclasses"""
        pass

    def get_map(self, name, item=None, none_map={}):
        return get_map(self, name=name, item=item, none_map=none_map)

    @property
    def base_name(self):
        return "sagent"#, basenum=len(self.chief.agents))
    
    @property
    def chief(self):
        return boss
        
    def __init__(self, **kwargs):
        """extends __init__ to set boss, add agent to boss's agent list and give unique default name.
        does some extra setup for particular types"""
        #self.boss.make_boss()
        super(sAgent, self).__init__(**kwargs)
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
                if get_tag(self, param, "unit", False) and get_tag(self, param, "unit_factor", True):
                    unit=get_tag(self, param, "unit", "")[0]
                    if unit in unit_dict:
                        set_tag(self, param, unit_factor=unit_dict[unit])
            elif typer==Callable:
                """autosets Callables to be logged"""
                func=getattr(self, param)
                setattr(self, param, log_func(func))
            self.extra_setup(param, typer)
        
class SubAgent(Atom):
    """Underlying class that implements all universal aspects and adds boss functionalities"""
    name=Unicode().tag(private=True, desc="name of agent. A default will be provided if none is given")
    desc=Unicode().tag(private=True, desc="optional description of agent")
    full_interface=Bool(False).tag(private=True, desc="agent wide GUI control")
    plot_all=Bool(False).tag(private=True, desc="agent wide override for plotting")
    view=Enum("Auto").tag(private=True, desc="can be overwritten in children to allow custom views")
    main_params=List().tag(private=True, desc="main parameters: allows control over what is displayed and in what order")

    @property
    def boss(self):
        """returns boss singleton instance. can be overwritten in subclasses to change boss"""
        return boss

    @property
    def abort(self):
        """shortcut to boss' abort control"""
        return self.boss.abort
       
    def data_save(self, name, value):
        """shortcut to boss' data saving"""
        self.boss.data_save(self, name, value)
 
#    def draw_plot(self):
#        """shortcut to plotting"""
#        self.boss.draw_plot(self)
#
    def show(self):
        """shortcut to show"""
        self.boss.show(agent=self)

    @property
    def base_name(self):
        """default base name of base if no name is given. can be overwritten in subclasses"""
        return "base"

    @property
    def reserved_names(self):
        """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
        return get_reserved_names(self) #get_all_tags("private", True)

    @property
    def all_params(self):
        """all params to perform logging and display operations on"""
        return get_all_params(self)

    @property
    def all_main_params(self):
        """all_params that are not tagged as sub"""
        return get_all_main_params(self)

    def _default_main_params(self):
        """defaults to all members in all_params that are not tagged as sub.
        Can be overwritten to allow some minimal custom layout control,
        e.g. order of presentation and which members are shown. Use self.all_main_params to get a list of
        all members that could be in main_params"""
        return self.all_main_params

    def get_map(self, name, item=None, none_map={}):
        return get_map(self, name=name, item=item, none_map=none_map)
        
    def run_func(self, name, **kwargs):
        return run_func(self, name, **kwargs)
#
#    def func2log(self, name, cmdstr):
#        """returns cmd associated with cmdstr in tag and converts it to a log if it isn't already.
#          returns None if cmdstr is not in metadata"""
#        cmd=self.get_tag(name, cmdstr)
#        if not isinstance(cmd, func_log) and cmd is not None:
#            cmd=func_log(cmd)
#            self.set_tag(name, **{cmdstr:cmd})
#        return cmd
#
#    def get_run_params(self, name, key, notself=False, none_value=[]):
#        """returns the run parameters of get_cmd and set_cmd. Used in GUI"""
#        cmd=self.func2log(name, key)
#        if cmd is None:
#            return none_value
#        else:
#            run_params=cmd.run_params[:]
#            if notself:
#                if name in run_params:
#                    run_params.remove(name)
#            return run_params
#
    def _observe_plot_all(self, change):
        """if instrument plot_all changes, change all plot tags of parameters"""
        if change['type']!='create':
            set_all_tags(self, plot=self.plot_all)

    def _observe_full_interface(self, change):
        """if instrument full_interface changes, change all full_interface tags of parameters"""
        if change['type']!='create':
            self.set_all_tags(full_interface=self.full_interface)


    def extra_setup(self, param, typer):
        """do nothing function to allow custom setup extension in subclasses"""
        pass

    def __init__(self, **kwargs):
        """extends __init__ to set boss, add agent to boss's agent list and give unique default name.
        does some extra setup for particular types"""
        self.boss.make_boss()
        super(SubAgent, self).__init__(**kwargs)
        if "name" not in kwargs:
            self.name= "{basename}__{basenum}".format(basename=self.base_name, basenum=len(self.boss.agents))
        self.boss.agents.append(self)
        for param in get_all_params(self):
            typer=get_type(self, param)
            if typer in [Range, FloatRange]:
                """autosets low/high tags for Range and FloatRange"""
                set_tag(self, param, low=self.get_member(param).validate_mode[1][0], high=self.get_member(param).validate_mode[1][1])
            if typer in [Int, Float, Range, FloatRange]:
                """autosets units for Ints and Floats"""
                if get_tag(self, param, "unit", False) and get_tag(self, param, "unit_factor", True):
                    unit=get_tag(self, param, "unit", "")[0]
                    if unit in unit_dict:
                        set_tag(self, param, unit_factor=unit_dict[unit])
            elif typer==Callable:
                """autosets Callables to be logged"""
                func=getattr(self, param)
                setattr(self, param, log_func(func))
            self.extra_setup(param, typer)
 
class Spy(SubAgent):
    """uses observers to log all changes"""
    def __setattr__(self, name, value):
        if name in get_all_params(self):
            value=lowhigh_check(self, name, value)            
        super(Spy, self).__setattr__(name, value)

    def log_changes(self, change):
        """a simple logger for all changes"""
        set_log(self, change["name"], change["value"])

    def extra_setup(self, param, typer):
        """adds observers to all params"""
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

class osubagent(object):
    """a non-atom convenience subagent class"""
    name="" 
    title= ""
    desc= ""
    full_interface=False 
    plot_all=False 
    view="Auto" 

    @property
    def base_name(self):
        """default base name of base if no name is given. can be overwritten in subclasses"""
        return "base"

    @property
    def reserved_names(self):
        """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
        return get_reserved_names(self) #get_all_tags("private", True)

    @property
    def all_params(self):
        """all params to perform logging and display operations on"""
        return get_all_params(self)

    @property
    def all_main_params(self):
        """all_params that are not tagged as sub"""
        return get_all_main_params(self)
    @property
    def main_params(self):
        """defaults to all members in all_params that are not tagged as sub.
        Can be overwritten to allow some minimal custom layout control,
        e.g. order of presentation and which members are shown. Use self.all_main_params to get a list of
        all members that could be in main_params"""
        return self.all_main_params 

    @property
    def boss(self):
        """returns boss singleton instance. can be overwritten in subclasses to change boss"""
        return boss

    @property
    def abort(self):
        """shortcut to boss' abort control"""
        return self.boss.abort

class oagent(osubagent):
    """uses setattr to log"""
    def __setattr__(self, name, value):
        log_it=False
        if name in get_all_params(self):
            log_it=True
            value=lowhigh_check(self, name, value)            
        super(oagent, self).__setattr__(name, value)
        if log_it:
            set_log(self, name, value)

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


