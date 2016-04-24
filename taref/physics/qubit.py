# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:45:44 2016

@author: thomasaref

Collection of functions relating to qubits, particularly transmons
"""

from scipy.constants import e, h, hbar, k as kB, epsilon_0 as eps0, pi
c_eta = 0.8

from numpy import (sin, cos, sqrt, exp, empty, mean, exp, log10, arange, array, ndarray, delete,
                   absolute, dtype, angle, amin, amax, linspace, zeros, shape)


from taref.core.api import Agent, Array
from taref.core.extra_setup import tagged_property
from atom.api import Enum, Float, Int

Tc_Al=1.315 #critical temperature of aluminum
Delta_Al=200.0e-6*e #gap of aluminum

def Delta(Tc):
    """BCS theory superconducting gap"""
    return 1.764*kB*Tc

def Tc(Delta):
    return Delta/(1.764*kB)

def Ic_from_Rn(Rn, Delta):
    """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
    return pi*Delta/(2.0*e)/Rn

def Rn(Ic, Delta):
    """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
    return pi*Delta/(2.0*e)/Ic

def Ejmax(Ic):
    """Josephson energy"""
    return hbar*Ic/(2.0*e)

def Ic_from_Ejmax(Ejmax):
    """inverse Josephson energy"""
    return Ejmax*(2.0*e)/hbar

def Ec(Cq):
    """Charging energy"""
    return e**2/(2.0*Cq)

def Cq_from_Ec(Ec):
    return e**2/(2.0*Ec)

def Ej(Ejmax, flux_over_flux0):
    return Ejmax*absolute(cos(pi*flux_over_flux0))

def EjdivEc(Ej, Ec):
    return Ej/Ec

def fq_approx(Ej, Ec):
    return sqrt(8.0*Ej*Ec)

def fq(Ej, Ec):
    E0 =  -Ej + sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
    E1 =  -Ej + sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
    return (E1-E0)/h

def anharm(EjdivEc, Ec):
    Ej=EjdivEc*Ec
    E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
    E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
    E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
    return (E2-E1)-(E1-E0)

def Ej_from_fq(fq, Ec):
    """h*fq=sqrt(8.0*Ej*Ec) - Ec"""
    return ((h*fq+Ec)**2)/(8.0*Ec)

def flux_over_flux0(voltage, offset, flux_factor):
    return (voltage-offset)*flux_factor

def voltage_from_flux(flux_over_flux0, offset, flux_factor):
    return flux_over_flux0/flux_factor+offset

def flux_parabola(voltage, offset, flux_factor, Ejmax, Ec):
    flx_d_flx0=flux_over_flux0(voltage=voltage, offset=offset, flux_factor=flux_factor)
    qEj=Ej(Ejmax=Ejmax, flux_over_flux0=flx_d_flx0)
    return fq(Ej=qEj, Ec=Ec)

def detuning(fq0, fq):
    return 2.0*pi*(fq0 - fq)

def transmon_energy(Ej, Ec, m):
    return -Ej+sqrt(8.0*Ej*Ec)*(m+0.5) - (Ec/12.0)*(6.0*m**2+6.0*m+3.0)

def transmon_energy_levels(EjdivEc, Ec, n=3):
    Ej=EjdivEc*Ec
    return [transmon_energy(Ej, Ec, m) for m in range(n)]

class Qubit(Agent):
    """Theoretical description of qubit"""
    base_name="qubit"
    #def _default_main_params(self):
    #    return ["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct",
    #            "material", "Dvv", "K2", "vf", "epsinf",
    #            "Rn", "Ic", "Ejmax", "Ej", "Ec", "EjmaxdivEc", "EjdivEc",
    #            "fq", "fq_max", "fq_max_full", "flux_over_flux0", "G_f0", "G_f",
   #             "ng", "Nstates", "EkdivEc"]

    superconductor=Enum("Al")

    def _observe_superconductor(self, change):
        if self.superconductor=="Al":
            self.Delta=Delta_Al

    Tc=Float(Tc_Al).tag(desc="Critical temperature of superconductor", unit="K")

    @tagged_property(label="Gap", tex_str=r"$\Delta(0)$", unit="ueV", desc="Superconducting gap 200 ueV for Al",
                     reference="BCS", expression=r"$1.764 k_B T_c$")
    def Delta(self, Tc):
        return Delta(Tc)

    @Delta.fget.setter
    def _get_Tc(self, Delta):
        return Tc(Delta)

    loop_width=Float(1.0e-6).tag(desc="loop width of SQUID", unit="um", label="loop width")
    loop_height=Float(1.0e-6).tag(desc="loop height of SQUID", unit="um", label="loop height")

    @tagged_property(desc="Area of SQUID loop", unit="um^2", expression="$width \times height$",
                     comment="Loop width times loop height", label="loop area")
    def loop_area(self, loop_width, loop_height):
        return loop_width*loop_height

    Cq=Float(1.0e-13).tag(desc="shunt capacitance", unit="fF", tex_str=r"$C_q$")

    Rn=Float(10.0e3).tag(desc="Normal resistance of SQUID", unit="kOhm", label="DC Junction resistance", tex_str=r"$R_n$")

    @tagged_property(desc="critical current of SQUID", unit="nA", label="Critical current", tex_str=r"$I_C$")
    def Ic(self, Rn, Delta):
        return Ic_from_Rn(Rn, Delta)

    @Ic.fget.setter
    def _get_Rn(self, Ic, Delta):
        return Rn(Ic, Delta)

    @tagged_property(desc="""Max Josephson Energy""", unit="hGHz")#, unit_factor=1.0e9*h)
    def Ejmax(self, Ic):
        return Ejmax(Ic)

    @Ejmax.fget.setter
    def _get_Ic(self, Ejmax):
        return Ic_from_Ejmax(Ejmax)

    @tagged_property(desc="Charging Energy", unit="hGHz")#, unit_factor=1.0e9*h)
    def Ec(self, Cq):
        return Ec(Cq)

    @Ec.fget.setter
    def _get_Cq(self, Ec):
        return Cq_from_Ec(Ec)

    @Ec.fget.setter
    def _get_Ejmax(self, Ec, EjmaxdivEc):
        return EjmaxdivEc*Ec

    @tagged_property(desc="Maximum Ej over Ec")
    def EjmaxdivEc(self, Ejmax, Ec):
        return Ejmax/Ec

    @tagged_property(unit="hGHz")#, unit_factor=1.0e9*h)
    def Ej(self, Ejmax, flux_over_flux0):
        return Ej(Ejmax, flux_over_flux0)

    @tagged_property(desc="Ej over Ec")
    def EjdivEc(self, Ej, Ec):
        return Ej/Ec

    @tagged_property(unit="hGHz", label="fq max")#, unit_factor=1.0e9*h)
    def fq_approx_max(self, Ejmax, Ec):
        return fq_approx(Ejmax, Ec)

    @tagged_property(unit="hGHz", label="fq max full")#, unit_factor=1.0e9*h)
    def fq_max(self, Ejmax, Ec):
        return  fq(Ejmax, Ec)

    @tagged_property(desc="""Operating frequency of qubit""", unit="GHz")
    def fq(self, Ej, Ec):
        return fq(Ej, Ec)

    @tagged_property(desc="absolute anharmonicity", unit="hGHz")
    def anharm(self, EjdivEc, Ec):
        return anharm(EjdivEc, Ec)

    @fq.fget.setter
    def _get_Ej(self, fq, Ec):
        return Ej_from_fq(fq, Ec)

    voltage=Float().tag(unit="V")
    offset=Float(0.09).tag(unit="V", log=False)
    flux_factor=Float(0.195)

    @tagged_property()
    def flux_over_flux0(self, voltage, offset, flux_factor):
        return flux_over_flux0(voltage, offset, flux_factor)

    @flux_over_flux0.fget.setter
    def _get_voltage(self, flux_over_flux0, offset, flux_factor):
        return voltage_from_flux(flux_over_flux0, offset, flux_factor)

    def flux_parabola(self, voltage):
        return flux_parabola(voltage, offset=self.offset, flux_factor=self.flux_factor, Ejmax=self.Ejmax, Ec=self.Ec)

    def detuning(self, fq_off):
        return detuning(self.fq, fq_off)

    n_energy=Int(3)

    @tagged_property()
    def transmon_energy_levels(self, EjdivEc, Ec, n_energy):
        return transmon_energy_levels(EjdivEc, Ec, n_energy)

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

    ng=Float(0.5).tag(desc="charge on gate line")
    Nstates=Int(50).tag(desc="number of states to include in mathieu approximation. More states is better approximation")
    order=Int(3)
    EkdivEc=Array().tag(unit2="Ec")


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


if __name__=="__main__":
    a=Qubit()
    from atom.api import FloatRange
    from taref.core.api import tag_Property
    from taref.plotter.api import LineFitter

    class Fitter(LineFitter):
        Ejmax=FloatRange(0.001, 100.0, 40.0).tag(tracking=True)
        offset=FloatRange(0.0, 100.0, 18.0).tag(tracking=True)

        @tag_Property(private=True)
        def data(self):
            return a.flux_parabola(linspace(-1,1,100), self.offset, a.flux_factor, self.Ejmax*h, a.Ec)

    d=Fitter()
    a.show(d.plotter, d)