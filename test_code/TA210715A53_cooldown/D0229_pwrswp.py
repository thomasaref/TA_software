# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:46:49 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_Read, TA53_Fund, qdt, idt
from atom.api import Typed, Unicode, Float, observe, FloatRange, Int
from h5py import File
from taref.core.universal import Array
from numpy import float64, linspace, shape, reshape, squeeze, mean, angle, absolute, sqrt, cos, pi, log10
from taref.core.atom_extension import tag_Property
from taref.physics.units import dB
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from taref.core.agent import Operative
from taref.physics.fundamentals import hbar, e

class Fitter(Operative):
     offset=FloatRange(-1.0, 1.0, qdt.offset).tag(tracking=True)
     flux_factor=FloatRange(0.01, 1.0, qdt.flux_factor).tag(tracking=True)
     extra_atten=FloatRange(0.0, 30.0, 0.0).tag(tracking=True)
     #pwr=Array()

     @tag_Property(plot=True, private=True)
     def PdBm_from_Ic(self):
         flux_over_flux0=(a.yoko-self.offset)*self.flux_factor
         Ej=qdt.Ejmax*absolute(cos(pi*flux_over_flux0))
         I=Ej*(2.0*e)/hbar
         mu_q=0.8*qdt.K2*qdt.Np
         gm=2*mu_q*qdt.W*qdt.epsinf*2*pi*qdt.f0/qdt.K2
         phi=I/gm #=gm*phi

         mu=0.8*qdt.K2*idt.Np
         V=phi/mu
         Pwatts=(V**2)/50.0
         PdBm=10.0*log10(Pwatts/0.001)+self.extra_atten
         return PdBm
         #pwr=a.pwr-a.rt_atten-a.fridge_atten
         #Pwatts=0.001*10.0**(pwr/10.0)
         #V=sqrt(Pwatts*50.0)







     @tag_Property(plot=True, private=True)
     def flux_parabola(self):
        flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_over_flux0)
        return qdt._get_fq(Ej, qdt.Ec)
         #return qdt.flux_parabola(voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)

     yoko=Array().tag(unit="V", plot=True, label="Yoko", private=True)

     plotter=Typed(Plotter).tag(private=True)

     @observe("offset", "flux_factor", "extra_atten")
     def update_plot(self, change):
         if change["type"]=="update":
             if "flux_parabola" in self.plotter.plot_dict:
                 self.get_member("flux_parabola").reset(self)
                 self.plotter.plot_dict["flux_parabola"].clt.set_ydata(self.flux_parabola)
             if "PdBm_from_Ic" in self.plotter.plot_dict:
                 self.get_member("PdBm_from_Ic").reset(self)
                 self.plotter.plot_dict["PdBm_from_Ic"].clt.set_ydata(self.PdBm_from_Ic)
             self.plotter.draw()

     #powind=Int(1)

     #def _observe_powind(self, change):
     #   if change["type"]=="update":
     #       a.powind=self.powind
     #       a.get_member("MagAbs").reset(a)
     #       if "magabs" in b.plot_dict:
     #           b.plot_dict["magabs"].clt.set_array(a.MagAbs)

class Lyzer(TA53_Fund):
    rd_hdf=Typed(TA53_Read)

    comment=Unicode().tag(read_only=True, spec="multiline")

    rt_atten=Float(20)

    rt_gain=Float(23*2)

    frequency=Array().tag(unit="GHz", plot=True, label="Frequency")
    yoko=Array().tag(unit="V", plot=True, label="Yoko")
    Magcom=Array().tag(private=True)
    pwr=Array()

    probe_frq=Float().tag(unit="GHz", label="Probe frequency", read_only=True)
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")

    frqind=Int(222)
    powind=Int(0)


    @tag_Property(display_unit="dB", plot=True)
    def MagdB(self):
        return self.Magcom[self.frqind, :, :]/dB

    @tag_Property(plot=True)
    def Phase(self):
        return angle(self.Magcom[self.frqind, :, :])#-mean(self.Magcom[:, self.powind, 297:303], axis=1, keepdims=True))

    @tag_Property(plot=True)
    def MagAbsPow(self):
        bg=(mean(self.Magcom[:, self.powind, 0:1], axis=1, keepdims=True)+mean(self.Magcom[:, self.powind, 699:700], axis=1, keepdims=True))/2.0

        return absolute(self.Magcom[:, self.powind, :]-bg) #mean(self.Magcom[self.frqind, :, 299:300], axis=1, keepdims=True))

    @tag_Property( plot=True)
    def MagAbs(self):
        #return absolute(self.Magcom[:, :])
        bg=(mean(self.Magcom[self.frqind, :, 0:1], axis=1, keepdims=True)+mean(self.Magcom[self.frqind, :, 699:700], axis=1, keepdims=True))/2.0

        return absolute(self.Magcom[self.frqind, :, :]-bg) #mean(self.Magcom[self.frqind, :, 299:300], axis=1, keepdims=True))



    def _default_rd_hdf(self):
        return TA53_Read(main_file="Data_0229/S4A4_TA53_SC1516_pwrswp_faster.hdf5")

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            print f["Traces"].keys()
            self.comment=f.attrs["comment"]
            print f["Instrument config"].keys()
            self.probe_frq=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs["Start frequency"]
            self.probe_pwr=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs["Output power"]
            print f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs
