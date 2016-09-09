# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 00:02:26 2016

@author: thomasaref
"""
from taref.core.log import log_debug
from numpy import log10, absolute, pi
from taref.physics.fundamentals import h, e

class unit_func(object):
    """base unit, returns value with no operation"""
    def __init__(self, unit="", format_str=None, output_unit="", output_format_str=None):
        self.unit=unit
        if format_str is None:
            format_str=unit
        self.format_str=format_str
        self.output_unit=output_unit
        if output_format_str is None:
            output_format_str=output_unit
        self.output_format_str=output_format_str

    def show_unit(self, value, precision=3):
        """a utility function for displaying a value with unit added on as a string"""
        form_str="{0:." + str(precision) + "g}"
        if self.format_str=="":
            return form_str.format(value)
        form_str+=" {1}"
        return form_str.format(value, self.format_str)

    def __rmul__(self, value):
        if value is None:
            return value
        return self.func(value)

    def __rdiv__(self, value):
        if value is None:
            return value
        if isinstance(value, unit_func):
            if value.output_unit==self.output_unit:
                class new_unit(unit_func):
                    def func(obj, val):
                        return self.inv_func(value.func(val))
                    def inv_func(obj, val):
                        return value.inv_func(self.func(val))
                return new_unit(unit=value.unit, output_unit=self.unit,
                                format_str=value.format_str[4:], output_format_str=self.format_str[4:])
        return self.inv_func(value)

    def func(self, value):
        return value

    def inv_func(self, value):
        return value

unitless=unit_func()

class mult_unit(unit_func):
    """multiplication returns unit in output_units, division returns output unit in units"""
    def __init__(self, unit_factor=None, unit="", format_str=None, output_unit=""):
        self.unit_factor=unit_factor
        super(mult_unit, self).__init__(unit=unit, format_str=format_str, output_unit=output_unit)

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
upi= mult_unit(pi, unit="pi",  format_str=r"$\pi$")
fm= mult_unit(1.0e-15, unit="fm", output_unit="m")
pm= mult_unit(1.0e-12, unit="pm", output_unit="m")
nm= mult_unit(1.0e-9,  unit="nm", output_unit="m")
um= mult_unit(1.0e-6,  unit="um", output_unit="m", format_str=r"$\mu$m")
mm= mult_unit(1.0e-3,  unit="mm", output_unit="m")
cm= mult_unit(0.01,    unit="cm", output_unit="m")
m=  unit_func(unit="m",  output_unit="m")
km= mult_unit(1.0e3,   unit="km", output_unit="m")

um_sq=mult_unit(unit_factor=1.0e-12, unit="um^2", output_unit="m^2", format_str=r"$\mu$m$^2$")

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

class dBm_unit(unit_func):
    def func(self, value):
        return value*dB_pwr*0.001

    def inv_func(self, value):
        return (value/0.001)/dB_pwr

dBm=dBm_unit(unit="dBm", output_unit="W")

fW= mult_unit(1.0e-15, unit="fW", output_unit="W")
pW= mult_unit(1.0e-12, unit="pW", output_unit="W")
nW= mult_unit(1.0e-9,  unit="nW", output_unit="W")
uW= mult_unit(1.0e-6,   unit="uW", output_unit="W")
mW= mult_unit(1.0e-3,  unit="mW", output_unit="W")
W = unit_func(unit="W",  output_unit="W")

V = unit_func(unit="V",  output_unit="V")
eV=mult_unit(unit_factor=1.0*e, unit="eV", output_unit="J")
ueV=mult_unit(unit_factor=1.0e-6*e, unit="ueV", output_unit="J")


fF= mult_unit(1.0e-15, unit="fF", output_unit="F")
F = unit_func(unit="F",  output_unit="F")

nA= mult_unit(1.0e-9,  unit="nA", output_unit="A")
A = unit_func(unit="A",  output_unit="A")

Ohm=  unit_func(unit="Ohm",  output_unit="Ohm")
kOhm= mult_unit(1.0e3,   unit="kOhm", output_unit="Ohm")


m_per_s=unit_func(unit="m/s", output_unit="m/s")

Hz = unit_func(unit="Hz",  output_unit="Hz")
kHz= mult_unit(1.0e3,  unit="kHz", output_unit="Hz")
MHz= mult_unit(1.0e6,  unit="MHz", output_unit="Hz")
GHz= mult_unit(1.0e9,  unit="GHz", output_unit="Hz")
THz= mult_unit(1.0e12, unit="THz", output_unit="Hz")

hGHz=mult_unit(unit_factor=1.0e9*h, unit="hGHz", output_unit="J")
hHz = unit_func(unit="hHz",  output_unit="J")
#J = unit_func(unit="hHz",  output_unit="J")

dBm_per_mW=dBm/mW
dBm_per_mW.unit="dBm/mW"

K = unit_func(unit="K",  output_unit="K")

percent=mult_unit(1.0/100.0, unit="%", output_unit="", format_str="\%")

UNIT_TUPLE=(fm, pm, nm, um, mm, cm, m, km,
            um_sq,
            dB, dB_pwr, dBm, dBm_per_mW,
            Hz, kHz, MHz, GHz, THz,
            hHz, hGHz,
            fW, pW, nW, uW, mW, W,
            V,
            eV, ueV,
            F,fF,
            Ohm, kOhm,
            A, nA,
            m_per_s,
            K,
            percent, upi)
UNIT_DICT=dict([(unit.unit, unit) for unit in UNIT_TUPLE])
#UNIT_DICT["%"]=percent
#UNIT_DICT["m/s"]=m_per_s
#UNIT_DICT["dBm/mW"]=dBm_per_mW

if __name__=="__main__":
    print  0.5/dB, -6*dB
    print  0.5/dB_pwr, -6*dB_pwr

    print unit_dict
    print 1/mW
    print 1.0e-1*mW/dBm
    dbmw=dBm/mW
    print dbmw.unit, dbmw.output_unit, dbmw.format_str
    print -20*dBm/mW
    print 0.1/(dBm/mW)
