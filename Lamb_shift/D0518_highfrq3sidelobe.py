# -*- coding: utf-8 -*-
"""
Created on Tue May 17 20:49:11 2016

@author: thomasaref
"""


from TA88_fundamental import TA88_Lyzer, TA88_Read


a=TA88_Lyzer( name="d0518", on_res_ind=374, VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0519/S1A4_high_frq_trans_3_sidelobe.hdf5"),
            desc="S1A4 high frequency side lobe 3",
            offset=-0.04,
            fit_indices=[range(80,499)]) #33, 70
a.filt.center=27
a.filt.halfwidth=6
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.1
a.flux_axis_type="fq" #"flux"
a.end_skip=20
a.save_folder.main_dir=a.name

if __name__=="__main__":
    pls=a.fft_plots()
    a.save_plots(pls)
    a.widths_plot()
    a.center_plot()
    a.heights_plot()
    a.background_plot().show()


