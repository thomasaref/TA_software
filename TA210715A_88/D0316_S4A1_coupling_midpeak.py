# -*- coding: utf-8 -*-
"""
Created on Sun May  8 13:25:50 2016

@author: thomasaref
"""
from TA88_fundamental import TA88_Lyzer, TA88_Read, qdt
from taref.physics.fitting_functions import lorentzian
from numpy import absolute, fft
from taref.plotter.api import Plotter, line, scatter





s4a1_mp=TA88_Lyzer(name="S4A1_midpeak", filt_center=31, filt_halfwidth=22,
                   on_res_ind=260,
              VNA_name='RS VNA', port_name='S21',
              rd_hdf=TA88_Read(main_file="Data_0316/S4A1_TA88_coupling_search_midpeak.hdf5"),
              #indices=range(65, 984+1),
              fit_func=lorentzian,
              flux_factor=qdt.flux_factor*1000.0/560.0,
              offset=0.0)
s4a1_mp.read_data()
s4a1_mp.magabs_colormesh()#"colormesh S4A1")
s4a1_mp.magabsfilt_colormesh()#"filtcolormesh S4A1")
s4a1_mp.magabsfilt2_colormesh()#"filtcolormesh S4A1")

s4a1_mp.filt_compare(s4a1_mp.start_ind )
#s4a1_mp.filt_compare(s4a1_mp.on_res_ind )
#s4a1_mp.magdBfilt_colormesh()
#s4a1_mp.magdBfiltbgsub_colormesh()
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
def plot_widths(self, plotter=None):
    print "first fit"
    #tstart=time()
    #fq_vec=array([sqrt(f*(f-2*self.qdt._get_Lamb_shift(f=f))) for f in self.frequency])

    #fit_p=self.fano_fit(263, fq_vec)
    #print self.p_guess, fit_p

    #fit=lorentzian(fq_vec, fit_p[1:])
    #pl, pf=line(fq_vec, self.MagAbsFilt_sq[263, :])
    #line(fq_vec, fit, plotter=pl, color="red")
    #pl.show()
    print self.ls_f.shape, self.yoko.shape

    fit_params=self.full_fano_fit(self.fq)
    print (fit_params[1, :]).shape
    pl, pf=scatter(self.ls_f[self.indices], absolute(fit_params[1, :]), color="red", label=self.name, plot_name="widths_{}".format(self.name))

    line(self.ls_f, self.qdt._get_coupling(self.frequency)+0*1.8e6, plotter=pl)
    return pl

plot_widths(s4a1_mp) .show()
#ifft_plot(s4a1_mp).show()
        #d.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "trans_ifft.pdf")
        #d.show()