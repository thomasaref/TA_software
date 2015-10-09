# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:33:40 2015

@author: thomasaref
"""

from scipy.constants import e, k, h, hbar, epsilon_0 as eps0, pi
from numpy import (sqrt, float64, shape, reshape, linspace, log10, absolute, cos, mean, transpose, amax, amin,
                   array, squeeze)

dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/"

def dB(x):
    return 20*log10(absolute(x))

#Table values:
W=25.0e-6
Npq=9
aq=80.0e-9

v=3488.0 #Literature value for LiNb YZ
epsinf=46.0*eps0 #Literature value for LiNb YZ

Tc=1.315 #critical temperature of aluminum
Delta=200.0e-6*e
Rn=(8.93e3+9.35e3)/2.0

#Calculated values
Ic=pi*Delta/(2.0*e)/Rn #Ambegaokar Baratoff formula
Ejmax=hbar*Ic/(2.0*e)

Cq=sqrt(2.0)*W*Npq*epsinf #Morgan
Ec=e**2/(2.0*Cq)

def flux_rescale(yoko):
    return (yoko-0.07)*0.198

def flux_parabola(flux_over_flux0):
    Ej = Ejmax*absolute(cos(pi*flux_over_flux0))
    E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
    E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
    return (E1-E0)/h

def detuning(f0, flux_over_flux0):
    return 2.0*pi*(f0 - flux_parabola(flux_over_flux0))

def lorentzian(f, f0, P_in, g):
    g=2.0*pi*g/2.0
    N_in=P_in/(h*f0)
    d_omega=2.0*pi*(f0-f)
    S22=[]
    for N_idx, N in enumerate(N_in):
        S22.append((1.0+1j*d_omega/g)/(1.0 + d_omega**2/g**2 + 2.0*N/g))
    return squeeze(array(S22))

# Qubit reflection, for an incoming N_in phonons per second *at the qubit*
def  r_qubit(f0, G, g, d_omega, P_in):
    N_in=P_in/(h*f0)
    #G = Gamma_tot
    #g = gamma_10
    P22=[]
    for N_idx, N in enumerate(N_in):
        P22.append(-(G/(2.0*g))*(1.0+1j*d_omega/g)/(1.0 + d_omega**2/g**2 + 2.0*N/g))
    return squeeze(array(P22))

def print_fundamentals():
    """For double checking values"""
    print "Fundamental constants:"
    print "pi={}".format(pi)
    print "e={}".format(e)
    print "k={}".format(k)
    print "h={}".format(h)
    print "hbar={}".format(hbar)
    print "eps0={}".format(eps0)
    print 
    print "Material constants (Lithium Niobate YZ):"
    print "v={}".format(v)
    print "epsinf={}".format(epsinf)
    print 
    print "Sample constants:"
    print "W={} m".format(W)
    print "Npq={}".format(Npq)
    print "aq={}".format(aq)
    print "Rn={}".format(Rn)
    print "Tc={}".format(Tc)
    print 
    
    #print calculated values
    print "Calculated values:"
    print "check gap of aluminum, Delta={:.2e}".format(1.764*k*Tc/e)
    print "Critical current, Ic={}".format(Ic) 
    print "Ejmax={0} K= {1} Hz".format(Ejmax/k, Ejmax/h)
    print "Qubit capacitance = {} F".format(Cq)
    print "Ec = {0} K = {1} Hz".format(Ec/k, Ec/h)
    print "Ejmax/Ec={}".format(Ejmax/Ec)
    print "fq_max=sqrt(8*Ejmax*Ec)={} Hz".format(sqrt(8.0*Ejmax*Ec)/h)
    print "fq_max_full={} Hz".format(flux_parabola(0.0))
    print
    print "Qubit center frequency = {} Hz".format(v/(8*aq))
    
