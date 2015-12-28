# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from atom.api import Unicode, Enum, Float, Int, ContainerList, Callable, Bool, List
from taref.core.chief import chief
from taref.core.backbone import Backbone, log_func, _UPDATE_PREFIX_, get_attr

from functools import wraps
from taref.core.log import log_debug
from inspect import getmembers
from collections import OrderedDict
#def func(f):
#    #f=fn.im_func
#    argcount=f.func_code.co_argcount
#    argnames=list(f.func_code.co_varnames[0:argcount])
#    if "self" in argnames:
#        argnames.remove("self")
#    f.argnames=argnames
#    return f
#
#    #    for name in argnames:
#    #            upd_list=self.get_tag(name, "update", [])
#    #            if name not in upd_list:
#    #                upd_list.append(param+"_func")
#    #                self.set_tag(name, update=upd_list)
#
#def updates(fn):
#    """a decorator to stop infinite recursion. also stores run_params as an attribute"""
#    @wraps(fn)
#    def updfunc(change):
#        if not hasattr(updfunc, "callblock"):
#            updfunc.callblock=""
#        if change["name"]!=updfunc.callblock: # and change['type']!='create':
#            log_debug(change)
#
#            updfunc.callblock=change["name"]
#            fn(change)
#            updfunc.callblock=""
#    updfunc.run_params=get_run_params(fn)
#    return updfunc

   
class SubAgent(Backbone):
    """Adds chief functionality to Backbone"""
    name=Unicode().tag(private=True, desc="name of agent. A default will be provided if none is given")
    desc=Unicode().tag(private=True, desc="optional description of agent")
    
#    def get_update_list(self):
#        return [attr[0] for attr in getmembers(self) if attr[0].startswith(_UPDATE_PREFIX_)]
        
    def show(self):
        self.chief.show()

    def extra_setup(self, param, typer):
        """Can be overwritten to allow custom setup extension in subclasses"""
        self.es_log_callables(param, typer)
        #self.es_funcs(param, typer)
        
#    def es_funcs(self, param, typer):
#        if hasattr(self, param+"_func"):
#            f=getattr(self, param+"_func").im_func
#            argcount=f.func_code.co_argcount
#            argnames=list(f.func_code.co_varnames[0:argcount])
#            if "self" in argnames:
#                argnames.remove("self")
#            f.argnames=argnames
#            for name in argnames:
#                upd_list=self.get_tag(name, "update", [])
#                if name not in upd_list:
#                    upd_list.append(param+"_func")
#                    self.set_tag(name, update=upd_list)
#                    
#                    

#
#            #@updates
#            def _updat_(change):
#                if param not in updated:
#                    log_debug(change)
#                    log_debug(updated)
#
#                    kwargs=dict(zip(argnames, [getattr(self, arg) for arg in argnames]))
#                    #with self.suppress_notifications():
#                    updated.append(param)
#                    setattr(self, param, getattr(self, param+"_func")(**kwargs))
#                    updated.remove(param)
#                    
#            #def _param_update(change):
#                                    
#            self.observe(argnames, _updat_)
#            for arg in argnames:
#                kwargs={}
#                for arg in argnames:
#                    kwargs[arg]=getattr(self, arg)
#            setattr(self, param, getattr(self, param+"_func")(**kwargs))
        
    def es_log_callables(self, param, typer):
        """extra setup function that autosets Callables to be logged"""
        if typer==Callable:
            func=getattr(self, param)
            setattr(self, param, log_func(func))
        
    @property
    def base_name(self):
        return "subagent"

    @property
    def chief(self):
        """gets chief of agent. can be overwritten in children classes"""
        return chief

    @property
    def abort(self):
        """shortcut to chief's abort control"""
        return self.chief.abort

    @property
    def default_list(self):
        return []
        
    def __init__(self, **kwargs):
        """extends Backbone __init__ to add agent to boss's agent list
        and give unique default name."""
        super(SubAgent, self).__init__(**kwargs)
        if "name" not in kwargs:
            self.name="{basename}__{basenum}".format(basename=self.base_name, basenum=len(self.chief.agents))
        self.chief.agents.append(self)
        updates=[attr[0] for attr in getmembers(self) if attr[0].startswith(_UPDATE_PREFIX_)]
        for update_func in updates:
            f=getattr(self, update_func).im_func
            argcount=f.func_code.co_argcount
            argnames=list(f.func_code.co_varnames[0:argcount])
            if "self" in argnames:
                argnames.remove("self")
            f.argnames=argnames
            for name in argnames:
                upd_list=self.get_tag(name, "update", [])
                if update_func not in upd_list:
                    upd_list.append(update_func)
                    self.set_tag(name, update=upd_list)
        log_debug(self.default_list)                    
        for param in self.default_list:
            if param not in kwargs and not hasattr(self, "_default_"+param) and hasattr(self, "_update_"+param):
                setattr(self, param, self.get_default(param))
            else:
                setattr(self, param, getattr(self, param))
                    
