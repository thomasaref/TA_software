# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:13:47 2017

@author: thomasaref
"""

from numpy import sqrt, pi, sin, linspace, absolute
#from matplotlib.pyplot import plot, show, figure

from taref.plotter.api import line
from TA88_fundamental import qdt

qdt.gate_type="constant"
print qdt.f/1e9
qdt.f=qdt.f0+1.0
f0=qdt.f0/1e9
f=linspace(4.0, 6.0, 1001)
Np=qdt.Np
w0=2*pi*f0
gamma=2*pi*qdt.coupling/1e9
print gamma
print f0
print Np
X=Np*pi*(f-f0)/f0
pl="fig1"
line(absolute(-gamma/w0*sin(2*X)-2*X)/(2*X**2)-X/(Np*pi), pl=pl).show()
f=4.999999

f0=5.000001
f=linspace(4, 6, 1001)

g=30.0/(2*pi)
Np=9
print 3*f0/(Np*g)
X=pi*Np*(f-f0)/f0

Ga=g*(sin(X)/X)**2
Ba=g*(sin(2*X)-2*X)/(2*X**2)

f1=f0
f2=f0+sqrt(5.0)*f0/(pi*Np)*sqrt(1.0-3*f0/(Np*g))
f3=f0-sqrt(5.0)*f0/(pi*Np)*sqrt(1.0-3*f0/(Np*g))

w=2*pi*f
w0sq=(2*pi*f0)**2
r=Ga/(Ga+1j*Ba+1j*w/2.0+w0sq/(2j*w))

plot(f, absolute(r))
plot(f, absolute(-g*(sin(2*X)-2*X)/(2*X**2)-2*X*2*f0/(Np)))

plot([f1, f1], [0.0, 1.0])

plot([f2, f2], [0.0, 1.0])

plot([f3, f3], [0.0, 1.0])

figure()
plot(f, -Ba)
plot(f,f-f0)

figure()
plot(f, absolute(-g*(sin(2*X)-2*X)/(2*X**2)-2*X*2*f0/(Np)))

show()

#r=Ga/(Ga+1/2w)*(Ba/w+w^2-w0^2)
#
#X=np pi (w/w0-1)=X/Np pi+1
#Ba/w0C=Xw0(w/w0+1)
#Ba/C=Xw0^2(X/Nppi+2)
#
#
#g(sin(2X)-2X)/(2X^2)=Xw0^2(X/Nppi+2)
#g(2X/3)=Xw0^2(X/Nppi+2)
#g/w0^2(2X/3)Nppi=X^2+2NppiX
#
#=X^2+2NppiX-g/w0^2(2X/3)Nppi
