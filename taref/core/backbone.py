# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:52:51 2015

@author: thomasaref

A collection of functions for using taref's dynamic view. To maintain compatibility with Atom and object
derived objects, these are defined as standalone functions. Get functions usually return some none_value even
if the value did not exist.
"""

from inspect import getmembers
from atom.api import Atom, List, Callable, Enum, Int, Float, Range, FloatRange, Property #Callable, Unicode, Bool, List
from functools import wraps
from numpy import shape, ndarray
from enaml.application import deferred_call
from threading import Thread
from types import FunctionType

from taref.core.log import log_info, log_debug

#_UPDATE_PREFIX_="_update_"
_MAPPING_SUFFIX_="_mapping"

def set_value_map(obj, name, value):
    """checks floats and ints for low/high limits and automaps an Enum when setting. Not working for List?"""
    value=lowhigh_check(obj, name, value)
    if get_type(obj, name)==Enum:
        return get_map(obj, name, value)
    return value

def get_run_params(f):
    """returns names of parameters a function will call"""
    if hasattr(f, "run_params"):
        return f.run_params
    argcount=f.func_code.co_argcount
    return f.func_code.co_varnames[0:argcount]

class logging_f(object):
    """A logging wrapper that is compatible with both functions or Callables.
    Auto sets self in the function call to self.obj if it has been set
    for easier use of Callables"""
    def __init__(self, func):
        self.func=func
        self.obj=None
        self.log=True
        self.run_params=[param for param in get_run_params(func) if param!="self"]

    def __call__(self, obj=None, *args, **kwargs):
        """call logs the call if desired and autoinserts kwargs and obj"""
        log_debug((obj, args, kwargs))
        if obj is None:
            obj=self.obj
        if len(args)==0:
            for param in self.run_params:
                if param in kwargs:
                    if type(kwargs[param])==type(get_attr(obj, param)):
                        setattr(obj, param, kwargs[param])
                else:
                    if param in obj.property_names:
                        obj.get_member(param).reset(obj)
                    value=getattr(obj, param)
                    value=set_value_map(obj, param, value)
                    kwargs[param]=value
        #if hasattr(obj, "chief"): #not working. how to get return value?
        #    objargs=(obj,)+args
        #    return_value=do_it_if_needed(obj.chief, self.func, *objargs, **kwargs)
        #else:
        return_value=self.func(obj, *args, **kwargs)
        if self.log:
            log_debug(kwargs)
            log_debug((self.func.func_name, return_value))
        return return_value

class tagged_callable(object):
    """disposable decorator class that returns a Callable tagged with kwargs.
    Logging is initiated if tags private is not True or log is False"""
    def __init__(self, **kwargs):
        self.kwargs=kwargs

    def __call__(self, func):
        t_func=logging_f(func)
        if self.kwargs.get("private", False) or not self.kwargs.get("log", True):
            t_func.log=False
        return Callable(t_func).tag(**self.kwargs)

class property_f(logging_f):
    def __init__(self, func):
        super(property_f, self).__init__(func)
        name_list=self.func.func_name.split("_get_")
        if name_list[0]=="":
            self.name=name_list[1]
        else:
            self.name=name_list[0]
        self.fset_list=[]

    def setter(self, func):
        s_func=property_f(func)
        self.fset_list.append(s_func)
        return s_func

    def fset_maker(self, obj):
        def setit(obj, value):
            for fset in self.fset_list:
                argvalues=[self.param_decider(obj, param, value)
                                 for param in fset.run_params]
                setattr(obj, fset.name, fset(obj, *argvalues))
        return setit

    def param_decider(self, obj, param, value):
        if param==self.name:
            return value
        return getattr(obj, param)

class tagged_property(object):
    """disposable decorator class that returns a cached Property tagged with kwargs"""
    def __init__(self, **kwargs):
        self.kwargs=kwargs

    def __call__(self, func):
        t_func=property_f(func)
        if self.kwargs.get("private", False) or not self.kwargs.get("log", True):
            t_func.log=False
        return Property(t_func, cached=True).tag(**self.kwargs)

class tag_Property(object):
    """disposable decorator class that returns a cached Property tagged with kwargs"""
    def __init__(self, **kwargs):
        self.kwargs=kwargs

    def __call__(self, func):
        return Property(func, cached=True).tag(**self.kwargs)

def private_property(fget):
    """ A decorator which converts a function into a cached Property tagged as private.
    Improves performance greatly over property!
    Parameters
    ----------
    fget : callable
        The callable invoked to get the property value. It must accept
        a single argument which is the owner object.
    """
    return Property(fget, cached=True).tag(private=True)

def get_member(obj, name):
    """returns a member if get_member exists and the attribute itself if it does not"""
    if hasattr(obj, "get_member"):
        return obj.get_member(str(name))
    return getattr(obj, str(name))

def members(obj):
    """returns members if defined, e.g. Atom class, or attributes whose names don't start with _"""
    if hasattr(obj, "members"):
        return obj.members()
    return dict([mem for mem in getmembers(obj) if mem[0][0]!="_"])

