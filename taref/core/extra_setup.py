# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 22:29:11 2016

@author: thomasaref
"""
from atom.api import Callable, Range, FloatRange
from taref.core.atom_extension import  get_tag, set_tag
from taref.core.callable import make_instancemethod
from taref.core.log import log_debug
from taref.physics.units import UNIT_DICT

def setup_callables(self, param, typer):
    """Auto makes Callables into instance methods"""
    if typer == Callable:
        func=getattr(self, param)
        if func is not None:
            make_instancemethod(self, func)

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
