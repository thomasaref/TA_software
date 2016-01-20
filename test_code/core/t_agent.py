# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:45:12 2015

@author: thomasaref
"""

from taref.core.agent import SubAgent, Spy, Agent
from atom.api import Int, Float, ContainerList, Dict, Atom
from taref.core.log import log_info, log_debug
from taref.core.shower import shower

log_info(1)
class Test(SubAgent):
    a=Float()
    b=Int()
t=Test()
t2=Test()

print type(t2).agent_dict
def run_test():
    print t.agent_dict
    t.a=5
    print "ran run_test"

def run_test2():
    t2.b=3
    print "ran run_test2"

t.add_func(run_test)
#t.chief.add_func(run_test2)
#t.full_run()
#print t.agent_dict
#t.chief.add_func(t.chief.chief_run_test)
#print t.name
#print t2.name
#print t.base_name
#print t.chief
#print t.abort
#print t.desc
#shower(t, t2)
print type(t.activated)
print type(t.run_all)

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
