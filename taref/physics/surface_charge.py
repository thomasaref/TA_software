# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:43:08 2016

@author: thomasaref
"""

from taref.physics.fundamentals import pi, eps0, sin, cos, linspace, real, fft, array, absolute, float64, imag, sqrt, int64
from taref.physics.legendre import lgf, lgf_arr, Legendre
from atom.api import Float, Typed, Enum, Int, Bool
from taref.core.api import t_property, Agent, private_property, SProperty, log_func
from taref.plotter.api import line
from scipy.signal import hann
from scipy.fftpack import  rfft, irfft, ifft
from scipy.integrate import trapz, simps

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

    def _default_ft(self):
        return "double"

    @t_property(desc="multiplier based on finger type")
    def ft_mult(self, ft):
        return {"double" : 2.0, "single" : 1.0}[ft]

    f=Float(4.4e9).tag(desc="Operating frequency, e.g. what frequency is being stimulated/measured")

    f0=Float(5.0000001e9).tag(unit="GHz", desc="Center frequency of IDT", reference="", tex_str=r"$f_0$", label="Center frequency")

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
        return vf/f0

    @lbda0.setter
    def _get_f0(self, lbda0, vf):
        return vf/lbda0

    k=SProperty()
    @k.getter
    def _get_k(self, lbda):
        return 2*pi/lbda

    @k.setter
    def _get_lbda_get_k(self, k):
        return 2*pi/k

    k0=SProperty()
    @k0.getter
    def _get_k0(self, lbda0):
        return 2*pi/lbda0

    @k0.setter
    def _get_lbda0_get_k0(self, k0):
        return 2*pi/k0

    eta=Float(0.5).tag(desc="metalization ratio")

    @log_func
    def _get_eta(self, a, g):
         """metalization ratio"""
         return a/(a+g)

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
    def _get_a_get_g(self, g,  eta):
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
    def _get_lbda0_get_a(self, a, eta, ft_mult):
        return a/eta*2.0*ft_mult

    @private_property
    def fixed_freq(self):
        return linspace(self.fixed_freq_min, self.fixed_freq_max, self.N_fixed).astype(float64)


    N_fixed=Int(100000)
    fixed_freq_max=Float()
    fixed_freq_min=Float(0.01)

    def _default_fixed_freq_max(self):
        return 200.0*self.f0

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

    fixed_update=Bool(False)

    def fixed_reset(self):
        self.lgf1.Pv(0.0, -cos(pi*self.eta), 0)
        self.lgf2.Pv(self.fixed_freq_max/(2*self.ft_mult*self.f0), cos(pi*self.eta))
        self.get_member("fixed_freq").reset(self)
        self.get_member("fixed_alpha").reset(self)

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

    alpha=SProperty()
    @alpha.getter
    def _get_alpha(self, f, f0, ft_mult, eta, epsinf):
        m=self._get_m(f=f, f0=f0, ft_mult=ft_mult)
        s=self._get_s(f=f, f0=f0, ft_mult=ft_mult)
        return 2*sin(pi*s)/self.lgf1.Pv(-s)*self.lgf2.Pv(m)

    @private_property
    def surface_x(self):
        fs=self._get_fs(f=self.fixed_freq)
        df=1.0/(fs[1]-fs[0])/2.0#*self.lbda0/2
        return linspace(-df/2.0, df/2.0, self.N_fixed)

    @private_property
    def surface_charge(self):
        return fft.fftshift(real(ifft(self.fixed_alpha)))
        #Magcom*hann(len(Magcom)
        #return fft.fftshift(fft.fftfreq(self.N_fixed, 1.0)), fft.fftshift(real(fft.ifft(self.fixed_alpha)))
        #return real(fft.fftshift(fft.ifft(self.fixed_alpha)))#.astype(float64)

    @private_property
    def surface_voltage(self):
        lbda=self._get_lbda(f=self.fixed_freq)
        kCs=self._get_k(lbda)#*self.epsinf
        return fft.fftshift(real(fft.ifft(self.fixed_alpha/kCs))).astype(float64)

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


def element_factor_plot(pl="element_factor", **kwargs):
    rho=Rho.process_kwargs(kwargs)
    rho.ft="single"
    f=linspace(0.0, 500e9, 10000)
    print "start plot"
    pl, pf=line(f/rho.f0, rho._get_alpha(f=f), plotter=pl, plot_name="single", color="blue", label="single finger", **kwargs)
    print "finish plot"
    rho.ft="double"
    pl= line(f/rho.f0, rho._get_alpha(f=f), plotter=pl, plot_name="double", color="red", label="double finger", linestyle="dashed")[0]
    pl.xlabel="frequency/center frequency"
    pl.ylabel="element factor"
    pl.set_ylim(-1.0, 2.0)
    pl.legend()
    return pl

def surface_charge_plot(pl="surface charge", **kwargs):
    rho=Rho.process_kwargs(kwargs)
    rho.ft="single" #"double"
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
    #element_factor_plot()#.show()
    surface_charge_plot().show()