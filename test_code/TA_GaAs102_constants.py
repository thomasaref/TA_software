# -*- coding: utf-8 -*-
"""
Created on Fri Feb  6 09:53:13 2015

@author: thomasaref
"""

from TA_Fundamentals import h, _document, _all_dict, _material_dict

Dvv=_material_dict["GaAs"]['Dvv']
epsinf=_material_dict["GaAs"]['epsinf']
v=_material_dict["GaAs"]['v']

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

_IDT_parameters=dict(f0 = dict(desc="fundamental frequency of IDT",
                                      check_value=4.8066e9,
                                      unit="Hz",
                                      latex='f_0'),
                     Ntr = dict(desc="number of finger pairs on transmon",
                                check_value=20,
                                unit="",
                                latex='N_{tr}'),
                     Wtr = dict(desc="length of fingers on transmon",
                                check_value=25.0e-6,
                                unit="m",
                                latex='W_{tr}'),
                     f1 = dict(desc="From Per's SAW-model3.nb Mathematica sheet",
                                check_value=5.0266e9,
                                unit="Hz",
                                latex='f_1'),
                     f2 = dict(desc="From Per's SAW-model3.nb Mathematica sheet",
                                check_value=6.2508e9,
                                unit="Hz",
                                latex='f_2'),
                     T = dict(desc="Temperature in Kelvin",
                                check_value=0.03,
                                unit="K",
                                latex='T'))

_all_dict.update(_IDT_parameters)                                      
if __name__=="__main__":
    _document(locals())