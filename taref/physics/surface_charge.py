# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:43:08 2016

@author: thomasaref
"""

from taref.physics.fundamentals import pi, eps0, sin, cos, linspace, real, fft, array, absolute, float64, imag, sqrt, int64
from taref.physics.legendre import lgf, lgf_arr, Legendre
from atom.api import Float, Typed, Enum, Int, Bool
from taref.core.api import t_property, Agent, private_property, SProperty, log_func, get_tag, log_callable
from taref.plotter.api import line, Plotter
from scipy.signal import hann
from scipy.fftpack import  rfft, irfft, ifft
from scipy.integrate import trapz, simps
from collections import OrderedDict

from enaml import imports
with imports():
    from taref.physics.surface_charge_e import SurfaceChargeView


def alpha(f, f0, eta=0.5, ft_mult=1, Nmax=2000):
    """Fourier transform of charge for 1 positive finger IDT.
    ft_mult=1 for single finger and 2 for double finger. eta is metallization ratio"""
    pieta=pi*eta
    if isinstance(f, float):
        m=int(f/(2*ft_mult*f0))
        s=f/(2*ft_mult*f0)-m
        return 2*sin(pi*s)/lgf(-s, -cos(pieta), Nmax=Nmax)*lgf(m, cos(pieta), Nmax=Nmax)
    m=(f/(2*ft_mult*f0)).astype(int)
    s=f/(2*ft_mult*f0)-m
    return 2*sin(pi*s)/lgf_arr(-s, -cos(pieta), 0)*lgf_arr(m, cos(pieta))

class Rho(Agent):
    base_name="rho"

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz').tag(label="material", expression="Substrate")

    def _default_material(self):
        return 'LiNbYZ'

    def _observe_material(self, change):
        if change["type"]=="update":
            self.Dvv=None
            self.vf=None
            self.epsinf=None

    @t_property(desc="coupling strength (relative speed difference)", unit="%", tex_str=r"$\Delta v/v$", expression=r"$\Delta v/v=(v_f-v_m)/v_f$", label="piezoelectric coupling")
    def Dvv(self, material):
        return {"STquartz" : 0.06e-2, 'GaAs' : 0.035e-2, 'LiNbYZ' : 2.4e-2,
                 'LiNb128' : 2.7e-2, 'LiNbYZX'  : 0.8e-2}[material]

    K2=SProperty().tag(desc="coupling strength", unit="%", tex_str=r"K$^2$", expression=r"K$^2=2\Delta v/v$", label="piezoelectric coupling")
    @K2.getter
    def _get_K2(self, Dvv):
        r"""Coupling strength. K$^2=2\Delta v/v$"""
        return Dvv*2.0

    @K2.setter
    def _get_Dvv(self, K2):
        """other coupling strength. free speed minus metal speed all over free speed"""
        return K2/2.0

    @t_property(desc="speed of SAW on free surface", unit="m/s", expression=r"$v_f$", format_str=r"{0:.4g} m/s", label="free SAW speed")
    def vf(self, material):
        return {"STquartz" : 3159.0, 'GaAs' : 2900.0, 'LiNbYZ' : 3488.0,
                 'LiNb128' : 3979.0, 'LiNbYZX' : 3770.0}[material]

    @t_property(desc="Capacitance of one finger pair per unit length", expression=r"$\epsilon_\infty=C_S$", label="SAW permittivity")
    def epsinf(self, material):
        return {"STquartz" : 5.6*eps0, 'GaAs' : 1.2e-10, 'LiNbYZ' : 46.0*eps0,
                 'LiNb128' : 56.0*eps0, 'LiNbYZX' : 46.0*eps0}[material]

    ft=Enum("double", "single").tag(desc="finger type of IDT", label="Finger type")

    def _observe_ft(self, change):
        if change["type"]=="update":
            self.ft_mult=None
            self.Ct_mult=None

    def _default_ft(self):
        return "double"

    @t_property(desc=r"single : 1, double : 2", label="finger type multiplier", expression=r"$c_{ft}$")
    def ft_mult(self, ft):
        return {"double" : 2.0, "single" : 1.0}[ft]

    @t_property(dictify={ "single" : 1.0, "double" : sqrt(2)}, label="Capacitance multiplier", expression=r"$c_c$", desc=r"single : $1$, double : $\sqrt{2}$")
    def Ct_mult(self, ft):
        return get_tag(self, "Ct_mult", "dictify")[ft]

    f=Float().tag(desc="what frequency is being stimulated/measured", unit="GHz", label="Operating frequency", expression=r"$f$")

    def _default_f(self):
        """default f is 1Hz off from f0"""
        return self.f0#-1.0

    f0=Float(5.0000001e9).tag(unit="GHz", desc="Center frequency of IDT", reference="", expression=r"$f_0$", label="Center frequency")

    lbda=SProperty().tag(unit="um", desc="wavelength", reference="", label="wavelength", expression=r"$\lambda=v_f/f$")
    @lbda.getter
    def _get_lbda(self, f, vf):
        """wavelength relationship to speed and frequency"""
        return vf/f

    @lbda.setter
    def _get_f(self, lbda, vf):
        """frequency relationship to speed and wavelength"""
        return vf/lbda

    lbda0=SProperty().tag(unit="um", desc="Center wavelength", reference="", label="center wavelength", expression=r"$\lambda_0=v_f/f_0$")
    @lbda0.getter
    def _get_lbda0(self, f0, vf):
        return vf/f0

    @lbda0.setter
    def _get_f0(self, lbda0, vf):
        return vf/lbda0

    k=SProperty().tag(label="Wavenumber", expression=r"$k=2\pi/\lambda$")
    @k.getter
    def _get_k(self, lbda):
        return 2*pi/lbda

    @k.setter
    def _get_lbda_get_k(self, k):
        return 2*pi/k

    k0=SProperty().tag(label="Center wavenumber", expression=r"$k_0=2\pi/\lambda_0$")
    @k0.getter
    def _get_k0(self, lbda0):
        return 2*pi/lbda0

    @k0.setter
    def _get_lbda0_get_k0(self, k0):
        return 2*pi/k0

    eta=Float(0.5).tag(desc="metalization ratio", label="metallization ratio", expression=r"$\eta$")

    @log_func
    def _get_eta(self, a, g):
         """metalization ratio"""
         return a/(a+g)

    g=SProperty().tag(desc="gap between fingers", unit="um", label="finger gap", expression=r"$g$")
    @g.getter
    def _get_g(self, a, eta):
        """gap given metalization and finger width
        eta=a/(a+g)
        => a=(a+g)*eta
        => (1-eta)*a=g*eta
        => g=a*(1/eta-1)"""
        return a*(1.0/eta-1.0)

    @g.setter
    def _get_a_get_g(self, g,  eta):
        """finger width given gap and metalization ratio
        eta=a/(a+g)
        => a=(a+g)*eta
        => (1-eta)*a=g*eta
        => a=g*eta/(1-eta)"""
        return g*eta/(1.0-eta)

    a=SProperty().tag(desc="width of fingers", unit="um", label="finger width", expression=r"$a$")
    @a.getter
    def _get_a(self, eta, lbda0, ft_mult):
        """finger width from lbda0"""
        return eta*lbda0/(2.0*ft_mult)

    @a.setter
    def _get_lbda0_get_a(self, a, eta, ft_mult):
        return a/eta*2.0*ft_mult

    p=SProperty().tag(desc="periodicity", unit="um", label="finger periodicity", expression=r"$p=a+g$")
    @p.getter
    def _get_p(self, a, g):
        """periodicity from a and g"""
        return a+g

    @p.setter
    def _get_lbda0_get_p(self, p, ft_mult):
        return 2*ft_mult*p

    @private_property
    def fixed_freq(self):
        return linspace(self.fixed_freq_min, self.fixed_freq_max, self.N_fixed).astype(float64)

    N_fixed=Int(10000)
    fixed_freq_max=Float()
    fixed_freq_min=Float(0.01)

    def _default_fixed_freq_max(self):
        return 20.0*self.f0

    def _default_fixed_freq_min(self):
        return 0.01*self.f0

    lgf1=Typed(Legendre)#.tag(sub=True)
    lgf2=Typed(Legendre)#.tag(sub=True)

    def _default_lgf1(self):
        return Legendre(x=-cos(pi*self.eta), Nmult=0)

    def _default_lgf2(self):
        return Legendre(x=cos(pi*self.eta), v=self._get_m(f=self.fixed_freq_max))

    def _observe_eta(self, change):
        if change["type"]=="update":
            if self.fixed_update:
                self.fixed_reset()

    fixed_update=Bool(False).tag(desc="if True, changing eta will trigger an update of fixed values (slow computation)")

    #@log_callable()
    def fixed_reset(self):
        self.lgf1.Pv(0.0, -cos(pi*self.eta), 0)
        self.lgf2.Pv(self.fixed_freq_max/(2*self.ft_mult*self.f0), cos(pi*self.eta))
        self.get_member("fixed_freq").reset(self)
        self.get_member("fixed_alpha").reset(self)
        self.get_member("surface_x").reset(self)
        self.get_member("surface_charge").reset(self)
        self.get_member("surface_voltage").reset(self)

    @private_property
    def fixed_alpha(self):
        return self._get_alpha(f=self.fixed_freq)

    @private_property
    def fixed_m(self):
        return self._get_m(f=self.fixed_freq)

    @private_property
    def fixed_s(self):
        return self._get_s(f=self.fixed_freq)

    m=SProperty().tag(desc="integer number of wavelengths")
    @m.getter
    def _get_m(self, f, f0, ft_mult):
        fs=self._get_fs(f=f, f0=f0, ft_mult=ft_mult)
        if isinstance(f, float):
            return int(fs)
        return fs.astype(int64)

    s=SProperty()
    @s.getter
    def _get_s(self, f, f0, ft_mult):
        fs=self._get_fs(f=f, f0=f0, ft_mult=ft_mult)
        m=self._get_m(f=f, f0=f0, ft_mult=ft_mult)
        return fs-m

    fs=SProperty()
    @fs.getter
    def _get_fs(self, f, f0, ft_mult):
        return f/(2.0*ft_mult*f0)

    alpha=SProperty().tag(desc="single : 1.694, double : 1.247", label="mu multiplier", expression=r"$\alpha$")
    @alpha.getter
    def _get_alpha(self, f, f0, ft_mult, eta, epsinf):
        m=self._get_m(f=f, f0=f0, ft_mult=ft_mult)
        s=self._get_s(f=f, f0=f0, ft_mult=ft_mult)
        return 2*sin(pi*s)/self.lgf1.Pv(-s)*self.lgf2.Pv(m)

    alpha0=SProperty()
    @alpha0.getter
    def _get_alpha0(self, f0, ft_mult, eta, epsinf):
        return self._get_alpha(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf)

    @private_property
    def surface_x(self):
        fs=self._get_fs(f=self.fixed_freq)
        df=1.0/(fs[1]-fs[0])/2.0#*self.lbda0/2
        return linspace(-df/2.0, df/2.0, self.N_fixed)

    @private_property
    def surface_charge(self):
        return fft.fftshift(real(ifft(self.fixed_alpha*self.epsinf)))

    @private_property
    def surface_voltage(self):
        lbda=self._get_lbda(f=self.fixed_freq)
        kCs=self._get_k(lbda)#*self.epsinf
        return fft.fftshift(real(fft.ifft(self.fixed_alpha/kCs))).astype(float64)

    @private_property
    def view_window(self):
        return SurfaceChargeView(agent=self)

    @private_property
    def plot_func_dict(self):
        return OrderedDict([("legendre test", dict(code=self.lgf1.lgf_test_plot)),
                            ("plot_alpha", dict(code=self.plot_alpha)),
                            ("plot surface charge", dict(code=self.plot_surface_charge)),
                            ("plot surface voltage", dict(code=self.plot_surface_voltage)),
                            ])

    def plot_alpha(self, pl=None, **kwargs):
        if pl is None:
            pl="alpha_"+self.name
        f, alpha=self.fixed_freq, self.fixed_alpha
        pl, pf=line(f/self.f0, alpha, plotter=pl, plot_name=self.name, color="blue", label=self.name, **kwargs)
        pl.xlabel="frequency/center frequency"
        pl.ylabel="element factor"
        pl.set_ylim(-1.0, 2.0)
        return pl

    def plot_surface_charge(self, pl=None, **kwargs):
        if pl is None:
            pl="surface_charge_"+self.name
        x, charge=self.surface_x, self.surface_charge
        pl, pf=line(x, charge, plotter=pl, plot_name=self.name, color="blue", label=self.name, **kwargs)
        pl.xlabel="x/center wavelength"
        pl.ylabel="surface charge"
        #pl.set_ylim(-1.0, 2.0)
        return pl

    def plot_surface_voltage(self, pl=None, **kwargs):
        if pl is None:
            pl="surface_voltage_"+self.name
        x, voltage=self.surface_x, self.surface_voltage
        pl, pf=line(x, voltage, plotter=pl, plot_name=self.name, color="blue", label=self.name, **kwargs)
        pl.xlabel="x/center wavelength"
        pl.ylabel="surface voltage"
        #pl.set_ylim(-1.0, 2.0)
        return pl

def test_plot(**kwargs):
    rho=Rho.process_kwargs(kwargs)
    rho.ft="single"
    kdiv2pi=(rho.fixed_freq[1]-rho.fixed_freq[0])/rho.vf
    k=2*pi*rho.fixed_freq/rho.vf
    lbda0=1.0 #rho.lbda0
    xx=linspace(-1.75*lbda0, 1.75*lbda0, 201)
    rhox=array([sum(2*kdiv2pi*rho.fixed_alpha*cos(k*x)) for x in xx])
    pl=line(xx, rhox, linewidth=0.5)[0]
    return pl
#test_plot().show()

@Rho.add_func
def element_factor_plot(pl="element_factor", **kwargs):
    rho=Rho.process_kwargs(kwargs)
    rho.ft="single"
    f=linspace(0.0, 500e9, 10000)
    print "start plot"
    pl=line(f/rho.f0, rho._get_alpha(f=f), plotter=pl, plot_name="single", color="blue", label="single finger", **kwargs)
    print "finish plot"
    rho.ft="double"
    pl= line(f/rho.f0, rho._get_alpha(f=f), plotter=pl, plot_name="double", color="red", label="double finger", linestyle="dashed")
    pl.xlabel="frequency/center frequency"
    pl.ylabel="element factor"
    pl.set_ylim(-1.0, 2.0)
    pl.set_xlim(0.0, 20.0)
    pl.legend()
    return pl

@Rho.add_func
def metallization_plot(pl="metalization", **kwargs):
    rho=Rho.process_kwargs(kwargs)
    rho.eta=0.5
    rho.ft="single"
    pl=line(rho.fixed_freq/rho.f0, rho.fixed_alpha, plotter=pl, plot_name="0.5", color="blue", label="0.5", **kwargs)
    rho.eta=0.75
    rho.fixed_reset()
    line(rho.fixed_freq/rho.f0, rho.fixed_alpha, plotter=pl, plot_name="0.6", color="red", label="0.6", **kwargs)
    rho.eta=0.25
    rho.fixed_reset()
    line(rho.fixed_freq/rho.f0, rho.fixed_alpha, plotter=pl, plot_name="0.4", color="green", label="0.4", **kwargs)
    pl.set_xlim(0.0, 20.0)
    pl.set_ylim(-2.0, 2.0)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="element factor"
    pl.legend()
    return pl

@Rho.add_func
def surface_charge_plot(pl="surface charge", **kwargs):
    rho=Rho.process_kwargs(kwargs)
    #rho.ft="single" #"double"
    #charge=real(fft.fftshift(fft.ifft(rho.fixed_alpha)))#.astype(float64)
    print rho.a, rho.g
    #print rho.surface_charge.dtype
    #print max(rho.surface_voltage/rho.epsinf)
    #x=linspace()
    #x=linspace(-rho.N_fixed/2+.001, rho.N_fixed/2+0.0, rho.N_fixed)/800.0
    print rho.surface_charge.shape, rho.surface_x.shape
    pieta=pi*rho.eta
    #a=0.25 #rho.a
    lbda0=1.0 #rho.lbda0
    x=linspace(-1.75*10*lbda0, 1.75*10*lbda0, 20001)
    s=linspace(0.0,1.0, 20001)

    def rh(x):
        m=int(2*x/(lbda0))
        if absolute(2*x/lbda0-m)<1.0/4.0:
            theta=4*pi*x/lbda0
            return 2/lbda0*2*sqrt(2.0)*((1.0)**m)/sqrt(cos(theta)-cos(pieta))*trapz(sin(pi*s)*cos((s-1/2)*theta)/rho.lgf1.Pv(-s),s)
        if absolute(2*x/lbda0-m-1)<1.0/4.0:
            theta=4*pi*x/lbda0
            return 2/lbda0*2*sqrt(2.0)*((1.0)**m)/sqrt(cos(theta)-cos(pieta))*trapz(sin(pi*s)*cos((s-1/2)*theta)/rho.lgf1.Pv(-s),s)
        if absolute(2*x/lbda0-m+1)<1.0/4.0:
            theta=4*pi*x/lbda0
            return 2/lbda0*2*sqrt(2.0)*((1.0)**m)/sqrt(cos(theta)-cos(pieta))*trapz(sin(pi*s)*cos((s-1/2)*theta)/rho.lgf1.Pv(-s),s)

        return 0.0

    rgh=array([rh(xx) for xx in x])/1.694
    line(1*x, rgh, linewidth=0.5, pl=pl)

    #line(real(fft.fft(rgh)))
    #line(imag(fft.fft(rgh)))

    line(rho.fixed_freq, rho.fixed_alpha)
    print "line done"
    pl, pf=line(rho.surface_x, rho.surface_charge*rgh[10000]/rho.surface_charge[rho.N_fixed/2], plotter=pl, plot_name="single", color="blue", label="single finger", **kwargs)
    #charge=real(fft.fftshift(fft.ifft(rho.fixed_alpha/rho.fixed_freq*rho.f0)))#.astype(float64)
    pl, pf=line(rho.surface_x, rho.surface_voltage*1e6, plotter=pl, plot_name="singled", color="red", label="single finger2", **kwargs)

    xprime=linspace(-2.000001, 2.0, 200) #[0.01, 1.01] #range(10)
    print "trapz"
    #line(xprime, array([trapz(rho.surcharge/absolute(x-xp), x) for xp in xprime]))
    print "trapz done"
    pl.xlabel="frequency/center frequency"
    pl.ylabel="element factor"
    #pl.legend()
    return pl

def surface_charge_plot2(pl="surface charge2", **kwargs):
    idt=idt_process(kwargs)
    idt.ft="single"
    charge=fft.fftshift(fft.ifft(idt.fixed_alpha))

    pl, pf=line( charge[:-400]+charge[400:], plotter=pl, plot_name="single", color="blue", label="single finger", **kwargs)


    #idt.ft="double"
    #idt.fixed_reset()
    #pl= line(idt.fixed_freq/idt.f0, idt.fixed_alpha, plotter=pl, plot_name="double", color="red", label="double finger", linestyle="dashed")[0]
    pl.xlabel="frequency/center frequency"
    pl.ylabel="element factor"
    #pl.legend()
    return pl
if __name__=="__main__":
    rho=Rho()
    print dir(rho)
    print rho.members().keys()
    rho.show()

    rho.ft="single"
    print rho.alpha
    rho.ft="double"
    print rho.alpha

    #element_factor_plot()#.show()
    surface_charge_plot().show()