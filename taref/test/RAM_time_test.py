# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 18:15:03 2017

@author: thomasaref
"""

from numpy import matrix, log10, exp, sqrt, pi, absolute, linspace, array, shape, imag
from scipy.signal import hilbert
#from matplotlib.pyplot import plot, show, figure, pcolormesh
from taref.plotter.api import line, colormesh
from time import time
def P_one_freq(Np, f, p, ts, vf=3488.0, rs=1j*0.2, Cs=4.07e-10, W=25.0e-6, K2=0.048, alpha=1.2):     
        w=2*pi*f
        Y0=w*W*Cs/K2
        lbda=vf/f
        k=2*pi/lbda
        
        jkp=1j*k*p
        
        A=matrix([[1.0/ts*exp(-jkp), rs/ts],
                  [-rs/ts, 1.0/ts*exp(jkp)]])
        #Np=int((N+3)/4.0)
        N=4*Np-3
        
        #print A
        AN=A**N
        #print AN
        (AN11, AN12,
         AN21, AN22)=(AN[0,0], AN[0,1], AN[1,0], AN[1,1])
        
        #print AN11, AN12,AN21, AN22
        
        P11=-AN21/AN22
        P21=AN11-AN12*AN21/AN22
        P12=1.0/AN22
        P22=AN12/AN22
        D = -1.0j*alpha*K2/2.0*sqrt(Y0)

        B=matrix([(1-rs/ts+1/ts)*exp(-jkp/2), (1+rs/ts+1/ts)*exp(jkp/2)])
        
        L=p*N
        
        
        strt=matrix([[0],[1.0/AN22*exp(-1j*k*(L-2*p)/2.0)]])
        
        #[(4*n-4, 4*n-3)for n in range(1, Np+1)]
        
        Asum=sum([A**(4*n-4)+A**(4*n-3) for n in range(1, Np+1)])
        
        P32=D*(B*(Asum*strt))[0,0]
        P23=-P32/2.0
        P13=P23
        P31=-2.0*P13
        Ga=absolute(P13)**2+absolute(P23)**2
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32, Ga)

frqs=linspace(2.0e9, 7.0e9, 300)
pl="ga"           
def Pmatrix(Np=5, frqs=frqs, f0=4.5e9, vf=3488.0, rs=-1j*0.03, Cs=4.07e-10, W=25.0e-6):
    ts=sqrt(1+rs**2)
    lbda0=vf/f0
    p=lbda0/4.0
    #N=4*Np-3
    #Np=int((N+3)/4.0)

    C=sqrt(2.0)*Np*W*Cs
    Pmat=array([P_one_freq(Np=Np, f=f, p=p, ts=ts, rs=rs) for f in frqs])#, dtype=complex)
    #print shape(Pmat)
    (P11, P12, P13,
     P21, P22, P23,
     P31, P32, Ga)=(Pmat[:,0], Pmat[:,1], Pmat[:,2],
                    Pmat[:,3], Pmat[:,4], Pmat[:,5],
                    Pmat[:,6], Pmat[:,7], absolute(Pmat[:,8]))
    Ba=-imag(hilbert(Ga))
    w=2*pi*frqs
    P33=Ga+1j*Ba+1j*w*C
    if 0:
        line(frqs, Ga, pl=pl)
        line(frqs, Ba, pl=pl)

    return (P11, P12, P13,
            P21, P22, P23,
            P31, P32, P33)
    
def PtoS( P11, P12, P13,
         P21, P22, P23,
         P31, P32, P33, YL=1/50.0):
     YLplusP33=YL+P33
     sqrtYL=sqrt(YL)
     S11=P11-P13*P31/YLplusP33
     S12=P12-P13*P32/YLplusP33
     S13=2.0*sqrtYL*P13/YLplusP33
     S21=P21-P23*P31/YLplusP33
     S22=P22-P23*P32/YLplusP33
     S23=-P31*sqrtYL*P23/YLplusP33
     S31=-P31*sqrtYL/YLplusP33
     S32=-P32*sqrtYL/YL+P33
     S33=(YL-P33)/YLplusP33
     return (S11, S12, S13,
             S21, S22, S23,
             S31, S32, S33) 
             
def trans(Np):
    tstart=time()
    
    (P11, P12, P13,
     P21, P22, P23,
     P31, P32, P33)=Pmatrix(Np)
    
    (S11, S12, S13,
     S21, S22, S23,
     S31, S32, S33)=PtoS( P11, P12, P13,
                          P21, P22, P23,
                          P31, P32, P33)        
    print time()-tstart
    return S13*S31
    
data=[trans(m) for m in range(1,27+1)]
#figure()
colormesh(10*log10(absolute(data)**2))
#plot(frqs, 10*log10(absolute(S13*S31)**2))
#figure()

colormesh(absolute(data)**2)#.show()

colormesh(absolute(data)).show()
#show()

