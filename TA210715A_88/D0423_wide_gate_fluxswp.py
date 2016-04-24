# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Lyzer, TA88_Read, qdt
from taref.plotter.api import colormesh, line
from taref.core.api import set_tag, set_all_tags
from numpy import array, squeeze, sqrt, pi, mod, floor_divide, trunc, arccos, shape
from atom.api import FloatRange
from taref.core.api import tag_Property
from taref.plotter.api import LineFitter
from taref.physics.fundamentals import h
from scipy.optimize import fsolve

s3a4_wg=TA88_Lyzer(filt_start_ind=0, filt_end_ind=0, on_res_ind=260,# VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0423/S3A4_widegate.hdf5"))
s3a4_wg.read_data(s3a4_wg)

def magabs_colormesh(self):
    pl, pf=colormesh(self.frequency/1e9, self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0]), plotter="magabs_{}".format(self.name))
    pl.set_xlim(min(self.frequency/1e9), max(self.frequency/1e9))
    pl.set_ylim(min(self.yoko), max(self.yoko))
    pl.xlabel="Yoko (V)"
    pl.ylabel="Frequency (GHz)"
    return pl

#def flux_par(self, pl, offset, flux_factor):
#    set_tag(qdt, "EjdivEc", log=False)
#    set_tag(qdt, "Ej", log=False)
#    set_tag(qdt, "offset", log=False)
#    set_tag(qdt, "flux_factor", log=False)
#
#    print qdt.max_coupling, qdt.coupling_approx
#    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
#    Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0)
#    EjdivEc=Ej/qdt.Ec
#    #fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
#    ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
#    ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
#    line(self.yoko, ls_fq/1e9, plotter=pl, color="blue", linewidth=0.5, label=r"$\Delta_{1,0}$")
#    line(self.yoko, ls_fq2/1e9, plotter=pl, color="red", linewidth=0.5, label=r"$\Delta_{2,1}$")
#    #pl.set_ylim(-1.0, 0.6)
#    #pl.set_xlim(0.7, 1.3)
#    return pl

from taref.physics.qubit import flux_parabola, Ej_from_fq, voltage_from_flux

def flux_par3(self, offset=-0.1, flux_factor=0.5312, Ejmax=h*40.5e9, pl=None):
    set_all_tags(qdt, log=False)
    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    #print flux_o_flux0-pi/2*trunc(flux_o_flux0/(pi/2.0))
    #Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
    #EjdivEc=Ej/qdt.Ec
    fq_vec=array([sqrt(f*(f+1.0*qdt.call_func("calc_Lamb_shift", fqq=f))) for f in self.frequency])
    fq_vec=array([f-qdt.call_func("calc_Lamb_shift", fqq=f) for f in self.frequency])

    Ej=Ej_from_fq(fq_vec, qdt.Ec)
    flux_d_flux0=arccos(Ej/Ejmax)#-pi/2

    if pl is not None:
        volt=voltage_from_flux(flux_d_flux0, offset, flux_factor)
        line(s3a4_wg.frequency/1e9, volt, plotter=pl)
        EjdivEc=Ej/qdt.Ec
        fq_vec=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
        Ej=Ej_from_fq(fq_vec, qdt.Ec)
        flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
        volt=voltage_from_flux(flux_d_flux0, offset, flux_factor)
        line(s3a4_wg.frequency/1e9, volt, plotter=pl)
    #flux_d_flux0.append(-)
    return voltage_from_flux(flux_d_flux0, offset, flux_factor)

print shape(flux_par3(s3a4_wg, 0.0, 0.3, qdt.Ejmax))#, shape(self.frequency)
def flux_par2(self, offset, flux_factor, Ejmax):
    set_all_tags(qdt, log=False)
    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
    EjdivEc=Ej/qdt.Ec
    fq_vec=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    results=[]
    for fq in fq_vec:
        def Ba_eqn(x):
            return x[0]**2+2.0*x[0]*qdt.call_func("calc_Lamb_shift", fqq=x[0])-fq**2
        results.append(fsolve(Ba_eqn, fq))
    return squeeze(results)/1e9

#flux_par2(s3a4_wg, 0.0, 0.18, qdt.Ejmax)

def flux_par(self, offset, flux_factor, Ejmax):
    set_all_tags(qdt, log=False)
#    set_tag(qdt, "EjdivEc", log=False)
#    set_tag(qdt, "Ej", log=False)
#    set_tag(qdt, "offset", log=False)
#    set_tag(qdt, "flux_factor", log=False)
    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
    EjdivEc=Ej/qdt.Ec
    fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    ls=qdt.call_func("calc_Lamb_shift", fqq=fq)
    return fq/1e9
    ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
    ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
    return ls_fq/1e9#, ls_fq2/1e9

pl=magabs_colormesh(s3a4_wg)#.show()
#flux_par3(s3a4_wg, pl=pl)
#pl.show()

class Fitter(LineFitter):
    Ejmax=FloatRange(0.001, 100.0, qdt.Ejmax/h/1e9).tag(tracking=True)
    offset=FloatRange(-5.0, 5.0, 0.0).tag(tracking=True)
    flux_factor=FloatRange(0.1, 5.0, 0.3).tag(tracking=True)

    def _default_plotter(self):
        if self.plot_name=="":
            self.plot_name=self.name
        pl1, pf=line(s3a4_wg.frequency/1e9, self.data, plot_name=self.plot_name, plotter=pl)
        self.plot_name=pf.plot_name
        return pl1

    @tag_Property(private=True)
    def data(self):
        return flux_par3(s3a4_wg, offset=self.offset, flux_factor=self.flux_factor, Ejmax=self.Ejmax*h*1e9)

d=Fitter()
d.show(d.plotter)

#s3a4_wg
#s3a4_mp.magabsfilt_colormesh("filtcolormesh S3A4 mp")
#s3a4_mp.magdBfilt_colormesh("filtdB S1A4 wide")
#s3a4_mp.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
        #a2.filt_compare(a2.start_ind, bb2)
#s3a4_mp.filt_compare("filt_compare_off_res", s3a4_mp.start_ind)
#s3a4_mp.filt_compare("filt_compare_on_res", s3a4_mp.on_res_ind)
#s3a4_mp.ifft_plot("ifft_S3A4 midpeak")
#s3a4_mp.ifft_dif_plot("ifft__dif_S1A4 wide")

