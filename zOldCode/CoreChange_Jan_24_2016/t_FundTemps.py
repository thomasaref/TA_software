# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 17:32:20 2015

@author: thomasaref
"""

from enaml import imports
from enaml.qt.qt_application import QtApplication
from atom.api import Atom, Bool, Int, Str, Coerced, Instance, Float, Unicode, Enum, Callable, Typed, Range, FloatRange, ContainerList, List
from LOG_functions import log_debug
from numpy import array, ndarray

def show(a):
    app = QtApplication()
    with imports():
        from e_FundTemps import Main
    view=Main(instr=a)
    view.show()
    app.start() 

class testChief(Atom):
    busy=Bool()
    abort=Bool()
    progress=Int()

testchief=testChief()

class subtest(Atom):
    st_int=Int()
    st_str=Str()
    
class test(Atom):
    #Ints can have units, show_value, unit_factor and low/high limits
    t_int=Int().tag(unit="um", show_value=True, unit_factor=20, low=0, high=5)
    #Ints can be shown as spin boxes or int fields
    t_int_intfield=Int().tag(unit="um", show_value=True, unit_factor=20, low=0, high=5, spec="intfield")
    #Coerced of basic types have same behavior as basic type, e.g. this coerced int acts like the Int above
    t_coerced_int=Coerced(int).tag(unit="um", show_value=True, unit_factor=20, low=0, high=5, spec="intfield")
    
    #ranges are represented with sliders
    t_range=Range(0, 5, 1)
    t_floatrange=FloatRange(0.0, 5.0, 1.0)
    #You can include other classes
    t_typed=Typed(subtest, ())
    t_instance=Instance(subtest, ())
    
    #lists
    t_list=List(default=[1.2, 1.3, 1.4])
    t_containerlist=ContainerList(default=[1.2, 1.3, 1.4]).tag(unit="um")
    
    #how to do a numpy array
    t_coerced_arr=Coerced(ndarray, coercer=array)#.tag(private=7)

    #Floats can have units, show_value, unit_factor and low/high limits
    t_float=Float().tag(unit="GHz", show_value=True, unit_factor=0.2, low=-1.0, high=1)
    #A Bool demostrating the label functionality
    t_bool=Bool().tag(label="MY BOOL")
    
    
    #Unicode Field display    
    t_unicode=Unicode("blah")
    
    #Unicode Multiline Field disply
    t_unicode_multiline=Unicode("blah").tag(spec="multiline")
    
    #unmapped Enum
    t_enum=Enum("one", "two", "three")

    #mapped Enum
    @property
    def t_enum_map_mapping(self):
        return dict(one=1, two=2, three=3)
    
    t_enum_map=Enum("one","two","three")

    #attribute mapped enum
    @property
    def t_enum_attr_mapping(self):
        return dict(t_int=self.t_int, t_float=self.t_float, t_bool=self.t_bool)

    t_enum_attr=Enum("t_int","t_float","t_bool").tag(map_type="attribute")


    #Note: extra run features (extra args, run lockout, abort) only function if chief is defined    
    @Callable
    def a(self):
        from time import sleep
        log_debug("a_called")
        for n in range(5):
            log_debug(n)
            if self.abort:
                break
            sleep(0.4)
        log_debug("a_endded")

    @property    
    def chief(self):
        return testchief
        
    @property    
    def busy(self):
        return testchief.busy
        
    @property    
    def abort(self):
        return testchief.abort

a=test()
a.t_coerced_arr=[0.1, 0.2]

show(a)

#from taref.core.log import log_info, log_debug
#from taref.core.atom_extension import log_func
#
#_MAPPING_SUFFIX_="_mapping"
#
#def get_view(obj, default_view, default_name="NO_NAME"):
#    view=getattr(obj, "view_window", default_view)
#    view.name=getattr(obj, "name", default_name)
#    if view.title=="":
#        view.title=view.name
#    return view
#
#def set_value_map(obj, name, value):
#    """checks floats and ints for low/high limits and automaps an Enum when setting. Not working for List?"""
#    value=lowhigh_check(obj, name, value)
#    if get_type(obj, name)==Enum:
#        return get_map(obj, name, value)
#    return value
#
#def get_run_params(f, skip_first=True):
#    """returns names of parameters a function will call"""
#    if hasattr(f, "run_params"):
#        return f.run_params
#    argcount=f.func_code.co_argcount
#    if skip_first:
#        return list(f.func_code.co_varnames[1:argcount])
#    return list(f.func_code.co_varnames[0:argcount])
#
#class logging_f(object):
#    """A logging wrapper that is compatible with both functions or Callables.
#    Auto sets self in the function call to self.obj if it has been set
#    for easier use of Callables"""
#    def __init__(self, func, log=True):
#        self.func=func
#        self.log=log
#        self.run_params=[param for param in get_run_params(func)][1:]
#
#    def __call__(self, obj, *args, **kwargs):
#        """call logs the call if desired and autoinserts kwargs and obj"""
#        #log_debug(obj, args, kwargs, n=1)
#        if len(args)==0:
#            for param in self.run_params:
#                if param in kwargs:
#                    if type(kwargs[param])==type(get_attr(obj, param)):
#                        setattr(obj, param, kwargs[param])
#                else:
#                    if param in obj.property_dict.keys():
#                        obj.get_member(param).reset(obj)
#                    value=getattr(obj, param)
#                    value=set_value_map(obj, param, value)
#                    kwargs[param]=value
#        #if hasattr(obj, "chief"): #not working. how to get return value?
#        #    objargs=(obj,)+args
#        #    return_value=do_it_if_needed(obj.chief, self.func, *objargs, **kwargs)
#        #else:
#        return_value=self.func(obj, *args, **kwargs)
#        if self.log:
#            #log_debug(kwargs)
#            log_debug(self.func.func_name, return_value, n=1)
#        return return_value
#
#class tagged_callable(object):
#    """disposable decorator class that returns a Callable tagged with kwargs.
#    Logging is initiated if tags private is not True or log is False"""
#    default_kwargs={}
#
#    def __init__(self, **kwargs):
#        """adds default_kwargs if not specified in kwargs"""
#        for key in self.default_kwargs:
#            kwargs[key]=kwargs.get(key, self.default_kwargs[key])
#        self.kwargs=kwargs
#
#    def __call__(self, func):
#        t_func=logging_f(func)
#        if self.kwargs.get("private", False) or not self.kwargs.get("log", True):
#            t_func.log=False
#        return Callable(t_func).tag(**self.kwargs)
#
#class property_f(logging_f):
#    def __init__(self, func):
#        super(property_f, self).__init__(func)
#        name_list=self.func.func_name.split("_get_")
#        if name_list[0]=="":
#            self.name=name_list[1]
#        else:
#            self.name=name_list[0]
#        self.fset_list=[]
#
#    def setter(self, func):
#        s_func=property_f(func)
#        self.fset_list.append(s_func)
#        return s_func
#
#    def fset_maker(self, obj):
#        def setit(obj, value):
#            for fset in self.fset_list:
#                argvalues=[self.param_decider(obj, param, value)
#                                 for param in fset.run_params]
#                setattr(obj, fset.name, fset(obj, *argvalues))
#        return setit
#
#    def param_decider(self, obj, param, value):
#        if param==self.name:
#            return value
#        return getattr(obj, param)
#
#class tagged_property(object):
#    """disposable decorator class that returns a cached Property tagged with kwargs"""
#    def __init__(self, **kwargs):
#        self.kwargs=kwargs
#
#    def __call__(self, func):
#        t_func=property_f(func)
#        if self.kwargs.get("private", False) or not self.kwargs.get("log", False):
#            t_func.log=False
#        return Property(t_func, cached=True).tag(**self.kwargs)
#
#class tag_Property(object):
#    """disposable decorator class that returns a cached Property tagged with kwargs"""
#    def __init__(self, **kwargs):
#        self.kwargs=kwargs
#
#    def __call__(self, func):
#        return Property(func, cached=True).tag(**self.kwargs)
#
#class tag_Callable(object):
#    """disposable decorator class that returns a Callable tagged with kwargs"""
#    def __init__(self, **kwargs):
#        self.kwargs=kwargs
#
#    def __call__(self, func):
#        return Callable(func).tag(**self.kwargs)
#
#from functools import wraps
#def log_func(func):
#    @wraps
#    def new_func(obj, *args, **kwargs):
#        """call logs the call if desired and autoinserts kwargs and obj"""
#        #log_debug(obj, args, kwargs, n=1)
#        if len(args)==0:
#            for param in self.run_params:
#                if param in kwargs:
#                    if type(kwargs[param])==type(get_attr(obj, param)):
#                        setattr(obj, param, kwargs[param])
#                else:
#                    if param in obj.property_dict.keys():
#                        obj.get_member(param).reset(obj)
#                    value=getattr(obj, param)
#                    value=set_value_map(obj, param, value)
#                    kwargs[param]=value
#        #if hasattr(obj, "chief"): #not working. how to get return value?
#        #    objargs=(obj,)+args
#        #    return_value=do_it_if_needed(obj.chief, self.func, *objargs, **kwargs)
#        #else:
#        return_value=self.func(obj, *args, **kwargs)
#        if self.log:
#            #log_debug(kwargs)
#            log_debug(self.func.func_name, return_value, n=1)
#        return return_value
#
#class tag_Callable2(tag_Callable):
#    """disposable decorator class that returns a Callable tagged with kwargs"""
#    def __call__(self, func):
#        if "run_params" not in self.kwargs:
#            self.kwargs["run_params"]=get_run_params(func)
#        super(tag_Callable2, self).__call__(func)
#
#def private_property(fget):
#    """ A decorator which converts a function into a cached Property tagged as private.
#    Improves performance greatly over property!
#    Parameters
#    ----------
#    fget : callable
#        The callable invoked to get the property value. It must accept
#        a single argument which is the owner object.
#    """
#    return Property(fget, cached=True).tag(private=True)
#
##redundant
#def get_member(obj, name):
#    """returns a member if get_member exists and the attribute itself if it does not.
#    Returns the member of obj specified by name. This allows easy access to member functions and is included in the Atom api"""
#    if hasattr(obj, "get_member"):
#        return obj.get_member(str(name))
#    return getattr(obj, str(name))
#
##remove?
#def reset_property(obj, name):
#    get_member(obj, name).reset(obj)
#
##redundant
#def members(obj):
#    """returns members if defined, e.g. Atom class, or attributes whose names don't start with _
#    Returns the member dictionary of obj.
#    This allows easy access to all members and is included in the Atom api"""
#    if hasattr(obj, "members"):
#        return obj.members()
#    return dict([mem for mem in getmembers(obj) if mem[0][0]!="_"])
#
##remove?
#def get_metadata(obj, name):
#    """returns the metadata of a member if it exists and generates an empty dictionary if it does not
#        Returns the metadata dictionary of member of obj specified by name.
#    This allows easy access to metadata and autogenerates an empty dictionary if metadata is None."""
#    if isinstance(obj, Atom):
#        member=obj.get_member(name)
#        if member.metadata is None:
#            member.metadata={}
#        return member.metadata
#    return {}
#
##remove
#def set_tag(obj, name, **kwargs):
#    """sets the tag of a member using Atom's built in tag functionality"""
#    member=obj.get_member(name)
#    member.tag(**kwargs)
#
##remove?
#def set_all_tags(obj, **kwargs):
#    """set all parameters tags using keyword arguments.
#        Shortcut to use Atom's tag functionality to set metadata on members not marked private, i.e. all_params.
#    This is an easy way to set the same tag on all params"""
#    for param in get_all_params(obj):
#        set_tag(obj, param, **kwargs)
#
#
#def get_tag(obj, name, key, none_value=None):
#    """returns the tag key of a member name an returns none_value if it does not exist
#        Shortcut to use Atom's retrive particular metadata which returns a none_value if it does not exist.
#    This is an easy way to get a tag on a particular member and provide a default if it isn't there."""
#    metadata=get_metadata(obj, name)
#    return metadata.get(key, none_value)
#
##remove?
#def get_all_tags(obj, key, key_value=None, none_value=None, search_list=None):
#    """returns a list of names of parameters with a certain key_value
#        Shortcut retrieve members with particular metadata. There are several variants based on inputs.
#        With only obj and key specified, returns all member names who have that key
#        with key_value specified, returns all member names that have that key set to key_value
#        with key_value and none_value specified equal, returns all member names that have that key set to key_value or do not have the tag
#        specifying search list limits the members searched
#        Finally, if key_value is none, returns those members not matching none_value"""
#    if search_list is None:
#        search_list=members(obj)
#    if key_value is None:
#        return [x for x in search_list if none_value!=get_tag(obj, x, key, none_value)]
#    return [x for x in search_list if key_value==get_tag(obj, x, key, none_value)]
#
#
#def get_map(obj, name, value=None, reset=False):
#    """gets the mapped value specified by the property mapping and returns the attribute value if it doesn't exist
#        gets the map of an Enum defined in the property name_mapping.
#        value can be used to get the map for another value besides the Enum's current one."""
#    if value is None:
#        value=getattr(obj, name)
#    mapping_name=name+_MAPPING_SUFFIX_
#    if hasattr(obj, mapping_name):
#        if reset:
#            reset_property(obj, mapping_name)
#        return getattr(obj, mapping_name)[value]
#    return value
#
##remove?
#def get_inv(obj, name, value):
#    """returns the inverse mapped value (meant for an Enum)"""
#    if hasattr(obj, name+_MAPPING_SUFFIX_):
#        return {v:k for k, v in getattr(obj, name+_MAPPING_SUFFIX_).iteritems()}[value]
#    return value
#
#
#def get_type(obj, name):
#    """returns type of member with given name, with possible override via tag typer"""
#    typer=type(get_member(obj, name))
#    return get_tag(obj, name, "typer", typer)
#
##remove?
#def get_reserved_names(obj):
#    """reserved names not to perform standard logging and display operations on,
#           i.e. members that are tagged as private and will behave as usual Atom members"""
#    return get_all_tags(obj, "private", True)
#
##remove?
#def get_all_params(obj):
#    """all members that are not tagged as private, i.e. not in reserved_names and will behave as agents"""
#    return get_all_tags(obj, key="private", key_value=False, none_value=False)
#
##remove?
#def get_all_main_params(obj):
#    """all members in all_params that are not tagged as sub.
#     Convenience function for more easily custom defining main_params in child classes"""
#    return get_all_tags(obj, 'sub', False, False, get_all_params(obj))
#
##remove?
#def get_main_params(obj):
#    """returns main_params if it exists and all possible main params if it does not"""
#    if hasattr(obj, "main_params"):
#        return obj.main_params
#    return get_all_main_params(obj)
#
#def get_attr(obj, name, none_value=None):
#    """returns the attribute if the obj has it and the none_value if it does not"""
#    return getattr(obj, name, none_value)
#
#def set_attr(self, name, value, **kwargs):
#    """utility function for setting tags while setting value"""
#    setattr(self, name, value)
#    if kwargs!={}:
#        set_tag(self, name, **kwargs)
#
###remove?
#def pass_func(*args, **kwargs):
#    pass
#
##remove?
#def run_func(obj, name, none_func=pass_func, *args, **kwargs):
#    if hasattr(obj, str(name)):
#        return getattr(obj, name)(*args, **kwargs)
#    return none_func(*args, **kwargs)
#
##remove?
#def lowhigh_check(obj, name, value):
#    """can specify low and high tags to keep float or int within a range."""
#    if type(value) in (float, int):
#        metadata=get_metadata(obj, name)
#        if 'low' in metadata:
#            if value<metadata['low']:
#                return metadata['low']
#        if 'high' in metadata:
#            if value>metadata['high']:
#                return metadata['high']
#    return value

