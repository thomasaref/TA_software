# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 14:01:26 2016

@author: thomasaref
"""

from atom.api import Float, Int, Atom, Bool, cached_property, Value
from numpy import append, interp, absolute, linspace, array
from taref.plotter.api import line, scatter
from scipy.special import legendre


def lgf(v, x, Nmax=2000, threshold=1.0e-5):
    """Series expression for Legendre function. Assumes |x|<1 and has problems converging for large v"""
    am=1.0
    cs=am
    for m in range(1, Nmax):
        am=(m-1.0-v)*(m+v)*(1.0-x)*am/(2.0*m**2)
        cs+=am
        if absolute(am)<threshold:
            break
    return cs

def lgf_fixed(x, Nmult=0, eval_neg=False, Nspacing=2001, Nmax=2000, threshold=1.0e-5):
    """uses recurrence relation and interpolation to expand range of Legendre function evaluation by multiples of Nmult.
    Evaulates negative Nmult symmetrically if eval_neg is True"""
    print Nspacing, eval_neg, Nmult
    v_arr=linspace(-1.0, 1.0, Nspacing)
    lgf_fix=array([lgf(v, x, Nmax, threshold) for v in v_arr])
    for n in range(Nmult):
        #print n
        v=linspace(n+1.0, n+2.0, 1001)
        lgf1=interp(v-1.0, v_arr, lgf_fix)
        lgf2=interp(v-2.0, v_arr, lgf_fix)
        lgf_fix=append(lgf_fix, (2.0*v-1.0)*x*lgf1/v-(v-1.0)*lgf2/v)
        v_arr=append(v_arr, v)
    if eval_neg:
        v_arr=append((-v_arr[1000:]-1)[::-1], v_arr)
        lgf_fix=append(lgf_fix[1000:][::-1], lgf_fix)
    print "lgf fixed done"
    return v_arr, lgf_fix

def lgf_arr(v, x, Nmult=None, eval_neg=False, Nspacing=2001, Nmax=2000, threshold=1.0e-5):
    """uses interpolation to evaluate Legendre function at given values of v_arr"""
    if Nmult is None:
        Nmult=int(max(v)+1)
    v_arr, lgf_fix=lgf_fixed(x, Nmult, eval_neg=eval_neg, Nspacing=Nspacing, Nmax=Nmax, threshold=threshold)
    return interp(v, v_arr, lgf_fix)

class Legendre(Atom):
    """wraps Legendre function evaluation in an Atom class"""
    threshold=Float(1.0e-5).tag(desc="threshold to evaluate sum coeffiecients too")
    Nmax=Int(2000).tag(desc="max iterations in sum")
    eval_neg=Bool(False).tag(desc="whether to extend fixed values to negative nu")
    Nspacing=Int(2001).tag(desc="spacing of -1 to 1 range for interpolation")

    Nmult=Int(0).tag(desc="number of extensions of -1 to 1 range of sum by recursion relation")

    x=Value().tag(private=True, desc="value to evaluate legendre at")

    def Pv(self, v, x=None, Nmult=None):
        if x is None:
            return interp(v, *self.fixed_leg)
        if Nmult is None:
            Nmult=self.calc_Nmult(v)
        self.x=x
        self.Nmult=Nmult
        self.fixed_reset()
        return interp(v, *self.fixed_leg)

    def calc_Nmult(self, v):
        if type(v) in (float, int):
            return int(v)+1
        return int(max(v)+1)

    def __init__(self, **kwargs):
        v=kwargs.pop("v", None)
        if v is not None:
            kwargs["Nmult"]=kwargs.pop("Nmult", self.calc_Nmult(v))
        super(Legendre, self).__init__(**kwargs)

    @cached_property
    def fixed_leg(self):
        if self.x is None:
            raise Exception("x not set!")
        return lgf_fixed(self.x, Nmult=self.Nmult, eval_neg=self.eval_neg, Nspacing=self.Nspacing, Nmax=self.Nmax, threshold=self.threshold)

    def fixed_reset(self):
        self.get_member("fixed_leg").reset(self)

def lgf_plot(pl="legendre", **kwargs):
    nu_max=30
    v_arr=linspace(-1.0, nu_max, 1000)
    print "start plot"
    pl=line(v_arr, lgf_arr(v_arr, 0.0), pl=pl, color="blue", linewidth=0.5, label=r"$P_{\nu}(0)$")[0]
    line(v_arr, lgf_arr(v_arr, 0.25, nu_max), pl=pl, color="red", linewidth=0.5, label=r"$P_{\nu}(0.25)$")
    line(v_arr, lgf_arr(v_arr, 0.5, nu_max), pl=pl, color="green", linewidth=0.5, label=r"$P_{\nu}(0.5)$")
    line(v_arr, lgf_arr(v_arr, 0.75, nu_max), pl=pl, color="purple", linewidth=0.5, label=r"$P_{\nu}(0.75)$")
    print "stop plot"
    for nu in range(nu_max):
        scatter(array([nu]), array([legendre(nu)(0.0)]), pl=pl, color="blue")
        scatter(array([nu]), array([legendre(nu)(0.25)]), pl=pl, color="red")
        scatter(array([nu]), array([legendre(nu)(0.5)]), pl=pl, color="green")
        scatter(array([nu]), array([legendre(nu)(0.75)]), pl=pl, color="purple")

    pl.xlabel=r"$\nu$"
    pl.ylabel=r"$P_{\nu}(x)$"
    pl.legend()
    pl.set_ylim(-0.75, 1.5)

    return pl

def lgf_plot2(pl="legendre", **kwargs):
    lg=Legendre()
    nu_max=30
    v_arr=linspace(-1.0, nu_max, 1000)
    print "start plot"
    pl=line(v_arr, lg.Pv(v_arr, 0.0), pl=pl, color="blue", linewidth=0.5, label=r"$P_{\nu}(0)$")[0]
    line(v_arr, lg.Pv(v_arr, 0.25), pl=pl, color="red", linewidth=0.5, label=r"$P_{\nu}(0.25)$")
    line(v_arr, lg.Pv(v_arr, 0.5), pl=pl, color="green", linewidth=0.5, label=r"$P_{\nu}(0.5)$")
    line(v_arr, lg.Pv(v_arr, 0.75), pl=pl, color="purple", linewidth=0.5, label=r"$P_{\nu}(0.75)$")
    print "stop plot"
    if 1:
        for nu in range(nu_max):
            scatter(array([nu]), array([legendre(nu)(0.0)]), pl=pl, color="blue")
            scatter(array([nu]), array([legendre(nu)(0.25)]), pl=pl, color="red")
            scatter(array([nu]), array([legendre(nu)(0.5)]), pl=pl, color="green")
            scatter(array([nu]), array([legendre(nu)(0.75)]), pl=pl, color="purple")

        pl.xlabel=r"$\nu$"
        pl.ylabel=r"$P_{\nu}(x)$"
        pl.legend()
        pl.set_ylim(-0.75, 1.5)

    return pl

if __name__=="__main__":
    #lgf_plot()#.show()
    lgf_plot2().show()