# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 19:12:36 2016

@author: thomasaref
"""

from atom.api import Property, Callable

_MAPPING_SUFFIX_="_mapping"

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
    obj.get_member(name).reset(obj)

def get_map(obj, name, value=None, reset=False):
    """gets the mapped value specified by the property mapping and returns the attribute value if it doesn't exist
        gets the map of an Enum defined in the property name_mapping.
        value can be used to get the map for another value besides the Enum's current one."""
    if value is None:
        value=getattr(obj, name)
    mapping_name=name+_MAPPING_SUFFIX_
    if hasattr(obj, mapping_name):
        if reset:
            obj.get_member(mapping_name).reset(obj)
        return getattr(obj, mapping_name)[value]
    return value





class tag_Property(object):
    """disposable decorator class that returns a cached Property tagged with kwargs"""
    def __init__(self, cached=True, **kwargs):
        self.kwargs=kwargs
        self.cached=cached

    def __call__(self, func):
        return Property(func, cached=self.cached).tag(**self.kwargs)

class tag_Callable(object):
    """disposable decorator class that returns a Callable tagged with kwargs"""
    def __init__(self, **kwargs):
        self.kwargs=kwargs

    def __call__(self, func):
        return Callable(func).tag(**self.kwargs)