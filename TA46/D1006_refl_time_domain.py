# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:33:47 2015

@author: thomasaref
"""

from numpy import loadtxt, linspace, shape, reshape, float64, mean, absolute, amax, amin, cos, pi, squeeze, sqrt, angle, log10, exp, sin
from matplotlib.pyplot import plot, show, xlabel, ylabel, title, pcolormesh, legend, colorbar, ylim
from h5py import File
from TA210715A46_Fund import dB

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1006/TA46_pxi_pulse_refl_flux_swp.hdf5"

with File(file_path, 'r') as f:
    anr_pwr=f["Instrument config"]['Anritsu MG369X Signal generator - GPIB: 5, Anritsu Sig Gen at localhost'].attrs["Power"]
    print f["Instrument config"]['Anritsu MG369X Signal generator - GPIB: 5, Anritsu Sig Gen at localhost'].attrs["Frequency"]
    print f["Instrument config"]['PXI Aeroflex 303x Digitizer - GPIB: PXI4::15::INSTR, PXI Dig at localhost'].attrs['RF Frequency'] #.keys() #['Anritsu MG369X Signal generator - GPIB: 5, Anritsu Sig Gen at localhost'].attrs["Frequency"]

    print f.attrs["comment"]
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
    yoko=data[:, 0, 0].astype(float64)
    time=linspace(tstart, tstart+tstep*(sm-1), sm)
    print shape(Magcom)
    Magcom=squeeze(Magcom)
    print shape(Magcom)
    print shape(yoko)


def plotmaptime():
    pcolormesh(yoko, time*1e6, absolute(Magcom))
    title("Reflection vs flux \n and time (1 us pulse) at 4.46 GHz")
    xlabel("Flux (V)")
    ylabel("Time (us)")
    #ylim(0, 1.5)
    colorbar()





IQ=Magcom
pwrlin=0.001*10**((anr_pwr-20.0)/10.0)
voltlin=sqrt(50.0*pwrlin)
sigpwr=10*log10(absolute(IQ)**2)
siglin=0.001*10**(sigpwr/10.0)
sigvolt=sqrt(50.0*siglin)
S11=sigvolt/voltlin
th=angle(IQ)
S11c=S11*exp(1j*th)  

def plotmapdBtime():
    pcolormesh(yoko, time*1e6, dB(S11c), vmin=-65, vmax=-30)
    title("Reflection (dB) vs flux \n and time (1 us pulse) at 4.46 GHz")
    xlabel("Flux (V)")
    ylabel("Time (us)")
    #ylim(0, 1.5)
    colorbar()

def maxandmin_intime():
    plot(time*1e6, dB(S11c[:, 148]), label="Max refl, yoko=3.15 V".format(yoko[315]))
    plot(time*1e6, dB(S11c[:, 200]), label="Min refl, yoko=2.21 V".format(yoko[221]))
    xlabel("Time (us)")
    ylabel("Reflection (dB)")
    title("Time domain reflection at 4.46 GHz")
    ylim(-65, -30)
    legend()


def time_cuts():
    plot(yoko, dB(S11c[35, :]), label="20 ns after start of pulse".format(time[35]-time[30])) 
    plot(yoko, dB(S11c[46, :]), label="64 ns after start of pulse".format(time[46]-time[30]))
    plot(yoko, dB(S11c[83, :]), label="212 ns after start of pulse".format(time[83]-time[30]))
    plot(yoko, dB(S11c[90, :]), label="240 ns after start of pulse".format(time[90]-time[30]))
    plot(yoko, dB(S11c[100, :]), label="280 ns after start of pulse".format(time[100]-time[30]))
    plot(yoko, dB(S11c[110, :]), label="320 ns after start of pulse".format(time[110]-time[30]))

    plot(yoko, dB(S11c[153, :]), label="492 ns after start of pulse".format(time[153]-time[30]))
    plot(yoko, dB(S11c[230, :]), label="800 ns after start of pulse".format(time[230]-time[30]))

    plot(yoko, dB(S11c[294, :]), label="1056 ns after start of pulse".format(time[294]-time[30]))

    title("Flux modulation at various times at 4.46 GHz")
    xlabel("Flux (V)")
    ylabel("Reflection (dB)")
    legend()

if __name__=="__main__":
    maxandmin_intime()
    show()
    time_cuts()
    show()
    plotmapdBtime()
    show()
    plotmaptime()
    show()
    

    
