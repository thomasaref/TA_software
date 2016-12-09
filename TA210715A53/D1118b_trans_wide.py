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


a=TA53_VNA_Pwr_Lyzer(name="d1118", on_res_ind=301,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1118/S3A4_trans_swp_n5n15dBm.hdf5"), #long_test.hdf5"), #
        fit_indices=[ #range(7, 42), range(79, 120), range(171, 209), range(238, 296),
                     range(316, 358),range(391, 518), range(558, 603),
                    # range(629, 681), range(715, 771), range(790, 845),
                    # range(872, 921), range(953, 960), range(963, 985)
                     ],
         desc="transmission power sweep",
         offset=-0.1,
        # read_data=read_data,
         swp_type="yoko_first",
        )
a.filt.center=0 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
a.filt.halfwidth=100 #8 #10
#a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.3 #0.035
a.flux_axis_type="fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"
a.end_skip=20
#a.flux_indices=[range(len(a.yoko)-1)]
a.show_quick_fit=True
a.save_folder.main_dir=a.name

a.pwr_ind=1
if __name__=="__main__":
    a.read_data()

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
    pl_centers=a.center_plot(auto_xlim=False, x_min=3.9, x_max=5.1, auto_ylim=False, y_min=3.9, y_max=5.1,
                             xlabel="Frequency (GHz)", ylabel="Qubit Frequency (GHz)")
    line(array([3.5, 5.5]), array([3.5, 5.5]), pl=pl_centers, color="green")
    pl_widths=a.widths_plot(auto_xlim=False, x_min=3.9, x_max=5.1, auto_ylim=False, y_min=0.1, y_max=0.6,
                            xlabel="Frequency (GHz)", ylabel="$\Gamma/2\pi$ (GHz)")#.show()

    def widths_plot(self, **kwargs):
        process_kwargs(self, kwargs, pl="widths2_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
        pl=scatter(array(self.flat_indices), absolute([fp[0] for fp in self.fit_params]), **kwargs)
        return pl

    def center_plot(self, **kwargs):
        process_kwargs(self, kwargs, pl="center2_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
        pl=scatter(array(self.flat_indices), array([fp[1] for fp in self.fit_params]), **kwargs)
        return pl
    plw=widths_plot(a)
    plc=center_plot(a)
    a.pwr_ind=0
    a.fit_indices=[ range(7, 42), range(79, 120), range(171, 209), range(238, 291), #range(558, 603),
                   range(629, 681),
                   range(715, 764), range(803, 835),
                     range(879, 915), range(953, 960), range(963, 985)]

    a.get_member("fit_params").reset(a)
    a.get_member("MagcomFilt").reset(a)
    a.fitter.fit_params=None
    widths_plot(a, pl=plw, color="blue")
    center_plot(a, pl=plc, color="blue")

    pl_centers=a.center_plot(auto_xlim=False, x_min=3.9, x_max=5.1, auto_ylim=False, y_min=3.9, y_max=5.1,
                             xlabel="Frequency (GHz)", ylabel="Qubit Frequency (GHz)", pl=pl_centers)
    line(array([3.5, 5.5]), array([3.5, 5.5]), pl=pl_centers, color="green")
    pl_widths=a.widths_plot(auto_xlim=False, x_min=3.9, x_max=5.1, auto_ylim=False, y_min=0.1, y_max=0.6,
                            xlabel="Frequency (GHz)", ylabel="$\Gamma/2\pi$ (GHz)", pl=pl_widths)#.show()

    plc.show()
    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomData[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    #pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip], absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 335, :]),
    #              ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()

    #pl2=scatter(a.pwr, absolute(absolute(a.MagcomFilt[69, 335, :])-absolute(a.MagcomFilt[69,0, :])), xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$")#.show()

    #pls=[pl_raw, pl_ifft, pl_fft, pl1, pl2, pl3]
    pls=[pl_centers, pl_widths]
    #a.save_plots(pls)
    pls[-1].show()
