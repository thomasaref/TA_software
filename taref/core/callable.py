# -*- coding: utf-8 -*-
"""
Created on Fri May  6 16:13:43 2016

@author: thomasaref

Utilities associated with Callables and functions
"""
from functools import wraps
from types import MethodType
from taref.core.log import log_debug
from atom.api import Callable

def log_func(func, log=False, log_message=None, threaded=False):
    """function decorator that enables logging and threading. Doesn't return value from thread."""
    if log_message is None:
        log_message="RAN: {0} {1}"
    @wraps(func)
    def new_func(self, *args, **kwargs):
        if new_func.log:
            log_debug(new_func.log_message.format(getattr(self, "name", ""), new_func.func_name), n=2)
        for param in new_func.run_params[len(args):]:
            if param not in kwargs:
                kwargs[param]=getattr(self, param)
        if new_func.threaded: #doesn't return value from thread
            names=[thread.name for thread in self.thread_list if new_func.func_name in thread.name]
            return self.add_thread("{0} {1}".format(new_func.func_name, len(names)), func, *((self,)+args), **kwargs)
        else:
            return func(self, *args, **kwargs)
        return func(self, *args, **kwargs)
    new_func.run_params=get_run_params(func, skip=1)
    new_func.log=log
    new_func.log_message=log_message
    new_func.threaded=threaded
    return new_func

class LogFunc(object):
    """disposable decorator class that exposes logging and threading options in log_func"""
    def __init__(self, **kwargs):
        self.threaded=kwargs.get("threaded", False)
        self.log=kwargs.get("log", False)
        self.log_message=kwargs.get("log_message", None)

    def __call__(self, func):
        return log_func(func, log=self.log, log_message=self.log_message, threaded=self.threaded)

def make_instancemethod(obj, func, name=None):
    """decorator for adding func as instancemethod to obj"""
    if name is None:
        name=func.func_name
    new_func=log_func(func)
    setattr(obj, name, MethodType(new_func, obj, type(obj)))
    return func

class instancemethod(object):
    """disposable decorator object for instancemethods defined outside of Atom class"""
    def __init__(self, obj, name=None):
        self.name=name
        self.obj=obj

    def __call__(self, func):
        make_instancemethod(self.obj, func, self.name)
        return func

def get_run_params(f, skip=1):
    """returns names of parameters a function will call, skips first parameter if skip_first is True"""
    if hasattr(f, "run_params"):
        return f.run_params#[skip:]
    argcount=f.func_code.co_argcount
    return list(f.func_code.co_varnames[skip:argcount])

class tag_callable(object):
    """disposable decorator class that returns a Callable tagged with kwargs"""
    default_kwargs={}
    def __init__(self, **kwargs):
        """adds default_kwargs if not specified in kwargs"""
        for key in self.default_kwargs:
            kwargs[key]=kwargs.get(key, self.default_kwargs[key])
        self.kwargs=kwargs

    def __call__(self, func):
        return Callable(func).tag(**self.kwargs)

class log_callable(tag_callable):
    def __call__(self, func):
        new_func=LogFunc(**self.kwargs)(func)
        return super(log_callable, self).__call__(new_func)

class thread_callable(log_callable):
    default_kwargs=dict(threaded=True)