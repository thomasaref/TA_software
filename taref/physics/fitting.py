# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:43:28 2016

@author: thomasaref

Collection of functions put into a format for easy use of scipy.optimize's leastsq fit
"""
from scipy.optimize import leastsq, curve_fit
from numpy import array, amin, amax, argmin, argmax, mean, ndarray
from time import time
from atom.api import Atom, Enum, Float, Int, Callable, Typed#, cached_property
from taref.core.api import private_property

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
    #xmax=amax(sig)
    xmin=amin(sig) #xmean-xmin=fp2
    xmean=(mean(sig[:10])+mean(sig[-10:]))/2.0 #xmean=fp2+fp3
    return [gamma, x[argmin(sig)], xmean-xmin, xmin]

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

class LeastSqFitter(Atom):
    """Atom wrapper for least square fitting"""
    fit_func=Callable().tag(private=True)
    p_guess_func=Callable().tag(private=True)
    fit_params=Typed(ndarray)
    p_guess=Typed(ndarray)

    @private_property
    def resid_func(self):
        def residuals(p, x, y):
            return y-self.fit_func(x,p)
        return residuals

    def leastsq_fit(self, x, y, *args, **kwargs):
        pguess=self.p_guess_func(x, y, *args, **kwargs)
        pbest=leastsq(self.resid_func, pguess, args=(x, y), full_output=1)[0]
        return pbest

    def full_fit(self, x, y, indices=None, *args, **kwargs):
        print "started leastsq fitting"
        tstart=time()
        if indices is None:
            indices=range(len(y))
        fit_params=[self.leastsq_fit(x, y[n], *args, **kwargs)  for n in indices]
        self.fit_params=array(zip(*fit_params)).transpose()
        print "ended leastsq fitting {}".format(time()-tstart)
        return self.fit_params

    def make_p_guess(self, x, y, indices=None, *args, **kwargs):
        if indices is None:
            indices=range(len(y))
        pguess=[self.p_guess_func(x, y[n], *args, **kwargs) for n in indices]
        self.p_guess=array(zip(*pguess)).transpose()
        return self.p_guess

    def reconstruct_fit(self, x, fit_params=None):
        if fit_params is None:
            fit_params=self.fit_params
        return array([self.fit_func(x, fp) for fp in fit_params])

class LorentzianFitter(LeastSqFitter):
    """Atom wrapper for Lorentzian least square fitting"""
    fit_type=Enum("lorentzian", "refl_lorentzian")
    gamma=Float(1.0).tag(desc="width of peak for initial guess")
    end_indices=Int(10).tag(desc="indices to average for background guess")

    fit_func_dict={"lorentzian" : lorentzian,
                   "refl_lorentzian" : refl_lorentzian}

    p_guess_dict={"lorentzian" : lorentzian_p_guess,
                "refl_lorentzian" : refl_lorentzian_p_guess}

    @private_property
    def fit_func(self):
        return self.fit_func_dict[self.fit_type]

    @private_property
    def p_guess_func(self):
        return self.p_guess_dict[self.fit_type]

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

    a=LorentzianFitter()
    p0=array([3.2, 25.0, 1e-2, 0.3])
    spread=linspace(1.0, 2.0, 100)

    x=linspace(0.0, 100.0, 1000)
    sig=array([lorentzian(x, p0*sp_e)+1.0e-3*randn(len(x)) for sp_e in spread])#.transpose()
    pl, pf=colormesh(sig)

    #fd=a.leastsq_fit(sig[0,:], x)
    #print fd
    #pl, pf=line(x, sig[0,:])
    #print
    #line(x, a.reconstruct_fit(x, array([fd]).transpose()), pl=pl, color="red")
    #pl.show()
    #plt.plot(x, sig.transpose())
    #signorm, xmin, xmax=normalize(sig)
    #signorm=sig

    #fp1=full_fit(lorentzian2, lorentzian_p_guess, sig, x).transpose()
    #fit=lorentzian2(x, *fp)#denormalize(lorentzian(x, fp), xmin, xmax)
    #fit=array([lorentzian2(x, *fp_e) for fp_e in fp1])

    #plt.plot(x, fit)
    #colormesh(fit, pl=pl)

    a.full_fit(x, sig)
    colormesh(a.reconstruct_fit(x), pl=pl)
    fp=full_leastsq_fit(lorentzian, lorentzian_p_guess, sig, x).transpose()
    #print fp
    fit=array([lorentzian(x, fp_e) for fp_e in fp])
    #print fit.shape
    #denormalize(lorentzian(x, fp), xmin, xmax)
    #colormesh(fit, pl=pl)#[0].show()
    #pl, pf=line(fp[:, 0], color="red")
    pl, pf=line(a.fit_params[:, 0], color="red")

    #line(fp1[:,0], color="green", pl=pl)
    line(spread*3.2, pl=pl)
    pl.show()

    #plt.plot(x, fit.transpose())

    #plt.show()
