# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:21:36 2016

@author: thomasaref
"""
from .value import Value

class Coerced(Value):
    def __init__(self, typer, args=(), kwargs={}, factory=None, coercer=None):
        super(Coerced, self).__init__(value=None)
        if factory is not None:
            self.def_func=factory
        else:
            self.def_func = lambda: coercer(*args, **kwargs)
        self.coercer=coercer or typer

    def get_func(self, obj, typ):
        self.defaulter(obj)
        return self.value

    def set_func(self, obj, value):
        self.value=self.coercer(value)
