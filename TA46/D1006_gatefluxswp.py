# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:26:51 2015

@author: thomasaref
"""

from numpy import sin, squeeze, shape, linspace, log10, mean, amax, amin, absolute, reshape, transpose, real, imag, angle, cos, sqrt, array, exp, delete
from TA210715A46_Fund import dB, flux_rescale, flux_parabola, lorentzian
from h5py import File
from matplotlib.pyplot import pcolormesh, xlabel, title, ylabel, colorbar, plot, show, ylim, xlim
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1006/TA46_gate_flux_swp_4p2t4p5GHz.hdf5"

from numpy import float64
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
    pwr=data[:, 0, 0]
    yoko= data[0, 1, :]
    yoko=yoko.astype(float64)
    freq=linspace(fstart, fstart+fstep*(sm-1), sm)

def gatecolormesh_noindex(pwi):
    pcolormesh(dB(Magcom[:, pwi, :]))

def gatecolormesh(pwi):
    pcolormesh(yoko, freq, dB(Magcom[:, 0, :]))
    xlabel("Flux (V)")
    ylabel("Frequency (Hz)")
    title("Reflection fluxmap at -117 dBm")
    colorbar()

Magabs=Magcom-mean(Magcom[:, :, 149:152 ], axis=2, keepdims=True)

def gate_bgsub_colormesh(pwi):
    pcolormesh(yoko, freq, absolute(Magabs[:, pwi, :]))

    ylim(amin(freq), amax(freq))
    xlabel("Flux (V)")
    ylabel("Frequency (Hz)")
    title("Gate fluxmap at {} dBm".format(-87-18-20))
    colorbar()

def gate_bgsub_colormesh_wparabola(pwi):
    gate_bgsub_colormesh(pwi) 
    plot(yoko, flux_parabola(flux_rescale(yoko)), "w", linewidth=3, alpha=0.5, )

print freq[103]

def cs_gate_bgsub(fqi, pwi):
    plot(yoko, absolute(Magabs[fqi, pwi, :])/amax(absolute(Magabs[fqi, pwi, :])))
    g=10.0e-6
    RR=lorentzian(flux_parabola(flux_rescale(yoko)), freq[fqi], [0.0], g)
    #RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*10.0e6))
    #plot(yoko, absolute(RR)/amax(absolute(RR)), label="50 MHz {}".format(g))
    xlabel("Flux (V)")
    ylabel("Gate response normalized")
    title("Gate cross section")

if __name__=="__main__":
    gatecolormesh_noindex(5)
    show()
    gatecolormesh(5)
    show()
    gate_bgsub_colormesh(5)
    show()
    gate_bgsub_colormesh_wparabola(5)
    show()
    cs_gate_bgsub(103, 4)
    show()
        