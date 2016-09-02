# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:28:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read_NP, TA88_Lyzer, TA88_Read#, qdt
from taref.physics.qdt import QDT
from taref.plotter.api import scatter, line,  LineFitter, Plotter
from atom.api import FloatRange, Typed, Unicode
from taref.core.universal import ODict
from numpy import append, linspace
from taref.core.api import tag_property, get_all_tags, get_tag
from taref.physics.fundamentals import h

npr=TA88_Read_NP(file_path=r"/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/D0629_flux_parabola.txt",
                 show_data_str=True)
data=npr.read()

#qdt=QDT(name="fitting_qdt",
#        material='LiNbYZ',
#        ft="double",
#        S_type="RAM",
#        a=80.0e-9, #f0=5.35e9,
#        Np=9,
#        Rn=3780.0, #(3570.0+4000.0)/2.0, Ejmax=h*44.0e9,
#        W=25.0e-6,
#        eta=0.5,
#        flux_factor=0.515, #0.2945, #0.52,
#        voltage=1.21,
#        offset=-0.07)
#qdt.Ejmax=h*44.0e9 #h*44.0e9
#qdt.f0=5.38e9 #5.35e9
#qdt.Ct=1.25e-13
#qdt.K2=qdt.K2*0.9
class QDTFitter(QDT):
    base_name="qdt_fitter"

    plotter=Typed(Plotter).tag(private=True)
    plot_name=Unicode().tag(private=True)
    data_dict=ODict().tag(private=True)

    def __setattr__(self, name, value):
        super(QDTFitter, self).__setattr__(name, value)
        self.update_plot(dict(type="update"))

    #def extra_setup(self, param, typer):
    #    """adds log_changes observer to all params"""
    #    super(QDTFitter, self).extra_setup(param, typer)
    #    self.observe(param, self.update_plot)

    def _default_plotter(self):
        if self.plot_name=="":
            self.plot_name=self.name
        pl=Plotter(name=self.name)
        for param in get_all_tags(self, "plot"):
            print param
            pl, pf=line(*getattr(self, param), plot_name=get_tag(self, param, "plot"), plotter=pl, pf_too=True)
            self.data_dict[param]=pf.plot_name
        return pl

    def update_plot(self, change):
        if change["type"]=="update":
            print self.data_dict
            for param, plot_name in self.data_dict.iteritems():
                print param, plot_name
                self.get_member(param).reset(self)
                self.plotter.plot_dict[plot_name].alter_xy(*getattr(self,param))

    @tag_property(private=True)
    def frequency(self):
        return linspace(3.5e9, 7.5e9, 1000)

    @tag_property(private=True, plot="flux_par")
    def data(self):
        freq=append(self.frequency/1e9, self.frequency/1e9)
        freq=append(freq, freq)
        return freq, self._get_Vfq0_many(f=self.frequency)[1]

qdt=QDTFitter(name="fitting_qdt",
        material='LiNbYZ',
        ft="double",
        #S_type="RAM",
        a=80.0e-9, #f0=5.35e9,
        Np=9,
        Rn=3780.0, #(3570.0+4000.0)/2.0, Ejmax=h*44.0e9,
        W=25.0e-6,
        eta=0.5,
        flux_factor=0.495, #0.515, #0.2945, #0.52,
        voltage=1.21,
        offset=-0.07,
        plot_name="centers")
qdt.Ejmax=2.75e-23 #h*44.0e9 #h*44.0e9
qdt.f0=5.32e9 #5.35e9
#qdt.Ct=1.25e-13
qdt.K2=0.038
qdt.S_type="simple"
qdt.couple_type="sinc^2"
qdt.Lamb_shift_type="formula"
qdt.Np=9.5
qdt.Ec=1e-25
#f=Fitter(plot_name="centers")
pl1=qdt.plotter
scatter(data[:, 0], data[:, 1], fig_width=9, fig_height=6, pl=pl1, color="red").show()

