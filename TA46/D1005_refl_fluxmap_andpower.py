# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 12:39:31 2015

@author: thomasaref
"""

from h5py import File
from numpy import float64, shape, reshape, linspace, mean, amin, amax, absolute
from TA210715A46_Fund import dB, fridge_attn
from matplotlib.pyplot import pcolormesh, show, xlabel, ylabel, title, colorbar, ylim, xlim, plot

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1005/TA_A46_refl_fluxmap_andpower.hdf5"

with File(file_path, 'r') as f:
    print f.attrs["comment"]
    #print f["Traces"].keys()
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

print shape(Magcom)


#powind=0
#frqind=234
#print pwr[powind]

def plotdBnoindex():
    pcolormesh( dB(Magcom[:, 0, :]))

def plotdB_colormap(pwi):
    pcolormesh(yoko, freq, dB(Magcom[:, pwi, :]))
    xlabel("Flux (V)")
    ylabel("Frequency (Hz)")
    caption="{} dBm".format(pwr[pwi]-fridge_attn)
    title("Reflection fluxmap at {}".format(caption))
    ylim(amin(freq), amax(freq))
    colorbar()
    plotdB_colormap.caption=caption 

Magabs=Magcom-mean(Magcom[:, :, 184:188 ], axis=2, keepdims=True)


def plotabs_colormap(pwi):
    #Magabs=Magcom[:,pwi, :]-mean(Magcom[:, pwi, 184:188 ], axis=1, keepdims=True)
    pcolormesh(yoko, freq, absolute(Magabs[:,pwi,:]))
    xlabel("Flux (V)")
    ylabel("Frequency (Hz)")
    caption="{0} dBm with bgsub at {1:.2f} V".format(pwr[pwi]-fridge_attn, yoko[186])
    title("Reflection fluxmap at {}".format(caption))
    ylim(amin(freq), amax(freq))
    colorbar()
    return caption 

#print freq[106]

#plt.plot(flux_parabola((yoko-2.5)*0.195), absolute(Magcom[106, :]))
#plt.show()
#plt.plot(amax(absolute(Magcom), axis=0))
#plt.plot(absolute(Magcom[105, :]))
#plot( absolute(Magabs[106, 0,  :]))#/amax(absolute(Magcom[106, 0, :])))
#plot( absolute(Magabs[106, 5,  :]))#/amax(absolute(Magcom[106, 0, :])))
#plot( absolute(Magabs[106, 10,  :]))#/amax(absolute(Magcom[106, 0, :])))

#plot( pwr-fridge_attn, absolute(Magabs[106, :,  251]))#/amax(absolute(Magcom[106, 0, :])))

show()
if __name__=="__main__":
    plotdBnoindex()
    show()
    plotdB_colormap(0)
    show()
    plotdB_colormap(7)
    show()

    plotabs_colormap(0)
    show()

    plotabs_colormap(7)
    show()
    