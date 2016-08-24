# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:21:36 2016

@author: thomasaref
"""
from .value import Value

class Coerced(Value):
    def __init__(self, typer, args=(), kwargs={}, factory=None, coercer=None):
        super(Coerced, self).__init__(value=None)
        self.typer=typer
        self.coercer=coercer or typer
        if factory is not None:
            self.default_func=factory
        else:
            self.default_func = lambda: self.coercer(*args, **kwargs)

    #def get_func(self, obj, typ):
    #    self.defaulter(obj)
    #    return self.value

    def set_func(self, obj, value):
        self.value=self.coercer(value)
