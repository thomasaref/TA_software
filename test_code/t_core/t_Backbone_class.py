# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:47:35 2015

@author: thomasaref
"""

from taref.core.backbone import Backbone, private_property, tagged_property, tagged_callable
from atom.api import Int, Float, Enum, List, Range, FloatRange


class Test(Backbone):
    a=Int()
    b=Float().tag(sub=True)
    c=Int().tag(private=True)
    d=Float().tag(private=True)
t=Test()
print
print """all_params returns all members not tagged with private=True"""
print 'print t.all_params'
print t.all_params
print
print """all_main_params returns all params not tagged with sub=True"""
print 'print t.all_main_params'
print t.all_main_params
print
print """reserved_names returns all members tagged with private=True. """
print 't.reserved_names'
print t.reserved_names
print
print "main_params defaults to those params not tagged sub=True. in this case a"
print 't.main_params'
print t.main_params

class Test2(Test):
    @private_property
    def main_params(self):
        return ['b', 'c']
t=Test()
print """main_params can be overwritten allowing custom ordering of members"""
print t.main_params




print
class Test(Backbone):
    a=Float()
    b=Float().tag(unit="um")
    c=Float().tag(unit="um", unit_factor=3.0)
t=Test()
print 't.unit_dict'
print t.unit_dict
print "In this case, you can see how tagging b with unit='um' autosets the unit_factor to 1.0e-6"
print 't.get_metadata("a")'
print t.get_metadata("a")
print 't.get_metadata("b")'
print t.get_metadata("b")
print 't.get_metadata("c")'
print t.get_metadata("c")

class Test(Backbone):
    @tagged_property(unit="5")
    def a(self):
        return 4
    @private_property
    def b(self):
        return 4
t=Test()
print t.property_dict
print t.property_names
print t.property_items

class Test(Backbone):
    a=Int()
    b=Float().tag(sub=True, unit="um", low=1.0)
    c=Int().tag(private=True)
    d=Float().tag(private=True)
t=Test()
print t.b
t.b=0.0
print t.b

class Test(Backbone):
    a=Int()
    @tagged_callable(desc="my function")
    def my_f(self, a):
        print "ran my_f and a={}".format(a)

    def _observe_a(self, change):
        print change
t=Test()
t.my_f()
t.my_f(t, 4)
t.my_f(a=4)

class Test(Backbone):
    a=Range(0, 3, 1)
    b=FloatRange(0.0, 3.0, 1.0)
t=Test()
print t.get_metadata("a")
print t.get_metadata("b")

def test_get_map():
    class Test(Backbone):
        a=Enum(1,2,3)
        b=List(default=[1,2,3])
        @property
        def a_mapping(self):
            return {1:"a", 2:"b", 3:"c"}

    t=Test()
    print t.a, t.get_map("a"), t.get_map("a", 3)

