# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:05:32 2016

@author: thomasaref
"""

from numpy import pi, linspace, sin, amax, argmin, argmax, cos, append
from scipy.constants import h
from taref.plotter.api import Plotter, line
from taref.core.api import SProperty, s_property
from taref.physics.idt import IDT
from taref.physics.qubit import Qubit

from taref.physics.fundamentals import sqrt, pi, e, h, array, eig, delete, sin, sinc_sq, sinc, linspace, zeros, absolute, cos, arange



class QDT(IDT, Qubit):
    base_name="QDT"

    #lamb_shifted_transmon_energy=SProperty()
    #@lamb_shifted_transmon_energy.getter
    def _get_lamb_shifted_transmon_energy(self, Ej, Ec, m, couple_mult, f0, K2, Np):
        Em=-Ej+sqrt(8.0*Ej*Ec)*(m+0.5) - (Ec/12.0)*(6.0*m**2+6.0*m+3.0)
        if m==0:
            return Em
        Emm1=-Ej+sqrt(8.0*Ej*Ec)*(m-1+0.5) - (Ec/12.0)*(6.0*(m-1)**2+6.0*(m-1)+3.0)
        fq=(Em-Emm1)/h
        fls=self._get_Lamb_shift(f=fq, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np)
        return Em+h*fls

    lamb_shifted_transmon_energy_levels=SProperty()
    @lamb_shifted_transmon_energy_levels.getter
    def _get_lamb_shifted_transmon_energy_levels(self, Ej, couple_mult, f0, K2, Np, Ec, n_energy):
        return [self._get_lamb_shifted_transmon_energy(Ej=Ej, Ec=Ec, m=m, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np) for m in range(n_energy)]

    lamb_shifted_fq=SProperty().tag(desc="""Operating frequency of qubit""", unit="GHz")
    @lamb_shifted_fq.getter
    def _get_lamb_shifted_fq(self, Ej, Ec):
        E0, E1=self._get_lamb_shifted_transmon_energy_levels(Ej=Ej, Ec=Ec, n_energy=2)
        return (E1-E0)/h

    lamb_shifted_anharm=SProperty().tag(desc="absolute anharmonicity", unit="hGHz")
    @lamb_shifted_anharm.getter
    def _get_lamb_shifted_anharm(self, Ej, Ec):
        E0, E1, E2=self._get_lamb_shifted_transmon_energy_levels(Ej=Ej, Ec=Ec, n_energy=3)
        return (E2-E1)/h-(E1-E0)/h

    lamb_shifted_fq2=SProperty().tag(desc="""20 over 2 freq""", unit="GHz")
    @lamb_shifted_fq2.getter
    def _get_lamb_shifted_fq2(self, Ej, Ec):
        E0, E1, E2=self._get_lamb_shifted_transmon_energy_levels(Ej=Ej, Ec=Ec, n_energy=3)
        return (E2-E0)/h/2.0

    #@s_property(desc="shunt capacitance of QDT", unit="fF")
    #def Cq(self, C):
    #    return C

    #@Cq.setter
    #def _get_C_get_Cq(self, Cq):
    #    return Cq

    ls_flux_parabola=SProperty()
    @ls_flux_parabola.getter
    def _get_ls_flux_parabola(self, voltage, offset, flux_factor, Ejmax, Ec):
        flx_d_flx0=self._get_flux_over_flux0(voltage=voltage, offset=offset, flux_factor=flux_factor)
        qEj=self._get_Ej(Ejmax=Ejmax, flux_over_flux0=flx_d_flx0)
        return self._get_lamb_shifted_fq(Ej=qEj, Ec=Ec)#, fq2(qEj, Ec)

    ls_f=SProperty().tag(sub=True)
    @ls_f.getter
    def _get_ls_f(self, f, couple_mult, f0, K2, Np):
        try:
            return array([sqrt(qf*(qf-2*self._get_Lamb_shift(f=qf, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np))) for qf in f])
        except TypeError:
            return sqrt(f*(f-2*self._get_Lamb_shift(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np)))

    ls_voltage_from_flux_par=SProperty().tag(sub=True)
    @ls_voltage_from_flux_par.getter
    def _get_ls_voltage_from_flux_par(self, f, C, Ejmax, offset, flux_factor, couple_mult, f0, K2, Np):
        ls_f=self._get_ls_f(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np)
        Ec=self._get_Ec(C=C)
        Ej=self._get_Ej_get_fq(fq=ls_f, Ec=Ec)
        flux_d_flux0=self._get_flux_over_flux0_get_Ej(Ej=Ej, Ejmax=Ejmax)
        return ls_f/1e9, self._get_voltage(flux_over_flux0=flux_d_flux0, offset=offset, flux_factor=flux_factor)

    ls_voltage_from_flux_par_many=SProperty().tag(sub=True)
    @ls_voltage_from_flux_par_many.getter
    def _get_ls_voltage_from_flux_par_many(self, f, C, Ejmax, offset, flux_factor, couple_mult, f0, K2, Np):
        ls_f=self._get_ls_f(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np)
        Ec=self._get_Ec(C=C)
        Ej=self._get_Ej_get_fq(fq=ls_f, Ec=Ec)
        fdf0=self._get_flux_over_flux0_get_Ej(Ej=Ej, Ejmax=Ejmax)
        flux_d_flux0=append(fdf0, -fdf0)
        flux_d_flux0=append(flux_d_flux0, -fdf0+pi)
        flux_d_flux0=append(flux_d_flux0, fdf0-pi)
        freq=append(f, f)
        freq=append(freq, freq)
        return freq/1e9, self._get_voltage(flux_over_flux0=flux_d_flux0, offset=offset, flux_factor=flux_factor)

    S11=SProperty()
    @S11.getter
    def _get_S11(self, f, couple_mult, f0, K2, Np, C, L):
        Ga=self._get_Ga(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C)
        Ba=self._get_Ba(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C)
        w=2*pi*f
        try:
            return Ga/(Ga+1j*Ba+1j*w*C+1.0/(1j*w*L))
        except ValueError:
            return array([Ga/(Ga+1j*Ba+1j*w*C+1.0/(1j*w*qL)) for qL in L])

    S13=SProperty()
    @S13.getter
    def _get_S13(self, f, couple_mult, f0, K2, Np, C, L, GL):
        Ga=self._get_Ga(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C)
        Ba=self._get_Ba(f=f, couple_mult=couple_mult, f0=f0, K2=K2, Np=Np, C=C)
        w=2*pi*f
        try:
            return 1j*sqrt(2.0*Ga*GL)/(Ga+1j*Ba+1j*w*C+1.0/(1j*w*L))
        except ValueError:
            return array([1j*sqrt(2.0*Ga*GL)/(Ga+1j*Ba+1j*w*C+1.0/(1j*w*qL)) for qL in L])


def energy_level_plot(qdt, fig_width=9.0, fig_height=6.0):
    pl=Plotter(fig_width=fig_width, fig_height=fig_height)
    EjdivEc=linspace(0.1, 300, 3000)
    Ej=EjdivEc*qdt.Ec
    E0, E1, E2=qdt._get_transmon_energy_levels(Ej=Ej, n_energy=3)
    line(EjdivEc, (E0+Ej)/h/1e9, plotter=pl, linestyle="dashed", linewidth=1.0)
    line(EjdivEc, (E1+Ej)/h/1e9, plotter=pl, linestyle="dashed", linewidth=1.0)
    line(EjdivEc, (E2+Ej)/h/1e9, plotter=pl, linestyle="dashed", linewidth=1.0)

    E0p, E1p, E2p=qdt._get_lamb_shifted_transmon_energy_levels(Ej=Ej, n_energy=3)
    line(EjdivEc, (E0p+Ej)/h/1e9, plotter=pl, color="red", linewidth=1.0)
    line(EjdivEc, (E1p+Ej)/h/1e9, plotter=pl, color="green", linewidth=1.0)
    line(EjdivEc, (E2p+Ej)/h/1e9, plotter=pl, color="purple", linewidth=1.0)
    pl.xlabel="$E_j/E_c$"
    pl.ylabel="Frequency (GHz)"
    return pl

def anharm_plot(qdt, fig_width=9.0, fig_height=6.0, ymin=-1.5, ymax=1.0):
    """Lamb shifted anharmonicity plot"""
    pl=Plotter(fig_width=fig_width, fig_height=fig_height)
    EjdivEc=linspace(0.1, 300, 3000)
    Ej=EjdivEc*qdt.Ec
    E0, E1, E2=qdt._get_transmon_energy_levels(Ej=Ej, n_energy=3)
    anharm=(E2-E1)-(E1-E0)

    E0p, E1p, E2p=qdt._get_lamb_shifted_transmon_energy_levels(Ej=Ej, n_energy=3)

    anharmp=(E2p-E1p)-(E1p-E0p)

    fq= (E1-E0)/h
    ls_fq=(E1p-E0p)/h
    fq2=(E2-E1)/h
    ls_fq2=(E2p-E1p)/h

    line(EjdivEc, anharm/h/1e9, plotter=pl, linewidth=0.5, color="purple", label=r"anharm")
    line(EjdivEc, anharmp/h/1e9, plotter=pl, linewidth=0.5, color="black", label=r"ls anharm")
    line(EjdivEc, (ls_fq-fq)/1e9, plotter=pl, color="blue", linewidth=0.5, label=r"$\Delta_{1,0}$")
    line(EjdivEc, (ls_fq2-fq2)/1e9, plotter=pl, color="red", linewidth=0.5, label=r"$\Delta_{2,1}$")
    pl.set_ylim(ymin, ymax)
    #pl.set_xlim(0.7, 1.3)
    pl.xlabel=r"$E_J/E_C$"
    pl.ylabel=r"$\Delta$ (GHz)"
    pl.legend(loc='lower left')
    #pl.set_ylim(-2, 1.5)
    #pl.set_xlim(0.0, 70)

    #anharm=qdt.call_func("anharm", EjdivEc=EjdivEc)
    #anharmp=qdt.call_func("lamb_shifted_anharm", EjdivEc=EjdivEc)
    #fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    #ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
    #ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
    #pl, pf=line(fq, anharm/h, linewidth=0.5, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$")

    #pl, pf=line(EjdivEc, anharmp/h/1e9, linewidth=1.0, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$", plotter=pl)
    #line(EjdivEc, anharm/h/1e9, linewidth=1.0, color="purple", label=r"anharm", plotter=pl)

    #line(EjdivEc, (ls_fq-fq)/1e9, plotter=pl, color="blue", linewidth=1.0, label=r"$\Delta_{1,0}$")
    #E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
    #fq2=(E2-E1)/h
    #line(EjdivEc, (ls_fq2-fq2)/1e9, plotter=pl, color="red", linewidth=1.0, label=r"$\Delta_{2,1}$")
    #pl.xlabel=r"$E_j/E_c$"
    #pl.ylabel=r"$\Delta (GHz)$"
    #pl.legend(loc='lower right')
    #fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
    #line(EjdivEc, fq, plotter=pl, color="green", linewidth=0.5)

    #line(EjdivEc, E1p, plotter=pl, color="green", linewidth=0.5)
    #line(EjdivEc, E2p, plotter=pl, color="purple", linewidth=0.5)
    return pl

antonqdt=QDT(name="antonqdt", material='LiNbYZ', #10 finger QDT used for anharmonicity plot in Anton's paper
        ft="double",
        a=80.0e-9,
        Np=10,
        Rn=3780.0, #(3570.0+4000.0)/2.0,
        W=25.0e-6,
        eta=0.5,
        flux_factor=0.2945,
        voltage=1.21,
        offset=0.0)
antonqdt.Ec=antonqdt.f0*0.1*h #Ec is 1/10 of f0


def anton_anharm_plot(fig_width=9, fig_height=6):
    """reproduces anharm plot in Anton's paper"""

    pl=Plotter(fig_width=fig_width, fig_height=fig_height)

    #print qdt.f0*h/qdt.Ec, qdt.epsinf/3.72
    #qdt.Np=10
    #qdt.Ec=qdt.f0*0.1*h

    EjdivEc=linspace(0.1, 300, 3000)
    Ej=EjdivEc*antonqdt.Ec

    print antonqdt.C, antonqdt.C, antonqdt.Ec, antonqdt._get_Ec(antonqdt.C)

    print antonqdt.max_coupling, antonqdt.epsinf, antonqdt.f0*h/antonqdt.Ec
    E0, E1, E2=antonqdt._get_transmon_energy_levels(Ej=Ej, n_energy=3)
    anharm=(E2-E1)-(E1-E0)

    E0p, E1p, E2p=antonqdt._get_lamb_shifted_transmon_energy_levels(Ej=Ej, n_energy=3)

    anharmp=(E2p-E1p)-(E1p-E0p)

    fq= (E1-E0)/h#qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    ls_fq=(E1p-E0p)/h #qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
    fq2=(E2-E1)/h
    ls_fq2=(E2p-E1p)/h #qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)

    line(fq/antonqdt.f0, (anharmp/h-anharm/h)/(2.0*antonqdt.max_coupling), plotter=pl, linewidth=0.5, color="black", label=r"$\Delta_{2,1}-\Delta_{1,0}$")
    line(fq/antonqdt.f0, (ls_fq-fq)/(2.0*antonqdt.max_coupling), plotter=pl, color="blue", linewidth=0.5, label=r"$\Delta_{1,0}$")
    line(fq/antonqdt.f0, (ls_fq2-fq2)/(2.0*antonqdt.max_coupling), plotter=pl, color="red", linewidth=0.5, label=r"$\Delta_{2,1}$")
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

