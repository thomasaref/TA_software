# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:47:35 2015

@author: thomasaref
"""

from taref.core.backbone import Backbone
from atom.api import Int, Float, Enum, List


def test_all_params():
    class Test(Backbone):
        a=Int()
        b=Float()
        c=Int().tag(private=True)
    t=Test()        
    print """all_params returns all members not tagged with private=True"""
    print t.all_params
test_all_params()

def test_all_main_params():
    class Test(Backbone):
        a=Int()
        b=Float().tag(sub=True)
        c=Int().tag(private=True)
    t=Test()        
    print """all_main_params returns all params not tagged with sub=True"""
    print t.all_main_params
test_all_main_params()

def test_reserved_names():
    class Test(Backbone):
        a=Int()
        b=Float().tag(sub=True)
        c=Int().tag(private=True)
        d=Float().tag(private=True)
    t=Test()        
    print """reserved_names returns all members tagged with private=True. """
    print t.reserved_names
test_reserved_names()


def test_get_metadata():
    class Test(Backbone):
        a=Int()
        b=Float().tag(sub=True, unit="um")
        c=Int().tag(private=True)
        d=Float().tag(private=True)
    t=Test()        
    print """get_metadata returns returns the metadata dictionary of a member. 
    In this case, you can see how tagging b with unit='um' autosets the unit_factor to 1.0e-6"""
    print t.get_metadata("b")
    print t.get_metadata("d")
        
test_get_metadata()

def test_unit_dict():
    class Test(Backbone):
        a=Int()
        b=Float().tag(sub=True, unit="um")
        c=Int().tag(private=True)
        d=Float().tag(private=True)
    t=Test()        
    print """get_metadata returns returns the metadata dictionary of a member. 
    In this case, you can see how tagging b with unit='um' autosets the unit_factor to 1.0e-6"""
    print t.unit_dict
test_unit_dict()

def test_lowhigh_check():
    class Test(Backbone):
        a=Int()
        b=Float().tag(sub=True, unit="um", low=1.0)
        c=Int().tag(private=True)
        d=Float().tag(private=True)
    t=Test()        
    print """get_metadata returns returns the metadata dictionary of a member. 
    In this case, you can see how tagging b with unit='um' autosets the unit_factor to 1.0e-6"""
    print t.b
    print t.lowhigh_check("b", 0)  
    t.b=0.0
    
test_lowhigh_check()
    
def test_Backbone_main_params():
    class Test(Backbone):
        a=Int()
        b=Float().tag(sub=True)
        c=Int().tag(private=True)        
    a=Test()
    print "main_params defaults to those params not tagged sub=True. in this case a and b"
    print a.main_params
    class Test(Backbone):
        a=Int()
        b=Float().tag(sub=True)
        c=Int().tag(private=True)
        
        def _default_main_params(self):
            return ['b', 'c']

    a=Test()
    print """Using Atom's _default functionality, main_params can be overwritten.
           this allows custom ordering of params when displaying and can even display 
           non params."""
    print a.main_params
    
test_Backbone_main_params()

def test_get_map():
    class Test(Backbone):
        a=Enum(1,2,3)
        b=List(default=[1,2,3])
        @property
        def a_mapping(self):
            return {1:"a", 2:"b", 3:"c"}
    
    t=Test()
    print t.a, t.get_map("a"), t.get_map("a", 3)
    
test_get_map()    