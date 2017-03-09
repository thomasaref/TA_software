# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, qdt, TA53_Save_NP, TA53_Read_NP
from numpy import (absolute,  trunc, arccos, shape, float64, linspace, reshape,
                   squeeze, argmax, array, log10, swapaxes, amax, angle)
from taref.plotter.api import colormesh, scatter, line
from h5py import File
from taref.core.api import process_kwargs
from taref.physics.filtering import Filter
from time import time


from TA88_fundamental import bg_A1, bg_A4



a=TA53_VNA_Pwr_Lyzer(name="d1112", on_res_ind=635,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1112/S3A4_trans_pwr_swp.hdf5"), #long_test.hdf5"), #
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="transmission power sweep",
         offset=-0.3,
        # read_data=read_data,
         swp_type="yoko_first",
        )
a.filt.center=0 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
a.filt.halfwidth=12 #8 #10
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.1 #0.035
a.flux_axis_type="flux" #"yoko" #"flux" #"fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"
a.end_skip=20
#a.flux_indices=[range(len(a.yoko)-1)]

a.save_folder.main_dir=a.name

a.read_data()
a.pwr_ind=22
if __name__=="__main__":
    a.filter_type="None"
    pl_raw=a.magabs_colormesh()
    #pl1=colormesh(absolute(a.MagcomData[:, :, 30]))

    pl_ifft=a.ifft_plot()#.show()
    #a.pwr_ind=22

    a.filter_type="FFT"
    pl_fft=a.magabs_colormesh()#.show()
    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomData[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip], absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 635, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    print a.frequency[69] 
    print a.pwr.shape
    print a.flux_axis.shape                 
    pl1=colormesh(a.flux_axis, a.pwr-30-60, absolute(a.MagcomFilt[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)", pl="TA53_pwr")
    #a.save_plots([pl1])
    #pl1.show()
    pl2=scatter(a.pwr, absolute(absolute(a.MagcomFilt[69, 635, :])-absolute(a.MagcomFilt[69,0, :])), xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$")#.show()

    onres=20*log10(absolute(a.MagcomFilt[69, 635, :]))-bg_A4(a.frequency[69])
    offres=20*log10(absolute(a.MagcomFilt[69, 0, :]))-bg_A4(a.frequency[69])
    scatter(a.pwr-30-60, absolute(onres-offres))
    #scatter(b.pwr-30-60, 10**(absolute(onres-offres)/20.0))
    scatter(a.pwr-30-60, absolute(10**(onres/20.0)-10**(offres/20.0)))
    #scatter(b.pwr-30-60, absolute(10**(onres/20.0)))

    if 1:
        pl=colormesh(qdt.phi_arr, qdt.pwr_arr-qdt.atten, absolute(qdt.fexpt2), cmap="RdBu_r")
        lp=line(qdt.pwr_arr-qdt.atten, 0.12*absolute(qdt.fexpt2[:, 30]))
        lp=line(qdt.pwr_arr-qdt.atten, 0.12*absolute(qdt.fexpt2[:, 30+1]), pl=lp)
        lp=line(qdt.pwr_arr-qdt.atten, 0.12*absolute(qdt.fexpt2[:, 30-1]), pl=lp)

        pl=colormesh(qdt.phi_arr, qdt.pwr_arr-qdt.atten, 1-absolute(qdt.fexpt2), cmap="RdBu_r")

        pl=colormesh(qdt.phi_arr, qdt.pwr_arr, 10*log10(absolute(qdt.fexpt2)), cmap="RdBu_r")#.show()
    
    pl_pwr_sat=scatter(a.pwr-30-60-20, absolute(10**(onres/20.0)-10**(offres/20.0)),
                xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$", pl=lp,
                  auto_ylim=False, y_min=0.0, y_max=0.12, marker_size=3.0,
                  auto_xlim=False, x_min=-30-90, x_max=10-90).show()

    pls=[pl_raw, pl_ifft, pl_fft, pl1, pl2, pl3]
    nps=TA53_Save_NP(file_path=r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/test_data/Lamb_shift/extract_data/TA53_pwr_sat.txt")
    print pl_pwr_sat.savedata()
    #nps.save(pl_pwr_sat.savedata())
    npr=TA53_Read_NP(file_path=nps.file_path, show_data_str=True)
    data=npr.read()
    scatter(data[:, 0], data[:, 1])
    #nps.data_buffer=pl1.savedata()
    #a.save_plots(pls)
    pls[0].show()
