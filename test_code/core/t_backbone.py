# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 20:56:45 2015

@author: thomasaref
"""

from taref.core.backbone import (get_member, members, get_metadata, set_tag, set_all_tags, get_tag, get_all_tags, get_map, get_inv, get_type,
        get_reserved_names, get_all_params, get_all_main_params, get_main_params, set_log, lowhigh_check, get_attr, Backbone)

from taref.core.log import log_info

from atom.api import Atom, Int, Float, Enum

def test_get_member():
    class Test(Atom):
        a=Int()
        b=Float()
    t=Test()
    log_info("""get_member(obj, name):
    Returns the member of obj specified by name
    In this example, member a who is an Int. 
    This allows easy access to member functions and is included in the Atom api""")
    print get_member(t, "a")

test_get_member()


def test_members():
    class Test(Atom):
        a=Int()
        b=Float()
    t=Test()
    log_info("""members(obj):
    Returns the member dictionary of obj.
    In this example: a an Int and b a Float
    This allows easy access to all members and is included in the Atom api""")
    print members(t)

test_members()


def test_get_metadata():
    class Test(Atom):
        a=Int().tag(c=4)
        b=Float()
    t=Test()
    log_info("""get_metadata(obj, name):
    Returns the metadata dictionary of member of obj specified by name.
    In this example, member a who is tagged with c=4 and member b who has no metadata. 
    This allows easy access to metadata and autogenerates an empty dictionary if metadata is None.""")
    print get_metadata(t, "a")
    print get_metadata(t, "b")

test_get_metadata()

   
def test_set_tag():
    class Test(Atom):
        a=Int().tag(c=4)
        b=Float()
    t=Test()
    log_info("""set_tag(obj, name, key=value):
    Shortcut to use Atom's tag functionality to set metadata.
    In this example, member a who is already tagged with c=4 becomes tagged with t="p" 
    This allows easy access to Atom's tag functionality.""")
    set_tag(t, "a", t="p")
    print get_metadata(t, "a")
    print get_metadata(t, "b")

test_set_tag()

def test_set_all_tags():
    class Test(Atom):
        a=Int().tag(c=4)
        b=Float()
    t=Test()
    log_info("""set_all_tags(obj, key=value):
    Shortcut to use Atom's tag functionality to set metadata on members not marked private, i.e. all_params.
    In this example, member a and member b becomes tagged with t='p' 
    This is an easy way to set the same tag on all params""")
    set_all_tags(t, t="p")
    print get_metadata(t, "a")
    print get_metadata(t, "b")

test_set_all_tags()


def test_get_tag():
    class Test(Atom):
        a=Int().tag(c=4)
        b=Float()
    t=Test()
    log_info("""get_tag(obj, name, key):
    Shortcut to use Atom's retrive particular metadata which returns a none_value if it does not exist.
    In this example, member a is tagged with c=4 and b is not so it returns the default of 'five'
    This is an easy way to get a tag on a particular member and provide a default if it isn't there.""" )
    print get_tag(t, "a", "c", "five")
    print get_tag(t, "b", "c", "five")

test_get_tag()

def test_get_all_tags():
    class Test(Atom):
        a=Int().tag(c=4)
        b=Float().tag(c=5)
        c=Int().tag(c=5)
        d=Float()
    t=Test()
    log_info("""get_all_tags(obj, key, key_value=None, none_value=None, search_list=None):
    Shortcut retrieve members with particular metadata. There are several variants based on inputs.
    With only obj and key specified, returns all member names who have that key
    In this example, a, c and b""")
    print get_all_tags(t, "c")
    log_info("""with key_value specified, returns all member names that have that key set to key_value
    In this example, a""")
    print get_all_tags(t, "c", 4)
    log_info("""with key_value and none_value specified equal, returns all member names that
    have that key set to key_value or do not have the tag
    In this example, a and d""")
    print get_all_tags(t, "c", 4, 4)
    log_info("""specifying search list limits the members searched
    In this example, c is excluded from the search list above""")
    print get_all_tags(t, "c", 5, 5, ["a", "b", "d"])
    log_info("""Finally, if key_value is none, returns those members not matching none_value
    In this example, b and c since a is tagged as 4 and d is not tagged""")
    print get_all_tags(t, "c", None, 4,)

    
