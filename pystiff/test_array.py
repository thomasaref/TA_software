# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 14:51:00 2016

@author: thomasaref
"""

from pystiff.api import Object, Int, Coerced, Typed, List, Tuple, Array, CArray, Set, Dict, ODict

class Test_Array(Object):
    #a=List()
    #b=Tuple()
    #c=Array()
    #d=CArray()
    #e=Set()
    #f=Dict()
    g=ODict()

a=Test_Array()
a.g[2]=1
print a.g
print a.a, a.b, a.c, a.d, a.e, a.f, a.g
print type(a.a), type(a.b), type(a.c), type(a.d), type(a.e), type(a.f), type(a.g)
a.d=[1,2]
print a.d
a.d=[2,3]
print a.d
a.g[2]=5
a.g[3]=6
print a.g
a.c=[1,2]
