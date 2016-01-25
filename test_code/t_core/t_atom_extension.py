# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 20:56:45 2015

@author: thomasaref
"""
from taref.core.log import log_info
from taref.core.atom_extension import (set_tag, set_all_tags, get_tag, get_all_tags, get_map, get_inv, get_type,
        get_reserved_names, get_all_params, get_all_main_params, get_main_params, set_log, lowhigh_check, private_property, tag_Callable, tag_Property)

from atom.api import Atom, Int, Float, Enum, Unicode, Bool, List, Dict
from taref.core.universal import Array
from numpy import array




print
log_info("test code:")
print """class Test(Atom):
    a=Int().tag(tg=4)
    b=Float()
t=Test()"""
class Test(Atom):
    a=Int().tag(tg=4)
    b=Float()
t=Test()
print
print 'set_tag(t, "a", z="p")'
set_tag(t, "a", z="p")
print 'print t.get_member("a").metadata'
print t.get_member("a").metadata
print 'print t.get_member("b").metadata'
print t.get_member("b").metadata
print
print 'set_all_tags(t, z=True)'
set_all_tags(t, z=True)
print 'print t.get_member("a").metadata'
print t.get_member("a").metadata
print 'print t.get_member("b").metadata'
print t.get_member("b").metadata
print
print 'get_tag(t, "a", "tg", "five")'
print get_tag(t, "a", "tg", "five")
print 'get_tag(t, "b", "tg", "five")'
print get_tag(t, "b", "tg", "five")
print 'get_tag(t, "a", "tg")'
print get_tag(t, "a", "tg")
print 'get_tag(t, "b", "tg")'
print get_tag(t, "b", "tg")
print
log_info("test code:")
class Test(Atom):
    a=Int().tag(tg=4)
    b=Float()
    c=Unicode("blah").tag(tg=4)
    d=Bool().tag(tg=5)
t=Test()
print """class Test(Atom):
    a=Int().tag(tg=4)
    b=Float()
    c=Unicode("blah").tag(tg=4)
    d=Bool().tag(tg=5)
t=Test()"""
print
print "With only obj and key specified, returns all member names who have that key"
print 'get_all_tags(obj=t, key="tg")'
print get_all_tags(obj=t, key="tg")
print
print "with key_value specified, returns all member names that have that key set to key_value"
print 'get_all_tags(obj=t, key="tg", key_value=4)'
print get_all_tags(t, "tg", 4)
print
print "with key_value and none_value specified equal, returns all member names that have that key set to key_value or do not have the tag"
print 'get_all_tags(obj=t, key="tg", key_value=4, none_value=4)'
print get_all_tags(t, "tg", 4, 4)
print
print "specifying search list limits the members searched"
print 'get_all_tags(obj=t, key="tg", key_value=4, none_value=4, search_list=["a", "b", "d"])'
print get_all_tags(t, "tg", 4, 4, ["a", "b", "d"])
print
print "Finally, if key_value is none, returns those members not matching none_value"
print 'get_all_tags(obj=t, key="tg", key_value=None, none_value=4)'
print get_all_tags(t, "tg", None, 4)
print
log_info("test code:")
print """class Test(Atom):
    en=Enum("a", "b", "c")

    #private_property is a cached Property tagged with private=True
    @private_property
    def en_mapping(self):
        return {"a" : 1, "b":2, "c":3}
