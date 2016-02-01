# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 21:05:03 2015

@author: thomasaref

Gathers all useful constants and functions in one location. Also initiates a default log_file.
"""

from scipy.constants import e, h, hbar, k as kB, epsilon_0 as eps0, pi
c_eta = 0.8

from numpy import (sin, cos, sqrt, exp, empty, mean, exp, log10, arange, array, ndarray, delete,
                   absolute, dtype, angle, amin, amax, linspace, zeros, shape)
from numpy.fft import fft, ifft
from numpy.linalg import eig
from atom.api import Float

def zero_arr(x):
    return zeros(shape(x))

def dB(x):
    return 20.0*log10(absolute(x))

def inv_dB(y):
    return 10.0**(y/20.0)

def dB_pwr(x):
    return 10.0*log10(absolute(x))

def inv_dB_pwr(y):
    return 10.0**(y/10.0)

PREFIX_DICT={"n":1.0e-9, "u":1.0e-6, "m":1.0e-3, "c":1.0e-2,
           "G":1.0e9, "M":1.0e6, "k":1.0e3,}

def UdBm2lin(unit="mW", unit_factor=1.0):
    unit_factor=PREFIX_DICT.get(unit[0], unit_factor)
    def NdBm2lin(y):
        return 0.001*inv_dB_pwr(y)/unit_factor
    NdBm2lin.unit=unit
    return NdBm2lin

dBm2lin=UdBm2lin()

def Ulin2dBm(unit="W", unit_factor=1.0):
    unit_factor=PREFIX_DICT.get(unit[0], unit_factor)
    def Nlin2dBm(x):
        return dB_pwr(x*unit_factor/0.001)
    Nlin2dBm.unit="dBm"
    return Nlin2dBm
lin2dBm=Ulin2dBm()

def dBm_Float(value=-100.0):
    return Float(value).tag(unit="dBm", display_func=dBm2lin)

def mW_Float(value=1.0e-10):
    return Float(value).tag(unit="mW", display_func=lin2dBm)

def magphase(y, response="Mag"):
        if dtype("complex128")==y.dtype:
            if response=="Phase":
                return angle(y)
            elif response=="Mag (dB)":
                return dB(y)
            else:
                return absolute(y)
        return y

def normalize(x):
    return (x-amin(x))/(amax(x)-amin(x))

def normalize_1d(x):
    return (x-amin(x, axis=1, keepdims=True))/(amax(x, axis=1, keepdims=True)-amin(x, axis=1, keepdims=True))

def sinc(X):
    """sinc function which doesn't autoinclude pi"""
    return sin(X)/X

def sinc_sq(X):
    """sinc squared which doesn't autoinclude pi"""
    return (sinc(X))**2

Tc=1.315 #critical temperature of aluminum
Delta=200.0e-6*e #gap of aluminum

