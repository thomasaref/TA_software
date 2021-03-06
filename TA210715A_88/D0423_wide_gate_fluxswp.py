# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Lyzer, TA88_Read, qdt
from taref.plotter.api import colormesh, line, Plotter
from taref.core.api import set_tag, set_all_tags
from numpy import array, nan_to_num, squeeze, append, sqrt, pi, mod, floor_divide, trunc, arccos, shape
from atom.api import FloatRange
from taref.core.api import tag_Property
from taref.plotter.api import LineFitter
from taref.physics.fundamentals import h
from scipy.optimize import fsolve

s3a4_wg=TA88_Lyzer(filt_start_ind=0, filt_end_ind=0, on_res_ind=260,# VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0423/S3A4_widegate.hdf5"))
s3a4_wg.read_data(s3a4_wg)

def magabs_colormesh2(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
    fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])

    pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
    pl, pf=colormesh(fq_vec, self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0]), plotter=pl)
    pf.set_clim(-0.3, 0.1)
    #pl.set_xlim(min(self.frequency/1e9), max(self.frequency/1e9))
    pl.set_ylim(min(self.yoko), max(self.yoko))

    pl.ylabel="Yoko (V)"
    pl.xlabel="Frequency (GHz)"
    return pl

def magabs_colormesh(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
    fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])
    freq, frq2=flux_parabola(self.yoko, offset, 0.16, Ejmax, qdt.Ec)

    pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
    pl, pf=colormesh(freq, fq_vec, (self.MagdB.transpose()-self.MagdB[:, 0]).transpose(), plotter=pl)
    pf.set_clim(-0.3, 0.1)
    line([min(freq), max(freq)], [min(freq), max(freq)], plotter=pl)
    flux_o_flux0=flux_over_flux0(self.yoko, offset, flux_factor)
    qEj=Ej(Ejmax, flux_o_flux0)
    EjdivEc=qEj/qdt.Ec
    ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
    ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)

    frq2=qdt.call_func("lamb_shifted_anharm", EjdivEc=EjdivEc)/h
    line(ls_fq, ls_fq2, plotter=pl)

    #pl.set_xlim(min(self.frequency/1e9), max(self.frequency/1e9))
    #pl.set_ylim(min(self.yoko), max(self.yoko))

    pl.ylabel="Yoko (V)"
    pl.xlabel="Frequency (GHz)"
    return pl

def line_cs(self, ind=210):
    print self.frequency[ind]/1e9
    pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_cs_{}".format(self.name))
    pl, pf=line(self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0])[:, ind], plotter=pl, linewidth=1.0)
    pl.xlabel="Yoko (V)"
    pl.ylabel="Magnitude (dB)"
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

from taref.physics.qubit import  flux_parabola, Ej_from_fq, voltage_from_flux, flux_over_flux0, Ej
from taref.physics.qdt import lamb_shifted_anharm, calc_freq_shift, lamb_shifted_fq, lamb_shifted_fq2

def fq2(Ej, Ec):
    E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
    #E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
    E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
    return (E2-E0)/h/2

def Ej_from_fq2(fq2, Ec):
    return (((2*h*fq2+3.0*Ec)/2.0)**2)/(8.0*Ec)