t=Test()"""

class Test(Atom):
    en=Enum("a", "b", "c")

    @private_property
    def en_mapping(self):
        return {"a" : 1, "b":2, "c":3}
t=Test()
print
print "get_map returns the mapping of an Enum"
print 'print t.en, get_map(t, "en")'
print t.en, get_map(t, "en")
print
print 't.en="b"'
print 'print t.en, get_map(t, "en")'
t.en="b"
print t.en, get_map(t, "en")
print
print "if value is specified returns what the Enum would map to at that value"
print 't.en, get_map(t, "en", "c")'
print t.en, get_map(t, "en", "c")
print
print "get_inv inverts the Enum mapping and returns the appropriate value"
print 't.en, get_inv(t, "en", 1)'
print t.en, get_inv(t, "en", 1)
print
print 't.en, get_inv(t, "en", 2)'
print t.en, get_inv(t, "en", 2)
print
print 't.en, get_inv(t, "en", 3)'
print t.en, get_inv(t, "en", 3)
print
log_info("test code:")
print "Enum can also be mapped to object variables"
print """class Test(Atom):
    en=Enum("b", "c")
    b=Float()
    c=Int(2)
    @property
    def en_mapping(self):
       return {"b":self.b, "c":self.c}
t=Test()"""

class Test(Atom):
    en=Enum("b", "c")
    b=Float()
    c=Int(2)

    @private_property
    def en_mapping(self):
       return {"b":self.b, "c":self.c}
t=Test()
print
print 'print t.en, get_map(t, "en")'
print t.en, get_map(t, "en")
print
print 't.b=5.0'
print 'print t.en, get_map(t, "en")'
print 'print t.en, get_map(t, "en", reset=True)'
t.b=5.0
print t.en, get_map(t, "en")
print t.en, get_map(t, "en", reset=True)
print
print 'print t.en, get_map(t, "en", "c")'
print t.en, get_map(t, "en", "c")
print
print 't.c=8'
print 't.en, get_map(t, "en", c, reset=True)'
t.c=8
print t.en, get_map(t, "en", "c", reset=True)
print
print 't.en="c"'
print 'print t.en, get_map(t, "en")'
t.en="c"
print t.en, get_map(t, "en")
print
log_info("test code:")
print"""class Test(Atom):
    a=Int().tag(c=4, private=True)
    b=Float()
    c=Int().tag(sub=True)

    @private_property
    def main_params(self):
        return ["c"]
t=Test()"""

class Test(Atom):
    a=Int().tag(c=4, private=True)
    b=Float()
    c=Int().tag(sub=True)

    @private_property
    def main_params(self):
        return ["c"]
t=Test()
print
print "get_reserved_names returns all names of members tagged as private=True"
print 'get_reserved_names(t)'
print get_reserved_names(t)
print
print "get_all_params returns all names of members not tagged as private=True"
print 'get_all_params(t)'
print get_all_params(t)
print
print "get_all_main_params returns all params in all_params that are not tagged as sub"
print 'get_all_main_params(t)'
print get_all_main_params(t)
print
print "get_main_params defaults to get_all main_params but can be overwritten in the class"
print 'get_main_params(t)'
print get_main_params(t)

print
log_info("test code:")
print """class Test(Atom):
    a=Int().tag(c=4)
    b=Int().tag(typer=str)
t=Test()"""

class Test(Atom):
    a=Int(3).tag(c=4)
    b=Int().tag(typer=str)
t=Test()
print
print "get_type returns the type of the member, equivalent to type(t.get_member('a'))"
print 'get_type(t, "a")'
print get_type(t, "a")
print
print "the type returned by get_type can be overwritten by the typer tag"
print 'get_type(t, "b")'
print get_type(t, "b")
print
log_info("test code:")
print """class Test(Atom):
        a=Int(3).tag(low=1, high=5)
        b=Int().tag(low=1)
        c=Int().tag(high=5)
        d=Int()
