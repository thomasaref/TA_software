# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:14:50 2015

@author: thomasaref
"""

from scipy.constants import pi, e, epsilon_0 as eps0, h
from numpy import linspace, sin, sinc, cos, sqrt
from matplotlib.pyplot import plot, show, xlabel, ylabel, title, xlim, ylim, legend

Np=9

K2=0.046

v=3488.0
lbda0=96.0e-9
lbda0q=80.0e-9

print v/(lbda0*8)
print v/(lbda0q*8)

f0=4.54e9
fq0=5.45e9

#Table values:
W=25.0e-6
epsinf=46.0*eps0 #Literature value for LiNb YZ

C=sqrt(2.0)*W*Np*epsinf
print e**2/(2.0*C)/h/1.0e9
print f0/fq0
Gact=0.45*Np*K2*fq0/1.0e9
print Gact

def couple_theory():
    f=linspace(4.0e9, 6.0e9, 201)
    #phi=pi*(f-fq0)/fq0
    #plot(f, (1-cos(Np*phi))/(1-cos(phi))/Np**2, 'o')
    plot(f/1.0e9, Gact*(sin(Np/2.0*pi*(f-fq0)/fq0)/(Np/2.0*pi*(f-fq0)/fq0))**2, label="Qubit IDT Np/2")
    plot(f/1.0e9, Gact*(sin(Np*pi*(f-fq0)/fq0)/(Np*pi*(f-fq0)/fq0))**2, label="Qubit IDT Np")
    #plot(f, sinc(Np*(f-fq0)/fq0)**2, 'o')
    #plot(f, sinc(Np/2.0*(f-fq0)/fq0)**2, 'o')
    
    plot([f0/1.0e9, f0/1.0e9], [0, Gact], label="IDT")
    xlabel("Frequency (GHz)")
    ylabel("Coupling/$2\pi$ (GHz)")
    title("Coupling theory plot")
    legend(loc=2)
def couple_theory_zoom():
    couple_theory()
    xlim(4.4, 4.6)
    ylim(0, 0.2)
    
if __name__=="__main__":
    couple_theory()
    show()
    couple_theory_zoom()
    show()
    
    x=linspace(0.001, 2*pi, 101)
    plot(x, sin(x)/x)
    plot(x, sinc(x))
    show()