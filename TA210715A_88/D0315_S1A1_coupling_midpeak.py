# -*- coding: utf-8 -*-
"""
Created on Sun May  8 13:25:50 2016

@author: thomasaref
"""
from TA88_fundamental import TA88_Lyzer, TA88_Read
from taref.physics.fitting_functions import refl_lorentzian
from numpy import absolute, fft
from taref.plotter.api import Plotter, line

s4a1_mp=TA88_Lyzer(name="S1A1_midpeak", filt_center=37, filt_halfwidth=7,
                   on_res_ind=260,
              VNA_name='RS VNA', port_name='S21',
              rd_hdf=TA88_Read(main_file="Data_0315/S1A1_TA88_coupling_search_midpeak.hdf5"),
              indices=range(65, 984+1),
              fit_func=refl_lorentzian)

s4a1_mp.read_data()
s4a1_mp.magabs_colormesh()#"colormesh S4A1")
s4a1_mp.magabsfilt_colormesh()#"filtcolormesh S4A1")
s4a1_mp.filt_compare(s4a1_mp.on_res_ind )
s4a1_mp.filt_compare(s4a1_mp.start_ind )

s4a1_mp.magdBfilt_colormesh()
s4a1_mp.magdBfiltbgsub_colormesh()
#s4a1_mp.filt_compare("filt_compare_on_res", s4a1_mp.on_res_ind)
s4a1_mp.hann_ifft_plot()
s4a1_mp.ifft_plot().show()#"ifft_S4A1")
def ifft_plot(self):
    pl=Plotter(fig_width=6, fig_height=4)

    line("ifft_{}".format(self.name), absolute(fft.ifft(self.Magcom[:,self.on_res_ind])), label="On resonance")
    line("ifft_{}".format(self.name), absolute(fft.ifft(self.Magcom[:,0])), label="Off resonance", color="red")
    pl.legend()
    pl.set_xlim(0, 100)
    pl.xlabel="Time (#)"
    pl.ylabel="Absolute Magnitude"
    return pl
#ifft_plot(s4a1_mp).show()
        #d.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "trans_ifft.pdf")
        #d.show()