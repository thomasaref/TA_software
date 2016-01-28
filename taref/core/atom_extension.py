# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 19:12:36 2016

@author: thomasaref
utility functions that extend Atom
A collection of functions for using taref's dynamic view. To maintain compatibility with Atom and object
derived objects, these are defined as standalone functions.
"""

from atom.api import Property, Callable, Coerced, Enum, Float, Int, Unicode, List, Dict, Str, ContainerList, Range, FloatRange
from numpy import shape, ndarray
from taref.core.log import log_debug, log_info
from functools import wraps
from enaml.application import deferred_call
from threading import Thread
from types import MethodType


_MAPPING_SUFFIX_="_mapping"
UNIT_DICT={"n":1.0e-9, "u":1.0e-6, "m":1.0e-3, "c":1.0e-2,
              "G":1.0e9, "M":1.0e6, "k":1.0e3,
              "%":1.0/100.0}

def set_tag(obj, name, **kwargs):
    """sets the tag of a member using Atom's built in tag functionality"""
    obj.get_member(name).tag(**kwargs)

def set_all_tags(obj, **kwargs):
    """set all parameters tags using keyword arguments.
        Shortcut to use Atom's tag functionality to set metadata on members not marked private, i.e. all_params.
    This is an easy way to set the same tag on all params"""
    for param in get_all_params(obj):
        set_tag(obj, param, **kwargs)

def get_tag(obj, name, key, none_value=None):
    """returns the tag key of a member name an returns none_value if it does not exist
        Shortcut to use Atom's retrive particular metadata which returns a none_value if it does not exist.
    This is an easy way to get a tag on a particular member and provide a default if it isn't there.
    runs slightly faster in this form"""
    metadata=obj.get_member(name).metadata
    if metadata is None:
        return none_value
    return metadata.get(key, none_value)

def get_all_tags(obj, key, key_value=None, none_value=None, search_list=None):
    """returns a list of names of parameters with a certain key_value
        Shortcut retrieve members with particular metadata. There are several variants based on inputs.
        With only obj and key specified, returns all member names who have that key
        with key_value specified, returns all member names that have that key set to key_value
        with key_value and none_value specified equal, returns all member names that have that key set to key_value or do not have the tag
        specifying search list limits the members searched
        Finally, if key_value is none, returns those members not matching none_value"""
    if search_list is None:
        search_list=obj.members()
    if key_value is None:
        return [x for x in search_list if none_value!=get_tag(obj, x, key, none_value)]
    return [x for x in search_list if key_value==get_tag(obj, x, key, none_value)]

def get_type(obj, name):
    """returns type of member with given name, with possible override via tag typer"""
    typer=type(obj.get_member(name))
    return get_tag(obj, name, "typer", typer)

def get_property_names(obj):
    if hasattr(obj, "property_names"):
        return obj.property_names
    return [name for name in get_all_params(obj) if type(obj.get_member(name)) is Property]

def get_property_values(obj):
    if hasattr(obj, "property_values"):
        return obj.property_values
    return [obj.get_member(name) for name in get_all_params(obj) if type(obj.get_member(name)) is Property]

def call_func(obj, name, **kwargs):
    """calls a func using keyword assignments. If name corresponds to a Property, calls the get func.
    otherwise, if name_mangled func "_get_"+name exists, calls that. Finally calls just the name if these are not the case"""
    if name in get_property_names(obj):
        return obj.get_member(name).fget(obj, **kwargs)
    elif name in get_all_params(obj) and hasattr(obj, "_get_"+name):
        return getattr(obj, "_get_"+name)(obj, **kwargs)
    return getattr(obj, name)(obj, **kwargs)

def reset_property(obj, name):
    obj.get_member(name).reset(obj)

def reset_properties(obj):
    """resets all  properties"""
    for item in get_property_values(obj):
        item.reset(obj)

def lowhigh_check(obj, name, value):
    """can specify low and high tags to keep float or int within a range."""
    if type(value) in (float, int):
        low=get_tag(obj, name, 'low')
        if low is not None:
            if value<low:
                return low
        high=get_tag(obj, name, 'high')
        if high is not None:
            if value>high:
                return high
    return value

