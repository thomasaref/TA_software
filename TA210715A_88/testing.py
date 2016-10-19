# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Lyzer, TA88_Read#, qdt
from taref.plotter.api import colormesh, line, Plotter, scatter
from taref.core.api import set_tag, set_all_tags
from numpy import array, squeeze, append, sqrt, pi, mod, floor_divide, trunc, arccos, shape, linspace, interp, absolute, fft, log10, angle, unwrap
from atom.api import FloatRange
from taref.plotter.api import LineFitter
from taref.physics.fundamentals import h#, filt_prep
from time import time

a=TA88_Lyzer(name="testing", on_res_ind=182, VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0221/S4A4_TA88_swp.hdf5"),
              desc="looking",
              #offset=-0.09,
            #fit_indices=[range(19, 259+1),range(300, 566+1)],
            ) #33, 70
a.filt.center=110
a.filt.halfwidth=30
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.05 #0.01
a.flux_axis_type="fq" #"flux"
a.end_skip=10
a.save_folder.main_dir=a.name

if __name__=="__main__":

    #pls=a.fft_plots()
    #a.save_plots(pls)
    #pls[0].show()
    #pl=a.magabs_colormesh()#magabs_colormesh3(s3a4_wg)
    #pl=a.hann_ifft_plot()
    #pl=a.ifft_plot()
    #a.filt_compare(a.on_res_ind)
    #filt=filt_prep(601, s3a4_wg.filt_start_ind, s3a4_wg.filt_end_ind)
    #line(filt*0.001, plotter=pl)
    #, plotter="magabsfilt_{}".format(self.name))
    a.read_data()
    colormesh(a.MagAbs)
    pl=a.magabs_colormesh()
    #pl.savefig(dir_path=a.save_folder.dir_path, fig_name=pl.name)
    a.filter_type="FFT"
    a.ifft_plot()#.show() #auto_xlim=False, x_min=0.0, x_max=1.0, time_axis_type="time", show_legend=True, auto_ylim=False, y_min=-0.0001, y_max=0.0012).show()
    pl=a.magabs_colormesh().show() #auto_zlim=False, vmin=0.0, vmax=0.0009)
    #a.filter_type="Fit"
    #a.magabs_colormesh(auto_zlim=False, vmin=0.0, vmax=0.0009)

    #a.widths_plot()
    #a.center_plot().show()