def get_metadata(obj, name):
    """returns the metadata of a member if it exists and generates an empty dictionary if it does not"""
    if isinstance(obj, Atom):
        member=obj.get_member(name)
        if member.metadata is None:
            member.metadata={}
        return member.metadata
    return {}

def set_tag(obj, name, **kwargs):
    """sets the tag of a member using Atom's built in tag functionality"""
    member=obj.get_member(name)
    member.tag(**kwargs)

def set_all_tags(obj, **kwargs):
    """set all parameters tags using keyword arguments"""
    for param in get_all_params(obj):
        set_tag(obj, param, **kwargs)

def get_tag(obj, name, key, none_value=None):
    """returns the tag key of a member name an returns none_value if it does not exist"""
    metadata=get_metadata(obj, name)
    return metadata.get(key, none_value)

def get_all_tags(obj, key, key_value=None, none_value=None, search_list=None):
    """returns a list of names of parameters with a certain key_value"""
    if search_list is None:
        search_list=members(obj)
    if key_value is None:
        return [x for x in search_list if none_value!=get_tag(obj, x, key, none_value)]
    return [x for x in search_list if key_value==get_tag(obj, x, key, none_value)]

def get_map(obj, name, value=None):
    """gets the mapped value specified by the property mapping and returns the attribute value if it doesn't exist"""
    if value is None:
        value=getattr(obj, name)
    if hasattr(obj, name+"_mapping"):
        return getattr(obj, name+"_mapping")[value]
    return value

def get_inv(obj, name, value):
    """returns the inverse mapped value (meant for an Enum)"""
    if hasattr(obj, name+_MAPPING_SUFFIX_):
        return {v:k for k, v in getattr(obj, name+_MAPPING_SUFFIX_).iteritems()}[value]
    return value

def get_type(obj, name):
    """returns type of member with given name, with possible override via tag typer"""
    typer=type(get_member(obj, name))
    return get_tag(obj, name, "typer", typer)

