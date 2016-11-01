# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Two_Tone_Lyzer, TA53_Read, qdt
from numpy import absolute,  trunc, arccos, shape, float64, linspace, reshape
from taref.plotter.api import colormesh, scatter, line

a=TA53_VNA_Two_Tone_Lyzer(name="d1013", on_res_ind=30,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1029/S1A4_all_close_two_tone.hdf5"),
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="Gate to IDT low frequency",
         offset=-0.3,
         #swp_type="yoko_first",
        )
a.filt.center=57 #139 #106 #  #137
a.filt.halfwidth=20
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.1 #0.035
a.flux_axis_type="yoko" #"flux" #"fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"

a.end_skip=10
#a.flux_indices=[range(479, 712)] #range(0,41), range(43, 479), range(482, len(a.yoko))]
#a.bgsub_type="dB" #"Abs"

a.save_folder.main_dir=a.name

a.read_data()
#a.pwr_ind=39
print a.yoko.shape
a.filter_type="None"
a.magabs_colormesh(fig_width=6.0, fig_height=4.0)#.show()
#scatter(absolute(a.MagcomFilt[170, 192, :]))
#scatter(absolute(a.MagcomFilt[170, :, 3]))
a.ifft_plot(fig_width=6.0, fig_height=4.0)#.show() #, time_axis_type="time",
a.filter_type="FFT"
colormesh(absolute(a.MagcomFilt[750, :, :]))#.show()
colormesh(absolute(a.MagcomFilt[:, :, 50]))#.show()

from taref.core.api import process_kwargs
from taref.physics.filtering import Filter
from numpy import amax, array
filt=Filter(center=-13, halfwidth=5)


def ifft_plot(self, **kwargs):
    process_kwargs(self, kwargs, pl="hannifft_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
    on_res=absolute(filt.window_ifft(self.MagcomFilt[200,30, :]))
    #strt=absolute(self.filt.window_ifft(self.Magcom[:,self.start_ind]))
    #stop=absolute(self.filt.window_ifft(self.Magcom[:,self.stop_ind]))

    pl=line(filt.fftshift(on_res),  color="red",
           plot_name="onres_{}".format(self.on_res_ind),label="{:.4g}".format(self.flux_axis[self.on_res_ind]), **kwargs)
    #line(self.time_axis, self.filt.fftshift(strt), pl=pl, linewidth=1.0, color="purple",
    #     plot_name="strt {}".format(self.start_ind), label="{:.4g}".format(self.flux_axis[self.start_ind]))
    #line(self.time_axis, self.filt.fftshift(stop), pl=pl, linewidth=1.0, color="blue",
    #     plot_name="stop {}".format(self.stop_ind), label="{:.4g}".format(self.flux_axis[self.stop_ind]))

    filt.N=len(on_res)
    filt_frq=filt.freqz
    #filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
    top=amax(on_res)#, amax(strt), amax(stop)])
    line(filt_frq*top, plotter=pl, color="green", label="wdw")
    pl.xlabel=kwargs.pop("xlabel", self.time_axis_label)
    pl.ylabel=kwargs.pop("ylabel", "Mag abs")
    double_filt= array([[filt.fft_filter(a.MagcomFilt[m,n, :]) for n in a.flat_flux_indices] for m in a.flat_indices])#.transpose()
    print double_filt.shape
    colormesh(absolute(double_filt[750, :, :]))
    colormesh(absolute(double_filt[500, :, :]))
    colormesh(absolute(double_filt[250, :, :]))

    colormesh(absolute(double_filt[:, :, 75]))
    colormesh(absolute(double_filt[:, :, 50]))
    colormesh(absolute(double_filt[:, :, 25]))

    return pl
ifft_plot(a).show()


colormesh(absolute(a.MagcomFilt[250, :, :])).show()
colormesh(absolute(a.MagcomFilt[293, :, :, 0]))#.show()
colormesh(absolute(a.MagcomFilt[370, :, :, 0]))#.show()

colormesh(absolute(a.MagcomFilt[293, :, :, 3]))#.show()
colormesh(absolute(a.MagcomFilt[370, :, :, 3]))#.show()

colormesh(absolute(a.MagcomFilt[293, :, 30, :]))#.show()

colormesh(absolute(a.MagcomFilt[55, :, :, 0]))#.show()
colormesh(absolute(a.MagcomFilt[55, :, :, 1]))#.show()
colormesh(absolute(a.MagcomFilt[55, :, :, 2]))#.show()
colormesh(absolute(a.MagcomFilt[55, :, :, 3]))#.show()

colormesh(absolute(a.MagcomFilt[:, 30, :, 0]))#.show()
colormesh(absolute(a.MagcomFilt[:, 30, :, 1]))#.show()
colormesh(absolute(a.MagcomFilt[:, 30, :, 2]))#.show()
colormesh(absolute(a.MagcomFilt[:, 30, :, 3]))#.show()


a.filter_type="FFT"

#a.pwr_ind=10
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind])).show()
#a.pwr_ind=9
#a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
#a.pwr_ind=8
#a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
offset=0
a.pwr_ind=15+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=14+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=13+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=12+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=11+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=10+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=9+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
a.pwr_ind=8+offset
a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind])).show()

#a.filter_type="Fit"
#pl, pf=a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pf_too=True)
                               #auto_zlim=False, vmin=0.0, vmax=0.02)
#a.widths_plot()
#a.center_plot()#.show()
#a.filter_type="FFT"
a.magabs_colormesh(fig_width=6.0, fig_height=4.0).show()

if __name__=="__main2__":
    pls=a.fft_plots()
    #a.save_plots(pls)
    pls[0].show()
