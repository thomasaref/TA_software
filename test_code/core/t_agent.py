# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:45:12 2015

@author: thomasaref
"""

from taref.core.agent import SubAgent, Spy, Agent
from atom.api import Int, Float, ContainerList, Dict
from taref.core.log import log_info, log_debug

log_info(1)
class Test(SubAgent):
    a=Float()
    b=Int()
t=Test()
t2=Test()
print t.name
print t2.name
print t.base_name
print t.chief
print t.abort
print t.desc
t.show()


log_info("""Spy's use observers to log so only changes trigger logging""")
class Test(Spy):
    a=Int()
    b=Float().tag(high=4)
    c=ContainerList()
t=Test()
t.a=1
t.a=1
t.b=1.0
t.b=1
t.c.append(2)
t.b=5

log_info("""Agents use setattr to log changes so repeated = statements will still log""")
class Test(Agent):
    a=Int()
    b=Float()
    c=ContainerList()
    d=Dict()
t=Test()
t.a=1
t.a=1
t.b=1.0
t.b=1
t.c=[1]
t.c.append(2)