class Fitter(LineFitter):
    Ejmax=FloatRange(0.001, 100.0, qdt.Ejmax/h/1e9).tag(tracking=True)
    offset=FloatRange(-5.0, 5.0, qdt.offset).tag(tracking=True)
    flux_factor=FloatRange(0.1, 5.0, qdt.flux_factor).tag(tracking=True)
    f0=FloatRange(4.0, 6.0, qdt.f0/1e9).tag(tracking=True)
    alpha=FloatRange(0.0, 2.0, 0.0*qdt.couple_mult).tag(tracking=True)
    Ct=FloatRange(0.1, 10.0, qdt.Ct/1e-13).tag(tracking=True)

    @tag_property(private=True)
    def frequency(self):
        return linspace(3.5e9, 7.5e9, 1000)

#    def _default_plotter(self):
#        if self.plot_name=="":
#            self.plot_name=self.name
#        freq=self.frequency[:]/1e9
#        freq=append(freq, freq)
#        freq=append(freq, freq)
#        pl1, pf=line(*self.data, plot_name=self.plot_name, pf_too=True)
#        self.plot_name=pf.plot_name
#        return pl1

    @tag_property(private=True, plot="flux_par")
    def data(self):
        freq=append(self.frequency/1e9, self.frequency/1e9)
        freq=append(freq, freq)
        return freq, qdt._get_Vfq0_many(f=self.frequency, f0=self.f0*1e9, Ct=self.Ct*1e-13,
                                         Ejmax=self.Ejmax*h*1e9, offset=self.offset,
                                          flux_factor=self.flux_factor)[1]#, plotter=pl, color="red", linewidth=1.0)

        return self.frequency/1e9, qdt._get_Vfq0(f=self.frequency, f0=self.f0*1e9, Ct=self.Ct*1e-13,
                                                 Ejmax=self.Ejmax*h*1e9, offset=self.offset,
                                                  flux_factor=self.flux_factor)#, plotter=pl, color="red", linewidth=1.0)
        #return flux_par3(s3a4_wg, offset=self.offset, flux_factor=self.flux_factor,
        #                 C=self.Ct*1e-13, Ejmax=self.Ejmax*h*1e9, f0=self.f0*1e9, alpha=self.alpha)

f=Fitter(plot_name="centers")
pl1=f.plotter
scatter(data[:, 0], data[:, 1], fig_width=9, fig_height=6, pl=pl1, color="red").show()

a=TA88_Lyzer(on_res_ind=201,# VNA_name="RS VNA", filt_center=15, filt_halfwidth=15,
        rd_hdf=TA88_Read(main_file="Data_0628/S4A4_just_gate_overnight_flux_swp.hdf5"))



a.filt.center=0
a.filt.halfwidth=200
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.01
a.flux_axis_type="yoko"#"flux"
#a.end_skip=10
#a.fit_indices=[range(2, 14), range(15, 17), range(19,23), range(24, 26), range(29, 37), range(38, 39), range(44, 46), range(48, 52),
#               range(54, 66), range(67, 69), range(70, 85), range(105, 107), range(108, 116), range(122, 129), [130], range(132, 134), [138],
# range(182,184), range(188, 193), range(217, 251+1), range(266, 275+1), range(314, 324+1)]
#a.flux_indices=[range(400,434), range(436, 610)]
#a.flux_indices=[range(200, 400)]
a.read_data()
a.ifft_plot()

a.bgsub_type="dB"
#a.filter_type="FFT"
pl0=a.magabs_colormesh(vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False, pl="magabs", fig_width=9, fig_height=6)

pl=a.magabs_colormesh(vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False, fig_width=9, fig_height=6)
scatter(data[:, 1], data[:, 0], pl=pl, color="cyan")
pl1=scatter(data[:, 0], data[:, 1], fig_width=9, fig_height=6)

line(a.voltage_from_flux_par2[0]/1e9, a.voltage_from_flux_par2[1], pl=pl1, color="red")#.show()
#pl1.show()

#if 0:
    #pl0.savefig(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/", "fluxmap")

    #pl.savefig(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/", "fluxmap_w_peaks")

    #pl1.savefig(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/", "just_peaks")


