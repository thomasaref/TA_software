# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:03:08 2016

@author: thomasaref
"""

#from taref.test.test_frames import Test
from taref.core.log import msg, log_debug, f_top
from taref.core.agent import Operative
from atom.api import Float, Unicode
from taref.core.shower import shower

class Test2(Operative):
    a=Float()
    b=Unicode()

    def _observe_a(self, change):
        print msg(change)

    def _observe_b(self, change):
        log_debug(change)

    def another_f(self):
        print msg("that", n=5)
        log_debug("this")
        log_debug("this", n=100)
        fb=f_top()
        print fb.f_locals

    #def show(self):
    #    shower(self)
t=Test2()
t.another_f()

print msg("yoyoyoy")
t.show()