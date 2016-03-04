# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:46:49 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read, TA88_Fund, qdt
from atom.api import Typed, Unicode, Float, observe, FloatRange
from h5py import File
from taref.core.universal import Array
from numpy import float64, linspace, shape, reshape, squeeze, mean, angle, absolute, array
from taref.core.atom_extension import tag_Property
from taref.physics.units import dB
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from taref.core.agent import Operative

class Fitter(Operative):
     offset=FloatRange(-1.0, 1.0, -0.036).tag(tracking=True)
     flux_factor=FloatRange(0.01, 1.0, qdt.flux_factor).tag(tracking=True)

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
             self.plotter.plot_dict["magabs_flux"].clt.set_xdata(self.flux_parabola*1e-9)
             self.plotter.draw()

class Lyzer(TA88_Fund):
    rd_hdf=Typed(TA88_Read)

    comment=Unicode().tag(read_only=True, spec="multiline")

    rt_atten=Float(60)

    rt_gain=Float(26*2)

    time=Array().tag( plot=True, label="Time")
    yoko=Array().tag(unit="V", plot=True, label="Yoko")
    Magcom=Array().tag(private=True)

    probe_frq=Float().tag(unit="GHz", label="Probe frequency", read_only=True)
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")



    @tag_Property(display_unit="dB", plot=True)
    def MagdB(self):
        return self.Magcom[:, :]/dB

    @tag_Property(plot=True)
    def Phase(self):
        return angle(self.Magcom[:, :])#-mean(self.Magcom[:, 297:303], axis=1, keepdims=True))

    @tag_Property( plot=True)
    def MagAbs(self):
        #return absolute(self.Magcom[:, :])
        return absolute(self.Magcom[:, :])#-mean(self.Magcom[:, 2500:2501], axis=1, keepdims=True))


    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0223/S1A1_TA88_time_domain_fluxswp.hdf5")

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            print f["Traces"].keys()
            self.comment=f.attrs["comment"]
            print f["Instrument config"].keys()
            self.probe_frq=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs["Start frequency"]
            self.probe_pwr=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs["Output power"]
            print f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs.keys()
#
            print f["Data"]["Channel names"][:]
            Magvec=f["Traces"]["Digitizer 1 - Trace"]#[:]
            data=f["Data"]["Data"]
            print shape(data)
#
            self.yoko=data[:,0,0].astype(float64)
            tstart=f["Traces"]['Digitizer 1 - Trace_t0dt'][0][0]
            tstep=f["Traces"]['Digitizer 1 - Trace_t0dt'][0][1]
            print shape(Magvec)
            sm=shape(Magvec)[0]
            sy=shape(data)
            s=(sm, sy[0], sy[2])
            print s
            Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
            Magcom=reshape(Magcom, s, order="F")
            self.time=linspace(tstart, tstart+tstep*(sm-1), sm)
            print shape(Magcom)
            Magcom=squeeze(Magcom)
            self.Magcom=Magcom.transpose()
            #Magabs=Magcom[:, :, :]-mean(Magcom[:, 197:200, :], axis=1, keepdims=True)


a=Lyzer()
a.read_data()
c=Fitter()
c.yoko=a.yoko[:]
b=Plotter()
def magdB_colormesh():
    b.colormesh("magdB", a.time*1e6, a.yoko,  a.MagdB)
    #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
    #b.set_ylim(4.4e9, 4.5e9)
    b.xlabel="Yoko (V)"
    b.ylabel="Frequency (Hz)"
    b.title="Reflection fluxmap"

def magabs_colormesh():
    flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=a.yoko, offset=c.offset, flux_factor=c.flux_factor)

    b.colormesh("magabs", a.time*1e6, flux_over_flux0, a.MagAbs)
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

def magabs_cs():
    b.line_plot("magabs_cs", c.flux_parabola, mean(a.MagAbs[58:59, :], axis=0))
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
    b.line_plot("spd_fit", t*1e6,  (t*qdt.vf)*1e6, label="(3488 m/s)t")

