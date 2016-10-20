# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_VNA_Lyzer, TA88_Read, TA88_VNA_Pwr_Lyzer
from taref.plotter.api import colormesh, line, scatter
from numpy import absolute

a=TA88_VNA_Lyzer(name="testing", on_res_ind=58, VNA_name="RS VNA", #241
              rd_hdf=TA88_Read(main_file="Data_0307/S1A4_TA88_wide_f_flux_swp2.hdf5"), #S1A4_TA88_coupling_search.hdf5"),
              desc="looking",
              #offset=-0.09,
            #fit_indices=[range(19, 259+1),range(300, 566+1)],
            ) #33, 70

a.filt.center=150 #125
a.filt.halfwidth=30
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.05 #0.01
a.flux_axis_type="fq" #"flux"
a.end_skip=10
a.save_folder.main_dir=a.name
a.bgsub_type="dB"

if 0:
    b=TA88_VNA_Pwr_Lyzer(name="testing", on_res_ind=231, VNA_name="RS VNA",
                  rd_hdf=TA88_Read(main_file="Data_0222/S4A1_TA88_powswp.hdf5"),
                  desc="looking", swp_type="yoko_first",
                )

    b.filt.center=18
    b.filt.halfwidth=10
    b.fitter.fit_type="lorentzian"
    b.fitter.gamma=0.05 #0.01
    b.flux_axis_type="fq" #"flux"
    b.end_skip=10
    b.save_folder.main_dir=b.name

if __name__=="__main__":
    if 0:
        b.read_data()
        scatter(absolute(b.MagcomFilt[50, 370, :]))
        colormesh(absolute(b.MagcomFilt[50, :, :]))#.show()

        b.magabs_colormesh()
        b.ifft_plot()

        b.filter_type="FFT"
        #b.ifft_plot()
        b.pwr_ind=0
        b.magabs_colormesh()
        b.pwr_ind=3
        b.magabs_colormesh()
        b.pwr_ind=6
        b.magabs_colormesh()
        b.pwr_ind=9
        b.magabs_colormesh().show()

    a.read_data()
    colormesh(a.MagAbs)
    pl=a.magabs_colormesh()#.show()
    #pl.savefig(dir_path=a.save_folder.dir_path, fig_name=pl.name)
    a.ifft_plot()#.show() #auto_xlim=False, x_min=0.0, x_max=1.0, time_axis_type="time", show_legend=True, auto_ylim=False, y_min=-0.0001, y_max=0.0012).show()
    a.filter_type="FFT"

    pl=a.magabs_colormesh().show() #auto_zlim=False, vmin=0.0, vmax=0.0009)
    #a.filter_type="Fit"
    #a.magabs_colormesh(auto_zlim=False, vmin=0.0, vmax=0.0009)

    #a.widths_plot()
    #a.center_plot().show()
