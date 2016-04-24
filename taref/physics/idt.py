# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 01:07:15 2016

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.physics.fundamentals import sinc_sq, pi, eps0
from taref.core.atom_extension import private_property, get_tag
from taref.core.extra_setup import tagged_property, property_func
from taref.core.agent import Agent
from atom.api import Float, Int, Enum

from numpy import arange, linspace, sqrt
from matplotlib.pyplot import plot, show, xlabel, ylabel, title, xlim, ylim, legend

def eta(a, g):
    """metalization ratio"""
    return a/(a+g)

#def periodicity(a, g):
#    """periodicity of IDT?"""
#    return a+g

def K2(Dvv):
    r"""Coupling strength. K$^2=2\Delta v/v$"""
    return Dvv*2.0

def Dvv(K2):
    """other couplign strength. free speed minus metal speed all over free speed"""
    return K2/2.0

Ct_mult={"double" : sqrt(2), "single" : 1.0}
def Ct(mult, W, epsinf, Np):
    """Morgan page 16, 145"""
    return mult*W*epsinf*Np

def epsinf(mult, W, Ct, Np):
    """reversing capacitance to extract eps infinity"""
    return Ct/(mult*W*Np)

def lbda(vf, f):
    """wavelength relationship to speed and frequency"""
    return vf/f

def f(vf, lbda):
    """frequency relationship to speed and wavelength"""
    return vf/lbda

def g(a, eta):
    """gap given metalization and finger width
       eta=a/(a+g)
       => a=(a+g)*eta
       => (1-eta)*a=g*eta
       => g=a*(1/eta-1)"""
    return a*(1.0/eta-1.0)

def a_from_g(eta, g):
    """finger width given gap and metalization ratio
       eta=a/(a+g)
       => a=(a+g)*eta
       => (1-eta)*a=g*eta
       => a=g*eta/(1-eta)"""
    return g*eta/(1.0-eta)

mult_dict={"double" : 2.0, "single" : 1.0}
def a_from_lbda0(eta, lbda0, mult):
    """finger width from lbda0"""
    return eta*lbda0/(2.0*mult)

def lbda0_from_a(a, eta, mult):
    return a/eta*2.0*mult

def Ga_f(Ga_0, Np, f, f0):
    """sinc squared behavior of real part of IDT admittance"""
    return Ga_0*sinc_sq(Np*pi*(f-f0)/f0)

material_dict={"STquartz": dict(epsinf=5.6*eps0, Dvv=0.06e-2, vf=3159.0),
               'GaAs':     dict(epsinf=1.2e-10, Dvv=0.035e-2, vf=2900.0),
               'LiNbYZ':   dict(epsinf=46*eps0, Dvv=2.4e-2, vf=3488.0),
               'LiNb128':  dict(epsinf=56*eps0, Dvv=2.7e-2, vf=3979.0),
               'LiNbYZX':  dict(epsinf=46*eps0, Dvv=0.8e-2, vf=3770.0)}

