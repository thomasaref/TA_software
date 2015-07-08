# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 18:59:55 2015

@author: thomasaref
"""

from atom.api import Atom, Int, Float, Coerced

class blah(Atom):
    a=Float(2)
    b=Coerced(int) #(2)
    c=Int(2)
    
    def _observe_a(self, change):
        print change
    
d=blah()

#print d.a, d.b, d.c
#print d.a/2, d.b/2
#print d.a/d.b, d.c/d.b

d.a=5
d.a=10
d.a=10
d.b="3"
print d.b
#d.c=3.4