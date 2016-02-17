# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 00:02:26 2016

@author: thomasaref
"""
from taref.physics.fundamentals import dB, inv_dB, dB_pwr, inv_dB_pwr
from taref.core.log import log_debug

class unit_func(object):
    def __init__(self, unit="", format_str=None, coercer=float, output_unit=""):
        self.unit=unit
        if format_str is None:
            format_str=r"{0} "+unit
        else:
            format_str=r"{0} "+format_str
        self.format_str=format_str
        self.coercer=coercer
        self.output_unit=output_unit

    def __rmul__(self, value):
        if value is None:
            return value
        return self.func(self.coercer(value))

    def __rdiv__(self, value):
        if value is None:
            return value
        return self.inv_func(self.coercer(value))


class mult_unit(unit_func):
    def __init__(self, unit_factor=None, unit="", format_str=None, coercer=float, output_unit=""):
        self.unit_factor=unit_factor
        super(mult_unit, self).__init__(unit=unit, format_str=format_str, coercer=coercer, output_unit=output_unit)

    def __rmul__(self, value):
        if self.unit_factor is None:
            return value
        return super(mult_unit, self).__rmul__(value)

    def __rdiv__(self, value):
        if self.unit_factor is None:
            return value
        return super(mult_unit, self).__rdiv__(value)

    def func(self, value):
        return value*self.unit_factor

    def inv_func(self, value):
        return value/self.unit_factor
        
mm= mult_unit(0.001, unit="mm", output_unit="m")
cm= mult_unit(0.01,  unit="cm", output_unit="m")
m=  mult_unit(1.0,   unit="m",  output_unit="m")

unit_dict={"mm" : mm,
           "m"  : m}

class dB_unit(unit_func):
    def func(self, value):
        return dB(value)

    def inv_func(self, value):
        return inv_dB(value)

dBu=dB_unit(unit="dB")

print  0.5*dBu, -6/dBu
class dBm_unit(unit_func):
    def func(self, value):
        return 0.001*inv_dB_pwr(value)#/self.unit_factor

    def inv_func(self, value):
        return dB_pwr(value/0.001)

dBm=dBm_unit(unit="dBm", output_unit="W")
mW= mult_unit(0.001, unit="mW", output_unit="W")

print 1/mW
print 1*mW#/dBm