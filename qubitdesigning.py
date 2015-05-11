# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 18:20:16 2015

@author: thomasaref
"""






from numpy import tanh, sqrt
from scipy.constants import k, e, pi, h, hbar, epsilon_0 as eps0


zerogp = 200e-6 #200 uV, gap of aluminum at zero temperature
Tc=1.3
Delta=1.76*k*Tc
#print Delta*1e6
#T=0.3
#print pi*Delta/(2*e)*tanh(Delta/(2*k*T))
Ic=100e-9
Rn=pi*Delta/(2.0*e)/Ic
print Rn
EjoverEc=65

f0=4.8e9

Ej= sqrt(EjoverEc*(h*f0)**2/8.0) 
Ec=Ej/EjoverEc
Ctr = e**2/(2.0*Ec)
Ltr = (hbar/(2.0*e ))**2/Ej
#Ej=hbar Ic/(2.0*e)
Ic=Ej/hbar*(2.0*e)# Ic/(2.0*e)

N=7
W=25.0e-6
epsinf=46*eps0
#                Dvv=2.4e-2,
#                v=3488.0),
Ctr=N*W*epsinf*sqrt(2)
Ec = e**2/(2.0*Ctr)
Ej=Ec*EjoverEc

f0=sqrt((8.0/EjoverEc)*Ej**2)/h#= EjoverEc*(h*f0)**2/8.0 
print Ej, Ec, Ctr, Ltr, Ic
Rn=pi*Delta/(2.0*e)/Ic
print Rn, Ej/Ec, f0/1.0e9