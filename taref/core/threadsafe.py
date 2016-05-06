# -*- coding: utf-8 -*-
"""
Created on Fri May  6 16:10:30 2016

@author: thomasaref

thread safe function calls for use with threaded applications
"""
from enaml.application import Application, deferred_call#, schedule
from taref.core.atom_extension import set_attr, set_tag
from taref.core.log import log_debug

def safe_call(func, *args, **kwargs):
    """utility function for safely calling functions that doesn't return anything"""
    if Application.instance() is None:
        return func(*args, **kwargs)
    deferred_call(func, *args, **kwargs)

def safe_setattr(obj, name, value):
    """thread safe sets attribute if enaml application is running. otherwise, just does setattr"""
    safe_call(setattr, obj, name, value)

def safe_set_attr(obj, name, value, **kwargs):
    """thread safe sets attribute if enaml application is running. otherwise, just does setattr"""
    safe_call(set_attr, obj, name, value, **kwargs)

def safe_log_debug(*args, **kwargs):
    """thread safe call to logging"""
    safe_call(log_debug, *args, **kwargs)

def safe_set_tag(obj, name, **kwargs):
    safe_call(set_tag, obj, name, **kwargs)