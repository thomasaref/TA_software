# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 16:49:13 2014

@author: thomasaref
"""

from scipy.constants import e, h, hbar, k as kB, epsilon_0 as eps0, pi
c_eta = 0.8
eps=1.2e-10

from numpy import exp

f0 = 4.8066e9     # The acoustic center frequency for the IDT
Ntr = 20   #number of finger pairs on transmon
Wtr = 25.0e-6
f1 = 5.0266e9# From Per's "SAW-model3.nb" Mathematica sheet
f2 = 6.2508e9#  From Per's "SAW-model3.nb" Mathematica sheet
T = 0.03  # Temperature in kelvin

#print "Fitted device constants:"
EJmax = 22.2e9*h
EC = 0.22e9*h
flux_per_volt = 2/(2.70+4.18) #Check this again from the cross section through the fluxmap
base_flux_offset = (0.343-0.2121)/2 #   The basic flux offset. Varies from meas. to meas though.

# The commented constants work quite well with everything except time domain data.
S11_0 = 0.5094
S21_0 = 0.28 # 0.26181; %0.270
S22_0 = 0.546# 0.55;
theta_L = 0.613349 # 0.64; %-2.55068; %-0.59;
Gamma_ac = 38.2059e6*2*pi# 38e6*2*pi;
Gamma_Phi = 0*2*pi
IDT_fridge_att = 83 # dB
gate_fridge_att = 83

T_CT = 0;
theta_CT = 1.0
xi = 0.003 # Resub chg from 0.003
Omega_el_squared_coeff = 1.2*3.9666e+21  # Omega^2 in angular frequency = omega_el_square_coeff * gate_power_at_fridgetop
crosstalk = 0.009*exp(1j*1.8*pi/4) # Complex S21 (gate to IDT) in amplitude units, with the phase related to that of the acoustic signal

Gamma_tot = (1+xi)*Gamma_ac
Gamma_el = xi*Gamma_tot
Gamma_tot = Gamma_ac + Gamma_el
gamma_10 = Gamma_tot/2 + Gamma_Phi
hf0 = h*f0
P_ac_to_N_in = (1/hf0)*abs(S21_0/(1+S22_0*exp(2j*theta_L)))**2

resonance_flux=-0.276160914385



material_dict=dict(
    LiNbYZ=dict(epsinf=46*eps0,
                Dvv=2.4e-2,
                v=3488.0),
    STquartz=dict(epsinf=5.6*eps0,
                  Dvv=0.06e-2,
                  v=3159.0),
    GaAs=dict(epsinf=1.2e-10,
              Dvv=0.035e-2,
              v=2900.0),
    LiNb128=dict(epsinf=56*eps0,
                 Dvv=2.7e-2,
                 v=3979.0),
    LiNbYZX=dict(epsinf=46*eps0,
                 Dvv=0.8e-2,
                 v=3770.0),
    MDCQuartz=dict(Dvv=0.2/2.0/100.0,
                      epsinf=5.0e-11,
                      v=3642.0),
    LiTaZY=dict(Dvv=0.93/2.0/100.0,
              epsinf=4.4e-10,
              v=3329.0),
    LiTaMDC=dict(Dvv=1.54/2.0/100.0,
               epsinf=4.4e-10,
               v=3370.0))

material="LiNbYZ"
Dvv=material_dict[material]['Dvv']
epsinf=material_dict[material]['epsinf']
v=material_dict[material]['v']


from atom.api import Float, Int, Dict, Bool, Enum, ContainerList, List, Typed, Unicode, Coerced, Constant, Range, FloatRange
from Atom_Boss import Master
from Atom_Base import Slave

class Master_Check(Master):
    name_checker=Dict()
    plot_list=List()

    def name_check(self, mydict):
        for key in filter(lambda aname: not aname.startswith('_'), mydict.keys()):
            if key not in self.name_checker.keys():
                print key+" not in members!"
            else:
                checkstr=""
                if mydict[key]!=self.name_checker[key][0]:
                    checkstr+=key+"Name mismatch!"
                else:
                    checkstr+=key+" verified"
                check_value=self.name_checker[key][1]
                if check_value!=None:
                    if (mydict[key]-check_value)/check_value<0.001:
                        checkstr+=" and "+ key+" matches check value"
                    else:
                        checkstr+=" and "+key+" does not match check value"
                print checkstr

_master_check=Master_Check()

class Check(Slave):
    def set_boss(self):
        self.boss=_master_check

    def __init__(self, **kwargs):
        super(Check, self).__init__(**kwargs)
        for key in self.members().keys():
            if key not in self.reserved_names:
                self.boss.name_checker.update({key: (getattr(self, key), self.get_tag(key, 'check_value'))})

#    def const_check(self, mydict):
#        for key, item in self.members.iteritems():
#            if key in mydict:
#                pass
#            else:
#                print key+" not in members!"
#    def name_check(self, mydict):
#        for key in filter(lambda aname: not aname.startswith('_'), mydict.keys()):
#            if key not in self.members().keys():
#                print key+" not in members!"
#            else:
#                checkstr=""
#                if mydict[key]!=getattr(self, key):
#                    checkstr+=key+"Name mismatch!"
#                else:
#                    checkstr+=key+" verified"
#                check_value=self.get_tag(key, 'check_value')
#                if check_value!=None:
#                    if (getattr(self, key)-check_value)/check_value<0.001:
#                        checkstr+=" and "+ key+" matches check value"
#                    else:
#                        checkstr+=" and "+key+" does not match check value"
#                    print checkstr

class Natural_Constants(Check):
    h=Constant(h).tag(desc="Planck's constant",
                    unit="",
                    check_value = 6.62606957e-34,
                    latex= 'h')

    hbar = Constant(hbar).tag(desc="Reduced Planck's constant",
                       check_value=1.054571726e-34,
                       unit='',
                       latex='\hbar')

    kB=Constant(kB).tag(desc="Boltzmann's constant",
                     check_value=1.3806488e-23,
                     unit='',
                     latex='k_B')

    e = Constant(e).tag(desc="charge of an electron",
                     check_value=1.60217657e-19,
                     unit="C",
                     latex='e')

    eps0 = Constant(eps0).tag(desc="permittivity of free space",
                       check_value=8.85418782e-12,
                       unit="F/m",
                       latex='\epsilon_0')

    pi = Constant(pi).tag(desc="ratio of circle's circumference to diameter",
                       check_value=3.141592654,
                       unit="",
                       latex='\pi')

natural_constants=Natural_Constants()

class Material_Parameters(Check):
    c_eta = Float(c_eta).tag(desc="The element factor",
                             check_value=0.8,
                             unit="for 50% metallization (Datta assuming sqrt(2) cancellation)",
                             latex='c_\eta')

    material = Enum(*sorted(material_dict.keys()))

    def _default_material(self):
        return material

    Dvv = FloatRange(0.00001, 10/100.0, Dvv).tag(
                label="Dvv",
                unit=None,
                LiNb=2.4/100.0,
                reference="Morgan pg 9",
                desc="Piezoelectric coupling constant",
                aka="K^2/2")

    epsinf=FloatRange(0.0001*1.0e-12, 500*8.85e-12, epsinf).tag(
                 label="epsilon_infty",
                 unit="F/m",
                 LiNb=46.0*8.85e-12,
                 reference="Morgan pg 9",
                 aka="C_S in Datta (50% metalization)",
                 desc="Capacitance for one finger pair")

    v = FloatRange(1000.0, 10000.0, v).tag(
              label="v",
              unit="m/s",
              desc="propagation velocity of SAW (free surface)") # propagation velocity for YZ lithium niobate --- page 9 Morgan's Book

    def _observe_material(self, change):
        self.Dvv=material_dict[self.material]['Dvv']
        self.epsinf=material_dict[self.material]['epsinf']
        self.v=material_dict[self.material]['v']

material_parameters=Material_Parameters()

class Device_Parameters(Check):
    f0 = Float(f0).tag(desc="The acoustic center frequency for the IDT",
                            unit='Hz',
                            check_value=4.8066e9,
                            latex='f_0')
    Ntr = Int(Ntr).tag(desc='number of finger pairs on transmon',
                        check_value=20,
                        latex='N_{tr}')
    Wtr = Float(Wtr).tag(desc='length of IDT fingers on transmon',
                        check_value=25.0e-6,
                        latex='W_{tr}')

    f1 = Float(f1).tag(desc= "From Per's 'SAW-model3.nb' Mathematica sheet",
                        check_value=5.0266e9,
                        unit='Hz',
                        latex='f_1')
    f2 = Float(f2).tag(desc="From Per's 'SAW-model3.nb' Mathematica sheet",
                        check_value=6.2508e9,
                        unit='Hz',
                        latex='f_1')
    T = Float(T).tag(desc="Temperature in kelvin",
                    check_value=0.03,
                    unit='K',
                    latex='T')

class Fitted_Device_Constants(Check):
    EJmax = Float(EJmax).tag(desc="Maximum Josephson energy",
                            check_value=22.2e9*h,
                            Unit='j',
                            latex='E_{Jmax}')

    EC = Float(EC).tag(desc="Charging energy",
                        check_value=0.22e9*h,
                        unit='J',
                        latex='E_C')

    flux_per_volt = Float(flux_per_volt).tag(desc="Check this again from the cross section through the fluxmap",
                    check_value=2/(2.70+4.18),
                    latex='flux per volt')

    base_flux_offset = Float(base_flux_offset).tag(desc="The basic flux offset. Varies from meas. to meas though.",
                        check_value=(0.343-0.2121)/2,
                        latex='base_flux_offset')#
#
## The commented constants work quite well with everything except time domain data.
    S11_0 = Float(S11_0).tag(desc='',
                            check_value=0.5094,
                            latex='S_{110}')
    S21_0 = Float(S21_0).tag(desc='',
                                check_value=0.28,
                                latex='S_{210}')# 0.26181; %0.270
    S22_0 = Float(S22_0).tag(check_value=0.546,
                                latex='S_{220}')# 0.55;
    theta_L = Float(theta_L).tag(check_value=0.613349,
                                latex='\theta_L') # 0.64; %-2.55068; %-0.59;
    Gamma_ac = Float(Gamma_ac).tag(check_value=38.2059e6*2*pi,
                                    latex='\Gamma_{ac}')# 38e6*2*pi;
    Gamma_Phi = Float(Gamma_Phi).tag(check_value=0*2*pi,
                                    latex='\Gamma_{\Phi}')
    IDT_fridge_att = Float(IDT_fridge_att).tag(check_value=83,
                                    unit='dB')
    gate_fridge_att = Float(gate_fridge_att).tag(check_value=83, unit='dB')

    T_CT = Float(T_CT).tag(desc="?", check_value=0)
    theta_CT = Float(theta_CT).tag(check_value=1.0)
    xi = Float(xi).tag(check_value=0.003, desc='Resub chg from 0.003')
    Omega_el_squared_coeff = Float(Omega_el_squared_coeff).tag(check_value=1.2*3.9666e+21,
         desc='Omega^2 in angular frequency = omega_el_square_coeff * gate_power_at_fridgetop')
#    crosstalk = Coerced(complex).tag(check_value=0.009*exp(1j*1.8*pi/4),
#                      desc='Complex S21 (gate to IDT) in amplitude units, with the phase related to that of the acoustic signal')
#    def _default_crosstalk(self):
#        return crosstalk

fitted_device_constants=Fitted_Device_Constants()
device_parameters=Device_Parameters()

class other_constants(Slave):
    data_base_directory=Unicode('/Users/martin/Dropbox/GaAsBestData/')


class derived_constants(Check):
    Gamma_el = Float(Gamma_el).tag(latex='\Gamma_{el}')
    Gamma_tot = Float(Gamma_tot).tag(latex='\Gamma')
    gamma_10 = Float(gamma_10).tag(latex='\gamma_{10}')
    hf0 = Float(h * f0).tag(latex='hf_0')
    P_ac_to_N_in = Coerced(complex)

    def _default_P_ac_to_N_in(self):
        return P_ac_to_N_in

    resonance_flux = Float(resonance_flux).tag(check_value=-0.276160914385)