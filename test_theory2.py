# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:33:47 2015

@author: thomasaref
"""

from numpy import loadtxt, linspace, shape, reshape, float64, mean, absolute, amax, amin, cos, pi
from matplotlib.pyplot import plot, show, xlabel, ylabel, title
from h5py import File

if 0:
    a=loadtxt("/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Theory_280915/PerE0andE1.txt")
    b=loadtxt("/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Theory_280915/PerE1minusE0.txt")
    
    ng=linspace(-0.6, 1.6, (1.6+0.6)/0.01+1)
    plot(ng, b)
    show()

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0928/TA_A58_scb_refl_fluxcut2.hdf5"

with File(file_path, 'r') as f:
    print f["Traces"].keys()
    Magvec=f["Traces"]["Rohde&Schwarz Network Analyzer - S12"]#[:]
    data=f["Data"]["Data"]
    fstart=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][0]
    fstep=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][1]
    print fstep
    print shape(Magvec)
    print shape(data)
    sm=shape(Magvec)[0]
    sy=shape(data)
    s=(sm, sy[0], sy[2]) 
    print s
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
    Magcom=reshape(Magcom, s, order="F")
    #Magcom=delete(Magcom, 73, axis=1)
    yoko=data[:, 0, 0].astype(float64)
    #pwr=delete(pwr, 73)
    rept= data[0, 1, :].astype(float64)
    freq=linspace(fstart, fstart+fstep*(sm-1), sm)
    
    #print Magcom.dtype, pwr.dtype, yoko.dtype, freq.dtype
    print rept
    print yoko
    print freq
    print shape(Magcom)
    Magcom=mean(Magcom, axis=0)
    print shape(Magcom)
    Magcom=mean(Magcom, axis=1)
    
absMag=absolute(Magcom[-200:]) 
yoko=yoko[-200:]   


plot(yoko, (absMag-amin(absMag))/(amax(absMag)-amin(absMag)))#-(0.06*yoko+0.2))

plot(yoko, absolute(cos(pi*(yoko+1.35)*0.27)))#, refl/amax(refl))
title("normalized reflection vs flux (alternating)")
xlabel("flux (V)")
ylabel("R or f (normalized)")
show()

plot(absolute(cos(pi*(yoko+1.35)*0.27)), (absMag-amin(absMag))/(amax(absMag)-amin(absMag)))#-(0.06*yoko+0.2))
title("normalized reflection vs normalized f (alternating)")
xlabel("f normalized")
ylabel("R normalized")
show()
plot(yoko, (absMag-amin(absMag))/(amax(absMag)-amin(absMag)))#-(0.06*yoko+0.2))

plot(yoko, absolute(cos(pi*(yoko+0.4)*0.54)))#, refl/amax(refl))
title("normalized reflection vs flux (fmax on high)")
xlabel("flux (V)")
ylabel("R or f (normalized)")

show()

plot(absolute(cos(pi*(yoko+0.4)*0.54)), (absMag-amin(absMag))/(amax(absMag)-amin(absMag)))#-(0.06*yoko+0.2))
title("normalized reflection vs normalized f (fmax on high)")
xlabel("f normalized")
ylabel("R normalized")


show()

plot(yoko, (absMag-amin(absMag))/(amax(absMag)-amin(absMag)))#-(0.06*yoko+0.2))

plot(yoko, absolute(cos(pi*(yoko-0.55)*0.54)))#, refl/amax(refl))
title("normalized reflection vs flux (fmax on low)")
xlabel("flux (V)")
ylabel("R or f (normalized)")

show()

plot(absolute(cos(pi*(yoko-0.55)*0.54)), (absMag-amin(absMag))/(amax(absMag)-amin(absMag)))#-(0.06*yoko+0.2))
title("normalized reflection vs normalized f (fmax on low)")
xlabel("f normalized")
ylabel("R normalized")
show()
