# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:08:41 2016

@author: thomasaref
"""

from taref.saw.qdt import QDT
from taref.saw.idt import IDT
from taref.core.atom_extension import get_tag, tag_Property
from taref.filer.read_file import Read_HDF5
from taref.filer.filer import Folder
from taref.core.agent import Agent
from atom.api import Float, Unicode, Typed, Int, Callable, Enum
from taref.core.universal import Array
from numpy import array, log10, fft, exp, float64, linspace, shape, reshape, squeeze, mean, angle, absolute, sin, pi
from h5py import File
from scipy.optimize import leastsq
from taref.core.log import log_debug
from taref.plotter.fig_format import Plotter
from taref.physics.units import dBm, dB

class TA88_Read(Read_HDF5):
    def _default_folder(self):
        return Folder(base_dir="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216", quality="", main_dir="Data_0221")

class TA88_Fund(Agent):
    fridge_atten=Float(60)
    fridge_gain=Float(45)

qdt=QDT(material='LiNbYZ',
        ft="double",
        a=80.0e-9,
        Np=9,
        Rn=3780.0, #(3570.0+4000.0)/2.0,
        W=25.0e-6,
        eta=0.5,
        flux_factor=0.2945,
        voltage=1.21,
        offset=0.0)

idt=IDT(material='LiNbYZ',
        ft="double",
        Np=36,
        W=25.0e-6,
        eta=0.5,
        a=96.0e-9)


class plot_func(object):
    def __init__(self, plot_key=None):
        self.plot_key=plot_key

    def __call__(self, func):
        if self.plot_key is None:
            self.plot_key=func.func_name

def plots(func):
    """decorator that assists with plotting function definition"""
    def plotty_func(self, plotter=None, *args, **kwargs):
        if plotter is None:
            plotter=Plotter()
        elif isinstance(plotter, basestring):
            if plotter in self.agent_dict:
                plotter=self.agent_dict[plotter]
            else:
                plotter=Plotter(name=plotter)
        return func(self, plotter=plotter, *args, **kwargs)
    return plotty_func

def lorentzian(x,p):
    return p[2]*(((x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def refl_lorentzian(x,p):
    return p[2]*(p[0]**2/(p[0]**2+(x-p[1])**2))+p[3]

def fano(x, p):
    return p[2]*(((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def refl_fano(x, p):
    return p[2]*(1.0-((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

class Lyzer(TA88_Fund):

    #def _default_main_params(self):
    #    return ["rt_atten", "fridge_atten", "fridge_gain", "rt_gain", "comment", "flux_factor", "offset", "fit_type",
    #            "on_res_ind", "start_ind", "stop_ind", "filt_start_ind", "filt_end_ind"]

    rd_hdf=Typed(TA88_Read)
    rt_atten=Float(40)
    rt_gain=Float(23*2)
    comment=Unicode().tag(read_only=True, spec="multiline")
    frequency=Array().tag(unit="GHz", plot=True, label="Frequency", sub=True)
    yoko=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    pwr=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    frq2=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    Magcom=Array().tag(sub=True)
    offset=Float(-0.035)
    flux_factor=Float(0.2925)

    on_res_ind=Int()
    start_ind=Int()
    stop_ind=Int()
    filt_end_ind=Int(58)
    filt_start_ind=Int(5)


    fit_func=Callable(fano).tag(private=True)
    #resid_func=Callable(fano_residuals).tag(private=True)

    def resid_func(self, p, y, x):
        return y-self.fit_func(x, p)

    fit_type=Enum("Transmission", "Reflection")

    @tag_Property(plot=True, sub=True)
    def flux_par(self):
        flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_over_flux0)
        return qdt._get_fq(Ej, qdt.Ec)

    @tag_Property(sub=True)
    def flux_over_flux0(self):
        return (self.yoko-self.offset)*self.flux_factor

    @tag_Property()
    def p_guess(self):
        #return [200e6,4.5e9, 0.002, 0.022, 0.1]
        return [200e6,4.5e9, 0.002, 0.022]

    @tag_Property(sub=True)
    def indices(self):
        return range(len(self.frequency))
        #return [range(81, 120+1), range(137, 260+1), range(269, 320+1), range(411, 449+1)]#, [490]]#, [186]]

    def fft_filter(self, n):
        myifft=fft.ifft(self.Magcom[:,n])
        myifft[self.filt_end_ind:-self.filt_end_ind]=0.0
        if self.filt_start_ind!=0:
            myifft[:self.filt_start_ind]=0.0
            myifft[-self.filt_start_ind:]=0.0
        return fft.fft(myifft)

    @tag_Property(plot=True, sub=True)
    def MagdB(self):
        return 10.0*log10(self.MagAbs)

    @tag_Property(plot=True, sub=True)
    def MagAbs(self):
        return absolute(self.Magcom)

    @tag_Property(plot=True, sub=True)
    def MagAbsFilt(self):
        return absolute(self.MagcomFilt)

    @tag_Property(plot=True, sub=True)
    def MagdBFilt(self):
        return 10.0*log10(self.MagAbsFilt)

    @tag_Property(plot=True, sub=True)
    def MagdBFiltbgsub(self):
        #return self.MagAbsFilt/mean(self.MagAbsFilt[:, 0:5], axis=1, keepdims=True)
        return self.MagdBFilt-10.0*log10(mean(self.MagAbsFilt[:, 0:5], axis=1, keepdims=True))

    @tag_Property(plot=True, sub=True)
    def MagAbsFilt_sq(self):
        return self.MagAbsFilt**2

    @tag_Property(plot=True, sub=True)
    def MagcomFilt(self):
        return array([self.fft_filter(n) for n in range(len(self.yoko))]).transpose()

    @plots
    def magabs_colormesh(self, plotter):
        plotter.colormesh("magabs_{}".format(self.name), self.yoko, self.frequency, self.MagAbs)
        plotter.set_ylim(min(self.frequency), max(self.frequency))
        plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    @plots
    def ifft_plot(self, plotter):
        plotter.line_plot("ifft_{}".format(self.name), absolute(fft.ifft(self.Magcom[:,self.on_res_ind])))
        plotter.line_plot("ifft_{}".format(self.name), absolute(fft.ifft(self.Magcom[:,self.start_ind])))
        plotter.line_plot("ifft_{}".format(self.name), absolute(fft.ifft(self.Magcom[:,self.stop_ind])))

    @plots
    def ifft_dif_plot(self, plotter):
        plotter.line_plot("ifft_dif1_{}".format(self.name), absolute(absolute(fft.ifft(self.Magcom[:,self.start_ind]))-absolute(fft.ifft(self.Magcom[:,self.on_res_ind]))))
        plotter.line_plot("ifft_dif2_{}".format(self.name), absolute(absolute(fft.ifft(self.Magcom[:,self.stop_ind]))-absolute(fft.ifft(self.Magcom[:,self.on_res_ind]))))
        plotter.line_plot("ifft_dif3_{}".format(self.name), absolute(absolute(fft.ifft(self.Magcom[:,self.stop_ind]))-absolute(fft.ifft(self.Magcom[:,self.start_ind]))))

    @plots
    def filt_compare(self, ind, plotter=None):
        plotter.line_plot("magabs_{}".format(self.name), self.frequency, self.MagdB[:, ind], label="MagAbs (unfiltered)")
        plotter.line_plot("magabs_{}".format(self.name), self.frequency, self.MagdBFilt[:, ind], label="MagAbs (filtered)")

    @plots
    def magabsfilt_colormesh(self, plotter):
        plotter.colormesh("magabsfilt_{}".format(self.name), self.yoko, self.frequency, self.MagAbsFilt)
        plotter.set_ylim(min(self.frequency), max(self.frequency))
        plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    @plots
    def magdBfilt_colormesh(self, plotter):
        plotter.colormesh("magdBfilt_{}".format(self.name), self.yoko, self.frequency, self.MagdBFilt)
        plotter.set_ylim(min(self.frequency), max(self.frequency))
        plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="MagdB fluxmap {}".format(self.name)

    @plots
    def magdBfiltbgsub_colormesh(self, plotter):
        plotter.colormesh("magdBfiltbgsub_{}".format(self.name), self.yoko, self.frequency, self.MagdBFiltbgsub)
        plotter.set_ylim(min(self.frequency), max(self.frequency))
        plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="MagdB bg sub fluxmap {}".format(self.name)

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            Magvec=f["Traces"]["RS VNA - S21"]
            data=f["Data"]["Data"]
            self.comment=f.attrs["comment"]
            self.yoko=data[:,0,0].astype(float64)
            fstart=f["Traces"]['RS VNA - S21_t0dt'][0][0]
            fstep=f["Traces"]['RS VNA - S21_t0dt'][0][1]
            sm=shape(Magvec)[0]
            sy=shape(data)
            print sy
            s=(sm, sy[0], 1)#sy[2])
            Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
            Magcom=reshape(Magcom, s, order="F")
            self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            self.Magcom=squeeze(Magcom)
            self.stop_ind=len(self.yoko)-1

    def full_fano_fit(self):
        log_debug("started fano fitting")
        fit_params=[self.fano_fit(n)  for n in self.indices]
        fit_params=array(zip(*fit_params))
        log_debug("ended fano fitting")
        return fit_params

    @plots
    def plot_widths(self, plotter):
        fit_params=self.full_fano_fit()
        plotter.scatter_plot("widths_{}".format(self.name), fit_params[0, :], absolute(fit_params[1, :]), color="red", label=self.name)

    def fano_fit(self, n):
        pbest= leastsq(self.resid_func, self.p_guess, args=(self.MagAbsFilt_sq[n, :], self.flux_par), full_output=1)
        best_parameters = pbest[0]
        #log_debug(best_parameters)
        #if 0:#n==539 or n==554:#n % 10:
            #b.line_plot("magabs_flux", self.flux_par*1e-9, (self.MagAbsFilt_sq[n, :], label="{}".format(n), linewidth=0.2)
            #b.line_plot("lorentzian", self.flux_par*1e-9, self.fit_func(self.flux_par,best_parameters), label="fit {}".format(n), linewidth=0.5)
        return (self.frequency[n], best_parameters[0], best_parameters[1], best_parameters[2], best_parameters[3])

class TransLyzer(Lyzer):
    def _default_fit_func(self):
        return lorentzian

    def _default_fit_type(self):
        return "Transmission"

#    @tag_Property()
#    def p_guess(self):
#        return [200e6,4.5e9, 0.002, 0.022, 0.1]
#
#    def _default_fit_func(self):
#        return fano
class ReflLyzer(Lyzer):
    def _default_fit_func(self):
        return refl_lorentzian

    def _default_fit_type(self):
        return "Reflection"


class TransTimeLyzer(TransLyzer):
    f_ind=Int()
    t_ind=Int()
    t_start_ind=Int(63)
    t_stop_ind=Int(77)

    time=Array().tag( plot=True, label="Time", sub=True)
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")

    @tag_Property( plot=True, sub=True)
    def MagAbs(self):
        print self.frequency[self.f_ind]
        return absolute(self.Magcom[:, self.f_ind, :].transpose())#-mean(self.Magcom[:, 99:100, self.pind].transpose(), axis=1, keepdims=True))

    #@tag_Property( plot=True, sub=True)
    #def MagAbsTime(self):
    #    return absolute(mean(self.Magcom[self.t_start_ind:self.t_stop_ind, :, :], axis=0).transpose())
    @tag_Property(plot=True, sub=True)
    def MagAbsFilt(self):

        return 10.0**((20.0*log10(absolute(self.MagcomFilt))-self.probe_pwr)/20.0)#/(self.probe_pwr*dBm)

    @tag_Property(plot=True, sub=True)
    def MagcomFilt(self):
        return mean(self.Magcom[self.t_start_ind:self.t_stop_ind, :, :], axis=0)#/(self.probe_pwr*dBm)#.transpose()

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            self.probe_pwr=f["Instrument config"]["Anritsu 68377C Signal generator - GPIB: 8, Pump3 at localhost"].attrs["Power"]

            print f["Traces"].keys()
            self.comment=f.attrs["comment"]
            print f["Data"]["Channel names"][:]
            Magvec=f["Traces"]["TA - LC Trace"]
            #Magvec=f["Traces"]["Digitizer2 - Trace"]#[:]
            data=f["Data"]["Data"]
            print shape(data)
            self.frequency=data[:,0,0].astype(float64)
            self.yoko=data[0,1,:].astype(float64)
            print self.frequency
            tstart=f["Traces"]['TA - Trace_t0dt'][0][0]
            tstep=f["Traces"]['TA - Trace_t0dt'][0][1]
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
            self.Magcom=Magcom[:]#.transpose()
            print shape(self.Magcom)

    @plots
    def magabs_colormesh(self, plotter=None):
        plotter.colormesh("magabs", self.time*1e6, self.yoko, self.MagAbs)
        plotter.xlabel="Time (us)"
        plotter.ylabel="Magnitude (abs)"
        plotter.title="Reflection vs time"
        plotter.set_ylim(min(self.yoko), max(self.yoko))
        plotter.set_xlim(min(self.time)*1e6, max(self.time)*1e6)
        plotter.xlabel="Yoko (V)"
        plotter.ylabel="Frequency (Hz)"
        plotter.title="Magabs fluxmap {}".format(self.name)

    @plots
    def filt_compare(self, ind, plotter=None):
        #plotter.line_plot("magabs_{}".format(self.name), self.frequency, self.MagAbs[:, ind], label="MagAbs (unfiltered)")
        plotter.line_plot("magabs_{}".format(self.name), self.frequency, self.MagAbsFilt[:, ind], label="MagAbs (time)")

#    def magabstime_colormesh(self, plotter=None):
#        if plotter is None:
#            plotter=self.plotter
#        plotter.colormesh("magabs", self.frequency, self.yoko, self.MagAbsTime)
#        plotter.xlabel="Time (us)"
#        plotter.ylabel="Magnitude (abs)"
#        plotter.title="Reflection vs time"

if __name__=="__main__":
    print get_tag(qdt, "a", "unit")
    print qdt.latex_table()
    from taref.plotter.fig_format import Plotter
    from taref.physics.fundamentals import sinc, sinc_sq,e
    print e
    b=Plotter()
    from numpy import linspace, pi, absolute, sqrt
    freq=linspace(1e9, 10e9, 1000)
    #qdt.ft="single"
    #qdt.get_member("mult").reset(qdt)
    #qdt.get_member("lbda0").reset(qdt)

    print qdt.f0, qdt.G_f0
    if 0:
        G_f=(1.0/sqrt(2.0))*0.5*qdt.Np*qdt.K2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-qdt.f0)/qdt.f0))
        b.line_plot("sinc", freq, G_f, label="sinc/sqrt(2)")
        G_f=0.5*qdt.Np*qdt.K2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-qdt.f0)/qdt.f0))
        b.line_plot("sinc2", freq, G_f, label="sinc")
        G_f=0.5*qdt.Np*qdt.K2*qdt.f0*sinc_sq(qdt.Np*pi*(freq-qdt.f0)/qdt.f0)
        b.line_plot("sinc_sq", freq, G_f, label="sinc_sq")
        b.vline_plot("listen", 4.475e9, alpha=0.3, color="black")
        b.vline_plot("listent", 4.55e9, alpha=0.3, color="black")
        b.vline_plot("listenb", 4.4e9, alpha=0.3, color="black")
    if 0:
        freq=4.475e9
        f0=linspace(5e9, 6e9, 1000)
        G_f=(1.0/sqrt(2.0))*0.5*qdt.Np*qdt.K2*f0*absolute(sinc(qdt.Np*pi*(freq-f0)/f0))
        b.line_plot("sinc", f0, G_f, label="sinc/sqrt(2)")
        G_f=0.5*qdt.Np*qdt.K2*f0*absolute(sinc(qdt.Np*pi*(freq-f0)/f0))
        b.line_plot("sinc2", f0, G_f, label="sinc")
        G_f=0.5*qdt.Np*qdt.K2*f0*sinc_sq(qdt.Np*pi*(freq-f0)/f0)
        b.line_plot("sinc_sq", f0, G_f, label="sinc_sq")
        b.vline_plot("theory", 5.45e9, alpha=0.3, color="black", label="theory")
        #b.vline_plot("listent", 4.55e9, alpha=0.3, color="black")
        #b.vline_plot("listenb", 4.4e9, alpha=0.3, color="black")

    if 1:
        from numpy import pi, linspace, sin, amax, argmin, argmax, cos
        from scipy.constants import h
        Np=qdt.Np
        f0=5.45e9
        w0=2*pi*f0
        #qdt.Dvv=0.001
        vf=3488.0
        freq=linspace(1e9, 10e9, 1000)
        print qdt.flux_factor, qdt.offset, qdt.Ejmax/h, qdt.Ec/h
        def flux_to_Ej(voltage,  offset=qdt.offset, flux_factor=qdt.flux_factor, Ejmax=qdt.Ejmax):
            flux_over_flux0=(voltage-offset)*flux_factor
            Ej=Ejmax*absolute(cos(pi*flux_over_flux0))
            return Ej

        def calc_Lamb_shift(fq, Dvv=qdt.Dvv):
            epsinf=qdt.epsinf
            W=qdt.W

            wq=2.0*pi*fq#print wq

            X=Np*pi*(wq-w0)/w0
            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            C=sqrt(2.0)*Np*W*epsinf
            #Ga=Ga0*(sin(X)/X)**2.0
            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
            return -Ba/(2.0*C)/(2.0*pi)

        def calc_Coupling(fqq, Dvv=qdt.Dvv):
            epsinf=qdt.epsinf
            W=qdt.W

            wq=2.0*pi*fqq#print wq

            X=Np*pi*(wq-w0)/w0
            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            C=sqrt(2.0)*Np*W*epsinf
            Ga=Ga0*(sin(X)/X)**2.0
            #Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
            return Ga/(2.0*C)/(2.0*pi)

        def energy_levels(EjdivEc, Ec=qdt.Ec, Dvv=qdt.Dvv):
            print Ec/h
            Ec=Ec
            Ej=EjdivEc*Ec
            w0n=sqrt(8.0*Ej*Ec)/h*(2.0*pi)
            #epsinf=qdt.epsinf
            #W=qdt.W
            #Dvv=qdt.Dvv
            E0p =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0#-Ba/(2.0*C)*0.5 #(n +1/2)

            E1p =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)# -Ba/(2.0*C)*1.5

            E2p =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)#-Ba/(2.0*C)*2.5
            E3p =  sqrt(8.0*Ej*Ec)*3.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)#-Ba/(2.0*C)*3.5

            E0p=E0p/h
            E1p=E1p/h
            E2p=E2p/h
            E3p=E3p/h
            #fq=sqrt(8.0*Ej*Ec)
            #wq=2.0*pi*fq#print wq

            #X=Np*pi*(wq-w0)/w0
            #Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            #C=sqrt(2.0)*Np*W*epsinf
            #Ga=Ga0*(sin(X)/X)**2.0
            #Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)

            #E10=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-Ec/(1.0+Ba/(wq*C))
            #E21=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-2.0*Ec/(1.0+Ba/(wq*C))
            #return E10/h, (E21+E10)/h/2.0
            #E_{tot}=-E_J+\sqrt{8E_J E_C}(n +1/2)-(B_a/2C)(n +1/2)-\dfrac{E_C}{12}(6n^2+6n+3)
            E0 =  E0p#+calc_Lamb_shift(E0p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0-Ba/(2.0*C)*0.5 #(n +1/2)

            E1 =  E1p+calc_Lamb_shift(E1p-E0p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0) -Ba/(2.0*C)*1.5

            E2 =  E2p+calc_Lamb_shift(E2p-E1p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)-Ba/(2.0*C)*2.5
            E3 =  E3p+calc_Lamb_shift(E3p-E2p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*3.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)-Ba/(2.0*C)*3.5
            return E0, E1, E2, E3, E0p, E1p, E2p, E3p, w0n
            return (E1-E0)/h, (E2-E1)/h#/3.0
            #return qdt._get_fq(Ej, qdt.Ec)

        EjdivEc=linspace(0.001, 300, 3000).astype(float64)
        Ejmax=qdt.Ejmax
        E0,E1,E2,E3, E0p, E1p, E2p, E3p, w0n=energy_levels(EjdivEc, Ec=qdt.Ec, Dvv=qdt.Dvv)

        b.line_plot("E0", EjdivEc, E0, label="E0")
        b.line_plot("E1", EjdivEc, E1, label="E1")
        b.line_plot("E2", EjdivEc, E2, label="E2")
        b.line_plot("E3", EjdivEc, E3, label="E3")

        DEP=E1p-E0p
        d=Plotter(fig_height=5.0, fig_width=7.0)
        #Plotter(name="anharm")
        d.line_plot("E0", E1p-E0p, (E2-E1)-(E1-E0)-((E2p-E1p)-(E1p-E0p)), label="E0")
        d.line_plot("E1", E1p-E0p, E1-E0-(E1p-E0p), label="E1")
        d.line_plot("E2", E1p-E0p, E2-E1-(E2p-E1p), label="E2")
        #d.line_plot("E3", EjdivEc, E3, label="E3")
        #E0,E1,E2,E3=energy_levels(EjdivEc, Dvv=0.0)

        b.line_plot("E0p", EjdivEc, E0p, label="E0p")
        b.line_plot("E1p", EjdivEc, E1p, label="E1p")
        b.line_plot("E2p", EjdivEc, E2p, label="E2p")
        b.line_plot("E3p", EjdivEc, E3p, label="E3p")

        #d.line_plot("E0p", EjdivEc, (E2p-E1p)-(E1p-E0p), label="E0p")
        #d.line_plot("E1p", E1p-E0p, (E2p-E1p)-DEP, label="E1p")
        #d.line_plot("E2p", E1p-E0p, E3p-E2p, label="E2p")
        #b.show()
        yo = linspace(-2.0, 2.0, 2000)
        Ej=flux_to_Ej(yo, Ejmax=Ejmax)
        EjdivEc=Ej/qdt.Ec
        E0,E1,E2,E3, E0p, E1p, E2p, E3p, w0n=energy_levels(EjdivEc, Dvv=qdt.Dvv)
        Gamma10=calc_Coupling(E1-E0)
        Gamma20=calc_Coupling((E2-E0)/2.0)
        #d.scatter_plot("blah", E1-E0, Gamma10, label="E_{10}")
        #d.scatter_plot("lbs", (E2-E0)/2.0, Gamma20, label="E_{20}/2")
        fw0=linspace(4e9, 7e9, 2000) #E1-E0 #sqrt(8*Ej*qdt.Ec)/h
        d.line_plot("asdf", fw0/1e9, calc_Coupling(fw0)/1e9, label=r"$G_a/2C$", color="blue")
        d.line_plot("asdfd", fw0/1e9, calc_Lamb_shift(fw0)/1e9, label=r"$-B_a/2C$", color="red")
        d.legend()

        d.mpl_axes.xlabel="Frequency (GHz)"
        d.mpl_axes.ylabel="Frequency (GHz)"
        d.set_ylim(-1.0, 1.5)
        #dd.set_xlim(4.2, 5.0)
        #d.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_Ba.pdf")
        #d.show()


        dd=Plotter(fig_height=7.0, fig_width=7.0)
        def listen_coupling(f_listen, Dvv=qdt.Dvv):
            epsinf=qdt.epsinf
            W=qdt.W
            w=2.0*pi*f_listen
            Np=36
            f0=idt.f0
            print f0 #4.5e9
            w0=2*pi*f0
            X=Np*pi*(w-w0)/w0
            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            C=sqrt(2.0)*Np*W*epsinf
            Ga=Ga0*(sin(X)/X)**2.0
            #Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
            return Ga/(2.0*C)/(2.0*pi)

        dd.line_plot("asdf", fw0/1e9, calc_Coupling(fw0)/1e9, label=r"$G_a/2C$", color="blue")
        dd.line_plot("asdfd", fw0/1e9, calc_Lamb_shift(fw0)/1e9, label=r"$-B_a/2C$", color="red")
        dd.line_plot("listen", fw0/1e9, listen_coupling(fw0)/4/1e9, label=r"$G_a^{IDT}/2C^{IDT}/4$", color="green")
        dd.plot_dict["listen"].mpl.linestyle="dashed"
        dd.legend()
        #dd.set_ylim(-1.0, 1.5)
        #dd.set_xlim(min(self.yoko), max(self.yoko))
        dd.mpl_axes.xlabel="Frequency (GHz)"
        dd.mpl_axes.ylabel="Frequency (GHz)"
        #dd.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_all.pdf")#, format="eps")
        dd.set_ylim(-0.01, 0.1)
        dd.set_xlim(4.2, 5.0)
        #dd.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_all_zoom.pdf")#, format="eps")

        #dd.show()
        #plotter.mpl_axes.title="MagdB fluxmap {}".format(self.name)
        #Plotter().line_plot("asdf", yo, fw0+calc_Lamb_shift(fw0))

        def R_lor(f_listen, fqq, w0n1, Dvv=qdt.Dvv):
            w=2*pi*f_listen
            epsinf=qdt.epsinf
            W=qdt.W
            X=Np*pi*(f_listen-f0)/f0
            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            C=sqrt(2.0)*Np*W*epsinf
            Ga=Ga0*(sin(X)/X)**2.0
            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
            w0nn=2*pi*fqq#w0n1#-Ba/(2.0*C)
            Gamma=calc_Coupling(fqq, Dvv=Dvv)
            L=1/(C*(w0nn**2.0))
            return  Ga/(Ga+1.0j*Ba+1.0j*w*C+1.0/(1.0j*w*L))
            #return -2Gamma10*(gamma10-idw)/(4*(gamma10*2+dw**2)) #+Gamma10*Gamma21*(gamma20+idw)*0
            #return 1-2*Gamma10/(2*(gamma10-1.0j*dw)+(OmegaC**2)/(2*gamma20-2j*(dw+dwc)))
            return -Gamma/(Gamma+1.0j*(w-w0nn))
#        def R_full(f_listen=4.3e9, fq=5.0e9, fq2=6.0e9):
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
#            wq=2.0*pi*fq
#            wq2=2.0*pi*fq2
#
#            L=1/(C*(wq**2.0))
#            L2=1/(C*(wq2**2.0))
#
#            Gamma=Ga/(2.0*C)
#            #return 1.0/(1.0 +1.0j*(w_listen-wq)/Gamma), 1.0/(1.0 +1.0j*(w_listen-wq2)/Gamma)
#            return Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L)), Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L2))


        temp=[]
        t2=[]
        qfreq=[]
        for f in freq:
            Gamma=calc_Coupling(E1-E0)
            w0nn=2*pi*(E1p-E0p)
            w=2*pi*f
            #R1=-Gamma/(Gamma+1.0j*(w-w0nn))
            R1=R_lor(f, E1p-E0p, w0n)
            #Gamma=calc_Coupling((E2p-E0p)/2.0)
            #w0nn=2*pi*(E2p-E0p)/2.0
            #R2=-Gamma/(Gamma+1.0j*(w-w0nn))
            anharm=(E2-E1)-(E1-E0)
            R2=R_lor(f, E1p-E0p+anharm/2.0, w0n)
            #R1, R2=R_full(f, E1-E0, (E2-E0)/2.0)
            #qfreq.append(freq[argmax(R)])
            #imax=argmax(R)
            #print imax
            #f1=fq[argmin(absolute(fq-f))]
            #f2=freq[argmin(absolute(R[imax:-1]-0.5))]
            t2.append(R2)
            temp.append(R1)
        temp=array(temp)
        #b.line_plot("coup", freq, t2)
        c=Plotter()
        g=Plotter()
        c.colormesh("R_full", yo, freq, 10*log10(absolute(temp)+absolute(t2)))
        g.colormesh("R_full", yo, freq, absolute(temp))
        h=Plotter()
        h.colormesh("R_full", yo, freq, absolute(t2))


        #g.colormesh('R_angle', yo, freq, angle(temp))        #b.line_plot("Ba", freq, t2)
        #b.line_plot("Ga", freq, temp)
        b.show()

    if 0:
        from numpy import pi, linspace, sin, amax, argmin, argmax, cos
        from scipy.constants import h
        Np=qdt.Np
        f0=5.45e9
        w0=2*pi*f0

        vf=3488.0
        freq=linspace(0.0001e9, 15e9, 2000)
        print qdt.flux_factor, qdt.offset, qdt.Ejmax/h, qdt.Ec/h
        def flux_par(w_listen, voltage, offset=qdt.offset, flux_factor=qdt.flux_factor, Ejmax=qdt.Ejmax, Ec=qdt.Ec):
            flux_over_flux0=(voltage-offset)*flux_factor
            Ej=Ejmax*absolute(cos(pi*flux_over_flux0))
            epsinf=qdt.epsinf
            W=qdt.W
            Dvv=qdt.Dvv
            fq=sqrt(8.0*Ej*Ec)/h
            wq=2.0*pi*fq#print wq

            X=Np*pi*(wq-w0)/w0
            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            C=sqrt(2.0)*Np*W*epsinf
            #Ga=Ga0*(sin(X)/X)**2.0
            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)

            E10=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-Ec/(1.0+Ba/(wq*C))
            E21=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-2.0*Ec/(1.0+Ba/(wq*C))
            return E10/h, (E21+E10)/h/2.0
            E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
            E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
            E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
            E3 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)

            return (E1-E0)/h, (E2-E0)/h#/3.0
            #return qdt._get_fq(Ej, qdt.Ec)

        def R_full(f_listen=4.3e9, voltage=0.001):


            w_listen=2*pi*f_listen
            epsinf=qdt.epsinf
            W=qdt.W
            Dvv=qdt.Dvv
            w0=2*pi*f0


            X=Np*pi*(f_listen-f0)/f0
            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            C=sqrt(2.0)*Np*W*epsinf
            Ga=Ga0*(sin(X)/X)**2.0
            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)

            #C_prime=Ba/w_listen+C
            #Ec_prime=e**2/(2.0*C_prime)
            #BadwC=Ba/(w_listen*C)
            fq, fq2=flux_par(w_listen, voltage, offset=0.0, flux_factor=0.2945, Ejmax=qdt.Ejmax, Ec=qdt.Ec)
            wq=2.0*pi*fq
            wq2=2.0*pi*fq2

            L=1/(C*(wq**2.0))
            L2=1/(C*(wq2**2.0))

            #Lc=5000.0
            #Qi=pi*5000.0/(vf/f0*(1-0.999))
            #Qe=1.0/(5.74*vf*50.0*epsinf*W*Dvv*2)*5000.0/36**2

            #r=((Qe-Qi)+2j*Qi*Qe*(fq2-f0)/f0)/((Qe+Qi)+2j*Qi*Qe*(fq2-f0)/f0)

            #w2=Ecprime

            #b.line_plot("Ba", f_listen, Ba)
            #b.line_plot("Ga", f_listen, Ga)
            #return Ba/(2*C*2*pi), Ga/(2*C*2*pi)
            #print Ga, Ba, w_listen*C
            return fq, Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L))+Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L2))
        #R=Ga/(Ga+1j*w_listen*C+1/(1j*w_listen*L))
            #b.line_plot("semiclassical", fq, absolute(R)**2, label=str(f_listen))
        #b.line_plot("semiclassical", fq, Ba)

        temp=[]
        t2=[]
        qfreq=[]
        yo = linspace(-5.0, 5.0, 1000)
        #yo=yo[328:500]
        #fq=array([flux_par(yn)[0] for yn in yo])
        #fq2=array([flux_par(yn)[1] for yn in yo])

        for f in freq:
                #X2=36*pi*(f-4.4e9)/4.4e9
                #wrap=(sin(X2)/X2)**2
            fq, R=R_full(f, yo)
            #qfreq.append(freq[argmax(R)])
            #imax=argmax(R)
            #print imax
            #f1=fq[argmin(absolute(fq-f))]
            #f2=freq[argmin(absolute(R[imax:-1]-0.5))]
            t2.append(fq)
            temp.append(R)
        temp=array(temp)
        #b.line_plot("coup", freq, t2)
        d=Plotter()
        #b.line_plot("Ba", freq, t2)
        #b.line_plot("Ga", freq, temp)

        b.colormesh("R_full", yo, freq, 10*log10(absolute(temp)))
        d.colormesh('R_angle', yo, freq, angle(temp))

        #fft.ifft(418, 328, 500)
        def ifft_plot(name, plotter, Magcom, ind):
            plotter.line_plot("ifft_{}".format(name), absolute(fft.ifft(Magcom[:,ind])), label="ifft_{}".format(name))


        c=Plotter()
        #c.line_plot('R_angle', yo, t2)

        #c.line_plot("cross_sections1", yo, t2)#, label="{:.3f}V".format(yo[500]))

        #c.line_plot("cross_sections1", freq, 10*log10(absolute(temp[:, 500])), label="{:.3f}V".format(yo[500]))
        #c.line_plot("cross_sections2", freq, 10*log10(absolute(temp[:, 428])), label="{:.3f}V".format(yo[428]))
        #c.line_plot("cross_sections3", freq, 10*log10(absolute(temp[:, 401])), label="{:.3f}V".format(yo[401]))
        #c.line_plot("cross_sections4", freq, 10*log10(absolute(temp[:, 385])), label="{:.3f}V".format(yo[385]))
        #c.line_plot("cross_sections5", freq, 10*log10(absolute(temp[:, 380])), label="{:.3f}V".format(yo[380]))
        #c.line_plot("cross_sections6", freq, 10*log10(absolute(temp[:, 368])), label="{:.3f}V".format(yo[368]))

        q=Plotter()
        #q.line_plot("cross_sections1", freq, angle(temp[:, 500]), label="{:.3f}V".format(yo[500]))
        #q.line_plot("cross_sections2", freq, angle(temp[:, 428]), label="{:.3f}V".format(yo[428]))
        #q.line_plot("cross_sections3", freq, angle(temp[:, 401]), label="{:.3f}V".format(yo[401]))
        #q.line_plot("cross_sections4", freq, angle(temp[:, 385]), label="{:.3f}V".format(yo[385]))
        #q.line_plot("cross_sections5", freq, angle(temp[:, 380]), label="{:.3f}V".format(yo[380]))
        #q.line_plot("cross_sections6", freq, angle(temp[:, 368]), label="{:.3f}V".format(yo[368]))


        #ifft_plot(328, c, temp, 328)
        #ifft_plot(418, c, temp, 418)
        #ifft_plot(500, c, temp, 500)
        def fft_filter(mg, n):
            myifft=fft.ifft(mg[:,n])
            #myifft[16:-16]=0.0
            #if self.filt_start_ind!=0:
            myifft[:11]=0.0
            myifft[-11:]=0.0
            return fft.fft(myifft)
        #t2=array([fft_filter(temp, n) for n in range(len(yo))])
        #b.colormesh("R_filt",# yo[328:500], freq[::4],
        #absolute(t2[328:500, :]))
        #R_full(4.2500001e9)
        #R_full(4.3000001e9)
        #R_full(4.3500001e9)
        #fq=linspace(4e9, 5e9, 1000)
        #X=Np*pi*(fq-f0)/f0
        #Ga=(sin(X)/X)**2.0
        #Ba=(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
        #b.line_plot("Ga", fq, Ga)
        #b.line_plot("Ba", fq, Ba)
        #sqrt(1/(C))/2*p
        #b.line_plot("semiclassical", fq, absolute(R)/amax(absolute(R)))
    #b.show()
    qdt.show()
