# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:43:28 2016

@author: thomasaref

Collection of functions put into a format for easy use of scipy.optimize's leastsq fit
"""
from scipy.optimize import leastsq, curve_fit
from numpy import array, amin, amax, argmin, argmax, mean
from time import time


def leastsq_fit(resid_func, p_guess_func, y, x, *args, **kwargs):
    p_guess=p_guess_func(x,y, *args, **kwargs)
    pbest= leastsq(resid_func, p_guess, args=(y, x), full_output=1)
    best_parameters = pbest[0]
    return (best_parameters[0], best_parameters[1], best_parameters[2], best_parameters[3])

def full_leastsq_fit(fit_func, p_guess_func, y, x, indices=None, *args, **kwargs):
    print "started leastsq fitting"
    tstart=time()
    if indices is None:
        indices=range(len(y))
    def residuals(p, y, x):
        """residuals of fitting function"""
        return y-fit_func(x, p)
    fit_params=[leastsq_fit(residuals, p_guess_func, y[n], x, *args, **kwargs)  for n in indices]
    fit_params=array(zip(*fit_params))
    print "ended leastsq fitting {}".format(time()-tstart)
    return fit_params

def lorentzian_p_guess(x, sig, gamma=1.0):
    xmax=amax(sig)
    #xmin=amin(sig)
    xmean=(mean(sig[:10])+mean(sig[-10:]))/2.0
    return [gamma, x[argmin(sig)], xmax-xmean, xmean]

def lorentzian(x,p):
    return p[2]*(((x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def lorentzian2(x,*p):
    return p[2]*(((x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def refl_lorentzian_p_guess(x, sig, gamma=1.0):
    xmax=amax(sig)
    xmin=amin(sig)
    return [gamma, x[argmax(sig)], xmax-xmin, xmax]

def refl_lorentzian(x,p):
    return p[2]*(p[0]**2/(p[0]**2+(x-p[1])**2))+p[3]

def fano(x, p):
    return p[2]*(((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def refl_fano(x, p):
    return p[2]*(1.0-((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def rpt_fit(fit_func, p_guess_func, y, x, *args, **kwargs):
    p_guess=p_guess_func(x,y, *args, **kwargs)
    popt, pcov= curve_fit(fit_func, x, y, p0=p_guess, maxfev=0)
    return popt #best_parameters = pbest[0]
    #return (best_parameters[0], best_parameters[1], best_parameters[2], best_parameters[3])

def full_fit(fit_func, p_guess_func, y, x, indices=None, *args, **kwargs):
    print "started fitting"
    tstart=time()
    if indices is None:
        indices=range(len(y))
    fit_params=[rpt_fit(fit_func, p_guess_func, y[n], x, *args, **kwargs)  for n in indices]
    fit_params=array(zip(*fit_params))
    print "ended fitting {}".format(time()-tstart)
    return fit_params

if __name__=="__main__":
    from numpy.random import randn
    from numpy import linspace
    #import matplotlib.pyplot as plt
    from taref.plotter.api import colormesh, line
    #from taref.physics.fundamentals import normalize

    def normalize(x):
        xmin=amin(x)
        xmax=amax(x)
        return (x-xmin)/(xmax-xmin), xmin, xmax

    def denormalize(xnorm, xmin, xmax):
        return xnorm*(xmax-xmin)+xmin

    p0=array([3.2, 25.0, 1e-2, 0.3])
    spread=linspace(1.0, 2.0, 100)

    x=linspace(0.0, 100.0, 1000)
    sig=array([lorentzian(x, p0*sp_e)+10.0e-3*randn(len(x)) for sp_e in spread])#.transpose()
    pl, pf=colormesh(sig)
    #plt.plot(x, sig.transpose())
    #signorm, xmin, xmax=normalize(sig)
    #signorm=sig

    #fp1=full_fit(lorentzian2, lorentzian_p_guess, sig, x).transpose()
    #fit=lorentzian2(x, *fp)#denormalize(lorentzian(x, fp), xmin, xmax)
    #fit=array([lorentzian2(x, *fp_e) for fp_e in fp1])

    #plt.plot(x, fit)
    #colormesh(fit, pl=pl)

    fp=full_leastsq_fit(lorentzian, lorentzian_p_guess, sig, x).transpose()
    print fp
    fit=array([lorentzian(x, fp_e) for fp_e in fp])
    print fit.shape
    #denormalize(lorentzian(x, fp), xmin, xmax)
    colormesh(fit, pl=pl)#[0].show()
    pl, pf=line(fp[:, 0], color="red")
    #line(fp1[:,0], color="green", pl=pl)
    line(spread*3.2, pl=pl)
    pl.show()

    #plt.plot(x, fit.transpose())

    #plt.show()
