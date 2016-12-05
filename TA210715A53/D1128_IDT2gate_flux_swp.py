# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Two_Tone_Pwr_Lyzer, TA53_Read, qdt
from numpy import (absolute,  trunc, arccos, shape, float64, linspace, reshape,
                   squeeze, argmax, array, log10, swapaxes, amax, angle)
from taref.plotter.api import colormesh, scatter, line
from h5py import File
from taref.core.api import process_kwargs
from taref.physics.filtering import Filter
from time import time


def read_data(self):
    with File(self.rd_hdf.file_path, 'r') as f:
        self.comment=f.attrs["comment"]

        Magvec=f["Traces"]["{0} - {1}".format(self.VNA_name, self.port_name)]
        data=f["Data"]["Data"]
        print shape(Magvec) #91*11=1001
        print shape(data)
        self.yoko=data[:, 0, 0].astype(float64)
        self.pwr2=data[0, 1, :8].astype(float64)
        self.frq2=data[0, 2, ::8].astype(float64)
        sm=shape(Magvec)[0]
        s=(sm, self.yoko.shape[0], self.pwr2.shape[0], self.frq2.shape[0])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        fstart=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][0]
        fstep=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][1]
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        print Magcom.shape
        #Magcom=swapaxes(Magcom, 1, 2)
        print Magcom.shape
        self.MagcomData=squeeze(Magcom)
        self.stop_ind=len(self.yoko)-1
        self.filt.N=len(self.frequency)

a=TA53_VNA_Two_Tone_Pwr_Lyzer(name="d1128", on_res_ind=54,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1128/S4A1S1_pwr_flux_2frq.hdf5"), #long_test.hdf5"), #
        #fit_indices=[range(850, 2300)], #range(48,154+1), range(276, 578+1)],
         desc="transmission power sweep",
         offset=-0.1,
         read_data=read_data,
         swp_type="yoko_first",
        )
a.filt.center=31 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
a.filt.halfwidth=10 #8 #10
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.3 #0.035
a.flux_axis_type="yoko" #"fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"
a.end_skip=20
#a.flux_indices=[range(len(a.yoko)-1)]
#a.time_axis_type="time"
a.save_folder.main_dir=a.name

a.read_data()
a.pwr2_ind=7
a.frq2_ind=1

if __name__=="__main__":
    a.filter_type="None"
    colormesh(absolute(a.MagcomData[:, :, 7, a.frq2_ind]))#.show()

def ifft_plot(self, **kwargs):
    process_kwargs(a, kwargs, pl="hannifft_{0}_{1}_{2}".format(a.filter_type, a.bgsub_type, a.name))
    on_res=absolute(self.filt.window_ifft(self.MagcomData[:,self.on_res_ind, self.pwr2_ind, self.frq2_ind]))
    strt=absolute(self.filt.window_ifft(self.MagcomData[:,self.start_ind, self.pwr2_ind, self.frq2_ind]))
    stop=absolute(self.filt.window_ifft(self.MagcomData[:,self.stop_ind, self.pwr2_ind, self.frq2_ind]))

    pl=line(self.time_axis, self.filt.fftshift(on_res),  color="red",
           plot_name="onres_{}".format(self.on_res_ind),label="{:.4g}".format(self.on_res_ind), **kwargs)
    line(self.time_axis, self.filt.fftshift(strt), pl=pl, linewidth=1.0, color="purple",
         plot_name="strt {}".format(self.start_ind), label="{:.4g}".format(self.start_ind))
    line(self.time_axis, self.filt.fftshift(stop), pl=pl, linewidth=1.0, color="blue",
         plot_name="stop {}".format(self.stop_ind), label="{:.4g}".format(self.stop_ind))

    self.filt.N=len(on_res)
    filt=self.filt.freqz
    #filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
    top=max([amax(on_res), amax(strt), amax(stop)])
    line(self.time_axis, filt*top, plotter=pl, color="green", label="wdw")
    pl.xlabel=kwargs.pop("xlabel", self.time_axis_label)
    pl.ylabel=kwargs.pop("ylabel", "Mag abs")
    return pl

pl2=ifft_plot(a)#.show()

if 1:
    tstart=time()
    double_filt= array([[[a.filt.fft_filter(a.MagcomData[:,n, m, p]) for n in range(len(a.yoko))] for m in range(len(a.pwr2))] for p in range(len(a.frq2))])#.transpose()
    print time()-tstart
    print double_filt.shape
    double_filt=swapaxes(double_filt, 0, 3)
    double_filt=swapaxes(double_filt, 1, 2)
    print double_filt.shape
    for i in range(len(a.pwr2)):
        pl=colormesh(absolute(double_filt[a.end_skip:-a.end_skip,:, i,a.frq2_ind]))#.show()
    colormesh(absolute(double_filt[a.end_skip:-a.end_skip,54, :,a.frq2_ind])).show()

if 0:
    pl_raw=a.magabs_colormesh()
    a.phase_colormesh()

    a.bgsub_type="dB"
    a.magabs_colormesh()
    #pl1=colormesh(absolute(a.MagcomData[:, :, 30]))

    pl_ifft=a.ifft_plot()#.show()
    #a.pwr_ind=22

    a.filter_type="FFT"
    pl_fft=a.magabs_colormesh()#.show()
    a.magdB_colormesh()
    a.phase_colormesh()

    a.bgsub_type="None"
    pl1=a.magdB_colormesh()
    a.phase_colormesh()
    pl2=a.magabs_colormesh().show()
    a.filter_type="Fit"
    a.magabs_colormesh(pl=pl2)
    a.magdB_colormesh(pl=pl1)
    cp=a.center_plot()
    wp=a.widths_plot().show()
    a.pwr_ind=1
    a.filter_type="FFT"
    pl_fft=a.magabs_colormesh().show()
    a.bgsub_type="None"
    pl1=a.magdB_colormesh()
    pl2=a.magabs_colormesh()
    a.filter_type="Fit"
    a.magabs_colormesh(pl=pl2)
    a.magdB_colormesh(pl=pl1)
    a.center_plot(pl=cp, color="red")
    a.widths_plot(pl=wp, color="red").show()


    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomData[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip], absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 335, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()

    pl2=scatter(a.pwr, absolute(absolute(a.MagcomFilt[69, 335, :])-absolute(a.MagcomFilt[69,0, :])), xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$")#.show()

    pls=[pl_raw, pl_ifft, pl_fft, pl1, pl2, pl3]
    #a.save_plots(pls)
    pls[0].show()