##remove?
#def data_save(obj, name, value):
#    """data saving. does nothing if data_save is not defined"""
#    if hasattr(obj, "data_save"):
#        obj.datasave(name, value)
#
##remove?
#def set_log(obj, name, value):
#   """called when parameter of given name is set to value i.e. instr.parameter=value. Customized messages for different types. Also saves data"""
#   if get_tag(obj, name, 'log', True):
#       label=get_tag(obj, name, 'label', name)
#       unit=get_tag(obj, name, 'unit', "")
#       obj_name=get_attr(obj, "name", "NO_NAME")
#       typer=get_type(obj, name)
#       if typer==Coerced:
#           typer=type(getattr(obj, name))
#       if typer==Enum:
#           log_info("Set {instr} {label} to {value} ({map_val})".format(
#                 instr=obj_name, label=label, value=value,
#                 map_val=get_map(obj, name, value)))
#       elif typer in (List, ContainerList):
#           log_info("Set {instr} {label} to {length} list".format(
#               instr=obj_name, label=label, length=shape(value)))
#       elif typer==ndarray:
#           log_info("Set {instr} {label} to {length} array".format(
#               instr=obj_name, label=label, length=shape(value)))
#       elif typer==Dict:
#           log_info("Set {instr} {label} dict".format(instr=obj_name, label=label))
#       elif typer in (Unicode, Str):
#           log_info("Set {instr} {label} to {length} length string".format(instr=obj_name, label=label, length=len(value)))
#       elif typer==Float:
#           unit_factor=get_tag(obj, name, 'unit_factor', 1.0)
#           log_info("Set {instr} {label} to {value} {unit}".format(
#                             instr=obj_name, label=label, value=float(value)/unit_factor, unit=unit), n=3)
#       elif typer==Int:
#           unit_factor=get_tag(obj, name, 'unit_factor', 1)
#           log_info("Set {instr} {label} to {value} {unit}".format(
#                             instr=obj_name, label=label, value=int(value)/unit_factor, unit=unit))
#       else:
#           log_info("Set {instr} {label} to {value} {unit}".format(
#                             instr=obj_name, label=label, value=value, unit=unit))
#   if hasattr(obj, "data_save"):
#       obj.datasave(name, value)
