# -*- coding: utf-8 -*-
"""
Created on Sun May  8 13:25:50 2016

@author: thomasaref
"""
from TA88_fundamental import TA88_VNA_Lyzer, TA88_Read, qdt
from numpy import absolute, fft
from taref.plotter.api import Plotter, line, scatter

a=TA88_VNA_Lyzer(name="S4A1_wide",
             desc="S4A1 Main peak",
                   on_res_ind=260,
              VNA_name='RS VNA', port_name='S21',
              rd_hdf=TA88_Read(main_file="Data_0313/S4A1_TA88_coupling_search_midpeak.hdf5"),
              #fit_indices=[range(65, 984+1)],
              #fit_func=lorentzian,
              flux_factor=qdt.flux_factor*1000.0/560.0,
              offset=-0.045
              )#, fit_type="yoko")
a.filt.center=31
a.filt.halfwidth=22
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.055 #0.01
a.flux_axis_type="fq" #"flux"
a.end_skip=10

a.save_folder.main_dir=a.name
#a.read_data()

def S4A1_midpeak_plots():
    a.read_data()
    a.filter_type="None"
    pl1=a.magabs_colormesh(fig_width=6.0, fig_height=4.0)
    pl1.add_label("a)")
    a.filter_type="FFT"
    pl2=a.ifft_plot(fig_width=6.0, fig_height=4.0, time_axis_type="time",
                auto_xlim=False, x_min=-0.05, x_max=1.0, show_legend=True)#, auto_ylim=False, y_min=-0.0001, y_max=0.008)
    pl2.add_label("b)")
    dif=pl2.y_max*0.1
    pl2.y_min=-dif
    pl2.y_max+=dif

    pl3, pf3=a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pf_too=True)
                           #auto_zlim=False, vmin=0.0, vmax=0.02)
    pl3.add_label("c)")

    a.filter_type="Fit"
    pl4=a.magabs_colormesh(fig_width=6.0, fig_height=4.0,
                           auto_zlim=False, vmin=pf3.vmin, vmax=pf3.vmax, auto_ylim=False, y_min=pl3.y_min, y_max=pl3.y_max)
    pl4.add_label("d)")

    pl_list=[pl1, pl2, pl3, pl4]
    return pl_list

if __name__=="__main__":
    #pls=S4A1_midpeak_plots()
    pls=a.fft_plots()

    #a.save_plots(pls)
    pls[0].show()

    pl=a.magabs_colormesh()
    a.filter_type="FFT"
    a.ifft_plot()
    pl=a.magabs_colormesh()
    a.filter_type="Fit"
    a.magabs_colormesh()
    #line(a.frequency, a.ls_f)[0].show()
    a.widths_plot()
    a.center_plot()
    a.heights_plot()
    a.background_plot().show()

    s4a1_mp.magabs_colormesh()#"colormesh S4A1")
    s4a1_mp.magabsfilt_colormesh()#"filtcolormesh S4A1")
    s4a1_mp.magabsfilt2_colormesh()#"filtcolormesh S4A1")

    s4a1_mp.filt_compare(s4a1_mp.start_ind )
    #s4a1_mp.filt_compare(s4a1_mp.on_res_ind )
    #s4a1_mp.magdBfilt_colormesh()
    #s4a1_mp.magdBfiltbgsub_colormesh()
    #s4a1_mp.filt_compare("filt_compare_on_res", s4a1_mp.on_res_ind)
    s4a1_mp.hann_ifft_plot()
    s4a1_mp.ifft_plot()#.show()#"ifft_S4A1")
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
        pl, pf=scatter(self.frequency[self.indices], absolute(fit_params[1, :]), color="red", label=self.name, plot_name="widths_{}".format(self.name))

        line(self.frequency, self.qdt._get_coupling(self.frequency)+0*1.8e6, plotter=pl)
        return pl

    plot_widths(s4a1_mp) .show()
    #ifft_plot(s4a1_mp).show()
            #d.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "trans_ifft.pdf")
            #d.show()