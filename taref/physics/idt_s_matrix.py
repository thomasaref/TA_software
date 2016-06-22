# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:20:20 2016

@author: thomasaref
"""

from taref.core.api import SProperty, private_property
from taref.physics.idt import IDT

class IDT_S_Matrix(IDT):
    S11=SProperty()
    @S11.getter
    def _get_S11(self, f):
        return self.get_fix("S11", f)

    @private_property
    def fixed_S11(self):
        return self.fixed_S[0]

    S12=SProperty()
    @S12.getter
    def _get_S12(self, f):
        return self.get_fix("S12", f)

    @private_property
    def fixed_S12(self):
        return self.fixed_S[1]

    S13=SProperty()
    @S13.getter
    def _get_S13(self, f):
        return self.get_fix("S13", f)

    @private_property
    def fixed_S13(self):
        return self.fixed_S[2]

    S21=SProperty()
    @S21.getter
    def _get_S21(self, f):
        return self.get_fix("S21", f)

    @private_property
    def fixed_S21(self):
        return self.fixed_S[3]

    S22=SProperty()
    @S22.getter
    def _get_S22(self, f):
        return self.get_fix("S22", f)

    @private_property
    def fixed_S22(self):
        return self.fixed_S[4]

    S23=SProperty()
    @S23.getter
    def _get_S23(self, f):
        return self.get_fix("S23", f)

    @private_property
    def fixed_S23(self):
        return self.fixed_S[5]

    S31=SProperty()
    @S31.getter
    def _get_S31(self, f):
        return self.get_fix("S31", f)

    @private_property
    def fixed_S31(self):
        return self.fixed_S[6]

    S32=SProperty()
    @S32.getter
    def _get_S32(self, f):
        return self.get_fix("S32", f)

    @private_property
    def fixed_S32(self):
        return self.fixed_S[7]

    S33=SProperty()
    @S33.getter
    def _get_S33(self, f):
        return self.get_fix("S33", f)

    @private_property
    def fixed_S33(self):
        return self.fixed_S[8]