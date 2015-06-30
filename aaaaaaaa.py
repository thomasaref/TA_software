# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 16:39:12 2015

@author: thomasaref
"""

class A(object):
    _a=0
    d=dict(a=1, b=2, c=3)
    
    def get_a(self):
        return self._a
        
    def set_a(self, value):
        if value<5:        
            self._a=value

    a=property(fget=get_a, fset=set_a)
    
    #@property
    def c(self):
        return self.d['a']

   
        
a=["b", "c", "d"]
print range(len(a))# [i for n,d in enumerate(a)]