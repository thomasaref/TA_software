# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:24:28 2016

@author: thomasaref
"""
import collections

class metacls(type):
    d=2
    
    def dd(self):
        pass 
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()
        
    def __new__(mcs, name, bases, ddict):
        print mcs
        print name
        print bases
        print ddict
        ddict['foo'] = 'metacls was here'
        return type.__new__(mcs, name, bases, ddict)

class sub(object):        
    dd=4

    __metaclass__=metacls
    d=2
    a=1
class test(object):
    b=sub()
    
    def __init2__(self):
        self.c=sub()

a=test()
print a.__dict__
#print a.foo