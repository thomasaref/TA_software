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

def normalize(x):
    return (x-amin(x))/(amax(x)-amin(x))

def normalize_1d(x):
    return (x-amin(x, axis=1, keepdims=True))/(amax(x, axis=1, keepdims=True)-amin(x, axis=1, keepdims=True))

fridge_attn=87.0
#Table values:
W=25.0e-6
Npq=9
aq=80.0e-9

v=3488.0 #Literature value for LiNb YZ
epsinf=46.0*eps0 #Literature value for LiNb YZ

Tc=1.315 #critical temperature of aluminum
Delta=200.0e-6*e
Rn=9.2e3#(8.93e3+9.35e3)/2.0

#Calculated values
Ic=pi*Delta/(2.0*e)/Rn #Ambegaokar Baratoff formula
Ejmax=hbar*Ic/(2.0*e)

Cq=sqrt(2.0)*W*Npq*epsinf #Morgan
Ec=e**2/(2.0*Cq)

def flux_rescale(yoko, offset=0.09):
    #return (yoko-0.07)*0.198
    return (yoko-offset)*0.195

def flux_parabola(flux_over_flux0):
    Ej = Ejmax*absolute(cos(pi*flux_over_flux0))
    E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
    E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
    return (E1-E0)/h

def detuning(f0, flux_over_flux0):
    return 2.0*pi*(f0 - flux_parabola(flux_over_flux0))
    
    
def lorentzsweep(f, f0, P_in, g):
    SS22=[]
    for fin in f0:
        SS22.append(lorentzian(f, fin, P_in, g))
    return squeeze(SS22)
        
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
    

#tex.append(r"\begin{tabular}{|p{5 cm}|p{3 cm}|}")
#tex.append(r"\hline")
#tex.append(r"Talking/Listening IDTs & {} \\")
#tex.append(r"\hline")
#tex.append(r"Finger type & double finger\\")
#tex.append(r"\hline")
#tex.append(r"Number of finger pairs, $N_p$ & 36\\")
#tex.append(r"\hline")
#tex.append(r"Overlap length, $W$ & 25 $\mu$m\\")
#tex.append(r"\hline")
#tex.append(r"finger width, $a$ & 96 nm\\")
#tex.append(r"\hline")
#tex.append(r"Metallization ratio & 50\%\\")
#tex.append(r"\hline")
#tex.append(r"\end{tabular}")
#
#tex.append(r"\subsection{Sample values}")
#tex.append(r"\begin{tabular}{|p{5 cm}|p{3 cm}|}")
#tex.append(r"\hline")
#tex.append(r"Talking/Listening IDTs & {} \\")
#tex.append(r"\hline")
#tex.append(r"Distance qubit to reflection IDT & 200 $\mu$m\\")
#tex.append(r"\hline")
#tex.append(r"Distance qubit to transmission IDT & 300 $\mu$m\\")
#tex.append(r"\hline")
#tex.append(r"Speed of SAW & 3488 m/s\\")
#tex.append(r"\hline")
#tex.append(r"Capacitance per finger pair, $\epsilon_\infty$ & $46\epsilon_0$\\")
#tex.append(r"\hline")
#tex.append(r"Metallization ratio & 50\%\\")
#tex.append(r"\hline")
#tex.append(r"\end{tabular}")
#tex.append(r"")

#tex.append(r"\subsection{Calculated qubit values}")
#tex.append(r"\begin{tabular}{|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|}")
#tex.append(r"\hline")
#tex.append(r"Calculated values qubit & Value & Expression & Comment\\")
#tex.append(r"\hline")
#tex.append(r"Center frequency & 5.45 GHz & $v/(8a_q)$ & speed over wavelength\\")
#tex.append(r"\hline")
#tex.append(r"Gap $\Delta(0)$ & 200e-6 eV & $1.764 k_B T_c$ & BCS\\")
#tex.append(r"\hline")
#tex.append(r"Normal resistance, $R_n$ & 9.14 kOhms & mean(DC junction resistances) & Tunable \\")
#tex.append(r"\hline")
#tex.append(r"Critical current, $I_c$ & 35 nA &  $\dfrac{\pi \Delta(0)}{2e}$ & Ambegaokar Baratoff formula \\")
#tex.append(r"\hline")
#tex.append(r"Ej\_max & 0.82 K, 17 GHz & $\dfrac{\hbar I_c}{2e R_n}$ & {} \\")
#tex.append(r"\hline")
#tex.append(r"Capacitance from fingers $C_q$ & 130 fF & $\sqrt{2} W N_{pq} \epsilon_\infty$ & Morgan chp 1 \\")
#tex.append(r"\hline")
#tex.append(r"\(E_c\) & {7.2 mK,} {150 MHz} & $\dfrac{e^2}{2 C}$ & Charging energy \\")
#tex.append(r"\hline")
#tex.append(r"Ejmax/Ec & 115 & Ejmax/Ec & transmon limit \\")
#tex.append(r"\hline")
#tex.append(r"Estimated max frequency of qubit & 4.37 GHz & {} & full transmon expression \\")
#tex.append(r"\hline")
#tex.append(r"\end{tabular}")
#
#tex.append(r"\subsection{Calculated IDT values}")
#tex.append(r"\begin{tabular}{|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|}")
#tex.append(r"\hline")
#tex.append(r"Calculated values IDT & Value & Expression & Comment\\")
#tex.append(r"\hline")
#tex.append(r"Center frequency & 4.54 GHz & $v/(8a)$ & speed over wavelength\\")
#tex.append(r"\hline")
#tex.append(r"Capacitance from fingers $C$ & 518 fF & $\sqrt{2} W N_{p} \epsilon_\infty$ & Morgan chp 1 \\")
#tex.append(r"\hline")
#tex.append(r"$Ga0$ & {7.2 mK,} {150 MHz} & $\dfrac{e^2}{2 C}$ & Charging energy \\")
#tex.append(r"\hline")
#tex.append(r"F width at half max & 115 & Ejmax/Ec & transmon limit \\")
#tex.append(r"\hline")
#tex.append(r"\end{tabular}")