def flux_par4(self, offset=-0.08, flux_factor=0.16, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
    set_all_tags(qdt, log=False)
    flux_o_flux0=flux_over_flux0(self.yoko, offset, flux_factor)
    qEj=Ej(Ejmax, flux_o_flux0)
    #flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    freq, frq2=flux_parabola(self.yoko, offset, flux_factor, Ejmax, qdt.Ec)
    fq1=lamb_shifted_fq2(qEj/qdt.Ec, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv)
    line(self.yoko, freq, plotter=pl, linewidth=1.0, alpha=0.5)
    line(self.yoko, fq1/2, plotter=pl, linewidth=1.0, alpha=0.5)

def flux_par3(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
    set_all_tags(qdt, log=False)
    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    #print flux_o_flux0-pi/2*trunc(flux_o_flux0/(pi/2.0))
    #Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
    #EjdivEc=Ej/qdt.Ec
    fq_vec=array([sqrt(f*(f+1.0*qdt.call_func("calc_Lamb_shift", fqq=f))) for f in self.frequency])
    fq_vec=array([f-qdt.call_func("calc_Lamb_shift", fqq=f) for f in self.frequency])
    fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])
    Ej=Ej_from_fq(fq_vec, qdt.Ec)
    flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
    flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
    flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax)+pi)
    flux_d_flux0=append(flux_d_flux0, arccos(Ej/Ejmax)-pi)

    if pl is not None:
        volt=voltage_from_flux(flux_d_flux0, offset, flux_factor)
        freq=s3a4_wg.frequency[:]/1e9
        freq=append(freq, freq) #append(freq, append(freq, freq)))
        freq=append(freq, freq)
        #freq=append(freq, freq)
        line(freq, volt, plotter=pl, linewidth=1.0, alpha=0.5)
        Ejdivh=Ej/h
        w0=4*Ejdivh*(1-sqrt(1-fq_vec/(2*Ejdivh)))
        EjdivEc=Ej/qdt.Ec
        #print -(w0**2)/(8*Ejdivh)
        
        ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
        E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
        fq2=(E2-E1)/h
        f_vec=lamb_shifted_anharm(EjdivEc, qdt.ft, qdt.Np, qdt.f0, qdt.epsinf, qdt.W, qdt.Dvv)
        print f_vec/h
        ah=-ls_fq2/2#-fq2)
        #fq_vec=array([sqrt((f-ah[n])*(f-ah[n]+alpha*calc_freq_shift(f-ah[n], qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for n, f in enumerate(self.frequency)])
        fq_vec=array([f/2-qdt.call_func("calc_Lamb_shift", fqq=f/2) for f in self.frequency])
        coup=qdt.call_func("calc_coupling", fqq=self.frequency)
        print coup
        volt=array([
          voltage_from_flux(arccos(Ej_from_fq(f-f_vec[c]/h/2, qdt.Ec)/Ejmax), offset, flux_factor)
          for c,f in enumerate(self.frequency)])
        #freq=nan_to_num(freq)/1e9
        #print freq
        freq=s3a4_wg.frequency[:]/1e9

        #freq=(s3a4_wg.frequency[:]+coup)/1e9
        #freq=append(freq, freq)
        #freq=append(freq, freq)
        #Ej=Ej_from_fq(fq_vec, f_vec/h)
        #flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
        #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
        #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax)+pi)
        #flux_d_flux0=append(flux_d_flux0, arccos(Ej/Ejmax)-pi)

        #freq=append(freq, freq)
        #fq_vec+=f_vec/h/2
        #fq2_vec=fq2(Ej, qdt.Ec)
        #Ej=Ej_from_fq(fq_vec, qdt.Ec) #qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
        #Ej=Ej_from_fq(fq_vec, qdt.Ec)
        #flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
        #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
        #volt=voltage_from_flux(flux_d_flux0, offset, flux_factor)
        line(freq, volt, plotter=pl, plot_name="second", color="green", linewidth=1.0, alpha=0.5)
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
#pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#           fig_name="wide_gate_colormap.png")
flux_par4(s3a4_wg, pl=pl)#.show()#, f0=5.45e9, alpha=1.0)
#pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#           fig_name="wide_gate_colormap_bothpar.png")

#pl=line_cs(s3a4_wg, 190)
#pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#           fig_name="wide_gate_cs_5p4.pdf")
#pl=line_cs(s3a4_wg, 210)
#pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#           fig_name="wide_gate_cs_5p6.pdf")
#pl=line_cs(s3a4_wg, 239)
#pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#           fig_name="wide_gate_cs_5p89.pdf")
#pl=line_cs(s3a4_wg, 246)
#pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#           fig_name="wide_gate_cs_5p96.pdf")
#pl=line_cs(s3a4_wg, 256)
#pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#           fig_name="wide_gate_cs_6p06.pdf")


#pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#           fig_name="wide_gate_colormap_bothpar.png")
pl.show()

class Fitter(LineFitter):
    Ejmax=FloatRange(0.001, 100.0, qdt.Ejmax/h/1e9).tag(tracking=True)
    offset=FloatRange(-5.0, 5.0, 0.0).tag(tracking=True)
    flux_factor=FloatRange(0.1, 5.0, 0.3).tag(tracking=True)
    f0=FloatRange(4.0, 6.0, qdt.f0/1e9).tag(tracking=True)
    alpha=FloatRange(0.1, 2.0, 1.0).tag(tracking=True)

    def _default_plotter(self):
        if self.plot_name=="":
            self.plot_name=self.name
        freq=s3a4_wg.frequency[:]/1e9
        freq=append(freq, freq)
        freq=append(freq, freq)
        pl1, pf=line(freq, self.data, plot_name=self.plot_name, plotter=pl)
        self.plot_name=pf.plot_name
        return pl1

    @tag_Property(private=True)
    def data(self):
        return flux_par3(s3a4_wg, offset=self.offset, flux_factor=self.flux_factor, Ejmax=self.Ejmax*h*1e9, f0=self.f0*1e9, alpha=self.alpha)

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

