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
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0929/TA_A58_scb_time_trans.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0929/TA_A58_scb_time_refl_fluxtswp.hdf5"
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1006/TA46_pxi_pulse_refl_flux_swp.hdf5"

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
    yoko=data[:, 0, 0].astype(float64)
    #pwr=delete(pwr, 73)
    time=linspace(tstart, tstart+tstep*(sm-1), sm)
    
    #freq=linspace(4.0e9, 5.0e9, 1001)
    #print Magcom.dtype, pwr.dtype, yoko.dtype, freq.dtype
    #print rept
    #print yoko
    #print time
    print shape(Magcom)
    Magcom=squeeze(Magcom)
    print shape(Magcom)
    print shape(yoko)
    print yoko
    #print freq
    #Magcom=mean(Magcom, axis=1)
    
#absMag=absolute(Magcom[-200:]) 
#yoko=yoko[-200:]   

pcolormesh(yoko, time*1e6, absolute(Magcom))
show()



def dB(x):
    return 20*log10(absolute(x))

IQ=Magcom
pwrlin=0.001*10**((20.0-20.0)/10.0)
voltlin=sqrt(50.0*pwrlin)
sigpwr=10*log10(absolute(IQ)**2)
siglin=0.001*10**(sigpwr/10.0)
sigvolt=sqrt(50.0*siglin)
S11=sigvolt/voltlin
th=angle(IQ)
S11c=S11*exp(1j*th)  

#pcolormesh(dB(S11c))
#show()
#plot(dB(S11c[:, :]))
#show()
#plot(freq)
#show() ,

if 1:
    plot(time*1e6, dB(S11c[:, 148]), label="Max refl, yoko=3.15 V".format(yoko[315]))
    plot(time*1e6, dB(S11c[:, 200]), label="Min refl, yoko=2.21 V".format(yoko[221]))
    
    #==============================================================================
    # plot(time*1e6, dB(S11c[:, 2040]), label="64 ns from pulse start {}".format(freq[2040]))
    xlabel("Time (us)")
    ylabel("Reflection (dB)")
    title("Time domain reflection at 4.51 GHz")
    ylim(-90, -50)
    legend()
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

#Xf=X(freq)    
#plot( dB(S11c[32, 0:501]), label="8 ns after start of pulse {}".format(time[32]-time[30]))
#show()
#plot(yoko, dB(S11c[32, :]), label="8 ns after start of pulse{}".format(time[32]-time[30]))
#plot(yoko, dB(S11c[34, :]), label="16 ns after start of pulse{}".format(time[34]-time[30]))
plot(yoko, dB(S11c[35, :]), label="20 ns after start of pulse{}".format(time[35]-time[30]))
plot(yoko, dB(S11c[46, :]), label="64 ns after start of pulse{}".format(time[46]-time[30]))
#plot(yoko, dB(S11c[50, :]), label="64 ns after start of pulse {}".format(time[50]-time[30]))
#plot(yoko, dB(S11c[60, :]), label="64 ns after start of pulse {}".format(time[60]-time[30]))
#plot(yoko, dB(S11c[70, :]), label="64 ns after start of pulse{}".format(time[70]-time[30]))
#
plot(yoko, dB(S11c[83, :]), label="212 ns after start of pulse{}".format(time[83]-time[30]))
plot(yoko, dB(S11c[90, :]), label="240 ns after start of pulse {}".format(time[90]-time[30]))
plot(yoko, dB(S11c[100, :]), label="280 ns after start of pulse {}".format(time[100]-time[30]))
plot(yoko, dB(S11c[110, :]), label="320 ns after start of pulse{}".format(time[110]-time[30]))

plot(yoko, dB(S11c[153, :]), label="492 ns after start of pulse{}".format(time[153]-time[30]))
plot(yoko, dB(S11c[230, :]), label="800 ns after start of pulse{}".format(time[230]-time[30]))

plot(yoko, dB(S11c[294, :]), label="1056 ns after start of pulse{}".format(time[294]-time[30]))

#plot(yoko[0:501], dB(S11c[300, 0:501]), label="{}".format(time[33]-time[30]))
#plot(yoko[0:501], dB(S11c[338, 0:501]), label="{}".format(time[34]-time[30]))
#plot(freq, dB((1.0-R(freq))*(sin(Xf)/Xf)**2)-36.45)
#plot(freq, dB(Ga(X(freq))*2*sqrt(50.0)/(50.0+Y(freq)))/1.0+6)
title("Flux modulation at various times at 4.51 GHz")
xlabel("Flux (V)")
ylabel("Reflection (dB)")
#ylim(-52.2, -51.2)
legend()
#plot(freq, dB(1.0-R(freq))-36.45)

show()
plot(dB(S11c[294, :]), label="1056 ns after start of pulse{}".format(time[294]-time[30]))
show()
pcolormesh(yoko[0:501], time*1e6, dB(S11c[:,0:501]), 
           vmin=-52.2, vmax= -51.2,
           ) #amax(dB(S11c)))
title("Reflection vs flux and time (1 us pulse) at 4.51 GHz")
xlabel("Flux (V)")
ylabel("Time (us)")
ylim(0, 1.5)
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