t=Test()
"""
class Test(Atom):
        a=Int(3).tag(low=1, high=5)
        b=Int().tag(low=1)
        c=Int().tag(high=5)
        d=Int()
t=Test()
print
print "lowhigh_check assertains if a value is within the tags 'low' and 'high'"
print 'lowhigh_check(t, "a", 3)'
print lowhigh_check(t, "a", 3)
print
print 'lowhigh_check(t, "a", 7)'
print lowhigh_check(t, "a", 7)
print
print 'lowhigh_check(t, "a", 0)'
print lowhigh_check(t, "a", 0)
print
print 'lowhigh_check(t, "b", 3)'
print lowhigh_check(t, "b", 3)
print
print 'lowhigh_check(t, "b", 7)'
print lowhigh_check(t, "b", 7)
print
print 'lowhigh_check(t, "b", 0)'
print lowhigh_check(t, "b", 0)
print
print 'lowhigh_check(t, "c", 3)'
print lowhigh_check(t, "c", 3)
print
print 'lowhigh_check(t, "c", 7)'
print lowhigh_check(t, "c", 7)
print
print 'lowhigh_check(t, "c", 0)'
print lowhigh_check(t, "c", 0)
print
print 'lowhigh_check(t, "d", 3)'
print lowhigh_check(t, "d", 3)
print
print 'lowhigh_check(t, "d", 7)'
print lowhigh_check(t, "d", 7)
print
print 'lowhigh_check(t, "d", 0)'
print lowhigh_check(t, "d", 0)
print
log_info("test code:")
print """class Test(Atom):
        a=Int(3).tag(low=1, high=5)
        b=Int().tag(low=1)
        c=Int().tag(high=5)
        d=Int()
t=Test()
"""

class Test(Atom):
    name=Unicode("test_name").tag(private=True)
    a=Int().tag(label="Big A")
    b=Float().tag(unit=" mm")
    c=Unicode()
    d=List()
    en=Enum(1, 2, 3)
    arr=Array()
    f=Dict()

    @private_property
    def en_mapping(self):
        return {1:"a", 2:"b", 3:"c"}
t=Test()
print
print 'set_log(t, "a", 3)'
set_log(t, "a", 3)
print
print 'set_log(t, "b", 3)'
set_log(t, "b", 3)
print
print 'set_log(t, "c", "3")'
set_log(t, "c", "3")
print
print 'set_log(t, "d", [3])'
set_log(t, "d", [3])
print
print 'set_log(t, "arr", array([3]))'
set_log(t, "arr", array([3]))
print
print 'set_log(t, "en", 3)'
set_log(t, "en", 3)
print
print 'set_log(t, "f", dict(a=3))'
set_log(t, "f", dict(a=3))

log_info("test code:")
class Test(Atom):
    @tag_Callable(label="Run me")
    def func(self):
        print "func ran"

t=Test()
print t.get_member("func").metadata
t.func(t)


log_info("test code:")
class Test(Atom):
    @tag_Property(cached=False, label="my prop")
    def prop(self):
        return "blah"

t=Test()
print t.get_member("prop").metadata
print t.prop

from atom.api import Callable
from taref.core.atom_extension import instancemethod
class Test(Atom):
    name="test"
    def im(self):
        return "blah"
    im_c=Callable().tag(log=True)
t=Test()

@instancemethod(t)
def im_c(self):
    return "blah"

print t.im_c, t.im, im_c
print t.im_c(), t.im(), im_c(t)

from taref.core.atom_extension import _setup_callables, tag_Callable
class Test(Atom):
    name="test"
    @tag_Callable(log=True)
    def im(self):
        return "blah"



    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        for param in get_all_params(self):
            typer=get_type(self, param)
            _setup_callables(self, param, typer)
t=Test()
t.im()

from taref.core.atom_extension import property_func, tagged_property, _setup_property_fs
class Test(Atom):
    name="test"
    _im=1
    @tagged_property()
    def im(self):
        return "blah"

    @im.setter
    def st_im(self, value):
        self._im=value

    @im.setter
    def st2_im(self, value):
        print value

    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        for param in get_all_params(self):
            typer=get_type(self, param)
            _setup_property_fs(self, param, typer)
t=Test()
print t.im
t.im=5
print t._im
#print t.im.pname, t.im.setter, t.im.run_params, t.im.fset_list

#def test_Backbone():
#    class Test(Backbone):
#        a=Int()
#    t=Test()
#    log_info("Backbone internalizes many of these functions")
#    print t.a
#test_Backbone()




#c=to()
#print get_member(c, "a")
#print members(c)
#print get_metadata(c, "a")
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
