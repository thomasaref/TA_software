# -*- coding: utf-8 -*-
"""
Created on Tue May  3 13:52:33 2016

@author: thomasaref
"""
from taref.core.api import get_run_params
from functools import wraps
from atom.api import Property, Atom, Callable, Float, AtomMeta

def property_func(func):
    name_list=func.func_name.split("_get_")
    if name_list[0]=="":
        name=name_list[1]
    else:
        name=name_list[0]
    new_func=log_func(func, name)
    new_func.fset_list=[]
    def setter(set_func):
        s_func=property_func(set_func)
        new_func.fset_list.append(s_func)
        return s_func
    new_func.setter=setter
    return new_func


def param_decider(obj, value, param, pname):
    if param==pname:
        return value
    return getattr(obj, param)

def fset_maker(fget, name):
    def setit(obj, value):
        for fset in fget.fset_list:
            argvalues=[param_decider(obj, value, param, name) for param in fset.run_params]
            setattr(obj, fset.pname, fset(obj, *argvalues))
    return setit

class tagged_property(object):
    def __init__(self, **tags):
        #self.propify=kwargs.pop('propify', False)
        self.tags=tags

    def __call__(self, func):
        new_func=func_runner(func)
        new_func.fset_list=[]
        def setter(set_func):
            s_func=func_runner(set_func)
            new_func.fset_list.append(s_func)
            return s_func
        new_func.setter=setter
        return Property(new_func).tag(**self.tags)
        #return func_runner(func, **self.kwargs)

def func_runner(func, **tags):
    @wraps(func)
    def new_func(self, *args, **kwargs):
        for param in new_func.run_params[len(args):]:
            if param not in kwargs:
                kwargs[param]=getattr(self, param)
        return func(self, *args, **kwargs)
    new_func.run_params=get_run_params(func, skip=1)
    return new_func#, Property(new_func)

class NewAtomMeta(AtomMeta):
    def __new__(meta, name, bases, dct):
        update_dict={}
        print dct
        for param, itm in dct.items():
            if isinstance(itm, Property): #hasattr(value, "propify"):
                print param
                func_name=param+"_func"
                update_dict[func_name]=itm.fget
                if getattr(itm.fget, 'fset_list', [])!= []:
                    print param, itm#.fget.fset_list
                    def set_it(self, value):
                        print self, itm, value
                        self.Dvv=value
                        #for fset in item.fget.fset_list:
                        #    fset(self, value)
                    itm.setter(set_it)
        dct.update(update_dict)
        return AtomMeta.__new__(meta, name, bases, dct)

class Test(Atom):
    __metaclass__=NewAtomMeta
    Dvv=Float(3)
    #b=Float(4)

    @tagged_property(desc="coupling strength", unit="%", tex_str=r"K$^2$", expression=r"K$^2=2\Delta v/v$")
    def K2(self, Dvv):
        return Dvv*2

    @K2.fget.setter
    def _get_Dvv(self, K2):
        return K2/2

    #@tagged_property(propify=True, label="bill")
    #def test_func(self, a, b):
    #    """hi there"""
    #    print a,b
    #    return a

    #@test_func.setter
    #def _get_a(self, K2):
    #    print K2

t=Test()
#t.a
#t.a=1
print t.K2
#print t.test_func()
#print t.test_func_P
#t.test_func_P=4
print t.members()
print t.K2_func(35)
print t.Dvv
print t.K2
t.K2=32
print t.K2, t.Dvv
#print t.get_member("test_func_P")#.metadata
#print t.test_func.run_params
#print t.test_func

#@FuncRunner(t)
#def test_func(a, b):
#    print a, b

#t.test_func()