antonqdt3=QDT(name="antonqdt3", material='LiNbYZ', #10 finger QDT used for anharmonicity plot in Anton's paper
        ft="double",
        a=80.0e-9,
        Np=3,
        Rn=3780.0, #(3570.0+4000.0)/2.0,
        W=25.0e-6,
        eta=0.5,
        flux_factor=0.2945,
        voltage=1.21,
        offset=0.0)
antonqdt3.Ec=antonqdt3.f0*0.1*h #Ec is 1/10 of f0

def anton_lamb_shift_plot(fig_width=9.0, fig_height=6.0):
    """reproduces coupling/lamb shift plot in Anton's paper"""
    pl=Plotter(fig_width=fig_width, fig_height=fig_height)
    EjdivEc=linspace(0.1, 300, 10000)
    Ej=EjdivEc*antonqdt.Ec
    #E0, E1, E2=antonqdt._get_transmon_energy_levels(Ej=Ej, n_energy=3)
    fq=antonqdt._get_fq(Ej)
    #anharm=(E2-E1)-(E1-E0)
    #E0p, E1p, E2p=antonqdt._get_lamb_shifted_transmon_energy_levels(Ej=Ej, n_energy=3)
    #anharmp=(E2p-E1p)-(E1p-E0p)
    #fq= (E1-E0)/h#qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    coup=antonqdt._get_coupling(fq)
    ls=antonqdt._get_Lamb_shift(fq)
    line(fq/antonqdt.f0, 2.0*coup/(2.0*antonqdt.max_coupling), plotter=pl, linewidth=0.5, color="red", label=r"$\Gamma$, $N=10$")
    line(fq/antonqdt.f0, ls/(2.0*antonqdt.max_coupling), plotter=pl, color="green", linewidth=0.5, label=r"$\Delta$, $N=10$")

    #antonqdt.Np=3
    Ej=EjdivEc*antonqdt3.Ec
    fq=antonqdt3._get_fq(Ej)
    coup=antonqdt3._get_coupling(fq)
    ls=antonqdt3._get_Lamb_shift(fq)
    line(fq/antonqdt3.f0, 2.0*coup/(2.0*antonqdt3.max_coupling), plotter=pl, linewidth=0.5, color="blue", label=r"$\Gamma$, $N=3$")
    line(fq/antonqdt3.f0, ls/(2.0*antonqdt3.max_coupling), plotter=pl, color="black", linewidth=0.5, label=r"$\Delta$, $N=3$")
    pl.set_ylim(-0.4, 1.0)
    pl.set_xlim(0.2, 1.8)
    pl.xlabel=r"$f_{10}/f_{IDT}$"
    pl.ylabel=r"$\Delta/\Gamma_{10}^{MAX}$"
    pl.legend(loc='upper right')
    return pl

if __name__=="__main__":
    anton_anharm_plot()
    #anharm_plot(antonqdt).show()
    anton_lamb_shift_plot().show()

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
    print qdt.C, qdt.Cq, qdt.Ec, qdt._get_Ec(qdt.C)
    yoko=linspace(-5,5,3000)
    #print a.calc_coupling(fqq=4.5e9), a.call_func("coupling", Ga=1.0)
    from taref.plotter.api import line, Plotter
    from taref.core.api import set_tag






    pl=energy_level_plot(qdt)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #       fig_name="energy_levels.pdf")
    anharm_plot(qdt)
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