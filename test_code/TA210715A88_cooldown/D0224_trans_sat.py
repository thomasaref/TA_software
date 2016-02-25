# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:46:49 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read, TA88_Fund, qdt
from atom.api import Typed, Unicode, Float, observe, FloatRange
from h5py import File
from taref.core.universal import Array
from numpy import float64, linspace, shape, reshape, squeeze, mean, angle, absolute, array, log10, newaxis, amax
from taref.core.atom_extension import tag_Property
from taref.physics.units import dB, dBm
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from taref.core.agent import Operative
from taref.physics.units import h
class Fitter(Operative):
     offset=FloatRange(-1.0, 1.0, -0.015).tag(tracking=True)
     flux_factor=FloatRange(0.01, 1.0, 0.2945).tag(tracking=True)
     Ec=FloatRange(100.0, 200.0, 150.0).tag(tracking=True)

     @tag_Property(plot=True, private=True)
     def flux_parabola(self):
        flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_over_flux0)
        return qdt._get_fq(Ej, h*self.Ec*1e6)
         #return qdt.flux_parabola(voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)

     yoko=Array().tag(unit="V", plot=True, label="Yoko", private=True)

     freq=FloatRange(4.0e9, 5.0e9, 4.354e9)#
     plotter=Typed(Plotter).tag(private=True)

     @observe("offset", "flux_factor", "Ec", "freq")
     def update_plot(self, change):
         if change["type"]=="update":
             self.get_member("flux_parabola").reset(self)
             self.plotter.plot_dict["flux_1"].clt.set_xdata(self.freq)
             self.plotter.plot_dict["flux_2"].clt.set_xdata(self.freq+self.Ec*1e6)
             self.plotter.plot_dict["flux_3"].clt.set_xdata(self.freq+2*self.Ec*1e6)

             self.plotter.draw()

class Lyzer(TA88_Fund):
    rd_hdf=Typed(TA88_Read)

    comment=Unicode().tag(read_only=True, spec="multiline")

    rt_atten=Float(20)

    rt_gain=Float(26*2)

    pwr=Array().tag( plot=True, label="Time")
    yoko=Array().tag(unit="V", plot=True, label="Yoko")
    Magcom=Array().tag(private=True)

    probe_frq=Float().tag(unit="GHz", label="Probe frequency", read_only=True)
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")



    @tag_Property(display_unit="dB", plot=True)
    def MagdB(self):
        return self.Magcom[:, :]/dB-self.fridge_gain-self.rt_gain

    @tag_Property(ddisplay_unit="dB", plot=True)
    def ReldB(self):
        return self.MagdB-self.pwr

    @tag_Property(plot=True)
    def RelAbs(self):
        return 10.0**(self.ReldB/20.0)

    @tag_Property(plot=True)
    def Phase(self):
        return angle(self.Magcom[:, :])#-mean(self.Magcom[:, 297:303], axis=1, keepdims=True))

    @tag_Property( plot=True)
    def MagAbs(self):
        #return absolute(self.Magcom[:, :])
        return absolute(self.Magcom[:, :])#-mean(self.Magcom[0:1, :], axis=0, keepdims=True))


    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0224/S1A4_TA88_dig_trans_sat.hdf5")

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            print f.keys()
            print f["Data"].keys()
            #I=f["Data"][:] #["('Digitizer 1 - AvgTrace', 'Real')"]
            #Q=f["Data"][('Digitizer 1 - AvgTrace', 'Imaginary')]
            self.comment=f.attrs["comment"]
            print f["Instrument config"].keys()
            self.probe_frq=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs["Start frequency"]
            self.probe_pwr=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs["Output power"]
            print f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs.keys()
#
            print f["Data"]["Channel names"][:]
            #Magvec=f["Traces"]["Digitizer 1 - Trace"]#[:]
            data=f["Data"]["Data"]
            print shape(data)
#
            self.yoko=data[0,1,:].astype(float64)
            pwr=data[:,0,0].astype(float64)-self.fridge_atten-self.rt_atten
            self.pwr = pwr[:, newaxis]
            I=data[:, 2, :]
            Q=data[:, 3, :]
            self.Magcom=I+1j*Q

            #pwr_in=pwr/dBm

            #pwr_out=20*log10(I**2+Q**2)



            #tstart=f["Traces"]['Digitizer 1 - Trace_t0dt'][0][0]
            #tstep=f["Traces"]['Digitizer 1 - Trace_t0dt'][0][1]
            #print shape(Magvec)
            #sm=shape(Magvec)[0]
            #sy=shape(data)
            #s=(sm, sy[0], sy[2])
            #print s
            #Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
            #Magcom=reshape(Magcom, s, order="F")
            #self.time=linspace(tstart, tstart+tstep*(sm-1), sm)
            #print shape(Magcom)
            #Magcom=squeeze(Magcom)
            #self.Magcom=Magcom.transpose()

            #Magabs=Magcom[:, :, :]-mean(Magcom[:, 197:200, :], axis=1, keepdims=True)


