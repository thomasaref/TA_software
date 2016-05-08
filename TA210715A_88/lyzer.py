# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 12:42:53 2016

@author: thomasaref
"""

from taref.core.api import Agent, Array, tag_property, log_debug, s_property
from taref.filer.read_file import Read_HDF5
from taref.physics.qdt import QDT
from taref.physics.fitting_functions import fano, lorentzian, refl_lorentzian, full_fano_fit, full_fit
from taref.physics.filtering import fft_filter, hann_ifft, fft_filter2, fft_filter3, filt_prep
from taref.plotter.api import line, colormesh, scatter
from atom.api import Float, Typed, Unicode, Int, Callable, Enum, List
from h5py import File
from numpy import float64, shape, reshape, linspace, squeeze, fft, log10, absolute, array, amax, amin
from scipy.optimize import leastsq, curve_fit
from taref.physics.qdt import QDT

class LyzerBase(Agent):
    qdt=QDT()
    base_name="lyzer_base"
    fridge_atten=Float(60)
    fridge_gain=Float(45)

    rd_hdf=Typed(Read_HDF5)
    rt_atten=Float(40)
    rt_gain=Float(23*2)

    offset=Float(-0.035)
    flux_factor=Float(0.2925)

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
        print sy
        s=(sm, sy[0], 1)#sy[2])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        self.Magcom=squeeze(Magcom)
        self.stop_ind=len(self.yoko)-1

class Lyzer(LyzerBase):
    base_name="lyzer"
    #def _default_main_params(self):
    #    return ["rt_atten", "fridge_atten", "fridge_gain", "rt_gain", "comment", "flux_factor", "offset", "fit_type",
    #            "on_res_ind", "start_ind", "stop_ind", "filt_start_ind", "filt_end_ind"]

    frequency=Array().tag(unit="GHz", plot=True, label="Frequency", sub=True)
    yoko=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    #pwr=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    #frq2=Array().tag(unit="V", plot=True, label="Yoko", sub=True)
    Magcom=Array().tag(sub=True)
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")

    on_res_ind=Int()
    start_ind=Int()
    stop_ind=Int()
    filt_center=Int()
    filt_halfwidth=Int()
    indices=List()
    port_name=Unicode('S21')
    VNA_name=Unicode("RS VNA")
    #filt_end_ind=Int(58)
    #filt_start_ind=Int(5)

    @tag_property()
    def filt_start_ind(self):
        return self.filt_center-self.filt_halfwidth+1

    @tag_property()
    def filt_end_ind(self):
        return self.filt_center+self.filt_halfwidth#-1

    #@s_property()
    #def filt_center_ind(self, filt_start_ind, filt_end_ind):
    #    return (filt_start_ind+filt_end_ind)/2

    #@filt_center_ind.setter
    #def _get_filt_start_ind(self, filt_center_ind, filt_width):
    #    return

    #def _get_filt_end_ind(self, filt_center_ind, filt_width):
    #    return

    #@s_property()
    #def filt_width(self, filt_start_ind, filt_end_ind):
    #    return filt_end_ind-filt_start_ind

    #@filt_center_ind.setter
    #def _get_filt_start_ind(self, filt_center_ind, filt_width):
    #    return (2*filt_center_ind-filt_width)/2

    #@filt_width.setter
    #def _get_filt_start_ind_get_(self, filt_width, filt_center_ind):
    #    return (2*filt_center_ind-filt_width)/2

    #@filt_center_ind.setter
    #def _get_filt_end_ind(self, filt_center_ind, filt_width):
    #    return (2*filt_center_ind+filt_width)/2

    #@filt_width.setter
    #def _get_filt_end_ind_get_(self, filt_width, filt_center_ind):
    #    return (2*filt_center_ind+filt_width)/2

    fit_func=Callable(fano).tag(private=True)
    read_data=Callable(read_data).tag(sub=True)

    fit_type=Enum("Transmission", "Reflection")

    @tag_property(plot=True, sub=True)
    def fq(self):
        return self.qdt._get_fq(Ej=self.Ej, Ec=self.qdt.Ec)

    @tag_property(plot=True, sub=True)
    def Ej(self):
        return self.qdt._get_Ej(Ejmax=self.qdt.Ejmax, flux_over_flux0=self.flux_over_flux0)

    @tag_property(sub=True)
    def flux_over_flux0(self):
        return self.qdt._get_flux_over_flux0(voltage=self.yoko, offset=self.offset, flux_factor=self.qdt.flux_factor)

    @tag_property()
    def p_guess(self):
        return [200e6,4.5e9, 0.002, 0.022, 0.1]

    def _default_indices(self):
        return range(len(self.frequency))
        #return [range(81, 120+1), range(137, 260+1), range(269, 320+1), range(411, 449+1)]#, [490]]#, [186]]

    def fft_filter(self, n):
        myifft=fft.ifft(self.Magcom[:,n])
        myifft[self.filt_end_ind:-self.filt_end_ind]=0.0
        if self.filt_start_ind!=0:
            myifft[:self.filt_start_ind]=0.0
            myifft[-self.filt_start_ind:]=0.0
        return fft.fft(myifft)

    @tag_property(plot=True, sub=True)
    def MagdB(self):
        return 10.0*log10(self.MagAbs)

    @tag_property(plot=True, sub=True)
    def MagAbs(self):
        return absolute(self.Magcom)

    @tag_property(plot=True, sub=True)
    def MagAbsFilt(self):
        return absolute(self.MagcomFilt)

    @tag_property(plot=True, sub=True)
    def MagdBFilt(self):
        return 10.0*log10(self.MagAbsFilt)

    @tag_property(plot=True, sub=True)
    def MagcomFilt(self):
        #return array([fft_filter4(self.Magcom[:,n], self.filt_center) for n in range(len(self.yoko))]).transpose()
        return array([fft_filter3(self.Magcom[:,n], self.filt_start_ind, self.filt_end_ind) for n in range(len(self.yoko))]).transpose()

    def magabs_colormesh(self):
        pl, pf=colormesh(self.yoko, self.frequency/1e9, self.MagAbs, plotter="magabs_{}".format(self.name))
        pl.set_ylim(min(self.frequency/1e9), max(self.frequency/1e9))
        pl.set_xlim(min(self.yoko), max(self.yoko))
        pl.xlabel="Yoko (V)"
        pl.ylabel="Frequency (GHz)"
        return pl

    def ifft_plot(self):
        p, pf=line(absolute(fft.ifft(self.Magcom[:,self.on_res_ind])), plotter="ifft_{}".format(self.name),
               plot_name="onres_{}".format(self.on_res_ind),label="i {}".format(self.on_res_ind), color="red")
        line(absolute(fft.ifft(self.Magcom[:,self.start_ind])), plotter=p, linewidth=1.0,
             plot_name="strt {}".format(self.start_ind), label="i {}".format(self.start_ind))
        line(absolute(fft.ifft(self.Magcom[:,self.stop_ind])), plotter=p, linewidth=1.0,
             plot_name="stop {}".format(self.stop_ind), label="i {}".format(self.stop_ind))
        return p

    def hann_ifft_plot(self):
        on_res=hann_ifft(self.Magcom[:,self.on_res_ind])
        strt=hann_ifft(self.Magcom[:,self.start_ind])
        stop=hann_ifft(self.Magcom[:,self.stop_ind])

        p, pf=line(absolute(on_res), plotter="hann_ifft_{}".format(self.name), color="red",
               plot_name="onres_{}".format(self.on_res_ind),label="i {}".format(self.on_res_ind))
        line(absolute(strt), plotter=p, linewidth=1.0,
             plot_name="strt {}".format(self.start_ind), label="i {}".format(self.start_ind))
        line(absolute(stop), plotter=p, linewidth=1.0,
             plot_name="stop {}".format(self.stop_ind), label="i {}".format(self.stop_ind))

        filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
        top=max([amax(absolute(on_res)), amax(absolute(strt)), amax(absolute(stop))])
        line(filt*top, plotter=p, color="green")

        return p

    def filt_compare(self, ind):
        p, pf=line(self.frequency, self.MagdB[:, ind], label="MagAbs (unfiltered)", plotter="filtcomp_{}".format(self.name))
        line(self.frequency, self.MagdBFilt[:, ind], label="MagAbs (filtered)", plotter=p)

    def magabsfilt_colormesh(self):
        p, pf=colormesh(self.yoko[10:-10], self.frequency[10:-10]/1e9, self.MagAbsFilt[10:-10, 10:-10], plotter="magabsfilt_{}".format(self.name))
        p.set_ylim(min(self.frequency[10:-10]/1e9), max(self.frequency[10:-10]/1e9))
        p.set_xlim(min(self.yoko[10:-10]), max(self.yoko[10:-10]))
        #pf.set_clim(amin(self.MagAbsFilt), amax(self.MagAbsFilt))
        p.xlabel="Yoko (V)"
        p.ylabel="Frequency (GHz)"

    def magdBfilt_colormesh(self):
        return colormesh(self.yoko, self.frequency/1e9, self.MagdBFilt, plotter="magdBfilt_{}".format(self.name),
                    xlabel="Yoko (V)", ylabel="Frequency (GHz)")

    def magdBfiltbgsub_colormesh(self):
        return colormesh(self.yoko, self.frequency/1e9, (self.MagdBFilt.transpose()-self.MagdBFilt[:, self.start_ind]).transpose(),
                         plotter="magdBfiltbgsub_{}".format(self.name), xlabel="Yoko (V)", ylabel="Frequency (GHz)")

    def full_fano_fit(self):
        log_debug("started fano fitting")
        fit_params=[self.fano_fit(n)  for n in self.indices]
        fit_params=array(zip(*fit_params))
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
        return full_fit(self.fit_func, self.p_guess, MagAbsFilt_sq, self.fq, indices=self.indices)

    def plot_widths(self, plotter=None):
        fit_params=self.full_fano_fit()
        scatter(fit_params[0, :], absolute(fit_params[1, :]), color="red", label=self.name, plot_name="widths_{}".format(self.name), plotter=plotter)

    def resid_func(self, p, y, x):
        """residuals of fitting function"""
        return y-self.fit_func(x, p)

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

class ReflLyzer(Lyzer):
    def _default_fit_func(self):
        return refl_lorentzian

    def _default_fit_type(self):
        return "Reflection"
