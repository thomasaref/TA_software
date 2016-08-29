# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:16:13 2016

@author: thomasaref
"""
from .value import Value

class TypedValue(Value):
    """extends value to allow type checking. defaulter is also updated"""
    typer=None
    allow_None=False

    def default_func(self):
        return self.typer()

    def validate(self, value):
        if value is None:
            return self.allow_None
        return type(value)==self.typer

#    def defaulter(self, obj):
#        if self.uninitialized:
#            def_func=getattr(obj, "_default_"+self.name, None)
#            if def_func is None:
#                value=self.def_func()
#            else:
#                value=def_func()
#            self.__set__(obj, value)

    def __set__(self, obj, value):
        #self.namer(obj)
        if self.uninitialized:
            self.uninitialized=False
            self.set_parent(obj)
        obj.notify({"obj" : self, "value" : value, "op" : "set"})
        if not self.validate(value):
            raise Exception("Wrong type")
        self.set_func(obj, value)