# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 17:23:16 2016

@author: thomasaref
"""

from itertools import combinations
from time import time

class piece(object):
    def __init__(self, wh, name, rotated=False):
        self.x=0.0
        self.y=0.0
        self.w=wh.real
        self.h=wh.imag
        #self.xcoords=[0.5*a for a in range(1, size*2+1)]
        #self.ycoords=[0.5*a for a in range(1, size*2+1)]
        self.placed=False
        self.name=name
        #if rotated:
        #    self.name=str((self.h, self.w))+"r"
        #else:
        #    self.name=str((self.w, self.h))

    def __str__(self):
        return str((self.w, self.h))

    def rotate(self):
        return piece(self.h+1j*self.w, self.name+"r", True)
        h=self.h
        self.h=self.w
        self.w=h
        return self
        
    def le(self):
        return self.x-self.w/2.0

    def re(self):
        return self.x+self.w/2.0

    def te(self):
        return self.y-self.h/2.0

    def be(self):
        return self.y+self.h/2.0

    @property
    def area(self):
        return self.w*self.h
#def piece_sum(alist):
        
a1=piece(32+11j, "a1")
a2=piece(32+10j,"a2") 
a3=piece(10+7j, "a3")
a4=piece(21+14j, "a4")
a5=piece(21+18j, "a5")
a6=piece(21+18j, "a6")
a7=piece(17+14j, "a7")
a8=piece(14+4j, "a8")
a9=piece(21+14j, "a9")
a10=piece(28+7j, "a10")
a11=piece(28+14j, "a11")
a12=piece(28+6j, "a12")

size=56

alist=[a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12]
#alist=[piece(a) for a in alist]
blist=alist+[a.rotate() for a in alist]
print "yo"
print [str(bl) for bl in blist]
print [bl.name for bl in blist]
tstart=time()
combos = sum([map(list, combinations(blist, i)) for i in range(2,len(blist) + 1)], [])
print time()-tstart
print len(combos)

def valid_combo(cb):
    w_sum=sum([el.w for el in cb])
    #h_sum=sum([el.h for el in cb])
    if int(w_sum)==56:
        return True #"horiz"
    #elif int(h_sum)==56:
    #    return "vert"
    return False

tstart=time()
    
h_sols=[[el for el in cb] for cb in combos if valid_combo(cb)]
#v_sols=[[str(el) for el in cb] for cb in combos if valid_combo(cb)=="vert"]
print time()-tstart

print len(h_sols)#, len(v_sols)
print [[str(el) for el in h] for h in h_sols]
print [[el.name for el in h] for h in h_sols]

def nf(h, name="a12"):
    for el in h:
        if name in el.name:
            return True
    return False
print [[el.name for el in h] for h in h_sols if nf(h)]    
#print combos


def area_check(alist):
    return sum([a.area for a in alist])
    return sum([a.real*a.imag for a in alist])
print area_check(alist)
print 56*56
print alist[0].w, alist[0].h
alist[0].rotate()
print alist[0].w, alist[0].h

def soln_search(tlist):
    if len(tlist)>1:
        for i in range(len(tlist)):
            tl=tlist[:]
            el=tl.pop(i)
            soln_search(tl)
    else:
        el=tlist[0]
    
for r in range(2):
    a.rotate()
