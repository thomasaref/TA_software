# -*- coding: utf-8 -*-
"""
Created on Sun May  8 11:19:59 2016

@author: thomasaref
"""

from scipy.signal import hann, boxcar, freqz, firwin, lfilter, filtfilt, flattop, blackmanharris, tukey, convolve, fftconvolve
from numpy import hanning, append, zeros, log10, absolute, unwrap, arctan2, imag, real, fft, angle, linspace, nan_to_num
from atom.api import Atom, Float, Int, Enum, Bool, cached_property, observe
from taref.core.api import private_property

window_dict=dict(boxcar=boxcar,
                 hann=hann,
                 flattop=flattop,
                 blackmanharris=blackmanharris,
                 tukey=tukey)

def ifft_x_Ndt(N, dt):
    """gives x axis of ifft (fftshifted)"""
    return linspace(-dt/2.0, dt/2.0, N)

def ifft_x_fs(fs):
    """gives x axis of ifft (fftshifted)"""
    N=len(fs)
    dt=1.0/(fs[1]-fs[0])
    return ifft_x_Ndt(N, dt)

def window(length, window_type="hann"):
    return window_dict.get(window_type, window_type)(length)

def window_ifft(Magcom, window):
    """windows the data before applying an ifft"""
    return fft.ifft(Magcom*window)

def fft_filt_prep(length, start_ind, stop_ind, filt_func="tukey", reflect=True):
    """prepares a fft_filter consisting of a window around given start and stop indices. (fftshifted)"""
    filt_func=window_dict.get(filt_func, filt_func)
    filt=zeros(length)
    if stop_ind==0:
        stop_ind=length/2
    filt[length/2+start_ind:length/2+stop_ind]=filt_func(stop_ind-start_ind)
    if reflect:
        filt[length/2-stop_ind:length/2-start_ind]=filt_func(stop_ind-start_ind)
    return filt

def fft_filter(Magcom, window, filt, renormalize=True, offset_from_zero=1.0e-12):
    """filtering with window and filt (window in ifft domain). Renormalize redivides by window to scale output"""
    filt_data=fft.fft(fft.ifftshift(fft.fftshift(window_ifft(Magcom, window=window))*filt))
    if renormalize:
        return filt_data/(window+offset_from_zero)
    return filt_data

def fir_filt_prep(length, start_ind, stop_ind, numtaps=1000, window="blackmanharris"):
    """preps the FIR filter."""
    if start_ind==0:
        return firwin(numtaps, stop_ind, pass_zero=True,
                  nyq=length/2.0,
                  window=window)
    return firwin(numtaps, [start_ind, stop_ind], pass_zero=False,
                  nyq=length/2.0,
                  window=window)

def fir_filter(Magcom, filt, padtype="odd"):
    """applies a FIR filter to data in Magcom"""
    return fftconvolve(Magcom, filt, mode="same")
    return filtfilt(filt, [1.0], Magcom, method="gust")

def fir_freqz(filt, length):
    """return complex frequency response of filter filt"""
    return freqz(filt, worN=length, whole=True)[1]


class Filter(Atom):
    """Atom wrapper for filtering functionality"""
    window_type=Enum("hann", "boxcar")
    fir_window=Enum("flattop", "blackmanharris")
    filt_func=Enum("tukey", "boxcar", "hann")
    reflect=Bool(False)
    renormalize=Bool(True)
    N=Int()
    numtaps=Int(1000)
    filter_type=Enum("FFT", "FIR")
    dt=Float()
    pad_type=Enum("odd", "even", "constant", None)

    center=Int()
    halfwidth=Int()

    @classmethod
    def fftshift(cls, result):
        return fft.fftshift(result)

    def _observe_filter_type(self, change):
        self.get_member("filt_prep").reset(self)
        self.get_member("freqz").reset(self)

    @observe("center", "halfwidth")
    def change_center_halfwidth(self, change):
        self.get_member("start_ind").reset(self)
        self.get_member("stop_ind").reset(self)


    @cached_property
    def start_ind(self):
        return self.center-self.halfwidth+1

    @cached_property
    def stop_ind(self):
        return self.center+self.halfwidth

    @private_property
    def window(self):
        return window(self.N, self.window_type)

    def ifft_x(self, fs=None):
        """gives x axis of ifft (fftshifted)"""
        if fs is not None:
            self.N=len(fs)
            self.dt=1.0/(fs[1]-fs[0])
        return ifft_x_Ndt(self.N, self.dt)

    def window_ifft(self, Magcom):
        """windows the data before applying an ifft"""
        if self.N==0:
            self.N=len(Magcom)
            self.get_member("window").reset(self)
        return window_ifft(Magcom, self.window)

    @private_property
    def filt_prep(self):
        if self.filter_type=="FFT":
            return fft_filt_prep(self.N, self.start_ind, self.stop_ind, filt_func=self.filt_func, reflect=self.reflect)
        return fir_filt_prep(self.N, self.start_ind, self.stop_ind, numtaps=self.numtaps, window=self.fir_window)

    def fft_filter(self, Magcom):
        return fft_filter(Magcom, window=self.window, filt=self.filt_prep, renormalize=self.renormalize)

    def fir_filter(self, Magcom):
        return fir_filter(Magcom, filt=self.filt_prep)

    def filtering(self, Magcom):
        if self.filter_type=="FFT":
            return self.fft_filter(Magcom)
        return self.fir_filter(Magcom)

    @private_property
    def freqz(self):
        if self.filter_type=="FIR":
            return fir_freqz(self.filt_prep, self.N)
        return self.filt_prep



