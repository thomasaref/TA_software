# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 23:15:33 2015

@author: thomasaref
"""

from atom.api import Atom, Float, Coerced, Enum, Typed, List
from enaml import imports
from enaml.qt.qt_application import QtApplication
from a_Base import get_type, get_main_params,  Base
from a_Boss import show
from threading import Thread
from time import sleep

from atom.api import Atom, Bool, Int, Callable, ContainerList

from enaml.application import deferred_call
from enaml.widgets.api import Window, Container, ProgressBar, PushButton, Field

#print BaseView#(instr, type(instr))

def myfunc(model, b=2):
    #model.busy=True
    for n in range(10):
        model.boss.progress=n*10
        if model.abort:
            break
        model.ov=n
        print model.ov, model.b
        sleep(0.2)


#class To(object):
#    d=4
#    b=4.3
#    c=u"blah"
#    f=True
#    g=[3,2]
#    h=(5,6)
#
#    def blah(self):
#        print "ran blah"
#
#    def __setattr__(self, name, value):
#        super(To, self).__setattr__(name, value)
#        print "set {name} to {value}".format(name=name, value=value)
#
#    #main_params=['d', 'a', 'b']
#

class S(Base):
     aa=Float() #Enum("a","b","c")
     bb=Int()
class T(Base):
    a=Typed(S, ())
    ov=Int()
    b=Float(2.3).tag(unit="bbb", label="blahhafd", low=0.0)
    g=ContainerList().tag(low=1)
    
    def _default_g(self):
        return range(100)
    c=Callable(myfunc)#    c=Coerced(int)#.tag()

    @Callable
    def cc(self, b=2):
        for n in range(10):
            self.boss.progress=n*10
            if self.abort:
                break
            self.ov=n
            print self.ov, self.b
            sleep(0.2)

    d=Enum('b', 'c', 'ov')

a=T()
print a.get_map("g", 0)#print a.get_member('g').item
a.show()
print a.g
b=T()
print [bb.name for bb in b.boss.bases]
#b.cc()
#b.boss.show_bases=True
#a.show()##print b.d
##a._show()
##print a.d