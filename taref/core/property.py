# -*- coding: utf-8 -*-
"""
Created on Fri May  6 11:31:56 2016

@author: thomasaref
Collection of Property related utilities
"""

from atom.api import Property, Atom, Float, Enum, Value
from atom_extension import get_all_params
from taref.core.callable import LogFunc

def get_property_names(obj):
    """returns property names that are in all_params"""
    if hasattr(obj, "property_names"):
        return obj.property_names
    return [name for name in get_all_params(obj) if isinstance(obj.get_member(name), Property)]

def get_property_values(obj):
    """returns property values that are in all_params"""
    if hasattr(obj, "property_values"):
        return obj.property_values
    return [obj.get_member(name) for name in get_all_params(obj) if isinstance(obj.get_member(name), Property)]

#def reset_property(obj, name):
#    """shortcut to reset of property"""
#    obj.get_member(name).reset(obj)

def reset_property(obj, *args):
    """resets all  properties in args. resets all properties in  all_params if no args passed"""
    if args==():
        for item in get_property_values(obj):
            print item
            item.reset(obj)
    else:
        for name in args:
            print name
            obj.get_member(name).reset(obj)

def reset_properties(obj, property_list=None):
    """resets all  properties that are in all_params"""
    if property_list is None:
        property_list=get_property_values(obj)
    for item in property_list:
        item.reset(obj)

def private_property(fget):
    """ A decorator which converts a function into a cached Property tagged as private.
    Improves performance greatly over property!
    """
    return Property(fget, cached=True).tag(private=True)

class SProperty(Property):
    """a Property that accepts multiple set functions, defaults to cached.
    it automatically makes """
    def __init__(self, fget=None, fset=None, fdel=None, cached=True):
        """calls super init and create fset_list"""
        super(SProperty, self).__init__(fget=None, fset=None, fdel=fdel, cached=cached)
        self.fset_list=[]
        if fget is not None:
            self.getter(fget)
        self.initify(fset)

    def initify(self, fset):
        """additional initialization. applies setter to fset if it is not None"""
        if fset is not None:
            self.setter(fset)

    def fset_maker(self):
        """creates a fset that calls functions in fset_list"""
        def fset_clt(obj, value):
            for fset in self.fset_list:
                fset(obj, value)
        return fset_clt

    def logify(self, func):
        """applies log_func to function and returns it"""
        if self.metadata is None:
            return LogFunc()(func)
        else:
            return LogFunc(**self.metadata)(func)

    def getify(self, func):
        """additional getter operation just returns function by default"""
        return func

    def getter(self, func):
        """extended getter makes function into log_func and applies getify to it"""
        func=self.logify(func)
        fget=self.getify(func)
        super(SProperty, self).getter(fget)
        return func

    def setter(self, func):
        """setter makes function into log_func, applies setify, adds it to fset_list and creates fset function if it does not exist"""
        func=self.logify(func)
        self.fset_list.append(self.setify(func))
        if self.fset is None:
            super(SProperty, self).setter(self.fset_maker())
        return func

    def setify(self, func):
        """splits set function name using _get_ delimiter and creates auto set function"""
        pname=func.func_name.split("_get_")[1]
        def autoset(obj, value):
            setattr(obj, pname, func(obj, value))
        return autoset

class TProperty(SProperty):
    """a property that autostores a value to a private value. returns private value unless
    private value is None"""
    def __init__(self, fget=None, fset=None, fdel=None, cached=True):
        super(TProperty, self).__init__(fget=fget, fset=fset, fdel=fdel, cached=cached)

    def initify(self, fset):
        if self.fset is None:
            super(SProperty, self).setter(self.fset_maker())
        self.fset_list.append(self.passify_fset())

    def getify(self, func):
        def getit(obj):
            temp=getattr(obj, "_"+self.name)
            if temp is None:
                return func(obj)
            return temp
        return getit

    def passify_fset(self):
        def setit(obj, value):
            setattr(obj, "_"+self.name, value)
        return setit

    @classmethod
    def extra_setup(cls, param, itm, update_dict):
        if isinstance(itm, TProperty):
            update_dict["_"+param]=Value().tag(private=True)


class tag_property(object):
    """disposable decorator class that returns a Property tagged with kwargs.
    cached keyword in kwargs defaults to True"""
    default_kwargs={}
    prop_class=Property

    def __init__(self, **kwargs):
        """adds default_kwargs if not specified in kwargs"""
        for key in self.default_kwargs:
            kwargs[key]=kwargs.get(key, self.default_kwargs[key])
        cached=kwargs.pop("cached", True)
        self.prop=self.prop_class(cached=cached).tag(**kwargs)

    def __call__(self, func):
        self.prop.getter(func)
        return self.prop

class s_property(tag_property):
    """disposable decorator class that returns a SetProperty tagged with kwargs, defaults to cached"""
    prop_class=SProperty

class t_property(tag_property):
    """disposable decorator class that returns a SetProperty tagged with kwargs, defaults to cached"""
    prop_class=TProperty


if __name__=="__main__":
    class Test(Atom):
        a=SProperty(cached=False)
        c=Float()
        #b=TProperty(cached=False)#.tag(blah=3)
        #_b=Value()
        d=Enum("single", "double")

        @t_property(cached=False)
        def b(self, d):
            return {"single" : 3, "double" : 4}[d]

        @a.getter
        def _get_a(self, c):
            return 2*c

        @a.setter
        def _get_c(self, a):
            return a/2


    t=Test()
    z=Test()
    print t.a, t.c, z.a, z.c
    t.a=2
    print t.a, t.c, z.a, z.c
    t.c=4
    print t._get_a(1), t._get_c(3.0), z._get_a(), z._get_c()
    print t.a, t.c, z.a, z.c

    print t.b, z.b, t.a, t.c
    t.b=2
    print t.b, z.b
    t.b=None
    print t.b, z.b
    print t._b
    print t._a

    #print t.get_member("b").private_param
