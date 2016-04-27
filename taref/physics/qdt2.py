# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:05:32 2016

@author: thomasaref
"""

from taref.physics.qubit import Qubit, transmon_energy_levels
from numpy import pi, linspace, sin, amax, argmin, argmax, cos
from scipy.constants import h

from taref.core.api import log_func, log_callable
from taref.physics.idt import IDT
from taref.core.extra_setup import tagged_property
from atom.api import Float, Int
from taref.core.universal import Array
from taref.physics.fundamentals import sqrt, pi, e, h, array, eig, delete, sin, sinc_sq, sinc, linspace, zeros, absolute, cos, arange

def coupling_approx(Np, K2, f0):
    """approximate coupling at center frequency of QDT, in Hz (double finger)"""
    return 0.55*Np*K2*f0

Ga0_mult={"single":2.871, "double":3.111}
def Ga0(mult, f0, epsinf, W, Dvv, Np):
    """Ga0 from morgan"""
    return mult*2*pi*f0*epsinf*W*Dvv*(Np**2)

coupling_mult={"single" : 0.71775, "double" : 0.54995}
def Ga0div2C(mult, f0, K2, Np):
    """coupling at center frequency, in Hz (2 pi removed)"""
    return mult*f0*K2*Np

def X(Np, f, f0):
    """standard frequency dependence"""
    return Np*pi*(f-f0)/f0

def Ga(f, mult, f0, K2, Np, C):
    return coupling(f, mult, f0, K2, Np)*2*C*2*pi

def Ba(f, mult, f0, K2, Np, C):
    return -Lamb_shift(f, mult, f0, K2, Np)*2*C*2*pi

def coupling(f, mult, f0, K2, Np):
    gamma0=Ga0div2C(mult, f0, K2, Np)
    gX=X(Np, f, f0)
    return gamma0*(sin(gX)/gX)**2.0

def Lamb_shift(f, mult, f0, K2, Np):
    """returns Lamb shift"""
    gamma0=Ga0div2C(mult, f0, K2, Np)
    gX=X(Np, f, f0)
    return -gamma0*(sin(2.0*gX)-2.0*gX)/(2.0*gX**2.0)

Ct_mult={"double" : sqrt(2), "single" : 1.0}
#def calc_Lamb_shift(fq, ft, Np, f0, epsinf, W, Dvv):
#    """returns Lamb shift in Hz"""
#    X=Np*pi*(fq-f0)/f0
#    Ga0=Ga0_mult[ft]*2*pi*f0*epsinf*W*Dvv*(Np**2)
#    C=Ct_mult[ft]*Np*W*epsinf
#    Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#    return -Ba/(2.0*C)/(2.0*pi)
#
#def calc_freq_shift(fq, ft, Np, f0, epsinf, W, Dvv):
#    """returns Lamb shift in Hz"""
#    X=Np*pi*(fq-f0)/f0
#    Ga0=Ga0_mult[ft]*2*pi*f0*epsinf*W*Dvv*(Np**2)
#    C=Ct_mult[ft]*Np*W*epsinf
#    Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#    return Ba/C/(2.0*pi)
#
#def calc_coupling(fq, ft, Np, f0, Dvv, epsinf, W):
#    X=Np*pi*(fq-f0)/f0
#    Ga0=Ga0_mult[ft]*2*pi*f0*epsinf*W*Dvv*(Np**2)
#    C=Ct_mult[ft]*Np*W*epsinf
#    Ga=Ga0*(sin(X)/X)**2.0
#    return Ga/(2.0*C)/(2.0*pi)

def lamb_shifted_transmon_energy(Ej, Ec, m, mult, f0, K2, Np):
    Em=-Ej+sqrt(8.0*Ej*Ec)*(m+0.5) - (Ec/12.0)*(6.0*m**2+6.0*m+3.0)
    if m==0:
        return Em
    Emm1=-Ej+sqrt(8.0*Ej*Ec)*(m-1+0.5) - (Ec/12.0)*(6.0*(m-1)**2+6.0*(m-1)+3.0)
    fq=(Em-Emm1)/h
    fls=Lamb_shift(fq, mult, f0, K2, Np)
    return Em+h*fls

def lamb_shifted_transmon_energy_levels(EjdivEc, n, mult, f0, K2, Np, C):
    Ec=e**2/(2.0*C)
    Ej=EjdivEc*Ec
    return [lamb_shifted_transmon_energy(Ej, Ec, m, mult, f0, K2, Np) for m in range(n)]

#def lamb_shifted_anharm(EjdivEc, mult, f0, K2, Np, C):
#    E0, E1, E2=lamb_shifted_transmon_energy_levels(EjdivEc, 3, mult, f0, K2, Np, C)
#    return (E2-E1)-(E1-E0)
#
#def lamb_shifted_fq(EjdivEc, mult, Np, f0, epsinf, W, Dvv):
#    E0, E1=lamb_shifted_transmon_energy_levels(EjdivEc, 2, ft, Np, f0, epsinf, W, Dvv)
#    return (E1-E0)/h
#
#def lamb_shifted_fq2(EjdivEc, ft, Np, f0, epsinf, W, Dvv):
#    E0, E1, E2=lamb_shifted_transmon_energy_levels(EjdivEc, 3, ft, Np, f0, epsinf, W, Dvv)
#    return (E2-E0)/h

class QDT(IDT, Qubit):
    base_name="QDT"
    couple_mult=Float(0.55)

    def _observe_ft(self, change):
        if change["type"]=="update":
            self.couple_mult=coupling_mult[self.ft]

    @tagged_property()
    def Ga0(self, ft, f0, epsinf, W, Dvv, Np):
        """Ga0 from morgan"""
        return Ga0(Ga0_mult[ft], f0, epsinf, W, Dvv, Np)

    @tagged_property(desc="""Coupling at IDT center frequency""", unit="GHz",
                     label="Coupling at center frequency", tex_str=r"$\gamma_{f0}$")
    def coupling_approx(self, Np, K2, f0):
        return coupling_approx(Np, K2, f0)

    @tagged_property()
    def max_coupling(self, couple_mult, f0, K2, Np):
        return Ga0div2C(couple_mult, f0, K2, Np)

    @tagged_property(desc="""Coupling adjusted by sinc sq""", unit="GHz", tex_str=r"$G_f$", label="frequency adjusted coupling")
    def coupling(self, f, couple_mult, f0, K2, Np):
        return coupling(f, couple_mult, f0, K2, Np)

    @tagged_property(desc="""Lamb shift""", unit="GHz", tex_str=r"$G_f$", label="frequency adjusted lamb_shift")
    def Lamb_shift(self, f, couple_mult, f0, K2, Np):
        return Lamb_shift(f, couple_mult, f0, K2, Np)

    #@log_callable(sub=True)
    #def calc_Lamb_shift(self, fqq, ft, Np, f0, epsinf, W, Dvv):
    #    return calc_Lamb_shift(fqq, ft, Np, f0, epsinf, W, Dvv)#ft=self.ft, Np=self.Np, f0=self.f0, epsinf=self.epsinf, W=self.W, Dvv=self.Dvv)

    #@log_callable(sub=True)
    #def calc_coupling(self, fqq, ft, Np, f0, Dvv, epsinf, W):
    #    return calc_coupling(fqq, ft, Np, f0, Dvv, epsinf, W) #ft=self.ft, Np=self.Np, f0=self.f0, Dvv=self.Dvv, epsinf=self.epsinf, W=self.W)

    @log_callable(sub=True)
    def lamb_shifted_transmon_energy_levels(self, EjdivEc, n_energy, couple_mult, f0, K2, Np, Cq):
        return lamb_shifted_transmon_energy_levels(EjdivEc, n_energy, couple_mult, f0, K2, Np, Cq)#ft=self.ft, Np=self.Np, f0=self.f0, epsinf=self.epsinf,
                                                   #W=self.W, Dvv=self.Dvv)

    #@log_callable(sub=True)
    #def lamb_shifted_anharm(self, EjdivEc, ft, Np, f0, epsinf, W, Dvv):
    #    return lamb_shifted_anharm(EjdivEc, ft, Np, f0, epsinf, W, Dvv)

    #@log_callable(sub=True)
    #def lamb_shifted_fq(self, EjdivEc, ft, Np, f0, epsinf, W, Dvv):
    #    return lamb_shifted_fq(EjdivEc, ft, Np, f0, epsinf, W, Dvv)

    #@log_callable(sub=True)
    #def lamb_shifted_fq2(self, EjdivEc, ft, Np, f0, epsinf, W, Dvv):
    #    return lamb_shifted_fq2(EjdivEc, ft, Np, f0, epsinf, W, Dvv)

    @tagged_property(desc="shunt capacitance of QDT", unit="fF")
    def Cq(self, Ct):
        return Ct

    @Cq.fget.setter
    def _get_Ct(self, Cq):
        return Cq



if __name__=="__main__":
    qdt=QDT(material='LiNbYZ',
        ft="double",
        a=80.0e-9,
        Np=9,
        Rn=3780.0, #(3570.0+4000.0)/2.0,
        W=25.0e-6,
        eta=0.5,
        flux_factor=0.2945,
        voltage=1.21,
        offset=0.0)
    EjdivEc=linspace(0.1, 300, 3000)
    yoko=linspace(-5,5,3000)
    #print a.calc_coupling(fqq=4.5e9), a.call_func("coupling", Ga=1.0)
    from taref.plotter.api import line, Plotter
    from taref.core.api import set_tag

    def energy_level_plot():
        pl=Plotter(fig_width=9.0, fig_height=6.0)

        set_tag(qdt, "EjdivEc", log=False)
        E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
        Ej=EjdivEc*qdt.Ec
        pl, pf=line(EjdivEc, (E0+Ej)/h/1e9, linestyle="dashed", linewidth=1.0, plotter=pl)
        line(EjdivEc, (E1+Ej)/h/1e9, plotter=pl, linestyle="dashed", linewidth=1.0)
        line(EjdivEc, (E2+Ej)/h/1e9, plotter=pl, linestyle="dashed", linewidth=1.0)
        E0p, E1p, E2p=qdt.call_func("lamb_shifted_transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
        line(EjdivEc, (E0p+Ej)/h/1e9, plotter=pl, color="red", linewidth=1.0)
        line(EjdivEc, (E1p+Ej)/h/1e9, plotter=pl, color="green", linewidth=1.0)
        line(EjdivEc, (E2p+Ej)/h/1e9, plotter=pl, color="purple", linewidth=1.0)
        pl.xlabel="$E_j/E_c$"
        pl.ylabel="Frequency (GHz)"
        return pl

    def anharm_plot():
        """reproduces anharm plot in Anton's paper"""
        set_tag(qdt, "EjdivEc", log=False)
        set_tag(qdt, "Ej", log=False)

        #qdt.epsinf=qdt.epsinf/3.72
        qdt.Np=10
        qdt.Ec=qdt.fq*0.1*h

        print qdt.max_coupling, qdt.coupling_approx
        E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
        anharm=(E2-E1)-(E1-E0)

        E0p, E1p, E2p=qdt.call_func("lamb_shifted_transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)

        anharmp=(E2p-E1p)-(E1p-E0p)

        fq= (E1-E0)/h#qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
        ls_fq=(E1p-E0p)/h #qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        fq2=(E2-E1)/h
        ls_fq2=(E2p-E1p)/h #qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)

        pl, pf=line(fq/qdt.f0, (anharmp/h-anharm/h)/(2.0*qdt.max_coupling), linewidth=0.5, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$")
        line(fq/qdt.f0, (ls_fq-fq)/(2.0*qdt.max_coupling), plotter=pl, color="blue", linewidth=0.5, label=r"$\Delta_{1,0}$")
        line(fq/qdt.f0, (ls_fq2-fq2)/(2.0*qdt.max_coupling), plotter=pl, color="red", linewidth=0.5, label=r"$\Delta_{2,1}$")
        pl.set_ylim(-1.0, 0.6)
        pl.set_xlim(0.7, 1.3)
        pl.xlabel=r"$f_{10}/f_{IDT}$"
        pl.ylabel=r"$\Delta/\Gamma_{10}^{MAX}$"
        pl.legend(loc='lower left')
        #fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        #line(EjdivEc, fq, plotter=pl, color="green", linewidth=0.5)

        #line(EjdivEc, E1p, plotter=pl, color="green", linewidth=0.5)
        #line(EjdivEc, E2p, plotter=pl, color="purple", linewidth=0.5)
        return pl

    def anharm_plot2():
        """reproduces anharm plot in Anton's paper"""
        set_tag(qdt, "EjdivEc", log=False)
        set_tag(qdt, "Ej", log=False)
        pl=Plotter(fig_width=9.0, fig_height=6.0)
        #qdt.epsinf=qdt.epsinf/3.72
        #qdt.Np=10
        #qdt.Ec=qdt.fq*0.1*h
        print qdt.max_coupling, qdt.coupling_approx
        #flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=yoko)
        #Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0)
        #EjdivEc=Ej/qdt.Ec
        anharm=qdt.call_func("anharm", EjdivEc=EjdivEc)
        anharmp=qdt.call_func("lamb_shifted_anharm", EjdivEc=EjdivEc)
        fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
        ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
        #pl, pf=line(fq, anharm/h, linewidth=0.5, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$")

        pl, pf=line(EjdivEc, anharmp/h/1e9, linewidth=1.0, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$", plotter=pl)
        line(EjdivEc, anharm/h/1e9, linewidth=1.0, color="purple", label=r"anharm", plotter=pl)

        line(EjdivEc, (ls_fq-fq)/1e9, plotter=pl, color="blue", linewidth=1.0, label=r"$\Delta_{1,0}$")
        E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
        fq2=(E2-E1)/h
        line(EjdivEc, (ls_fq2-fq2)/1e9, plotter=pl, color="red", linewidth=1.0, label=r"$\Delta_{2,1}$")
        pl.set_ylim(-2, 1.5)
        #pl.set_xlim(0.0, 70)
        pl.xlabel=r"$E_j/E_c$"
        pl.ylabel=r"$\Delta (GHz)$"
        #pl.legend(loc='lower right')
        #fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        #line(EjdivEc, fq, plotter=pl, color="green", linewidth=0.5)

        #line(EjdivEc, E1p, plotter=pl, color="green", linewidth=0.5)
        #line(EjdivEc, E2p, plotter=pl, color="purple", linewidth=0.5)
        return pl
    pl=energy_level_plot()
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #       fig_name="energy_levels.pdf")
    anharm_plot()
    #pl=anharm_plot2()
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #       fig_name="anharm1.pdf")
    pl.show()

    #a.show()

#Np=qdt.Np
#f0=5.45e9
#w0=2*pi*f0
##qdt.Dvv=0.001
#vf=3488.0
#freq=linspace(1e9, 10e9, 1000)
#print qdt.flux_factor, qdt.offset, qdt.Ejmax/h, qdt.Ec/h
#def flux_to_Ej(voltage,  offset=qdt.offset, flux_factor=qdt.flux_factor, Ejmax=qdt.Ejmax):
#    flux_over_flux0=(voltage-offset)*flux_factor
#    Ej=Ejmax*absolute(cos(pi*flux_over_flux0))
#    return Ej
#
#
#
#def energy_levels(EjdivEc, Ec=qdt.Ec, Dvv=qdt.Dvv):
#    print Ec/h
#    Ec=Ec
#    Ej=EjdivEc*Ec
#    w0n=sqrt(8.0*Ej*Ec)/h*(2.0*pi)
#    #epsinf=qdt.epsinf
#    #W=qdt.W
#    #Dvv=qdt.Dvv
#    E0p =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0#-Ba/(2.0*C)*0.5 #(n +1/2)
#
#    E1p =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)# -Ba/(2.0*C)*1.5
#
#    E2p =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)#-Ba/(2.0*C)*2.5
#    E3p =  sqrt(8.0*Ej*Ec)*3.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)#-Ba/(2.0*C)*3.5
#
#    E0p=E0p/h
#    E1p=E1p/h
#    E2p=E2p/h
#    E3p=E3p/h
#    #fq=sqrt(8.0*Ej*Ec)
#    #wq=2.0*pi*fq#print wq
#
#    #X=Np*pi*(wq-w0)/w0
#    #Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#    #C=sqrt(2.0)*Np*W*epsinf
#    #Ga=Ga0*(sin(X)/X)**2.0
#    #Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#
#    #E10=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-Ec/(1.0+Ba/(wq*C))
#    #E21=sqrt(8.0*Ej*Ec/(1.0+Ba/(wq*C)))-2.0*Ec/(1.0+Ba/(wq*C))
#    #return E10/h, (E21+E10)/h/2.0
#    #E_{tot}=-E_J+\sqrt{8E_J E_C}(n +1/2)-(B_a/2C)(n +1/2)-\dfrac{E_C}{12}(6n^2+6n+3)
#    E0 =  E0p#+calc_Lamb_shift(E0p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0-Ba/(2.0*C)*0.5 #(n +1/2)
#
#    E1 =  E1p+calc_Lamb_shift(E1p-E0p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0) -Ba/(2.0*C)*1.5
#
#    E2 =  E2p+calc_Lamb_shift(E2p-E1p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)-Ba/(2.0*C)*2.5
#    E3 =  E3p+calc_Lamb_shift(E3p-E2p, Dvv=Dvv) #sqrt(8.0*Ej*Ec)*3.5 - (Ec/12.0)*(6.0*3**2+6.0*3+3.0)-Ba/(2.0*C)*3.5
#    return E0, E1, E2, E3, E0p, E1p, E2p, E3p, w0n
#    return (E1-E0)/h, (E2-E1)/h#/3.0
#    #return qdt._get_fq(Ej, qdt.Ec)
#
#EjdivEc=linspace(0.001, 300, 3000).astype(float64)
#Ejmax=qdt.Ejmax
#E0,E1,E2,E3, E0p, E1p, E2p, E3p, w0n=energy_levels(EjdivEc, Ec=qdt.Ec, Dvv=qdt.Dvv)
#
#b.line_plot("E0", EjdivEc, E0, label="E0")
#b.line_plot("E1", EjdivEc, E1, label="E1")
#b.line_plot("E2", EjdivEc, E2, label="E2")
#b.line_plot("E3", EjdivEc, E3, label="E3")
#
#DEP=E1p-E0p
#d=Plotter(fig_height=5.0, fig_width=7.0)
##Plotter(name="anharm")
#d.line_plot("E0", E1p-E0p, (E2-E1)-(E1-E0)-((E2p-E1p)-(E1p-E0p)), label="E0")
#d.line_plot("E1", E1p-E0p, E1-E0-(E1p-E0p), label="E1")
#d.line_plot("E2", E1p-E0p, E2-E1-(E2p-E1p), label="E2")
##d.line_plot("E3", EjdivEc, E3, label="E3")
##E0,E1,E2,E3=energy_levels(EjdivEc, Dvv=0.0)
#
#b.line_plot("E0p", EjdivEc, E0p, label="E0p")
#b.line_plot("E1p", EjdivEc, E1p, label="E1p")
#b.line_plot("E2p", EjdivEc, E2p, label="E2p")
#b.line_plot("E3p", EjdivEc, E3p, label="E3p")
#
##d.line_plot("E0p", EjdivEc, (E2p-E1p)-(E1p-E0p), label="E0p")
##d.line_plot("E1p", E1p-E0p, (E2p-E1p)-DEP, label="E1p")
##d.line_plot("E2p", E1p-E0p, E3p-E2p, label="E2p")
##b.show()
#yo = linspace(-2.0, 2.0, 2000)
#Ej=flux_to_Ej(yo, Ejmax=Ejmax)
#EjdivEc=Ej/qdt.Ec
#E0,E1,E2,E3, E0p, E1p, E2p, E3p, w0n=energy_levels(EjdivEc, Dvv=qdt.Dvv)
#Gamma10=calc_Coupling(E1-E0)
#Gamma20=calc_Coupling((E2-E0)/2.0)
##d.scatter_plot("blah", E1-E0, Gamma10, label="E_{10}")
##d.scatter_plot("lbs", (E2-E0)/2.0, Gamma20, label="E_{20}/2")
#fw0=linspace(4e9, 7e9, 2000) #E1-E0 #sqrt(8*Ej*qdt.Ec)/h
#d.line_plot("asdf", fw0/1e9, calc_Coupling(fw0)/1e9, label=r"$G_a/2C$", color="blue")
#d.line_plot("asdfd", fw0/1e9, calc_Lamb_shift(fw0)/1e9, label=r"$-B_a/2C$", color="red")
#d.legend()
#
#d.mpl_axes.xlabel="Frequency (GHz)"
#d.mpl_axes.ylabel="Frequency (GHz)"
#d.set_ylim(-1.0, 1.5)
##dd.set_xlim(4.2, 5.0)
##d.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_Ba.pdf")
##d.show()
#
#
#dd=Plotter(fig_height=7.0, fig_width=7.0)
#def listen_coupling(f_listen, Dvv=qdt.Dvv):
#    epsinf=qdt.epsinf
#    W=qdt.W
#    w=2.0*pi*f_listen
#    Np=36
#    f0=idt.f0
#    print f0 #4.5e9
#    w0=2*pi*f0
#    X=Np*pi*(w-w0)/w0
#    Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#    C=sqrt(2.0)*Np*W*epsinf
#    Ga=Ga0*(sin(X)/X)**2.0
#    #Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#    return Ga/(2.0*C)/(2.0*pi)
#
#dd.line_plot("asdf", fw0/1e9, calc_Coupling(fw0)/1e9, label=r"$G_a/2C$", color="blue")
#dd.line_plot("asdfd", fw0/1e9, calc_Lamb_shift(fw0)/1e9, label=r"$-B_a/2C$", color="red")
#dd.line_plot("listen", fw0/1e9, listen_coupling(fw0)/4/1e9, label=r"$G_a^{IDT}/2C^{IDT}/4$", color="green")
#dd.plot_dict["listen"].mpl.linestyle="dashed"
#dd.legend()
##dd.set_ylim(-1.0, 1.5)
##dd.set_xlim(min(self.yoko), max(self.yoko))
#dd.mpl_axes.xlabel="Frequency (GHz)"
#dd.mpl_axes.ylabel="Frequency (GHz)"
##dd.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_all.pdf")#, format="eps")
#dd.set_ylim(-0.01, 0.1)
#dd.set_xlim(4.2, 5.0)
##dd.savefig("/Users/thomasaref/Dropbox/Current stuff/Linneaus180416/", "Ga_all_zoom.pdf")#, format="eps")
#
##dd.show()
##plotter.mpl_axes.title="MagdB fluxmap {}".format(self.name)
##Plotter().line_plot("asdf", yo, fw0+calc_Lamb_shift(fw0))
#
#def R_lor(f_listen, fqq, w0n1, Dvv=qdt.Dvv):
#    w=2*pi*f_listen
#    epsinf=qdt.epsinf
#    W=qdt.W
#    X=Np*pi*(f_listen-f0)/f0
#    Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#    C=sqrt(2.0)*Np*W*epsinf
#    Ga=Ga0*(sin(X)/X)**2.0
#    Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#    w0nn=2*pi*fqq#w0n1#-Ba/(2.0*C)
#    Gamma=calc_Coupling(fqq, Dvv=Dvv)
#    L=1/(C*(w0nn**2.0))
#    return  Ga/(Ga+1.0j*Ba+1.0j*w*C+1.0/(1.0j*w*L))
#    #return -2Gamma10*(gamma10-idw)/(4*(gamma10*2+dw**2)) #+Gamma10*Gamma21*(gamma20+idw)*0
#    #return 1-2*Gamma10/(2*(gamma10-1.0j*dw)+(OmegaC**2)/(2*gamma20-2j*(dw+dwc)))
#    return -Gamma/(Gamma+1.0j*(w-w0nn))
##        def R_full(f_listen=4.3e9, fq=5.0e9, fq2=6.0e9):
##
##
##            w_listen=2*pi*f_listen
##            epsinf=qdt.epsinf
##            W=qdt.W
##            Dvv=qdt.Dvv
##            w0=2*pi*f0
##
##
##            X=Np*pi*(f_listen-f0)/f0
##            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
##            C=sqrt(2.0)*Np*W*epsinf
##            Ga=Ga0*(sin(X)/X)**2.0
##            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
##
##            wq=2.0*pi*fq
##            wq2=2.0*pi*fq2
##
##            L=1/(C*(wq**2.0))
##            L2=1/(C*(wq2**2.0))
##
##            Gamma=Ga/(2.0*C)
##            #return 1.0/(1.0 +1.0j*(w_listen-wq)/Gamma), 1.0/(1.0 +1.0j*(w_listen-wq2)/Gamma)
##            return Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L)), Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L2))
#
#
#temp=[]
#t2=[]
#qfreq=[]
#for f in freq:
#    Gamma=calc_Coupling(E1-E0)
#    w0nn=2*pi*(E1p-E0p)
#    w=2*pi*f
#    #R1=-Gamma/(Gamma+1.0j*(w-w0nn))
#    R1=R_lor(f, E1p-E0p, w0n)
#    #Gamma=calc_Coupling((E2p-E0p)/2.0)
#    #w0nn=2*pi*(E2p-E0p)/2.0
#    #R2=-Gamma/(Gamma+1.0j*(w-w0nn))
#    anharm=(E2-E1)-(E1-E0)
#    R2=R_lor(f, E1p-E0p+anharm/2.0, w0n)
#    #R1, R2=R_full(f, E1-E0, (E2-E0)/2.0)
#    #qfreq.append(freq[argmax(R)])
#    #imax=argmax(R)
#    #print imax
#    #f1=fq[argmin(absolute(fq-f))]
#    #f2=freq[argmin(absolute(R[imax:-1]-0.5))]
#    t2.append(R2)
#    temp.append(R1)
#temp=array(temp)
##b.line_plot("coup", freq, t2)
#c=Plotter()
#g=Plotter()
#c.colormesh("R_full", yo, freq, 10*log10(absolute(temp)+absolute(t2)))
#g.colormesh("R_full", yo, freq, absolute(temp))
#h=Plotter()
#h.colormesh("R_full", yo, freq, absolute(t2))
#
#
##g.colormesh('R_angle', yo, freq, angle(temp))        #b.line_plot("Ba", freq, t2)
##b.line_plot("Ga", freq, temp)
#b.show()