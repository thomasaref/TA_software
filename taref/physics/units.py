# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 00:02:26 2016

@author: thomasaref
"""
#from taref.physics.fundamentals import dB, inv_dB, dB_pwr, inv_dB_pwr
from taref.core.log import log_debug
from numpy import log10, absolute

class unit_func(object):
    """base unit, returns value with no operation"""
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
        if isinstance(value, unit_func):
            if value.output_unit==self.output_unit:
                class new_unit(unit_func):
                    def func(self, val):
                        return self.func(value.func(val))

                    def inv_func(self, val):
                        return self.inv_func(value.inv_func(val))

                return new_unit(unit=self.unit, output_unit=value.output_unit, format_str=value.format_str)
        return self.inv_func(self.coercer(value))

    def func(self, value):
        return value

    def inv_func(self, value):
        return value

unitless=unit_func()

class mult_unit(unit_func):
    """multiplication returns unit in output_units, division returns output unit in units"""
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

fm= mult_unit(1.0e-15, unit="fm", output_unit="m")
pm= mult_unit(1.0e-12, unit="pm", output_unit="m")
nm= mult_unit(1.0e-9,  unit="nm", output_unit="m")
um= mult_unit(1.0e-6,  unit="um", output_unit="m", format_str=r"{0} $\mu$m")
mm= mult_unit(1.0e-3,  unit="mm", output_unit="m")
cm= mult_unit(0.01,    unit="cm", output_unit="m")
m=  mult_unit(1.0,     unit="m",  output_unit="m")
km= mult_unit(1.0e3,   unit="km", output_unit="m")

class dB_unit(unit_func):
    def func(self, value):
        return 10.0**(value/20.0)

    def inv_func(self, value):
        return 20.0*log10(absolute(value))



class dB_pwr_unit(unit_func):
    def func(self, value):
        return 10.0**(value/10.0)

    def inv_func(self, value):
        return 10.0*log10(absolute(value))

dB=dB_unit(unit="dB", output_unit="")
dB_pwr=dB_pwr_unit(unit="dB_pwr", output_unit="")
print  0.5/dB, -6*dB
print  0.5/dB_pwr, -6*dB_pwr

class dBm_unit(unit_func):
    def func(self, value):
        return value*dB_pwr*0.001

    def inv_func(self, value):
        return (value/0.001)/dB_pwr

dBm=dBm_unit(unit="dBm", output_unit="W")

fW= mult_unit(1.0e-15, unit="mW", output_unit="W")
pW= mult_unit(1.0e-12, unit="mW", output_unit="W")
nW= mult_unit(1.0e-9,  unit="mW", output_unit="W")
uW= mult_unit(1.0-6,   unit="mW", output_unit="W")
mW= mult_unit(1.0e-3,  unit="mW", output_unit="W")
W = mult_unit(1.0,     unit="W",  output_unit="W")

print 1/mW
print 1.0e-1*mW/dBm
dbmw=dBm/mW
print 0.0*dbmw
print 0.1/dbmw
Hz = mult_unit(1.0,    unit="Hz",  output_unit="Hz")
kHz= mult_unit(1.0e3,  unit="kHz", output_unit="Hz")
MHz= mult_unit(1.0e6,  unit="MHz", output_unit="Hz")
GHz= mult_unit(1.0e9,  unit="GHz", output_unit="Hz")
THz= mult_unit(1.0e12, unit="THz", output_unit="Hz")

unit_tuple=(fm, pm, nm, um, mm, cm, m, km,
            dB, dB_pwr, dBm,
            Hz, kHz, MHz, GHz, THz,
            pW, nW, uW, mW, W)
unit_dict=dict([(unit.unit, unit) for unit in unit_tuple])
print unit_dict