# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:46:09 2016

@author: thomasaref
"""

from numpy import pi, linspace, sin, amax, argmin, argmax, cos, absolute, sqrt, float64
from scipy.constants import h, e, epsilon_0 as eps0
#from taref.plotter.fig_format import Plotter

Np=9
f0=5.45e9
w0=2*pi*f0
vf=3488.0
freq=linspace(1e9, 10e9, 1000)

Ejmax=50.0e9
epsinf=46*eps0/3.72#*sqrt(2)

W=25.0e-6

Dvv=0.024
Ga0=3.11*w0*epsinf*W*Dvv*Np**2

C=sqrt(2.0)*Np*W*epsinf
Ec=e**2/(2*C)
print Ec/h

Gamma0=Ga0/(2*C)/(2.0*pi)
print Gamma0

def flux_to_Ej(voltage,  offset=0.0, flux_factor=1.0, Ejmax=Ejmax):
    flux_over_flux0=(voltage-offset)*flux_factor
    Ej=Ejmax*absolute(cos(pi*flux_over_flux0))
    return Ej

def calc_Lamb_shift(fq):
    wq=2.0*pi*fq
    X=Np*pi*(wq-w0)/w0
    Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
    return -Ba/(2.0*C)/(2.0*pi)

def calc_Coupling(fq):
    wq=2.0*pi*fq#print wq
    X=Np*pi*(wq-w0)/w0
    Ga=Ga0*(sin(X)/X)**2.0
    return Ga/(2.0*C)/(2.0*pi)

def energy_levels(EjdivEc):
    Ej=EjdivEc*Ec
    E0p =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0#-Ba/(2.0*C)*0.5 #(n +1/2)
    E1p =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)# -Ba/(2.0*C)*1.5
    E2p =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)#-Ba/(2.0*C)*2.5
    E3p =  sqrt(8.0*Ej*Ec)*3.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)#-Ba/(2.0*C)*3.5
    return E0p, E1p, E2p, E3p

EjdivEc=linspace(30, 300, 3000).astype(float64)
E0,E1,E2,E3=energy_levels(EjdivEc)
b=Plotter()
b.line_plot("E0", EjdivEc, E0/h, label="E0", linestyle="dashed", linewidth=1)
b.line_plot("E1", EjdivEc, E1/h, label="E1", linestyle="dashed", linewidth=1)
b.line_plot("E2", EjdivEc, E2/h, label="E2", linestyle="dashed", linewidth=1)
b.line_plot("E3", EjdivEc, E3/h, label="E3", linestyle="dashed", linewidth=1)

D1=calc_Lamb_shift((E1-E0)/h)
D2=calc_Lamb_shift((E2-E1)/h)
D3=calc_Lamb_shift((E3-E2)/h)

E0s=E0/h
E1s=E1/h+D1
E2s=E2/h+D2
E3s=E3/h+D3

b.line_plot("E0", EjdivEc, E0s, label="E0", linewidth=1, color="red")
b.line_plot("E1", EjdivEc, E1s, label="E1", linewidth=1, color="green")
b.line_plot("E2", EjdivEc, E2s, label="E2", linewidth=1, color="purple")
b.line_plot("E3", EjdivEc, E3s, label="E3", linewidth=1, color="black")

d=Plotter(fig_height=5.0, fig_width=7.0)

d.line_plot("E1",  (E1-E0)/h, E1s-E0s, label="E1", color="red", linewidth=0.5)
d.line_plot("E2",  (E1-E0)/h, E2s-E1s, label="E2", color="blue", linewidth=0.5)
d.line_plot("E4",  (E1-E0)/h, (E2s-E0s)/2.0, label="E2", color="purple", linewidth=0.5)
#d.line_plot("E3",  (E2s-E0s)/2, E3s-E2s, label="E3", color="purple", linewidth=0.5)
d.line_plot("anharm",  (E1-E0)/h, (E2s-E1s)-(E1s-E0s), label="E0", linewidth=0.5, color="green")
d.line_plot("anharm2",  (E1-E0)/h, (E2-E1)/h-(E1-E0)/h, label="E0", linewidth=0.5, color="black")
d.line_plot("zero", [min((E1-E0)/h), max((E1-E0)/h)], [0.0, 0.0], linewidth=0.5)

d.show()

d=Plotter(fig_height=5.0, fig_width=7.0)

d.line_plot("E1", (E1-E0)/h/f0, (E1s-E0s-(E1-E0)/h)/(2.0*Gamma0), label="E1", color="red", linewidth=0.5)
d.line_plot("E2", (E1-E0)/h/f0, (E2s-E1s-(E2-E1)/h)/(2.0*Gamma0), label="E2", color="blue", linewidth=0.5)
d.line_plot("anharm", (E1-E0)/h/f0, ((E2s-E1s)-(E1s-E0s)-((E2-E1)/h-(E1-E0)/h))/(2.0*Gamma0), label="E0", linewidth=0.5, color="green")

d.line_plot("D1", (E1-E0)/h/f0, D1/(2.0*Gamma0), label="$\Delta_{1,0}$", color="blue",  linewidth=0.5)
d.line_plot("D2", (E1-E0)/h/f0, (D2-D1)/(2.0*Gamma0), label="$\Delta_{2,1}$", color="red", linewidth=0.5)
d.line_plot("anh", (E1-E0)/h/f0, (D2-2*D1)/(2.0*Gamma0), label="$\Delta_{2,1}-\Delta_{1,0}$", color="black", linewidth=0.5)

#d.line_plot("E1", (E1-E0)/h/f0, (E1s-E0s-(E1-E0)/h)/(2.0*Gamma0), label="E1", color="red", linewidth=0.5)
#d.line_plot("E2", (E1-E0)/h/f0, (E2s-E1s-(E2-E1)/h)/(2.0*Gamma0), label="E2", color="blue", linewidth=0.5)
#d.line_plot("anharm", (E1-E0)/h/f0, ((E2s-E1s)-(E1s-E0s)-((E2-E1)/h-(E1-E0)/h))/(2.0*Gamma0), label="E0", linewidth=0.5, color="green")


d.set_xlim(0.7, 1.3)
d.set_ylim(-1, 0.7)
d.mpl_axes.ylabel="$\Delta/\Gamma_{10}^{MAX}$"
d.mpl_axes.xlabel="$\omega_{10}/\omega_{IDT}$"
d.axes.legend(loc='lower left')
#d.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Anharm.pdf")
d.show()
#d.line_plot("E3", EjdivEc, E3, label="E3")
#E0,E1,E2,E3=energy_levels(EjdivEc, Dvv=0.0)