class IDT(Agent):
    """Theoretical description of IDT"""
    base_name="IDT"
    #main_params=["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct",
    #            "material", "Dvv", "K2", "vf", "epsinf"]



    Ga_0=Float(1).tag(desc="Conductance at center frequency of IDT", label="G a0")
    f=Float(4.4e9).tag(desc="Operating frequency, e.g. what frequency is being stimulated/measured")

    ft=Enum("double", "single").tag(desc="finger type of IDT", label="Finger type", show_value=False)

    @tagged_property(desc="multiplier based on finger type")
    def mult(self):
        return {"double" : 2.0, "single" : 1.0}[self.ft]

    Np=Int(7).tag(desc="\# of finger pairs", low=1, tex_str=r"$N_p$", label="\# of finger pairs")

    ef=Int(0).tag(desc="for edge effect compensation",
                    label="\# of extra fingers", low=0)

    W=Float(25.0e-6).tag(desc="height of finger.", unit="um")

    eta=Float(0.5).tag(desc="metalization ratio")

    epsinf=Float(46*eps0).tag(desc="Capacitance of single finger pair per unit length", tex_str=r"$\epsilon_\infty$")

    Dvv=Float(2.4e-2).tag(desc="coupling strength", unit="%", tex_str=r"$\Delta v/v$", expression=r"$(v_f-v_m))/v_f$")

    vf=Float(3488.0).tag(desc="speed of SAW on free surface", unit="m/s", tex_str=r"$v_f$")

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')

    f0=Float(5.0e9).tag(unit="GHz", desc="Center frequency of IDT", reference="", tex_str=r"$f_0$", label="Center frequency")

    @property_func
    def _get_eta(self, a, g):
         return eta(a, g)

    #@tagged_property(desc="periodicity. this should be twice width for 50\% metallization")
    #def p(self, a, g):
    #    return a+g

    @tagged_property(desc="coupling strength", unit="%", tex_str=r"K$^2$", expression=r"K$^2=2\Delta v/v$")
    def K2(self, Dvv):
        return K2(Dvv)

    @K2.fget.setter
    def _get_Dvv(self, K2):
        return Dvv(K2)

    @tagged_property(unit="F", desc="Total capacitance of IDT", reference="Morgan page 16/145")
    def Ct(self, ft, W, epsinf, Np):
        return Ct(Ct_mult[ft], W, epsinf, Np)

    @Ct.fget.setter
    def _get_epsinf(self, ft, W, Ct, Np):
        return epsinf(Ct_mult[ft], W, Ct, Np)

    @tagged_property(unit="um", desc="Center wavelength", reference="")
    def lbda0(self, vf, f0):
        return lbda(vf, f0)

    @lbda0.fget.setter
    def _get_f0(self, vf, lbda0):
        return f(vf, lbda0)

    @tagged_property(desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz", unit="um")
    def g(self, a, eta):
        return g(a, eta)

    @g.fget.setter
    def _get_a_get_(self, eta, g):
        return a_from_g(eta, g)

    @tagged_property(desc="width of fingers", unit="um")
    def a(self, eta, lbda0, mult):
        return a_from_lbda0(eta, lbda0, mult)

    @a.fget.setter
    def _get_lbda0_get_(self, a, eta, mult):
        return lbda0_from_a(a, eta, mult)

    @tagged_property(desc="Ga adjusted for frequency f", label="Ga f")
    def Ga_f(self, Ga_0, Np, f, f0):
        return Ga_f(Ga_0, Np, f, f0)

    def _observe_material(self, change):
        if self.material=="STquartz":
            self.epsinf=5.6*eps0
            self.Dvv=0.06e-2
            self.vf=3159.0
        elif self.material=='GaAs':
            self.epsinf=1.2e-10
            self.Dvv=0.035e-2
            self.vf=2900.0
        elif self.material=='LiNbYZ':
            self.epsinf=46*eps0
            self.Dvv=2.4e-2
            self.vf=3488.0
        elif self.material=='LiNb128':
            self.epsinf=56*eps0
            self.Dvv=2.7e-2
            self.vf=3979.0
        elif self.material=='LiNbYZX':
            self.epsinf=46*eps0
            self.Dvv=0.8e-2
            self.vf=3770.0
        else:
            print "Material not listed"

    def _default_material(self):
        return 'LiNbYZ'

    @private_property
    def view_window2(self):
        from enaml import imports
        with imports():
            from taref.saw.idt_e import IDT_View
        return IDT_View(idt=self)

if __name__=="__main__":
    from taref.core.shower import shower
    a=IDT()
    b=IDT()

    log_debug(a.K2, b.K2)
    a.Dvv=5
    print a._get_Dvv(4)
    log_debug(a.get_member("K2").fget.fset_list)
    log_debug(a.get_member("K2").fset(a, 3))

    log_debug(a.get_member("K2").fset)

    print a.K2, b.K2
    for param in a.all_params:
        print get_tag(a, param, "unit")
    shower(a)
    print a.call_func("eta", a=0.2e-6, g=0.8e-6)#, vf=array([500.0, 600.0]), lbda0=array([0.5e-6, 0.6e-6]))
    a.plot_data("f0", lbda0=linspace(0.1e-6, 1.0e-6, 10000))
    print a.get_tag("lbda0", "unit_factor")
    show()
    if 1:
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