# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:22:09 2016

@author: thomasaref
"""

from .typedvalue import TypedValue

class Typed(TypedValue):
    """Typed are objects of a particular type"""
    allow_None=True

    def __init__(self, typer, args=None, kwargs=None, factory=None):
        super(Typed, self).__init__(value=None)
        if factory is not None:
            self.default_func=factory
        elif args is not None or kwargs is not None:
            args = args or ()
            kwargs = kwargs or {}
            self.default_func = lambda: typer(*args, **kwargs)
        else:
            self.default_func = lambda: None
        self.typer=typer
