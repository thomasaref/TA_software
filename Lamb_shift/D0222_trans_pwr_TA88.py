# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import qdt, TA88_VNA_Lyzer, TA88_Read, TA88_VNA_Pwr_Lyzer, bg_A1, TA88_Read_NP, TA88_Save_NP
from taref.plotter.api import colormesh, line, scatter
from numpy import absolute, log10

file_path=r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/test_data/Lamb_shift/extract_data/TA88_pwr_sat.txt"
npr=TA88_Read_NP(file_path=file_path, show_data_str=True)
data=npr.read()
pl=scatter(data[:, 0], data[:, 1])
file_path=r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/test_data/Lamb_shift/extract_data/TA53_pwr_sat.txt"
npr=TA88_Read_NP(file_path=file_path, show_data_str=True)
data=npr.read()
pl=scatter(data[:, 0], data[:, 1], pl=pl)#.show()


a=TA88_VNA_Lyzer(name="testing", on_res_ind=182, VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0222/S4A1_TA88_swp_5Vtn5V.hdf5"),
              desc="looking",
              #offset=-0.09,
            #fit_indices=[range(19, 259+1),range(300, 566+1)],
            ) #33, 70

a.filt.center=14
a.filt.halfwidth=5
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.05 #0.01
a.flux_axis_type="fq" #"flux"
a.end_skip=10
a.save_folder.main_dir=a.name

if 1:
    b=TA88_VNA_Pwr_Lyzer(name="d0222", on_res_ind=370, VNA_name="RS VNA",
                  rd_hdf=TA88_Read(main_file="Data_0222/S4A1_TA88_powswp.hdf5"),
                  desc="looking", swp_type="yoko_first",
                                flux_factor=qdt.flux_factor*1000.0/560.0,

                )
                
    b.filt.center=14
    b.filt.halfwidth=5
    b.fitter.fit_type="lorentzian"
    b.fitter.gamma=0.05 #0.01
    b.flux_axis_type="flux" #"yoko" #"fq" #"flux"
    b.end_skip=10
    b.save_folder.main_dir=b.name

if __name__=="__main__":
    if 1:
        b.read_data()
        print b.comment
        scatter(absolute(b.MagcomFilt[50, 370, :]))
        print b.frequency[50]
        colormesh(absolute(b.MagcomFilt[b.end_skip:-b.end_skip, 362, :]))#.show()
        pl1=colormesh(b.flux_axis, b.pwr-40-60, absolute(b.MagcomFilt[50, :, :]).transpose(), pl="TA88_pwr")
        #b.save_plots([pl1])
        print b.pwr
        print b.flux_axis.shape
        pl1.show()

        onres=20*log10(absolute(b.MagcomFilt[50, 362, :]))+10-bg_A1(b.frequency[50])
        offres=20*log10(absolute(b.MagcomFilt[50, 0, :]))+10-bg_A1(b.frequency[50])
        scatter(b.pwr-40-60, absolute(onres-offres))
        pl_pwr_sat=scatter(b.pwr-40-60, absolute(10**(onres/20.0)-10**(offres/20.0)))

        nps=TA88_Save_NP(file_path=r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/test_data/Lamb_shift/extract_data/TA88_pwr_sat.txt")
        nps.save(pl_pwr_sat.savedata())
        npr=TA88_Read_NP(file_path=nps.file_path, show_data_str=True)
        data=npr.read()
        scatter(data[:, 0], data[:, 1]).show()

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
