# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, qdt
from numpy import (absolute,  trunc, arccos, shape, float64, linspace, reshape,
                   squeeze, argmax, array, log10, swapaxes, amax, angle)
from taref.plotter.api import colormesh, scatter, line
from h5py import File
from taref.core.api import process_kwargs
from taref.physics.filtering import Filter
from time import time


a=TA53_VNA_Pwr_Lyzer(name="d1117", on_res_ind=301,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1117/S3A4_trans_swp_n12n10dBm.hdf5"), #long_test.hdf5"), #
        fit_indices=[range(850, 2300)], #range(48,154+1), range(276, 578+1)],
         desc="transmission power sweep",
         offset=-0.1,
        # read_data=read_data,
         swp_type="yoko_first",
        )
a.filt.center=0 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
a.filt.halfwidth=400 #8 #10
#a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.3 #0.035
a.flux_axis_type="fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"
a.end_skip=20
#a.flux_indices=[range(len(a.yoko)-1)]

a.save_folder.main_dir=a.name

a.read_data()
a.pwr_ind=0
if __name__=="__main__":
    a.filter_type="None"
    pl_raw=a.magabs_colormesh()
    a.bgsub_type="dB"
    a.magabs_colormesh()
    #pl1=colormesh(absolute(a.MagcomData[:, :, 30]))

    pl_ifft=a.ifft_plot()#.show()
    #a.pwr_ind=22

    a.filter_type="FFT"
    pl_fft=a.magabs_colormesh()#.show()
    a.bgsub_type="None"
    pl1=a.magdB_colormesh()
    pl2=a.magabs_colormesh()
    a.filter_type="Fit"
    a.magabs_colormesh(pl=pl2)
    a.magdB_colormesh(pl=pl1)
    a.center_plot()
    a.widths_plot().show()


    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomData[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip], absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 335, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()

    pl2=scatter(a.pwr, absolute(absolute(a.MagcomFilt[69, 335, :])-absolute(a.MagcomFilt[69,0, :])), xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$")#.show()

    pls=[pl_raw, pl_ifft, pl_fft, pl1, pl2, pl3]
    #a.save_plots(pls)
    pls[0].show()
