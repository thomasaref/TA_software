# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:43:28 2016

@author: thomasaref

Collection of functions put into a format for easy use of scipy.optimize's leastsq fit
"""
from scipy.optimize import leastsq, curve_fit
from numpy import array


def fano_fit(resid_func, p_guess, y, x):
    pbest= leastsq(resid_func, p_guess, args=(y, x), full_output=1)
    best_parameters = pbest[0]
    return (best_parameters[0], best_parameters[1], best_parameters[2], best_parameters[3])

def full_fano_fit(fit_func, p_guess, y, x, indices=None):
    print "started fano fitting"
    if indices is None:
        indices=range(len(y))
    def residuals(p, y, x):
        """residuals of fitting function"""
        return y-fit_func(x, p)
    fit_params=[fano_fit(residuals, p_guess, y[n], x)  for n in indices]
    fit_params=array(zip(*fit_params))
    print "ended fano fitting"
    return fit_params

def lorentzian(x,p):
    return p[2]*(((x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def refl_lorentzian(x,p):
    return p[2]*(p[0]**2/(p[0]**2+(x-p[1])**2))+p[3]

def fano(x, p):
    return p[2]*(((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def refl_fano(x, p):
    return p[2]*(1.0-((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

def rpt_fit(fit_func, p_guess, y, x):
    popt, pcov= curve_fit(fit_func, x, y, p0=p_guess)
    return popt #best_parameters = pbest[0]
    #return (best_parameters[0], best_parameters[1], best_parameters[2], best_parameters[3])

def full_fit(fit_func, p_guess, y, x, indices=None):
    print "started fitting"
    if indices is None:
        indices=range(len(y))
    fit_params=[rpt_fit(fit_func, p_guess, y[n], x)  for n in indices]
    fit_params=array(zip(*fit_params))
    print "ended fitting"
    return fit_params