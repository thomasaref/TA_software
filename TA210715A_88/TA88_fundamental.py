# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:08:41 2016

@author: thomasaref
"""

from taref.physics.qdt import QDT
from taref.physics.idt import IDT
#from taref.core.atom_extension import get_tag, tag_property
from taref.filer.read_file import Read_HDF5, Read_NP
from taref.filer.filer import Folder
from taref.filer.save_file import Save_NP
from taref.core.agent import Agent
from atom.api import Float, Unicode, Typed, Int, Callable, Enum
from taref.core.universal import Array
from numpy import array, log10, sqrt, fft, exp, float64, linspace, shape, reshape, squeeze, mean, angle, absolute, sin, pi
from h5py import File
from scipy.optimize import leastsq
from taref.core.log import log_debug
from taref.plotter.plotter import line, colormesh, Plotter
from taref.physics.units import dBm, dB
from taref.physics.fundamentals import h#Ej, fq, flux_over_flux0

#from lyzer import Lyzer
from taref.analysis.api import Lyzer, VNA_Lyzer, VNA_Pwr_Lyzer

class TA88_Read(Read_HDF5):
    def _default_folder(self):
        return Folder(base_dir="/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/TA210715A88_cooldown210216", quality="", main_dir="Data_0221")

class TA88_Save_NP(Save_NP):
    def _default_folder(self):
        return Folder(base_dir="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed")

class TA88_Read_NP(Read_NP):
    def _default_folder(self):
        return Folder(base_dir="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed")

#read_dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216"

ideal_qdt=QDT(name="idealQDT",
        material='LiNbYZ',
        ft="double",
        a=80.0e-9, #f0=5.35e9,
        Np=9,
        Rn=(3570.0+4000.0)/2.0,# Ejmax=h*44.0e9,
        W=25.0e-6,
        eta=0.5,
        flux_factor=0.495, #0.52, #0.2945, #0.52,
        voltage=2.2, #1.21,
        offset=-0.07,
        loop_width=2.7e-6,
        loop_height=1.5e-6)
ideal_qdt.fixed_freq_max=20.0*ideal_qdt.f0

ideal_qdt.S_type="simple"
ideal_qdt.Y0_type="center" #"formula"
ideal_qdt.df_type="center" #"formula"
ideal_qdt.mus_type="center" #"formula"
ideal_qdt.Ga_type="sinc" #"giant atom"
ideal_qdt.Ba_type="formula" #"hilbert"
ideal_qdt.rs_type="formula"
ideal_qdt.f=ideal_qdt.fq
#qdt=QDT(material='LiNbYZ',
#        ft="double",
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

qdt=QDT(name="fittedQDT",
        material='LiNbYZ',
        ft="double",
        #S_type="RAM",
        a=80.0e-9, #f0=5.35e9,
        Np=9,
        Rn=3780.0, #(3570.0+4000.0)/2.0, Ejmax=h*44.0e9,
        W=25.0e-6,
        eta=0.5,
        flux_factor=0.495, #0.515, #0.2945, #0.52,
        voltage=2.2, #1.21,
        offset=-0.07,
        loop_width=2.7e-6,
        loop_height=1.5e-6)
#qdt.Ejmax=2.75e-23 #h*44.0e9 #h*44.0e9
qdt.f0=5.30e9 #5.35e9
#qdt.fixed_freq_max=20.0*qdt.f0
#qdt.eta=0.55
qdt.Np=9.5
qdt.K2=0.042
qdt.gate_type="capacitive"
qdt.Cc=35e-15
qdt.Cground=5e-15
qdt.magabs_type="S33"
qdt.Rn=2800.0
qdt.fixed_freq_min=3.5e9
qdt.fixed_freq_max=7.5e9
qdt.fixed_fq_min=1e9
qdt.fixed_fq_max=7.0e9

#qdt.Ct=1.25e-13
#qdt.K2=0.038
#qdt.Y0_type="center"
#qdt.df_type="center"
#qdt.mus_type="center"
#qdt.Ga_type="sinc"
#qdt.Ba_type="formula"
#qdt.rs_type="constant"
#qdt.S_type="simple"
#qdt.Y0_type="center" #"formula"
#qdt.df_type="center" #"formula"
#qdt.mus_type="center" #"formula"
#qdt.Ga_type="sinc" #"giant atom"
#qdt.Ba_type="formula" #"hilbert"
#qdt.rs_type="constant" #"formula"
#qdt.flux_factor_beta=0.01
#qdt.Np=9.5
#qdt.Ec=1e-25
#qdt.dephasing=10e6
#qdt.dephasing_slope=3e-3
qdt.f=qdt.fq

ideal_idt=IDT(name="idealIDT",
              material='LiNbYZ',
        ft="double",
        Np=36,
        W=25.0e-6,
        eta=0.5,
        a=96.0e-9)

idt=IDT(material='LiNbYZ',
        ft="double",
        Np=36.5,
        W=25.0e-6,
        eta=0.5,
        a=96.0e-9)
idt.f0=4.452e9

#print qdt.all_params
#print idt.all_params
class TA88_Lyzer(Lyzer):
    qdt=qdt
    idt=idt

class TA88_VNA_Pwr_Lyzer(VNA_Pwr_Lyzer):
    qdt=qdt
    idt=idt

class TA88_VNA_Lyzer(VNA_Lyzer):
    qdt=qdt
    idt=idt


    def fft_plots(self):
        self.read_data()
        self.filter_type="None"
        pl1=self.magabs_colormesh(fig_width=6.0, fig_height=4.0)
        pl1.add_label("a)")
        pl2=self.ifft_plot(fig_width=6.0, fig_height=4.0, #time_axis_type="time",
                    auto_xlim=False, x_min=-0.05, x_max=1.0, show_legend=True)#, auto_ylim=False, y_min=-0.0001, y_max=0.008)
        self.filter_type="FFT"

        pl2.add_label("b)")
        dif=pl2.y_max*0.1
        pl2.y_min=-dif
        pl2.y_max+=dif

        self.filter_type="Fit"

        pl3, pf3=self.magabs_colormesh(fig_width=6.0, fig_height=4.0, pf_too=True)
                               #auto_zlim=False, vmin=0.0, vmax=0.02)
        pl3.add_label("d)")

        self.filter_type="FFT"
        pl4=self.magabs_colormesh(fig_width=6.0, fig_height=4.0,
                               auto_zlim=False, vmin=pf3.vmin, vmax=pf3.vmax, auto_ylim=False, y_min=pl3.y_min, y_max=pl3.y_max)
        pl4.add_label("c)")

        pl_list=[pl1, pl2, pl4, pl3]
        return pl_list

a=TA88_Lyzer( name="theory_check",
         desc="theory check plots",
         )
a.save_folder.main_dir=a.name

def coupling_plot():
    pl=Plotter(fig_width=6.0, fig_height=4.0)
    fw0=linspace(4e9, 7e9, 2000)
    line(fw0/1e9, qdt._get_coupling(fw0)/1e9, label=r"$G_a/2C$", color="blue", plotter=pl)
    line(fw0/1e9, qdt._get_Lamb_shift(fw0)/1e9, label=r"$-B_a/2C$", color="red", plotter=pl)
    line(fw0/1e9, idt._get_coupling(fw0)/4/1e9, label=r"$G_a^{IDT}/2C/4$", color="green", linewidth=1.0, plotter=pl)
    pl.set_ylim(-1.0, 1.5)
    pl.legend(loc='lower right')
    return pl

def anharm_plot2(qdt, fig_width=9.0, fig_height=6.0, ymin=-1.5, ymax=1.0):
    """Lamb shifted anharmonicity plot"""
    pl=Plotter(fig_width=fig_width, fig_height=fig_height)
    fw0=linspace(2e9, 7e9, 2000)
    lsfw0=array([sqrt(f*(f-2*qdt._get_Lamb_shift(f=f))) for f in fw0])
    Ej=qdt._get_Ej_get_fq(fq=lsfw0)
    E0, E1, E2=qdt._get_transmon_energy_levels(Ej=Ej, n_energy=3)
    anharm=(E2-E1)-(E1-E0)
    E0p, E1p, E2p=qdt._get_lamb_shifted_transmon_energy_levels(Ej=Ej, n_energy=3)
    anharmp=(E2p-E1p)-(E1p-E0p)
    line(lsfw0/1e9, anharm/h/1e9, plotter=pl, linewidth=0.5, color="purple", label=r"anharm")
    line(lsfw0/1e9, anharmp/h/1e9, plotter=pl, linewidth=0.5, color="black", label=r"ls anharm")
    line(fw0/1e9, qdt._get_coupling(fw0)/qdt.max_coupling, label=r"$G_a/2C$", color="blue", plotter=pl)
    pl.xlabel=r"$E_J/E_C$"
    pl.ylabel=r"$\Delta$ (GHz)"
    pl.legend(loc='lower left')
    return pl

def mag_theory(qdt, fig_width=9.0, fig_height=6.0):
    pl=Plotter(fig_width=fig_width, fig_height=fig_height)
    fw0=linspace(2e9, 8e9, 2000)
    voltage=linspace(-5, 5, 3000)
    fq=qdt._get_flux_parabola(voltage=voltage)
    L=qdt._get_L(fq=fq)
    print "yo"
    S11=qdt._get_S11(f=fw0, L=L)
    print "done s11"
    colormesh(fw0/1e9, voltage, absolute(S11), plotter=pl)
    #line(*qdt._get_ls_voltage_from_flux_par_many(f=fw0), plotter=pl, linewidth=0.5, alpha=0.5, color="cyan")
    print "done plot"
    return pl
    ls_f=sqrt(fw0*(fw0-2*qdt._get_Lamb_shift(f=fw0)-2*qdt._get_coupling(f=fw0)))
    Ec=qdt._get_Ec()
    Ej=qdt._get_Ej_get_fq(fq=ls_f, Ec=Ec)
    flux_d_flux0=qdt._get_flux_over_flux0_get_Ej(Ej=Ej)
    V1=qdt._get_voltage(flux_over_flux0=flux_d_flux0)
    line(fw0/1e9, qdt._get_voltage(flux_over_flux0=flux_d_flux0), plotter=pl, linewidth=0.3, color="darkgray")
    print "yo2"
    ls_f=sqrt(fw0*(fw0-2*qdt._get_Lamb_shift(f=fw0)+2*qdt._get_coupling(f=fw0)))
    Ec=qdt._get_Ec()
    Ej=qdt._get_Ej_get_fq(fq=ls_f, Ec=Ec)
    flux_d_flux0=qdt._get_flux_over_flux0_get_Ej(Ej=Ej)
    V2=qdt._get_voltage(flux_over_flux0=flux_d_flux0)
    line(fw0/1e9,V2, plotter=pl, linewidth=0.3, color="darkgray")

    p, pf=line(fw0/1e9, absolute(V2-V1)/max(absolute(V2-V1)), linewidth=0.3, color="blue")
    line(fw0/1e9, qdt._get_coupling(f=fw0)/qdt.max_coupling, linewidth=0.3, color="red", plotter=p)
    print "yo3"
    #fw02=(qdt._get_Ga(f=fw0)-qdt._get_Ba(f=fw0))/(4*pi*qdt.C)
    #line(fw0, fw0+fw02, plotter=pl)
    #line(*qdt._get_ls_voltage_from_flux_par_many(f=fw0+fw02), plotter=pl, linewidth=0.5, alpha=0.5, color="cyan")

    return pl

def phase_theory(qdt, fig_width=9.0, fig_height=6.0):
    pl=Plotter(fig_width=fig_width, fig_height=fig_height)
    fw0=linspace(2e9, 8e9, 2000)
    voltage=linspace(-5, 5, 1000)
    fq=qdt._get_flux_parabola(voltage=voltage)
    L=qdt._get_L(fq=fq)
    S11=qdt._get_S11(f=fw0, L=L)
    colormesh(fw0/1e9, voltage, angle(S11), plotter=pl)
    line(*qdt._get_ls_voltage_from_flux_par_many(f=fw0), plotter=pl, linewidth=0.5, alpha=0.5, color="cyan")
    return pl

def S13_mag_theory(qdt, fig_width=9.0, fig_height=6.0):
    pl=Plotter(fig_width=fig_width, fig_height=fig_height)
    fw0=linspace(2e9, 8e9, 2000)
    voltage=linspace(-5, 5, 1000)
    fq=qdt._get_flux_parabola(voltage=voltage)
    L=qdt._get_L(fq=fq)
    S13=qdt._get_S13(f=fw0, L=L)
    colormesh(fw0/1e9, voltage, 10*log10(absolute(S13)), plotter=pl)
    line(*qdt._get_ls_voltage_from_flux_par_many(f=fw0), plotter=pl, linewidth=0.5, alpha=0.5, color="cyan")
    return pl

def S13_phase_theory(qdt, fig_width=9.0, fig_height=6.0):
    pl=Plotter(fig_width=fig_width, fig_height=fig_height)
    fw0=linspace(2e9, 8e9, 2000)
    voltage=linspace(-5, 5, 1000)
    fq=qdt._get_flux_parabola(voltage=voltage)
    L=qdt._get_L(fq=fq)
    S13=qdt._get_S13(f=fw0, L=L)
    colormesh(fw0/1e9, voltage, angle(S13), plotter=pl)
    line(*qdt._get_ls_voltage_from_flux_par_many(f=fw0), plotter=pl, linewidth=0.5, alpha=0.5, color="cyan")
    return pl

if __name__=="__main__":
    pl0=qdt.lgf1.lgf_test_plot()
    from taref.physics.surface_charge import element_factor_plot, metallization_plot, Rho
    pl1=element_factor_plot()
    pl2=metallization_plot()
    rho=Rho()
    rho.fixed_freq_max=2000.0*rho.f0
    pl3=rho.plot_alpha() #auto_xlim=False, x_min=0, x_max=20)
    pl4=rho.plot_surface_charge(auto_xlim=False, x_min=-3, x_max=3, auto_ylim=False, y_min=-3e-12, y_max=3e-12)
    pl5=rho.plot_surface_voltage(auto_xlim=False, x_min=-3, x_max=3)
    pl6=line(rho.surface_x[2000:-500], rho.surface_voltage[2000:-500]+rho.surface_voltage[500:-2000]+rho.surface_voltage[2500:],
         pl="superposition", auto_xlim=False, x_min=-3, x_max=3)
    pl6.xlabel="x/center wavelength"
    pl6.ylabel="surface voltage"
    from taref.physics.idt import metallization_couple, metallization_Lamb, couple_comparison, Lamb_shift_comparison, hilbert_check
    pl7=metallization_couple()
    pl8=metallization_Lamb()
    pl9=couple_comparison()
    pl10=Lamb_shift_comparison()
    pl11=hilbert_check()
    a.save_plots([pl0, pl1, pl2, pl3, pl4, pl5, pl6, pl7, pl8, pl9, pl10, pl11])
    pl1.show()

    from taref.physics.qdt import anharm_plot
    print qdt.max_coupling
    #anharm_plot2(qdt)#.show()

    #coupling_plot()#.show()
    mag_theory(qdt).show()
    phase_theory(qdt)#.show()
    S13_mag_theory(qdt)#.show()
    S13_phase_theory(qdt).show()

#        dd.line_plot("asdf", fw0/1e9, calc_Coupling(fw0)/1e9, label=r"$G_a/2C$", color="blue")
#        dd.line_plot("asdfd", fw0/1e9, calc_Lamb_shift(fw0)/1e9, label=r"$-B_a/2C$", color="red")
#        dd.line_plot("listen", fw0/1e9, listen_coupling(fw0)/4/1e9, label=r"$G_a^{IDT}/2C^{IDT}/4$", color="green")

#class TransTimeLyzer(Lyzer):
#    f_ind=Int()
#    t_ind=Int()
#    t_start_ind=Int(63)
#    t_stop_ind=Int(77)
#
#    time=Array().tag( plot=True, label="Time", sub=True)
#    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")
#
#    @tag_Property( plot=True, sub=True)
#    def MagAbs(self):
#        print self.frequency[self.f_ind]
#        return absolute(self.Magcom[:, self.f_ind, :].transpose())#-mean(self.Magcom[:, 99:100, self.pind].transpose(), axis=1, keepdims=True))
#
#    #@tag_Property( plot=True, sub=True)
#    #def MagAbsTime(self):
#    #    return absolute(mean(self.Magcom[self.t_start_ind:self.t_stop_ind, :, :], axis=0).transpose())
#    @tag_Property(plot=True, sub=True)
#    def MagAbsFilt(self):
#        return 10.0**((20.0*log10(absolute(self.MagcomFilt))-self.probe_pwr)/20.0)#/(self.probe_pwr*dBm)
#
#    @tag_Property(plot=True, sub=True)
#    def MagcomFilt(self):
#        return mean(self.Magcom[self.t_start_ind:self.t_stop_ind, :, :], axis=0)#/(self.probe_pwr*dBm)#.transpose()
#
#    def read_data(self):
#        with File(self.rd_hdf.file_path, 'r') as f:
#            self.probe_pwr=f["Instrument config"]["Anritsu 68377C Signal generator - GPIB: 8, Pump3 at localhost"].attrs["Power"]
#
#            print f["Traces"].keys()
#            self.comment=f.attrs["comment"]
#            print f["Data"]["Channel names"][:]
#            Magvec=f["Traces"]["TA - LC Trace"]
#            #Magvec=f["Traces"]["Digitizer2 - Trace"]#[:]
#            data=f["Data"]["Data"]
#            print shape(data)
#            self.frequency=data[:,0,0].astype(float64)
#            self.yoko=data[0,1,:].astype(float64)
#            print self.frequency
#            tstart=f["Traces"]['TA - Trace_t0dt'][0][0]
#            tstep=f["Traces"]['TA - Trace_t0dt'][0][1]
#            print shape(Magvec)
#            sm=shape(Magvec)[0]
#            sy=shape(data)
#            s=(sm, sy[0], sy[2])
#            print s
#            Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
#            Magcom=reshape(Magcom, s, order="F")
#            self.time=linspace(tstart, tstart+tstep*(sm-1), sm)
#            print shape(Magcom)
#            Magcom=squeeze(Magcom)
#            self.Magcom=Magcom[:]#.transpose()
#            print shape(self.Magcom)
#
#    def magabs_colormesh(self, plotter=None):
#        plotter.colormesh("magabs", self.time*1e6, self.yoko, self.MagAbs)
#        plotter.xlabel="Time (us)"
#        plotter.ylabel="Magnitude (abs)"
#        plotter.title="Reflection vs time"
#        plotter.set_ylim(min(self.yoko), max(self.yoko))
#        plotter.set_xlim(min(self.time)*1e6, max(self.time)*1e6)
#        plotter.xlabel="Yoko (V)"
#        plotter.ylabel="Frequency (Hz)"
#        plotter.title="Magabs fluxmap {}".format(self.name)
#
#    def filt_compare(self, ind, plotter=None):
#        #plotter.line_plot("magabs_{}".format(self.name), self.frequency, self.MagAbs[:, ind], label="MagAbs (unfiltered)")
#        plotter.line_plot("magabs_{}".format(self.name), self.frequency, self.MagAbsFilt[:, ind], label="MagAbs (time)")
#
##    def magabstime_colormesh(self, plotter=None):
##        if plotter is None:
##            plotter=self.plotter
##        plotter.colormesh("magabs", self.frequency, self.yoko, self.MagAbsTime)
##        plotter.xlabel="Time (us)"
##        plotter.ylabel="Magnitude (abs)"
##        plotter.title="Reflection vs time"
#
#if __name__=="__main__":
#    print get_tag(qdt, "a", "unit")
#    print qdt.latex_table()
#    from taref.physics.fundamentals import sinc, sinc_sq,e
#    print e
#    b=Plotter()
#    from numpy import linspace, pi, absolute, sqrt
#    freq=linspace(1e9, 10e9, 1000)
#    #qdt.ft="single"
#    #qdt.get_member("mult").reset(qdt)
#    #qdt.get_member("lbda0").reset(qdt)
#
#    print qdt.f0, qdt.G_f0
#    if 0:
#        G_f=(1.0/sqrt(2.0))*0.5*qdt.Np*qdt.K2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-qdt.f0)/qdt.f0))
#        b.line_plot("sinc", freq, G_f, label="sinc/sqrt(2)")
#        G_f=0.5*qdt.Np*qdt.K2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-qdt.f0)/qdt.f0))
#        b.line_plot("sinc2", freq, G_f, label="sinc")
#        G_f=0.5*qdt.Np*qdt.K2*qdt.f0*sinc_sq(qdt.Np*pi*(freq-qdt.f0)/qdt.f0)
#        b.line_plot("sinc_sq", freq, G_f, label="sinc_sq")
#        b.vline_plot("listen", 4.475e9, alpha=0.3, color="black")
#        b.vline_plot("listent", 4.55e9, alpha=0.3, color="black")
#        b.vline_plot("listenb", 4.4e9, alpha=0.3, color="black")
#    if 0:
#        freq=4.475e9
#        f0=linspace(5e9, 6e9, 1000)
#        G_f=(1.0/sqrt(2.0))*0.5*qdt.Np*qdt.K2*f0*absolute(sinc(qdt.Np*pi*(freq-f0)/f0))
#        b.line_plot("sinc", f0, G_f, label="sinc/sqrt(2)")
#        G_f=0.5*qdt.Np*qdt.K2*f0*absolute(sinc(qdt.Np*pi*(freq-f0)/f0))
#        b.line_plot("sinc2", f0, G_f, label="sinc")
#        G_f=0.5*qdt.Np*qdt.K2*f0*sinc_sq(qdt.Np*pi*(freq-f0)/f0)
#        b.line_plot("sinc_sq", f0, G_f, label="sinc_sq")
#        b.vline_plot("theory", 5.45e9, alpha=0.3, color="black", label="theory")
#        #b.vline_plot("listent", 4.55e9, alpha=0.3, color="black")
#        #b.vline_plot("listenb", 4.4e9, alpha=0.3, color="black")
#
#    if 1:
#        from numpy import pi, linspace, sin, amax, argmin, argmax, cos
#        from scipy.constants import h
#        Np=qdt.Np
#        f0=5.45e9
#        w0=2*pi*f0
#        #qdt.Dvv=0.001
#        vf=3488.0
#        freq=linspace(1e9, 10e9, 1000)
#        print qdt.flux_factor, qdt.offset, qdt.Ejmax/h, qdt.Ec/h
#        def flux_to_Ej(voltage,  offset=qdt.offset, flux_factor=qdt.flux_factor, Ejmax=qdt.Ejmax):
#            flux_over_flux0=(voltage-offset)*flux_factor
#            Ej=Ejmax*absolute(cos(pi*flux_over_flux0))
#            return Ej
#
#        def calc_Lamb_shift(fq, Dvv=qdt.Dvv):
#            epsinf=qdt.epsinf
#            W=qdt.W
#
#            wq=2.0*pi*fq#print wq
#
#            X=Np*pi*(wq-w0)/w0
#            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#            C=sqrt(2.0)*Np*W*epsinf
#            #Ga=Ga0*(sin(X)/X)**2.0
#            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#            return -Ba/(2.0*C)/(2.0*pi)
#
#        def calc_Coupling(fqq, Dvv=qdt.Dvv):
#            epsinf=qdt.epsinf
#            W=qdt.W
#
#            wq=2.0*pi*fqq#print wq
#
#            X=Np*pi*(wq-w0)/w0
#            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#            C=sqrt(2.0)*Np*W*epsinf
#            Ga=Ga0*(sin(X)/X)**2.0
#            #Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#            return Ga/(2.0*C)/(2.0*pi)
#
#        def energy_levels(EjdivEc, Ec=qdt.Ec, Dvv=qdt.Dvv):
#            print Ec/h
#            Ec=Ec
#            Ej=EjdivEc*Ec
#            w0n=sqrt(8.0*Ej*Ec)/h*(2.0*pi)
#            #epsinf=qdt.epsinf
#            #W=qdt.W
#            #Dvv=qdt.Dvv
#            E0p =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0#-Ba/(2.0*C)*0.5 #(n +1/2)
#
#            E1p =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)# -Ba/(2.0*C)*1.5
#
#            E2p =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)#-Ba/(2.0*C)*2.5
#            E3p =  sqrt(8.0*Ej*Ec)*3.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)#-Ba/(2.0*C)*3.5
#
#            E0p=E0p/h
#            E1p=E1p/h
#            E2p=E2p/h
#            E3p=E3p/h
#            #fq=sqrt(8.0*Ej*Ec)
#            #wq=2.0*pi*fq#print wq
#
#            #X=Np*pi*(wq-w0)/w0
#            #Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#            #C=sqrt(2.0)*Np*W*epsinf
#            #Ga=Ga0*(sin(X)/X)**2.0
#            #Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#
#            #E10=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-Ec/(1.0+Ba/(wq*C))
#            #E21=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-2.0*Ec/(1.0+Ba/(wq*C))
#            #return E10/h, (E21+E10)/h/2.0
#            #E_{tot}=-E_J+\sqrt{8E_J E_C}(n +1/2)-(B_a/2C)(n +1/2)-\dfrac{E_C}{12}(6n^2+6n+3)
#            E0 =  E0p#+calc_Lamb_shift(E0p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0-Ba/(2.0*C)*0.5 #(n +1/2)
#
#            E1 =  E1p+calc_Lamb_shift(E1p-E0p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0) -Ba/(2.0*C)*1.5
#
#            E2 =  E2p+calc_Lamb_shift(E2p-E1p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)-Ba/(2.0*C)*2.5
#            E3 =  E3p+calc_Lamb_shift(E3p-E2p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*3.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)-Ba/(2.0*C)*3.5
#            return E0, E1, E2, E3, E0p, E1p, E2p, E3p, w0n
#            return (E1-E0)/h, (E2-E1)/h#/3.0
#            #return qdt._get_fq(Ej, qdt.Ec)
#
#        EjdivEc=linspace(0.001, 300, 3000).astype(float64)
#        Ejmax=qdt.Ejmax
#        E0,E1,E2,E3, E0p, E1p, E2p, E3p, w0n=energy_levels(EjdivEc, Ec=qdt.Ec, Dvv=qdt.Dvv)
#
#        b.line_plot("E0", EjdivEc, E0, label="E0")
#        b.line_plot("E1", EjdivEc, E1, label="E1")
#        b.line_plot("E2", EjdivEc, E2, label="E2")
#        b.line_plot("E3", EjdivEc, E3, label="E3")
#
#        DEP=E1p-E0p
#        d=Plotter(fig_height=5.0, fig_width=7.0)
#        #Plotter(name="anharm")
#        d.line_plot("E0", E1p-E0p, (E2-E1)-(E1-E0)-((E2p-E1p)-(E1p-E0p)), label="E0")
#        d.line_plot("E1", E1p-E0p, E1-E0-(E1p-E0p), label="E1")
#        d.line_plot("E2", E1p-E0p, E2-E1-(E2p-E1p), label="E2")
#        #d.line_plot("E3", EjdivEc, E3, label="E3")
#        #E0,E1,E2,E3=energy_levels(EjdivEc, Dvv=0.0)
#
#        b.line_plot("E0p", EjdivEc, E0p, label="E0p")
#        b.line_plot("E1p", EjdivEc, E1p, label="E1p")
#        b.line_plot("E2p", EjdivEc, E2p, label="E2p")
#        b.line_plot("E3p", EjdivEc, E3p, label="E3p")
#
#        #d.line_plot("E0p", EjdivEc, (E2p-E1p)-(E1p-E0p), label="E0p")
#        #d.line_plot("E1p", E1p-E0p, (E2p-E1p)-DEP, label="E1p")
#        #d.line_plot("E2p", E1p-E0p, E3p-E2p, label="E2p")
#        #b.show()
#        yo = linspace(-2.0, 2.0, 2000)
#        Ej=flux_to_Ej(yo, Ejmax=Ejmax)
#        EjdivEc=Ej/qdt.Ec
#        E0,E1,E2,E3, E0p, E1p, E2p, E3p, w0n=energy_levels(EjdivEc, Dvv=qdt.Dvv)
#        Gamma10=calc_Coupling(E1-E0)
#        Gamma20=calc_Coupling((E2-E0)/2.0)
#        #d.scatter_plot("blah", E1-E0, Gamma10, label="E_{10}")
#        #d.scatter_plot("lbs", (E2-E0)/2.0, Gamma20, label="E_{20}/2")
#        fw0=linspace(4e9, 7e9, 2000) #E1-E0 #sqrt(8*Ej*qdt.Ec)/h
#        d.line_plot("asdf", fw0/1e9, calc_Coupling(fw0)/1e9, label=r"$G_a/2C$", color="blue")
#        d.line_plot("asdfd", fw0/1e9, calc_Lamb_shift(fw0)/1e9, label=r"$-B_a/2C$", color="red")
#        d.legend()
#
#        d.mpl_axes.xlabel="Frequency (GHz)"
#        d.mpl_axes.ylabel="Frequency (GHz)"
#        d.set_ylim(-1.0, 1.5)
#        #dd.set_xlim(4.2, 5.0)
#        #d.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_Ba.pdf")
#        #d.show()
#
#
#        dd=Plotter(fig_height=7.0, fig_width=7.0)
#        def listen_coupling(f_listen, Dvv=qdt.Dvv):
#            epsinf=qdt.epsinf
#            W=qdt.W
#            w=2.0*pi*f_listen
#            Np=36
#            f0=idt.f0
#            print f0 #4.5e9
#            w0=2*pi*f0
#            X=Np*pi*(w-w0)/w0
#            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#            C=sqrt(2.0)*Np*W*epsinf
#            Ga=Ga0*(sin(X)/X)**2.0
#            #Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#            return Ga/(2.0*C)/(2.0*pi)
#
#        dd.line_plot("asdf", fw0/1e9, calc_Coupling(fw0)/1e9, label=r"$G_a/2C$", color="blue")
#        dd.line_plot("asdfd", fw0/1e9, calc_Lamb_shift(fw0)/1e9, label=r"$-B_a/2C$", color="red")
#        dd.line_plot("listen", fw0/1e9, listen_coupling(fw0)/4/1e9, label=r"$G_a^{IDT}/2C^{IDT}/4$", color="green")
#        dd.plot_dict["listen"].mpl.linestyle="dashed"
#        dd.legend()
#        #dd.set_ylim(-1.0, 1.5)
#        #dd.set_xlim(min(self.yoko), max(self.yoko))
#        dd.mpl_axes.xlabel="Frequency (GHz)"
#        dd.mpl_axes.ylabel="Frequency (GHz)"
#        #dd.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_all.pdf")#, format="eps")
#        dd.set_ylim(-0.01, 0.1)
#        dd.set_xlim(4.2, 5.0)
#        #dd.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_all_zoom.pdf")#, format="eps")
#
#        #dd.show()
#        #plotter.mpl_axes.title="MagdB fluxmap {}".format(self.name)
#        #Plotter().line_plot("asdf", yo, fw0+calc_Lamb_shift(fw0))
#
#        def R_lor(f_listen, fqq, w0n1, Dvv=qdt.Dvv):
#            w=2*pi*f_listen
#            epsinf=qdt.epsinf
#            W=qdt.W
#            X=Np*pi*(f_listen-f0)/f0
#            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#            C=sqrt(2.0)*Np*W*epsinf
#            Ga=Ga0*(sin(X)/X)**2.0
#            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#            w0nn=2*pi*fqq#w0n1#-Ba/(2.0*C)
#            Gamma=calc_Coupling(fqq, Dvv=Dvv)
#            L=1/(C*(w0nn**2.0))
#            return  Ga/(Ga+1.0j*Ba+1.0j*w*C+1.0/(1.0j*w*L))
#            #return -2Gamma10*(gamma10-idw)/(4*(gamma10*2+dw**2)) #+Gamma10*Gamma21*(gamma20+idw)*0
#            #return 1-2*Gamma10/(2*(gamma10-1.0j*dw)+(OmegaC**2)/(2*gamma20-2j*(dw+dwc)))
#            return -Gamma/(Gamma+1.0j*(w-w0nn))
##        def R_full(f_listen=4.3e9, fq=5.0e9, fq2=6.0e9):
##
##
##            w_listen=2*pi*f_listen
##            epsinf=qdt.epsinf
##            W=qdt.W
##            Dvv=qdt.Dvv
##            w0=2*pi*f0
##
##
##            X=Np*pi*(f_listen-f0)/f0
##            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
##            C=sqrt(2.0)*Np*W*epsinf
##            Ga=Ga0*(sin(X)/X)**2.0
##            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
##
##            wq=2.0*pi*fq
##            wq2=2.0*pi*fq2
##
##            L=1/(C*(wq**2.0))
##            L2=1/(C*(wq2**2.0))
##
##            Gamma=Ga/(2.0*C)
##            #return 1.0/(1.0 +1.0j*(w_listen-wq)/Gamma), 1.0/(1.0 +1.0j*(w_listen-wq2)/Gamma)
##            return Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L)), Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L2))
#
#
#        temp=[]
#        t2=[]
#        qfreq=[]
#        for f in freq:
#            Gamma=calc_Coupling(E1-E0)
#            w0nn=2*pi*(E1p-E0p)
#            w=2*pi*f
#            #R1=-Gamma/(Gamma+1.0j*(w-w0nn))
#            R1=R_lor(f, E1p-E0p, w0n)
#            #Gamma=calc_Coupling((E2p-E0p)/2.0)
#            #w0nn=2*pi*(E2p-E0p)/2.0
#            #R2=-Gamma/(Gamma+1.0j*(w-w0nn))
#            anharm=(E2-E1)-(E1-E0)
#            R2=R_lor(f, E1p-E0p+anharm/2.0, w0n)
#            #R1, R2=R_full(f, E1-E0, (E2-E0)/2.0)
#            #qfreq.append(freq[argmax(R)])
#            #imax=argmax(R)
#            #print imax
#            #f1=fq[argmin(absolute(fq-f))]
#            #f2=freq[argmin(absolute(R[imax:-1]-0.5))]
#            t2.append(R2)
#            temp.append(R1)
#        temp=array(temp)
#        #b.line_plot("coup", freq, t2)
#        c=Plotter()
#        g=Plotter()
#        c.colormesh("R_full", yo, freq, 10*log10(absolute(temp)+absolute(t2)))
#        g.colormesh("R_full", yo, freq, absolute(temp))
#        h=Plotter()
#        h.colormesh("R_full", yo, freq, absolute(t2))
#
#
#        #g.colormesh('R_angle', yo, freq, angle(temp))        #b.line_plot("Ba", freq, t2)
#        #b.line_plot("Ga", freq, temp)
#        b.show()
#
#    if 0:
#        from numpy import pi, linspace, sin, amax, argmin, argmax, cos
#        from scipy.constants import h
#        Np=qdt.Np
#        f0=5.45e9
#        w0=2*pi*f0
#
#        vf=3488.0
#        freq=linspace(0.0001e9, 15e9, 2000)
#        print qdt.flux_factor, qdt.offset, qdt.Ejmax/h, qdt.Ec/h
#        def flux_par(w_listen, voltage, offset=qdt.offset, flux_factor=qdt.flux_factor, Ejmax=qdt.Ejmax, Ec=qdt.Ec):
#            flux_over_flux0=(voltage-offset)*flux_factor
#            Ej=Ejmax*absolute(cos(pi*flux_over_flux0))
#            epsinf=qdt.epsinf
#            W=qdt.W
#            Dvv=qdt.Dvv
#            fq=sqrt(8.0*Ej*Ec)/h
#            wq=2.0*pi*fq#print wq
#
#            X=Np*pi*(wq-w0)/w0
#            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#            C=sqrt(2.0)*Np*W*epsinf
#            #Ga=Ga0*(sin(X)/X)**2.0
#            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#
#            E10=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-Ec/(1.0+Ba/(wq*C))
#            E21=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-2.0*Ec/(1.0+Ba/(wq*C))
#            return E10/h, (E21+E10)/h/2.0
#            E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
#            E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
#            E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
#            E3 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)
#
#            return (E1-E0)/h, (E2-E0)/h#/3.0
#            #return qdt._get_fq(Ej, qdt.Ec)
#
#        def R_full(f_listen=4.3e9, voltage=0.001):
#
#
#            w_listen=2*pi*f_listen
#            epsinf=qdt.epsinf
#            W=qdt.W
#            Dvv=qdt.Dvv
#            w0=2*pi*f0
#
#
#            X=Np*pi*(f_listen-f0)/f0
#            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#            C=sqrt(2.0)*Np*W*epsinf
#            Ga=Ga0*(sin(X)/X)**2.0
#            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#
#            #C_prime=Ba/w_listen+C
#            #Ec_prime=e**2/(2.0*C_prime)
#            #BadwC=Ba/(w_listen*C)
#            fq, fq2=flux_par(w_listen, voltage, offset=0.0, flux_factor=0.2945, Ejmax=qdt.Ejmax, Ec=qdt.Ec)
#            wq=2.0*pi*fq
#            wq2=2.0*pi*fq2
#
#            L=1/(C*(wq**2.0))
#            L2=1/(C*(wq2**2.0))
#
#            #Lc=5000.0
#            #Qi=pi*5000.0/(vf/f0*(1-0.999))
#            #Qe=1.0/(5.74*vf*50.0*epsinf*W*Dvv*2)*5000.0/36**2
#
#            #r=((Qe-Qi)+2j*Qi*Qe*(fq2-f0)/f0)/((Qe+Qi)+2j*Qi*Qe*(fq2-f0)/f0)
#
#            #w2=Ecprime
#
#            #b.line_plot("Ba", f_listen, Ba)
#            #b.line_plot("Ga", f_listen, Ga)
#            #return Ba/(2*C*2*pi), Ga/(2*C*2*pi)
#            #print Ga, Ba, w_listen*C
#            return fq, Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L))+Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L2))
#        #R=Ga/(Ga+1j*w_listen*C+1/(1j*w_listen*L))
#            #b.line_plot("semiclassical", fq, absolute(R)**2, label=str(f_listen))
#        #b.line_plot("semiclassical", fq, Ba)
#
#        temp=[]
#        t2=[]
#        qfreq=[]
#        yo = linspace(-5.0, 5.0, 1000)
#        #yo=yo[328:500]
#        #fq=array([flux_par(yn)[0] for yn in yo])
#        #fq2=array([flux_par(yn)[1] for yn in yo])
#
#        for f in freq:
#                #X2=36*pi*(f-4.4e9)/4.4e9
#                #wrap=(sin(X2)/X2)**2
#            fq, R=R_full(f, yo)
#            #qfreq.append(freq[argmax(R)])
#            #imax=argmax(R)
#            #print imax
#            #f1=fq[argmin(absolute(fq-f))]
#            #f2=freq[argmin(absolute(R[imax:-1]-0.5))]
#            t2.append(fq)
#            temp.append(R)
#        temp=array(temp)
#        #b.line_plot("coup", freq, t2)
#        d=Plotter()
#        #b.line_plot("Ba", freq, t2)
#        #b.line_plot("Ga", freq, temp)
#
#        b.colormesh("R_full", yo, freq, 10*log10(absolute(temp)))
#        d.colormesh('R_angle', yo, freq, angle(temp))
#
#        #fft.ifft(418, 328, 500)
#        def ifft_plot(name, plotter, Magcom, ind):
#            plotter.line_plot("ifft_{}".format(name), absolute(fft.ifft(Magcom[:,ind])), label="ifft_{}".format(name))
#
#
#        c=Plotter()
#        #c.line_plot('R_angle', yo, t2)
#
#        #c.line_plot("cross_sections1", yo, t2)#, label="{:.3f}V".format(yo[500]))
#
#        #c.line_plot("cross_sections1", freq, 10*log10(absolute(temp[:, 500])), label="{:.3f}V".format(yo[500]))
#        #c.line_plot("cross_sections2", freq, 10*log10(absolute(temp[:, 428])), label="{:.3f}V".format(yo[428]))
#        #c.line_plot("cross_sections3", freq, 10*log10(absolute(temp[:, 401])), label="{:.3f}V".format(yo[401]))
#        #c.line_plot("cross_sections4", freq, 10*log10(absolute(temp[:, 385])), label="{:.3f}V".format(yo[385]))
#        #c.line_plot("cross_sections5", freq, 10*log10(absolute(temp[:, 380])), label="{:.3f}V".format(yo[380]))
#        #c.line_plot("cross_sections6", freq, 10*log10(absolute(temp[:, 368])), label="{:.3f}V".format(yo[368]))
#
#        q=Plotter()
#        #q.line_plot("cross_sections1", freq, angle(temp[:, 500]), label="{:.3f}V".format(yo[500]))
#        #q.line_plot("cross_sections2", freq, angle(temp[:, 428]), label="{:.3f}V".format(yo[428]))
#        #q.line_plot("cross_sections3", freq, angle(temp[:, 401]), label="{:.3f}V".format(yo[401]))
#        #q.line_plot("cross_sections4", freq, angle(temp[:, 385]), label="{:.3f}V".format(yo[385]))
#        #q.line_plot("cross_sections5", freq, angle(temp[:, 380]), label="{:.3f}V".format(yo[380]))
#        #q.line_plot("cross_sections6", freq, angle(temp[:, 368]), label="{:.3f}V".format(yo[368]))
#
#
#        #ifft_plot(328, c, temp, 328)
#        #ifft_plot(418, c, temp, 418)
#        #ifft_plot(500, c, temp, 500)
#        def fft_filter(mg, n):
#            myifft=fft.ifft(mg[:,n])
#            #myifft[16:-16]=0.0
#            #if self.filt_start_ind!=0:
#            myifft[:11]=0.0
#            myifft[-11:]=0.0
#            return fft.fft(myifft)
#        #t2=array([fft_filter(temp, n) for n in range(len(yo))])
#        #b.colormesh("R_filt",# yo[328:500], freq[::4],
#        #absolute(t2[328:500, :]))
#        #R_full(4.2500001e9)
#        #R_full(4.3000001e9)
#        #R_full(4.3500001e9)
#        #fq=linspace(4e9, 5e9, 1000)
#        #X=Np*pi*(fq-f0)/f0
#        #Ga=(sin(X)/X)**2.0
#        #Ba=(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#        #b.line_plot("Ga", fq, Ga)
#        #b.line_plot("Ba", fq, Ba)
#        #sqrt(1/(C))/2*p
#        #b.line_plot("semiclassical", fq, absolute(R)/amax(absolute(R)))
#    #b.show()
#    qdt.show()
