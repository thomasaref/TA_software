# -*- coding: utf-8 -*-
"""
Created on Tue May 17 20:49:11 2016

@author: thomasaref
"""


from TA88_fundamental import TA88_Lyzer, TA88_Read
from taref.physics.fitting_functions import lorentzian

a=TA88_Lyzer(filt_center=27, filt_halfwidth=6, on_res_ind=360, VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0519/S1A4_high_frq_trans_3_sidelobe.hdf5"),
            fit_func=lorentzian,# p_guess=[5e6,4.32e9, 3e-7, 3e-6], #[0.2,2.3, 3e-7, 7.5e-7],
            offset=-0.03) #33, 70
a.read_data()


if __name__=="__main__":
    a.magabs_colormesh()
    pl=a.magabsfilt_colormesh()
    #line(a.frequency, a.ls_f)[0].show()
    pl=a.hann_ifft_plot()

    a.widths_plot()
    a.center_plot()
    a.heights_plot()
    a.background_plot().show()
    #pl=a.magabs_colormesh()#magabs_colormesh3(s3a4_wg)
    #pl=a.ifft_plot()
    #a.filt_compare(a.on_res_ind)
    #filt=filt_prep(601, s3a4_wg.filt_start_ind, s3a4_wg.filt_end_ind)
    #line(filt*0.001, plotter=pl)
    #colormesh(s3a4_wg.MagAbsFilt)#, plotter="magabsfilt_{}".format(self.name))

    a.magabsfilt_colormesh().show()
