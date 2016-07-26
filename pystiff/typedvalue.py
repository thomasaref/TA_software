# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:16:13 2016

@author: thomasaref
"""
from .value import Value

class TypedValue(Value):
    """extends value to allow type checking. defaulter is also updated"""
    typer=None

    def validate(self, value):
        if value is None:
            return True
        return type(value)==self.typer

    def defaulter(self, obj):
        if self.value is None:
            def_func=getattr(obj, "_default_"+self.name, None)
            if def_func is None:
                value=self.def_func()
            else:
                value=def_func()
            if not self.validate(value):
                raise Exception("Wrong type")
            self.value=value

    def __set__(self, obj, value):
        #self.namer(obj)
        obj.notify(self, value)
        if not self.validate(value):
            raise Exception("Wrong type")
        self.set_func(obj, value)
