# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from atom.api import Unicode, Bool, Enum, List, Float, Int, ContainerList, Callable, Range, FloatRange

#from a_Chief import show
from a_Backbone import (get_all_params, get_type, obackbone, Backbone,
                        lowhigh_check, set_log, get_tag, set_tag, unit_dict, log_func)

    
def list_recursion(mylist, index=0):
    """a test of list recursion"""
    item=mylist[index]
    print index, item
    if isinstance(item, list):
        return list_recursion(item)
    return

from a_Chief import boss

class oagent(obackbone):
    @property
    def boss(self):
        """returns boss singleton instance. can be overwritten in subclasses to change boss"""
        return boss

    @property
    def abort(self):
        """shortcut to boss' abort control"""
        return self.boss.abort

class SubAgent(Backbone):
    """under class that adds boss functionalities to Backbone"""
    @property
    def boss(self):
        """returns boss singleton instance. can be overwritten in subclasses to change boss"""
        return boss

    @property
    def abort(self):
        """shortcut to boss' abort control"""
        return self.boss.abort
       
    def data_save(self, name, value):
        """shortcut to data saving"""
        self.boss.data_save(self, name, value)
 
       

#    def draw_plot(self):
#        """shortcut to plotting"""
#        self.boss.draw_plot(self)
#
    def show(self):
        """shortcut to showing"""
        self.boss.show(agent=self)

    def extra_setup(self, param, typer):
        """do nothing function to allow custom setup extension in subclasses"""
        pass

    def __init__(self, **kwargs):
        """extends __init__ to set boss and add instrument to boss's instrument list.
        Also adds observers for ContainerList parameters so if item in list is changed via some list function other than setattr, notification is still given.
        Finally, sets all Callables to be log decorated if they weren't already."""
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
        self.observe(param, self.log_changes)
        
        
class Agent(SubAgent):
    """uses __setattr__ to log changes except for ContainerList"""
    def __setattr__(self, name, value):
        log_it=False
        if name in get_all_params(self):
            log_it=True
            value=lowhigh_check(self, name, value)            
        super(Agent, self).__setattr__(name, value)
        if log_it:
            set_log(self, name, value)

    def extra_setup(self, param, typer):
        if typer==ContainerList:
            self.observe(param, self.log_changes)

if __name__=="__main__":
    from a_Backbone import run_func, log_func

    class tSpy(Spy):
        a=Float().tag(unit="A", unit_factor=10.0, label="Current", no_spacer=True, show_value=True)
        b=Unicode()
        c=Unicode().tag( no_spacer=True, spec="multiline")
        d=Int().tag(unit="A", unit_factor=10, label="Current",show_value=True)
        e=Enum("arg")   
        
        @Callable      
        def g(self):
            print self, a
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


