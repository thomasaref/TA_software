# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:26:51 2015

@author: thomasaref
"""

from h5py import File
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0914/TA_A58_scb_refl_powsat_1.hdf5"
from numpy import squeeze, shape, linspace, log10, mean, amax, amin, absolute, reshape, transpose, real, imag, angle

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0912/TA_A58_scb_trans_powfluxswp_higherbw.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0913/TA_A58_scb_refl_powfluxswp_higherbw_revV.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp_higherpower.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0911/TA_A58_scb_refl_powfluxswp_higherbw.hdf5"
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp.hdf5"
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0915/TA_A58_scb_refl_powfluxswp_lowpow.hdf5"

powind=0
frqind=4
#from HDF5_functions import read_hdf5

#print read_hdf5(file_path)

with File(file_path, 'r') as f:
    Magvec=f["Traces"]["Agilent VNA - S21"]#[:]
    data=f["Data"]["Data"]
    f0=f["Traces"]['Agilent VNA - S21_t0dt'][0][0]
    fstep=f["Traces"]['Agilent VNA - S21_t0dt'][0][1]

    sm=shape(Magvec)[0]
    sy=shape(data)
    s=(sm, sy[0], sy[2]) 
    print s
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
    Magcom=reshape(Magcom, s, order="F")

    yoko=data[:, 0, 0]
    pwr= data[0, 1, :]
    freq=linspace(f0, f0+fstep*(sm-1), sm)

print pwr

def dB(x):
    return 20*log10(absolute(x))

#Magvec=Magdict[0]
#print shape(Magvec)
#diffS11=[]    
#for n, a in enumerate(yoko):
#    Magvec=Magdict[yoko[n]]
    #MagvecdB=dB(Magvec)
#MagvecdB=Magdict[:,0,:]-mean(Magdict[:,0,:], axis=0, keepdims=True)
#    diffS11.append(amax(MagvecdB)-amin(MagvecdB))

import matplotlib.pyplot as plt

#plt.plot(dB(Magcom[:, :, 0]))
#Magcom=Magcom[:,:, powind]-mean(Magcom[:, :, powind ], axis=1, keepdims=True)

#diffS11=(amax(Magcom[4, powind, :]))
#diffS11=[]
#for n, a in enumerate(pwr):
#    MagcomdB=Magcom[:,:,n]-mean(Magcom[:,  82:83, n ], axis=1, keepdims=True)
#    MagcomdB=absolute(MagcomdB)
#    #diffS11.append(MagcomdB[942, 140]-MagcomdB[942, 85])
#    diffS11.append(mean(MagcomdB[866:1000, 124:155], axis=1)-mean(MagcomdB[866:1000, 73:96], axis=1))

#diffS11=amax(Magcom[frqind, :, 20:], axis=1)-amin(Magcom[frqind, :, 20:], axis=1)
#diffS11=absolute(Magcom[frqind, :, 57]-Magcom[frqind, :, 16])

if 0:
    Magy=amax(dB(Magcom[:, :, powind]), axis=1)-amin(dB(Magcom[:, :, powind]), axis=1)
    #plt.plot(Magy)
    ind1=0
    ind2=250
    plt.plot(dB(Magcom[:, :, powind]-mean(Magcom[:, :, powind], axis=1, keepdims=True)))
    plt.show()
#MagcomdB=Magcom[890, :, :]    
#MagcomdB=mean(Magcom[985:995,:, :], axis=0)
MagcomdB=mean(Magcom[120:125,:, :], axis=0)

#MagcomdB=mean(Magcom[944:946,:, :], axis=0)
#MagcomdB=mean(Magcom[419:421,:, :], axis=0)
MagcomdB=dB(MagcomdB)
MagcomdB=absolute(Magcom[:, 50:, powind]-mean(Magcom[:, 50:, powind], axis=1, keepdims=True))

#print freq[985:995]
print freq[122:123]

#powind=0
#frqind=4
if 0:
    file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp_higherpower.hdf5"
    
    with File(file_path, 'r') as f:
        Magvec=f["Traces"]["Agilent VNA - S21"][:]
        data=f["Data"]["Data"][:]
        f0, fstep=squeeze(f["Traces"]['Agilent VNA - S21_t0dt'][:])
    
    sm=shape(Magvec)[0]
    sy=shape(data)
    s=(sm, sy[0], sy[2]) 
    print s
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
    Magcom=reshape(Magcom, s, order="F")
    
    yoko=data[:, 0, 0]
    pwr= data[0, 1, :]
    freq=linspace(f0, f0+fstep*(sm-1), sm)
    
    print pwr
    
    MagcomdB2=mean(Magcom[985:995,:, :], axis=0)
    MagcomdB2=dB(MagcomdB2)

    print freq[985:995]

if 0:
    #plt.plot(MagcomdB[:, powind])
    #plt.plot(MagcomdB[133, :])
    plt.plot(pwr-20-87, mean(MagcomdB[130:136,:]+20, axis=0)-mean(MagcomdB[230:240,:]+20, axis=0))
    plt.plot(pwr-87, mean(MagcomdB2[135:145,:], axis=0)-mean(MagcomdB2[230:240,:], axis=0))

if 1:
    plt.imshow( MagcomdB[:, :], 
                #vmin=amin(MagcomdB),
                #vmax=-41.4, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                #extent=[amin(yoko),amax(yoko), amin(freq),amax(freq)],            
                 )
    plt.colorbar()
plt.show()
#Magcom=Magcom[frqind, :, :]#-mean(Magcom[frqind, :, :], axis=0, keepdims=True)
#plt.plot(transpose(absolute(Magcom[(0, 5, 10, 15, 25, 30), :])))
#plt.legend([0, 5, 10, 15, 25, 30])
#plt.show()

#MagcomdB=Magcom[:,:,powind]-mean(Magcom[:, 381:382, powind ], axis=1, keepdims=True)
#MagcomdB=absolute(MagcomdB)
#
##MagcomdB=dB(Magcom)
#plt.imshow(  MagcomdB[:, :], 
#            #vmin=amin(Magvec),
#            #vmax=0.001, #amax(Magvec), 
#            aspect="auto", origin="lower",
#            interpolation="none",
#            #extent=[amin(yoko),amax(yoko), amin(freq),amax(freq)],
#            
#             )
#plt.colorbar()
#plt.show()
        
#powind=3
#Magvec=Magdict[pwr[powind]]
#print pwr[powind]
##print shape(Magvec[509, :]), shape(yoko)