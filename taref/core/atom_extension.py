# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 19:12:36 2016

@author: thomasaref
"""

from atom.api import Property, Callable, Coerced, Atom
from taref.core.log import log_debug
_MAPPING_SUFFIX_="_mapping"

#def new_func(self):
#    print self.unit_factor
#
#class Floater(Atom):
#    a=Range()
#    desc=Unicode()
#    unit=Unicode()
#    show_uvalue=Bool(False)
#    unit_factor=Float(1.0)
#    minimum=Float()
#    maximum=Float()
#    new_func=Callable(new_func)
#
#    def __init__(self, **kwargs):
#        super(Floater, self).__init__(**kwargs)
#        for name in self.members():
#            if type(self.get_member(name)) ==Callable:
#                setattr(self, name, MethodType(getattr(self, name), self, type(self)))
#
#    def test_func(self):
#        pass
#
#a=Floater()
#
#print a.test_func
##a.new_func=MethodType(new_func, a, type(a))
#
##print help(type(a.test_func))
#print a.new_func
#a.new_func()
#print a.members()
from types import MethodType
def make_instancemethod(obj, func):
    setattr(obj, func.func_name, MethodType(func, obj, type(obj)))

def get_run_params(f, skip_first=True):
    """returns names of parameters a function will call"""
    if hasattr(f, "run_params"):
        return f.run_params
    argcount=f.func_code.co_argcount
    if skip_first:
        return list(f.func_code.co_varnames[1:argcount])
    return list(f.func_code.co_varnames[0:argcount])

def get_member(obj, name):
    """returns a member if get_member exists and the attribute itself if it does not.
    Returns the member of obj specified by name. This allows easy access to member functions and is included in the Atom api"""
    if hasattr(obj, "get_member"):
        return obj.get_member(str(name))
    return getattr(obj, str(name))

def get_metadata(obj, name):
    """returns the metadata of a member if it exists and generates an empty dictionary if it does not
        Returns the metadata dictionary of member of obj specified by name.
    This allows easy access to metadata and autogenerates an empty dictionary if metadata is None."""
    if isinstance(obj, Atom):
        member=obj.get_member(name)
        if member.metadata is None:
            member.metadata={}
        return member.metadata
    return {}

def get_tag(obj, name, key, none_value=None):
    """returns the tag key of a member name an returns none_value if it does not exist
        Shortcut to use Atom's retrive particular metadata which returns a none_value if it does not exist.
    This is an easy way to get a tag on a particular member and provide a default if it isn't there."""
    member=obj.get_member(name)
    if member.metadata is None:
        member.metadata={}
    return member.metadata.get(key, none_value)

def get_type(obj, name):
    """returns type of member with given name, with possible override via tag typer"""
    typer=type(obj.get_member(name))
    return get_tag(obj, name, "typer", typer)

def reset_property(obj, name):
    """shortcut to atom's property reset functionality"""
    get_member(obj, name).reset(obj)

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

class tag_Property(object):
    """disposable decorator class that returns a cached Property tagged with kwargs"""
    def __init__(self, cached=True, **kwargs):
        self.kwargs=kwargs
        self.cached=cached

    def __call__(self, func):
        return Property(func, cached=self.cached).tag(**self.kwargs)

def private_property(fget):
    """ A decorator which converts a function into a cached Property tagged as private.
    Improves performance greatly over property!
    """
    return Property(fget, cached=True).tag(private=True)

class tag_Callable(object):
    """disposable decorator class that returns a Callable tagged with kwargs"""
    def __init__(self, **kwargs):
        self.kwargs=kwargs

    def __call__(self, func):
        return Callable(func).tag(**self.kwargs)


def set_tag(obj, name, **kwargs):
    """sets the tag of a member using Atom's built in tag functionality"""
    obj.get_member(name).tag(**kwargs)

def set_all_tags(obj, **kwargs):
    """set all parameters tags using keyword arguments.
        Shortcut to use Atom's tag functionality to set metadata on members not marked private, i.e. all_params.
    This is an easy way to set the same tag on all params"""
    for param in get_all_params(obj):
        set_tag(obj, param, **kwargs)

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

def get_reserved_names(obj):
    """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
    return get_all_tags(obj, key="private", key_value=True)

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