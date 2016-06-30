# -*- coding: utf-8 -*-
"""
Created on Sun May  8 11:19:59 2016

@author: thomasaref
"""

from scipy.signal import hann, boxcar, freqz, firwin, lfilter, filtfilt, flattop, blackmanharris
from numpy import hanning, append, zeros, log10, absolute, unwrap, arctan2, imag, real, fft, angle, linspace

def fft_filter(Magcom, filt_start_ind=0, filt_end_ind=0):
    """original fft filter func. essentially a boxcar window"""
    myifft=fft.ifft(Magcom)
    if filt_end_ind!=0:
        myifft[filt_end_ind:-filt_end_ind]=0.0
    if filt_start_ind!=0:
        myifft[:filt_start_ind]=0.0
        myifft[-filt_start_ind:]=0.0
    return fft.fft(myifft)

def ifft_x(fs):
    """gives x axis of ifft (fftshifted)"""
    N=len(fs)
    df=1.0/(fs[1]-fs[0])/2.0
    return linspace(-df/2.0, df/2.0, N)

def window_ifft(Magcom, window=hann):
    """windows the data before applying an ifft"""
    return fft.fftshift(fft.ifft(Magcom*window(len(Magcom))))

def filt_prep(length, start_ind, stop_ind, filt_func=hann):
    """prepares a filter consisting of a window around given start and stop indices"""
    filt=zeros(length)
    if stop_ind==0:
        stop_ind=length
    filt[start_ind:stop_ind]=filt_func(stop_ind-start_ind)
    return filt

def window_fft_filter(Magcom, filt_start_ind=0, filt_end_ind=0, filt_func=hann, window=hann, renormalize=True):
    """filtering with window function defaulting to hann"""
    filt=filt_prep(len(Magcom), filt_start_ind, filt_end_ind, filt_func=filt_func)
    if renormalize:
        return fft.fft(fft.ifftshift(window_ifft(Magcom, window=window)*filt))/window(len(Magcom))
    return fft.fft(fft.ifftshift(window_ifft(Magcom, window=window)*filt))

def hann_ifft(Magcom):
    """hann windows the data before applying an ifft"""
    return fft.ftshift(fft.ifft(Magcom*hann(len(Magcom))))

def fft_filter3(Magcom, filt_start_ind=0, filt_end_ind=0, filt_func=hann):
    """hann windows the data before filtering and then divides by hann window at the end"""
    #newMagcom=Magcom #zeros(padlen*2+len(Magcom))
    #newMagcom[padlen:-padlen]=Magcom
    filt=filt_prep(len(Magcom), filt_start_ind, filt_end_ind, filt_func=filt_func)
    return fft.fft(hann_ifft(Magcom)*filt)/hann(len(Magcom))

def fft_filter4(Magcom, filt_center=0):
    filt=zeros(len(Magcom))
    filt[filt_center]=1
    return fft.fft(hann_ifft(Magcom)*filt)/hann(len(Magcom))

def fir_filt_prep(length, start_ind, stop_ind, numtaps=None, window="flattop"):
    if numtaps is None:
        numtaps=length/3
    return firwin(numtaps, [start_ind, stop_ind], pass_zero=False,
                  nyq=length/2.0,
                  window=window)

def fir_filter(Magcom, filt_start_ind=0, filt_end_ind=0, numtaps=None, window='blackmanharris'):
    filt=fir_filt_prep(len(Magcom), filt_start_ind, filt_end_ind, numtaps=numtaps, window=window)
    return filtfilt(filt, [1.0], Magcom)#[:, len(filt) - 1:]

if __name__=="__main__":
    from numpy.random import randn
    from numpy.fft import rfft
    from numpy import zeros, sin, arange
    import matplotlib.pyplot as plt
    filt=fir_filt_prep(800, 250, 300, 1001)#, window="blackmanharris")
    #plt.plot(filt)

    #plt.plot(absolute(fft.fft(filt)))
    if 0:
        impulse = zeros(1000)
        impulse[500] = 1
        plt.plot(absolute(window_ifft(impulse)))
        plt.show()
    #imp_ff = filtfilt(filt, [1.0], impulse)
    #imp_lf = lfilter(filt, [1.0], lfilter(filt, [1.0], impulse))
    #plt.plot(20*log10(absolute(rfft(imp_lf))))

    #plt.plot(20*log10(absolute(rfft(imp_ff))))


    sig = sin(3.14*arange(800)/10.0)+0.1*randn(800)  # Brownian noise
    plt.plot(absolute(window_ifft(sig)))
    filt=fir_filt_prep(len(sig), 30, 50)#, window="blackmanharris")
    #plt.plot(filt)

    plt.plot(fft.fftshift(absolute(freqz(filt, worN=len(sig), whole=True)[1])))

    print "start filt"
    sig_ff = fir_filter(sig, filt_start_ind=30, filt_end_ind=50, window="flattop")
    print "end filt"
    plt.figure()
    plt.plot(sig)
    plt.plot(sig_ff)
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

    plt.plot(absolute(freqz(filt, worN=400)[1]))

    plt.show()

    filt=filt_prep(101, 5, 50)
    plt.plot(filt)
    filt=filt_prep(101, 5, 50, hann)
    plt.plot(filt)
    filt=filt_prep(101, 5, 50, hanning)
    plt.plot(filt)
    filt=filt_prep2(101, 5, 50)
    plt.plot(absolute(freqz(filt, worN=101)[1]))

    plt.show()