def set_value_map(obj, name, value):
    """checks floats and ints for low/high limits and automaps an Enum when setting. Not working for List?"""
    value=lowhigh_check(obj, name, value)
    if get_type(obj, name)==Enum:
        return get_map(obj, name, value)
    return value

def log_func(func, pname=None):
    """logging decorator for Callables that logs call if tag log!=False"""
    func_name=func.func_name
    if pname is None:
        pname=func_name

    log_message=getattr(func, "log_message", "RAN: {0} {1}")
    @wraps(func)
    def new_func(self, *args, **kwargs):
        """logs the call of an instance method and autoinserts kwargs"""
        if get_tag(self, pname, "log", False):
            log_debug(log_message.format(getattr(self, "name", ""), func_name), n=1)
        if len(args)==0:
            members=self.members().keys()
            for param in get_run_params(new_func):
                if param in members:
                    if param in kwargs:
                        try:
                            setattr(self, param, kwargs[param])
                        except TypeError:
                            set_tag(self, param, do=kwargs[param])
                    else:
                        if param in get_property_names(self):
                            self.get_member(param).reset(self)
                        value=getattr(self, param)
                        value=set_value_map(self, param, value)
                        kwargs[param]=value
        #if hasattr(obj, "chief"): #not working. how to get return value?
        #    objargs=(obj,)+args
        #    return_value=do_it_if_needed(obj.chief, self.func, *objargs, **kwargs)
        #else:
        return func(self, *args, **kwargs)
    new_func.pname=pname
    new_func.run_params=get_run_params(func)
    return new_func

def make_instancemethod(obj, func, name=None):
    func=log_func(func, name)
    setattr(obj, func.pname, MethodType(func, obj, type(obj)))
    return func

class instancemethod(object):
    """disposable decorator object for instancemethods defined outside of Atom class"""
    def __init__(self, obj, name=None):
        self.name=name
        self.obj=obj

    def __call__(self, func):
        make_instancemethod(self.obj, func, self.name)
        return func

def get_run_params(f, skip_first=True):
    """returns names of parameters a function will call, skips first parameter if skip_first is True"""
    if hasattr(f, "run_params"):
        return f.run_params
    argcount=f.func_code.co_argcount
    if skip_first:
        return list(f.func_code.co_varnames[1:argcount])
    return list(f.func_code.co_varnames[0:argcount])

def get_map(obj, name, value=None, reset=False):
    """gets the mapped value specified by the property mapping and returns the attribute value if it doesn't exist
        gets the map of an Enum defined in the property name_mapping or tag mapping.
        value can be used to get the map for another value besides the Enum's current one."""
    if value is None:
        value=getattr(obj, name)
    mapping=get_tag(obj, name, "mapping")
    if mapping is None:
        mapping_name=name+_MAPPING_SUFFIX_
        if hasattr(obj, mapping_name):
            if reset:
                obj.get_member(mapping_name).reset(obj)
            return getattr(obj, mapping_name)[value]
    else:
        return mapping[value]
    return value

def get_inv(obj, name, value):
    """returns the inverse mapped value (meant for an Enum)"""
    mapping=get_tag(obj, name, "mapping")
    if mapping is None:
        if hasattr(obj, name+_MAPPING_SUFFIX_):
            return {v:k for k, v in getattr(obj, name+_MAPPING_SUFFIX_).iteritems()}[value]
    else:
            return {v:k for k, v in mapping.iteritems()}[value]
    return value


def private_property(fget):
    """ A decorator which converts a function into a cached Property tagged as private.
    Improves performance greatly over property!
    """
    return Property(fget, cached=True).tag(private=True)

class tag_Callable(object):
    """disposable decorator class that returns a Callable tagged with kwargs"""
    default_kwargs={}
    def __init__(self, **kwargs):
        """adds default_kwargs if not specified in kwargs"""
        for key in self.default_kwargs:
            kwargs[key]=kwargs.get(key, self.default_kwargs[key])
        self.kwargs=kwargs

    def __call__(self, func):
        return Callable(func).tag(**self.kwargs)

