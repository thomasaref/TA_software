# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 20:34:36 2016

@author: thomasaref
"""

import matplotlib.pyplot as plt

from atom.api import Atom, Float
class T(Atom):
    a=Float(2)
    b=Float(3)

t=T()
print t.members()

for name in t.members():
    print name, getattr(t, name)

for name in t.members():
    setattr(t, name, 5.0)

for name in t.members():
    print name, getattr(t, name)

#if 0:
#figure=plt.figure()
#axe=figure.add_subplot(111)
#line=axe.plot([1,2,3], [4,5,6])[0]
#print dir(line)
#print line.get_xydata()
#line.set_xdata([4,5,6])
#axe.set_xlim((1,10))
#plt.draw()
#plt.show()
#print line