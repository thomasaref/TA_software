# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:52:51 2015

@author: thomasaref

"""

from atom.api import Atom, Property
from taref.core.atom_extension import (UNIT_DICT, private_property, get_reserved_names, get_all_params,
get_all_main_params, lowhigh_check, make_instancemethod, get_type)
from taref.core.extra_setup import extra_setup


class Backbone(Atom):
    """Class combining primary functions for viewer operation"""
    unit_dict=UNIT_DICT

    @private_property
    def reserved_names(self):
        return get_reserved_names(self)

    @private_property
    def all_params(self):
        return get_all_params(self)

    @private_property
    def all_main_params(self):
        return get_all_main_params(self)

    @private_property
    def main_params(self):
        """defaults to all members in all_params that are not tagged as sub.
        Can be overwritten to allow some minimal custom layout control,
        e.g. order of presentation and which members are shown. Use all_main_params to get a list of
        all members that could be in main_params"""
        return self.all_main_params

    @private_property
    def property_dict(self):
        """returns a dict mapping property_names to property_items"""
        return dict([(name, self.get_member(name)) for name in self.all_params if type(self.get_member(name)) is Property])

    @private_property
    def property_names(self):
        """returns a dict mapping property_names to property_items"""
        return self.property_dict.keys()

    @private_property
    def property_values(self):
        """returns a dict mapping property_names to property_items"""
        return self.property_dict.values()

    def extra_setup(self, param, typer):
        extra_setup(self, param, typer)

    def call_func(self, name, **kwargs):
        """calls a func using keyword assignments. If name corresponds to a Property, calls the get func.
        otherwise, if name_mangled func "_get_"+name exists, calls that. Finally calls just the name if these are not the case"""
        if name in self.property_names:
            return self.property_dict[name].fget(self, **kwargs)
        elif name in self.all_params and hasattr(self, "_get_"+name):
            return getattr(self, "_get_"+name)(self, **kwargs)
        return getattr(self, name)(self, **kwargs)

    def __setattr__(self, name, value):
        """uses __setattr__ perform lowhigh_check on all_params"""
        if name in self.all_params:
            value=lowhigh_check(self, name, value)
        super(Backbone, self).__setattr__(name, value)

#    def reset_property(self, name):
#        self.get_member(name).reset(self)
#
#    def reset_properties(self):
#        """resets all  properties"""
#        for item in self.property_dict.values():
#            item.reset(self)

    def instancemethod(self, func):
        """decorator for adding instancemethods defined outside of class"""
        make_instancemethod(self, func)

    def __init__(self, *args, **kwargs):
        """extends __init__ to autoset low and high tags for Range and FloatRange, autoset units for Ints and Floats and allow extra setup"""
        super(Backbone, self).__init__(*args, **kwargs)
        for param in self.all_params:
            typer=get_type(self, param)
            self.extra_setup(param, typer)