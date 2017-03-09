# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:36:18 2017

@author: thomasaref
"""

from numpy import sqrt, pi, sin, cos, linspace, array, absolute, ones, shape
#import matplotlib.pyplot as plt
from taref.plotter.api import colormesh, line
from scipy.constants import h

Np=9
f0=5.3e9
f=4.5e9
frq_arr=linspace(1.0e9, 10.0e9, 1000)

Ec = 0.22e9/2*h # Charging energy.
Ejmax = 2*22.2e9*h # Maximum Josephson energy.


pwr=-100.0
Ic=112e-9

phi_arr=linspace(-1.0, 1.0, 500)*pi

Ct=136e-15
Cc=30e-15
Cground=0.0

Ga0=0.002
#print sqrt(1/(L*Ct))/(2*pi)
Rn=2800.0

    
def r(phi, f, pwr):
    w=2*pi*f

    Ej = Ejmax*absolute(cos(phi)) #Josephson energy as function of Phi.
    fq = sqrt(8.0*Ej*Ec)/h #\omega_m
    wq=2*pi*fq

    L=1.0/(Ct*wq**2)

    X=Np*pi*(f-f0)/f0

    Ga=Ga0*(sin(X)/X)**2
    Ba=Ga0*(sin(2*X)-2*X)/(2*X**2)

    Psaw=0.001*10**(pwr/10.0)
    Isq=4.0*Ga*Psaw#+0.0j
 
    if Isq<Ic**2:
        divL=1.0/L*sqrt(1.0-Isq/Ic**2)
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

phi_arr=linspace(0.01, 0.99, 500)*pi

pwr_arr=linspace(-120.0, -58.0, 1001)

r_arr=array([r(phi=phi_arr, f=f, pwr=pwr_el) for pwr_el in pwr_arr])
print r_arr.shape
colormesh(phi_arr, pwr_arr, absolute(r_arr))
line(pwr_arr, absolute(r_arr)[:, 262]).show()