class tag_Property(tag_Callable):
    """disposable decorator class that returns a cached Property tagged with kwargs"""
    def __init__(self, cached=True, **kwargs):
        super(tag_Property, self).__init__(**kwargs)
        self.cached=cached

    def __call__(self, func):
        return Property(func, cached=self.cached).tag(**self.kwargs)

def get_reserved_names(obj):
    """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
    if hasattr(obj, "reserved_names"):
        return obj.all_params
    return get_all_tags(obj, key="private", key_value=True)

def get_all_params(obj):
    """all members that are not tagged as private, i.e. not in reserved_names and will behave as agents.
        order of magnitude faster when combine with private_property"""
    if hasattr(obj, "all_params"):
        return obj.all_params
    return get_all_tags(obj, key="private", key_value=False, none_value=False)

def get_all_main_params(obj):
    """all members in all_params that are not tagged as sub.
     Convenience function for more easily custom defining main_params in child classes"""
    if hasattr(obj, "all_main_params"):
        return obj.all_main_params
    return get_all_tags(obj, 'sub', False, False, get_all_params(obj))

def get_main_params(obj):
    """returns main_params if it exists and all possible main params if it does not"""
    if hasattr(obj, "main_params"):
        return obj.main_params
    return get_all_main_params(obj)

def set_attr(self, name, value, **kwargs):
    """utility function for setting tags while setting value"""
    setattr(self, name, value)
    if kwargs!={}:
        set_tag(self, name, **kwargs)

def set_log(obj, name, value):
   """called when parameter of given name is set to value i.e. instr.parameter=value. Customized messages for different types. Also saves data"""
   if get_tag(obj, name, 'log', True) and not get_tag(obj, name, "tracking", False):
       label=get_tag(obj, name, 'label', name)
       unit=get_tag(obj, name, 'unit', "")
       obj_name=getattr(obj, "name", "NO_NAME")
       typer=get_type(obj, name)
       if typer==Coerced:
           typer=type(getattr(obj, name))
       if typer==Enum:
           log_info("Set {instr} {label} to {value} ({map_val})".format(
                 instr=obj_name, label=label, value=value,
                 map_val=get_map(obj, name, value)))
       elif typer in (List, ContainerList, list):
           log_info("Set {instr} {label} to {length} list".format(
               instr=obj_name, label=label, length=shape(value)))
       elif typer==ndarray:
           log_info("Set {instr} {label} to {length} array".format(
               instr=obj_name, label=label, length=shape(value)))
       elif typer==Dict:
           log_info("Set {instr} {label} dict".format(instr=obj_name, label=label))
       elif typer in (Unicode, Str):
           log_info("Set {instr} {label} to {length} length string".format(instr=obj_name, label=label, length=len(value)))
       elif typer==Float:
           unit_factor=get_tag(obj, name, 'unit_factor', 1.0)
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=float(value)/unit_factor, unit=unit), n=1)
       elif typer==Int:
           unit_factor=get_tag(obj, name, 'unit_factor', 1)
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=int(value)/unit_factor, unit=unit))
       else:
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=value, unit=unit))
   if hasattr(obj, "data_save"):
       obj.datasave(name, value)


def code_caller(topdog, code, *args, **kwargs):
    result=code(*args, **kwargs)
    try:
        deferred_call(setattr, topdog, 'busy', False)
        deferred_call(setattr, topdog, 'progress', 0)
        deferred_call(setattr, topdog, 'abort', False)
    except RuntimeError:
        topdog.busy=False
        topdog.progress=0
        topdog.abort=False
    return result

def do_it_if_needed(topdog, code, *args, **kwargs):
    if not topdog.busy:
        topdog.busy = True
        thread = Thread(target=code_caller, args=(topdog, code)+args, kwargs=kwargs)
        thread.start()