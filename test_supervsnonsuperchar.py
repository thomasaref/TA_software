# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:12:13 2015

@author: thomasaref
"""

from h5py import File
from numpy import shape, reshape, float64, mean, linspace, absolute, log10, squeeze
from matplotlib.pyplot import plot, show, legend


def read_VNA(file_path):
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
        pwr=data[:, 0, 0].astype(float64)
        #pwr=delete(pwr, 73)
        #rept= data[0, 1, :].astype(float64)
        freq=linspace(fstart, fstart+fstep*(sm-1), sm)
        
        #print Magcom.dtype, pwr.dtype, yoko.dtype, freq.dtype
        print pwr
        Magcom=squeeze(Magcom)
        print shape(Magcom)
    return freq, Magcom

def dB(x):
    return 20*log10(absolute(x))   

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_101kOhm_transl_4t5.hdf5"

freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:, 0]))

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_2600Ohm_transl_4t5.hdf5"
freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:,0]))

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_2700Ohm_transl_4t5.hdf5"
freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:,0]), label="2.7 kOhms")

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_3800Ohm_transl_4t5.hdf5"
#freq, Magcom=read_VNA(file_path)    
#plot(freq, dB(Magcom[:,0]), label="3.8 kOhms")

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_4100Ohm_transl_4t5.hdf5"
#freq, Magcom=read_VNA(file_path)    
#plot(freq, dB(Magcom[:,0]), label="4.1 kOhms")
legend()
show()


file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_101kOhm_refl_4t5.hdf5"
freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:,0]), label="101 kOhms")


file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_2600Ohm_refl_4t5.hdf5"
freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:,0])+1.5, label="2.6 kOhms")
show()


file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_101kOhm_refl_3t8.hdf5"
freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:,0]), label="101 kOhms")


file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_2600Ohm_refl_3t8.hdf5"
freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:,0])+1.5, label="2.6 kOhms")
show()

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_101kOhm_transl_3t8.hdf5"
freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:,0]), label="101 kOhms")


file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_1001/TA_A58_wuchar_2600Ohm_transl_3t8.hdf5"
freq, Magcom=read_VNA(file_path)    
plot(freq, dB(Magcom[:,0])+5, label="2.6 kOhms")
show()
