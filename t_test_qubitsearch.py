# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:47:37 2015

@author: thomasaref
"""

from Atom_Read_File import Read_HDF5
from numpy import squeeze, shape, linspace, mean, transpose
#from Plotter import Plotter
#a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/T_testy16.hdf5")
#a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA_D_characterize10_2p6kOhm.hdf5")
#a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_trans_flux_swp.hdf5")

a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_fluxswp_test.hdf5")

a.read()

#print a.data["Traces"].keys()
#print a.data

Magvec=a.data["Traces"]["Agilent VNA - S21"].data
Magvec=Magvec[:,1,:]
Magvec=transpose(Magvec)-Magvec[:, 500] #mean(Magvec, axis=1, keepdims=True)

yoko=a.data["Data"]["Data"].data
yoko=squeeze(yoko)

f0, fstep=squeeze(a.data["Traces"]['Agilent VNA - S21_t0dt'].data)
l=shape(Magvec)[0]
freq=linspace(f0, f0+fstep*(l-1), l)

#a=Plotter()
from numpy import array
from matplotlib.collections import LineCollection

print shape(Magvec)
#a.axe.plot(yoko, Magvec[1,:])
#a.axe.imshow(Magvec)
#b=LineCollection(((yoko, Magvec[1,:]),))
#a.show()

import matplotlib.pyplot as plt
plt.imshow(Magvec)
plt.show()