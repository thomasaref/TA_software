# -*- coding: utf-8 -*-
"""
Created on Tue May 17 20:49:11 2016

@author: thomasaref
"""


from TA88_fundamental import TA88_VNA_Lyzer, TA88_Read


a=TA88_VNA_Lyzer( name="d0502", on_res_ind=176, VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0502/S1A4_midpeak_trans.hdf5"),
            desc="S1A4 low frequency side lobe 1",
            offset=-0.08,
            #fit_indices=[range(111, 570)],
                         ) #33, 70
a.filt.center=22
a.filt.halfwidth=10
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.01
a.flux_axis_type="fq" #"flux"
a.end_skip=10
a.save_folder.main_dir=a.name

if __name__=="__main__":
    pls=a.fft_plots()
    #a.save_plots(pls)
    a.widths_plot()
    a.center_plot()
    a.heights_plot()
    a.background_plot().show()


if __name__=="__main__":
    a.filter_type="FFT"
    pl=a.magabs_colormesh()
    a.filter_type="Fit"
    a.magabs_colormesh(pl=pl)
    a.ifft_plot()

    #line(a.frequency, a.ls_f)[0].show()
    a.widths_plot()
    a.center_plot()
    a.heights_plot()
    a.background_plot().show()
    #pl=a.magabs_colormesh()#magabs_colormesh3(s3a4_wg)
    pl=a.hann_ifft_plot()
    #pl=a.ifft_plot()
    #a.filt_compare(a.on_res_ind)
    #filt=filt_prep(601, s3a4_wg.filt_start_ind, s3a4_wg.filt_end_ind)
    #line(filt*0.001, plotter=pl)
    #colormesh(s3a4_wg.MagAbsFilt)#, plotter="magabsfilt_{}".format(self.name))

    a.magabsfilt_colormesh().show()
