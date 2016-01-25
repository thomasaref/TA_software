# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 00:48:41 2016

@author: thomasaref
"""

from taref.core.atom_extension import get_tag, make_instancemethod, get_run_params, get_all_params
from atom.api import Atom, Callable, Property, Int
from taref.core.log import log_debug

from functools import wraps

def get_property_names(obj):
    if hasattr(obj, "property_dict"):
        return obj.property_dict.keys()
    return [name for name in get_all_params(obj) if isinstance(obj.get_member(name), Property)]

def log_func(func):
    name=func.func_name
    @wraps(func)
    def new_func(self, *args, **kwargs):
        """logs the call of an instance method and autoinserts kwargs"""
        if get_tag(self, name, "log", False):
            log_debug("RAN: {}".format(name), n=1)
        if len(args)==0:
            members=self.members()
            for param in get_run_params(new_func):
                if param in members:
                    if param in kwargs:
                        try:
                            setattr(self, param, kwargs[param])
                        except TypeError:
                            pass
                    else:
                        if param in get_property_names(self):
                            self.get_member(param).reset(self)
                        value=getattr(self, param)
                        #value=set_value_map(obj, param, value)
                        kwargs[param]=value
        #if hasattr(obj, "chief"): #not working. how to get return value?
        #    objargs=(obj,)+args
        #    return_value=do_it_if_needed(obj.chief, self.func, *objargs, **kwargs)
        #else:
        return func(self, *args, **kwargs)
    new_func.run_params=get_run_params(func)
    return new_func
    
class Test(Atom):
    a=Int()
    @Callable
    def new_func(self):
        print "ok"
        
    @Callable
    def old_func(self):
        print self

    def instancemethod(self, func):
        #if get_tag(self, func.func_name, "log", True):
        func=log_func(func)
        make_instancemethod(self, func)
        return func
            
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        for name in self.members():
            if isinstance(self.get_member(name),Callable):
                func=getattr(self, name)
                if func is not None:
                    self.instancemethod(func)
class instancemethod(object):
    def __init__(self, obj):
        self.obj=obj
    
    def __call__(self, func):
        #if get_tag(self.obj, func.func_name, "log", True):
        func=log_func(func)
        make_instancemethod(self.obj, func)
        return func
        
t=Test()
t2=Test()
t.get_member("a").tag(log=True)
print t.get_member("a").metadata
print t2.get_member("a").metadata

from types import MethodType

@instancemethod(t)
def new_func(obj):
    print obj
print globals()
new_func(t2) 
t2.new_func()
t.new_func()   
print isinstance(new_func, MethodType)
print isinstance(t.new_func, MethodType)

#make_instancemethod(t, new_func)

from taref.core.shower import shower
shower(t, t2)