# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 11:41:40 2016

@author: thomasaref
"""

from taref.core.read_file import Read_HDF5
from taref.core.shower import shower
from taref.core.atom_extension import tag_Property
from taref.core.extra_setup import tagged_property
from numpy import float64, linspace, shape, reshape, squeeze
from h5py import File
from taref.core.universal import Array
#read_hdf=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1008/TA46_refll_fluxpowswp_4p2GHz4pGHz.hdf5")

from taref.core.agent import SubAgent, Agent
from atom.api import Float, Typed, Unicode

class Fund(Agent):
    base_name="Fund"
    fridge_att=Float(87.0+20.0+5.0).tag(unit="dB")

fund=Fund()

class Lyzer(Agent):
    rd_hdf=Typed(Read_HDF5)#.tag(private=True)
    #fd=Typed(Fund, ())


    probe_frq=Float().tag(unit="GHz", label="Probe frequency", readonly=True)
    probe_pwr=Float().tag(unit="dBm", label="Probe power", readonly=True)
    yoko=Array().tag(unit="V")
    pwr=Array().tag(unit="dBm")
    Magcom=Array()
    freq=Array().tag(unit="GHz")

    def _default_rd_hdf(self):
        return Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1008/TA46_refll_fluxpowswp_4p2GHz4pGHz.hdf5")

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            print f["Traces"].keys()
            print f.attrs["comment"]
            print f["Instrument config"].keys()
            self.probe_frq=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192,  at localhost'].attrs["Start frequency"]
            self.probe_pwr=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192,  at localhost'].attrs["Output power"]

            print f["Data"]["Channel names"][:]
            Magvec=f["Traces"]["Rohde&Schwarz Network Analyzer - S12"]#[:]
            data=f["Data"]["Data"]
            print shape(data)

            self.yoko=data[:,0,0].astype(float64)
            self.pwr=data[0,1,:].astype(float64)
            fstart=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][0]
            fstep=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][1]
            print shape(Magvec)
            sm=shape(Magvec)[0]
            sy=shape(data)
            s=(sm, sy[0], sy[2])
            print s
            Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
            Magcom=reshape(Magcom, s, order="F")
            self.freq=linspace(fstart, fstart+fstep*(sm-1), sm)
            print shape(Magcom)
            Magcom=squeeze(Magcom)
#        powind=4
#        print pwr[powind]
#        Magabs=Magcom[:, :, :]-mean(Magcom[:, 197:200, :], axis=1, keepdims=True)
#
#        fridge_att=87.0+20.0+5.0
#        pwrlin=0*0.001*10.0**((pwr[powind]-fridge_att)/10.0)


#    @tagged_property()
#    def Magvec(self):
#        Magvec=self.rd_hdf.data["Traces"]["Rohde&Schwarz Network Analyzer - S12"][:]
#        #print Magvec
#        print shape(Magvec)
#        return Magvec
#
#    @tagged_property()
#    def data(self):
#        return self.rd_hdf.data["Data"]["Data"]
#
##    @tagged_property()
##    def Magcom(self, Magvec, data):
##        sm=shape(Magvec)[0]
##        sy=shape(data)
##        s=(sm, sy[0], sy[2])
##        print s
##        Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
##        Magcom=reshape(Magcom, s, order="F")
##        print shape(Magcom)
##        Magcom=squeeze(Magcom)
##        return Magcom
#
#    @tagged_property()
#    def sm(self, Magvec):
#        return shape(Magvec)[0]
#
#    @tagged_property()
#    def yoko(self, data):
##        data=self.rd_hdf.data["Data"]["Data"]
#        #pwr2=data[:,0,:].astype(float64)
#        print shape(data)
#
#        return data[:,0,0].astype(float64)
#
#    @tagged_property()
#    def pwr(self):
#        data=self.rd_hdf.data["Data"]["Data"]
#
#        return data[0,1,:].astype(float64)
#        #print pwr
#
#    @tagged_property(unit="GHz", label="Start frequency")
#    def fstart(self):
#        return self.rd_hdf.data["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][0]
#
#    @tagged_property(unit="GHz", label="Step frequency")
#    def fstep(self):
#        return self.rd_hdf.data["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][1]
#
#    @tagged_property(unit="GHz", label="Frequency")
#    def freq(self, fstart, fstep, sm):
#        return linspace(fstart, fstart+fstep*(sm-1), sm)

a=Lyzer()
#a.rd_hdf.read()
a.read_data()
print a.probe_frq, a.probe_pwr
print a.yoko.dtype
#print a.sm
shower(a)
#read_hdf.show()