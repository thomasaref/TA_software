# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 19:12:36 2016

@author: thomasaref

A collection of utility functions that extend Atom's functionality, used heavily by taref other modules.
To maintain compatibility with Atom classes, these are defined as standalone functions rather than extending the class.
Runtime also seem slightly better as standalone functions than as an extended class
"""

from atom.api import Coerced, Enum, Float, Int, Unicode, List, Dict, Str, ContainerList
from numpy import shape, ndarray
from taref.core.log import log_info, log_debug

_MAPPING_SUFFIX_="_mapping"

def get_value_check(obj, name, value):
        """Coerces value when getting. For Enum, this allows the inverse mapping."""
        if get_type(obj, name) is Enum:
            return get_inv(obj, name, value)
        else:
            return type(getattr(obj, name))(value)

def set_tag(obj, name, **kwargs):
    """sets the tag of a member using Atom's built in tag functionality"""
    obj.get_member(name).tag(**kwargs)

def set_all_tags(obj, **kwargs):
    """Shortcut to use Atom's tag functionality to set metadata on members not marked private, i.e. all_params. This is an easy way to set the same tag on all params"""
    for param in get_all_params(obj):
        set_tag(obj, param, **kwargs)

def get_tag(obj, name, key, none_value=None):
    """Shortcut to retrieve metadata from an Atom member which also returns a none_value if the metadata does not exist.
       This is an easy way to get a tag on a particular member and provide a default if it isn't there."""
    #log_debug(name)
    metadata=obj.get_member(name).metadata
    if metadata is None:
        return none_value
    return metadata.get(key, none_value)

def get_all_tags(obj, key, key_value=None, none_value=None, search_list=None):
    """returns a list of names of parameters with a certain key_value
       Shortcut retrieve members with particular metadata. There are several variants based on inputs.
           * With only obj and key specified, returns all member names who have that key
           * with key_value specified, returns all member names that have that key set to key_value
           * with key_value and none_value specified equal, returns all member names that have that key set to key_value or do not have the tag
           * specifying search list limits the members searched
           * Finally, if key_value is none, returns those members not matching none_value"""
    if search_list is None:
        search_list=obj.members()
    if key_value is None:
        return [x for x in search_list if none_value!=get_tag(obj, x, key, none_value)]
    return [x for x in search_list if key_value==get_tag(obj, x, key, none_value)]

def get_type(obj, name):
    """returns type of member with given name, with possible override via tag typer"""
    typer=type(obj.get_member(name))
    return get_tag(obj, name, "typer", typer)


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
           log_info("Set {instr} {label} to {value:g} {unit}".format(
                             instr=obj_name, label=label, value=float(value), unit=unit), n=1)
       elif typer==Int:
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=int(value), unit=unit))
       else:
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=value, unit=unit))


def check_initialized(self, change):
    if change["type"]=="update":
        if get_tag(self, change["name"], "initialized", False):
            raise Exception("{0} already initialized".format(change["name"]))

