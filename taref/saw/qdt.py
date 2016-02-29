# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:05:48 2016

@author: thomasaref
"""

from taref.saw.idt import IDT
from taref.saw.qubit import Qubit
from taref.core.extra_setup import tagged_property
from atom.api import Float, Int
from taref.core.universal import Array
from taref.physics.fundamentals import (eps0, sqrt, pi, Delta, hbar, e, h, ndarray, array, eig, delete,
                                        sin, sinc_sq, sinc, linspace, zeros, absolute, cos, arange)

class QDT(IDT, Qubit):
    base_name="QDT"

    @tagged_property(desc="""Coupling at IDT center frequency""", unit="GHz", label="Coupling at center frequency", tex_str=r"$G_{f0}$")
    def G_f0(self, Np, K2, f0):
        return 0.45*Np*K2*f0

    @tagged_property(desc="""Coupling adjusted by sinc sq""", unit="GHz", tex_str=r"$G_f$", label="frequency adjusted coupling")
    def G_f(self, G_f0, Np, fq, f0):
        #return G_f0*sinc_sq(Np*pi*(fq-f0)/f0)
        return absolute(G_f0*sinc(Np*pi*(fq-f0)/f0))

    ng=Float(0.5).tag(desc="charge on gate line")
    Nstates=Int(50).tag(desc="number of states to include in mathieu approximation. More states is better approximation")
    order=Int(3)
    EkdivEc=Array().tag(unit2="Ec")

    @tagged_property(desc="shunt capacitance of QDT", unit="fF")
    def Cq(self, Ct):
        return Ct

    @Cq.fget.setter
    def _get_Ct(self, Cq):
        return Cq

if __name__=="__main__":
    a=QDT()
    a.show()