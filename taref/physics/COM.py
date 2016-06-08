# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:40:39 2016

@author: thomasaref
"""

from numpy import conj,exp,sqrt,pi,zeros,cos,sin
from constants import v,Gamma,rho_fs

#Coupling of Modes (COM) calcuation as described in Morgan chapter 8. Eqn numbers refer to Morgan's eqn numbers
#h=30.0e-9 #film thickness
#rs=-0.03j  #-0.718j*Dvv-0.001j*h/lbda0
#ts=sqrt(1.0-abs(rs)**2.0)

ke=w/vf-1.0j*3.0e3 #you can include loss between electrodes by making adding imaginary component #ve=w/Re(ke)
#N=Np #number of finger pairs
rhoke=1.694*epsinf #this is given by eqn 5.59 which is an awful formula. I use numerical evaluation of eqn 5.59 given on page 13 middle paragraph
Np=9
C=Np*W*epsinf #L*Cl total capacitance of single finger IDT.
L=Np*2.0*p #length of single finger IDT

def com(lam0,k,r,x,W,L,C):
    """implementation of COM model. equation numbers refer to Morgan SAW book"""
    c12 = conj(-r/lam0*exp(-2j*k*lam0/2.0)) #c12=rs/p #eqn 8.41 assuming rs1=rs2=rs
    aT = rho_fs*sqrt(k*v*W*Gamma/2)
    a1 = conj(-1.0j*aT/lam0*exp(-1j*k*lam0/2-x)) #   a1=0.5*1.0j*rhoke*sqrt(2.0*w*W*Gs)/(2.0*p) #eqn 8.42 I had to insert a factor of 0.5 (similar to T matrix approach) which I don't quite understand.
                                               #This factor of 0.5 is probably due to the array factor of one pair of fingers

    kc=2*pi/lam0     #kc=kg=pi/p #eqn 8.23

    delta = k-kc #    d=ke-kg #eqn 8.23

    s=sqrt(delta**2.0-abs(c12)**2.0+0j) #eqn 8.35, 0j is so sqrt returns complex for negatives

    D = s*cos(s*L)+1.0j*delta*sin(s*L) #near eqn 8.40

    K1 = (conj(a1)*c12-1.0j*delta*a1)/s**2 #eqn 8.38

    K2 = (a1*conj(c12)+1.0j*delta*conj(a1))/s**2 #eqn 8.38

    P11 = -conj(c12)*sin(s*L)/D  #eqn 8.40a

    P12 = P21 = s*exp(-1.0j*kc*L)/D   #eqn 8.40b

    P22 = c12*sin(s*L)*exp(-2.0j*kc*L)/D #eqn 8.40c

    P31 = (2.0*conj(a1)*sin(s*L)-2.0*s*K2*(cos(s*L)-1.0))/D #eqn 8.40d

    P32 = exp(-1.0j*kc*L)*(-2.0*a1*sin(s*L)-2.0*s*K1*(cos(s*L)-1.0))/D #eqn 8.40e

    P13 = -P31/2.0 #eqn 8.40d

    P23 = -P32/2.0    #eqn 8.40e

    P33 = -K1*P31-K2*P32*exp(1.0j*kc*L)+2.0*(conj(a1)*K1-a1*K2)*L+1.0j*k*v*C #1.0j*w*Ct #eqn 8.40f

    Ya=-K1*P31-K2*P32*exp(1.0j*kc*L)+2.0*(conj(a1)*K1-a1*K2)*L #Ga+jBa (P33 without C term)

    return P11,P12,P13,P21,P22,P23,P33






