# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 01:07:15 2016

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.physics.fundamentals import sinc_sq, pi, eps0, lgf
from taref.core.agent import Agent
from atom.api import Float, Int, Enum, Value, Property, Typed
from taref.core.api import private_property, get_tag, SProperty, log_func, t_property, s_property, sqze, Array, tag_callable
from numpy import arange, linspace, sqrt, imag, real, sin, cos, interp, array, absolute, exp, ones, log10
#from matplotlib.pyplot import plot, show, xlabel, ylabel, title, xlim, ylim, legend
from scipy.signal import hilbert
from taref.plotter.api import line, Plotter


class IDT(Agent):
    """Theoretical description of IDT"""
    base_name="IDT"
    #main_params=["K2", "Dvv"] #"ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct",
    #            "material", "Dvv", "K2", "vf", "epsinf"]

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')

    def _default_material(self):
        return 'LiNbYZ'

    def _observe_material(self, change):
        if change["type"]=="update":
            self.Dvv=None
            self.vf=None
            self.epsinf=None

    @t_property(desc="coupling strength", unit="%", tex_str=r"$\Delta v/v$", expression=r"$(v_f-v_m))/v_f$")
    def Dvv(self, material):
        return {"STquartz" : 0.06e-2, 'GaAs' : 0.035e-2, 'LiNbYZ' : 2.4e-2,
                 'LiNb128' : 2.7e-2, 'LiNbYZX'  : 0.8e-2}[material]

    @t_property(desc="speed of SAW on free surface", unit="m/s", tex_str=r"$v_f$", format_str=r"{0:.4g} m/s")
    def vf(self, material):
        return {"STquartz" : 3159.0, 'GaAs' : 2900.0, 'LiNbYZ' : 3488.0,
                 'LiNb128' : 3979.0, 'LiNbYZX' : 3770.0}[material]

    @t_property(desc="Capacitance of single finger pair per unit length", tex_str=r"$\epsilon_\infty$")
    def epsinf(self, material):
        return {"STquartz" : 5.6*eps0, 'GaAs' : 1.2e-10, 'LiNbYZ' : 46.0*eps0,
                 'LiNb128' : 56.0*eps0, 'LiNbYZX' : 46.0*eps0}[material]

    ft=Enum("double", "single").tag(desc="finger type of IDT", label="Finger type", show_value=False)

    def _observe_ft(self, change):
        if change["type"]=="update":
            self.ft_mult=None
            self.Ga0_mult=None
            self.Ct_mult=None
            self.mu_mult=None

    def _default_ft(self):
        return "double"

    @t_property(desc="multiplier based on finger type")
    def ft_mult(self, ft):
        return {"double" : 2.0, "single" : 1.0}[ft]

    @t_property(dictify={"single" : 1.694**2, "double" : (1.247*sqrt(2))**2}) #{"single":2.87, "double":3.11}
    def Ga0_mult(self, ft):
        return get_tag(self, "Ga0_mult", "dictify")[ft]

    @t_property(dictify={ "single" : 1.0, "double" : sqrt(2)})
    def Ct_mult(self, ft):
        return get_tag(self, "Ct_mult", "dictify")[ft]


    @t_property()
    def mu_mult(self, ft):
        return {"single" : 1.694, "double" : 1.247}[ft]

    #coupling_mult_dict={"single" : 0.71775, "double" : 0.54995}

    couple_mult=SProperty()
    @couple_mult.getter
    def _get_couple_mult(self, Ga0_mult, Ct_mult):
        return Ga0_mult/(4*Ct_mult)

    f=Float(4.4e9).tag(desc="Operating frequency, e.g. what frequency is being stimulated/measured")

    Np=Float(9).tag(desc="\# of finger pairs", low=0.5, tex_str=r"$N_p$", label="\# of finger pairs")

    ef=Int(0).tag(desc="for edge effect compensation",
                    label="\# of extra fingers", low=0)

    W=Float(25.0e-6).tag(desc="height of finger.", unit="um")

    eta=Float(0.5).tag(desc="metalization ratio")

    f0=Float(5.0000001e9).tag(unit="GHz", desc="Center frequency of IDT", reference="", tex_str=r"$f_0$", label="Center frequency")

    C=SProperty().tag(unit="fF", desc="Total capacitance of IDT", reference="Morgan page 16/145")
    @C.getter
    def _get_C(self, epsinf, Ct_mult, W, Np):
        """Morgan page 16, 145"""
        return Ct_mult*W*epsinf*Np

    @C.setter
    def _get_epsinf(self, C, Ct_mult, W, Np):
        """reversing capacitance to extract eps infinity"""
        return C/(Ct_mult*W*Np)

    @log_func
    def _get_eta(self, a, g):
         """metalization ratio"""
         return a/(a+g)

    K2=SProperty().tag(desc="coupling strength", unit="%", tex_str=r"K$^2$", expression=r"K$^2=2\Delta v/v$")
    @K2.getter
    def _get_K2(self, Dvv):
        r"""Coupling strength. K$^2=2\Delta v/v$"""
        return Dvv*2.0

    @K2.setter
    def _get_Dvv(self, K2):
        """other coupling strength. free speed minus metal speed all over free speed"""
        return K2/2.0

    Ga0=SProperty().tag(desc="Conductance at center frequency")
    @Ga0.getter
    def _get_Ga0(self, Ga0_mult, f0, epsinf, W, Dvv, Np):
        """Ga0 from morgan"""
        return Ga0_mult*2*pi*f0*epsinf*W*Dvv*(Np**2)

    Ga0div2C=SProperty()
    @Ga0div2C.getter
    def _get_Ga0div2C(self, couple_mult, f0, K2, Np):
        """coupling at center frequency, in Hz (2 pi removed)"""
        return couple_mult*f0*K2*Np

    X=SProperty()
    @X.getter
    def _get_X(self, Np, f, f0):
        """standard frequency dependence"""
        return Np*pi*(f-f0)/f0

    couple_type=Enum("sinc^2", "giant atom", "df giant atom", "full expr", "full sum")

    coupling=SProperty().tag(desc="""Coupling adjusted by sinc sq""", unit="GHz", tex_str=r"$G_f$")
    @coupling.getter
    def _get_coupling(self, f, couple_mult, f0, K2, Np, eta, ft_mult, N_legendre, Ct_mult):
        if self.couple_type=="full sum":
            return self.get_fix("coupling", f)
        gX=self._get_X(Np=Np, f=f, f0=f0)
        if self.couple_type=="full expr":
            ele_f=self._get_alpha(f, f0, eta, ft_mult, N_legendre)
            return f0*K2*Np/(4*Ct_mult)*(ele_f*2*cos(pi*f/(4*f0))*(1.0/Np)*sin(gX)/sin(gX/Np))**2
        gamma0=self._get_Ga0div2C(couple_mult=couple_mult, f0=f0, K2=K2, Np=Np)
        if self.couple_type=="giant atom":
            return gamma0*(1.0/Np*sin(gX)/sin(gX/Np))**2
        elif self.couple_type=="df giant atom":
            return gamma0*(sqrt(2.0)*cos(pi*f/(4*f0))*1.0/Np*sin(gX)/sin(gX/Np))**2
        return gamma0*(sin(gX)/gX)**2.0

    N_legendre=Int(20).tag(desc="accuracy to evaluate Legendre expansion to")

    alpha=SProperty()
    @alpha.getter
    def _get_alpha(self, f, f0, eta, ft_mult, N_legendre):
        if isinstance(f, float):
            m=int(f/(2*ft_mult*f0))
            s=f/(2*ft_mult*f0)-m
        else:
            m=(f/(2*ft_mult*f0)).astype(int)
            s=f/(2*ft_mult*f0)-m
        pieta=pi*eta
        return 2*sin(pi*s)/lgf(-s, -cos(pieta), Nmax=N_legendre)*lgf(m, cos(pieta), Nmax=N_legendre)

    def fixed_reset(self):
        """resets fixed properties in proper order"""
        self.get_member("fixed_freq").reset(self)
        self.get_member("fixed_X").reset(self)
        self.get_member("fixed_alpha").reset(self)
        self.get_member("fixed_Asum").reset(self)
        self.get_member("fixed_coupling").reset(self)
        self.get_member("fixed_Lamb_shift").reset(self)
        self.get_member("fixed_Ga").reset(self)
        self.get_member("fixed_Ba").reset(self)
        self.get_member("fixed_S11").reset(self)

    @private_property
    def fixed_X(self):
        return self._get_X(f=self.fixed_freq)

    def get_fix(self, name, f):
        return interp(f, self.fixed_freq, getattr(self, "fixed_"+name))

    @private_property
    def fixed_coupling(self):
        gamma0=self.f0*self.K2*self.Np/(4*self.Ct_mult)
        if self.couple_type=="full sum":
            return gamma0*(self.fixed_alpha)**2*absolute(self.fixed_Asum)**2
        f, X, Np, f0=self.fixed_freq, self.fixed_X, self.Np, self.f0
        if self.couple_type=="full expr":
            ele_f=self.fixed_alpha
            return gamma0*(ele_f*2*cos(pi*f/(4*f0))*(1.0/Np)*sin(X)/sin(X/Np))**2
        if self.couple_type=="giant atom":
            return self.Ga0div2C*(1.0/Np*sin(X)/sin(X/Np))**2
        elif self.couple_type=="df giant atom":
            return self.Ga0div2C*(sqrt(2.0)*cos(pi*f/(4*f0))*1.0/Np*sin(X)/sin(X/Np))**2
        return self.Ga0div2C*(sin(X)/X)**2.0

    #def get_fix_coupling(self, f):
    #    return interp(f, self.fixed_freq, self.fixed_coupling)

    dloss1=Float(0.0)
    dloss2=Float(0.0)

    #propagation_loss=SProperty()
    #@propagation_loss.getter
    #def _get_propagation_loss(self, f, f0, dloss1, dloss2):
    #    return exp(-f/f0*dloss1-dloss2*(f/f0)**2)

    @t_property(sub=True)
    def polarity(self, Np, ft):
        if ft=="single":
            return arange(int(Np))+0.5
        return array(sqze(zip(arange(Np)+0.5, arange(Np)+0.75)))

    #@private_property
    #def fixed_polarity(self):
    #    return self.polarity

        #[0,1,0,1,0,1,0]
        #[0, 1/2, 1, 3/2, 2]
        #1/2, 3/2, 5/2
        #0, 1, 2
        #2*pi/

        #[0, 0, 1, 1, 0, 0, 1, 1, 0, 0]
        #[0, 1/4, 1/2, 3/4, 1, 5/4, 3/2, 7/4, 2]
        #[0, 1/4, 1/2, 0, 0, 5/4, 3/2, 0, 0]
        #[0, 1/4, 1/2, 0, 0, 5/4, 3/2, 0, 0]

    #g_arr=Array()
    #g_arr=SProperty().tag(sub=True)
    #@g_arr.getter
    @t_property(sub=True)
    def g_arr(self, polarity):
        return ones(len(polarity))

    Asum=SProperty().tag(sub=True)
    @Asum.getter
    def _get_Asum(self, f, f0, Np, dloss1, dloss2, g_arr, polarity):
        return 1.0/Np*array([sum([g_arr[i]*exp(2.0j*pi*frq/f0*n-frq/f0*dloss1*n-n*dloss2*(frq/f0)**2)
               for i, n in enumerate(polarity)]) for frq in f])

    @private_property
    def fixed_Asum(self):
        return self._get_Asum(f=self.fixed_freq)

    #def get_fix_Asum(self, f):
    #    return interp(f, self.fixed_freq, self.fixed_Asum)

    @private_property
    def fixed_alpha(self):
        return self._get_alpha(f=self.fixed_freq)

    #def get_fix_alpha(self, f):
    #    return interp(f, self.fixed_freq, self.fixed_alpha)

    @private_property
    def fixed_Lamb_shift(self):
        if self.Lamb_shift_type=="formula":
            X, Np=self.fixed_X, self.Np
            if self.couple_type=="sinc^2":
                return -self.Ga0div2C*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
            if self.couple_type=="giant atom":
                return self.Ga0div2C*(1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
        return imag(hilbert(self.fixed_coupling))

    #def get_fix_Lamb_shift(self, f):
    #    return interp(f, self.fixed_freq, self.fixed_Lamb_shift)

    max_coupling=SProperty().tag(desc="""Coupling at IDT center frequency""", unit="GHz",
                     label="Coupling at center frequency", tex_str=r"$\gamma_{f0}$")
    @max_coupling.getter
    def _get_max_coupling(self, couple_mult, f0, K2, Np, eta, ft_mult, N_legendre, Ct_mult):
        return self._get_coupling(f=f0+0.0001, couple_mult=couple_mult, f0=f0,
                K2=K2, Np=Np, eta=eta, ft_mult=ft_mult, N_legendre=N_legendre, Ct_mult=Ct_mult)
        #return self._get_Ga0div2C(couple_mult=couple_mult, f0=f0, K2=K2, Np=Np)

    Lamb_shift_type=Enum("hilbert", "formula")

    Lamb_shift=SProperty().tag(desc="""Lamb shift""", unit="GHz", tex_str=r"$G_f$")
    @Lamb_shift.getter
    def _get_Lamb_shift(self, f, couple_mult, f0, K2, Np, eta, ft_mult, N_legendre, Ct_mult):
        """returns Lamb shift"""
        if self.Lamb_shift_type=="formula":
            gamma0=self._get_Ga0div2C(couple_mult=couple_mult, f0=f0, K2=K2, Np=Np)
            gX=self._get_X(Np=Np, f=f, f0=f0)
            if self.couple_type=="sinc^2":
                return -gamma0*(sin(2.0*gX)-2.0*gX)/(2.0*gX**2.0)
            if self.couple_type=="giant atom":
                return gamma0*(1.0/Np)**2*2*(Np*sin(2*gX/Np)-sin(2*gX))/(2*(1-cos(2*gX/Np)))
        if self.couple_type=="full sum":
            return self.get_fix("Lamb_shift", f)
        yp=imag(hilbert(self._get_coupling(f=self.fixed_freq, couple_mult=couple_mult, f0=f0,
                K2=K2, Np=Np, eta=eta, ft_mult=ft_mult, N_legendre=N_legendre, Ct_mult=Ct_mult)))
        return interp(f, self.fixed_freq, yp)

    @private_property
    def fixed_freq(self):
        return linspace(self.fixed_freq_min, self.fixed_freq_max, self.N_fixed)

    N_fixed=Int(20000)
    fixed_freq_max=Float()
    fixed_freq_min=Float(0.0)

    def _default_fixed_freq_max(self):
        return 8.0*self.f0

    ZL=Float(50.0)
    ZL_imag=Float(0.0)
    GL=Float(1/50.0)
    dL=Float(0.0)

    S11=SProperty()
    @S11.getter
    def _get_S11(self, f, couple_mult, f0, K2, Np, C, ZL):
        Ga=self._get_Ga(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C)
        Ba=self._get_Ba(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C)
        w=2*pi*f
        return Ga/(Ga+1j*Ba+1j*w*C+1.0/ZL)

    @private_property
    def fixed_S11(self):
        f, Ga, Ba=self.fixed_freq, self.fixed_Ga, self.fixed_Ba
        w=2*pi*f
        C, ZL=self.C, self.ZL
        return Ga/(Ga+1j*Ba+1j*w*C+1.0/ZL)

    S13=SProperty()
    @S13.getter
    def _get_S13(self, f, couple_mult, f0, K2, Np, C, ZL, ZL_imag, GL, dL, eta):
        Ga=self._get_Ga(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C, eta=eta)
        Ba=self._get_Ba(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C, eta=eta)
        w=2*pi*f
        return 1j*sqrt(2*Ga*GL)/(Ga+1j*Ba+1j*w*C-1j/w*dL+1.0/ZL)

    S33=SProperty()
    @S33.getter
    def _get_S33(self, f, couple_mult, f0, K2, Np, C, ZL, ZL_imag, GL, dL):
        Ga=self._get_Ga(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C)
        Ba=self._get_Ba(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C)
        w=2*pi*f
        return (Ga+1j*Ba+1j*w*C-1j/w*dL-1.0/ZL)/(Ga+1j*Ba+1j*w*C-1j/w*dL+1.0/ZL)

    Ga=SProperty().tag(desc="Ga adjusted for frequency f")
    @Ga.getter
    def _get_Ga(self, f, couple_mult, f0, K2, Np, C, eta):
        return self._get_coupling(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, eta=eta)*2*C*2*pi
    @private_property
    def fixed_Ga(self):
        return self._get_Ga(f=self.fixed_freq)

    Ba=SProperty()
    @Ba.getter
    def _get_Ba(self, f, couple_mult, f0, K2, Np, C, eta):
        return -self._get_Lamb_shift(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, eta=eta)*2*C*2*pi
    @private_property
    def fixed_Ba(self):
        return self._get_Ba(f=self.fixed_freq)

    lbda=SProperty()
    @lbda.getter
    def _get_lbda(self, f, vf):
        """wavelength relationship to speed and frequency"""
        return vf/f

    @lbda.setter
    def _get_f(self, lbda, vf):
        """frequency relationship to speed and wavelength"""
        return vf/lbda

    lbda0=SProperty().tag(unit="um", desc="Center wavelength", reference="")
    @lbda0.getter
    def _get_lbda0(self, f0, vf):
        return self._get_lbda(f=f0, vf=vf)

    @lbda0.setter
    def _get_f0(self, lbda0, vf):
        return self._get_f(lbda=lbda0, vf=vf)

    g=SProperty().tag(desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz", unit="um")
    @g.getter
    def _get_g(self, a, eta):
        """gap given metalization and finger width
        eta=a/(a+g)
        => a=(a+g)*eta
        => (1-eta)*a=g*eta
        => g=a*(1/eta-1)"""
        return a*(1.0/eta-1.0)

    @g.setter
    def _get_a_get_(self, g,  eta):
        """finger width given gap and metalization ratio
        eta=a/(a+g)
        => a=(a+g)*eta
        => (1-eta)*a=g*eta
        => a=g*eta/(1-eta)"""
        return g*eta/(1.0-eta)

    a=SProperty().tag(desc="width of fingers", unit="um")
    @a.getter
    def _get_a(self, eta, lbda0, ft_mult):
        """finger width from lbda0"""
        return eta*lbda0/(2.0*ft_mult)

    @a.setter
    def _get_lbda0_get_(self, a, eta, ft_mult):
        return a/eta*2.0*ft_mult

    @private_property
    def view_window2(self):
        from enaml import imports
        with imports():
            from taref.saw.idt_e import IDT_View
        return IDT_View(idt=self)

#from functools import wraps
#
#class idt_plot(tag_callable):
#    def __call__(self, func):
#        @wraps(func)
#        def new_plot(self, *args, **kwargs):
#            self.idt=kwargs.pop("idt", self.idt)
#            if self.idt is None:
#                self.idt=IDT()
#            return func(self, *args, **kwargs)
#        return super(idt_plot, self).__call__(new_plot)

def idt_process(kwargs):
    idt=kwargs.pop("idt", None)
    if idt is None:
        return IDT()
    return idt

def element_factor_plot(pl="element_factor", **kwargs):
    idt=idt_process(kwargs)
    idt.ft="single"
    pl, pf=line(idt.fixed_freq/idt.f0, idt.fixed_alpha, plotter=pl, plot_name="single", color="blue", label="single finger", **kwargs)
    idt.ft="double"
    idt.fixed_reset()
    pl= line(idt.fixed_freq/idt.f0, idt.fixed_alpha, plotter=pl, plot_name="double", color="red", label="double finger", linestyle="dashed")[0]
    pl.xlabel="frequency/center frequency"
    pl.ylabel="element factor"
    pl.legend()
    return pl

def metallization_plot(pl="metalization", **kwargs):
    idt=idt_process(kwargs)
    idt.eta=0.5
    idt.ft="single"
    idt.N_legendre=1000

    idt.fixed_reset()
    pl=line(idt.fixed_freq/idt.f0, idt.fixed_alpha, plotter=pl, plot_name="0.5", color="blue", label="0.5", **kwargs)[0]
    idt.eta=0.75
    idt.fixed_reset()
    line(idt.fixed_freq/idt.f0, idt.fixed_alpha, plotter=pl, plot_name="0.6", color="red", label="0.6", **kwargs)
    idt.eta=0.25
    idt.fixed_reset()
    line(idt.fixed_freq/idt.f0, idt.fixed_alpha, plotter=pl, plot_name="0.4", color="green", label="0.4", **kwargs)
    idt.eta=0.5
    return pl
#metallization_plot().show()

def metallization_couple(pl="metalization", **kwargs):
    idt=idt_process(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.eta=0.5
    #idt.ft="single"
    idt.couple_type="full sum"
    idt.fixed_reset()
    pl=line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)[0]
    idt.eta=0.6
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.6", color="red", linewidth=0.3, label="0.6", **kwargs)
    idt.eta=0.4
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.4", color="green", linewidth=0.3, label="0.4", **kwargs)
    idt.eta=0.5
    return pl
metallization_couple()#.show()
def metallization_Lamb(pl="metalization", **kwargs):
    idt=idt_process(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.eta=0.5
    #idt.ft="single"
    idt.couple_type="full sum"
    idt.fixed_reset()
    pl=line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)[0]
    idt.eta=0.6
    idt.fixed_reset()
    #line(idt.fixed_freq/idt.f0, idt.fixed_Lamb_shift/idt.max_coupling, plotter=pl, linewidth=0.3, color="purple")
    line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.6", color="red", linewidth=0.3, label="0.6", **kwargs)
    idt.eta=0.4
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.4", color="green", linewidth=0.3, label="0.4", **kwargs)
    idt.eta=0.5
    return pl
metallization_Lamb().show()

def center_coupling_vs_eta(pl="f0_vs_eta", **kwargs):
    idt=idt_process(kwargs)
    eta=linspace(0.0, 1.0, 100)
    idt.ft="single"
    #idt.N_legendre=1000
    alpha=idt._get_alpha(f=idt.f0, eta=eta, N_legendre=1000)
    pl=line(eta, alpha, plotter=pl)[0]
    alpha=idt._get_alpha(f=3*idt.f0, eta=eta, N_legendre=1000)
    line(eta, alpha, plotter=pl, color="red")
    alpha=idt._get_alpha(f=5*idt.f0, eta=eta, N_legendre=1000)
    line(eta, alpha, plotter=pl, color="green")
    return pl #line(eta, idt._get_alpha(f=3*idt.f0, eta=eta))[0]

center_coupling_vs_eta().show()

def couple_comparison(pl="couple_compare", **kwargs):
    idt=idt_process(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.couple_type="sinc^2"
    pl, pf=line(frq/idt.f0, 10*log10(idt._get_coupling(frq)/idt.max_coupling), plotter=pl, linewidth=0.3, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, 10*log10(idt._get_coupling(frq)/idt.max_coupling), plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="df giant atom"
    line(frq/idt.f0, 10*log10(idt._get_coupling(frq)/idt.max_coupling), plotter=pl, color="green", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, 10*log10(idt._get_coupling(frq)/idt.max_coupling), plotter=pl, color="black", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full sum"
    line(frq/idt.f0, 10*log10(idt._get_coupling(frq)/idt.max_coupling), plotter=pl, color="purple", linewidth=0.3, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling/max coupling (dB)"
    pl.set_ylim(-30, 1.0)
    pl.legend()
    return pl

def fix_couple_comparison(pl="fix couple", **kwargs):
    idt=idt_process(kwargs)
    idt.couple_type="sinc^2"
    idt.fixed_reset()
    frq=linspace(0e9, 10e9, 10000)
    pl, pf=line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, linewidth=0.3, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="df giant atom"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="green", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full expr"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="black", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full sum"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="purple", linewidth=0.3, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling/max coupling (dB)"
    pl.set_ylim(-30, 1.0)
    pl.legend()
    return pl

def Lamb_shift_comparison(pl="ls_comp", **kwargs):
    idt=idt_process(kwargs)
    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc^2"
    #idt=IDT(Lamb_shift_type="formula", couple_type="sinc^2")
    frq=linspace(0e9, 10e9, 10000)
    pl, pf=line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, linewidth=0.3, label="sinc^2", **kwargs)
    #a=IDT(Lamb_shift_type="formula", couple_type="giant atom")
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    #a=IDT(Lamb_shift_type="hilbert", couple_type="sinc^2")
    idt.Lamb_shift_type="hilbert"
    idt.couple_type="sinc^2"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="green", linewidth=0.3, label="h(sinc^2)")
    #a=IDT(Lamb_shift_type="hilbert", couple_type="giant atom")
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="black", linewidth=0.3, label="h(giant atom)")
    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift/max coupling"
    pl.set_ylim(-1, 0.8)
    pl.legend()

    #line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl

def Lamb_shift_check(pl="ls_check", **kwargs):
    idt=idt_process(kwargs)
    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc^2"
    frq=linspace(0e9, 10e9, 10000)
    pl, pf=line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, linewidth=0.3, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="df giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="green", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="black", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full sum"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="purple", linewidth=0.3, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift/max coupling (dB)"
    pl.set_ylim(-1.0, 1.0)
    pl.legend()

    #line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl

def formula_comparison(pl=None, **kwargs):
    a=IDT()
    frq=linspace(3e9, 7e9, 10000)
    print a._get_coupling(frq)
    print a.max_coupling
    pl, pf=line(frq, a._get_coupling(frq)/a.max_coupling, plotter=pl, linewidth=1.0, **kwargs)
    line(frq, a._get_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="red", linewidth=1.0)
    #line(frq, coup, color="purple", plotter=pl, linewidth=0.3)
    line(frq, a._get_full_coupling(frq)/a.max_coupling, plotter=pl, color="green", linewidth=0.3)
    line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl

idt=IDT()
element_factor_plot(idt=idt)#.show()

Lamb_shift_comparison(idt=idt)

couple_comparison(idt=idt)#.show()

fix_couple_comparison(idt=idt)#.show()

Lamb_shift_check(idt=idt).show()

#formula_comparison()#.show()

#element_factor_plot(idt=idt).show()
if __name__=="__main__":
    #a=IDT(dloss1=0.0, dloss2=0.0, eta=0.6, ft="double")
    a=IDT(material='LiNbYZ',
          ft="double",
          a=80.0e-9, #f0=5.35e9,
          Np=9,
          #Rn=3780.0, #(3570.0+4000.0)/2.0, Ejmax=h*44.0e9,
          W=25.0e-6,
          eta=0.5,)
          #flux_factor=0.515, #0.2945, #0.52,
          #voltage=1.21,
          #offset=-0.07)
    a.f=a.f0
    print a.fixed_polarity
    print a.alpha
    print a.fixed_element_factor
    print a._get_element_factor(a.f0)
    from scipy.signal import hilbert
    from numpy import imag, real, sin, cos, exp, array, absolute


    frq=linspace(1e9, 10e9, 10000)

    X=a._get_X(f=frq)
    Np=a.Np
    f0=a.f0

    if 0:
        def Asum(N, k1=0.0, k2=0.0):
            return array([sum([exp(2.0j*pi*f/f0*n-f/f0*k1-k2*(f/f0)**2) for n in range(N)]) for f in frq])

        def Asum2(M):
            return array([sum([exp(2j*pi*M*f/f0)*exp(2j*pi*f/f0*m) for m in range(-M, M+1)]) for f in frq])

        def Asum3(M, k=1.0):
            return array([sum([exp(2j*pi*f/f0*m) for m in range(-M, M+1)]) for f in frq])

        def Asum4(M):
            return array([sum([2*cos(2*pi*f/f0*m) for m in range(0, M+1)]) for f in frq])-1

        def Asum5(M, g=0.9, g2=1.0):
            return array([g*2*cos(2*pi*f/f0*M) for f in frq])+array([g2*2*cos(2*pi*f/f0*(M-1)) for f in frq])+Asum4(M-2)

        def Asum6(g=1.0):
            return array([(g*exp(-2j*pi*f/f0*4)+exp(-2j*pi*f/f0*3)+exp(-2j*pi*f/f0*2)+exp(-2j*pi*f/f0*1)+1.0
            +exp(2j*pi*f/f0*1)+exp(2j*pi*f/f0*2)+exp(2j*pi*f/f0*3)+g*exp(2j*pi*f/f0*4)) for f in frq])

        def Asum7(g=1.0):
            return array([(g+exp(2j*pi*f/f0*1)+exp(2j*pi*f/f0*2)+exp(2j*pi*f/f0*3)+exp(2j*pi*f/f0*4)
            +exp(2j*pi*f/f0*5)+exp(2j*pi*f/f0*6)+exp(2j*pi*f/f0*7)+g*exp(2j*pi*f/f0*8)) for f in frq])

        A=Asum(9, k1=0.05, k2=0.05)
        A2=Asum2(4)
        A3=Asum3(4)
        A4=Asum4(4)
        A5=Asum5(4, 1.2, 1.0)
        A6=Asum6(0.5)
        A7=Asum7(0.5)

        pl=Plotter()
        #line(frq/1e9, real(A), plotter=pl)
        #line(frq/1e9, imag(A), plotter=pl, color="red")

        #line(frq/1e9, real(A2), plotter=pl, color="green", linewidth=0.5)
        #line(frq/1e9, imag(A2), plotter=pl, color="black", linewidth=0.5)

        line(frq/1e9, sin(pi*9*frq/f0)/sin(pi*frq/f0), plotter=pl)

        line(frq/1e9, real(A3), plotter=pl, color="green", linewidth=0.5)
        line(frq/1e9, imag(A3), plotter=pl, color="black", linewidth=0.5)

        line(frq/1e9, A4, plotter=pl, color="red", linewidth=0.5)
        #line(frq/1e9, A5, plotter=pl, color="purple", linewidth=0.5)
        line(frq/1e9, real(A6), plotter=pl, color="darkgray", linewidth=0.5)
        line(frq/1e9, imag(A6), plotter=pl, color="darkgray", linewidth=0.5)

        #pl.show()
        pl=Plotter()

        line(frq/1e9, 1/81.0*absolute(A)**2, plotter=pl, color="black")
        #line(frq/1e9, 1/81.0*absolute(sin(pi*9*frq/f0)/sin(pi*frq/f0))**2, plotter=pl, color="green", linewidth=0.4)
        #line(frq/1e9, 1/81.0*absolute(A5)**2, plotter=pl, color="blue", linewidth=0.5)
        line(frq/1e9, 1/81.0*absolute(A6)**2, plotter=pl, color="red", linewidth=0.5)
        line(frq/1e9, 1/81.0*absolute(A7)**2, plotter=pl, color="purple", linewidth=0.5)

        #line(frq/1e9, 1/9.0*absolute(A6), plotter=pl, color="red", linewidth=0.5)

        #line(frq/1e9, 1/9.0*absolute(A7), plotter=pl, color="purple", linewidth=0.5)

        pl.show()

    frq=linspace(0, 40e9, 10000)

    X=a._get_X(f=frq)
    Np=a.Np
    f0=a.f0

    #coup=(sqrt(2)*cos(pi*frq/(4*f0))*(1.0/Np)*sin(X)/sin(X/Np))**2
    coup=(sin(X)/X)**2

    #coup=(1.0/Np*sin(X)/sin(X/Np))**2


    element_factor_plot(a)
    pl=Plotter()
    line(frq, a._get_coupling(frq)/a.max_coupling, plotter=pl, linewidth=1.0)
    line(frq, a._get_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="red", linewidth=1.0)
    line(frq, coup, color="purple", plotter=pl, linewidth=0.3)
    line(frq, a._get_full_coupling(frq)/a.max_coupling/1.247**2/2, plotter=pl, color="green", linewidth=0.3)
    line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling/1.247**2/2, plotter=pl, color="black", linewidth=0.3)

    #hb=hilbert(coup) #a._get_coupling(frq))
    #line(frq, real(hb), plotter=pl, color="green", linewidth=0.3)
    #line(frq, imag(hb), plotter=pl, color="black", linewidth=0.3)
    #Baa= (1+cos(X/(4*Np)))*(1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
    Baa=-(sin(2.0*X)-2.0*X)/(2.0*X**2)
    #Baa= (1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
    line(frq, Baa, plotter=pl, color="cyan", linewidth=0.3)

    pl.show()

    b=IDT(ft="single")
    a.ft_mult=5
    print a.mu_mult, a.ft_mult, b.mu_mult, b.ft_mult
    print a.couple_mult, b.couple_mult
    a.ft="single"
    a.ft_mult=None
    print a.mu_mult, a.ft_mult, b.mu_mult, b.ft_mult
    print a.couple_mult, b.couple_mult

    print a.epsinf, a.C
    a.epsinf=4e-10
    print a.C
    a.C=7.1e-14
    print a.epsinf, a.C

    print a._get_C(W=35)



    #log_debug(a.K2, b.K2)
    #a.Dvv=5
    #a.K2=4
    #for name in a.all_params:
    #    print name, getattr(a, name)
    #a.a=90e-9
    #for name in a.all_params:
    #    print name, getattr(a, name)

    #print a._get_Dvv(4)
    #print a.K2_f(2)
    #log_debug(a.get_member("K2").fget.fset_list)
    #log_debug(a.get_member("K2").fset(a, 3))
    #log_debug(a.get_member("K2").fset)

    #print a.K2, b.K2
#    for param in a.all_params:
#        print get_tag(a, param, "unit")
        #print a.call_func("eta", a=0.2e-6, g=0.8e-6)#, vf=array([500.0, 600.0]), lbda0=array([0.5e-6, 0.6e-6]))
        #a.plot_data("f0", lbda0=linspace(0.1e-6, 1.0e-6, 10000))
        #print a.get_tag("lbda0", "unit_factor")
    a.show()
    if 0:
        print a.K2, a.Dvv
        #print dir(a.get_member("K2").fget.fset)
        a.K2=5
        a.Dvv=5
        print a.K2
        shower(a)
        #print a.K2, a.Dvv
        #print a.K2, a.Dvv


    if 0:
        print a.property_dict
        print a.get_member("p").fget()#.func_code.co_varnames#(a, 1, 1)
        #print a.p()
        #a.eta=0.6
        print a.p
        a.a=5e-6
        print a.p
        show(a)
        #a.get_member("lbda0").setter(a.set_func("lbda0"))
        #a.lbda0=1.0e-6

    if 0:
        print a.f0
        print a.a, a.f0
        a.a=0.5e-6
        print a.eta, a.a, a.g, a.f0
        a.eta=0.1
        print a.eta, a.a, a.g
        a.g=0.5e-6
        print a.eta, a.a, a.g
        print a.lbda0, a.f0

        print a.Ga_f