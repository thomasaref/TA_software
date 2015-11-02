# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 20:56:45 2015

@author: thomasaref
"""

from taref.core.backbone import (get_member, members, get_metadata, set_tag, set_all_tags, get_tag, get_all_tags, get_map, get_inv, get_type,
        get_reserved_names, get_all_params, get_all_main_params, get_main_params, set_log, lowhigh_check)


from atom.api import Atom, Int, Float, Enum

class Test(Atom):
    a=Int().tag(u="p", typer=float)
    b=Float().tag(u=3)
    c=Enum("a", "b", "c")

    @property
    def c_mapping(self):
        return dict(a=1, b=2, c=3)
        
class to(object):
    a=5
    b=4.3
    c="hey"
    d=True
    
b=Test()
print get_member(b, "a")
print members(b)
set_tag(b, "a", t=3)
print get_metadata(b, "a")
print get_metadata(b, "b")
set_all_tags(b, d=1)
print get_metadata(b, "a")
print get_metadata(b, "b")
print get_tag(b, "a", "u", "five")
print get_tag(b, "a", "a", "five")
print get_all_tags(b, "u")
print get_all_tags(b, "u", "p")

print get_map(b, "c")
print get_map(b, "c", "c")
print get_inv(b, "c", 2)
print get_type(b, "a")
print get_type(b, "b")

print get_reserved_names(b)
print get_all_params(b)
print get_all_main_params(b)
print get_main_params(b)

print 
print lowhigh_check(b, "a", 3)
print set_log(b, "a", 3)
c=to()
print get_member(c, "a")
print members(c)
print get_metadata(c, "a")
#set_tag(c, "a", t=3) #generates error for non Atom object


#        @log_func
#        def ff(self, a=2):
#            print self, a
#            print "a f says hello"
#
#
#    class tA(Atom):
#        a=Int(5)
#        b=Float(4.3)
#        c=Unicode("hey")
#        d=Bool(True)
#        f=Enum(1,2,3)
#        g=Enum("a", "b")
#
#        @Callable
#        @log_func
#        def ff(self, a=2):
#            print self, a
#            print "b f says hello"
#
#
#    a=to()
#    b=tA()
#    print get_member(a, "a"), get_member(b, "a")
#    print members(a), members(b)
#    set_tag(a,"a", bill=5, private=True)
#    set_tag(b,"a", bill="five", sub=True)
#    set_all_tags(a, bob=7)
#    set_all_tags(b, bob="seven")
#    print get_metadata(a, "a"), get_metadata(b, "a")
#    print get_tag(a, "a", "bill"), get_tag(b, "a", "bill")
#    print get_all_tags(a, "bill"), get_all_tags(a, "bill", "five"),  get_all_tags(b, "bill", "five")
#    print b.f, get_map(b, "f"), get_mapping(b, "f"), get_inv(b, "f", 2)
#    print b.g, get_map(b, "g"), get_mapping(b, "g"), get_inv(b, "f", 2)
#    print get_type(a, "a"), get_type(b, "a")
#    print get_reserved_names(a), get_reserved_names(b)
#    print get_all_params(a), get_all_params(b)
#    print get_all_main_params(a), get_main_params(b)
#    print get_main_params(a), get_main_params(b)
#    print get_attr(a, "a", "yes"), get_attr(b, "aa", "yes")
#
#    @log_func
#    def ff(self, a=2):
#        print self, a
#        print "f says hello"
#    a.gg=ff
#    a.ff(), b.ff(b), a.gg(a)
#    print get_run_params(ff), get_run_params(a.ff), get_run_params(a.gg)
#    print b.a, a.a
#    run_func(b, "ff", a=1), run_func(a, "ff", a=1), run_func(a, "gg")
#    print b.a, a.a
#
