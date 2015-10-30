# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 16:39:12 2015

@author: thomasaref
"""

from functools import wraps
from atom.api import Callable

print Callable

def f(**tags):
    def myfunc(fn):
        @wraps(fn)
        def inf(*args, **kwargs):
            print fn, "ran"
            return fn(*args, **kwargs)
        inf.metadata=tags
        return inf
    return myfunc
    
@f(hotdog="good")
def g(a=2):
    return a

print g()
print g(5)
print g.metadata
    
class A(object):
    _a=0
    d=dict(a=1, b=2, c=3)


    @f()    
    def get_a(self):
        return self._a
        
    
    @property
    def c(self):
        return self._a #2 #self.d['a']

    @c.setter
    def c(self, value):
        self._a=value
print A        
a=A()
print a.get_a()
a.c=4