#
#_material_dict=dict(
#    LiNbYZ=dict(epsinf=46.0*eps0,
#                Dvv=2.4e-2,
#                v=3488.0),
#    STquartz=dict(epsinf=5.6*eps0,
#                  Dvv=0.06e-2,
#                  v=3159.0),
#    GaAs=dict(epsinf=1.2e-10,
#              Dvv=0.035e-2,
#              v=2900.0),
#    LiNb128=dict(epsinf=56*eps0,
#                 Dvv=2.7e-2,
#                 v=3979.0),
#    LiNbYZX=dict(epsinf=46*eps0,
#                 Dvv=0.8e-2,
#                 v=3770.0),
#    MDCQuartz=dict(Dvv=0.2/2.0/100.0,
#                      epsinf=5.0e-11,
#                      v=3642.0),
#    LiTaZY=dict(Dvv=0.93/2.0/100.0,
#              epsinf=4.4e-10,
#              v=3329.0),
#    LiTaMDC=dict(Dvv=1.54/2.0/100.0,
#               epsinf=4.4e-10,
#               v=3370.0))
#
#_material="LiNbYZ"
#Dvv=_material_dict[_material]['Dvv']
#epsinf=_material_dict[_material]['epsinf']
#v=_material_dict[_material]['v']
#
#_material_parameters=dict(#material=dict(desc="material of substrate"),
#                          c_eta = dict(desc="The element factor",
#                                      check_value=0.8,
#                                      unit="for 50% metallization (Datta assuming sqrt(2) cancellation)",
#                                      latex='c_\eta'),
#                          Dvv = dict(unit="",
#                                     check_value=_material_dict["LiNbYZ"]['Dvv'],
#                                     reference="Morgan pg 9",
#                                     desc="Piezoelectric coupling constant",
#                                     aka="K^2/2",
#                                     latex="\Delta v/v"),
#                          epsinf=dict(unit="F/m",
#                                      check_value=_material_dict["LiNbYZ"]['epsinf'],
#                                      reference="Morgan pg 9",
#                                      aka="C_S in Datta (50% metalization)",
#                                      desc="Capacitance for one finger pair",
#                                      latex="\epsilon_\infty"),
#                          v=dict(unit="m/s",
#                                 desc="propagation velocity of SAW (free surface)",
#                                 check_value=_material_dict["LiNbYZ"]['v'],
#                                 latex="v_f")) # propagation velocity for YZ lithium niobate --- page 9 Morgan's Book
#
#_natural_constants=dict(h=dict(desc="Planck's constant",
#                              unit="",
#                              check_value = 6.62606957e-34,
#                              latex= 'h'),
#                       hbar = dict(desc="Reduced Planck's constant",
#                                   check_value=1.054571726e-34,
#                                   unit='',
#                                   latex='\hbar'),
#                       kB=dict(desc="Boltzmann's constant",
#                               check_value=1.3806488e-23,
#                               unit='',
#                               latex='k_B'),
#                       e =dict(desc="charge of an electron",
#                               check_value=1.60217657e-19,
#                               unit="C",
#                               latex='e'),
#                       eps0 = dict(desc="permittivity of free space",
#                                   check_value=8.85418782e-12,
#                                   unit="F/m",
#                                   latex='\epsilon_0'),
#                       pi = dict(desc="ratio of circle's circumference to diameter",
#                                 check_value=3.141592654,
#                                 unit="",
#                                 latex='\pi'))
#_fundamental_functions=dict(cos=dict(desc="cosine",
#                                     latex='\cos'),
#                            sin=dict(desc="sine",
#                                     latex='\sin'),
#                            exp=dict(desc="exponent",
#                                     latex='\exp'),
#                            sqrt=dict(desc="square root",
#                                      latex='\sqrt'),
#                            empty=dict(desc="makes empty array",
#                                       latex='empty'),
#                            mean=dict(desc="mean",
#                                      latex='mean'),
#                            fft=dict(desc="fast fourier transform",
#                                      latex='fft'),
#                            ifft=dict(desc="inverse fast fourier transform",
#                                      latex='fft'),
#                            absolute=dict(desc="absolute value",
#                                      latex='|{0}|'),
#                            angle=dict(desc="angle of complex number",
#                                      latex='fft'),
#                            log10=dict(desc="logarithm base 10",
#                                      latex='\log'))
#
#class _func_log(object):
#    """decorator class to allow function logging"""
#    def update_log(self, log_str):
#        log_info(log_str)
#
#    def set_run_params(self, arg_count):
#        self.run_params=list(self.f.func_code.co_varnames[0:arg_count])
#
#    def __init__(self, f):
#        self.f = f
#        self.set_run_params(self.f.func_code.co_argcount)
#        self.func_name=self.f.func_name
#        self.metadata=dict()
#
#    def __call__(self, *args, **kwargs):
#        self.update_log("RAN: {name}".format(
#                 name=self.f.func_name))#, run_params=self.run_params))
#        return self.f(*args, **kwargs)
#
#    def tag(self, **kwargs):
#        self.metadata.update(**kwargs)
#
#    def get_tag(self, key, none_value=""):
#        """gets tag key of parameter name and returns none_value if tag does not exist. very useful function"""
#        try:
#            return self.metadata[key]
#        except:
#            return none_value
#
#@_func_log
#def mean_and_remove_offset(raw_data, offset, dimension=2):
#    """Average over all flux values (it's a very narrow range)"""
#    return mean(raw_data, dimension) - offset
#mean_and_remove_offset.tag(latex="mean({0}, {2})-{1}")
#
#@_func_log
#def dB2amp(trace_dB):
#    """converts dB to amplitude"""
#    return 10.0**(trace_dB/20.0)
#dB2amp.tag(desc='dB to amplitude')
#
#@_func_log
#def dB(x):
#    """returns x in dB (factor of 20)"""
#    return 20.0*log10(absolute(x))
#dB.tag(desc='amplitude to dB')
#
##@_func_log
##def magphase(y, response="Mag"):
##    "returns mag, phase, mag dB respectively"""
##    if dtype("complex128")==y.dtype:
##        if response=="Phase":
##            return angle(y)
##        elif response=="Mag (dB)":
##            return dB(y)
##        else:
##            return absolute(y)
##    return y
#
#@_func_log
#def flux_parabola(flux_over_flux0, EJmax, EC):
#    """Omega_10 in regular frequency unit"""
#    EJ = EJmax*abs(cos(pi*flux_over_flux0))
#    E0 = -EJ + sqrt(8*EJ*EC)*0.5 - (EC/4)
#    E1 = -EJ + sqrt(8*EJ*EC)*1.5 - (EC/12.0)*(6+6+3)
#    return (E1-E0)/h
#flux_parabola.tag(latex="""E_j=E_{Jmax} |\cos(\pi \phi/\phi_0)|
#E_0=-E_J+(1/2)\sqrt(8 E_J E_C)-E_C/4
#E_1=-E_J+(3/2)\sqrt(8 E_J E_C)-(E_C/12)(6+6+3)
#f=(E_1-E_0)/h
#""")
#
#@_func_log
#def detuning(flux_over_flux0, f0):
#    """Per's definition: The detuning is positive for higher qubit frequency."""
#    d_omega = 2*pi*(f0 - flux_parabola(flux_over_flux0))
#    return d_omega
#detuning.tag(latex="2 \pi (f_0 - (E_1-E_0)/h)")
#
#
#@_func_log
#def r_qubit(d_omega, N_in, G, g):
#    """ Qubit reflection, for an incoming N_in phonons per second *at the qubit*
#        This is Per's expression, but adjusted for Anton's definition of detuning."""
#    P22 = empty(len(d_omega), len(N_in))
#    for N_idx in range(0,len(N_in)):
#        for d_omega_idx in range(1,len(d_omega)):
#            dw = d_omega(d_omega_idx)
#            N = N_in(N_idx)
##            G = Gamma_tot
##            g = gamma_10
#            #S21 = S21_0
#            #S22 = S22_0
#            #tL = const.theta_L
#            P22[d_omega_idx, N_idx] = -(G/(2.0*g))*(1+1j**dw/g)/(1 + dw**2/g**2 + 2.0*N/g)
#            # r(d_omega_idx, N_idx) = (0.5*const.Gamma_ac/const.gamma_10)*(1-1i*d_omega(d_omega_idx)/const.gamma_10)./(1 + (-d_omega(d_omega_idx)./const.gamma_10).^2 +2* N_in(N_idx)/(const.gamma_10));
#    return P22
#r_qubit.tag(desc='qubit reflection')
#
#@_func_log
#def t_qubit(d_omega, N_in, G, g, x):
#    """Qubit transmission, for an incoming N_in phonons per second. Uses Anton's
#       definition of detuning. Computing in regular frequencies"""
#    P21 = empty(len(d_omega), len(N_in))
#    for N_idx in range(len(N_in)):
#        for d_omega_idx in range(1,len(d_omega)):
#            dw = d_omega(d_omega_idx)
#            N = N_in(N_idx)
##            G = Gamma_tot
##            g = gamma_10
##            x = xi
#
#            P21[d_omega_idx, N_idx] = -sqrt(2.0*x*(1.0-x))*0.5*G*(g+1j*dw)/(dw**2 + g**2 + 4.0*x*g*N);
#            #Omega = 2*sqrt(N_in(N_idx)*const.Gamma_el/(2*pi));
#            #t(d_omega_idx, N_idx) = sqrt(0.5*const.Gamma_ac*const.Gamma_el)*(1i*d_omega(d_omega_idx) - const.Gamma_tot/2)./(d_omega(d_omega_idx).^2 + const.Gamma_tot^2/4 + Omega^2/2);
#    return P21
#
#@_func_log
#def t_qubit_Omega(d_omega, Omega, G, g):
#    """ Qubit transmission, for an incoming N_in phonons per second. Uses Anton's
#     definition of detuning. Computing in regular frequencies"""
#    P21 = empty(len(d_omega), len(Omega))
#    for O_idx in range(1,len(Omega)):
#        for d_omega_idx in range(1,len(d_omega)):
#            dw = d_omega(d_omega_idx)
#            #G = Gamma_tot
#            #g = gamma_10
#            #x = xi
#            P21[d_omega_idx, O_idx] = -(g+1j*dw)/(dw**2 + g**2 + (g/G)*Omega(O_idx)**2)
#            #Omega = 2*sqrt(N_in(N_idx)*const.Gamma_el/(2*pi));
#            #t(d_omega_idx, N_idx) = sqrt(0.5*const.Gamma_ac*const.Gamma_el)*(1i*d_omega(d_omega_idx) - const.Gamma_tot/2)./(d_omega(d_omega_idx).^2 + const.Gamma_tot^2/4 + Omega^2/2);
#    return P21
#
#@_func_log
#def S11_IDT(r_qubit, S11_0, S21_0, theta_L, S22_0):
#    """Total reflection seen from the IDT, for a given qubit reflection coefficient (Per's P21) using Per's Eq. 12"""
#    r_tot = S11_0+ S21_0**2/(exp(-2j*theta_L)/r_qubit - S22_0)
#    return r_tot
#S11_IDT.latex=""
#
#@_func_log
#def S11_IDT_no_IDT_ref(r_qubit, S21_0, theta_L, S22_0):
#    """using Per's Eq. 12"""
#    r_tot = S21_0**2/(exp(-2j*theta_L)/r_qubit - S22_0)
#    return r_tot
#
#@_func_log
#def S21_gate(t_qubit, r_qubit, T_CT, theta_CT, theta_L, S21_0, S22_0):
#    """Total transmission from gate to IDT (Per's Eq. 22), for given qubit
#      transmission and reflection coefficients (Per's P21 and P22)."""
#    t_tot = T_CT*exp(1j*theta_CT) + t_qubit*S21_0*exp(1j*theta_L)/(1 - S22_0*r_qubit*exp(2j*theta_L))
#    return t_tot
#
#@_func_log
#def S11_IDT_with_qubit(d_omega, P_in, hf0, S21_0):
#    """Total reflection for electrical power P_in applied to the IDT"""
#    N_in = S21_0**2*P_in/hf0
#    r_qub = r_qubit(d_omega, N_in)
#    r_tot = S11_IDT(r_qub)
#    return r_tot
#
#@_func_log
#def S21_gate_with_qubit(delta_omega, P_in, hf0):
#    """Total transmission for electrical power P_in applied to the gate"""
#    N_in = P_in/hf0
#    t_qub = t_qubit(delta_omega, N_in)
#    r_qub = r_qubit(delta_omega, N_in)
#    t_tot = S21_gate(t_qub, r_qub)
#    return t_tot
#
#_all_dict=dict()
#_all_dict.update(_material_parameters)
#_all_dict.update(_natural_constants)
#_all_dict.update(_fundamental_functions)
#
#def _document(_mydict):
#    _func_list=[]
#    _var_list=[]
#    _notdoc_list=[]
#    _ufunc_list=[]
#    for key in filter(lambda aname: not aname.startswith('_'), _mydict.keys()):
#        value=_mydict[key]
#        if type(value) not in (type,):# and not isinstance(value, object):
#            if key not in _all_dict.keys():
#                if isinstance(value, _func_log):
##                    print key #+": "+value.f.func_doc
#                    _func_list.append(key)
#                else:
##                    print key+" not documented!"
#                    _notdoc_list.append(key)
#            else:
#                if type(value) in (float, int, str, unicode):
##                    print key, value, _all_dict[key]
#                    _var_list.append(key)
#                #elif type(value) in (list, ndarray):
#                #    print value, len(value)
#                else:
#                    _ufunc_list.append(key)
##                    print key, _all_dict[key] #, value.__doc__ #__name__
#
#    print "Constants:"
#    for key in _var_list:
#        print key, _mydict[key], _all_dict[key]['desc']
#
#    print "\nPredef Functions:"
#    for key in _ufunc_list:
#        print key, _all_dict[key]['desc']
#    print "\nFunctions:"
#    for key in _func_list:
#        print key, _mydict[key].get_tag('desc')
#    print "\nNot documented"
#    for key in _notdoc_list:
#        print key
#
#
#                #if isinstance(func, FunctionType):
#                #    setattr(self, key, log(func))
#if __name__=="__main__":
##    _mydict=locals()
#    from numpy import ufunc, ndarray
#    from types import FunctionType
#    _document(locals())
