# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:52:51 2015

@author: thomasaref
"""

from inspect import getmembers

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
    """returns the metadata of a member if it exists and generates an appropriately indexed empty dictionary if it does not"""
    member=get_member(obj, name)
    if hasattr(member, "metadata"):
        if member.metadata is None:
            member.metadata={}
        return member.metadata
    if not hasattr(obj, "_metadata"):
        obj._metadata={name:{}}
    if obj._metadata.get(name, None) is None:
        obj._metadata[name]={}
    return obj._metadata[name]

def set_tag(obj, name, **kwargs):
    """sets the tag of a member using Atom's built in tag functionality or
    the object wide metadata dictionary for non-Atom objects"""
    member=get_member(obj, name)
    if hasattr(member, "tag"):
        member.tag(**kwargs)
    else:
        metadata=get_metadata(obj, name)
        metadata.update(**kwargs)


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
    if key_value==None:
        return [x for x in search_list if none_value!=get_tag(obj, x, key, none_value)]
    return [x for x in search_list if key_value==get_tag(obj, x, key, none_value)]

def get_map(obj, name, none_map={}):
    """gets the mapped value specified by dictionary mapping and uses none_map if it doesn't exist"""
    item=getattr(obj, name)
    mapping=get_tag(obj, name, "mapping", none_map)
    return mapping.get(item, item)

def get_type(obj, name):
    """returns type of parameter with given name"""
    typer=type(get_member(obj, name))
    #if typer in (Coerced, Instance, Typed):
    #     typer=type(getattr(obj, name)) #typer=get_member.validate_mode[1][1]
    return get_tag(obj, name, "typer", typer)


#def get_boss(obj):
#    """link to boss of object and uses base boss if none exists"""
#    if hasattr(obj, "boss"):
#        return obj.boss
#    return boss
    
#def get_abort(obj):
#    """shortcut to boss' abort if boss exists and default if not"""
#    if hasattr(obj, "boss"):
#        return obj.boss.abort
#    return get_boss(obj).abort

def get_reserved_names(obj):
    """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
    return get_all_tags(obj, "private", True)    

def get_all_params(obj):
    """all members that are not tagged as private, i.e. not in reserved_names and will behave as Bases"""
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
    if hasattr(obj, str(name)):
        return getattr(obj, name)
    return none_value
    
    
#def get_name(obj, default_name="NO NAME"):
#    if hasattr(obj, "name"):
#        return obj.name
#    return default_name
#    
#def get_view(obj, default_view="Auto"):
#    if hasattr(obj, "view"):
#        return obj.view
#    return default_view