test_get_all_tags()

def test_get_map_inv():
    class Test(Atom):
        a=Enum("a", "b", "c")
        @property
        def a_mapping(self):
           return {"a" : 1, "b":2, "c":3} 
    t=Test()
    log_info("""get_map(obj, name, value):
    gets the map of an Enum defined in the property name_mapping. value can be used to get the map for another value besides the Enum's current one. 
    In this example, member a is the Enum and the property a_mapping produces the mapping""")
    print "t.a={0} : map({1})={2}".format(t.a, t.a, get_map(t, "a"))
    t.a="b"
    print "t.a={0} : map({1})={2}".format(t.a, t.a, get_map(t, "a"))
    print "t.a={0} : map({1})={2}".format(t.a, "c", get_map(t, "a", "c"))
    
    log_info("get_inv reverses the map")
    print "inv({0})={1}".format(1, get_inv(t, "a", 1))
    print "inv({0})={1}".format(2, get_inv(t, "a", 2))
    print "inv({0})={1}".format(3, get_inv(t, "a", 3))

    log_info("the Enum can also be mapped to variables")
    class Test(Atom):
        a=Enum("b", "c")
        b=Float()
        c=Int(2)
        @property
        def a_mapping(self):
           return {"b":self.b, "c":self.c} 
    t=Test()
    print "t.b={0} : map({1})={2}".format(t.b, t.a, get_map(t, "a"))
    print "t.c={0} : map({1})={2}".format(t.c, "c", get_map(t, "a", "c"))
    t.a="c"
    t.c=5
    print "t.c={0} : map({1})={2}".format(t.c, t.a, get_map(t, "a"))

test_get_map_inv()

def test_get_reserved_names():   
    class Test(Atom):
        a=Int().tag(c=4, private=True)
        b=Float()
        c=Int().tag(sub=True)
        
        @property
        def main_params(self):
            return ["c"]

    t=Test()
    log_info("""get_reserved_names(obj):
    returns all members who are tagged with private=True
    In this example, member a""")
    print get_reserved_names(t)
    log_info("""get_all_params(obj):
    returns all members who are not tagged with private=True
    In this example, member b and c""")
    print get_all_params(t)
    log_info("""get_all_main_params(obj):
    returns all params who are not tagged with sub=True
    In this example, member b""")
    print get_all_main_params(t)
    log_info("""get_main_params(obj):
    returns all_main_params unless obj.main_params is defined
    In this example, member c""")
    print get_main_params(t)

def test_get_type():   
    class Test(Atom):
        a=Int().tag(c=4, private=True)
        b=Int().tag(typer=str)
    t=Test()
    log_info("""get_type(obj, name):
    returns member object type, i.e. Int instead of int
    In this example, Int""")
    print get_type(t, "a")
    log_info("""can be overwritten with the typer tag
    In this example, str""")
    print get_type(t, "b")

test_get_type()

def test_get_attr():
    class Test(Atom):
        a=Int(3)
    t=Test()
    log_info("""get_attr(obj, name, none_value=None)
    returns an attr like getattr but provides a default if the attr does not exist
    in this example, 3 and 0""")
    print get_attr(t, "a", 0)
    print get_attr(t, "b", 0)

test_get_attr()

def test_lowhigh_check():
    class Test(Atom):
        a=Int(3)
        b=Int()
    t=Test()
    log_info("""get_attr(obj, name, none_value=None)
    returns an attr like getattr but provides a default if the attr does not exist
    in this example, 3 and 0""")
    print lowhigh_check(t, "a", 3)

def test_set_log():
    class Test(Atom):
        a=Int(3)
    t=Test()
    log_info("""get_attr(obj, name, none_value=None)
    returns an attr like getattr but provides a default if the attr does not exist
    in this example, 3 and 0""")
    print set_log(t, "a", 3)

def test_Backbone():
    class Test(Backbone):
        a=Int()
    t=Test()    
    log_info("Backbone internalizes many of these functions")
    print t.a
test_Backbone()  


if 0:
    test_get_member()
    test_members()
    test_get_metadata()
    test_set_tag()
    test_set_all_tags()
  
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
