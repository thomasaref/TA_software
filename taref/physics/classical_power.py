# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:36:18 2017

@author: thomasaref
"""

from numpy import sqrt, pi, sin, cos, linspace, array, absolute, angle, ones, shape, meshgrid, reshape
#import matplotlib.pyplot as plt
from taref.plotter.api import colormesh, line
from scipy.constants import h, e, hbar

Np=9
f0=5.3e9
f=4.5e9
frq_arr=linspace(1.0e9, 10.0e9, 100)

Ec = 0.22e9/2*h # Charging energy.
Ejmax = 2*22.2e9*h # Maximum Josephson energy.


pwr=-100.0
Ic=112e-9

phi_arr=linspace(-1.0, 1.0, 50)*pi

Ct=136e-15
Cc=30e-15
Cground=0.0

Ga0=0.002
#print sqrt(1/(L*Ct))/(2*pi)
Rn=2800.0*10

def Icer(Isq, Ic, L, w):
    if Isq<Ic**2:
        divL=1.0/L*sqrt(1.0-Isq/Ic**2)
        YL=-1.0j/w*divL
    else:
        YL=1.0/Rn*ones(shape(L))
    return YL

def r(vg):
    phi, f, pwr=vg

    w=2*pi*f

    Ej = Ejmax*absolute(cos(phi)) #Josephson energy as function of Phi.
    Ic=2*e*Ej/hbar
    #print Ic
    fq = sqrt(8.0*Ej*Ec)/h #\omega_m
    wq=2*pi*fq

    L=1.0/(Ct*wq**2)

    X=Np*pi*(f-f0)/f0

    Ga=Ga0*(sin(X)/X)**2
    Ba=Ga0*(sin(2*X)-2*X)/(2*X**2)

    Psaw=0.001*10**(pwr/10.0)
    Isq=4.0*Ga*Psaw#+0.0j

    if Isq<Ic**2:
        divL=1.0/L*(1.0-Isq/Ic**2)
        YL=-1.0j/w*divL
    else:
        YL=1.0/Rn*ones(shape(L))

    P33plusYL=Ga+1.0j*Ba+1.0j*w*Ct+YL#-1.0j/w*divL
    Zatom=-1.0j/(w*Cc)+1.0/P33plusYL
    #Zeff=1.0/(1.0j*w*Cground+1.0/Zatom)
    ZS=50.0 #1.0/YS
    S33=(Zatom-ZS)/(Zatom+ZS)
    S13=S23=S32=S31=(1.0+S33)/2.0
    #return S33# S33
    return Ga/P33plusYL
    C=Ct(1+Ba/wCt)
    Ga/(Ga+1j*wC+divL/(1j*w))
#r_arr=array([r(phi=phi_arr, f=f_el, pwr=pwr) for f_el in frq_arr])
#colormesh(phi_arr, frq_arr, absolute(r_arr))#.show()#.transpose())


f=4.5e9

phi_arr=linspace(-1, 0.99, 500/1)*pi

pwr_arr=linspace(-120.0, -80.0, 101)

value_grid=array(meshgrid(phi_arr, f, pwr_arr))
value_grid=zip(value_grid[0, :, :].flatten(), value_grid[1, :, :].flatten(), value_grid[2, :, :].flatten())
#from qutip import parallel_map
from time import time
if 0:
    r_arr=parallel_map(r, value_grid,  progress_bar=True)
    #r_arr=reshape(r_arr, (len(phi_arr), len(pwr_arr))).transpose()
else:
    tstart=time()
    print tstart
    r_arr=array([r(vg) for vg in value_grid])
    print time()-tstart
    print r_arr.shape
r_arr=reshape(r_arr, (len(phi_arr), len(pwr_arr))).transpose()

print r_arr.shape
colormesh(phi_arr, pwr_arr, angle(r_arr))
line(phi_arr, absolute(r_arr)[32, :])
line(pwr_arr, absolute(r_arr)[:, 22]).show()
