# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 11:08:19 2015

@author: thomasaref
"""
from a_Agent import SubAgent
from a_Backbone import updater
from atom.api import Enum, Int, Float, observe, Bool, Property, Str, List
from scipy.constants import epsilon_0 as eps0
from numpy import sqrt
from LOG_functions import log_debug
#from functools import wraps

#def updater(fn):
#    @wraps(fn)
#    def myfunc(self, change):
#        if not hasattr(myfunc, "callblock"):
#            myfunc.callblock=""
#        if change["name"]!=myfunc.callblock: # and change['type']!='create':
#            myfunc.callblock=change["name"]
#            templog=self.get_tag(change["name"], "log", True)
#            self.set_tag(change["name"], log=False)
#            fn(self, change)
#            self.set_tag(change["name"], log=templog)
#            myfunc.callblock=""
#    return myfunc


class IDT(SubAgent):

#    def __setattr__(self, name, value):
#        """extends __setattr__ to allow logging and data saving and automatic sending if tag send_now is true.
#        This is preferable to observing since it is called everytime the parameter value is set, not just when it changes."""
#        if name in self.all_params:
#            value=self.coercer(name, value)
#        super(IDT, self).__setattr__( name, value)
#        loglist=self.get_all_tags("log", True, True, self.all_params)
#        for param in loglist:
#            self.observe(param, self.log_changes)
#
#    def log_changes(self, change):
#        self.set_log(change["name"], change["value"])
#
    ft=Enum("double", "single").tag(desc="'double' for double fingered, 'single' for single fingered.")

    @property
    def mult(self):
        return {"double" : 2, "single" : 1}[self.ft]

    Np=Int(7).tag(desc="number of finger pairs. this should be at least 1", low=1)
    ef=Int(0).tag(desc="number of extra fingers to compensate for edge effect. Defaults to 0")
    a=Float(0.05e-6).tag(desc="width of fingers (um). same as gap generally.", unit="um")
    W=Float(25.0e-6).tag(desc="height of finger.", unit="um")
    g=Float(0.05e-6).tag(desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz", unit="um")
    eta=Float(0.5).tag(desc="metalization ratio")
    epsinf=Float(46*eps0)#eps0, 300*eps0, 46*eps0)
    Dvv=Float(2.4e-2).tag(desc="coupling strength: K^2/2", unit="%", unit_factor=1/100.0)#0.001e-2, 5e-2, 2.4e-2)
    v=Float(3488.0).tag(desc="speed of SAW", unit="m/s")
    lock_eta=Bool(True).tag(desc="boolean controlling if metalization ratio is locked")

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')


    f0=Float(5.0e9).tag(label="f0",
                unit="GHz",
                desc="Center frequency",
                reference="")

    lbda0=Float(1.0e-6).tag(label="lbda0",
                unit="um",
                desc="Center wavelength",
                reference="")

    Ct=Float().tag(label="Ct",
                   unit="F",
                   desc="Total capacitance of IDT",
                   reference="Morgan page 16/145")

    @Property
    def p(self):
        return self.a+self.g
    p.tag(desc="periodicity. this should be twice width for 50% metallization")

    @observe('a', 'g')
    @updater
    def _update_eta(self, change):
        if not self.lock_eta:
            self.eta=self.a/(self.a+self.g)

    @observe('g', 'eta')
    @updater
    def _update_a(self, change):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => a=g*eta/(1-eta)"""
        self.a=self.g*self.eta/(1-self.eta)

    @observe('a', 'eta')
    @updater
    def _update_g(self, change):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => g=a*(1/eta-1)"""
        self.g= self.a*(1.0/self.eta-1.0)

    @observe('ft', 'W', 'epsinf', 'Np')
    @updater
    def _update_Ct(self, change):
        m={"double": sqrt(2.0), "single": 1.0}[self.ft]
        self.Ct=m*self.W*self.epsinf*self.Np

    @observe('f0', 'v')
    @updater
    def _update_lbda0(self, change):
        self.lbda0=self.v/self.f0

    @observe('ft', 'eta', 'lbda0')
    @updater
    def _update_a2(self, change):
        m={"double": 2, "single": 1}[self.ft]
        self.a=self.eta*self.lbda0/(2*m)

    @observe('v', 'lbda0')
    @updater
    def _update_f0(self, change):
        self.f0=self.v/self.lbda0

    def _observe_material(self, change):
        if self.material=="STquartz":
            self.epsinf=5.6*eps0
            self.Dvv=0.06e-2
            self.v=3159.0
        elif self.material=='GaAs':
            self.epsinf=1.2e-10
            self.Dvv=0.035e-2
            self.v=2900.0
        elif self.material=='LiNbYZ':
            self.epsinf=46*eps0
            self.Dvv=2.4e-2
            self.v=3488.0
        elif self.material=='LiNb128':
            self.epsinf=56*eps0
            self.Dvv=2.7e-2
            self.v=3979.0
        elif self.material=='LiNbYZX':
            self.epsinf=46*eps0
            self.Dvv=0.8e-2
            self.v=3770.0
        else:
            print "Material not listed"

    def _default_material(self):
        return 'LiNbYZ' #'GaAs'

if __name__=="__main__":
    a=IDT()
    #print a._observe_a, a._observe_g#, a.update_p
    a.show()

#from scipy.constants import epsilon_0 as eps0
#from numpy import sqrt

#class IDT(EBL_Base):
#    df=Enum("single", "double").tag(desc="'double' for double fingered, 'single' for single fingered. defaults to double fingered")
#    Np=Int(36).tag(desc="number of finger pairs. this should be at least 1 and defaults to 36.")
#    ef=Int(0).tag(desc="number of extra fingers to compensate for edge effect. Defaults to 0")
#    a=Float(0.096).tag(unit="um", desc="width of fingers (um). same as gap generally. Adjusting relative to gap is equivalent to adjusting the bias in Beamer")
#    gap=Float(0.096).tag(unit="um", desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz")
#    offset=Float(0.5).tag(unit="um", desc="gap between electrode and end of finger. The vertical offset of the fingers. Setting this to zero produces a shorted reflector")
#    W=Float(25.5).tag(unit="um", desc="height of finger")
#    hbox=Float(20.0).tag(desc="height of electrode box")
#    wbox=Float(30.0).tag(desc="width of electrode box. Setting to 0.0 (default) makes it autoscaling so it matches the width of the IDT")
#
#    epsinf=Float()
#    Dvv=Float()
#    v=Float()
#    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')
#
#    def _observe_material(self, change):
#        if self.material=="STquartz":
#            self.epsinf=5.6*eps0
#            self.Dvv=0.06e-2
#            self.v=3159.0
#        elif self.material=='GaAs':
#            self.epsinf=1.2e-10
#            self.Dvv=0.035e-2
#            self.v=2900.0
#        elif self.material=='LiNbYZ':
#            self.epsinf=46*eps0
#            self.Dvv=2.4e-2
#            self.v=3488.0
#        elif self.material=='LiNb128':
#            self.epsinf=56*eps0
#            self.Dvv=2.7e-2
#            self.v=3979.0
#        elif self.material=='LiNbYZX':
#            self.epsinf=46*eps0
#            self.Dvv=0.8e-2
#            self.v=3770.0
#        else:
#            log_warning("Material not listed")
#
#    f0=Float().tag(label="f0",
#                unit="GHz",
#                desc="Center frequency",
#                reference="")
#
#    @observe('w', 'v', 'gap', 'df')
#    def _get_f0(self, change):
#        v,a, g=self.v, self.a*1e-6, self.gap*1e-6
#        p=g+a
#        if self.df:
#            lbda0=4*p
#        else:
#            lbda0=2*p
#        self.f0=v/lbda0/1.0e9
#
#
#    Ct=Property().tag(label="Ct",
#                   unit="F",
#                   desc="Total capacitance of IDT",
#                   reference="Morgan page 16/145")
#    #@observe('epsinf', 'h', 'Np', 'df')
#    def _get_Ct(self):
#        W, epsinf, Np=self.h*1e-6, self.epsinf, self.Np
#        if self.df=="double":
#            return sqrt(2.0)*W*epsinf*Np
#        return W*epsinf*Np
#
#    def _default_material(self):
#        return 'LiNbYZ' #'GaAs'