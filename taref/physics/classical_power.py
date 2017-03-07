# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:36:18 2017

@author: thomasaref
"""

from numpy import sqrt, pi, sin, linspace, array, absolute
#import matplotlib.pyplot as plt
from taref.plotter.api import colormesh, line

Np=9
f0=5.3e9
f=4.55e9
frq_arr=linspace(1.0e9, 10.0e9, 1000)

def GaBa(f):
    X=Np*pi*(f-f0)/f0

    Ga0=0.002

    Ga=Ga0*(sin(X)/X)**2
    Ba=Ga0*(sin(2*X)-2*X)/(2*X**2)
    return Ga, Ba

Ga, Ba=GaBa(frq_arr)

pwr=-100.0
Ic=112e-9

fq_arr=linspace(1.0e9, 10.0e9, 1001)
wq_arr=2*pi*fq_arr

#L=8.99e-9
Ct=136e-15
L_arr=1/(Ct*wq_arr**2)

#print sqrt(1/(L*Ct))/(2*pi)
w=2*pi*frq_arr

def r(Li, pwr):
    Psaw=0.001*10**(pwr/10.0)
    Isq=4*Ga*Psaw#+0.0j
    divL=1/Li*sqrt(1.0-Isq/Ic**2)
    return Ga/(Ga+1j*Ba+1j*w*Ct+divL/(1j*w))
r_arr=array([r(Li, pwr) for Li in L_arr])
colormesh(fq_arr, frq_arr, absolute(r_arr).transpose())


frq_arr=linspace(4.0e9, 5.0e9, 1000)
Ga, Ba=GaBa(frq_arr)
w=2*pi*frq_arr

pwr_arr=linspace(-120.0, -60.0, 1001)
wq=2*pi*4.5e9
L=1/(Ct*wq**2)
r_arr=array([r(L, pw) for pw in pwr_arr])
colormesh(absolute(r_arr))
line(pwr_arr, absolute(r_arr)[:, 273]).show()
