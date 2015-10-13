# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:54:41 2015

@author: thomasaref
"""


from h5py import File
from numpy import float64, shape, reshape, linspace, mean, amin, amax, absolute, squeeze, log10, sqrt, angle, exp, array, transpose
from TA210715A46_Fund import dB, fridge_attn, lorentzian, flux_rescale, flux_parabola, normalize, lorentzsweep, normalize_1d
from matplotlib.pyplot import pcolormesh, show, xlabel, ylabel, title, colorbar, ylim, xlim, plot, legend


#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1007/TA46_refl_flux_swp_4p2GHz4p5GHz_n10dBm_20dB.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1007/TA46_refll_flux_swp2_4p25GHz4p35GHz_n10dBm_20dB.hdf5"
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1007/TA46_refl_flux_swp_4p2GHz4p5GHz_n10dBm.hdf5"

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1008/TA46_refll_fluxpowswp_4p2GHz4pGHz.hdf5"

with File(file_path, 'r') as f:
    print f["Traces"].keys()
    print f.attrs["comment"]
    print f["Instrument config"].keys()
    #ctl_frq=f["Instrument config"]['PXI Aeroflex 302x Signal Generator - GPIB: PXI3::13::INSTR, PXI SigGen at localhost'].attrs["Frequency"] #["Power"]
    probe_frq=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192,  at localhost'].attrs["Start frequency"]
    probe_pwr=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192,  at localhost'].attrs["Output power"]

    #print probe_frq, probe_pwr, ctl_frq        
    print f["Data"]["Channel names"][:]
    Magvec=f["Traces"]["Rohde&Schwarz Network Analyzer - S12"]#[:]
    data=f["Data"]["Data"]
    #pwr2=data[:,0,:].astype(float64)
    print shape(data)

    yoko=data[:,0,0].astype(float64)
    pwr=data[0,1,:].astype(float64)
    print pwr
    fstart=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][0]
    fstep=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][1]
    print shape(Magvec)
    sm=shape(Magvec)[0]
    sy=shape(data)
    s=(sm, sy[0], sy[2]) 
    print s
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
    Magcom=reshape(Magcom, s, order="F")
    freq=linspace(fstart, fstart+fstep*(sm-1), sm)
#    
    #freq=linspace(4.0e9, 5.0e9, 1001)
    #print Magcom.dtype, pwr.dtype, yoko.dtype, freq.dtype
    #print rept
    #print yoko
    #print time
    print shape(Magcom)
    Magcom=squeeze(Magcom)
#    print shape(Magcom)
#    print shape(yoko)
#    print yoko
    #print freq
    #Magcom=mean(Magcom, axis=1)
powind=4
print pwr[powind]    
Magabs=Magcom[:, :, :]-mean(Magcom[:, 197:200, :], axis=1, keepdims=True)

fridge_att=87.0+20.0+5.0
pwrlin=0.001*10.0**((pwr[powind]-fridge_att)/10.0)

if 0:
    pcolormesh(dB(Magcom[:, :, powind]))   
    show() 
    
def cs_refl_lowfrq(fqi, pwi):    
    plot(yoko, normalize(absolute(Magabs[fqi, :, pwi])))
    g=50.0e6
    RR=lorentzian(flux_parabola(flux_rescale(yoko, offset=-0.02)), freq[fqi], [pwrlin], g)
        #RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*10.0e6))
    plot(yoko, normalize(absolute(RR)), label="50 MHz {}".format(g))
    title("Cross section reflection (normalized) \n at {frq:.3f} GHz and {pwr} dBm".format(frq=freq[fqi]/1.0e9, pwr=pwr[pwi]))
    xlabel("Flux (V)")
    ylabel("Reflection (normalized)")

def cs_refl_lowfrq_dB(fqi, pwi):    
    fqi=103
    plot(yoko, normalize(dB(Magabs[fqi, :, pwi])))
    g=70.0e6
    RR=lorentzian(flux_parabola(flux_rescale(yoko, offset=-0.07)), freq[fqi], [0*pwrlin], g)
        #RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*10.0e6))
    plot(yoko, normalize(absolute(RR)), label="50 MHz {}".format(g))
        
if 0:
    show()
    
    pcolormesh(yoko, freq, absolute(lorentzsweep(flux_parabola(flux_rescale(yoko, offset=-0.07)), freq, [pwrlin], g)))
    plot(yoko, flux_parabola(flux_rescale(yoko, offset=-0.07)), "w", linewidth=3, alpha=0.5, )
    ylim(amin(freq), amax(freq))
    
    show()

if 0:
    pcolormesh(normalize_1d(absolute(Magabs[:, :, powind])))
    show() 

if 0:
    pcolormesh(absolute(Magabs[:, :, powind]))   
    show() 

def cm_refl_lowfrq(pwi):
    pcolormesh(yoko, freq, absolute(Magabs[:, :, pwi]))   
    ylim(amin(freq), amax(freq))
    title("Flux map at reflection {pwr} dBm".format(pwr=pwr[pwi]))
    xlabel("Flux (V)")
    ylabel("Reflection")

    

def cm_refl_lowfrq_dB(pwi):
    pcolormesh(yoko, freq, dB(Magcom[:, :, pwi]))   
    ylim(amin(freq), amax(freq))


def cm_refl_lowfrq_parabola(pwi):
    pcolormesh(yoko, freq, absolute(Magabs[:, :, pwi]))   
    plot(yoko, flux_parabola(flux_rescale(yoko, offset=-0.07)), "w", linewidth=3, alpha=0.5, )
    ylim(amin(freq), amax(freq))
    title("Flux map at reflection {pwr} dBm".format(pwr=pwr[pwi]))
    xlabel("Flux (V)")
    ylabel("Reflection")


if __name__=="__main__":
    cs_refl_lowfrq(103, 4)
    show()
    cs_refl_lowfrq(85, 4)
    show()
    cs_refl_lowfrq(199, 4)
    show()
    cs_refl_lowfrq(185, 4)
    show()

    #cm_refl_lowfrq_dB(4)
    #show()
    cm_refl_lowfrq(4)
    show
    cm_refl_lowfrq_parabola(4)
    show()
