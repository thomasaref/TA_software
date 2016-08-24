# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 13:14:30 2016

@author: thomasaref
"""

from .typedvalue import TypedValue


class Int(TypedValue):
    """a type checked integer"""
    typer=int

    def default_func(self):
        return 0

class Float(TypedValue):
    """a type checked float"""
    typer=float

    def default_func(self):
        return 0.0

class Complex(TypedValue):
    typer=complex

    def default_func(self):
        return 0.0+0.0j

class Long(TypedValue):
    typer=long

    def default_func(self):
        return 0L




