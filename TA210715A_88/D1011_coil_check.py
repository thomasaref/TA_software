# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from taref.core.api import Array
from TA88_fundamental import TA88_Lyzer, TA88_Read
from taref.plotter.api import colormesh, line, Plotter, scatter
from numpy import interp, poly1d, polyfit, array, absolute, squeeze, append, sqrt, pi, mod, floor_divide, trunc, arccos, shape, float64
from h5py import File


def read_data(self):
    with File(self.rd_hdf.file_path, 'r') as f:
        print f.keys()
        #print f["Channels"]
        data=f["Data"]["Data"]
        self.comment=f.attrs["comment"]
        self.yoko=data[:,0,0].astype(float64)
        self.current=data[:, 1, 0].astype(float64)
        #fstart=f["Traces"]['RS VNA - S21_t0dt'][0][0]
        #fstep=f["Traces"]['RS VNA - S21_t0dt'][0][1]
        #sm=shape(Magvec)[0]
        #sy=shape(data)
        #print sy
        #s=(sm, sy[0], 1)#sy[2])
        #Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        #Magcom=reshape(Magcom, s, order="F")
        #self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        #self.MagcomData=squeeze(Magcom)
        #self.stop_ind=len(self.yoko)-1
        #self.filt.N=len(self.frequency)


class Coil_Lyzer(TA88_Lyzer):
    current=Array().tag(unit="V", plot=True, label="Current", sub=True)

a=Coil_Lyzer(read_data=read_data,
        rd_hdf=TA88_Read(main_file="Data_1011/test_coil_setup_overnight.hdf5"))

a.read_data()
#print a.yoko
#print a.current
pf=polyfit(a.yoko, a.current, 3)
print pf
p=poly1d(pf)
pl=scatter(a.yoko, a.current)
line(a.yoko, p(a.yoko), pl=pl)#.show()
#pl=scatter(a.yoko, a.current)
endskip=0
mean_yoko=(a.yoko[1500-endskip:500+endskip:-1]+a.yoko[1500+endskip:2500-endskip]+a.yoko[3500-endskip:2500+endskip:-1]+a.yoko[3500+endskip:4500-endskip])/4.0
mean_current=(a.current[1500-endskip:500+endskip:-1]+a.current[1500+endskip:2500-endskip]+a.current[3500-endskip:2500+endskip:-1]+a.current[3500+endskip:4500-endskip])/4.0

#mean_current=(a.current[1499:501:-1]+a.current[1501:2499]+a.current[3499:2501:-1]+a.current[3501:4499])/4.0
line(a.yoko, a.current-p(a.yoko))#.show()
line(a.yoko)

line(a.yoko[a.yoko<5.9], a.current[a.yoko<5.9]-interp(a.yoko[a.yoko<5.9], mean_yoko, mean_current)).show()

line(a.yoko, a.current-interp(a.yoko, a.yoko[1500:500:-1], a.current[1500:500:-1])).show()
line(a.yoko[a.yoko<5.9], a.current-interp(a.yoko, a.yoko[1500:2500], a.current[1500:2500])).show()



