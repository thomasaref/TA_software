# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, qdt
from numpy import (absolute,  trunc, arccos, shape, float64, linspace, reshape,
                   squeeze, argmax, array, log10, swapaxes, amax, angle, sqrt)
from taref.plotter.api import colormesh, scatter, line
from h5py import File
from taref.core.api import process_kwargs
from taref.physics.filtering import Filter
from taref.physics.fundamentals import h
from time import time


a=TA53_VNA_Pwr_Lyzer(name="d1129", on_res_ind=54,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1129/S4A1S1_pwr_flux.hdf5"), #long_test.hdf5"), #
        #fit_indices=[range(850, 2300)], #range(48,154+1), range(276, 578+1)],
         desc="transmission power sweep",
         offset=-0.1,
        # read_data=read_data,
         swp_type="yoko_first",
        )
a.filt.center=31 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
a.filt.halfwidth=10 #8 #10
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.3 #0.035
a.flux_axis_type="yoko" #"fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"
a.end_skip=10
#a.flux_indices=[range(len(a.yoko)-1)]

a.save_folder.main_dir=a.name

a.read_data()
a.pwr_ind=-1
if __name__=="__main__":
    a.filter_type="None"
    pl_raw=a.magabs_colormesh()
    a.phase_colormesh()

    a.bgsub_type="dB"
    a.magabs_colormesh()
    #pl1=colormesh(absolute(a.MagcomData[:, :, 30]))

    pl_ifft=a.ifft_plot()#.show()
    #a.pwr_ind=22

    a.filter_type="FFT"
    pl_fft=a.magabs_colormesh()#.show()
    a.magdB_colormesh()
    a.phase_colormesh()

    a.bgsub_type="None"
    pl1=a.magdB_colormesh()
    a.phase_colormesh()
    pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip],
                  absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 54, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()
    pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip],
                  absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 74, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()
    pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip],
                  absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 45, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[119, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[109, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[99, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[431, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[441, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[421, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()

        #a.pwr_ind=i
    pls=[a.magabs_colormesh(pl=str(int(a.pwr[a.pwr_ind]))) for a.pwr_ind in range(len(a.pwr))]
    #a.save_plots(pls)

    pts=array([[28, 3.788, 2.643, 2.680],
    [113, 3.873,  2.634,  2.681],
    [186,  3.946, 2.627, 2.666],
    [263, 4.022, 2.644, 2.553],
    [347, 4.107, 2.645, 2.542],
    [426, 4.186, 2.657, 2.528],
    [507, 4.267,  2.659, 2.522]])
    print pts.shape

    def fq(self, volts):
        flux_d_flux0=self.qdt._get_flux_over_flux0(voltage=volts,
                   offset=self.offset, flux_factor=self.flux_factor)
        Ej=self.qdt._get_Ej(Ejmax=self.qdt.Ejmax, flux_over_flux0=flux_d_flux0)
        return self.qdt._get_fq(Ej=Ej, Ec=self.qdt.Ec)



    def ls_f(self, freqs):
        return array([sqrt(f*(f-2*self.qdt._get_Lamb_shift(f=f))) for f in freqs])
    pl=scatter(pts[:, 1], fq(a, pts[:, 2])/1e9)
    scatter(pts[:, 1], fq(a, pts[:, 3])/1e9, pl=pl, color="red")
    line(a.frequency/1e9, a.ls_f/1e9, pl=pl)

    ff=ls_f(a, a.frequency-1.3*a.qdt.Ec/h)+1.3*a.qdt.Ec/h

    line(a.frequency/1e9, ls_f(a, a.frequency)/1e9, pl=pl)

    line(a.frequency/1e9, ff/1e9, pl=pl, color="black")

    def ls_f2(self, volts):
        flux_d_flux0=self.qdt._get_flux_over_flux0(voltage=volts,
                   offset=self.offset, flux_factor=self.flux_factor)
        Ej=self.qdt._get_Ej(Ejmax=self.qdt.Ejmax, flux_over_flux0=flux_d_flux0)

        E0p, E1p, E2p=a.qdt._get_lamb_shifted_transmon_energy_levels(Ej=Ej, n_energy=3)

        #anharmp=(E2p-E1p)-(E1p-E0p)

        #fq= (E1-E0)/h#qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
        ls_fq=(E1p-E0p)/h #qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        #fq2=(E2-E1)/h
        ls_fq2=(E2p-E1p)/h #qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
        return ls_fq, ls_fq2

    lsf1, lsf2=ls_f2(a, a.yoko)
    print lsf1.shape
    line(lsf1/1e9, a.fq/1e9, color="green", pl=pl)
    line(lsf2/1e9, a.fq/1e9, color="purple", pl=pl)

    pl.show()
    a.filter_type="Fit"
    a.magabs_colormesh(pl=pl2)
    a.magdB_colormesh(pl=pl1)
    cp=a.center_plot()
    wp=a.widths_plot().show()
    a.pwr_ind=1
    a.filter_type="FFT"
    pl_fft=a.magabs_colormesh()#.show()
    a.bgsub_type="None"
    pl1=a.magdB_colormesh()
    pl2=a.magabs_colormesh()
    a.filter_type="Fit"
    a.magabs_colormesh(pl=pl2)
    a.magdB_colormesh(pl=pl1)
    a.center_plot(pl=cp, color="red")
    a.widths_plot(pl=wp, color="red").show()


    #pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomData[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()
    pl3=colormesh(a.pwr, a.freq_axis[a.end_skip:-a.end_skip], absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 335, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    pl1=colormesh(a.yoko, a.pwr, absolute(a.MagcomFilt[69, :, :]).transpose(), ylabel="Power (dBm)", xlabel=r"Yoko (V)")#.show()

    pl2=scatter(a.pwr, absolute(absolute(a.MagcomFilt[69, 335, :])-absolute(a.MagcomFilt[69,0, :])), xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$")#.show()

    pls=[pl_raw, pl_ifft, pl_fft, pl1, pl2, pl3]
    #a.save_plots(pls)
    pls[0].show()
