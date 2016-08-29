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

class Tuple(TypedValue):
    typer=tuple

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

class Set(TypedValue):
    typer=set

class ODict(TypedValue):
    typer=OrderedDict

