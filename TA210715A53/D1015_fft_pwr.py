# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, qdt
from numpy import absolute,  trunc, arccos, shape, float64, linspace, reshape
from taref.plotter.api import colormesh, scatter, line

a=TA53_VNA_Pwr_Lyzer(name="d1013", on_res_ind=316,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1015/S1A1_just_gate_pwr_flux_swp.hdf5"),
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="Gate to IDT low frequency",
         offset=-0.3,
         swp_type="yoko_first",
        )
a.filt.center=53 #139 #106 #  #137
a.filt.halfwidth=20
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.1 #0.035
a.flux_axis_type="flux" #"fq" #
a.bgsub_type="Abs" #"Complex" #"Abs" #"dB"

a.end_skip=10
#a.flux_indices=[range(479, 712)] #range(0,41), range(43, 479), range(482, len(a.yoko))]
#a.bgsub_type="Abs"

a.save_folder.main_dir=a.name

a.read_data()
a.pwr_ind=20
print a.yoko.shape, a.pwr.shape
a.filter_type="None"
a.magabs_colormesh(fig_width=6.0, fig_height=4.0)#.show()
#scatter(absolute(a.MagcomFilt[535, 316, :]))
#scatter(absolute(a.MagcomFilt[535, :, 7]))

colormesh(absolute(a.MagcomData[139, :, :]))#.show()
colormesh(absolute(a.MagcomData[129, :, :]))#.show()
colormesh(absolute(a.MagcomData[149, :, :]))#.show()

#a.ifft_plot(fig_width=6.0, fig_height=4.0)#.show() #, time_axis_type="time",

#a.filter_type="FFT"
#a.pwr_ind=10
#a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
#a.pwr_ind=9
#a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
#a.pwr_ind=8
#a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=15
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=6
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=5
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=4
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=3
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=2
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=1
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=0
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
