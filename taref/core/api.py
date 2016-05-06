# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:10:39 2016

@author: thomasaref
"""

#tag related
from .atom_extension import set_tag, set_all_tags, get_tag, get_all_tags, get_type
from .atom_extension import get_reserved_names, get_all_params, get_all_main_params, get_main_params, set_attr,set_log, check_initialized

#thread safe calls
from .threadsafe import safe_call, safe_setattr, safe_set_attr, safe_log_debug, safe_set_tag

#value checking/Enum related
from .atom_extension import get_value_check, lowhigh_check, set_value_map, get_map, get_inv

#Property related
from .property import (get_property_names, get_property_values, reset_property, reset_properties, private_property, tag_property,
                       SProperty, TProperty, s_property, t_property)

#Callable related
from .callable import log_func, make_instancemethod, instancemethod, get_run_params, tag_callable, log_callable, thread_callable

from .agent import Operative, Spy, Agent

from .shower import shower

from .universal import sqze, cap_case, read_text, write_text, Array, do_nothing, pass_factory, msg

from .log import log_debug, log_info, log_warning