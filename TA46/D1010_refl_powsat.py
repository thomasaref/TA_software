# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:54:41 2015

@author: thomasaref
"""


from h5py import File
from numpy import float64, shape, reshape, linspace, mean, amin, amax, absolute, squeeze, log10, sqrt, angle, exp
from TA210715A46_Fund import dB, fridge_attn
from matplotlib.pyplot import pcolormesh, show, xlabel, ylabel, title, colorbar, ylim, xlim, plot

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1010/TA46_pxi_refl_powsat.hdf5"

with File(file_path, 'r') as f:
    print f.keys()
    print f["Data"]["Channel names"][:]
    #Magvec=f["Traces"]["PXI Dig - Trace"]#[:]
    data=f["Data"]["Data"]
    print data.dtype
    print shape(data[:])
    pwr=data[:,0,:]
    yoko=data[:,1,:]
    lvlcorr=data[:,2,:]
    PXIIQ=data[:,3,:]+1j*data[:,4,:]
    print PXIIQ.dtype #=PXIIQ.astype(float)
    print shape(PXIIQ)
    
#    tstart=f["Traces"]['PXI Dig - Trace_t0dt'][0][0]
#    tstep=f["Traces"]['PXI Dig - Trace_t0dt'][0][1]
#    print tstart, tstep
#    print shape(Magvec)
#    print shape(data)
#    sm=shape(Magvec)[0]
#    sy=shape(data)
#    s=(sm, sy[0], sy[2]) 
#    print s
#    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
#    Magcom=reshape(Magcom, s, order="F")
#    #Magcom=delete(Magcom, 73, axis=1)
#    yoko=data[:, 0, 0].astype(float64)
#    #pwr=delete(pwr, 73)
#    time=linspace(tstart, tstart+tstep*(sm-1), sm)
#    
    #freq=linspace(4.0e9, 5.0e9, 1001)
    #print Magcom.dtype, pwr.dtype, yoko.dtype, freq.dtype
    #print rept
    #print yoko
    #print time
#    print shape(Magcom)
#    Magcom=squeeze(Magcom)
#    print shape(Magcom)
#    print shape(yoko)
#    print yoko
    #print freq
    #Magcom=mean(Magcom, axis=1)

    
#absMag=absolute(Magcom[-200:]) 
#yoko=yoko[-200:]   
pwrlin=0.001*10**((pwr-87)/10.0)
voltlin=sqrt(50.0*pwrlin)
sigpwr=10*log10(absolute(PXIIQ)**2)-70
siglin=0.001*10**(sigpwr/10.0)
sigvolt=sqrt(50.0*siglin)
S11=sigvolt/voltlin
th=angle(PXIIQ)
S11c=S11*exp(1j*th) 
print shape(S11c)
plot(pwr[:,0], absolute(S11c[:,0]-S11c[:,1]))
#    plt.pcolormesh(dB(S11c)) 
#pcolormesh(yoko, time*1e6, absolute(Magcom))
show()