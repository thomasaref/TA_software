# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:26:51 2015

@author: thomasaref
"""

from h5py import File
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0914/TA_A58_scb_refl_powsat_1.hdf5"
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0914/TA_A58_scb_refl_powsat_2.hdf5"

from numpy import squeeze, shape, linspace, log10, mean, amax, amin, absolute, reshape, transpose

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0912/TA_A58_scb_trans_powfluxswp_higherbw.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0913/TA_A58_scb_refl_powfluxswp_higherbw_revV.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp_higherpower.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0911/TA_A58_scb_refl_powfluxswp_higherbw.hdf5"

powind=22
frqind=7

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

yoko= data[:, 0, 0]
pwr=data[0, 1, :]
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
#    MagcomdB=Magcom[:,n,:]-mean(Magcom[:,  n, : ], axis=1, keepdims=True)
#    MagcomdB=absolute(MagcomdB)
##    diffS11.append(amax(MagcomdB[:, 57]-MagcomdB[:, 16])
##    diffS11.append(amax(MagcomdB[:, 20:], axis=1)-amin(MagcomdB[:, 20:], axis=1))
#    diffS11.append(mean(MagcomdB[:, 47:71], axis=1)-mean(MagcomdB[:, 12:27], axis=1))

#diffS11=amax(Magcom[frqind, :, 20:], axis=1)-amin(Magcom[frqind, :, 20:], axis=1)
#diffS11=absolute(Magcom[frqind, :, 57]-Magcom[frqind, :, 16])

#plt.plot( pwr, transpose(meandB(Magcom[frqind, 7, : ])))#-dB(Magcom[:, 208, : ])))
#plt.plot( pwr, transpose(mean(dB(Magcom)[frqind, 4:10, : ], axis=1)))#-dB(Magcom[:, 208, : ])))

#plt.plot(pwr, diffS11)
#plt.show()
#Magcom=Magcom[frqind, :, :]#-mean(Magcom[frqind, :, :], axis=0, keepdims=True)
#plt.plot(transpose(absolute(Magcom[(0, 5, 10, 15, 25, 30), :])))
#plt.legend([0, 5, 10, 15, 25, 30])
#plt.show()

#MagcomdB=Magcom[:,powind,:]-mean(Magcom[:,  powind, 16:17 ], axis=1, keepdims=True)
MagcomdB=Magcom[frqind,:,:]#-mean(Magcom[:,  powind, 16:17 ], axis=1, keepdims=True)

#MagcomdB=absolute(MagcomdB)

MagcomdB=dB(MagcomdB)
#MagcomdB=mean(dB(Magcom), axis=0)#-mean(Magcom[:,  powind, 16:17 ], axis=1, keepdims=True)

plt.imshow(  MagcomdB[:, :], 
            #vmin=amin(Magvec),
            #vmax=0.001, #amax(Magvec), 
            aspect="auto", origin="lower",
            interpolation="none",
            #extent=[amin(yoko),amax(yoko), amin(freq),amax(freq)],
            
             )
plt.colorbar()
plt.show()
        
#powind=3
#Magvec=Magdict[pwr[powind]]
#print pwr[powind]
##print shape(Magvec[509, :]), shape(yoko)