# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 13:14:30 2016

@author: thomasaref
"""

from .typedvalue import TypedValue


class Int(TypedValue):
    """a type checked integer"""
    typer=int
    
class Float(TypedValue):
    """a type checked float"""
    typer=float
