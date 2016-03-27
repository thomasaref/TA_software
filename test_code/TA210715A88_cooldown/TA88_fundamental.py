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
        plotter.xlabel="Yoko (V)"
        plotter.ylabel="Frequency (Hz)"
        plotter.title="Magabs fluxmap {}".format(self.name)

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
        plotter.xlabel="Yoko (V)"
        plotter.ylabel="Frequency (Hz)"
        plotter.title="Magabs fluxmap {}".format(self.name)

    @plots
    def magdBfilt_colormesh(self, plotter):
        plotter.colormesh("magdBfilt_{}".format(self.name), self.yoko, self.frequency, self.MagdBFilt)
        plotter.set_ylim(min(self.frequency), max(self.frequency))
        plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.xlabel="Yoko (V)"
        plotter.ylabel="Frequency (Hz)"
        plotter.title="MagdB fluxmap {}".format(self.name)

    @plots
    def magdBfiltbgsub_colormesh(self, plotter):
        plotter.colormesh("magdBfiltbgsub_{}".format(self.name), self.yoko, self.frequency, self.MagdBFiltbgsub)
        plotter.set_ylim(min(self.frequency), max(self.frequency))
        plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.xlabel="Yoko (V)"
        plotter.ylabel="Frequency (Hz)"
        plotter.title="MagdB bg sub fluxmap {}".format(self.name)

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
    from taref.physics.fundamentals import sinc, sinc_sq
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

    if 0:
        from numpy import pi, linspace, sin, amax, argmin, argmax
        Np=qdt.Np
        f0=5.35e9
        freq=linspace(4e9, 5e9, 1000)

        def R_full(f_listen=4.3e9):
            w_listen=2*pi*f_listen
            epsinf=qdt.epsinf
            W=qdt.W
            Dvv=qdt.Dvv
            w0=2*pi*f0

            fq=linspace(4e9, 5e9, 20)

            wq=2.0*pi*fq

            X=Np*pi*(f_listen-f0)/f0
            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            C=sqrt(2.0)*Np*W*epsinf
            L=1/(C*(wq**2.0))

            Ga=Ga0*(sin(X)/X)**2.0
            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)

            #b.line_plot("Ba", fq, Ba)
            #b.line_plot("Ga", fq, Ga)
            #print Ga, Ba, w_listen*C
            return Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L))
        #R=Ga/(Ga+1j*w_listen*C+1/(1j*w_listen*L))
            #b.line_plot("semiclassical", fq, absolute(R)**2, label=str(f_listen))
        #b.line_plot("semiclassical", fq, Ba)

        temp=[]
        t2=[]
        qfreq=[]
        for f in freq:
            X2=36*pi*(f-4.4e9)/4.4e9
            wrap=(sin(X2)/X2)**2
            R=absolute(R_full(f))**2
            #qfreq.append(freq[argmax(R)])
            imax=argmax(R)
            print imax
            f1=freq[argmin(absolute(R[0:imax]-0.5))]
            f2=freq[argmin(absolute(R[imax:-1]-0.5))]
            t2.append(f2-f1)
            temp.append(R)

        b.line_plot("coup", freq, t2)
        #b.colormesh("R_full", freq, freq, temp)
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
