# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 11:36:10 2016

@author: thomasaref
"""

from taref.core.agent import Agent
from taref.core.atom_extension import get_tag
from taref.physics.fundamentals import (eps0, sqrt, pi, Delta, hbar, e, h, kB, ndarray, array, eig, delete,
                                        sin, sinc_sq, linspace, zeros, absolute, cos, arange)
from taref.core.extra_setup import tagged_property, property_func
from atom.api import Float, Enum
from taref.core.universal import Array
from numpy.linalg import eigvalsh, eigvals

class Qubit(Agent):
    """Theoretical description of qubit"""

    superconductor=Enum("Al")

    def _observe_superconductor(self, change):
        if self.superconductor=="Al":
            #self.Tc=1.3157 #critical temperature of aluminum
            self.Delta=200.0e-6*e #gap of aluminum

    Tc=Float(1.315).tag(desc="Critical temperature of superconductor", unit="K")

    @tagged_property(label="Gap", tex_str=r"$\Delta(0)$", unit="ueV", desc="Superconducting gap 200 ueV for Al",
                     reference="BCS", expression=r"$1.764 k_B T_c$")
    def Delta(self, Tc):
        return 1.764*kB*Tc

    @Delta.fget.setter
    def _get_Tc(self, Delta):
        return Delta/(1.764*kB)



    base_name="qubit"
    #def _default_main_params(self):
    #    return ["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct",
    #            "material", "Dvv", "K2", "vf", "epsinf",
    #            "Rn", "Ic", "Ejmax", "Ej", "Ec", "EjmaxdivEc", "EjdivEc",
    #            "fq", "fq_max", "fq_max_full", "flux_over_flux0", "G_f0", "G_f",
   #             "ng", "Nstates", "EkdivEc"]

    loop_width=Float(1.0e-6).tag(desc="loop width of SQUID", unit="um", label="loop width")
    loop_height=Float(1.0e-6).tag(desc="loop height of SQUID", unit="um", label="loop height")

    @tagged_property(desc="Area of SQUID loop", unit="um^2", expression="$width \times height$", comment="Loop width times loop height", label="loop area")
    def loop_area(self, loop_width, loop_height):
        return loop_width*loop_height

    Cq=Float(1.0e-12).tag(desc="shunt capacitance", unit="fF", tex_str=r"$C_q$")

    Rn=Float(10.0e3).tag(desc="Normal resistance of SQUID", unit="kOhm", label="DC Junction resistance", tex_str=r"$R_n$")

    @tagged_property(desc="critical current of SQUID", unit="nA", label="Critical current", tex_str=r"$I_C$")
    def Ic(self, Rn):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Rn

    @Ic.fget.setter
    def _get_Rn(self, Ic):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Ic

    @tagged_property(desc="""Max Josephson Energy""", unit="hGHz")#, unit_factor=1.0e9*h)
    def Ejmax(self, Ic):
        """Josephson energy"""
        return hbar*Ic/(2.0*e)

    @Ejmax.fget.setter
    def _get_Ic(self, Ejmax):
        """inverse Josephson energy"""
        return Ejmax*(2.0*e)/hbar

    @tagged_property(desc="Charging Energy", unit="hGHz")#, unit_factor=1.0e9*h)
    def Ec(self, Cq):
        """Charging energy"""
        return e**2/(2.0*Cq)

    @Ec.fget.setter
    def _get_Cq(self, Ec):
        return e**2/(2.0*Ec)

    @Ec.fget.setter
    def _get_Ejmax(self, Ec, EjmaxdivEc):
        return EjmaxdivEc*Ec

    @tagged_property(desc="Maximum Ej over Ec")
    def EjmaxdivEc(self, Ejmax, Ec):
        return Ejmax/Ec


    @tagged_property(unit="hGHz")#, unit_factor=1.0e9*h)
    def Ej(self, Ejmax, flux_over_flux0):
        return Ejmax*absolute(cos(pi*flux_over_flux0))

    @tagged_property(desc="Ej over Ec")
    def EjdivEc(self, Ej, Ec):
        return Ej/Ec

    @tagged_property(unit="hGHz", label="fq max")#, unit_factor=1.0e9*h)
    def fq_max(self, Ejmax, Ec):
        return sqrt(8.0*Ejmax*Ec)

    @tagged_property(unit="hGHz", label="fq max full")#, unit_factor=1.0e9*h)
    def fq_max_full(self, Ejmax, Ec):
        return  h*self._get_fq(Ejmax, Ec)

    @tagged_property(desc="""Operating frequency of qubit""", unit="GHz")
    def fq(self, Ej, Ec):
        return self._get_fq(Ej, Ec)

    def _get_fq(self, Ej, Ec):
        E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
        E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
        return (E1-E0)/h

    @tagged_property(desc="absolute anharmonicity", unit="hGHz")
    def anharm(self, Ej, Ec):
        E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
        E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
        E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
        return (E2-E1)-(E1-E0)

    def _get_Ej(self, fq, Ec):
        """h*fq=sqrt(8.0*Ej*Ec) - Ec"""
        return ((h*fq+Ec)**2)/(8.0*Ec)

    voltage=Float().tag(unit="V")
    offset=Float(0.09).tag(unit="V", log=False)
    flux_factor=Float(0.195)

    @tagged_property()
    def flux_over_flux0(self, voltage, offset, flux_factor):
        return (voltage-offset)*flux_factor

    @flux_over_flux0.fget.setter
    def _get_voltage(self, flux_over_flux0, offset, flux_factor):
        return flux_over_flux0/flux_factor+offset

    #@tagged_property()
    def flux_parabola(self, voltage, offset, flux_factor, Ec):
        flux_over_flux0=self.call_func("flux_over_flux0", voltage=voltage, offset=offset, flux_factor=flux_factor)
        Ej=self.call_func("Ej", flux_over_flux0=flux_over_flux0)
        return self._get_fq(Ej=Ej, Ec=Ec)

    def detuning(self, f0, flux_over_flux0):
        return 2.0*pi*(f0 - self.call_func("flux_parabola", flux_over_flux0))


    def indiv_EkdivEc(self, ng, Ec, Ej, Nstates, order):
        NL=2*Nstates+1
        A=zeros((NL, NL))
        for b in range(0,NL):
            A[b, b]=4.0*Ec*(b-Nstates-a)**2
            if b!=NL-1:
                A[b, b+1]= -Ej/2.0
            if b!=0:
                A[b, b-1]= -Ej/2.0
        w,v=eig(A)
        print w, v
        #for n in range(order):



    def update_EkdivEc(self, ng, Ec, Ej, Nstates, order):
        """calculates transmon energy level with N states (more states is better approximation)
        effectively solves the mathieu equation but for fractional inputs (which doesn't work in scipy.special.mathieu_a)"""

#        if type(ng) not in (int, float):
#            d=zeros((order, len(ng)))
#        elif type(Ec) not in (int, float):
#            d=zeros((order, len(Ec)))
#        elif type(Ej) not in (int, float):
#            d=zeros((order, len(Ej)))
        if type(ng) in (int, float):
            ng=array([ng])
        d1=[]
        d2=[]
        d3=[]
        Ej=Ej/Ec
        Ec=1.0#/4.0
        for a in ng:
            NL=2*Nstates+1
            A=zeros((NL, NL))
            for b in range(0,NL):
                A[b, b]=4.0*Ec*(b-Nstates-a)**2
                if b!=NL-1:
                    A[b, b+1]= -Ej/2.0
                if b!=0:
                    A[b, b-1]= -Ej/2.0
            #w,v=eig(A)
            w=eigvalsh(A)
            d=w[0:order]
#            d1.append(min(w))#/h*1e-9)
#            w=delete(w, w.argmin())
#            d2.append(min(w))#/h*1e-9)
#            w=delete(w, w.argmin())
#            d3.append(min(w))#/h*1e-9)

        return array([array(d1), array(d2), array(d3)]).transpose()

    def sweepEc():
        Ecarr=Ej/EjoverEc
        E01a=sqrt(8*Ej*Ecarr)-Ecarr
        data=[]
        for Ec in Ecarr:
            d1, d2, d3= EkdivEc(ng=ng, Ec=Ec, Ej=Ej, N=50)
            E12=d3[0]-d2[0]
            E01=d2[0]-d1[0]
            anharm2=(E12-E01)#/E01
            data.append(anharm2)
        Ctr=e**2/(2.0*Ecarr*h*1e9)
        return E01a, Ctr, data, d1, d2, d3

    def get_plot_data(self, zname, **kwargs):
         """pass in an appropriate kwarg to get zdata for the zname variable back"""
         arg=kwargs.keys()[0]
         func_name=[upd for upd in self.get_tag(arg, "update") if upd.split("_update_")[1]==zname][0]
         func=getattr(self, func_name)
         f=func.im_func
         for name in f.argnames:
             if name not in kwargs:
                 kwargs[name]=getattr(self, name)
         return func(**kwargs)

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
             zdata=self.get_plot_data(zname, **{xname:xdata})
             xunit=self.get_tag(xname, "unit")
             xunit_factor=self.get_tag(xname, "unit_factor", 1.0)
         else:
             xname="#"
             xdata=arange(len(getattr(self, zname)))
             xunit=None
             xunit_factor=self.get_tag(xname, "unit_factor", 1.0)

         if xlabel_str is None:
             if xunit is None:
                 xlabel_str=xname
             else:
                 xlabel_str="{0} [{1}]".format(xname, xunit)
         xlabel(xlabel_str)

         if title_str is None:
             title_str="{0} vs {1}".format(zname, xname)
         title(title_str)
         print xdata.shape, zdata.shape
         plot(xdata*xunit_factor*xmult, zdata*zunit_factor*zmult, label=label)

         if add_legend:
             legend()

if __name__=="__main__":
    t=Qubit()
    print t.call_func("flux_over_flux0", voltage=linspace(0,1,10))
    print t.call_func("Ej", flux_over_flux0=linspace(0,1,10))
    print t.call_func("fq", Ej=linspace(0,1,10))

    t.show()