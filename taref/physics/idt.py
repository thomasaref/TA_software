# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 01:07:15 2016

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.physics.fundamentals import sinc_sq, pi, eps0
from taref.core.atom_extension import private_property, get_tag, tagged_property, log_func, tag_Property
#import taref.core.agent
#reload(taref.core.agent)
from taref.core.agent import Agent
from atom.api import Float, Int, Enum, Value, Property

from numpy import arange, linspace, sqrt, sin
from matplotlib.pyplot import plot, show, xlabel, ylabel, title, xlim, ylim, legend

#def property_func(func, **kwargs):
#    new_func=LogFunc(**kwargs)(func)
#    new_func.fset_list=[]
#    def setter(set_func):
#        s_func=LogFunc(**kwargs)(set_func)
#        s_func.pname=s_func.func_name.split("_get_")[1]
#        new_func.fset_list.append(s_func)
#        return s_func
#    new_func.setter=setter
#    return new_func
#
#class tagged_property(tag_Property):
#    def __call__(self, func):
#        return super(tagged_property, self).__call__(property_func(func, **self.kwargs))

def dict_property(**kwargs):
    def do_nothing(obj):
        pass
    return tagged_property(**kwargs)(do_nothing)

#class dict_property(tagged_property):
#    def __init__(self, key, dictify, **kwargs):
#        fget=self.dictify_fget(dictify, key)
#
#    def dictify_fget(self, private_param, dicty, key):
#        def getit(obj):
#            temp=getattr(obj, private_param)
#            if temp is None:
#                return dicty.get(getattr(obj, key), temp)
#            return temp
#        return getit
#
#    def dictify_fset(param, private_param):
#        def setit(obj, value):
#            return value
#        setit.pname=private_param
#        return setit


#class dict_Property(tag_Property):
#    def __call__(self, func):
#        new_func=super(dict_property, self).__call__(func)

def Ga_f(Ga_0, Np, f, f0):
    """sinc squared behavior of real part of IDT admittance"""
    return Ga_0*sinc_sq(Np*pi*(f-f0)/f0)



