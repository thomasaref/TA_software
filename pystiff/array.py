# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:44:38 2016

@author: thomasaref
"""
from .typedvalue import TypedValue
from .coerced import Coerced
from numpy import array, ndarray
from collections import OrderedDict

class List(TypedValue):
    typer=list

    #def default_func(self):
    #    return []

class Tuple(TypedValue):
    typer=tuple

    #def default_func(self):
    #    return ()

class Array(TypedValue):
    typer=ndarray

    def default_func(self):
        return array([])

class CArray(Coerced):
    def __init__(self, value=None):
        if value is None:
            value=[]
        super(CArray, self).__init__(typer=ndarray, args=(value,), coercer=array)

class Dict(TypedValue):
    typer=dict

    #def default_func(self):
    #    return dict()

class Set(TypedValue):
    typer=set

    #def default_func(self):
    #    return set()

#class OOrderedDict(OrderedDict):

class ODict(TypedValue):
    typer=OrderedDict

    def get_func(self, obj, typ):
        print obj, typ
        return self

    def __setitem__(self, key, value):
        self.parent.notify(self, "yoyo")#, key, value
        self.value[key]=value
        #super(OOrderedDict, self).__setitem__(key, value)

    #def default_func(self):
    #    return OrderedDict()

