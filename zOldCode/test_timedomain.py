# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:33:47 2015

@author: thomasaref
"""

from numpy import loadtxt, linspace, shape, reshape, float64, mean, absolute, amax, amin, cos, pi, squeeze, sqrt, angle, log10, exp, sin
from matplotlib.pyplot import plot, show, xlabel, ylabel, title, pcolormesh, legend, colorbar, ylim
from h5py import File

if 0:
    a=loadtxt("/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Theory_280915/PerE0andE1.txt")
    b=loadtxt("/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Theory_280915/PerE1minusE0.txt")
    
    ng=linspace(-0.6, 1.6, (1.6+0.6)/0.01+1)
    plot(ng, b)
    show()

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0928/TA_A58_scb_refl_fluxcut2.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0928/TA_A58_scb_refl_fluxcut3.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0928/TA_A58_scb_time_test5.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0928/TA_A58_scb_time_test5.hdf5"
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0929/TA_A58_scb_time_trans.hdf5"

with File(file_path, 'r') as f:
    #print f["Traces"].keys()
    Magvec=f["Traces"]["PXI Dig - Trace"]#[:]
    data=f["Data"]["Data"]
    tstart=f["Traces"]['PXI Dig - Trace_t0dt'][0][0]
    tstep=f["Traces"]['PXI Dig - Trace_t0dt'][0][1]
    print tstart, tstep
    print shape(Magvec)
    print shape(data)
    sm=shape(Magvec)[0]
    sy=shape(data)
    s=(sm, sy[0], sy[2]) 
    print s
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
    Magcom=reshape(Magcom, s, order="F")
    #Magcom=delete(Magcom, 73, axis=1)
    freq=data[:, 0, 0].astype(float64)
    #pwr=delete(pwr, 73)
    #time= data[0, 1, :].astype(float64)
    time=linspace(tstart, tstart+tstep*(sm-1), sm)
    
    #freq=linspace(4.0e9, 5.0e9, 1001)
    #print Magcom.dtype, pwr.dtype, yoko.dtype, freq.dtype
    #print rept
    #print yoko
    #print time
    print shape(Magcom)
    Magcom=squeeze(Magcom)
    print shape(Magcom)
    print shape(freq)
    #Magcom=mean(Magcom, axis=1)
    
#absMag=absolute(Magcom[-200:]) 
#yoko=yoko[-200:]   

pcolormesh(absolute(Magcom))
show()



def dB(x):
    return 20*log10(absolute(x))

IQ=Magcom
pwrlin=0.001*10**((20.0)/10.0)
voltlin=sqrt(50.0*pwrlin)
sigpwr=10*log10(absolute(IQ)**2)
siglin=0.001*10**(sigpwr/10.0)
sigvolt=sqrt(50.0*siglin)
S11=sigvolt/voltlin
th=angle(IQ)
S11c=S11*exp(1j*th)  

#pcolormesh(dB(S11c))
#show()
#plot(freq)
#show()
#plot(time*1e6, dB(S11c[:, 1872]), label="64 ns from pulse start {}".format(freq[1872]))
plot(time*1e6, dB(S11c[:, 2040]), label="64 ns from pulse start {}".format(freq[2040]))
xlabel("Time (us)")
ylabel("Transmission (dB)")
title("Time domain signal at 4.51 GHz")
ylim(-100, -40)
#legend()
show()

from scipy.constants import epsilon_0 as eps0
epsinf=46.0*eps0
Dvv=2.4/100.0
Np=55
W=7.0e-6
f0=4.48e9
print 3488.0/(0.096*8)

#0.8*1j 2 Dvv * Np * sin(X)/X

Gs=Dvv/epsinf
#2Ps=(1/4)*2*pi*f*W/Gs*|phi|**2 = Y0 phi|**2
#  Y0=sqrt(2pifW/2Gs)
#Pv=Vt**2 Ga/2 = Y0 |phi| **2

#Pv=2Ps
#1.247 * \epsinf Dvv/epsinf * sqrt(2pif*W/2Gs)
C=sqrt(2)*W*Np*46*eps0
print C

Ga0=3.11*2*pi*f0*epsinf*W*Dvv*Np**2
#Ga0=(sqrt(2)*1.247)**2  Y0 Dvv**2 Np**2
print 1/Ga0

def X(f):
    return pi*Np*(f-f0)/f0

def Ga(X):
     return Ga0*(sin(X)/X)**2

def Ba(X):
    return Ga0*(sin(2.0*X)-2.0*X)/(2*X**2)
    
def Y(f):
    return Ga(X(f))+1j*Ba(X(f))+1j*2.0*pi*f*C

def R(f):
    return (1.0/Y(f)-50.0)/(1.0/Y(f)+50.0)

Xf=X(freq)    
plot(freq, dB(S11c[294, :]), label="56 ns after pulse end".format(time[294]-time[280]))
#plot(freq, dB((1.0-R(freq))*(sin(Xf)/Xf)**2)-36.45)
plot(freq, dB(Ga(X(freq))*2*sqrt(50.0)/(50.0+Y(freq)))/1.0+6)
title("56 ns after pulse end theory compare")
xlabel("Frequency (Hz)")
ylabel("Transmission (dB)")
ylim(-100, -40)
#legend()
#plot(freq, dB(1.0-R(freq))-36.45)

show()
pcolormesh(freq, time*1e6, dB(S11c), 
           vmin=-80, vmax=amax(dB(S11c)))
title("Transmission vs freq and time (1 us pulse)")
xlabel("Frequency (Hz)")
ylabel("Time (us)")
ylim(0,3.0)
colorbar()
show()
    
plot(freq, dB(S11c[46, :]), label="64 ns from pulse start".format(time[46]-time[30]))
plot(freq, dB(S11c[67, :]), label="148 ns from pulse start".format(time[67]-time[30]))
plot(freq, dB(S11c[250, :]), label="880 ns from pulse start".format(time[250]-time[30]))
plot(freq, dB(S11c[294, :]), label="56 ns after pulse end".format(time[294]-time[30]))

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0926/TA_A58_scb_char_trans_4t5avg2.hdf5"
with File(file_path, 'r') as f:
    print f["Traces"].keys()
    Magvec=f["Traces"]["Agilent VNA - S12"]#[:]
    #print f["Data"].keys()
    #print f["Data"]["Channel names"][:]
    data=f["Data"]["Data"]
    fstart=f["Traces"]['Agilent VNA - S12_t0dt'][0][0]
    fstep=f["Traces"]['Agilent VNA - S12_t0dt'][0][1]
    sm=shape(Magvec)[0]
    freq=linspace(fstart, fstart+fstep*(sm-1), sm)
    print shape(data)
    pwr=data[:, 0, 0]
    #yoko= data[0, 1, :]
    print shape(pwr)
    #PXIavgpwr=data[:,2,:]
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]

def dB(x):
    return 20*log10(absolute(x))

plot(freq, dB(Magcom[:,2]), label="VNA")   
legend() 
xlabel("Frequency (Hz)")
ylabel("Transmission (dB)")
title("Comparison at various times to VNA")
ylim(-80, -30)
show()



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
