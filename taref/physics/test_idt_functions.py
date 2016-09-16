# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:55:30 2016

@author: thomasaref
"""

from scipy.constants import pi
from scipy.signal import hilbert
from numpy import linspace, sin, cos, imag
import matplotlib.pyplot as plt

frq=linspace(0.01e9, 10e9, 10000)
f0=5e9
Np=9

X=Np*pi*(frq-f0)/f0

c1=(sin(X)/X)**2.0

#(sqrt(2.0)*cos(pi*f/(4*f0))*1.0/Np*sin(gX)/sin(gX/Np))**2

c2=(1.0/Np*sin(X)/sin(X/Np))**2

l1=(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
l2=(1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))

h1=imag(hilbert(c1))
h2=imag(hilbert(c2))

plt.plot(frq/f0, c1)
plt.plot(frq/f0, c2)

plt.figure()
plt.plot(frq/f0, l1)
plt.plot(frq/f0, l2)

plt.figure()
plt.plot(frq/f0, l1)
plt.plot(frq/f0, h1)

plt.figure()
plt.plot(frq/f0, l2)
plt.plot(frq/f0, h2)


plt.show()
