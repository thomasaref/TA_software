# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:43:57 2015

@author: thomasaref
"""

from h5py import File
from numpy import shape, reshape, float64, linspace, absolute, mean, amin, amax
from matplotlib.pyplot import pcolormesh, plot, ylim, xlabel, ylabel, title, colorbar, show
from TA210715A46_Fund import flux_parabola, flux_rescale, dir_path

file_name="TA46_refll_fluxpowswp_4p2GHz4pGHz.hdf5"

with File(dir_path+file_name, 'r') as f:
    #print f["Traces"].keys()
    Magvec=f["Traces"]["Rohde&Schwarz Network Analyzer - S12"]
    data=f["Data"]["Data"]
    fstart=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][0]
    fstep=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][1]
    sm=shape(Magvec)[0]
    sy=shape(data)
    s=(sm, sy[0], sy[2]) 
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
    Magcom=reshape(Magcom, s, order="F")

    yoko=data[:, 0, 0]
    pwr= data[0, 1, :]
    yoko=yoko.astype(float64)
    freq=linspace(fstart, fstart+fstep*(sm-1), sm)

powind=4
print shape(Magcom)
print yoko[200]

Magabs=absolute(Magcom[:, :, powind]-mean(Magcom[:,190:,powind], axis=1, keepdims=True))

#pcolormesh(Magabs, vmin=0.0, vmax=0.0045 )
#show()

def refl_fluxmap():
    pcolormesh(yoko, freq, Magabs, vmin=0.0, vmax=0.0045 )
    plot(yoko, flux_parabola(flux_rescale(yoko)), "w", alpha=0.5)
    ylim(amin(freq), amax(freq))
    xlabel("Flux (V)")
    ylabel("Frequency (Hz)")
    title("Gate response fluxmap, at {} dBm".format(-87*0-20*0+pwr[powind]))
    colorbar()
    return file_name

if 0:
    freqind=85
    print freq[freqind]
    plot(yoko, transpose(Magabs[freqind, :]/amax(Magabs[freqind,:])))
    reflec=absolute(lorentzian(flux_parabola(flux_rescale(yoko)), freq[freqind], array([2.0e-16]), 10.0e6))
    plot(yoko, reflec/amax(reflec))
    #plot(amax(Magabs[:, :], axis=1)-amin(Magabs, axis=1))
    #xlim(100, 130)
    show()


file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1006/TA46_gate_flux_swp_4p2t4p5GHz.hdf5"

with File(file_path, 'r') as f:
    #print f["Traces"].keys()
    Magvec=f["Traces"]["Rohde&Schwarz Network Analyzer - S12"]
    data=f["Data"]["Data"]
    fstart=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][0]
    fstep=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][1]
    sm=shape(Magvec)[0]
    sy=shape(data)
    s=(sm, sy[0], sy[2]) 
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
    Magcom=reshape(Magcom, s, order="F")

    pwr=data[:, 0, 0]
    yoko= data[0, 1, :]
    yoko=yoko.astype(float64)
    freq=linspace(fstart, fstart+fstep*(sm-1), sm)

powind=4

if 0:
    pcolormesh(yoko, freq, dB(Magcom[:, powind, :]))
    xlabel("Flux (V)")
    ylabel("Frequency (Hz)")
    title("Gate response fluxmap, at {} dBm".format(-87-20+pwr[powind]))
    colorbar()
    show()    
if __name__=="__main__":
    refl_fluxmap()
    show()