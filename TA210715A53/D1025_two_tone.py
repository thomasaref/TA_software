# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Two_Tone_Pwr_Lyzer, TA53_Read, qdt
from numpy import absolute,  trunc, arccos, shape, float64, linspace, reshape
from taref.plotter.api import colormesh, scatter, line

a=TA53_VNA_Two_Tone_Pwr_Lyzer(name="d1013", on_res_ind=139,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1025/S1A4_one_side_two_tone3.hdf5"),
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="Gate to IDT low frequency",
         offset=-0.3,
         swp_type="yoko_first",
        )
a.filt.center=27*2 #139 #106 #  #137
a.filt.halfwidth=10
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.1 #0.035
a.flux_axis_type="yoko" #"flux" #"fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"

a.end_skip=10
#a.flux_indices=[range(479, 712)] #range(0,41), range(43, 479), range(482, len(a.yoko))]
a.bgsub_type="Complex" #"Abs" #"dB" #"Abs"

a.save_folder.main_dir=a.name

a.frq2_ind=0
a.pwr2_ind=1

a.read_data()
#a.pwr_ind=39
print a.yoko.shape
a.filter_type="None"
#a.magabs_colormesh(fig_width=6.0, fig_height=4.0)#.show()
scatter(absolute(a.MagcomFilt[170, 192, :]))
scatter(absolute(a.MagcomFilt[170, :, 0]))

colormesh(absolute(a.MagcomFilt[260, :, :]))#.show()
a.ifft_plot(fig_width=6.0, fig_height=4.0).show() #, time_axis_type="time",

a.filter_type="FFT"

a.pwr_ind=0
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))#.show()
a.pwr_ind=1
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=2
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
#offset=0
a.pwr_ind=3
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=4
print a.frq2[a.frq_ind]
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind])).show()
a.pwr_ind=13+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=12+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=11+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=10+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=9+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=8+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind])).show()

#a.filter_type="Fit"
#pl, pf=a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pf_too=True)
                               #auto_zlim=False, vmin=0.0, vmax=0.02)
#a.widths_plot()
#a.center_plot()#.show()
#a.filter_type="FFT"
a.magabs_colormesh(fig_width=6.0, fig_height=4.0).show()

if __name__=="__main2__":
    pls=a.fft_plots()
    #a.save_plots(pls)
    pls[0].show()
