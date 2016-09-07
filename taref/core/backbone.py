# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:52:51 2015

@author: thomasaref

"""

from atom.api import Atom, Property, AtomMeta, Range, FloatRange, Constant, ReadOnly
from taref.core.atom_extension import (get_reserved_names, get_all_params,
get_all_main_params, lowhigh_check, get_type, get_tag, set_tag)
from taref.core.property import TProperty, private_property
from taref.core.callable import make_instancemethod, setup_callables
from enaml.qt.qt_application import QtApplication
from taref.physics.units import UNIT_DICT#, unitless, dB, dBm
from numpy import float64
from taref.core.interact import Interact

from enaml import imports
with imports():
    from taref.core.agent_e import AutoAgentView, BasicView
    from taref.core.interactive_e import InteractiveWindow, CodeWindow
    from taref.core.log_e import LogWindow


def latex_value(self, param):
    unit=get_tag(self, param, "unit")
    if unit is None:
        if type(getattr(self, param)) in (int, float, float64):
            value=(r"{0:."+str(get_tag(self, param, "precision", 4))+"g}").format(getattr(self, param))
        else:
            value = str(getattr(self, param))
    else:
        value=unit.show_unit(getattr(self, param)/unit, get_tag(self, param, "precision", 4))
    return value


class BackboneAtomMeta(AtomMeta):
    @classmethod
    def extra_setup(cls, param, itm, update_dict):
        TProperty.extra_setup(param, itm, update_dict)

    def __new__(meta, name, bases, dct):
        update_dict={}
        for param, itm in dct.items():
            BackboneAtomMeta.extra_setup(param, itm, update_dict)
        dct.update(update_dict)
        return AtomMeta.__new__(meta, name, bases, dct)

def setup_ranges(self, param, typer):
    """Autosets low/high tags for Range and FloatRange"""
    if typer in [Range, FloatRange]:
        set_tag(self, param, low=self.get_member(param).validate_mode[1][0], high=self.get_member(param).validate_mode[1][1])

def setup_units(self, param, typer):
    """autosets units using unit_dict"""
    unit=get_tag(self, param, "unit")
    if unit is not None:
        unit_dict=getattr(self, "unit_dict", UNIT_DICT)
        if unit in unit_dict:
            set_tag(self, param, unit=unit_dict[unit])

class Backbone(Atom):
    """
    tarefdoc-process-docstring
    Class combining primary functions for viewer operation.
    Extends __init__ to allow extra setup.
    extends __setattr__ to perform low/high check on params"""
    __metaclass__=BackboneAtomMeta

    unit_dict=UNIT_DICT

    app=QtApplication.instance()

    @private_property
    def view_window(self):
        return AutoAgentView(agent=self)

    chief_window=BasicView()

    interact=Interact()

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
        """returns a dict mapping property_names to Property items"""
        return dict([(name, self.get_member(name)) for name in self.all_params if isinstance(self.get_member(name), Property)])

    @private_property
    def property_names(self):
        """returns property_dict.keys() (cached)"""
        return self.property_dict.keys()

    @private_property
    def property_values(self):
        """returns property dict.values() (cached)"""
        return self.property_dict.values()

    def extra_setup(self, param, typer):
        """Performs extra setup during initialization where param is name of parameter and typer is it's Atom type.
        Can be customized in child classes. default extra setup handles units, auto tags low and high for Ranges, and makes Callables into instancemethods"""
        setup_callables(self, param, typer)
        setup_ranges(self, param, typer)
        setup_units(self, param, typer)

#    def call_func(self, name, **kwargs):
#        """calls a func using keyword assignments. If name corresponds to a Property, calls the get func.
#        otherwise, if name_mangled func "_get_"+name exists, calls that. Finally calls just the name if these are not the case"""
#        if name in self.property_names:
#            return self.property_dict[name].fget(self, **kwargs)
#        elif name in self.all_params and hasattr(self, "_get_"+name):
#            return getattr(self, "_get_"+name)(self, **kwargs)
#        return getattr(self, name)(**kwargs)

    def __setattr__(self, name, value):
        """uses __setattr__ perform lowhigh_check on all_params"""
        if name in self.all_params:
            value=lowhigh_check(self, name, value)
        super(Backbone, self).__setattr__(name, value)

    def instancemethod(self, func):
        """decorator for adding instancemethods defined outside of class (meant for Callables)"""
        make_instancemethod(self, func)

    def __init__(self, **kwargs):
        """extends __init__ to allow extra setup for all params"""
        super(Backbone, self).__init__(**kwargs)
        for param in self.all_params:
            typer=get_type(self, param)
            self.extra_setup(param, typer)

    def latex_table_entry(self, param=None, value=None, expression=None, comment=None, design=None, label=None):
        if param is None:
            return [self.name.replace("_", " "),  r"Label", r"Value",  r"Design", r"Comment"]

        #tex_str=get_tag(self, param, "tex_str")
        #if tex_str is None:
        #    tex_str=param.replace("_", " ")
        if label is None:
            label=get_tag(self, param, "label", r"{}")
        if value is None:
            value=latex_value(self, param)
        if expression is None:
            expression=get_tag(self, param, "expression", param.replace("_", " "))
        if comment is None:
            comment=get_tag(self, param, "desc", r"{}")
        if design is None:
            design=get_tag(self, param, "design", r"{}")
        return [expression, label, value, design, comment]


    def latex_table(self, param_list=None, design=None):
        if param_list is None:
            param_list=self.main_params
        lt=[self.latex_table_entry()]
        for param in param_list:
            if design is None:
                lt.append(self.latex_table_entry(param))
            else:
                design_param=latex_value(design, param)
                lt.append(self.latex_table_entry(param, design=design_param))
        return lt

    def latex_table2(self, param_list=None):
        if param_list is None:
            param_list=self.main_params
        lt = [[self.name,  r"Value",  r"Expression", r"Comment"],]
        for param in param_list:
            unit=get_tag(self, param, "unit")
            #print param, type(getattr(self, param)) in (int, float, float64)
            if type(getattr(self, param)) in (int, float, float64):
                format_str=getattr(unit, "format_str", r"{0:.3g}")
            else:
                format_str=getattr(unit, "format_str", "{0}")
            print param, format_str
            if unit is not None:
                unit.show_unit()
                value=getattr(self, param)/unit
            else:
                value=getattr(self, param)
            tex_str=get_tag(self, param, "tex_str")
            if tex_str is None:
                tex_str=param.replace("_", " ")
            label=get_tag(self, param, "label")
            if label is not None:
                tex_str=label+", "+tex_str
            lt.append([tex_str,  format_str.format(value),
                       get_tag(self, param, "expression", r"{}"), get_tag(self, param, "desc", r"{}")])
        return lt