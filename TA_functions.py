# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 16:06:40 2015

@author: thomasaref
"""

from atom.api import Callable
from TA_func_defs import (Check, mean_and_remove_offset, flux_parabola, detuning, r_qubit, t_qubit, t_qubit_Omega,
    S11_IDT, S21_gate, S11_IDT_with_qubit, S21_gate_with_qubit, S11_IDT_no_IDT_ref, _master_check)

class Helper_Functions(Check):
    mean_and_remove_offset=Callable(mean_and_remove_offset).tag(**mean_and_remove_offset.metadata)
    flux_parabola=Callable(flux_parabola).tag(desc='Omega_10 in regular frequency units', **flux_parabola.metadata)
    detuning = Callable(detuning)
    r_qubit = Callable(r_qubit)
    t_qubit = Callable(t_qubit)
    t_qubit_Omega = Callable(t_qubit_Omega)

    S11_IDT = Callable(S11_IDT)
    S21_gate = Callable(S21_gate)
    S11_IDT_with_qubit = Callable(S11_IDT_with_qubit)
    S21_gate_with_qubit = Callable(S21_gate_with_qubit)
    S11_IDT_no_IDT_ref = Callable(S11_IDT_no_IDT_ref)

helper_functions=Helper_Functions()
print helper_functions.get_member('flux_parabola').metadata

if __name__=="__main__":
    print locals()
    if 0:
        _master_check.name_check(locals())