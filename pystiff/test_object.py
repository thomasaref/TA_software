# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:09:24 2016

@author: thomasaref
"""

from pystiff.api import Object, Int, Coerced, Typed

class Test(Object):
    c=Int(20)
    d=Coerced(int, (2,))
    
    def __init__(self):
        self.b=Int()
        
    f=Typed(int, (21,))
    g=Typed(float)

    def _default_d(self):
        return 4

if __name__=="__main__":
    a=Test()
    a.a=Int(3)
    print a.d
    a.d=2
    print a.f
    a.f=3
    print a.get_member("f").typer
    print a.get_member("g").typer
    print a.members("class").keys()

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
