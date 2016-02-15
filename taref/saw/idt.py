# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 01:07:15 2016

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.physics.fundamentals import sinc_sq, pi, eps0
from taref.core.atom_extension import private_property
from taref.core.extra_setup import tagged_property, property_func
from taref.core.agent import Agent
from atom.api import Float, Int, Enum, cached_property

from numpy import arange, linspace
from matplotlib.pyplot import plot, show, xlabel, ylabel, title, xlim, ylim, legend

def plot_data(self, zname, **kwargs):
     """pass in an appropriate kwarg to get zdata for the zname variable back"""
     xmult=kwargs.pop("xmult", 1.0)
     zmult=kwargs.pop("zmult", 1.0)
     label=kwargs.pop("label", "")

     if "xlim" in kwargs:
         xlim(kwargs["xlim"])

     if "ylim" in kwargs:
         ylim(kwargs["ylim"])

     zunit=self.get_tag(zname, "unit")
     zunit_factor=self.get_tag(zname, "unit_factor", 1.0)

     if zunit is None:
         zlabel_str=zname
     else:
         zlabel_str="{0} [{1}]".format(zname, zunit)

     ylabel(kwargs.pop("ylabel", zlabel_str))

     add_legend=kwargs.pop("legend", False)

     title_str=kwargs.pop("title", None)
     xlabel_str=kwargs.pop("xlabel", None)

     if len(kwargs)==1:
         xname, xdata=kwargs.popitem()
         zdata=self.call_func(zname, **{xname:xdata})
         xunit=self.get_tag(xname, "unit")
         xunit_factor=self.get_tag(xname, "unit_factor", 1.0)
     else:
         xname="#"
         xdata=arange(len(getattr(self, zname)))
         xunit=None
         xunit_factor=1.0#self.get_tag(xname, "unit_factor", 1.0)

     if xlabel_str is None:
         if xunit is None:
             xlabel_str=xname
         else:
             xlabel_str="{0} [{1}]".format(xname, xunit)
     xlabel(xlabel_str)

     if title_str is None:
         title_str="{0} vs {1}".format(zname, xname)
     title(title_str)
     #print xdata.shape, zdata.shape
     plot(xdata/xunit_factor*xmult, zdata/zunit_factor*zmult, label=label)

     if add_legend:
         legend()

class IDT(Agent):
    """Theoretical description of IDT"""
    base_name="IDT"
    #main_params=["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct",
    #            "material", "Dvv", "K2", "vf", "epsinf"]



    Ga_0=Float(1).tag(desc="Conductance at center frequency of IDT")
    f=Float(4.4e9).tag(desc="Operating frequency, e.g. what frequency is being stimulated/measured")

    ft=Enum("double", "single").tag(desc="finger type of IDT", label="Finger type", show_value=False)

    @tagged_property(desc="multiplier based on finger type")
    def mult(self):
        return {"double" : 2.0, "single" : 1.0}[self.ft]

    Np=Int(7).tag(desc="number of finger pairs. this should be at least 1", low=1)

    ef=Int(0).tag(desc="number of extra fingers to compensate for edge effect.",
                    label="# of extra fingers", low=0)

    W=Float(25.0e-6).tag(desc="height of finger.", unit="um")

    eta=Float(0.5).tag(desc="metalization ratio")

    epsinf=Float(46*eps0).tag(desc="Capacitance of single finger pair per unit length")

    Dvv=Float(2.4e-2).tag(desc="coupling strength: K^2/2", unit="%")

    vf=Float(3488.0).tag(desc="speed of SAW", unit=" m/s")

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')

    f0=Float(5.0e9).tag(unit="GHz", desc="Center frequency", reference="")

    @property_func
    def _get_eta(self, a, g):
         return a/(a+g)

    @tagged_property(desc="periodicity. this should be twice width for 50% metallization")
    def p(self, a, g):
        return a+g

    @tagged_property(desc="coupling strength", unit="%")
    def K2(self, Dvv):
        return Dvv*2.0

    @K2.fget.setter
    def _get_Dvv(self, K2):
        return K2/2.0

    @tagged_property(unit=" F", desc="Total capacitance of IDT", reference="Morgan page 16/145")
    def Ct(self, ft, W, epsinf, Np):
        m={"double" : 1.414213562373, "single" : 1.0}[ft]
        return m*W*epsinf*Np

    @tagged_property(unit="um", desc="Center wavelength", reference="")
    def lbda0(self, vf, f0):
        return vf/f0

    @lbda0.fget.setter
    def _get_f0(self, vf, lbda0):
        return vf/lbda0

    @tagged_property(desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz", unit="um")
    def g(self, a, eta):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => g=a*(1/eta-1)"""
        return a*(1.0/eta-1.0)

    @g.fget.setter
    def _get_a_get_(self, eta, g):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => a=g*eta/(1-eta)"""
        return g*eta/(1.0-eta)

    @tagged_property(desc="width of fingers (um).", unit="um")
    def a(self, eta, lbda0, mult):
        return eta*lbda0/(2.0*mult)

    @a.fget.setter
    def _get_lbda0_get_(self, a, eta, mult):
        return a/eta*2.0*mult

    @tagged_property(desc="Ga adjusted for frequency f")
    def Ga_f(self, Ga_0, Np, f, f0):
        return Ga_0*sinc_sq(Np*pi*(f-f0)/f0)

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