a=Lyzer()
a.read_data()
c=Fitter()
c.yoko=a.yoko
b=Plotter()
def magdB_colormesh():
    b.colormesh("magdB", a.yoko, a.pwr, a.MagdB)
    #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
    #b.set_ylim(4.4e9, 4.5e9)
    b.xlabel="Yoko (V)"
    b.ylabel="Frequency (Hz)"
    b.title="Reflection fluxmap"

def ReldB_colormesh():
    b.colormesh("magdB", c.flux_parabola, a.pwr, a.ReldB)#-amax(a.ReldB))
    b.vline_plot("flux_1", c.freq, color="blue", alpha=0.7)
    b.vline_plot("flux_2", c.freq, color="blue", alpha=0.7)
    b.vline_plot("flux_3", c.freq, color="blue", alpha=0.7)

    #b.set_ylim(4.4e9, 4.5e9)
    b.xlabel="Yoko (V)"
    b.ylabel="Frequency (Hz)"
    b.title="Reflection fluxmap"

def Relabs_colormesh():
    b.colormesh("magabs", c.flux_parabola, a.pwr, a.RelAbs)
    #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
    #b.set_ylim(4.4e9, 4.5e9)
    b.xlabel="Time (us)"
    b.ylabel="Magnitude (abs)"
    b.title="Reflection vs time"

def magabs_colormesh():
    b.colormesh("magabs", c.flux_parabola, a.pwr, a.MagAbs)
    #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
    #b.set_ylim(4.4e9, 4.5e9)
    b.xlabel="Time (us)"
    b.ylabel="Magnitude (abs)"
    b.title="Reflection vs time"
c.plotter=b

def phase_colormesh():
    b.colormesh("phase", a.yoko, a.frequency, a.Phase)
    b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
    b.set_ylim(4e9, 5e9)
    b.xlabel="Yoko (V)"
    b.ylabel="Frequency (Hz)"
    b.title="Reflection fluxmap"

def ReldB_cs():
    b.line_plot("magabs_cs", c.flux_parabola, a.ReldB[37, :])
    b.vline_plot("flux_1", c.freq, color="red", alpha=0.5, linewidth=0.5)
    b.vline_plot("flux_2", c.freq, color="red", alpha=0.5, linewidth=0.5)
    b.vline_plot("flux_3", c.freq, color="red", alpha=0.5, linewidth=0.5)

    #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
    #b.set_xlim(0, 7e9)
    #b.set_ylim(0, 0.02)

def magabs_cs2():
    b.line_plot("magabs_cs", a.time*1e6, a.MagAbs[ 0, :], label="Off resonance")
    b.line_plot("magabs_cs2", a.time*1e6, a.MagAbs[181, :], label="On resonance")
    b.xlabel="Time (us)"
    b.ylabel="Magnitude (abs)"
    b.title="Reflection time cross section"

def time_speed():
    print qdt.vf
    t=array([8.7e-8, 2.64e-7, 3.79e-7, 4.35e-7, 6.6e-7])-8.7e-8
    b.scatter_plot("spd", t*1e6, [0.0, 600.0, 1000.0, 1200.0, 2000.0], label="Reflections")
    b.line_plot("spd_fit", t*1e6,  (t*qdt.vf)*1e6, label="t*3488")

from numpy import pi
def quest():
    df=linspace(-1.0, 1.0, 1000)
    dw=2*pi*df
    G=2*pi*0.2
    b.line_plot("quest", dw, absolute(((1.0-2.0j*dw/G)/(1.0+(2*dw/G)**2.0))**2))
    b.line_plot("quest2", dw, 1/(1+(2.0*dw/G)**2.0))

    b.line_plot("width", [-G/2, G/2], [0.5, 0.5])
    Q=2*pi*f/G=f/df
    2*pi*df=G


if __name__=="__main__":
    #ReldB_colormesh()
    #ReldB_cs()
    quest()

    #Relabs_colormesh()

    #magabs_cs()
    #magabs_colormesh()
    #magabs_cs2()
    #time_speed()
    #b.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/test_data/")
    shower(b)


