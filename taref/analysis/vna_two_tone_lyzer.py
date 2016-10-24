# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:24:54 2016

@author: thomasaref
"""
from taref.core.api import Array, private_property, tag_property, reset_property
from taref.analysis.api import VNA_Pwr_Lyzer
from h5py import File
from numpy import float64, shape, reshape, linspace, squeeze, array, absolute, sqrt, swapaxes
from atom.api import Enum, Int

def read_data(self):
    with File(self.rd_hdf.file_path, 'r') as f:
        Magvec=f["Traces"]["{0} - {1}".format(self.VNA_name, self.port_name)]
        data=f["Data"]["Data"]
        print shape(Magvec[:]) #91*11=1001
        self.frq2=data[:, 0, 0]
        self.yoko=reshape(data[0,1, :], (91, 11), order="F")[:, 0]
        self.pwr=reshape(data[0,2, :], (91, 11), order="F")[0, :]

        raise Exception
        if self.swp_type=="pwr_first":
            self.pwr=data[:, 0, 0].astype(float64)
            self.yoko=data[0,1,:].astype(float64)
        elif self.swp_type=="yoko_first":
            self.pwr=data[0, 1, :].astype(float64)
            self.yoko=data[:, 0, 0].astype(float64)
        self.comment=f.attrs["comment"]
        fstart=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][0]
        fstep=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][1]

        sm=shape(Magvec)[0]
        sy=shape(data)
        s=(sm, sy[0], sy[2])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        if self.swp_type=="pwr_first":
            Magcom=swapaxes(Magcom, 1, 2)
        self.MagcomData=squeeze(Magcom)#[:, 2, :]
        self.stop_ind=len(self.yoko)-1
        self.filt.N=len(self.frequency)

class VNA_Two_Tone_Lyzer(VNA_Pwr_Lyzer):
    base_name="vna_two_tone_lyzer"

    frq2=Array().tag(unit="GHz", label="2nd frequency", sub=True)


    frq2_ind=Int()

    swp_type=Enum("pwr_first", "yoko_first")

    def _default_read_data(self):
        return read_data

    #def _observe_pwr_ind(self, change):
    #    reset_property(self, "Magcom")

    @tag_property(sub=True)
    def Magcom(self):
        if self.filter_type=="None":
            Magcom=self.MagcomData
        elif self.filter_type=="Fit":
            return self.MagAbsFit
        else:
            Magcom=self.MagcomFilt[self.indices, :, :]
        if self.bgsub_type=="Complex":
            return self.bgsub(Magcom)
        return Magcom[:, :, self.pwr_ind]

#array([[self.fft_filter_full(m, n, Magcom) for n in range(len(self.yoko))] for m in range(len(self.pwr))]).transpose()

    @private_property
    def MagcomFilt(self):
        if self.filt.filter_type=="FIR":
            return array([[self.filt.fir_filter(self.MagcomData[:,n,m]) for n in self.flat_flux_indices] for m in range(len(self.pwr))]).transpose()
        return array([[self.filt.fft_filter(self.MagcomData[:,n,m]) for n in self.flat_flux_indices]  for m in range(len(self.pwr))]).transpose()

    @tag_property( sub=True)
    def MagAbsFilt_sq(self):
        return absolute(self.MagcomFilt[:, :, self.pwr_ind])**2

    @private_property
    def fit_params(self):
        if self.fitter.fit_params is None:
            self.fitter.full_fit(x=self.flux_axis[self.flat_flux_indices], y=self.MagAbsFilt_sq, indices=self.flat_indices, gamma=self.fitter.gamma)
            if self.calc_p_guess:
                self.fitter.make_p_guess(self.flux_axis[self.flat_flux_indices], y=self.MagAbsFilt_sq, indices=self.flat_indices, gamma=self.fitter.gamma)
        return self.fitter.fit_params

    @private_property
    def MagAbsFit(self):
        return sqrt(self.fitter.reconstruct_fit(self.flux_axis[self.flat_flux_indices], self.fit_params))


