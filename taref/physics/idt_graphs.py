# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:24:00 2016

@author: thomasaref
"""

from idt import IDT
from numpy import linspace, sin, cos, real, imag
from taref.plotter.api import line
from scipy.constants import pi
from scipy.signal import hilbert


def metallization_couple(pl="metallization_couple", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.N_fixed=100000
    #idt.fixed_freq_max=20.0*idt.f0
    idt.eta=0.5
    #idt.ft="single"
    #idt.S_type="RAM"
    idt.couple_type="full expr"
    idt.fixed_reset()
    line(idt.fixed_freq/idt.f0, idt.fixed_coupling, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)

    pl=line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)
    idt.eta=0.6
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.6", color="red", linewidth=0.3, label="0.6", **kwargs)
    idt.eta=0.4
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.4", color="green", linewidth=0.3, label="0.4", **kwargs)
    idt.eta=0.5
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling"
    pl.legend()
    return pl
#metallization_couple()#.show()
def metallization_Lamb(pl="metallization_lamb", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.eta=0.5
    idt.N_fixed=100000
    #idt.fixed_freq_max=20.0*idt.f0

    #idt.ft="single"
    idt.couple_type="full expr"
    #idt.Lamb_shift_type="hilbert"
    idt.fixed_reset()
    pl=line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)
    idt.eta=0.6
    idt.fixed_reset()
    #line(idt.fixed_freq/idt.f0, idt.fixed_Lamb_shift/idt.max_coupling, plotter=pl, linewidth=0.3, color="purple")
    line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.6", color="red", linewidth=0.3, label="0.6", **kwargs)
    idt.eta=0.4
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.4", color="green", linewidth=0.3, label="0.4", **kwargs)
    idt.eta=0.5
    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift"
    pl.legend()
    return pl
#metallization_Lamb()#.show()

def sinc_check(pl="sinc_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="sinc"#, "giant atom", "full sum"
    idt.Ba_type="formula"
    idt.rs_type="constant"
    frq=linspace(0.01e9, 10e9, 10000)
    idt.fixed_freq_max=20.0*idt.f0
    pl=line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, label=idt.Ga_type, color="red",  **kwargs)
    X=idt.Np*pi*(frq-idt.f0)/idt.f0
    line(frq/idt.f0, (sin(X)/X)**2, plotter=pl, label=idt.Ga_type, color="green", **kwargs)
    line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    idt.Ba_type="hilbert"
    line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, color="red", **kwargs)
    line(frq/idt.f0, -imag(hilbert(idt._get_Ga(frq)/idt.Ga0_approx)), plotter=pl, label=idt.Ga_type, color="green", **kwargs)
    print idt.Ga0, idt.Ga0_approx
    print idt.Ga0_mult
    print idt.max_coupling, idt.max_coupling_approx
    return pl
#sinc_check()#.show()

def giant_atom_check(pl="giant_atom_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="giant atom"#, "full sum"
    idt.Ba_type="formula"
    idt.rs_type="constant"
    frq=linspace(0e9, 10e9, 10000)
    idt.fixed_freq_max=20.0*idt.f0
    pl=line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, label=idt.Ga_type, color="red",  **kwargs)
    X=idt.Np*pi*(frq-idt.f0)/idt.f0
    Np=idt.Np
    line(frq/idt.f0, (sin(X)/X)**2, plotter=pl, label=idt.Ga_type, color="purple", **kwargs)

    line(frq/idt.f0, (1.0/Np*sin(X)/sin(X/Np))**2, plotter=pl, label=idt.Ga_type, color="green", **kwargs)
    line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    idt.Ba_type="hilbert"
    line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, color="red", **kwargs)
    line(frq/idt.f0, -imag(hilbert(idt._get_Ga(frq)/idt.Ga0_approx)), plotter=pl, label=idt.Ga_type, color="green", **kwargs)
    print idt.Ga0, idt.Ga0_approx
    print idt.Ga0_mult
    print idt.max_coupling, idt.max_coupling_approx
    return pl
#giant_atom_check().show()

def sinc_variety_check(pl="sinc_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="sinc"#, "giant atom", "full sum"
    idt.Ba_type="formula"
    frq=linspace(0e9, 10e9, 10000)
    idt.fixed_freq_max=20.0*idt.f0
    pl=line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label="sinc", **kwargs)
    idt.Y0_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label="Y0", color="red", **kwargs)
    idt.Y0_type="center"
    idt.df_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label="df", color="green", **kwargs)
    idt.df_type="center"
    idt.mus_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label="alpha", color="purple", **kwargs)

    #X=idt.Np*pi*(frq-idt.f0)/idt.f0
    #line(frq/idt.f0, (sin(X)/X)**2, plotter=pl, label=idt.Ga_type, color="blue", **kwargs)
    #line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    #idt.Ba_type="hilbert"
    #line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    #line(frq/idt.f0, -imag(hilbert(idt._get_Ga(frq)/idt.Ga0_approx)), plotter=pl, label=idt.Ga_type, **kwargs)
    #print idt.Ga0, idt.Ga0_approx
    #print idt.Ga0_mult
    #print idt.max_coupling, idt.max_coupling_approx
    return pl
#sinc_variety_check().show()

def giant_atom_variety_check(pl="giant_atom_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="giant atom"#, "full sum"
    idt.Ba_type="formula"
    frq=linspace(0e9, 10e9, 10000)
    idt.fixed_freq_max=20.0*idt.f0
    pl=line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label="giant atom", **kwargs)
    idt.Y0_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label="Y0", color="red", **kwargs)
    idt.Y0_type="center"
    idt.df_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label="df", color="green", **kwargs)
    idt.df_type="center"
    idt.mus_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label="alpha", color="purple", **kwargs)

    X=idt.Np*pi*(frq-idt.f0)/idt.f0
    line(frq/idt.f0, (sin(X)/X)**2, plotter=pl, label="sinc", color="blue", **kwargs)
    #line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    #idt.Ba_type="hilbert"
    #line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    #line(frq/idt.f0, -imag(hilbert(idt._get_Ga(frq)/idt.Ga0_approx)), plotter=pl, label=idt.Ga_type, **kwargs)
    #print idt.Ga0, idt.Ga0_approx
    #print idt.Ga0_mult
    #print idt.max_coupling, idt.max_coupling_approx
    return pl
#giant_atom_variety_check().show()

def couple_comparison(pl="couple_compare", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0.01e9, 10*10e9, 10000)

    idt.fixed_freq_max=20.0*idt.f0
    idt.S_type="RAM"
    idt.eta=0.55
    #idt.Y0_type="center"
    #idt.df_type="center"
    #idt.mus_type="center"
    #idt.Ga_type="sinc"
    #idt.Ba_type="formula"
    #idt.rs_type="constant"

    #(P11, P12, P13,
    # P21, P22, P23,
    # P31, P32, P33), Ga, Ba, Ct=idt._get_RAM_P(frq=frq, Y0=None)
    #pl=line(frq/idt.f0, Ga/idt.Ga0_approx, plotter=pl, color="cyan", label=idt.S_type, **kwargs)

    pl=line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="cyan", label=idt.S_type, **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()

    idt.Ga_type="giant atom"
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="red", label="full expr", **kwargs)

    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="sinc"
    idt.Ba_type="formula"
    idt.rs_type="constant"
    pl=line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    idt.Ga_type="giant atom"
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="green", label=idt.Ga_type, **kwargs)
    #idt.couple_type="full expr"
    #line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="black", linewidth=0.5, label=idt.couple_type)
    #idt.couple_type="full sum"
    #line(frq/idt.f0, (idt._get_coupling(frq)), plotter=pl, color="purple", linewidth=0.5, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling"
    #pl.set_ylim(0.0, 1.3e9)
    pl.legend()
    return pl
#couple_comparison()#.show()

def Lamb_shift_comparison(pl="ls_compare", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0.01e9, 10*10e9, 10000)

    idt.fixed_freq_max=20.0*idt.f0
    idt.S_type="RAM"
    idt.eta=0.55

    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="cyan", label=idt.S_type, **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()

    idt.Ga_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="red", label="full expr", **kwargs)

    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="sinc"
    idt.Ba_type="formula"
    idt.rs_type="constant"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    idt.Ga_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="green", label=idt.Ga_type, **kwargs)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling"
    pl.legend()
    return pl
#Lamb_shift_comparison()#.show()

def RAM_comparison(pl="RAM_compare", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0.01e9, 10e9, 10000)
    #idt.Np=37
    idt.fixed_freq_max=20.0*idt.f0
    idt.S_type="RAM"
    idt.eta=0.55
    #idt.dloss1=0.19
    #idt.dloss2=0.88#*100


    #idt.Y0_type="center"
    #idt.df_type="center"
    #idt.mus_type="center"
    #idt.Ga_type="sinc"
    #idt.Ba_type="formula"
    #idt.rs_type="constant"
    #idt.rs=-0.017j
    pl=line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="blue", label=idt.S_type, **kwargs)
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="blue",  **kwargs)

    idt.S_type="simple"
    idt.fixed_reset()

    idt.Ga_type="giant atom"
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="red", label="full expr", **kwargs)
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="red",  **kwargs)

    #idt.S_type="RAM"
    #idt.ft="single"
    #idt.fixed_reset()
    #pl=line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="green", label="RAM single", **kwargs)
    #line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="green", label="RAM single", **kwargs)

    #pl=line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    #idt.Ga_type="giant atom"
    #line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="green", label=idt.Ga_type, **kwargs)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling/center coupling"
    pl.set_ylim(-0.7, 1.1)
    pl.legend()
    return pl

#RAM_comparison().show()

def RAM_single_vs_double(pl="RAM_sf_df", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0.01e9, 10e9, 10000)
    #idt.material="GaAs"
    #idt.Np=51
    idt.fixed_freq_max=20.0*idt.f0
    idt.S_type="RAM"
    pl=line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="blue", label=idt.S_type, **kwargs)
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="blue", **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()

    idt.Ga_type="giant atom"
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="red", label="full expr", **kwargs)
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="red", **kwargs)

    idt.S_type="RAM"
    idt.ft="single"
    idt.fixed_reset()
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, color="green", label="RAM single", **kwargs)
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling_approx, plotter=pl, color="green", **kwargs)

    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling"
    pl.set_ylim(-0.8, 1.1)
    pl.legend()
    return pl
RAM_single_vs_double().show() #IDT=IDT(Np=37)

def RAM_comparison(pl="RAM_compare", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    #idt2=IDT.process_kwargs(kwargs)

    frq=linspace(0.01e9, 10e9, 10000)
    idt.fixed_freq_max=2.0*idt.f0

    def _get_RAM_P_one_f(self, f, Dvv, epsinf, W, vf,  rs, p, N_IDT, alpha, ft, Np, f0, dloss1, dloss2, L_IDT):
        #Y0=self._get_Y0(f=f, Dvv=Dvv, epsinf=epsinf, W=W)
        #rs=self._get_rs(f=f)
        #print rs
        k=2*pi*f/vf#-1.0j*(f/f0*dloss1+dloss2*(f/f0)**2)
        ts = sqrt(1.0-absolute(rs)**2)
        A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
                           [-rs,             exp(1.0j*k*p)]])#.astype(complex128)
        #AN=A**int(N_IDT)
        #AN11, AN12, AN21, AN22= AN[0,0], AN[0,1], AN[1,0], AN[1,1]
        #P11=-AN21/AN22
        #P21=AN11-AN12*AN21/AN22
        #P12=1.0/AN22
        #P22=AN12/AN22
        #D = -1.0j*alpha*Dvv*sqrt(Y0)
        #B = matrix([(1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0), (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)])
        I = eye(2)

        P1=(I+A)
        P2=inv(I-A**4)*(I-A**(4*int(Np)))
        return 1/sqrt(2)*absolute(P1[1,1]*exp(-1.0j*k*p/2.0))*absolute(P2[1,1])**2 ##, P2

    #idt.Np=37
    #idt.ft="single"
    #idt.couple_type="full expr"
    #pl=line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, linewidth=0.5, label=idt.couple_type, **kwargs)
    #data=[_get_RAM_P_one_f(idt, f=f, Dvv=idt.Dvv, epsinf=idt.epsinf, W=idt.W, vf=idt.vf, rs=idt.rs, p=idt.p,
    #                             N_IDT=idt.N_IDT, alpha=idt.alpha0, ft=idt.ft, Np=idt.Np, f0=idt.f0, dloss1=idt.dloss1, dloss2=idt.dloss2, L_IDT=idt.L_IDT) for f in frq]
    #data=array(data)
    #print data.shape
    #line(frq, array(data), pl=pl, color="green")
    Np=idt.Np
    gX=idt._get_X(f=frq)
    #line(frq, 1/81.0*(sqrt(2.0)*cos(pi*frq/(4.0*idt.f0))*sin(gX)/sin(gX/Np))**2, pl=pl)#.show()
    #line(frq, 2.0*cos(pi*frq/(4.0*idt.f0)), pl=pl).show()
    print idt.f0, idt.Dvv, idt.epsinf, idt.W, idt.vf,  idt.rs, idt.p, idt.N_IDT, idt.alpha, idt.ft, idt.Np, idt.f0, idt.dloss1, idt.dloss2, idt.L_IDT
    #idt.S_type="RAM"
    idt.couple_type="full expr"
    idt.fixed_reset()

    #P=idt._get_RAM_P()
    gamma=idt._get_couple_factor(f=idt.fixed_freq)
    line(idt.fixed_freq, idt._get_couple_factor(f=idt.fixed_freq), plotter=pl, color="red", linewidth=0.5, label=idt.ft)#.show()
    line(idt.fixed_freq, gamma, plotter=pl, color="blue", linewidth=0.5, label=idt.ft).show()

    #line(idt.fixed_freq, gamma*2*idt.Ct*2*pi*P[1], plotter=pl, color="red", linewidth=0.5, label=idt.ft)#.show()
    #line(idt.fixed_freq, P[2], plotter=pl, color="green", linewidth=0.5, label=idt.ft)
    idt.S_type="simple"
    #idt.ft="double"
    idt.couple_type="df giant atom" #"full expr"
    idt.fixed_reset()
    line(idt.fixed_freq, gamma*2*idt.Ct*2*pi*idt._get_Ga(idt.fixed_freq)/idt.Ga0, plotter=pl, color="blue", linewidth=0.5, label=idt.ft).show()
    line(idt.fixed_freq, idt._get_Ba(idt.fixed_freq), plotter=pl, color="black", linewidth=0.5, label=idt.ft).show()

    #idt.Np=37
    #idt.fixed_freq_max=20.0*idt.f0

    #idt2.ft="single"

    #idt.fixed_reset()
    line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="red", linewidth=0.5, label=idt.ft)
    idt.ft="single"
    idt.fixed_reset()
    line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="green", linewidth=0.5, label=idt.ft)
    idt.S_type="simple"
    idt.ft="double"
    idt.couple_type="full expr"
    idt.fixed_reset()
    pl=line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, linewidth=0.5, label=idt.couple_type, **kwargs)

    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling"
    #pl.set_ylim(-30, 1.0)
    pl.legend()
    return pl
#RAM_comparison().show()
#couple_comparison()#.show()
def fix_couple_comparison(pl="fix couple", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.fixed_freq_max=20.0*idt.f0
    idt.couple_type="sinc sq"
    idt.fixed_reset()
    frq=linspace(0e9, 10e9, 10000)
    pl=line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, linewidth=0.3, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="df giant atom"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="green", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full expr"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="black", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full sum"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="purple", linewidth=0.3, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling/max coupling (dB)"
    pl.set_ylim(-30, 1.0)
    pl.legend()
    return pl

#fix_couple_comparison().show()
def Lamb_shift_comparison(pl="ls_comp", **kwargs):
    idt=IDT.process_kwargs(kwargs)

    #idt.rs=-0.01j
    #idt.dloss2=0.1*1e6
    #idt.eta=0.4
    frq=linspace(0e9, 10e9, 10000)
    #idt.N_fixed=100000
    idt.fixed_freq_max=20.0*idt.f0

    idt.S_type="RAM"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(f=frq), plotter=pl, color="cyan", linewidth=0.5, label=idt.S_type, **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()

    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc sq"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, linewidth=0.5, label="sinc^2", **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="red", linewidth=0.5, label=idt.couple_type)

    idt.Lamb_shift_type="hilbert"
    idt.couple_type="df giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="green", linewidth=0.5, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="black", linewidth=0.5, label=idt.couple_type)
    #idt.couple_type="full sum"
    #line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="purple", linewidth=0.5, label=idt.couple_type)

    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift"
    pl.set_ylim(-1e9, 1e9)
    pl.legend(loc="lower right")
    return pl

#Lamb_shift_comparison()#.show()

def hilbert_check(pl="hilbert", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    #idt.N_fixed=100000
    idt.fixed_freq_max=20.0*idt.f0
    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc sq"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, linewidth=1.0, label="sinc^2", **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="red", linewidth=1.0, label=idt.couple_type)
    idt.Lamb_shift_type="hilbert"
    idt.couple_type="sinc sq"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="green", linewidth=0.5, label="h(sinc^2)")
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="black", linewidth=0.5, label="h(giant atom)")

    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift"
    pl.set_ylim(-1e9, 1e9)
    pl.legend(loc="lower right")
    return pl

#hilbert_check().show()

def Lamb_shift_check(pl="ls_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.fixed_freq_max=20.0*idt.f0
    frq=linspace(0e9, 10e9, 10000)

    idt.S_type="RAM"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(f=frq)/idt.max_coupling, plotter=pl, color="cyan", linewidth=0.5, label=idt.S_type, **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()

    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc sq"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, linewidth=0.5, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="red", linewidth=0.5, label=idt.couple_type)
    idt.couple_type="df giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="green", linewidth=0.5, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="black", linewidth=0.5, label=idt.couple_type)
    #idt.couple_type="full sum"
    #line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="purple", linewidth=0.5, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift/max coupling (dB)"
    pl.set_ylim(-1.0, 1.0)
    pl.legend(loc="lower right")

    #line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl

#Lamb_shift_check().show()
def formula_comparison(pl=None, **kwargs):
    a=IDT()
    frq=linspace(3e9, 7e9, 10000)
    print a._get_coupling(frq)
    print a.max_coupling
    pl, pf=line(frq, a._get_coupling(frq)/a.max_coupling, plotter=pl, linewidth=1.0, **kwargs)
    line(frq, a._get_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="red", linewidth=1.0)
    #line(frq, coup, color="purple", plotter=pl, linewidth=0.3)
    line(frq, a._get_full_coupling(frq)/a.max_coupling, plotter=pl, color="green", linewidth=0.3)
    line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl
if 0:
    idt=IDT()
    element_factor_plot(idt=idt)#.show()

    Lamb_shift_comparison(idt=idt)

    couple_comparison(idt=idt)#.show()

    fix_couple_comparison(idt=idt)#.show()

    Lamb_shift_check(idt=idt).show()

#formula_comparison()#.show()

#element_factor_plot(idt=idt).show()
if __name__=="__main__":
    #a=IDT(dloss1=0.0, dloss2=0.0, eta=0.6, ft="double")
    a=IDT(material='LiNbYZ',
          ft="double",
          a=80.0e-9, #f0=5.35e9,
          Np=9,
          #Rn=3780.0, #(3570.0+4000.0)/2.0, Ejmax=h*44.0e9,
          W=25.0e-6,
          eta=0.5,)
          #flux_factor=0.515, #0.2945, #0.52,
          #voltage=1.21,
          #offset=-0.07)
    #print a.fixed_P
    a.fixed_reset()
    #a.Y0_type="center"
    #a.mus_type="center"
    #a.df_type="center"
    #print a.f0
    #Y0, mus/Dvv, df_corr, cpl_form
    #2.0*/a.K2*absolute(mus/Dvv *Dvv *df_corr*1.0)**2
    #(mus/Dvv*df_corr)**2  Dvv*(Np**2)

    #print 2*pi*a.f0*a.W*a.epsinf/a.K2
    print a.Ga0, a.Ga0_approx
    print a.Ga0_mult
    print a.max_coupling, a.max_coupling_approx
    #a.S_type="RAM"

if __name__=="__main2__":

    Lamb_shift_comparison()#.show()
    couple_comparison().show()
    #print a.fixed_P
    #print squeeze(a.fixed_coupling)
    a.show()
    a.f=a.f0
    print a.fixed_polarity
    print a.alpha
    print a.fixed_element_factor
    print a._get_element_factor(a.f0)
    from scipy.signal import hilbert
    from numpy import imag, real, sin, cos, exp, array, absolute


    frq=linspace(1e9, 10e9, 10000)

    X=a._get_X(f=frq)
    Np=a.Np
    f0=a.f0

    if 0:
        def Asum(N, k1=0.0, k2=0.0):
            return array([sum([exp(2.0j*pi*f/f0*n-f/f0*k1-k2*(f/f0)**2) for n in range(N)]) for f in frq])

        def Asum2(M):
            return array([sum([exp(2j*pi*M*f/f0)*exp(2j*pi*f/f0*m) for m in range(-M, M+1)]) for f in frq])

        def Asum3(M, k=1.0):
            return array([sum([exp(2j*pi*f/f0*m) for m in range(-M, M+1)]) for f in frq])

        def Asum4(M):
            return array([sum([2*cos(2*pi*f/f0*m) for m in range(0, M+1)]) for f in frq])-1

        def Asum5(M, g=0.9, g2=1.0):
            return array([g*2*cos(2*pi*f/f0*M) for f in frq])+array([g2*2*cos(2*pi*f/f0*(M-1)) for f in frq])+Asum4(M-2)

        def Asum6(g=1.0):
            return array([(g*exp(-2j*pi*f/f0*4)+exp(-2j*pi*f/f0*3)+exp(-2j*pi*f/f0*2)+exp(-2j*pi*f/f0*1)+1.0
            +exp(2j*pi*f/f0*1)+exp(2j*pi*f/f0*2)+exp(2j*pi*f/f0*3)+g*exp(2j*pi*f/f0*4)) for f in frq])

        def Asum7(g=1.0):
            return array([(g+exp(2j*pi*f/f0*1)+exp(2j*pi*f/f0*2)+exp(2j*pi*f/f0*3)+exp(2j*pi*f/f0*4)
            +exp(2j*pi*f/f0*5)+exp(2j*pi*f/f0*6)+exp(2j*pi*f/f0*7)+g*exp(2j*pi*f/f0*8)) for f in frq])

        A=Asum(9, k1=0.05, k2=0.05)
        A2=Asum2(4)
        A3=Asum3(4)
        A4=Asum4(4)
        A5=Asum5(4, 1.2, 1.0)
        A6=Asum6(0.5)
        A7=Asum7(0.5)

        pl=Plotter()
        #line(frq/1e9, real(A), plotter=pl)
        #line(frq/1e9, imag(A), plotter=pl, color="red")

        #line(frq/1e9, real(A2), plotter=pl, color="green", linewidth=0.5)
        #line(frq/1e9, imag(A2), plotter=pl, color="black", linewidth=0.5)

        line(frq/1e9, sin(pi*9*frq/f0)/sin(pi*frq/f0), plotter=pl)

        line(frq/1e9, real(A3), plotter=pl, color="green", linewidth=0.5)
        line(frq/1e9, imag(A3), plotter=pl, color="black", linewidth=0.5)

        line(frq/1e9, A4, plotter=pl, color="red", linewidth=0.5)
        #line(frq/1e9, A5, plotter=pl, color="purple", linewidth=0.5)
        line(frq/1e9, real(A6), plotter=pl, color="darkgray", linewidth=0.5)
        line(frq/1e9, imag(A6), plotter=pl, color="darkgray", linewidth=0.5)

        #pl.show()
        pl=Plotter()

        line(frq/1e9, 1/81.0*absolute(A)**2, plotter=pl, color="black")
        #line(frq/1e9, 1/81.0*absolute(sin(pi*9*frq/f0)/sin(pi*frq/f0))**2, plotter=pl, color="green", linewidth=0.4)
        #line(frq/1e9, 1/81.0*absolute(A5)**2, plotter=pl, color="blue", linewidth=0.5)
        line(frq/1e9, 1/81.0*absolute(A6)**2, plotter=pl, color="red", linewidth=0.5)
        line(frq/1e9, 1/81.0*absolute(A7)**2, plotter=pl, color="purple", linewidth=0.5)

        #line(frq/1e9, 1/9.0*absolute(A6), plotter=pl, color="red", linewidth=0.5)

        #line(frq/1e9, 1/9.0*absolute(A7), plotter=pl, color="purple", linewidth=0.5)

        pl.show()

    frq=linspace(0, 40e9, 10000)

    X=a._get_X(f=frq)
    Np=a.Np
    f0=a.f0

    #coup=(sqrt(2)*cos(pi*frq/(4*f0))*(1.0/Np)*sin(X)/sin(X/Np))**2
    coup=(sin(X)/X)**2

    #coup=(1.0/Np*sin(X)/sin(X/Np))**2


    element_factor_plot(a)
    pl=Plotter()
    line(frq, a._get_coupling(frq)/a.max_coupling, plotter=pl, linewidth=1.0)
    line(frq, a._get_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="red", linewidth=1.0)
    line(frq, coup, color="purple", plotter=pl, linewidth=0.3)
    line(frq, a._get_full_coupling(frq)/a.max_coupling/1.247**2/2, plotter=pl, color="green", linewidth=0.3)
    line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling/1.247**2/2, plotter=pl, color="black", linewidth=0.3)

    #hb=hilbert(coup) #a._get_coupling(frq))
    #line(frq, real(hb), plotter=pl, color="green", linewidth=0.3)
    #line(frq, imag(hb), plotter=pl, color="black", linewidth=0.3)
    #Baa= (1+cos(X/(4*Np)))*(1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
    Baa=-(sin(2.0*X)-2.0*X)/(2.0*X**2)
    #Baa= (1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
    line(frq, Baa, plotter=pl, color="cyan", linewidth=0.3)

    pl.show()

    b=IDT(ft="single")
    a.ft_mult=5
    print a.mu_mult, a.ft_mult, b.mu_mult, b.ft_mult
    print a.couple_mult, b.couple_mult
    a.ft="single"
    a.ft_mult=None
    print a.mu_mult, a.ft_mult, b.mu_mult, b.ft_mult
    print a.couple_mult, b.couple_mult

    print a.epsinf, a.C
    a.epsinf=4e-10
    print a.C
    a.C=7.1e-14
    print a.epsinf, a.C

    print a._get_C(W=35)



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
    a.show()
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