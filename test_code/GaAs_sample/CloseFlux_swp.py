# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:46:49 2016

@author: thomasaref
"""

from GaAs_fundamental import GaAs_Read, GaAs_Fund, qdt, h
from atom.api import Typed, Unicode, Float, observe, FloatRange
from h5py import File
from taref.core.universal import Array
from numpy import float64, linspace, shape, reshape, squeeze, mean, angle, absolute, pi, exp, tile
from taref.core.atom_extension import tag_Property
from taref.physics.units import dB
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from taref.core.agent import Operative

class Fitter(Operative):
     offset=FloatRange(-1.0, 1.0, qdt.offset+0.0018).tag(tracking=True)
     flux_factor=FloatRange(0.01, 1.0, qdt.flux_factor).tag(tracking=True) #0.299

     @tag_Property(plot=True, private=True)
     def flux_parabola(self):
        flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_over_flux0)
        return qdt._get_fq(Ej, qdt.Ec)
         #return qdt.flux_parabola(voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)

     yoko=Array().tag(unit="V", plot=True, label="Yoko", private=True)

     plotter=Typed(Plotter).tag(private=True)

     @observe("offset", "flux_factor")
     def update_plot(self, change):
         if change["type"]=="update":
             self.get_member("flux_parabola").reset(self)
             self.plotter.plot_dict["flux_parabola"].clt.set_ydata(self.flux_parabola)
             self.plotter.draw()

class Lyzer(GaAs_Fund):
    rd_hdf=Typed(GaAs_Read)

    comment=Unicode().tag(read_only=True, spec="multiline")

    rt_atten=Float(60)

    rt_gain=Float(23*2)

    frequency=Array().tag(unit="GHz", plot=True, label="Frequency")
    yoko=Array().tag(unit="V", plot=True, label="Yoko")
    Magcom=Array().tag(private=True)
    Magcom2=Array().tag(private=True)

    probe_frq=Float().tag(unit="GHz", label="Probe frequency", read_only=True)
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")



    @tag_Property(display_unit="dB", plot=True)
    def MagdB(self):
        return self.Magcom[:, :]/dB

    @tag_Property(plot=True)
    def Phase(self):
        return absolute(self.Magcom2)
        return angle(self.Magcom)#-mean(self.Magcom[:, 297:303], axis=1, keepdims=True))

    @tag_Property( plot=True)
    def MagAbs(self):
        #return absolute(self.Magcom[:, :])
        return absolute(self.Magcom)#-mean(self.Magcom[:, 0:1], axis=1, keepdims=True))


    def _default_rd_hdf(self):
        return GaAs_Read(main_file="S11_close_flux/meas.h5")

    def read_data(self):
        S11_offset = -31.2
        with File(self.rd_hdf.file_path, 'r') as f:
            print f.keys()
            print f["mag"].keys()
            self.frequency=f["mag"]["Frequency"][:]

            self.yoko=f["mag"]["Yoko voltage"][:]
            Magvec=f["mag"]["Mag"][:]
            phase=f["phase"]["Phase"][:]
            zfm_phase = phase*pi/180
            zfm_S11_dB = Magvec - S11_offset
            zfm_S11_amp = 10.0**(zfm_S11_dB/20.0)
            zfm_S11_complex = zfm_S11_amp*exp(1.0j*zfm_phase)
            self.Magcom=zfm_S11_complex
            self.Magcom2=zfm_S11_complex[:]
            self.comment=f.attrs["comment"]
        with File(self.rd_hdf.folder.dir_path+self.rd_hdf.folder.divider+"referencequbitoffres.h5", "r") as f:
            Magoff=f["mag"]["Mag"][:]
            phase_off=f["phase"]["Phase"][:]
            zfm_detuned_phase = phase_off*pi/180
            zfm_detuned_S11_dB = Magoff - S11_offset
            zfm_detuned_S11_amp = 10.0**(zfm_detuned_S11_dB/20.0)
            zfm_detuned_S11_complex = mean(zfm_detuned_S11_amp*exp(1.0j*zfm_detuned_phase), axis=1)
            #self.Magcom=zfm_detuned_S11_complex
            self.Magcom=self.Magcom-tile(zfm_detuned_S11_complex, (len(self.yoko), 1)).transpose()
            bg=(mean(self.Magcom2[:, 0:1], axis=1, keepdims=True)+mean(self.Magcom2[:, 239:240], axis=1, keepdims=True))/2.0
            self.Magcom2=self.Magcom2-bg #mean(self.Magcom[:, 0:1], axis=1, keepdims=True)





if __name__=="__main__":
    a=Lyzer()
    a.read_data()
    c=Fitter()
    c.yoko=a.yoko[:]
    b=Plotter()
    def magdB_colormesh():
        b.colormesh("magdB", a.yoko, a.frequency, a.MagdB)
        #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        b.set_ylim(4.803e9, 4.810e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    def magabs_colormesh():
        b.colormesh("magabs", a.yoko, a.frequency, a.MagAbs)
        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        b.set_ylim(4.803e9, 4.810e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"
    c.plotter=b

    def phase_colormesh():
        b.colormesh("phase", a.yoko, a.frequency, a.Phase)
        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        b.set_ylim(4.4e9, 4.5e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    def magabs_cs():
        #b.line_plot("bg", a.Phase)
        b.line_plot("magabs_cs", c.flux_parabola, mean(a.MagAbs[104:106, :], axis=0))
        #b.line_plot("magabs2", c.flux_parabola, mean(a.Phase[104:106, :], axis=0))
        #b.line_plot("magabs_cs", c.flux_parabola, a.MagAbs[105, :])
        #b.line_plot("magabs_cs", c.flux_parabola, a.MagAbs[106, :])

        #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)

    magabs_cs()
    #magabs_colormesh()
    #phase_colormesh()
    #magdB_colormesh()
    shower(b)


