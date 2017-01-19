# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:47:37 2015

@author: thomasaref
"""

from Atom_Read_File import Read_HDF5
from numpy import squeeze, shape, linspace, mean, transpose, log10
#from Plotter import Plotter
#a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/T_testy16.hdf5")
#a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA_D_characterize10_2p6kOhm.hdf5")
#a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_trans_flux_swp.hdf5")

#a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_fluxswp_test.hdf5")
a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_fluxswp_n3dBm.hdf5")

a.read()

#print a.data["Traces"].keys()
#print a.data

Magvec=a.data["Traces"]["Agilent VNA - S21"].data
print shape(Magvec)
from numpy import absolute
Magvec=20*log10(absolute(Magvec[:,0,:]+1j*Magvec[:,1,:]))
#Magvec=transpose(Magvec)-Magvec[:, 500] #mean(Magvec, axis=1, keepdims=True)
#Magvec=transpose(transpose(Magvec)-Magvec[:, 0])

yoko=a.data["Data"]["Data"].data
yoko=squeeze(yoko)

f0, fstep=squeeze(a.data["Traces"]['Agilent VNA - S21_t0dt'].data)
l=shape(Magvec)[0]
freq=linspace(f0, f0+fstep*(l-1), l)


b=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA_D_characterize5.hdf5")
b.read()

Magvecb=b.data["Traces"]["Agilent VNA - S21"].data
print shape(Magvecb)
Magvecb=20*log10(absolute(Magvecb[:,0,:]+1j*Magvecb[:,1,:]))-20

f0, fstep=squeeze(b.data["Traces"]['Agilent VNA - S21_t0dt'].data)
l=shape(Magvecb)[0]
freqb=linspace(f0, f0+fstep*(l-1), l)


#a=Plotter()
#from numpy import array
#a.axe.plot(freq, Magvec[:,1])
#a.axe.imshow(Magvec)
#b=LineCollection(((yoko, Magvec[1,:]),))
#a.show()

import matplotlib.pyplot as plt
#plt.plot(freq, Magvec[:,1])
#plt.plot(freqb, Magvecb[:,1])

#ax=plt.imshow(Magvec, aspect="auto", extent=[min(yoko),max(yoko), min(freq),max(freq)])#, interpolation="sinc") 
#ax.axes.set_title("blah")
#ax.axes.set_xlabel("yoko")
#ax.axes.set_ylabel("freq")


from matplotlib.collections import LineCollection
from matplotlib.colors import colorConverter
# Make a list of colors cycling through the rgbcmyk series.
colors = [colorConverter.to_rgba(c) for c in ('r','g','b','c','y','m','k')]

fig, ax4 = plt.subplots(1,1)
#nverts = 60
#ncurves = 20
#offs = (0.1, 0.0)
#
#from numpy import amax, cos, random, pi
#rs = random.RandomState([12345678])
#
#yy = linspace(0, 2*pi, nverts)
#ym = amax(yy)
#xx = (0.2 + (ym-yy)/ym)**2 * cos(yy-0.4) * 0.5
#segs = []
#for i in range(ncurves):
#    xxx = xx + 0.02*rs.randn(nverts)
#    curve = list(zip(xxx, yy*100))
#    segs.append(curve)
#    if i<2:
#        print segs

segs=[]
segs.append(list(zip(freq, Magvec[:, 1])))
segs.append(list(zip(freqb, Magvecb[:, 1])))

col = LineCollection(segs)#, offsets=offs)
ax4.add_collection(col, autolim=True)
col.set_color(colors)
ax4.autoscale_view()
ax4.set_title('Successive data offsets')
ax4.set_xlabel('Zonal velocity component (m/s)')
#ax4.set_ylabel('Depth (m)')
# Reverse the y-axis so depth increases downward
#ax4.set_ylim(ax4.get_ylim()[::-1])

plt.show()