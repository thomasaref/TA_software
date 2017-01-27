# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Lyzer, TA53_Read, qdt, idt
from numpy import (absolute,  trunc, arccos, shape, float64, linspace, reshape,
                   squeeze, argmax, array, log10, swapaxes, amax, angle)
from taref.plotter.api import colormesh, scatter, line
from h5py import File
from taref.core.api import process_kwargs
from taref.physics.filtering import Filter
from time import time

def read_data(self):
    with File(self.rd_hdf.file_path, 'r') as f:
        Magvec=f["Traces"]["{0} - {1}".format(self.VNA_name, self.port_name)]
        data=f["Data"]["Data"]
        print data.shape
        print Magvec.shape
        #if self.swp_type=="pwr_first":
        #    self.pwr=data[:, 0, 0].astype(float64)
        #    self.yoko=data[0,1,:].astype(float64)
        #elif self.swp_type=="yoko_first":
        #    self.pwr=data[0, 1, :].astype(float64)
        #    self.yoko=data[:, 0, 0].astype(float64)
        self.comment=f.attrs["comment"]
        fstart=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][0]
        fstep=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][1]

        sm=shape(Magvec)[0]
        sy=shape(data)
        s=(sm, sy[0], sy[2])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        #if self.swp_type=="pwr_first":
        #    Magcom=swapaxes(Magcom, 1, 2)
        self.MagcomData=squeeze(Magcom)#[:, 2, :]
        #self.stop_ind=len(self.yoko)-1
        self.filt.N=len(self.frequency)


a=TA53_VNA_Lyzer(name="d1122", on_res_ind=301,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1122/S3A4_careful_trans_direct.hdf5"), #long_test.hdf5"), #
        fit_indices=[range(850, 2300)], #range(48,154+1), range(276, 578+1)],
         desc="transmission power sweep",
         offset=-0.1,
         read_data=read_data,
        # swp_type="yoko_first",
        )
a.filt.center=0 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
a.filt.halfwidth=80 #8 #10
#a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.3 #0.035
a.flux_axis_type="fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"
a.end_skip=20
#a.flux_indices=[range(len(a.yoko)-1)]
a.rt_atten=30
a.save_folder.main_dir=a.name

a.read_data()

def ifft_plot(self, **kwargs):
    process_kwargs(self, kwargs, pl="hannifft_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
    on_res=absolute(self.filt.window_ifft(self.Magcom))

    pl=line(self.time_axis, self.filt.fftshift(on_res),  color="red",
           plot_name="onres_{}".format(self.on_res_ind),label="blah", **kwargs)

    self.filt.N=len(on_res)
    filt=self.filt.freqz
    #filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
    top=amax(on_res)
    line(self.time_axis, filt*top, plotter=pl, color="green", label="wdw")
    pl.xlabel=kwargs.pop("xlabel", self.time_axis_label)
    pl.ylabel=kwargs.pop("ylabel", "Mag abs")
    return pl
    
def MagcomFilt(self):
    if self.filt.filter_type=="FIR":
        return self.filt.fir_filter(self.MagcomData)
    return self.filt.fft_filter(self.MagcomData)

#a.pwr_ind=0
if __name__=="__main__":
    a.filter_type="None"
    pl=line(a.frequency, a.MagAbs)#.show()
    pl=line(a.frequency, a.MagdB)#.show()

    magfilt=MagcomFilt(a)
    magabs=absolute(magfilt)
    line(a.frequency, magabs)
    pl=line(a.frequency, 10.0*log10(magabs), color="red", pl=pl)
    idt.Np=56
    idt.f0=4.46e9 #4.452
    idt.K2=0.032
    (S11, S12, S13,
     S21, S22, S23,
     S31, S32, S33)=idt._get_simple_S(f=a.frequency)

    print idt.f0
    print a.comment
    print -a.fridge_atten+a.fridge_gain-a.rt_atten+a.rt_gain-10

    line(a.frequency, 10*log10(absolute(S13*S31))-14, color="green", pl=pl).show()    

    line(a.frequency, angle(magfilt))


    ifft_plot(a).show()
    #pl_raw=a.magabs_colormesh()
    #a.bgsub_type="dB"
    #a.magabs_colormesh()
    #pl1=colormesh(absolute(a.MagcomData[:, :, 30]))

    #pl_ifft=a.ifft_plot()#.show()
    #a.pwr_ind=22

    a.filter_type="FFT"
    line(a.frequency, a.MagAbs, pl=pl, color="red").show()

    pl_fft=a.magabs_colormesh()#.show()
    a.bgsub_type="None"
    pl1=a.magdB_colormesh()
    pl2=a.magabs_colormesh()
    #a.filter_type="Fit"
    #a.magabs_colormesh(pl=pl2)
    #a.magdB_colormesh(pl=pl1)
    #a.center_plot()
    #a.widths_plot().show()


    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomData[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip], absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 335, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()

    pl2=scatter(a.pwr, absolute(absolute(a.MagcomFilt[69, 335, :])-absolute(a.MagcomFilt[69,0, :])), xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$")#.show()

    pls=[pl_raw, pl_ifft, pl_fft, pl1, pl2, pl3]
    #a.save_plots(pls)
    pls[0].show()