class IDT(Agent):
    """Theoretical description of IDT"""
    base_name="IDT"
    #main_params=["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct",
    #            "material", "Dvv", "K2", "vf", "epsinf"]

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')

    Dvv=Property(cached=True).tag(desc="coupling strength", unit="%", tex_str=r"$\Delta v/v$",
                          expression=r"$(v_f-v_m))/v_f$", key="material",
                            dictify={"STquartz" : 0.06e-2,
                                     'GaAs'     : 0.035e-2,
                                     'LiNbYZ'   : 2.4e-2,
                                     'LiNb128'  : 2.7e-2,
                                     'LiNbYZX'  : 0.8e-2})

    vf=Property(cached=True).tag(desc="speed of SAW on free surface", unit="m/s",
                                 tex_str=r"$v_f$", key="material",
                                 dictify={"STquartz"  : 3159.0,
                                          'GaAs'      : 2900.0,
                                          'LiNbYZ'    : 3488.0,
                                          'LiNb128'   : 3979.0,
                                          'LiNbYZX'   : 3770.0})

    epsinf=dict_property(desc="Capacitance of single finger pair per unit length",
                                     tex_str=r"$\epsilon_\infty$", key="material",
                                     dictify={"STquartz"  : 5.6*eps0,
                                              'GaAs'      : 1.2e-10,
                                              'LiNbYZ'    : 46.0*eps0,
                                              'LiNb128'   : 56.0*eps0,
                                              'LiNbYZX'   : 46.0*eps0})

    ft=Enum("double", "single").tag(desc="finger type of IDT", label="Finger type", show_value=False)

    mult=Property(cached=True).tag(desc="multiplier based on finger type", dictify={"double" : 2.0, "single" : 1.0}, key="ft")#[self.ft]

    Ga0_mult=Property(cached=True).tag(dictify={"single" : 1.694**2, "double" : (1.247*sqrt(2))**2},  key="ft") #{"single":2.87, "double":3.11}

    Ct_mult=Property(cached=True).tag(dictify={ "single" : 1.0, "double" : sqrt(2)}, key="ft")


    mu=Property(cached=True).tag(dictify={"single" : 1.694, "double" : 1.247}, key="ft")

    #coupling_mult_dict={"single" : 0.71775, "double" : 0.54995}

    @tagged_property()
    def coupling_mult(self, Ga0_mult, Ct_mult):
        return Ga0_mult/(4*Ct_mult)

    f=Float(4.4e9).tag(desc="Operating frequency, e.g. what frequency is being stimulated/measured")

    Np=Float(7).tag(desc="\# of finger pairs", low=0.5, tex_str=r"$N_p$", label="\# of finger pairs")

    ef=Int(0).tag(desc="for edge effect compensation",
                    label="\# of extra fingers", low=0)

    W=Float(25.0e-6).tag(desc="height of finger.", unit="um")

    eta=Float(0.5).tag(desc="metalization ratio")

    f0=Float(5.0e9).tag(unit="GHz", desc="Center frequency of IDT", reference="", tex_str=r"$f_0$", label="Center frequency")

    @tagged_property(unit="F", desc="Total capacitance of IDT", reference="Morgan page 16/145")
    def C(self, epsinf, Ct_mult, W, Np):
        """Morgan page 16, 145"""
        return Ct_mult*W*epsinf*Np

    @C.fget.setter
    def _get_epsinf(self, C, Ct_mult, W, Np):
        """reversing capacitance to extract eps infinity"""
        return C/(Ct_mult*W*Np)

    @log_func
    def _get_eta(self, a, g):
         """metalization ratio"""
         return a/(a+g)

    @tagged_property(desc="coupling strength", unit="%", tex_str=r"K$^2$", expression=r"K$^2=2\Delta v/v$")
    def K2(self, Dvv):
        r"""Coupling strength. K$^2=2\Delta v/v$"""
        return Dvv*2.0

    @K2.fget.setter
    def _get_Dvv(self, K2):
        """other couplign strength. free speed minus metal speed all over free speed"""
        return K2/2.0

    @tagged_property(desc="Conductance at center frequency")
    def Ga0(self, Ga0_mult, f0, epsinf, W, Dvv, Np):
        """Ga0 from morgan"""
        return Ga0_mult*2*pi*f0*epsinf*W*Dvv*(Np**2)

    @tagged_property()
    def Ga0div2C(self, couple_mult, f0, K2, Np):
        """coupling at center frequency, in Hz (2 pi removed)"""
        return couple_mult*f0*K2*Np

    @tagged_property()
    def X(self, Np, f, f0):
        """standard frequency dependence"""
        return Np*pi*(f-f0)/f0

    @tagged_property()
    def coupling(self, f, couple_mult, f0, K2, Np):
        gamma0=self.Ga0div2C_f(couple_mult, f0, K2, Np)
        gX=self.X_f(Np, f, f0)
        return gamma0*(sin(gX)/gX)**2.0

    @tagged_property()
    def Lamb_shift(self, f, mult, f0, K2, Np):
        """returns Lamb shift"""
        gamma0=self.Ga0div2C_f(mult, f0, K2, Np)
        gX=self.X_f(Np, f, f0)
        return -gamma0*(sin(2.0*gX)-2.0*gX)/(2.0*gX**2.0)

    @tagged_property()
    def Ga(self, f, couple_mult, f0, K2, Np, C):
        return self.coupling_f(f, couple_mult, f0, K2, Np)*2*C*2*pi

    @tagged_property()
    def Ba(self, f, mult, f0, K2, Np, C):
        return -self.Lamb_shift_f(f, mult, f0, K2, Np)*2*C*2*pi

    @tagged_property()
    def lbda(self, vf, f):
        """wavelength relationship to speed and frequency"""
        return vf/f

    @lbda.fget.setter
    def _get_f(self, lbda, vf):
        """frequency relationship to speed and wavelength"""
        return vf/lbda

    @tagged_property(unit="um", desc="Center wavelength", reference="")
    def lbda0(self, vf, f0):
        return self.lbda_f(vf, f0)

    @lbda0.fget.setter
    def _get_f0(self, lbda0, vf):
        return self._get_f(lbda=lbda0, vf=vf)

    @tagged_property(desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz", unit="um")
    def g(self, a, eta):
        """gap given metalization and finger width
        eta=a/(a+g)
        => a=(a+g)*eta
        => (1-eta)*a=g*eta
        => g=a*(1/eta-1)"""
        return a*(1.0/eta-1.0)

    @g.fget.setter
    def _get_a_get_(self, g,  eta):
        """finger width given gap and metalization ratio
        eta=a/(a+g)
        => a=(a+g)*eta
        => (1-eta)*a=g*eta
        => a=g*eta/(1-eta)"""
        return g*eta/(1.0-eta)

    @tagged_property(desc="width of fingers", unit="um")
    def a(self, eta, lbda0, ft_mult):
        """finger width from lbda0"""
        return eta*lbda0/(2.0*ft_mult)

    @a.fget.setter
    def _get_lbda0_get_(self, a, eta, ft_mult):
        return a/eta*2.0*ft_mult

    @tagged_property(desc="Ga adjusted for frequency f", label="Ga f")
    def Ga_f(self, Ga_0, Np, f, f0):
        return Ga_f(Ga_0, Np, f, f0)

#    def _observe_material(self, change):
#        if self.material=="STquartz":
#            self.epsinf=5.6*eps0
#            self.Dvv=0.06e-2
#            self.vf=3159.0
#        elif self.material=='GaAs':
#            self.epsinf=1.2e-10
#            self.Dvv=0.035e-2
#            self.vf=2900.0
#        elif self.material=='LiNbYZ':
#            self.epsinf=46*eps0
#            self.Dvv=2.4e-2
#            self.vf=3488.0
#        elif self.material=='LiNb128':
#            self.epsinf=56*eps0
#            self.Dvv=2.7e-2
#            self.vf=3979.0
#        elif self.material=='LiNbYZX':
#            self.epsinf=46*eps0
#            self.Dvv=0.8e-2
#            self.vf=3770.0
#        else:
#            print "Material not listed"

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
    b=IDT(ft="single")
    #a.mult=5
    print a.mu, a.mult, b.mu, b.mult
    print a.coupling_mult, b.coupling_mult
    a.ft="single"
    a.mult=None
    print a.mu, a.mult, b.mu, b.mult
    print a.coupling_mult, b.coupling_mult

    print a.epsinf, a.C
    a.epsinf=4e-10
    print a.C
    a.C=7.1e-14
    print a.epsinf, a.C



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
    #a.show()
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