# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 14:40:44 2016

@author: thomasaref
"""
from .typedvalue import TypedValue
from collections import OrderedDict
from .coerced import Coerced

class NotifyValue(TypedValue):
    """Notifies on operations on submembers"""
    def get_func(self, obj, typ):
        return self

class NDict(NotifyValue):
    typer=dict

    def __setitem__(self, key, value):
        self.parent.notify({"obj" : self, "key" : key, 
               "value" : value, "op" : "setitem"})
        self.value[key]=value

    def __getitem__(self, key):
        return self.value[key]
    
class NODict(NDict):
    typer=OrderedDict

class NotifyList(list):
    #def __init__(self, parent):
    #    self.parent=parent

    def __setitem__(self, key, value):
        self.parent.notify({"obj" : self, "key" : key, 
               "value" : value, "op" : "setitem"})
        super(NotifyList, self).__setitem__(key, value)
        
class NList(Coerced):
    typer=NotifyList
    coercer=NotifyList

    def defaulter(self, obj):
        """determines default value if value is None"""
        if self.uninitialized:
            self.uninitialized=False
            if self.value is not None:
                self.__set__(obj, self.value)
            else:
                def_func=getattr(obj, "_default_"+self.name, self.default_func)
                value=def_func()
                self.__set__(obj, value)
            self.parent=obj
    
    def __init__(self, value=None):
        if value is None:
            self.value=value
        else:
            self.value=self.coercer(value)
    

        