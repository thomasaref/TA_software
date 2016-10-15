# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Lyzer, TA53_Read, qdt
#from taref.plotter.api import colormesh, line
from numpy import array, absolute, real, imag, nan_to_num, squeeze, append, sqrt, pi, mod, floor_divide, trunc, arccos, shape, float64, linspace, reshape
#from taref.physics.fitting import refl_lorent
#from taref.physics.fundamentals import h
from scipy.optimize import fsolve

from taref.physics.filtering import Filter

a=TA53_VNA_Lyzer(name="d1013", on_res_ind=63, filt=Filter(center=2, halfwidth=80, reflect=False),#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1013/S1A1_just_gate_careful_flux_swp.hdf5"),
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="Gate low frequency",
        )

a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.2 #0.035
a.flux_axis_type="flux" #"fq" #
a.bgsub_type="dB"
a.end_skip=10
#a.flux_indices=[range(0,41), range(43, 479), range(482, len(a.yoko))]
#a.bgsub_type="Abs"

a.save_folder.main_dir=a.name

a.read_data()
a.filter_type="None"
a.magabs_colormesh(fig_width=6.0, fig_height=4.0)

a.filter_type="FFT"
a.ifft_plot(fig_width=6.0, fig_height=4.0) #, time_axis_type="time",

#a.filter_type="Fit"
#a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pf_too=True)
                               #auto_zlim=False, vmin=0.0, vmax=0.02)
a.filter_type="FFT"
a.magabs_colormesh(fig_width=6.0, fig_height=4.0).show()

if __name__=="__main2__":
    pls=a.fft_plots()
    #a.save_plots(pls)
    pls[0].show()