if __name__=="__main__":
    from numpy import zeros, sin, arange, exp, pi
    import matplotlib.pyplot as plt
    from numpy.random import randn

    len_x=10000

    a=Filter(N=7, dt=1.5)
    print ifft_x_Ndt(7, 1.5), a.ifft_x()
    print ifft_x_fs(arange(5.0)), a.ifft_x(arange(5.0))
    print a.N, a.dt

    a.N=len_x
    plt.plot(window(len_x))
    plt.plot(a.window)

    x=linspace(0.1, 6.28, len_x)
    sig=sin(2*pi*38*x)+sin(2*pi*100*x)
    plt.figure()
    plt.plot(sig)

    if 0:
        plt.figure()
        t=ifft_x_fs(x)
        ifft_data=fft.fftshift(absolute(window_ifft(sig, window(len_x))))
        plt.plot(t, ifft_data)
        fft_filt=fft_filt_prep(len_x, 225, 250)
        plt.plot(t, fft_filt)
        fir_filt=fir_filt_prep(len_x, 225, 250, numtaps=3000)
        fir_frq=absolute(fft.fftshift(fir_freqz(fir_filt, len_x)))
        plt.plot(t, fir_frq)

    plt.figure()
    a.center=235
    a.halfwidth=14
    a.reflect=True
    a.filter_type="FFT"
    plt.plot(a.ifft_x(x), fft.fftshift(absolute(a.window_ifft(sig))))
    plt.plot(a.ifft_x(), a.freqz)
    a.filter_type="FIR"
    plt.plot(a.ifft_x(), fft.fftshift(absolute(a.freqz)))

    plt.figure()
    plt.plot(fft.fftshift(absolute(a.window_ifft(sig))))
    a.filter_type="FFT"
    plt.plot(a.freqz)
    a.filter_type="FIR"
    plt.plot(fft.fftshift(absolute(a.freqz)))

    #fir_filt=fir_filt_prep(len_x, 225, 250, numtaps=3000)
    #fir_frq=absolute(fft.fftshift(fir_freqz(fir_filt, len_x)))
    #plt.plot(t, fir_frq)

    plt.figure()
    a.filter_type="FFT"
    plt.plot(real(a.filtering(sig)))
    a.filter_type="FIR"
    plt.plot(a.filtering(sig))

    #plt.plot(fir_filter(sig, fir_filt))
    plt.ylim(-2,2)
    if 0:
        plt.figure()
        plt.plot(ifft_data)
        plt.plot(fft_filt)
        plt.plot(fir_frq)

        plt.figure()
        plt.plot(real(fft_filter(sig, window(len_x), fft_filt)))
        plt.plot(fir_filter(sig, fir_filt))
        plt.ylim(-2,2)
    plt.show()

    from numpy.fft import rfft
    #filt=fir_filt_prep(800, 250, 300, 1001)#, window="blackmanharris")
    #plt.plot(filt)

    #plt.plot(absolute(fft.fft(filt)))
    #if 0:
    #    impulse = zeros(1000)
    #    impulse[500] = 1
    #    plt.plot(absolute(window_ifft(impulse)))
    #    plt.show()
    #imp_ff = filtfilt(filt, [1.0], impulse)
    #imp_lf = lfilter(filt, [1.0], lfilter(filt, [1.0], impulse))
    #plt.plot(20*log10(absolute(rfft(imp_lf))))

    #plt.plot(20*log10(absolute(rfft(imp_ff))))

    len_x=10000

    impulse=zeros(len_x)
    impulse[0]=0.3
    impulse[500]=1.0
    impulse[1036]=0.25
    #plt.plot(impulse)
    sig=fft.fft(impulse+0.001*randn(len_x))
    plt.plot(absolute(sig))

    #plt.plot(absolute(fft.ifft(sig)))
    plt.show()
    #x=linspace(0.1, 800, len_x)#-300
    #sig = sin(3.14*x/100.0)*exp(0.1j*randn(800))+0.1*randn(800)  # Brownian noise
    #sig = sin(3.14*x/10.0)*exp(-3.14j*x/10.0)+sin(3.14*x/30.0)*exp(-3.14j*x/20.0)+0.1*randn(len_x)  # Brownian noise

