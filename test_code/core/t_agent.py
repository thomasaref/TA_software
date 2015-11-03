# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:45:12 2015

@author: thomasaref
"""

from taref.core.agent import SubAgent, Spy, Agent
from atom.api import Int, Float, ContainerList, Callable
from taref.core.log import log_info, log_debug

log_info(1)
class Test(SubAgent):
    a=Float()
    b=Int()

t=Test()
#print t.a


def test_SubAgent():
    log_info("""SubAgents auto log Callables, have auto naming and a chief and abort access, show option""")
    class Test(SubAgent):
        a=Int()
        b=Float()
        
        def afunc(self):
            print "ran afunc!"
        
        @Callable
        def bfunc(self):
            print "ran bfunc!"
            
    t=Test()
    t.a=1
    t.a=1
    t.b=1.0
    t.b=1
    t.afunc()
    t.bfunc(t)    #fix log func
    print t.abort
    print t.chief
    print t.all_main_params
    print t.main_params
    print t.base_name
    print t.name
    print t.desc
    t.show()

test_SubAgent()

log_info(1)
def test_Spy():
    log_info("""Spy's use observers to log so only changes trigger logging""")
    class Test(Spy):
        a=Int()
        b=Float()
        c=ContainerList()
    t=Test()
    t.a=1
    t.a=1
    t.b=1.0
    t.b=1
    t.c.append(2)
test_Spy()
log_debug(1)

def test_Agent():
    log_info("""Agents use setattr to log changes so repeated = statements will still log""")
    class Test(Agent):
        a=Int()
        b=Float()
        c=ContainerList()
    t=Test()
    t.a=1
    t.a=1
    t.b=1.0
    t.b=1
    t.c=[1]
    t.c.append(2)
test_Agent()
log_debug(1)
        