#
            print f["Data"]["Channel names"][:]
            Magvec=f["Traces"]["RS VNA - S21"]#[:]
            data=f["Data"]["Data"]
            print shape(data)
#
            self.yoko=data[0,1,:].astype(float64)
            self.pwr=data[:,0,0].astype(float64)

            print self.yoko
            fstart=f["Traces"]['RS VNA - S21_t0dt'][0][0]
            fstep=f["Traces"]['RS VNA - S21_t0dt'][0][1]
            print shape(Magvec)
            sm=shape(Magvec)[0]
            sy=shape(data)
            s=(sm, sy[0], sy[2])
            print s
            Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
            Magcom=reshape(Magcom, s, order="F")
            self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            print shape(Magcom)
            self.Magcom=squeeze(Magcom)
            #Magabs=Magcom[:, :, :]-mean(Magcom[:, 197:200, :], axis=1, keepdims=True)

if __name__=="__main__":
    a=Lyzer()
    a.read_data()
    c=Fitter()
    c.yoko=a.yoko[:]
    b=Plotter()
    def magdB_colormesh():
        #for pwi in range(11):
        if 1:
            a.frqind=1#pwi
            a.get_member("MagdB").reset(a)
            b.colormesh("magdB {}".format(a.frequency[a.frqind]), a.yoko, a.pwr, a.MagdB)
        #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        #b.set_ylim(4.4e9, 4.5e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    def magabs_colormesh():
        b.colormesh("magabs", a.yoko, a.pwr-a.rt_atten-a.fridge_atten, a.MagAbs)
        #b.colormesh("magabs", a.yoko, a.frequency, a.MagAbsPow)

        b.line_plot("PdBm_from_Ic", a.yoko, c.PdBm_from_Ic, color="orange", alpha=0.4)
        b.set_ylim(-110, -70)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    def magabs_allcolormesh():
        for pwi in range(11):
            a.powind=pwi
            a.get_member("MagAbs").reset(a)
            b.colormesh("magabs {}".format(a.pwr[a.powind]-a.rt_atten-a.fridge_atten), a.yoko, a.frequency, a.MagAbs)
        b.line_plot("flux_parabola", a.yoko, a.flux_parabola, color="orange", alpha=0.4)
        b.set_ylim(4.4e9, 4.55e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    c.plotter=b

    def phase_colormesh():
        b.colormesh("phase", a.yoko, a.pwr, a.Phase)
        #b.line_plot("flux_parabola", c.flux_parabola, a.yoko, color="orange", alpha=0.4)
        #b.set_ylim(4e9, 5e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    def magabs_cs():
        for pwi in range(10):
            b.line_plot("magabs {}".format(a.pwr[2*pwi]), a.yoko, a.MagAbs[2*pwi, :], label="{}".format(a.pwr[2*pwi]-a.rt_atten-a.fridge_atten))




    def satatt():
        #powsat=[]
        #for pwi in range(21):
        #    a.powind=pwi
        #    a.get_member("MagAbs").reset(a)
        #    data=a.MagAbs[412, :]
        #    powsat.append(max(data)-min(data))
        b.line_plot("powsat", a.pwr[:]-a.rt_atten-a.fridge_atten, a.MagAbs[:, 412]) #a.MagAbs[280, :], label=str(a.pwr[a.powind]))

    def pow_magabs_cs():
        for pwi in range(11):
            a.powind=pwi
            a.get_member("MagdB").reset(a)
            b.line_plot("cs {}".format(a.frequency[94]), c.flux_parabola, a.MagdB[94, :], label="{}".format(a.pwr[a.powind]-a.rt_atten-a.fridge_atten))

        #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        #b.set_xlim(0, 7e9)
        #b.set_ylim(0, 0.02)

    #magdB_colormesh()
    #magabs_cs()
    #pow_magabs_cs()
    magabs_colormesh()
    #phase_colormesh()
    #magabs_allcolormesh()
    #satatt()
    shower(b)


