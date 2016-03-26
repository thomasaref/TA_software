# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:53:23 2016

@author: thomasaref
"""

class Observer(object):
    def __init__(self, name):
        self.name=name
        #self.instr=instr
        #self.value=instr.getValue(name)

    def __call__(self):
        def func(obj):
            return obj._a
        return property(fget=func)

class Bond(object):
    def __init__(self):
        self._members={}
        for name in dir(self.__class__):
            if not name.startswith("_"):
                attr=getattr(self.__class__, name)
                if isinstance(attr, property):
                    self._members[name]=attr

    def members(self):
        return self._members

    def get_member(self, name):
        return self._members.get(name, None)

class Test(Bond):
    def __init__(self):
        self._a=2
        super
        self._members={}
        for name in dir(self.__class__):
            if not name.startswith("_"):
                attr=getattr(self.__class__, name)
                if isinstance(attr, property):
                    self._members[name]=attr

    @property
    def a(self):
        return self._a

    def b(self):
        print "ji"

    def members(self):
        return self._members

    def get_member(self, name):
        return self._members.get(name, None)


t=Test()
#print t.a
print dir(t.__class__)
print t.__class__.a
print t.members
print t.members()
print t.get_member("a")
print t.get_member("b")