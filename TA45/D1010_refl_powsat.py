# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:54:41 2015

@author: thomasaref
"""


from h5py import File
from numpy import float64, shape, reshape, linspace, mean, amin, amax, absolute, squeeze, log10, sqrt, angle, exp, array
from TA210715A46_Fund import dB, fridge_attn, lorentzian, flux_rescale, flux_parabola, normalize
from matplotlib.pyplot import pcolormesh, show, xlabel, ylabel, title, colorbar, ylim, xlim, plot, legend

if 0:
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

if 0:
    file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1010/TA46_pxi_fluxtest.hdf5"
    
    with File(file_path, 'r') as f:
        print f.attrs["comment"]
        print f["Instrument config"]['PXI Aeroflex 302x Signal Generator - GPIB: PXI3::13::INSTR, PXI SigGen at localhost'].attrs["Power"]
        print f.keys()
        print f["Data"]["Channel names"][:]
        #Magvec=f["Traces"]["PXI Dig - Trace"]#[:]
        data=f["Data"]["Data"]
        print data.dtype
        print shape(data[:])
        #pwr=data[:,0,:]
        yoko=data[:,0,:].astype(float64)
        lvlcorr=data[:,1,:]
        PXIIQ=data[:,2,:]+1j*data[:,3,:]
        print PXIIQ.dtype #=PXIIQ.astype(float)
        print shape(PXIIQ)

    plot(absolute(absolute(PXIIQ)-0.02760)/0.000319)
    #plot(lvlcorr)    
    print shape(yoko)
    yoko=squeeze(yoko)
    fridge_att=87.0+5.0
    pwr=array([-50.0])
    pwrlin=0.001*10.0**((pwr-fridge_att)/10.0)
    plot(normalize(absolute(lorentzian(flux_parabola(flux_rescale(yoko, offset=0.06)), 4.285e9, pwrlin, 50.0e6))))
    show()

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1010/TA46_VNA_refl_twotone_powsat.hdf5"

with File(file_path, 'r') as f:
    print f["Traces"].keys()
    print f.attrs["comment"]
    print f["Instrument config"].keys()
    ctl_frq=f["Instrument config"]['PXI Aeroflex 302x Signal Generator - GPIB: PXI3::13::INSTR, PXI SigGen at localhost'].attrs["Frequency"] #["Power"]
    probe_frq=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192,  at localhost'].attrs["Start frequency"]
    probe_pwr=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192,  at localhost'].attrs["Output power"]

    print probe_frq, probe_pwr, ctl_frq        
    print f["Data"]["Channel names"][:]
    Magvec=f["Traces"]["Rohde&Schwarz Network Analyzer - S12"]#[:]
    data=f["Data"]["Data"]
    pwr2=data[:,0,:].astype(float64)
    yoko2=data[:,1,:].astype(float64)
    
    fstart=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][0]
    fstep=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][1]
    print shape(Magvec)
    print shape(data)
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
#    Magcom=squeeze(Magcom)
#    print shape(Magcom)
#    print shape(yoko)
#    print yoko
    #print freq
    #Magcom=mean(Magcom, axis=1)
#pcolormesh(absolute(Magcom[0, :, 19:31]))   
#show() 
#absMag=absolute(Magcom[-200:]) 
#yoko=yoko[-200:]  
if 0: 
    pwrlin=0.001*10**((pwr-87)/10.0)
    voltlin=sqrt(50.0*pwrlin)
    sigpwr=10*log10(absolute(PXIIQ)**2)-70
    siglin=0.001*10**(sigpwr/10.0)
    sigvolt=sqrt(50.0*siglin)
    S11=sigvolt/voltlin
    th=angle(PXIIQ)
    S11c=S11*exp(1j*th) 
    print shape(S11c)
    #plot(pwr[:,0], absolute(S11c[:,0]-S11c[:,1]))

fridge_att=87.0

def VNA_twotone_colormesh():
    pcolormesh(yoko2, pwr2[:,0]-fridge_att, dB(Magcom[0, :, :]))
    ylim(-187, -87)
    xlim(5.0, 6.0)
    xlabel("Flux (V)")
    ylabel("Control power (dBm)")
    title("Reflection (dB) Probe at 4.403 GHz, -137 dBm,\n Control at 4.285  GHz")    
        
def VNA_twotonesat():    
    powsat=mean(dB(Magcom[0, :, 19:31]), axis=1)
    print shape(pwr2)
    print pwr2[:,0]

    print yoko2[0,:]
    print shape(yoko2)

    fridge_att=87.0+15.0*0.0
    pwrlin=0.001*10.0**((pwr2[:,0]-fridge_att)/10.0)
    powsat_theory=lorentzian(flux_parabola(flux_rescale(yoko2[0,:])), 4.285e9, pwrlin, 50.0e6)
    print shape(powsat_theory)


    plot(pwr2[:,0]-fridge_att, normalize(absolute(powsat_theory[:,56])), label="Theory 50 MHz coupling")    
    plot(pwr2[:,0]-fridge_att, normalize(powsat), label="Data")#mean(dB(Magcom[0, :, 19:31]), axis=1))

    xlabel("Control power (dBm)")
    ylabel("Reflection (normalized)")
    title("Reflection (normalized) Probe at 4.403 GHz, -137 dBm, \n Control at 4.285  GHz")    
    legend(loc=3)
#    plt.pcolormesh(dB(S11c)) 
#pcolormesh(yoko, time*1e6, absolute(Magcom))

if __name__=="__main__":
    VNA_twotone_colormesh()
    show()
    VNA_twotonesat()
    show()
    