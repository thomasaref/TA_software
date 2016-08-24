# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:09:24 2016

@author: thomasaref
"""

from pystiff.api import Object, Int, Coerced, Typed, List, Tuple, Array, CArray, Set, Dict, ODict

class Test_Array(Object):
    #a=List()
    #b=Tuple()
    #c=Array()
    #d=CArray()
    #e=Set()
    #f=Dict()
    g=ODict()

a=Test_Array()
a.g[2]=1
print a.g
print a.a, a.b, a.c, a.d, a.e, a.f, a.g
print type(a.a), type(a.b), type(a.c), type(a.d), type(a.e), type(a.f), type(a.g)
a.d=[1,2]
print a.d
a.d=[2,3]
print a.d
a.g[2]=5
a.g[3]=6
print a.g
a.c=[1,2]

class Test(Object):
    c=Int(20)
    cc=Int()
    d=Coerced(int, (22,))

    def __init__(self):
        self.b=Int()

    f=Typed(int, (21,))
    g=Typed(float)

    #def _default_d(self):
    #    return 4

if __name__=="__main2__":
    a=Test()
    a.c=2
    print a.c, a.cc, a.d, a.b, a.f, a.g
    a.g=5.2
    a.g=None



#    a.a=Int(3)
#    print a.d
#    a.d=2
#    print a.f
#    a.f=3
#    print a.get_member("f").typer
#    print a.get_member("g").typer
#    print a.members("class").keys()

    #print a.a
    #print a.c, a.d
    #a.c=3
    #a.a=1
    #print a.members()
    #print a.cls_members()
    #print a.ins_members()
    #print a.get_member("a").name

    #print a.a, a.members()
    #print getattr(a, "d", "b")
    #a.a=5
    #print a.a, a.c, a.__dict__, a.members()
    #print a.cls_members(), a.get_cls_member("c")
