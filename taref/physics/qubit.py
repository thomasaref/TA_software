# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:45:44 2016

@author: thomasaref

Collection of functions relating to qubits, particularly transmons
"""

from scipy.constants import e, h, hbar, k as kB, epsilon_0 as eps0, pi
c_eta = 0.8

from numpy import (sin, cos, arccos, sqrt, exp, empty, mean, exp, log10, arange, array, ndarray, delete,
                   absolute, dtype, angle, amin, amax, linspace, zeros, shape, append)


from taref.core.api import Agent, Array, SProperty, private_property
from atom.api import Enum, Float, Int
from taref.plotter.api import Plotter, line
from enaml import imports
with imports():
    from taref.physics.qubit_e import QubitView


Tc_Al=1.315 #critical temperature of aluminum
Delta_Al=200.0e-6*e #gap of aluminum

class Qubit(Agent):
    """Theoretical description of qubit"""
    base_name="qubit"
    #def _default_main_params(self):
    #    return ["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct",
    #            "material", "Dvv", "K2", "vf", "epsinf",
    #            "Rn", "Ic", "Ejmax", "Ej", "Ec", "EjmaxdivEc", "EjdivEc",
    #            "fq", "fq_max", "fq_max_full", "flux_over_flux0", "G_f0", "G_f",
   #             "ng", "Nstates", "EkdivEc"]

    dephasing=Float(0.0).tag(unit="GHz")

    @private_property
    def view_window(self):
        return QubitView(agent=self)

    superconductor=Enum("Al")

    def _observe_superconductor(self, change):
        if self.superconductor=="Al":
            self.Delta=Delta_Al

    Tc=Float(Tc_Al).tag(desc="Critical temperature of superconductor", unit="K")

    Delta=SProperty().tag(label="Gap", tex_str=r"$\Delta(0)$", unit="ueV", desc="Superconducting gap 200 ueV for Al",
                     reference="BCS", expression=r"$1.764 k_B T_c$")
    @Delta.getter
    def _get_Delta(self, Tc):
        """BCS theory superconducting gap"""
        return 1.764*kB*Tc

    @Delta.setter
    def _get_Tc(self, Delta):
        return Delta/(1.764*kB)

    loop_width=Float(1.0e-6).tag(desc="loop width of SQUID", unit="um", label="loop width")
    loop_height=Float(1.0e-6).tag(desc="loop height of SQUID", unit="um", label="loop height")

    loop_area=SProperty().tag(desc="Area of SQUID loop", unit="um^2", expression="$width \times height$",
                     comment="Loop width times loop height", label="loop area")
    @loop_area.getter
    def _get_loop_area(self, loop_width, loop_height):
        return loop_width*loop_height

    Ct=Float(1.0e-13).tag(desc="shunt capacitance", unit="fF", tex_str=r"$C_q$")

    Rn=Float(10.0e3).tag(desc="Normal resistance of SQUID", unit="kOhm", label="DC Junction resistance", tex_str=r"$R_n$")

    Ic=SProperty().tag(desc="critical current of SQUID", unit="nA", label="Critical current", tex_str=r"$I_C$")
    @Ic.getter
    def _get_Ic(self, Rn, Delta):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Rn

    @Ic.setter
    def _get_Rn(self, Ic, Delta):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Ic


    Ejmax=SProperty().tag(desc="""Max Josephson Energy""", unit="hGHz")#, unit_factor=1.0e9*h)
    @Ejmax.getter
    def _get_Ejmax(self, Ic):
        """Josephson energy"""
        return hbar*Ic/(2.0*e)

    @Ejmax.setter
    def _get_Ic_get_Ejmax(self, Ejmax):
        """inverse Josephson energy"""
        return Ejmax*(2.0*e)/hbar

    Ec=SProperty().tag(desc="Charging Energy", unit="hGHz")#, unit_factor=1.0e9*h)
    @Ec.getter
    def _get_Ec(self, Ct):
        """Charging energy"""
        return e**2/(2.0*Ct)

    @Ec.setter
    def _get_Ct(self, Ec):
        """inverse charging energy"""
        return e**2/(2.0*Ec)

    @Ec.setter
    def _get_Ejmax_get_Ec(self, Ec, EjmaxdivEc):
        return EjmaxdivEc*Ec

    EjmaxdivEc=SProperty().tag(desc="Maximum Ej over Ec")
    @EjmaxdivEc.getter
    def _get_EjmaxdivEc(self, Ejmax, Ec):
        return Ejmax/Ec

    Ej=SProperty().tag(unit="hGHz")
    @Ej.getter
    def _get_Ej(self, Ejmax, flux_over_flux0):
        return Ejmax*absolute(cos(flux_over_flux0)) #*pi

    @Ej.setter
    def _get_flux_over_flux0_get_Ej(self, Ej, Ejmax):
        return arccos(Ej/Ejmax)#/pi

    EjdivEc=SProperty().tag(desc="Ej over Ec")
    @EjdivEc.getter
    def _get_EjdivEc(self, Ej, Ec):
        return Ej/Ec

    fq_approx_max=SProperty().tag(unit="GHz", label="fq approx max")
    @fq_approx_max.getter
    def _get_fq_approx_max(self, Ejmax, Ec):
        return self._get_fq_approx(Ej=Ejmax, Ec=Ec)

    fq_approx=SProperty().tag(unit="GHz")
    @fq_approx.getter
    def _get_fq_approx(self, Ej, Ec):
        return (sqrt(8.0*Ej*Ec)-Ec)/h

    fq_max=SProperty().tag(unit="hGHz", label="fq max")
    @fq_approx.getter
    def _get_fq_max(self, Ejmax, Ec):
        return  self._get_fq(Ej=Ejmax, Ec=Ec)

    fq=SProperty().tag(desc="""Operating frequency of qubit""", unit="GHz")
    @fq.getter
    def _get_fq(self, Ej, Ec):
        E0, E1=self._get_transmon_energy_levels(Ej=Ej, Ec=Ec, n_energy=2)
        return (E1-E0)/h

    @fq.setter
    def _get_Ej_get_fq(self, fq, Ec):
        """h*fq=sqrt(8.0*Ej*Ec) - Ec"""
        return ((h*fq+Ec)**2)/(8.0*Ec)

    L=SProperty()
    @L.getter
    def _get_L(self, fq, Ct):
        return 1.0/(Ct*(2*pi*fq)**2)

    anharm=SProperty().tag(desc="absolute anharmonicity", unit="GHz")
    @anharm.getter
    def _get_anharm(self, Ej, Ec):
        E0, E1, E2=self._get_transmon_energy_levels(Ej=Ej, Ec=Ec, n_energy=3)
        return (E2-E1)/h-(E1-E0)/h

    fq2=SProperty().tag(desc="""20 over 2 freq""", unit="GHz")
    @fq2.getter
    def _get_fq2(self, Ej, Ec):
        E0, E1, E2=self._get_transmon_energy_levels(Ej=Ej, Ec=Ec, n_energy=3)
        return (E2-E0)/h/2.0

    voltage=Float().tag(unit="V")
    offset=Float(0.09).tag(unit="V")
    flux_factor=Float(0.195)

    flux_over_flux0=SProperty()
    @flux_over_flux0.getter
    def _get_flux_over_flux0(self, voltage, offset, flux_factor):
        return (voltage-offset)*flux_factor

    @flux_over_flux0.setter
    def _get_voltage(self, flux_over_flux0, offset, flux_factor):
        return flux_over_flux0/flux_factor+offset

    flux_parabola=SProperty()
    @flux_parabola.getter
    def _get_flux_parabola(self, voltage, offset, flux_factor, Ejmax, Ec):
        flx_d_flx0=self._get_flux_over_flux0(voltage=voltage, offset=offset, flux_factor=flux_factor)
        qEj=self._get_Ej(Ejmax=Ejmax, flux_over_flux0=flx_d_flx0)
        return self._get_fq(Ej=qEj, Ec=Ec)#, fq2(qEj, Ec)

    #freq_arr=Array().tag(desc="array of frequencies to evaluate over")
    f=Float(4.4e9).tag(desc="Operating frequency, e.g. what frequency is being stimulated/measured", unit="GHz")

    flux_from_fq=SProperty().tag(sub=True)
    @flux_from_fq.getter
    def _get_flux_from_fq(self, fq, Ct, Ejmax):
        Ec=self._get_Ec(Ct=Ct)
        Ej=self._get_Ej_get_fq(fq=fq, Ec=Ec)
        return self._get_flux_over_flux0_get_Ej(Ej=Ej, Ejmax=Ejmax)

    voltage_from_flux_par=SProperty().tag(sub=True)
    @voltage_from_flux_par.getter
    def _get_voltage_from_flux_par(self, fq, Ct, Ejmax, offset, flux_factor):
        #Ec=self._get_Ec(Ct=Ct)
        #Ej=self._get_Ej_get_fq(fq=fq, Ec=Ec)
        flux_d_flux0=self._get_flux_from_fq(fq, Ct, Ejmax) #self._get_flux_over_flux0_get_Ej(Ej=Ej, Ejmax=Ejmax)
        return self._get_voltage(flux_over_flux0=flux_d_flux0, offset=offset, flux_factor=flux_factor)

    voltage_from_flux_par_many=SProperty().tag(sub=True)
    @voltage_from_flux_par_many.getter
    def _get_voltage_from_flux_par_many(self, fq, Ct, Ejmax, offset, flux_factor):
        #Ec=self._get_Ec(Ct=Ct)
        #Ej=self._get_Ej_get_fq(fq=f, Ec=Ec)
        fdf0=self._get_flux_from_fq(fq, Ct, Ejmax) #self._get_flux_over_flux0_get_Ej(Ej=Ej, Ejmax=Ejmax)

        #fdf0=self._get_flux_over_flux0_get_Ej(Ej=Ej, Ejmax=Ejmax)
        flux_d_flux0=append(fdf0, -fdf0)
        flux_d_flux0=append(flux_d_flux0, -fdf0+pi)
        flux_d_flux0=append(flux_d_flux0, fdf0-pi)
        freq=append(fq, fq)
        freq=append(freq, freq)
        return freq/1e9, self._get_voltage(flux_over_flux0=flux_d_flux0, offset=offset, flux_factor=flux_factor)

    def detuning(self, fq_off):
        return 2.0*pi*(self.fq - fq_off)

    def transmon_energy(self, Ej, Ec, m):
        return -Ej+sqrt(8.0*Ej*Ec)*(m+0.5) - (Ec/12.0)*(6.0*m**2+6.0*m+3.0)

    transmon_energy_levels=SProperty().tag(sub=True)
    @transmon_energy_levels.getter
    def _get_transmon_energy_levels(self, Ej, Ec, n_energy):
        #Ej=EjdivEc*Ec
        return [self.transmon_energy(Ej, Ec, m) for m in range(n_energy)]

    n_energy=Int(3)

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
    EkdivEc=Array().tag(unit2="Ec", sub=True)


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


def energy_level_plot(qbt):
    """confirmation plot of transmon energy levels"""
    pl=Plotter(fig_width=9.0, fig_height=6.0)
    EjdivEc=linspace(0.1, 300, 3000)
    Ej=EjdivEc*qbt.Ec
    E0, E1, E2=qbt._get_transmon_energy_levels(Ej=Ej, n_energy=3)
    line(EjdivEc, (E0+Ej)/h/1e9, plotter=pl, linestyle="dashed", linewidth=1.0, color="blue")
    line(EjdivEc, (E1+Ej)/h/1e9, plotter=pl, linestyle="dashed", linewidth=1.0, color="red")
    line(EjdivEc, (E2+Ej)/h/1e9, plotter=pl, linestyle="dashed", linewidth=1.0, color="green")

    Ec=qbt.Ec
    E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
    E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
    E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)

    line(EjdivEc, E0/h/1e9, plotter=pl, linewidth=0.5, color="blue")
    line(EjdivEc, E1/h/1e9, plotter=pl, linewidth=0.5, color="red")
    line(EjdivEc, E2/h/1e9, plotter=pl, linewidth=0.5, color="green")

    pl.xlabel="$E_j/E_c$"
    pl.ylabel="Frequency (GHz)"
    return pl

def anharm_plot(qbt):
    pl=Plotter(fig_width=9.0, fig_height=6.0)
    EjdivEc=linspace(0.1, 300, 3000)
    Ej=EjdivEc*qbt.Ec
    fq=qbt._get_fq(Ej=Ej)
    fq2=qbt._get_fq2(Ej=Ej)
    anh=qbt._get_anharm(Ej=Ej)

    line(EjdivEc, fq/1e9, plotter=pl, linestyle="dashed", linewidth=1.0, color="blue")
    line(EjdivEc, fq2/1e9, plotter=pl, linestyle="dashed", linewidth=1.0, color="red")
    line(EjdivEc, (fq+anh)/1e9, plotter=pl, linestyle="dashed", linewidth=1.0, color="green")

    Ec=qbt.Ec
    E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
    E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
    E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
    fqp=(E1-E0)/h
    fq2p=(E2-E0)/h/2
    anhp=((E2-E1)-(E1-E0))/h
    line(EjdivEc, fqp/1e9, plotter=pl, linewidth=0.5, color="blue")
    line(EjdivEc, fq2p/1e9, plotter=pl, linewidth=0.5, color="red")
    line(EjdivEc, (fq+anhp)/1e9, plotter=pl, linewidth=0.5, color="green")
    return pl


if __name__=="__main__":
    a=Qubit()
    a.show()
    from atom.api import FloatRange
    from taref.core.api import tag_property
    from taref.plotter.api import LineFitter
    yoko=linspace(-5,5,3000)

    class Fitter(LineFitter):
        Ejmax=FloatRange(0.001, 100.0, 40.0).tag(tracking=True)
        offset=FloatRange(0.0, 100.0, 18.0).tag(tracking=True)

        @tag_property(private=True)
        def data(self):
            return a._get_flux_parabola(voltage=linspace(-1,1,100), offset=self.offset,
                                        Ejmax=self.Ejmax*h)

    d=Fitter()
    energy_level_plot(a)
    anharm_plot(a)
    a.show(d.plotter, d)

#        qdt=QDT(material='LiNbYZ',
#        ft="double",
#        a=80.0e-9,
#        Np=9,
#        Rn=3780.0, #(3570.0+4000.0)/2.0,
#        W=25.0e-6,
#        eta=0.5,
#        flux_factor=0.2945,
#        voltage=1.21,
#        offset=0.0)
#    EjdivEc=linspace(0.1, 300, 3000)
#    yoko=linspace(-5,5,3000)
#    #print a.calc_coupling(fqq=4.5e9), a.call_func("coupling", Ga=1.0)
#    from taref.plotter.api import line, Plotter
#    from taref.core.api import set_tag
#
#
#
#    def anharm_plot():
#        """reproduces anharm plot in Anton's paper"""
#        set_tag(qdt, "EjdivEc", log=False)
#        set_tag(qdt, "Ej", log=False)
#
#        #qdt.epsinf=qdt.epsinf/3.72
#        qdt.Np=10
#        qdt.Ec=qdt.fq*0.1*h
#
#        print qdt.max_coupling, qdt.coupling_approx
#        E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
#        anharm=(E2-E1)-(E1-E0)
#
#        E0p, E1p, E2p=qdt.call_func("lamb_shifted_transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
#
#        anharmp=(E2p-E1p)-(E1p-E0p)
#
#        fq= (E1-E0)/h#qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
#        ls_fq=(E1p-E0p)/h #qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
#        fq2=(E2-E1)/h
#        ls_fq2=(E2p-E1p)/h #qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
#
#        pl, pf=line(fq/qdt.f0, (anharmp/h-anharm/h)/(2.0*qdt.max_coupling), linewidth=0.5, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$")
#        line(fq/qdt.f0, (ls_fq-fq)/(2.0*qdt.max_coupling), plotter=pl, color="blue", linewidth=0.5, label=r"$\Delta_{1,0}$")
#        line(fq/qdt.f0, (ls_fq2-fq2)/(2.0*qdt.max_coupling), plotter=pl, color="red", linewidth=0.5, label=r"$\Delta_{2,1}$")
#        pl.set_ylim(-1.0, 0.6)
#        pl.set_xlim(0.7, 1.3)
#        pl.xlabel=r"$f_{10}/f_{IDT}$"
#        pl.ylabel=r"$\Delta/\Gamma_{10}^{MAX}$"
#        pl.legend(loc='lower left')
#        #fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
#        #line(EjdivEc, fq, plotter=pl, color="green", linewidth=0.5)
#
#        #line(EjdivEc, E1p, plotter=pl, color="green", linewidth=0.5)
#        #line(EjdivEc, E2p, plotter=pl, color="purple", linewidth=0.5)
#        return pl
#
#    def anharm_plot2():
#        """reproduces anharm plot in Anton's paper"""
#        set_tag(qdt, "EjdivEc", log=False)
#        set_tag(qdt, "Ej", log=False)
#        pl=Plotter(fig_width=9.0, fig_height=6.0)
#        #qdt.epsinf=qdt.epsinf/3.72
#        #qdt.Np=10
#        #qdt.Ec=qdt.fq*0.1*h
#        print qdt.max_coupling, qdt.coupling_approx
#        #flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=yoko)
#        #Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0)
#        #EjdivEc=Ej/qdt.Ec
#        anharm=qdt.call_func("anharm", EjdivEc=EjdivEc)
#        anharmp=qdt.call_func("lamb_shifted_anharm", EjdivEc=EjdivEc)
#        fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
#        ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
#        ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
#        #pl, pf=line(fq, anharm/h, linewidth=0.5, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$")
#
#        pl, pf=line(EjdivEc, anharmp/h/1e9, linewidth=1.0, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$", plotter=pl)
#        line(EjdivEc, anharm/h/1e9, linewidth=1.0, color="purple", label=r"anharm", plotter=pl)
#
#        line(EjdivEc, (ls_fq-fq)/1e9, plotter=pl, color="blue", linewidth=1.0, label=r"$\Delta_{1,0}$")
#        E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
#        fq2=(E2-E1)/h
#        line(EjdivEc, (ls_fq2-fq2)/1e9, plotter=pl, color="red", linewidth=1.0, label=r"$\Delta_{2,1}$")
#        pl.set_ylim(-2, 1.5)
#        #pl.set_xlim(0.0, 70)
#        pl.xlabel=r"$E_j/E_c$"
#        pl.ylabel=r"$\Delta (GHz)$"
#        #pl.legend(loc='lower right')
#        #fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
#        #line(EjdivEc, fq, plotter=pl, color="green", linewidth=0.5)
#
#        #line(EjdivEc, E1p, plotter=pl, color="green", linewidth=0.5)
#        #line(EjdivEc, E2p, plotter=pl, color="purple", linewidth=0.5)
#        return pl
#    pl=energy_level_plot()
#    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#    #       fig_name="energy_levels.pdf")
#    anharm_plot()
#    #pl=anharm_plot2()
#    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
#    #       fig_name="anharm1.pdf")
#    pl.show()
#
#    #a.show()

#Np=qdt.Np
#f0=5.45e9
#w0=2*pi*f0
##qdt.Dvv=0.001
#vf=3488.0
#freq=linspace(1e9, 10e9, 1000)
#print qdt.flux_factor, qdt.offset, qdt.Ejmax/h, qdt.Ec/h
#def flux_to_Ej(voltage,  offset=qdt.offset, flux_factor=qdt.flux_factor, Ejmax=qdt.Ejmax):
