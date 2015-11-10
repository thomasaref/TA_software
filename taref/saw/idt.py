# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 11:08:19 2015

@author: thomasaref
"""
from taref.core.agent import SubAgent
from taref.core.backbone import updater
from taref.physics.fundamentals import (eps0, sqrt, pi, Delta, hbar, e, h,
                                        sin, sinc_sq, linspace, zeros)
from taref.core.log import log_debug
from atom.api import Enum, Int, Float, observe, Bool, Property, Str, List, Range

class IDT(SubAgent):
    ft=Enum("double", "single").tag(desc="'double' for double fingered, 'single' for single fingered.")

    @property
    def mult(self):
        return {"double" : 2.0, "single" : 1.0}[self.ft]

    Np=Int(7).tag(desc="number of finger pairs. this should be at least 1", low=1)
    ef=Int(0).tag(desc="number of extra fingers to compensate for edge effect. Defaults to 0")
    a=Float(0.05e-6).tag(desc="width of fingers (um). same as gap generally.", unit="um")
    W=Float(25.0e-6).tag(desc="height of finger.", unit="um")
    g=Float(0.05e-6).tag(desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz", unit="um")
    eta=Float(0.5).tag(desc="metalization ratio")
    epsinf=Float(46*eps0)
    Dvv=Float(2.4e-2).tag(desc="coupling strength: K^2/2",
                      unit="%")
    K2=Float(4.8e-2).tag(desc="coupling strength: K^2/2",
                      unit="%")

    v=Float(3488.0).tag(desc="speed of SAW", unit=" m/s")
    lock_eta=Bool(True).tag(desc="boolean controlling if metalization ratio is locked")

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')


    f0=Float(5.0e9).tag(label="f0",
                unit="GHz",
                desc="Center frequency",
                reference="")

    lbda0=Float(0.775e-6).tag(label="lbda0",
                unit="um",
                desc="Center wavelength",
                reference="")

    Ct=Float().tag(label="Ct",
                   unit="F",
                   desc="Total capacitance of IDT",
                   reference="Morgan page 16/145")

    @Property
    def p(self):
        return self.a+self.g
    p.tag(desc="periodicity. this should be twice width for 50% metallization")

    @observe('Dvv')
    @updater
    def _update_K2(self, change):
        self.K2=self.Dvv*2.0

    @observe('K2')
    @updater
    def _update_Dvv(self, change):
        self.Dvv=self.K2/2.0
        
    @observe('a', 'g')
    @updater
    def _update_eta(self, change):
        if not self.lock_eta:
            self.eta=self.a/(self.a+self.g)

    @observe('g', 'eta')
    @updater
    def _update_a(self, change):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => a=g*eta/(1-eta)"""
        self.a=self.g*self.eta/(1-self.eta)

    @observe('a', 'eta')
    @updater
    def _update_g(self, change):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => g=a*(1/eta-1)"""
        self.g= self.a*(1.0/self.eta-1.0)

    @observe('ft', 'W', 'epsinf', 'Np')
    @updater
    def _update_Ct(self, change):
        self.Ct=sqrt(self.mult)*self.W*self.epsinf*self.Np

    @observe('f0', 'v')
    @updater
    def _update_lbda0(self, change):
        self.lbda0=self.v/self.f0
        
    @observe('a', 'g')
    @updater
    def _update_lbda02(self, change):
        self.lbda0=(self.a+self.g)*2*self.mult

    @observe('ft', 'eta', 'lbda0')
    @updater
    def _update_a2(self, change):
        self.a=self.eta*self.lbda0/(2*self.mult)

    @observe('v', 'lbda0')
    @updater
    def _update_f0(self, change):
        self.f0=self.v/self.lbda0

    def _observe_material(self, change):
        if self.material=="STquartz":
            self.epsinf=5.6*eps0
            self.Dvv=0.06e-2
            self.v=3159.0
        elif self.material=='GaAs':
            self.epsinf=1.2e-10
            self.Dvv=0.035e-2
            self.v=2900.0
        elif self.material=='LiNbYZ':
            self.epsinf=46*eps0
            self.Dvv=2.4e-2
            self.v=3488.0
        elif self.material=='LiNb128':
            self.epsinf=56*eps0
            self.Dvv=2.7e-2
            self.v=3979.0
        elif self.material=='LiNbYZX':
            self.epsinf=46*eps0
            self.Dvv=0.8e-2
            self.v=3770.0
        else:
            print "Material not listed"

    def _default_material(self):
        return 'LiNbYZ' #'GaAs'

    @property
    def base_name(self):
        return "idt"

def tomobserve(*pairs):
    obshandle=observe(*pairs)
    return TomHandler(obshandle, pairs)

from atom.atom import ObserveHandler

class TomHandler(ObserveHandler):
    def __init__(self, obshandle, pairs):
        self.inputpairs=pairs
        self.pairs = obshandle.pairs
        self.func = obshandle.func
        self.funcname = obshandle.funcname
        
    def __call__(self, func):
        """ Called to decorate the function."""
        func=updater(func)
        func.pairs=self.inputpairs
        return super(TomHandler, self).__call__(func)

from numpy import ndarray
class QDT(IDT):
    Ic=Float().tag(label="Critical current", 
                   desc="critical current of SQUID", unit="nA")
    Rn=Float(1.0e3).tag(desc="Normal resistance of SQUID", unit="kOhm")
    Ejmax=Float().tag(desc="""Max Josephson Energy""",
                       unit="GHz", unit_factor=1.0e9*h)
    Ec=Float().tag(desc="""Charging Energy""", 
                    unit="GHz", unit_factor=1.0e9*h)
    G_f0=Float().tag(desc="""Coupling at IDT center frequency""", unit="GHz")
    f=Float(4.5e9).tag(desc="""Operating frequency of qubit""", unit="GHz")
    G_f=Float().tag(desc="""Coupling adjusted by sinc^2""", unit="GHz")                    
 
#    def _validate_f(self, old, new):
#        if isinstance(new, ndarray):
#            self.set_tag("f", sweep=new)
#            test=new[0]
#        else:
#            test=new
#        assert isinstance(test, float)
#        return test
        
    def G_f0_func(self, Np, K2, f0):
        return 0.45*Np*K2*f0

    def Ic_func(self, Rn):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Rn

    def Ejmax_func(self, Ic):
        """Josephson energy"""
        return hbar*Ic/(2.0*e)

    def Ec_func(self, Ct):
        """Charging energy"""
        print e**2/(2.0*Ct)
        return e**2/(2.0*Ct)

#    def get_names(self, *args, **kwargs):
#        templist=[]        
#        for name in args:
#            item=kwargs.get(name, getattr(self, name))
#            templist.append(item)
#        return templist

    def G_f_func(self, G_f0, Np, f, f0):
        return G_f0*sinc_sq(Np*pi*(f-f0)/f0)
    
    #def test_func(self, G_f0, N_p, f, f0):
    #    pass
        
    #@tomobserve("G_f0", "Np", "f", "f0")
    #def _update_G_f(self, change):
    #    self.G_f=self.G_f_func(G_f0=self.G_f0, Np=self.Np, f=self.f, f0=self.f0)

    def plotty(self, zname, **kwargs):
         if hasattr(self, zname+"_func"):
             func=getattr(self, zname+"_func")
             f=func.im_func
             argcount=f.func_code.co_argcount
             argnames=list(f.func_code.co_varnames[0:argcount])
             if "self" in argnames:
                 argnames.remove("self")
            def _updat_(change):
                kwargs={}
                for arg in argnames:
                    kwargs[arg]=getattr(self, arg)
                setattr(self, param, getattr(self, param+"_func")(**kwargs))
             zdata=func(**kwargs)
             xdata=kwargs.values()[0]
             plot(xdata, zdata)

         
if __name__=="__main__":
    from matplotlib.pyplot import plot, show, xlabel, ylabel, title, xlim, ylim, legend

    #a=IDT()
    a=QDT()
    Np=9
    f0=4.500001e9
    
    
    #a.f=linspace(4.0e9, 11.0e9, 2001)
    #a.observe(("G_f0", "Np", "f", "f0"), a._update_G_f)
    #print dir(a.test_func.im_func)
    
    #print a.f
    print a.get_tag("f", "sweep")
    #a.plotty("G_f", f=linspace(4.0e9, 11.0e9, 2001))
    #show()
    #a.Rn=(7.62e3+7.96e3)/2.0
    #f=
#    G=zeros(frq.shape)
#    from numpy import shape
#    print frq.shape
#    print shape(frq)
#    print shape(G)
#    for n, f in enumerate(frq):
#        a.f=f
#        G[n]=a.G_f
    #print a._update_Ic.pairs
    f=a.get_tag("f", "sweep")
    #plot(f/1.0e9, a.G_f_func(f=f))
    #show()

    a.show()

#from scipy.constants import epsilon_0 as eps0
#from numpy import sqrt

#class IDT(EBL_Base):
#    df=Enum("single", "double").tag(desc="'double' for double fingered, 'single' for single fingered. defaults to double fingered")
#    Np=Int(36).tag(desc="number of finger pairs. this should be at least 1 and defaults to 36.")
#    ef=Int(0).tag(desc="number of extra fingers to compensate for edge effect. Defaults to 0")
#    a=Float(0.096).tag(unit="um", desc="width of fingers (um). same as gap generally. Adjusting relative to gap is equivalent to adjusting the bias in Beamer")
#    gap=Float(0.096).tag(unit="um", desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz")
#    offset=Float(0.5).tag(unit="um", desc="gap between electrode and end of finger. The vertical offset of the fingers. Setting this to zero produces a shorted reflector")
#    W=Float(25.5).tag(unit="um", desc="height of finger")
#    hbox=Float(20.0).tag(desc="height of electrode box")
#    wbox=Float(30.0).tag(desc="width of electrode box. Setting to 0.0 (default) makes it autoscaling so it matches the width of the IDT")
#
#    epsinf=Float()
#    Dvv=Float()
#    v=Float()
#    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')
#
#    def _observe_material(self, change):
#        if self.material=="STquartz":
#            self.epsinf=5.6*eps0
#            self.Dvv=0.06e-2
#            self.v=3159.0
#        elif self.material=='GaAs':
#            self.epsinf=1.2e-10
#            self.Dvv=0.035e-2
#            self.v=2900.0
#        elif self.material=='LiNbYZ':
#            self.epsinf=46*eps0
#            self.Dvv=2.4e-2
#            self.v=3488.0
#        elif self.material=='LiNb128':
#            self.epsinf=56*eps0
#            self.Dvv=2.7e-2
#            self.v=3979.0
#        elif self.material=='LiNbYZX':
#            self.epsinf=46*eps0
#            self.Dvv=0.8e-2
#            self.v=3770.0
#        else:
#            log_warning("Material not listed")
#
#    f0=Float().tag(label="f0",
#                unit="GHz",
#                desc="Center frequency",
#                reference="")
#
#    @observe('w', 'v', 'gap', 'df')
#    def _get_f0(self, change):
#        v,a, g=self.v, self.a*1e-6, self.gap*1e-6
#        p=g+a
#        if self.df:
#            lbda0=4*p
#        else:
#            lbda0=2*p
#        self.f0=v/lbda0/1.0e9
#
#
#    Ct=Property().tag(label="Ct",
#                   unit="F",
#                   desc="Total capacitance of IDT",
#                   reference="Morgan page 16/145")
#    #@observe('epsinf', 'h', 'Np', 'df')
#    def _get_Ct(self):
#        W, epsinf, Np=self.h*1e-6, self.epsinf, self.Np
#        if self.df=="double":
#            return sqrt(2.0)*W*epsinf*Np
#        return W*epsinf*Np
#
#    def _default_material(self):
#        return 'LiNbYZ' #'GaAs'