# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 16:00:51 2015

@author: thomasaref
"""

from numpy import mean
from numpy import sin, cos, sqrt, exp, empty

from atom.api import Callable
from TA_constants import Check, _master_check, EJmax, EC, pi, h, f0, Gamma_tot, gamma_10, xi, S11_0, theta_L, S22_0, S21_0, theta_CT, T_CT, hf0


class Fundamental_Functions(Check):
    cos=Callable(cos).tag(desc="cosine",
                          latex='\cos')

    sin=Callable(sin).tag(desc="sine",
                          latex='\sin')

    exp=Callable(exp).tag(desc="exponent",
                          latex='\exp')

    sqrt=Callable(sqrt).tag(desc="square root",
                            latex='\sqrt')

    empty=Callable(empty).tag(desc="makes empty array",
                              latex='empty')
    mean=Callable(mean).tag(desc="mean",
                              latex='mean')

fundamental_functions=Fundamental_Functions()

def update_log(log_str):
    _master_check.update_log(log_str)

class func_log:
    """decorator class to allow function logging"""
    def update_log(self, log_str):
        print log_str

    def __init__(self, f):
        self.f = f
        arg_count=self.f.func_code.co_argcount
        self.run_params=list(self.f.func_code.co_varnames[0:arg_count])
        self.func_name=self.f.func_name
        self.metadata=dict()

    def __call__(self, *args, **kwargs):
        update_log("RAN: {name}".format(
                 name=self.f.func_name))#, run_params=self.run_params))
        return self.f(*args, **kwargs)

    def tag(self, **kwargs):
        self.metadata.update(**kwargs)

@func_log
def mean_and_remove_offset(raw_data, offset, dimension=2):
    """Average over all flux values (it's a very narrow range)"""
    return mean(raw_data, dimension) - offset
mean_and_remove_offset.tag(latex="mean({0}, {2})-{1}")

def dB2amp(trace_dB):
    return 10.0**(trace_dB/20.0)

from numpy import log10, absolute, dtype, angle

def dB(x):
    return 20.0*log10(absolute(x))

def magphase(y, response="Mag"):
        if dtype("complex128")==y.dtype:
            if response=="Phase":
                return angle(y)
            elif response=="Mag (dB)":
                return dB(y)
            else:
                return absolute(y)
        return y

# Helper functions
# Omega_10 in regular frequency units
@func_log
def flux_parabola(flux_over_flux0):
    """Omega_10 in regular frequency unit"""
    EJ = EJmax*abs(cos(pi*flux_over_flux0))
    E0 = -EJ + sqrt(8*EJ*EC)*0.5 - (EC/4)
    E1 = -EJ + sqrt(8*EJ*EC)*1.5 - (EC/12.0)*(6+6+3)
    return (E1-E0)/h
flux_parabola.tag(latex="""E_j=E_{Jmax} |\cos(\pi \phi/\phi_0)|
E_0=-E_J+(1/2)\sqrt(8 E_J E_C)-E_C/4
E_1=-E_J+(3/2)\sqrt(8 E_J E_C)-(E_C/12)(6+6+3)
f=(E_1-E_0)/h
""")

# Per's definition: The detuning is positive for higher qubit frequency.

def detuning(flux_over_flux0):
    d_omega = 2*pi*(f0 - flux_parabola(flux_over_flux0))
    return d_omega
detuning.latex="2 \pi (f_0 - (E_1-E_0)/h)"

# Qubit reflection, for an incoming N_in phonons per second *at the qubit*
# This is Per's expression, but adjusted for Anton's definition of detuning.
def r_qubit(d_omega, N_in):
    P22 = empty(len(d_omega), len(N_in))
    for N_idx in range(0,len(N_in)):
        for d_omega_idx in range(1,len(d_omega)):
            dw = d_omega(d_omega_idx)
            N = N_in(N_idx)
            G = Gamma_tot
            g = gamma_10
            #S21 = S21_0
            #S22 = S22_0
            #tL = const.theta_L
            P22[d_omega_idx, N_idx] = -(G/(2.0*g))*(1+1j**dw/g)/(1 + dw**2/g**2 + 2.0*N/g)
            # r(d_omega_idx, N_idx) = (0.5*const.Gamma_ac/const.gamma_10)*(1-1i*d_omega(d_omega_idx)/const.gamma_10)./(1 + (-d_omega(d_omega_idx)./const.gamma_10).^2 +2* N_in(N_idx)/(const.gamma_10));
    return P22
r_qubit.latex=""
# Qubit transmission, for an incoming N_in phonons per second. Uses Anton's
# definition of detuning. Computing in regular frequencies
def t_qubit(d_omega, N_in):
    P21 = empty(len(d_omega), len(N_in))
    for N_idx in range(len(N_in)):
        for d_omega_idx in range(1,len(d_omega)):
            dw = d_omega(d_omega_idx)
            N = N_in(N_idx)
            G = Gamma_tot
            g = gamma_10;
            x = xi;

            P21[d_omega_idx, N_idx] = -sqrt(2.0*x*(1.0-x))*0.5*G*(g+1j*dw)/(dw**2 + g**2 + 4.0*x*g*N);
            #Omega = 2*sqrt(N_in(N_idx)*const.Gamma_el/(2*pi));
            #t(d_omega_idx, N_idx) = sqrt(0.5*const.Gamma_ac*const.Gamma_el)*(1i*d_omega(d_omega_idx) - const.Gamma_tot/2)./(d_omega(d_omega_idx).^2 + const.Gamma_tot^2/4 + Omega^2/2);
    return P21
t_qubit.latex=""
# Qubit transmission, for an incoming N_in phonons per second. Uses Anton's
# definition of detuning. Computing in regular frequencies
def t_qubit_Omega(d_omega, Omega, const):
    P21 = empty(len(d_omega), len(Omega))
    for O_idx in range(1,len(Omega)):
        for d_omega_idx in range(1,len(d_omega)):
            dw = d_omega(d_omega_idx)
            G = Gamma_tot
            g = gamma_10
            #x = xi
            P21[d_omega_idx, O_idx] = -(g+1j*dw)/(dw**2 + g**2 + (g/G)*Omega(O_idx)**2)
            #Omega = 2*sqrt(N_in(N_idx)*const.Gamma_el/(2*pi));
            #t(d_omega_idx, N_idx) = sqrt(0.5*const.Gamma_ac*const.Gamma_el)*(1i*d_omega(d_omega_idx) - const.Gamma_tot/2)./(d_omega(d_omega_idx).^2 + const.Gamma_tot^2/4 + Omega^2/2);
    return P21
t_qubit_Omega.latex=""

# Total reflection seen from the IDT, for a given qubit reflection coefficient (Per's P21)
def S11_IDT(r_qubit):
    # Per's Eq. 12
    r_tot = S11_0+ S21_0**2/(exp(-2j*theta_L)/r_qubit - S22_0)
    return r_tot
S11_IDT.latex=""

def S11_IDT_no_IDT_ref(r_qubit):
    # Per's Eq. 12
    r_tot = S21_0**2/(exp(-2j*theta_L)/r_qubit - S22_0)
    return r_tot
S11_IDT_no_IDT_ref.latex=""

# Total transmission from gate to IDT (Per's Eq. 22), for given qubit
# transmission and reflection coefficients (Per's P21 and P22).
def S21_gate(t_qubit, r_qubit):
    # Per's Eq. 22
    t_tot = T_CT*exp(1j*theta_CT) + t_qubit*S21_0*exp(1j*theta_L)/(1 - S22_0*r_qubit*exp(2j*theta_L))
    return t_tot
S21_gate.latex=""
# Total reflection for electrical power P_in applied to the IDT

def S11_IDT_with_qubit(d_omega, P_in):
    N_in = S21_0**2*P_in/hf0
    r_qub = r_qubit(d_omega, N_in)
    r_tot = S11_IDT(r_qub)
    return r_tot
S11_IDT_with_qubit.latex=""

# Total transmission for electrical power P_in applied to the gate
def S21_gate_with_qubit(delta_omega, P_in):
    N_in = P_in/hf0
    t_qub = t_qubit(delta_omega, N_in)
    r_qub = r_qubit(delta_omega, N_in)
    t_tot = S21_gate(t_qub, r_qub)
    return t_tot
S21_gate_with_qubit.latex=""
