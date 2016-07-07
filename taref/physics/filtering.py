# -*- coding: utf-8 -*-
"""
Created on Sun May  8 11:19:59 2016

@author: thomasaref
"""

from scipy.signal import hann, boxcar, freqz, firwin, lfilter, filtfilt, flattop, blackmanharris#, tukey
from numpy import hanning, append, zeros, log10, absolute, unwrap, arctan2, imag, real, fft, angle, linspace
from atom.api import Atom, Float, Int, Enum, Bool, cached_property, observe

import numpy as np

def tukey(M, alpha=0.5, sym=True):
    r"""Return a Tukey window, also known as a tapered cosine window.
    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an empty
        array is returned.
    alpha : float, optional
        Shape parameter of the Tukey window, representing the faction of the
        window inside the cosine tapered region.
        If zero, the Tukey window is equivalent to a rectangular window.
        If one, the Tukey window is equivalent to a Hann window.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.
    Returns
    -------
    w : ndarray
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).
    References
    ----------
    .. [1] Harris, Fredric J. (Jan 1978). "On the use of Windows for Harmonic
           Analysis with the Discrete Fourier Transform". Proceedings of the
           IEEE 66 (1): 51-83. doi:10.1109/PROC.1978.10837
    .. [2] Wikipedia, "Window function",
           http://en.wikipedia.org/wiki/Window_function#Tukey_window
    Examples
    --------
    Plot the window and its frequency response:
    >>> from scipy import signal
    >>> from scipy.fftpack import fft, fftshift
    >>> import matplotlib.pyplot as plt
    >>> window = signal.tukey(51)
    >>> plt.plot(window)
    >>> plt.title("Tukey window")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")
    >>> plt.ylim([0, 1.1])
    >>> plt.figure()
    >>> A = fft(window, 2048) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    >>> plt.plot(freq, response)
    >>> plt.axis([-0.5, 0.5, -120, 0])
    >>> plt.title("Frequency response of the Tukey window")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")
    """
    if M < 1:
        return np.array([])
    if M == 1:
        return np.ones(1, 'd')

    if alpha <= 0:
        return np.ones(M, 'd')
    elif alpha >= 1.0:
        return hann(M, sym=sym)

    odd = M % 2
    if not sym and not odd:
        M = M + 1

    n = np.arange(0, M)
    width = int(np.floor(alpha*(M-1)/2.0))
    n1 = n[0:width+1]
    n2 = n[width+1:M-width-1]
    n3 = n[M-width-1:]

    w1 = 0.5 * (1 + np.cos(np.pi * (-1 + 2.0*n1/alpha/(M-1))))
    w2 = np.ones(n2.shape)
    w3 = 0.5 * (1 + np.cos(np.pi * (-2.0/alpha + 1 + 2.0*n3/alpha/(M-1))))

    w = np.concatenate((w1, w2, w3))

    if not sym and not odd:
        w = w[:-1]
    return w

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

def fft_filt_prep(length, start_ind, stop_ind, filt_func="boxcar", reflect=True):
    """prepares a fft_filter consisting of a window around given start and stop indices. (fftshifted)"""
    filt_func=window_dict.get(filt_func, filt_func)
    filt=zeros(length)
    if stop_ind==0:
        stop_ind=length/2
    filt[length/2+start_ind:length/2+stop_ind]=filt_func(stop_ind-start_ind)
    if reflect:
        filt[length/2-stop_ind:length/2-start_ind]=filt_func(stop_ind-start_ind)
    return filt

def fft_filter(Magcom, window, filt, renormalize=True):
    """filtering with window and filt (window in ifft domain). Renormalize redivides by window to scale output"""
    filt_data=fft.fft(fft.ifftshift(fft.fftshift(window_ifft(Magcom, window=window))*filt))
    if renormalize:
        return filt_data/window
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
    return filtfilt(filt, [1.0], Magcom, padtype=padtype)

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

    @cached_property
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

    @cached_property
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

    @cached_property
    def freqz(self):
        print self.filter_type=="FIR"
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
    plt.figure()

    if 0:
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

    filt_start=450
    filt_end=550
    #plt.plot(sig)
    #plt.show()
    plt.plot(absolute(window_ifft(sig, shift=True, window="hann")))
    #plt.show()

    filt=fir_filt_prep(len(sig), filt_start, filt_end, numtaps=1000, window="flattop")#, window="blackmanharris")
    #plt.plot(filt)
    #print filt, part
    #plt.plot(fft.fftshift(absolute(freqz(filt, worN=len(sig), whole=True)[1])))
    plt.plot(absolute(fir_freqz(filt, len(sig), shift=True)))
    filt2=filt_prep(len(sig), filt_start, filt_end, shift=True, filt_func="boxcar", reflect=False)
    plt.plot(filt2)
    #plt.plot(absolute(window_ifft(sig, shift=False, window="hann"))*filt2)
    #plt.show()
    print "start filt"
    sig_ff = fir_filter(sig, filt_start_ind=filt_start, filt_end_ind=filt_end, window="flattop")
    print "end filt"
    print "start filt2"
    sig_ff2 = fft_filter(sig, filt_start_ind=filt_start, filt_end_ind=filt_end, renormalize=True,
                         window="hann", filt_func="boxcar", reflect=False)
    print "end filt2"

    plt.figure()
    plt.plot(absolute(sig[50:-50]))
    plt.plot(absolute(sig_ff[50:-50]))
    plt.plot(absolute(sig_ff2[50:-50]))
    #plt.plot(absolute(fft_filter_old(sig, 60, 100)))
    plt.show()

    #sig_f=fft_filter3(sig, 15, 25, blackmanharris)
    #sig_lf = lfilter(filt, [1.0], lfilter(filt, [1.0], sig))
    #plt.figure()
    #plt.plot(sig, color='silver', label='Original')
    #plt.plot(sig_ff, color='#3465a4', label='filtfilt')
    #plt.plot(absolute(sig_f), color='#cc0000', label='lfilter')
    #plt.legend(loc="best")
    #plt.ylim(-1, 1)
    #td_f=lfilter(filt, [1.0], td_ifft)
    #plt.plot(td_ifft)
    #plt.plot(td_f, '.')
    #w,h = freqz(filt, worN=101)
    #plt.plot(20*log10(absolute(h)))
    #plt.plot(unwrap(angle(h)))
    #filt=filt_prep3(101, 30,35)
    #w,h = freqz(filt, worN=101)
    #plt.plot(20*log10(absolute(h)))
    #plt.plot(unwrap(angle(h)))
#
#    plt.plot(absolute(freqz(filt, worN=400)[1]))
#
#    plt.show()
#
#    filt=filt_prep(101, 5, 50)
#    plt.plot(filt)
#    filt=filt_prep(101, 5, 50, hann)
#    plt.plot(filt)
#    filt=filt_prep(101, 5, 50, hanning)
#    plt.plot(filt)
#    filt=filt_prep2(101, 5, 50)
#    plt.plot(absolute(freqz(filt, worN=101)[1]))
#
#    plt.show()