class Spy(SubAgent):
    updating=Bool(True).tag(private=True)
        
    """Spy uses observers to log all changes"""
    def __setattr__(self, name, value):
        """setattr performs low/high check"""
        if name in self.all_params:
            value=self.lowhigh_check(name, value)
        super(Spy, self).__setattr__(name, value)
        
    def log_changes(self, change):
        """a simple logger for all changes"""
        if change["type"]!="create":
            log_debug("log changes")
            self.set_log(change["name"], change["value"])
            self.do_update(change["name"])
            
    def do_update(self, name):
        log_debug(name)
        if self.updating:
            self.updating=False
            results=self.search_update(name)
            for key in results:
                if key!=name:
                    setattr(self, key, results[key])
            self.updating=True

    def search_update(self, param, results=None):
        if results is None:
            results=OrderedDict()
            results[param]=getattr(self, param)
        for update_func in self.get_tag(param, "update", []):
            param=update_func.split("_update_")[1]
            if not param in results.keys():
                argnames=get_attr(getattr(self, update_func).im_func, "argnames")
                if argnames is not None:
                    argvalues= [results.get(arg, getattr(self, arg)) for arg in argnames]
                    kwargs=dict(zip(argnames,argvalues))
                    result=getattr(self, update_func)(**kwargs)
                    results[param]=result
                    self.search_update(param, results)
        return results

    def get_default(self, name, update_func=None):
        if update_func is None:
            update_func="_update_"+name
        argnames=getattr(self, update_func).im_func.argnames
        argvalues= [getattr(self, arg) for arg in argnames]
        kwargs=dict(zip(argnames,argvalues))
        return getattr(self, update_func)(**kwargs)

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        self.observe(param, self.log_changes)
        self.es_log_callables(param, typer)
        #if self.get_tag(param, "default", False)==True:
        #    setattr(self, param, self.get_default(param))
        #self.es_funcs(param, typer)

    @property
    def base_name(self):
        return "spy"


class Agent(Spy):
    """Agents use setattr rather than observers to log all changes"""
    def __setattr__(self, name, value):
        """uses __setattr__ to log changes except for ContainerList"""
        log_it=False
        if name in self.all_params:
            log_it=True
            value=self.lowhigh_check(name, value)
        super(Agent, self).__setattr__(name, value)
        if log_it:
            self.set_log(name, value)
            self.do_update(name)

#    def update_logger(self, name):
#        self.update_list.append(name)
#        log_debug((name, self.update_list))
#        for update_func in self.get_tag(name, "update", []):
#            param=update_func.split("_")[2]
#            if param not in self.update_list:
#                argnames=getattr(self, update_func).im_func.argnames
#                kwargs=dict(zip(argnames, [getattr(self, arg) for arg in argnames]))
#                setattr(self, param, getattr(self, update_func)(**kwargs))
#        self.update_list.remove(name)
#        log_debug((name, self.update_list))

    def extra_setup(self, param, typer):
        """adds observer for ContainerLists to catch changes not covered by setattr"""
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