def get_reserved_names(obj):
    """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
    return get_all_tags(obj, "private", True)

def get_all_params(obj):
    """all members that are not tagged as private, i.e. not in reserved_names and will behave as agents"""
    return get_all_tags(obj, key="private", key_value=False, none_value=False)

def get_all_main_params(obj):
    """all members in all_params that are not tagged as sub.
     Convenience function for more easily custom defining main_params in child classes"""
    return get_all_tags(obj, 'sub', False, False, get_all_params(obj))

def get_main_params(obj):
    """returns main_params if it exists and all possible main params if it does not"""
    if hasattr(obj, "main_params"):
        return obj.main_params
    return get_all_main_params(obj)

def get_attr(obj, name, none_value=None):
    """returns the attribute if the obj has it and the none_value if it does not"""
    return getattr(obj, name, none_value)

def set_attr(self, name, value, **kwargs):
    """utility function for setting tags while setting value"""
    setattr(self, name, value)
    if kwargs!={}:
        set_tag(self, name, **kwargs)

##remove?
def pass_func(*args, **kwargs):
    pass

def run_func(obj, name, none_func=pass_func, *args, **kwargs):
    if hasattr(obj, str(name)):
        return getattr(obj, name)(*args, **kwargs)
    return none_func(*args, **kwargs)

def lowhigh_check(obj, name, value):
    """can specify low and high tags to keep float or int within a range."""
    if type(value) in (float, int):
        metadata=get_metadata(obj, name)
        if 'low' in metadata:
            if value<metadata['low']:
                return metadata['low']
        if 'high' in metadata:
            if value>metadata['high']:
                return metadata['high']
    return value

def data_save(obj, name, value):
    """data saving. does nothing if data_save is not defined"""
    if hasattr(obj, "data_save"):
        obj.datasave(name, value)

def set_log(obj, name, value):
   """called when parameter of given name is set to value i.e. instr.parameter=value. Customized messages for different types. Also saves data"""
   if get_tag(obj, name, 'log', True):
       label=get_tag(obj, name, 'label', name)
       unit=get_tag(obj, name, 'unit', "")
       obj_name=get_attr(obj, "name", "NO_NAME")
       if get_type(obj, name)==Enum:
           log_info("Set {instr} {label} to {value} ({map_val})".format(
                 instr=obj_name, label=label, value=value,
                 map_val=get_map(obj, name, value)))
       #elif get_type(obj, name) in (Callable, type(dummyf)):
       #    log_info("Set {instr} {label} to {length} list".format(
       #        instr=obj_name, label=label, length=shape(getattr(obj, name))))
       elif type(value)==list:
           log_info("Set {instr} {label} to {length} list".format(
               instr=obj_name, label=label, length=shape(getattr(obj, name))))
       elif type(value)==ndarray:
           log_info("Set {instr} {label} to {length} array".format(
               instr=obj_name, label=label, length=shape(value)))
       elif type(value)==dict:
           log_info("Set {instr} {label}".format(instr=obj_name, label=label))
       elif type(value)==basestring:
           log_info("Set {instr} {label} to {length} string".format(instr=obj_name, label=label, length=len(value)))
       elif type(value)==float:
           unit_factor=get_tag(obj, name, 'unit_factor', 1.0)
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=value/unit_factor, unit=unit))
       elif type(value)==int:
           unit_factor=get_tag(obj, name, 'unit_factor', 1)
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=value/unit_factor, unit=unit))
       else:
           log_info("Set {instr} {label} to {value}".format(
                             instr=obj_name, label=label, value=value, unit=unit))
   data_save(obj, name, value)

unit_dict={"n":1.0e-9, "u":1.0e-6, "m":1.0e-3, "c":1.0e-2,
              "G":1.0e9, "M":1.0e6, "k":1.0e3,
              "%":1.0/100.0}

class Backbone(Atom):
    """Class combining primary functions for viewer operation"""
    main_params=List().tag(private=True, desc="main parameters: allows control over what is displayed and in what order")

    def get_metadata(self, name):
        return get_metadata(self, name)

    def set_tag(self, name, **kwargs):
        set_tag(self, name, **kwargs)

    def set_all_tags(self, **kwargs):
        set_all_tags(self, **kwargs)

    def get_tag(self, name, key, none_value=None):
        return get_tag(self, name, key, none_value)

    def get_all_tags(self, key, key_value=None, none_value=None, search_list=None):
        return get_all_tags(self, key, key_value, none_value, search_list)

    def get_type(self, name):
        return get_type(self, name)

    @private_property
    def reserved_names(self):
        return get_reserved_names(self)

    @private_property
    def all_params(self):
        return get_all_params(self)

    @private_property
    def all_main_params(self):
        return get_all_main_params(self)

    def _default_main_params(self):
        """defaults to all members in all_params that are not tagged as sub.
        Can be overwritten to allow some minimal custom layout control,
        e.g. order of presentation and which members are shown. Use all_main_params to get a list of
        all members that could be in main_params"""
        return self.all_main_params

    def lowhigh_check(self, name, value):
        return lowhigh_check(self, name, value)

    def set_log(self, name, value):
        set_log(self, name, value)

    def get_map(self, name, value=None):
        return get_map(self, name=name, value=value)

    @private_property
    def unit_dict(self):
        return unit_dict

    @private_property
    def property_names(self):
        """gets all params that are Properties"""
        return [name for name in self.all_params if self.get_type(name) is Property]

    @private_property
    def property_items(self):
        """get all items corrseponding to self.property_names"""
        return [self.get_member(name) for name in self.property_names]

    @private_property
    def property_dict(self):
        """returns a dict mapping property_names to property_items"""
        return dict(zip(self.property_names, self.property_items))

    def extra_setup(self, param, typer):
        """sets up property_fs, ranges, and units"""
        self._setup_property_fs(param, typer)
        self._setup_ranges(param, typer)
        self._setup_units(param, typer)

    def call_func(self, name, **kwargs):
        """calls a func using keyword assignments. If name corresponds to a Property, calls the get func.
        otherwise, if name_mangled func "_get_"+name exists, calls that. Finally calls just the name if these are not the case"""
        if name in self.property_dict:
            return self.property_dict[name].fget(self, **kwargs)
        elif name in self.all_params and hasattr(self, "_get_"+name):
            return getattr(self, "_get_"+name)(self, **kwargs)
        return getattr(self, name)(**kwargs)

    def __setattr__(self, name, value):
        """uses __setattr__ to log changes except for ContainerList"""
        if name in self.all_params:
            value=self.lowhigh_check(name, value)
        super(Backbone, self).__setattr__(name, value)

    def reset_properties(self):
        """resets all  properties"""
        for item in self.property_items:
            item.reset(self)

    def _setup_logging_fs(self):
        """sets up logging_f's pointing obj to self"""
        for name in [attr for attr, item in getmembers(self) if isinstance(item, logging_f)]:
            setattr(getattr(self, name), "obj", self)

    def _setup_property_fs(self, param, typer):
        """sets up property_f's pointing obj at self and setter at functions decorated with param.fget.setter"""
        item =get_attr(self.get_member(param), "fget")
        if isinstance(item, property_f):
            item.obj=self
            if item.fset_list!=[]:
                self.get_member(param).setter(item.fset_maker(self))

    def _setup_ranges(self, param, typer):
        """autosets low/high tags for Range and FloatRange"""
        if typer in [Range, FloatRange]:
            self.set_tag(param, low=self.get_member(param).validate_mode[1][0], high=self.get_member(param).validate_mode[1][1])

    def _setup_units(self, param, typer):
        """autosets units using unit_dict"""
        if typer in [Int, Float, Range, FloatRange, Property]:
            if self.get_tag(param, "unit", False) and (self.get_tag(param, "unit_factor") is None):
                unit=self.get_tag(param, "unit", "")[0]
                if unit in self.unit_dict:
                    unit_factor=self.get_tag(param, "unit_factor", self.unit_dict[unit])
                    self.set_tag(param, unit_factor=unit_factor)

    def __init__(self, **kwargs):
        """extends __init__ to autoset low and high tags for Range and FloatRange, autoset units for Ints and Floats and allow extra setup"""
        super(Backbone, self).__init__(**kwargs)
        self._setup_logging_fs()
        for param in self.all_params:
            typer=self.get_type(param)
            self.extra_setup(param, typer)

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

