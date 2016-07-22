# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:51:44 2016

@author: thomasaref
"""

from atom.api import Atom, Float
from collections import OrderedDict

#class Test(Atom):
#    a=Float().tag(blue="good")

class Value(object):
    def tag(self, **kwargs):
        self.metadata.update(kwargs)
        return self

class Property(Value):
    def __init__(self, fget=None, fset=None, cached=True):
        self.fget=fget
        self.fset=fset
        self.cached=cached
        self.metadata={"typer":int}

    def __get__(self, obj, typ):
        print self, obj, typ
        return self.fget(self)

class Int(Value):
    coercer=int
    def __init__(self, value=0):
        self.value=value
        self.metadata={}


    def __get__(self, obj, typ=None):
        print "got things"
        return self.value

    def __set__(self, obj, value):
        obj.notify(self, value)
        self.value=self.coercer(value)

class myAtom(object):

    @classmethod
    def get_member(cls, name):
        return cls.__dict__[name]

    @classmethod
    def members(cls):
        return dict([(name, member) for name, member in cls.__dict__.items() if hasattr(member, "tag")])

    def set_tag(self, name, **kwargs):
        self.get_member(name).metadata.update(kwargs)

    def get_tag(self, name, tag, none_value=None):
        return self.get_member(name).metadata.get(tag, none_value)



class test(myAtom):
    b=3
    c=Int().tag(five=5, typer=int)

    def notify(self, *args):
        print "parent", args

    @Property
    def blah(self):
        return 2

#    def __init__(self, a=2):
#        #self.a=a
#        self.get_member("c").parent=self#

        #super(test, self).__init__(a=a)




#a=Test()
b=test()
print b.c
print b.blah
b.c=4
print b.c
print b.get_member("c")
print b.get_member("c").metadata
print b.members()
b.set_tag("c", g=2)
print b.get_tag("c", "g")
print b.get_tag("c", "g2")
print b.get_tag("c", "five")

from taref.core.shower import shower
from taref.core.api import get_main_params, get_all_tags
print get_main_params(b)
print get_all_tags(b, key="private", key_value=False, none_value=False)
print b.members()
shower(b)

#print dir(a)
#print dir(b)
#print a.__atom_members__
#print b.__dict__
#b.set_tag("a", blue="good")
#print b.get_tag("a", "blue")
#print b.get_tag("a", "red")
#print b.members()
#print b.get_member("a")
#print b.__dict__
#print b.members()
