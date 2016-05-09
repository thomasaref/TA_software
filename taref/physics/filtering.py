# -*- coding: utf-8 -*-
"""
Created on Sun May  8 11:19:59 2016

@author: thomasaref
"""

from scipy.signal import hann, boxcar, freqz, firwin, lfilter, filtfilt, flattop, blackmanharris
from numpy import hanning, append, zeros, log10, absolute, unwrap, arctan2, imag, real, fft, angle



def fft_filter(Magcom, filt_start_ind=0, filt_end_ind=0):
    """original fft filter func. essentially a boxcar window"""
    myifft=fft.ifft(Magcom)
    if filt_end_ind!=0:
        myifft[filt_end_ind:-filt_end_ind]=0.0
    if filt_start_ind!=0:
        myifft[:filt_start_ind]=0.0
        myifft[-filt_start_ind:]=0.0
    return fft.fft(myifft)

def filt_prep(length, start_ind, stop_ind, filt_func=hann):
    filt=zeros(length)
    if stop_ind==0:
        stop_ind=length
    filt[start_ind:stop_ind]=filt_func(stop_ind-start_ind)
    return filt

def fft_filter2(Magcom, filt_start_ind=0, filt_end_ind=0, filt_func=hann):
    """filtering with window function defaulting to hann"""
    filt=filt_prep(len(Magcom), filt_start_ind, filt_end_ind, filt_func=filt_func)
    return fft.fft(fft.ifft(Magcom)*filt)

def hann_ifft(Magcom):
    """hann windows the data before applying an ifft"""
    return fft.ifft(Magcom*hann(len(Magcom)))

def fft_filter3(Magcom, filt_start_ind=0, filt_end_ind=0, filt_func=hann):
    """hann windows the data before filtering and then divides by hann window at the end"""
    filt=filt_prep(len(Magcom), filt_start_ind, filt_end_ind, filt_func=filt_func)
    return fft.fft(hann_ifft(Magcom)*filt)/hann(len(Magcom))

def fft_filter4(Magcom, filt_center=0):
    filt=zeros(len(Magcom))
    filt[filt_center]=1
    return fft.fft(hann_ifft(Magcom)*filt)/hann(len(Magcom))

def filt_prep2(length, start_ind, stop_ind, numtaps=101, window="flattop"):
    return firwin(numtaps, [start_ind, stop_ind], pass_zero=False, nyq=length, window=window)

#def filt_prep3(length, start_ind, stop_ind, n=1001, window="flattop"):#blackmanharris
#    """creates a bandpass filter by creating a lowpass and highpass fir filters,
#    using spectral inversion to merge the two"""
#    a=firwin(n, cutoff = start_ind, window=window, nyq=length)
#    b = - firwin(n, cutoff = stop_ind, window = window, nyq=length)
#    b[n/2] = b[n/2] + 1
#    d = - (a+b)
#    d[n/2] = d[n/2] + 1
#    return d
#
def fft_filter5(Magcom, filt_start_ind=0, filt_end_ind=0, window='flattop'):
    filt=filt_prep2(len(Magcom), filt_start_ind, filt_end_ind, window=window)#, numtaps=len(Magcom))
    return filtfilt(filt, [1.0], Magcom)#[:, len(filt) - 1:]
#    #return convolve(Magcom, filt)# mode='valid')
#    return fftconvolve(Magcom, filt)#b[np.newaxis, :], mode='valid')
#
#def fft_filter5(Magcom, filt_start_ind=0, filt_end_ind=0, filt_func=hann):
#
#    filt=filt_prep(len(Magcom), filt_start_ind, filt_end_ind, filt_func=filt_func)
#    return fftconvolve(filt, Magcom) #fft.fft(hann_ifft(Magcom)*filt)/hann(len(Magcom))
#



if __name__=="__main__":
    from numpy.random import randn
    from numpy.fft import rfft
    from numpy import zeros, sin, arange
    import matplotlib.pyplot as plt
    #td=filt_prep(101, 30,31, filt_func=boxcar)
    #td2=filt_prep(101, 10,11, filt_func=boxcar)

    #td_ifft=fft.fftshift(fft.ifft(td+td2))
    filt=filt_prep2(800, 15,25, 200)#, "blackmanharris")
    #impulse = zeros(1000)
    #impulse[500] = 1
    #imp_ff = filtfilt(filt, [1.0], impulse)
    #imp_lf = lfilter(filt, [1.0], lfilter(filt, [1.0], impulse))
    #plt.plot(20*log10(absolute(rfft(imp_lf))))

    #plt.plot(20*log10(absolute(rfft(imp_ff))))


    sig = sin(3.14*arange(800)/20.0)+0.1*randn(800)  # Brownian noise
    plt.plot(absolute(fft.ifft(sig)))
    print "start filt"
    sig_ff = filtfilt(filt, [1.0], sig)
    print "end filt"
    sig_f=fft_filter3(sig, 15, 25, blackmanharris)
    #sig_lf = lfilter(filt, [1.0], lfilter(filt, [1.0], sig))
    plt.figure()
    plt.plot(sig, color='silver', label='Original')
    plt.plot(sig_ff, color='#3465a4', label='filtfilt')
    plt.plot(absolute(sig_f), color='#cc0000', label='lfilter')
    plt.legend(loc="best")
    plt.ylim(-1, 1)
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
