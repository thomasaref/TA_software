# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 12:42:53 2016

@author: thomasaref
"""

from taref.core.api import Agent, Array, tag_property, log_debug, s_property
from taref.filer.read_file import Read_HDF5
from taref.physics.qdt import QDT
from taref.physics.fitting_functions import fano, lorentzian, refl_lorentzian, full_fano_fit, full_fit, lorentzian2
from taref.physics.filtering import window_ifft, fft_filter, filt_prep, fir_filt_prep, ifft_x, fir_freqz, Filter
from taref.plotter.api import line, colormesh, scatter, Plotter
from atom.api import Float, Typed, Unicode, Int, Callable, Enum, List
from h5py import File
from numpy import pi, append, angle, cos, sin, unwrap, arccos, float64, shape, reshape, linspace, squeeze, fft, log10, absolute, array, amax, amin, sqrt
from scipy.optimize import leastsq, curve_fit
from taref.physics.qdt import QDT
from taref.physics.fundamentals import bgsub2D
from functools import wraps

class plots(object):
    def __init__(self, pl=None):
        self.pl=pl

    def __call__(self, func):
        @wraps(func)
        def plot_func(self, pl=None, *args, **kwargs):
            if pl is None:
                pl=Plotter(fig_width=kwargs.pop("fig_width", 9.0), fig_height=kwargs.pop("fig_height", 6.0))
            return func(self, pl=pl, *args, **kwargs)
        return plot_func

class LyzerBase(Agent):
    #qdt=QDT()
    base_name="lyzer_base"
    fridge_atten=Float(60)
    fridge_gain=Float(45)

    @tag_property()
    def net_loss(self):
        return self.fridge_gain-self.fridge_atten+self.rt_gain-self.rt_atten


    rd_hdf=Typed(Read_HDF5)
    rt_atten=Float(40)
    rt_gain=Float(23*2)

    offset=Float(-0.035)
    flux_factor=Float(0.2925)

    def _default_offset(self):
        return self.qdt.offset

    def _default_flux_factor(self):
        return self.qdt.flux_factor

    comment=Unicode().tag(read_only=True, spec="multiline")

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
        #print sy
        s=(sm, sy[0], 1)#sy[2])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        self.MagcomData=squeeze(Magcom)
        self.stop_ind=len(self.yoko)-1

class Lyzer(LyzerBase):
    base_name="lyzer"

    filter_type=Enum("None", "FFT", "FIR", "Fit")
    bgsub_type=Enum("None", "Complex", "MagAbs", "MagdB")
    fit_type=Enum("fq", "yoko")

    frequency=Array().tag(unit="GHz", plot=True, label="Frequency", sub=True)
    yoko=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    #pwr=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    #frq2=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    MagcomData=Array().tag(sub=True, desc="raw data in compex form")
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")

    on_res_ind=Int()
    start_ind=Int()
    stop_ind=Int()

    indices=List()
    port_name=Unicode('S21')
    VNA_name=Unicode("RS VNA")

    filt=Typed(Filter, ())

    bgsub_start_ind=Int(0)
    bgsub_stop_ind=Int(1)
    bgsub_axis=Int(1)

    fit_func=Callable(lorentzian).tag(private=True)
    read_data=Callable(read_data).tag(sub=True)


    @tag_property(plot=True, sub=True)
    def fq(self):
        return self.qdt._get_fq(Ej=self.Ej, Ec=self.qdt.Ec)

    @tag_property(sub=True)
    def ls_f(self):
        #return array([f-self.qdt._get_Lamb_shift(f=f) for f in self.frequency])
        return array([sqrt(f*(f-2*self.qdt._get_Lamb_shift(f=f))) for f in self.frequency])

    @tag_property(sub=True)
    def voltage_from_flux_par(self):
        Ej=self.qdt._get_Ej_get_fq(fq=self.ls_f)
        flux_d_flux0=self.qdt._get_flux_over_flux0_get_Ej(Ej=Ej)
        return self.qdt._get_voltage(flux_over_flux0=flux_d_flux0, offset=self.offset, flux_factor=self.flux_factor)


    @tag_property(sub=True)
    def voltage_from_flux_par2(self):
        Ej=self.qdt._get_Ej_get_fq(fq=self.ls_f)
        fdf0=self.qdt._get_flux_over_flux0_get_Ej(Ej=Ej)
        flux_d_flux0=append(fdf0, -fdf0)
        flux_d_flux0=append(flux_d_flux0, -fdf0+pi)
        flux_d_flux0=append(flux_d_flux0, fdf0-pi)
        freq=append(self.frequency, self.frequency)
        freq=append(freq, freq)
        return freq, self.qdt._get_voltage(flux_over_flux0=flux_d_flux0, offset=self.offset, flux_factor=self.flux_factor)

    @tag_property(sub=True)
    def ls_flux_par(self):
        return self.qdt._get_ls_flux_parabola(voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)

    @tag_property(plot=True, sub=True)
    def Ej(self):
        return self.qdt._get_Ej(Ejmax=self.qdt.Ejmax, flux_over_flux0=self.flux_over_flux0)

    @tag_property(sub=True)
    def flux_over_flux0(self):
        return self.qdt._get_flux_over_flux0(voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)


    def _default_indices(self):
        return range(len(self.frequency))
        #return [range(81, 120+1), range(137, 260+1), range(269, 320+1), range(411, 449+1)]#, [490]]#, [186]]

#    def fft_filter(self, n):
#        myifft=fft.ifft(self.MagcomData[:,n])
#        myifft[self.filt_end_ind:-self.filt_end_ind]=0.0
#        if self.filt_start_ind!=0:
#            myifft[:self.filt_start_ind]=0.0
#            myifft[-self.filt_start_ind:]=0.0
#        return fft.fft(myifft)

    @tag_property(plot=True, sub=True)
    def MagdB(self):
        if self.bgsub_type=="MagdB":
            return self.bgsub(10.0*log10(absolute(self.Magcom)))
        return 10.0*log10(self.MagAbs)

    def bgsub(self, arr):
        return bgsub2D(arr, self.bgsub_start_ind, self.bgsub_stop_ind, self.bgsub_axis)

    @tag_property(plot=True, sub=True)
    def MagAbs(self):
        if self.bgsub_type=="MagdB":
            return 10.0**(self.MagdB/10.0)
        magabs=absolute(self.Magcom)
        if self.bgsub_type=="MagAbs":
            return self.bgsub(magabs) #return  (magabs-magabs[:,0]).transpose()
        return magabs

    @tag_property(plot=True, sub=True)
    def MagAbs_sq(self):
        return (self.MagAbs)**2

    @tag_property(plot=True, sub=True)
    def Phase(self):
        return angle(self.Magcom)

    @tag_property(sub=True)
    def Magcom(self):
        self.get_member("MagAbs").reset(self)
        self.get_member("MagAbs_sq").reset(self)
        self.get_member("MagdB").reset(self)
        self.get_member("Phase").reset(self)
        if self.filter_type=="None":
            Magcom=self.MagcomData
        elif self.filter_type=="Fit":
            Magcom=self.MagcomFit
        else:
            Magcom=self.MagcomFilt
        if self.bgsub_type=="Complex":
            return self.bgsub(Magcom) #(Magcom-Magcom[:,0]).transpose()
        return Magcom

    #@tag_property(plot=True, sub=True)
    #def MagAbsFilt(self):
    #    return absolute(self.MagcomFilt)#.transpose()-absolute(self.MagcomFilt[:,0])).transpose()

    #@tag_property(plot=True, sub=True)
    #def MagdBFilt(self):
    #    return 10.0*log10(self.MagAbsFilt)

    @tag_property(sub=True)
    def ifft_time(self):
        return self.filt.ifft_x(self.frequency)

    @tag_property(plot=True, sub=True)
    def MagcomFilt(self):
        if self.filt.filter_type=="FFT":
            return array([self.filt.fft_filter(self.MagcomData[:,n]) for n in range(len(self.yoko))]).transpose()
        return array([self.filt.fir_filter(self.MagcomData[:,n]) for n in range(len(self.yoko))]).transpose()
#
#        if self.filter_type=="Boxcar":
#            pass
#        elif self.filter_type=="FIR":
#            pass
#        #phase=angle(self.Magcom)
#        #phasefilt=(phase.transpose()-phase[:,0]).transpose()
#        #mc=absolute(self.Magcom)*(cos(phasefilt)+1j*sin(phasefilt))
#
#        #return array([fft_filter4(self.Magcom[:,n], self.filt_center) for n in range(len(self.yoko))]).transpose()
#        return array([fft_filter3(self.MagcomData[:,n], self.filt_start_ind, self.filt_end_ind) for n in range(len(self.yoko))]).transpose()


    @tag_property(sub=True)
    def MagAbsFit(self):
        if self.fit_type=="yoko":
            return sqrt(array([self.fit_func(self.yoko, fp) for fp in self.fit_params]))
        return sqrt(array([self.fit_func(self.fq, fp) for fp in self.fit_params]))

    #@tag_property(sub=True)
    #def MagdBFit(self):
    #    return 10*log10(self.MagAbsFit)

    @tag_property(sub=True)
    def fit_params(self):
        #if self.fit_type=="yoko":
        #    return self.
        return self.full_fano_fit(self.fq)

    #@plots
    def widths_plot(self, pl=None):
        scatter(self.frequency[self.indices]/1e9, absolute([fp[0] for fp in self.fit_params]), plotter=pl)
        line(self.frequency/1e9, self.qdt._get_coupling(self.frequency), plotter=pl, color="red")
        return pl

    #@plots
    def center_plot(self, pl=None):
        line(self.frequency[self.indices]/1e9, array([fp[1] for fp in self.fit_params]), plotter=pl)
        line(self.frequency/1e9, self.ls_f, plotter=pl, color="red", linewidth=1.0)
        return pl

    #@plots
    def heights_plot(self, pl=None):
        pl, pf=line(self.frequency[self.indices]/1e9, array([fp[3]-fp[2] for fp in self.fit_params]))
        return pl

    #@plots
    def background_plot(self, pl=None):
        pl, pf=line(self.frequency[self.indices]/1e9, array([fp[2]+fp[3] for fp in self.fit_params]))
        line(self.frequency[self.indices]/1e9, self.MagAbsFilt_sq[self.indices,0], plotter=pl, color="red")
        return pl


    def magabs_colormesh(self, **kwargs):
        pl=kwargs.pop("pl", "magabs{0}{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
        self.get_member("Magcom").reset(self)
        pl, pf=colormesh(self.yoko, self.frequency/1e9, self.MagAbs, pl=pl, **kwargs)
        pl.set_ylim(min(self.frequency/1e9), max(self.frequency/1e9))
        pl.set_xlim(min(self.yoko), max(self.yoko))
        pl.xlabel="Yoko (V)"
        pl.ylabel="Frequency (GHz)"
        return pl

#    def ifft_plot(self):
#        p, pf=line(absolute(fft.ifft(self.MagcomData[:,self.on_res_ind])), plotter="ifft_{}".format(self.name),
#               plot_name="onres_{}".format(self.on_res_ind),label="i {}".format(self.on_res_ind), color="red")
#        line(absolute(fft.ifft(self.MagcomData[:,self.start_ind])), plotter=p, linewidth=1.0,
#             plot_name="strt {}".format(self.start_ind), label="i {}".format(self.start_ind))
#        line(absolute(fft.ifft(self.MagcomData[:,self.stop_ind])), plotter=p, linewidth=1.0,
#             plot_name="stop {}".format(self.stop_ind), label="i {}".format(self.stop_ind))
#        return p

    def ifft_plot(self, **kwargs):
        pl=kwargs.pop("pl", "hannifft{0}{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))

        on_res=absolute(self.filt.window_ifft(self.MagcomData[:,self.on_res_ind]))
        strt=absolute(self.filt.window_ifft(self.MagcomData[:,self.start_ind]))
        stop=absolute(self.filt.window_ifft(self.MagcomData[:,self.stop_ind]))

        pl, pf=line(on_res, pl=pl, color="red",
               plot_name="onres_{}".format(self.on_res_ind),label="i {}".format(self.on_res_ind))
        line(strt, pl=pl, linewidth=1.0,
             plot_name="strt {}".format(self.start_ind), label="i {}".format(self.start_ind))
        line(stop, pl=pl, linewidth=1.0,
             plot_name="stop {}".format(self.stop_ind), label="i {}".format(self.stop_ind))

        self.filt.length=len(on_res)
        filt=self.filt.freqz
        #filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
        top=max([amax(on_res), amax(strt), amax(stop)])
        line(filt*top, plotter=pl, color="green")
        return pl

    def MagdB_cs(self, pl, ind):
        pl, pf=line(self.frequency, self.MagdB[:, ind], label="MagAbs (unfiltered)", plotter="filtcomp_{}".format(self.name))
        line(self.frequency, self.MagdBFilt[:, ind], label="MagAbs (filtered)", plotter=pl)
        return pl

    #@plots
    def filt_compare(self, ind):
        pl, pf=line(self.frequency, self.MagdB[:, ind], label="MagAbs (unfiltered)", plotter="filtcomp_{}".format(self.name))
        line(self.frequency, self.MagdBFilt[:, ind], label="MagAbs (filtered)", plotter=pl)
        return pl

    #@plots
    def ls_magabsfilt_colormesh(self, pl=None):
        colormesh(self.flux_over_flux0[10:-10], self.ls_f[10:-10]/1e9,
                        self.MagAbsFilt[10:-10, 10:-10], plotter=pl)#"magabsfilt_{}".format(self.name))
        return pl

    #@plots
    def magabsfilt_colormesh(self, pl=None, xlabel="$\Phi/\Phi_0$", ylabel="Frequency (GHz)"):
        colormesh(self.flux_over_flux0[10:-10], self.frequency[10:-10]/1e9,
                        self.MagAbsFilt[10:-10, 10:-10], #plot_name="magabsfiltf_{}".format(self.name),
                        plotter=pl, xlabel=xlabel, ylabel=ylabel)
        return pl

    #@plots
    def ls_magabsfit_colormesh(self, pl=None, xlabel="$\Phi/\Phi_0$", ylabel="Frequency (GHz)"):
        colormesh(self.flux_over_flux0[10:-10], self.ls_f[self.indices][10:-10]/1e9,
                        self.MagAbsFit[10:-10, 10:-10], plotter=pl, xlabel=xlabel, ylabel=ylabel)
    #@plots
    def magabsfit_colormesh(self, pl=None, xlabel="$\Phi/\Phi_0$", ylabel="Frequency (GHz)"):
        colormesh(self.flux_over_flux0[10:-10], self.frequency[self.indices][10:-10]/1e9,
                        self.MagAbsFit[10:-10, 10:-10], plotter=pl, xlabel=xlabel, ylabel=ylabel)

    #@plots
    def flux_line(self, pl=None, xlabel="$\Phi/\Phi_0$", ylabel="Frequency (GHz)"):
        xmin, xmax, ymin, ymax=pl.x_min, pl.x_max, pl.y_min, pl.y_max
        line(self.flux_over_flux0[10:-10], self.fq[10:-10]/1e9, plotter=pl, xlabel=xlabel, ylabel=ylabel)
        pl.x_min, pl.x_max, pl.y_min, pl.y_max=xmin, xmax, ymin, ymax
        pl.xlabel="$\Phi/\Phi_0$"
        pl.ylabel="Frequency (GHz)"
        return pl

    def magphasefilt_colormesh(self):
        phasefilt=angle(self.MagcomFilt[10:-10, 10:-10])
        #phasefilt=array([unwrap(phase[:,n], discont=5.5) for n in range(phase.shape[1])])
        phasefilt=(phasefilt.transpose()-phasefilt[:,0]).transpose()
        phasefilt=unwrap(phasefilt, discont=3.0, axis=1)
        #phasefilt=phasefilt-phasefilt[0, :]
        pl, pf=colormesh(self.flux_over_flux0[10:-10], self.frequency[10:-10]/1e9,
                         phasefilt, plotter="magphasefilt_{}".format(self.name))
        #print self.voltage_from_flux_par2[0].shape,self.voltage_from_flux_par2[1].shape
        #line(self.voltage_from_flux_par2[0]/1e9, self.voltage_from_flux_par2[1], plotter=p)
        #print max(self.voltage_from_flux_par), min(self.voltage_from_flux_par)
        pl.xlabel="Yoko (V)"
        pl.ylabel="Frequency (GHz)"
        return pl

    def magabsfilt2_colormesh(self):
        p, pf=colormesh(self.frequency[10:-10]/1e9, self.yoko[10:-10],
                        self.MagAbsFilt.transpose()[10:-10, 10:-10], plotter="magabsfilt2_{}".format(self.name))
        print self.voltage_from_flux_par2[0].shape,self.voltage_from_flux_par2[1].shape
        line(self.voltage_from_flux_par2[0]/1e9, self.voltage_from_flux_par2[1], plotter=p)
        #print max(self.voltage_from_flux_par), min(self.voltage_from_flux_par)
        p.xlabel="Yoko (V)"
        p.ylabel="Frequency (GHz)"
        return p

    def magdBfilt_colormesh(self):
        return colormesh(self.yoko, self.frequency/1e9, self.MagdBFilt, plotter="magdBfilt_{}".format(self.name),
                    xlabel="Yoko (V)", ylabel="Frequency (GHz)")

    def magdBfiltbgsub_colormesh(self):
        return colormesh(self.yoko, self.frequency/1e9, (self.MagdBFilt.transpose()-self.MagdBFilt[:, self.start_ind]).transpose(),
                         plotter="magdBfiltbgsub_{}".format(self.name), xlabel="Yoko (V)", ylabel="Frequency (GHz)")

    @tag_property(plot=True, sub=True)
    def MagAbsFilt_sq(self):
        return (self.MagAbsFilt)**2

    def full_fano_fit(self, fq):
        log_debug("started fano fitting")
        fit_params=[self.fano_fit(n, fq)  for n in self.indices]
        #fit_params=array(zip(*fit_params))
        log_debug("ended fano fitting")
        return fit_params

    def full_fano_fit2(self):
        MagAbsFilt_sq=self.MagAbsFilt**2
        return full_fano_fit(self.fit_func, self.p_guess, MagAbsFilt_sq, self.fq, indices=self.indices)

        #fit_params=[full_fano_fit(self.fit_func, self.p_guess, MagAbsFilt_sq[n, :], self.fq) for n in self.indices]
        #fit_params=array(zip(*fit_params))
        #return fit_params

    def full_fano_fit3(self):
        MagAbsFilt_sq=self.MagAbsFilt**2
        return full_fit(lorentzian2, self.p_guess, MagAbsFilt_sq, self.fq, indices=self.indices)

    def plot_widths(self, plotter=None):
        fit_params=self.full_fano_fit()
        scatter(fit_params[0, :], absolute(fit_params[1, :]), color="red", label=self.name, plot_name="widths_{}".format(self.name), plotter=plotter)

    def resid_func(self, p, y, x):
        """residuals of fitting function"""
        return y-self.fit_func(x, p)

    def fano_fit(self, n, fq):
        dat=self.MagAbsFilt_sq[n, :]
        datamax=max(dat)
        datamin=min(dat)
        if self.fit_type=="yoko":
            p_guess=[0.2, self.yoko[self.on_res_ind], datamax-datamin, dat[0]]
            pbest= leastsq(self.resid_func, p_guess, args=(dat, self.yoko), full_output=1)
        else:
            p_guess=[self.qdt._get_coupling(self.frequency[n]), self.ls_f[n], datamax-datamin, dat[0]]
            pbest= leastsq(self.resid_func, p_guess, args=(dat, fq), full_output=1)
        best_parameters = pbest[0]
        return (best_parameters[0], best_parameters[1], best_parameters[2], best_parameters[3])

class TransLyzer(Lyzer):
    def _default_fit_func(self):
        return lorentzian

    def _default_fit_type(self):
        return "Transmission"

class ReflLyzer(Lyzer):
    def _default_fit_func(self):
        return refl_lorentzian

    def _default_fit_type(self):
        return "Reflection"
