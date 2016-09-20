# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:55:30 2016

@author: thomasaref
"""

from scipy.constants import pi, epsilon_0 as eps0
from scipy.signal import hilbert
from numpy import linspace, sin, cos, imag, sqrt, absolute, matrix, exp, eye, array, squeeze, float64, ones, log
import matplotlib.pyplot as plt
from taref.physics.surface_charge import alpha
from numpy.linalg import inv

f0=5.000000001e9

frq=linspace(0.001e9, 2*f0, 10000).astype(float64)
Np=29
W=25.0e-6
ft="double"
vf=3488.0
Dvv=0.024
epsinf=46.0*eps0
X=Np*pi*(frq-f0)/f0

alp_0=alpha(f0, f0, ft_mult=2)
print alp_0
alp_arr=alpha(frq, f0, ft_mult=2)

def _get_Y0(f, Dvv, epsinf, W):
    return pi*f*W*epsinf/Dvv

Y0_arr=_get_Y0(f=frq, W=W, epsinf=epsinf, Dvv=Dvv)
Ga0=alp_0*Dvv*sqrt(Y0_arr)
Ga=alp_arr*Dvv*sqrt(Y0_arr)

def _get_rs(f, h=30.0e-9, vf=3488.0):
    lbda= vf/f
    rs=(-1.7/100-0.24*h/lbda)*1.0j
    #if absolute(rs)>=1.0:
    #    return 0.9999j
    return rs

def _get_RAM_P_one_f(f, p, N_IDT, L_IDT, f0, alpha, rs, Y0, dloss1, dloss2,
                     W, Np,  ft,
                     vf, Dvv, epsinf):
    #k=2*pi*f/vf#-1.0j*(f/f0*dloss1+dloss2*(f/f0)**2) 0.19 f/1e9 + 0.88 (f/1e9)**2 dB/us*1e6/3488 *log(10.0)/20.0
    k=2*pi*f/vf-1.0j*(0.19*f/1e9 + 0.88*(f/1e9)**2)*1e6/3488*log(10.0)/20.0
    ts = sqrt(1.0-absolute(rs)**2)
    A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
                       [-rs,             exp(1.0j*k*p)]])#.astype(complex128)
    AN=A**int(N_IDT)
    AN11, AN12, AN21, AN22= AN[0,0], AN[0,1], AN[1,0], AN[1,1]
    P11=-AN21/AN22
    P21=AN11-AN12*AN21/AN22
    P12=1.0/AN22
    P22=AN12/AN22
    D = -1.0j*alpha*Dvv*sqrt(Y0) #/(2.0*Np)
    #D = -1.0j*sqrt(self.Ga0)/(2.0*Np)#*alpha*Dvv*sqrt(Y0)

    B = matrix([(1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0), (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)])
    #B0 = (1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0)
    #B1 = (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)

    I = eye(2)
    if ft=="single":
        P32_base=(inv(I-A**2)*(I-A**(2*int(Np))))*matrix([[0],
                                                        [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-p)/2.0)]]) #geometric series
    else:
        P32_base=((I+A)*inv(I-A**4)*(I-A**(4*int(Np))))*matrix([[0],
                                                              [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-2.0*p)/2.0)]])
    P32=D*(B*P32_base)
        #P32=D*(B0*P32_base[0,0]+B1*P32_base[1,0])
        #P32=D*B*((I+A)*inv(I-A**4)*(I-A**(4*int(Np))))*matrix([[0],
        #                                                      [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-2.0*p)/2.0)]]))[0] #geometric series
    P31=P32
    P13=P23=-P31/2.0
    return (P11, P12, P13,
            P21, P22, P23,
            P31, P32)

def _get_RAM_P(frq, f0=5.000000001e9, alpha=1.247, rs=0.0j, Y0=None, dloss1=0.0, dloss2=0.0,
               W=25.0e-6, Np=9, ft="double",
               vf=3488.0, Dvv=0.024, epsinf=46.0*eps0):
    if Y0 is None:
        Y0=pi*f0*W*epsinf/Dvv

    Ct_mult={ "single" : 1.0, "double" : sqrt(2)}[ft]
    Ct=Ct_mult*W*epsinf*Np

    ft_mult={"double" : 2.0, "single" : 1.0}[ft]
    lbda0=vf/f0
    p=lbda0/(2*ft_mult)
    N_IDT=2*ft_mult*Np
    L_IDT=Np*lbda0

    if isinstance(alpha, float):
        alpha=ones(len(frq))*alpha
    if isinstance(rs, complex):
        rs=ones(len(frq))*rs
    if isinstance(Y0, float):
        Y0=ones(len(frq))*Y0
    print "start P"
    P=[_get_RAM_P_one_f(f=f, Dvv=Dvv, epsinf=epsinf, W=W, vf=vf, rs=rs[i], Y0=Y0[i], p=p,
                        N_IDT=N_IDT, alpha=alpha[i], ft=ft, Np=Np, f0=f0, dloss1=dloss1, dloss2=dloss2, L_IDT=L_IDT) for i, f in enumerate(frq)]
    print "P_done"

    (P11, P12, P13,
     P21, P22, P23,
     P31, P32)=[squeeze(P_ele) for P_ele in zip(*P)]
    print "P_done 2"
    Ga=2.0*absolute(P13)**2
    Ba=-imag(hilbert(Ga))
    P33=Ga+1.0j*Ba+2.0j*pi*f*Ct
    return (P11, P12, P13,
            P21, P22, P23,
            P31, P32, P33), Ga, Ba, Ct


c1=frq/f0*(sin(X)/X)**2.0


c2=frq/f0*(1.0/Np*sin(X)/sin(X/Np))**2

c3=frq/f0*(sqrt(2.0)*cos(pi*frq/(4*f0))*1.0/Np*sin(X)/sin(X/Np))**2

c4=frq/f0*(alp_arr/alp_0*sqrt(2.0)*cos(pi*frq/(4*f0))*1.0/Np*sin(X)/sin(X/Np))**2

(P11, P12, P13,
 P21, P22, P23,
 P31, P32, P33), Ga, Ba, Ct=_get_RAM_P(frq=frq, alpha=alp_arr, ft=ft, Y0=Y0_arr, rs=_get_rs(frq), Np=Np)

Y0=pi*f0*W*epsinf/Dvv
c5=(absolute(P13)/(alp_0*Dvv*sqrt(Y0)*Np*sqrt(2)))**2

absP13=absolute(P13)
#c5=(absP13/max(absP13[4000:6000]))**2

l1=-(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
l2=(1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))

h1=imag(hilbert(c1))
h2=imag(hilbert(c2))
h3=imag(hilbert(c3))
h4=imag(hilbert(c4))
h5=imag(hilbert(c5))

plt.figure()
plt.plot(frq/f0, l1, linewidth=2.0)
plt.plot(frq/f0, h1)
plt.xlim(0.0, 2.0)


plt.figure()
plt.plot(frq/f0, l2, linewidth=2.0)
plt.plot(frq/f0, h2)
plt.xlim(0.0, 2.0)

plt.figure()
plt.plot(frq/f0, alp_arr)

plt.figure()
plt.plot(frq/f0, c1, label="sinc sq")
#plt.plot(frq/f0, c2, label="giant atom")
#plt.plot(frq/f0, c3, label="df giant atom")
#plt.plot(frq/f0, c4, label="full expr")
plt.plot(frq/f0, c5, label="RAM")
#plt.xlim(0.0, 2.0)
plt.legend()

plt.figure()
plt.plot(frq/f0, l1, label="sinc sq")
#plt.plot(frq/f0, l2, label="giant atom")
#plt.plot(frq/f0, h3, label="df giant atom")
#plt.plot(frq/f0, h4, label="full expr")
plt.plot(frq/f0, h5, label="RAM")
#plt.xlim(0.0, 2.0)
plt.legend()



plt.show()
