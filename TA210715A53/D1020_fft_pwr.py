# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, qdt
from numpy import absolute,  trunc, arccos, shape, float64, linspace, reshape
from taref.plotter.api import colormesh, scatter, line

a=TA53_VNA_Pwr_Lyzer(name="d1013", on_res_ind=139,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1020/S1A4_one_side_pwr_flux_swp2.hdf5"),
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="Gate to IDT low frequency",
         offset=-0.3,
         swp_type="yoko_first",
        )
a.filt.center=53 #145 #0*105 #53 #139 #106 #  #137
a.filt.halfwidth=20
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.1 #0.035
a.flux_axis_type="yoko" #"flux" #"fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"

a.end_skip=10
#a.flux_indices=[range(479, 712)] #range(0,41), range(43, 479), range(482, len(a.yoko))]
#a.bgsub_type="dB" #"Abs"

a.save_folder.main_dir=a.name

a.read_data()
a.pwr_ind=39
print a.yoko.shape
a.filter_type="None"
a.magabs_colormesh(fig_width=6.0, fig_height=4.0)#.show()

probe_ind=271 #448 #343 #100 #187
pl1=scatter(a.pwr, absolute(a.MagcomFilt[probe_ind, 192, :])) #535
scatter(a.yoko, absolute(a.MagcomFilt[probe_ind, :, 7]))

pl2=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[probe_ind, :, :]).transpose(), cmap="nipy_spectral")#.show()
a.ifft_plot(fig_width=6.0, fig_height=4.0)#.show() #, time_axis_type="time",

a.filter_type="FFT"

#a.pwr_ind=10
#a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
#a.pwr_ind=9
#a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
#a.pwr_ind=8
#a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=21
pl3=a.magabs_colormesh(pl="dB"+str(a.pwr[a.pwr_ind])+"dB.jpg", cmap="nipy_spectral")

offset=0
a.pwr_ind=15+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=14+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=13+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=12+offset
pl4=a.magabs_colormesh(pl="dB"+str(a.pwr[a.pwr_ind])+"dB.jpg", cmap="nipy_spectral")
a.pwr_ind=11+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=10+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=9+offset
pl5=a.magabs_colormesh(pl="dB"+str(a.pwr[a.pwr_ind])+"dB.jpg", cmap="nipy_spectral")
a.pwr_ind=8+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind])).show()

#a.filter_type="Fit"
#pl, pf=a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pf_too=True)
                               #auto_zlim=False, vmin=0.0, vmax=0.02)
#a.widths_plot()
#a.center_plot()#.show()
#a.filter_type="FFT"
#a.magabs_colormesh(fig_width=6.0, fig_height=4.0).show()

if __name__=="__main__":
    #pls=a.fft_plots()
    pls=[pl1, pl2, pl3, pl4, pl5]
    #a.save_plots(pls)
    pls[0].show()