if __name__=="__main__":
    #magdB_colormesh()
    #magabs_cs()
    #magabs_colormesh()
    #b.line_plot("magabs_flux", c.flux_parabola, mean(a.MagAbs[:, 30:40], axis=1))
    b.line_plot("magabs_flux", c.flux_parabola*1e-9, mean(a.MagAbs[:, 72:85], axis=1))
    b.vline_plot('freq', 4.4622)
    b.line_plot("magabs_flux", c.flux_parabola*1e-9, mean(a.MagAbs[:, 96:102], axis=1))

    from scipy.optimize import leastsq # Levenberg-Marquadt Algorithm #

    def lorentzian(x,p):
        numerator =  (p[0]**2 )
        denominator = ( x - (p[1]) )**2 + p[0]**2
        y = p[2]*(numerator/denominator)+p[3]
        return y

    def residuals(p,y,x):
        err = y - lorentzian(x,p)
        return err

    #ind_bg_low = (x > min(x)) & (x < 450.0)
    #ind_bg_high = (x > 590.0) & (x < max(x))

    #x_bg = concatenate((x[ind_bg_low],x[ind_bg_high]))
    #y_bg = concatenate((y[ind_bg_low],y[ind_bg_high]))
    #m, c = polyfit(x_bg, y_bg, 1)
    #background = m*x + c
    #y_bg_corr = y - background

    # initial values #
    p = [200e6,4.5e9, 0.02, 0.022]  # [hwhm, peak center, intensity] #

    # optimization #
    pbest = leastsq(residuals,p,args=(mean(a.MagAbs[:, 72:85], axis=1), c.flux_parabola), full_output=1)
    best_parameters = pbest[0]
    print pbest[0]

    #print a.frequency[903]
    # fit to data #
    fit = lorentzian(c.flux_parabola,best_parameters)
    b.line_plot("lorentzian", c.flux_parabola*1e-9, fit)

    p = [200e6,4.5e9, -0.02, 0.022]  # [hwhm, peak center, intensity] #

    def lorentzian(x,p):
        numerator =  (p[0]**2 )
        denominator = ( x - (p[1]) )**2 + p[0]**2
        y = p[2]*(numerator/denominator)**2+p[3]
        return y

    def residuals(p,y,x):
        err = y - lorentzian(x,p)
        return err
    pbest = leastsq(residuals,p,args=(mean(a.MagAbs[:, 96:102], axis=1), c.flux_parabola), full_output=1)
    best_parameters = pbest[0]
    print pbest[0]
    fit = lorentzian(c.flux_parabola,best_parameters)
    b.line_plot("lorentzian", c.flux_parabola*1e-9, fit)

    class Fitter2(Operative):
      frequency=FloatRange(4.4, 4.5, 4.4622).tag(tracking=True)
      offset=FloatRange(0.00, 1.0e-2, 0.0).tag(tracking=True)
      height=FloatRange(0.00, 1.0e-2, 0.0).tag(tracking=True)
      width=FloatRange(10.0, 500.0, 50.0).tag(tracking=True)

      @tag_Property(plot=True, private=True)
      def lorenz(self):
         return lorentzian(c.flux_parabola, [self.width*1e6, self.frequency*1e9, self.height, self.offset])

      @observe("frequency", "offset", "width", "height")
      def update_plot(self, change):
         if change["type"]=="update":
             self.get_member("lorenz").reset(self)
             b.plot_dict["lorenz"].clt.set_ydata(self.lorenz)
             b.draw()
    d=Fitter2()
    bp=[  7.11932128e+07,   4.44542932e+09,   1.62596541e-04,  2.26753425e-05]
    fit2 = lorentzian(c.flux_parabola, bp)
    b.line_plot("lorenz", c.flux_parabola*1e-9, fit2)

    #magabs_cs2()
    #time_speed()
    #b.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/test_data/")
    shower(b)


