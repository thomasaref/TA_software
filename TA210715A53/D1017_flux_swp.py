# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Lyzer, TA53_Read#, qdt
#from taref.plotter.api import colormesh, line
from numpy import array, amax, absolute, real, imag, nan_to_num, squeeze, append, sqrt, pi, mod, floor_divide, trunc, arccos, shape, float64, linspace, reshape
#from taref.physics.fitting import refl_lorent
#from taref.physics.fundamentals import h
from scipy.optimize import fsolve
from taref.core.universal import ODict
from taref.core.api import process_kwargs, get_tag, get_all_tags, tag_property
from taref.physics.filtering import Filter
from taref.physics.qdt import QDT
from taref.plotter.api import line, colormesh, Plotter
from atom.api import Typed

a=TA53_VNA_Lyzer(name="d1013", on_res_ind=644,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1017/S1A1_just_gate_0dBm_flux_swp.hdf5"),
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="Gate to IDT low frequency",
         offset=-0.3
        )
a.filt.center=53 #106 #137
a.filt.halfwidth=20
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.1 #0.035
a.flux_axis_type="yoko" #"flux" #"fq" #


a.end_skip=10
#a.flux_indices=[range(479, 712)] #range(0,41), range(43, 479), range(482, len(a.yoko))]
#a.bgsub_type="Abs"

a.save_folder.main_dir=a.name

a.read_data()
a.filter_type="None"

a.magabs_colormesh(fig_width=6.0, fig_height=4.0)
a.bgsub_type="Abs" #"Complex" #"Abs" #"dB"
pl=a.magabs_colormesh(fig_width=6.0, fig_height=4.0)

V=linspace(min(a.yoko), max(a.yoko), 101)
a.qdt.qubit_type="transmon" #scb"
line(V, a.qdt._get_flux_parabola(voltage=V, ng=0.0)/1e9, pl=pl)
line(V, a.qdt._get_flux_parabola(voltage=V, ng=0.5)/1e9, pl=pl)

print a.qdt.qubit_type

a.ifft_plot(fig_width=6.0, fig_height=4.0)#.show() #, time_axis_type="time",

class QDTFitter(QDT):
    base_name="qdt_fitter"

    plotter=Typed(Plotter).tag(private=True)
    data_dict=ODict().tag(private=True)

    def __setattr__(self, name, value):
        super(QDTFitter, self).__setattr__(name, value)
        self.update_plot()

    def _default_plotter(self):
        #if self.plot_name=="":
        #    self.plot_name=self.name
        pl=Plotter(name=self.name)
        for param in get_all_tags(self, "plot"):
            #print param
            pl, pf=line(*getattr(self, param), plot_name=get_tag(self, param, "plot"), plotter=pl, pf_too=True)
            self.data_dict[param]=pf.plot_name
        return pl

    def update_plot(self):
        for param, plot_name in self.data_dict.iteritems():
            self.get_member(param).reset(self)
            self.plotter.plot_dict[plot_name].alter_xy(*getattr(self,param))

    @tag_property(private=True, plot="flux_par")
    def data(self):
        return V, self._get_flux_parabola(voltage=V)/1e9

qdt=QDTFitter(name="fitting_qdt",
        material='LiNbYZ',
        ft="double",
        #S_type="RAM",
        a=96.0e-9, #f0=5.35e9,
        Np=5,
        Rn=2950.0, #3780.0, #(3570.0+4000.0)/2.0, Ejmax=h*44.0e9,
        W=7.0e-6,
        eta=0.5,
        flux_factor=0.53, #0.495, #0.515, #0.2945, #0.52,
        voltage=2.7,
        offset=0.0,
        )
qdt.Ejmax=4.5e-23#2.75e-23 #h*44.0e9 #h*44.0e9
qdt.Cc=30e-15

qdt.Ec=2e-25
#qdt.f0=5.32e9 #5.35e9
#qdt.fixed_freq_max=20.0*qdt.f0

#qdt.Ct=1.25e-13
#qdt.K2=0.052
qdt.S_type="simple"
qdt.fixed_freq_max=20.0*qdt.f0

qdt.S_type="simple"
qdt.Y0_type="center" #"formula"
qdt.df_type="center" #"formula"
qdt.mus_type="center" #"formula"
qdt.Ga_type="sinc" #"giant atom"
qdt.Ba_type="formula" #"hilbert"
qdt.rs_type="formula"
qdt.qubit_type="scb" #"transmon" #"scb"
print qdt._get_anharm()
print qdt.anharm
#qdt.f=ideal_qdt.fq

#qdt.couple_type="sinc^2"
#qdt.Lamb_shift_type="formula"
#qdt.Np=9.5#9.5
#qdt.Ec=1e-25
#f=Fitter(plot_name="centers")
#qdt.gate_type="capacitive"
#qdt.magabs_type="S33"
#qdt.fixed_freq_min=3e9
#qdt.fixed_freq_max=8e9
#qdt.fixed_fq_min=1e9
#qdt.fixed_fq_max=10e9
#qdt.fitter.gamma=0.05
pl1=qdt.plotter
#pl1.show()

pl=a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pl=pl1).show()


if 0:
    a.filter_type="FFT"

    a.filter_type="Fit"
    pl, pf=a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pf_too=True)
                               #auto_zlim=False, vmin=0.0, vmax=0.02)
    a.widths_plot()
    a.center_plot()#.show()
    a.filter_type="FFT"
    a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pl=pl)#.show()
filt=Filter()
filt.center=80
filt.halfwidth=50
def ifft_plot(self, **kwargs):
    process_kwargs(a, kwargs, pl="hannifft2_{0}_{1}_{2}".format(a.filter_type, a.bgsub_type, a.name))
    on_res=absolute(filt.window_ifft(self.MagcomData[205,:]))
    strt=absolute(filt.window_ifft(self.MagcomData[266,:]))
    #stop=absolute(self.filt.window_ifft(self.MagcomData[:,self.stop_ind, self.frq2_ind]))

    pl=line( filt.fftshift(on_res),  color="red",
            plot_name="onres_{}".format(self.on_res_ind),label="{:.4g}".format(self.on_res_ind), **kwargs)
    line(filt.fftshift(strt), pl=pl, linewidth=1.0, color="purple",
         plot_name="strt {}".format(self.start_ind), label="{:.4g}".format(self.start_ind))
        #line(self.time_axis, self.filt.fftshift(stop), pl=pl, linewidth=1.0, color="blue",
        #     plot_name="stop {}".format(self.stop_ind), label="{:.4g}".format(self.stop_ind))

    filt.N=len(on_res)
    filty=filt.freqz
    top=amax(on_res)#, amax(strt), amax(stop)])
    line( filty*top, plotter=pl, color="green", label="wdw")
    pl.xlabel=kwargs.pop("xlabel", self.time_axis_label)
    pl.ylabel=kwargs.pop("ylabel", "Mag abs")
    double_filt=array([filt.fft_filter(self.MagcomData[n, :]) for n in range(len(self.frequency))])
    colormesh((absolute(double_filt[:, 30:-30]).transpose()-absolute(double_filt[:, 30])).transpose())
    return pl

ifft_plot(a).show()
if __name__=="__main2__":
    pls=a.fft_plots()
    #a.save_plots(pls)
    pls[0].show()
