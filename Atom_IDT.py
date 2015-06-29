# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 11:08:19 2015

@author: thomasaref
"""
from a_Base import Base
from atom.api import Enum, Int, Float, observe, Bool#, Property 
from scipy.constants import epsilon_0 as eps0
from numpy import sqrt

class IDT(Base):
    finger_type=Enum("double", "single").tag(desc="'double' for double fingered, 'single' for single fingered. defaults to double fingered")
    Np=Int(36) #1, 1000, 7).tag(desc="number of finger pairs. this should be at least 1 and defaults to 36.")
    ef=Int()#0, 100, 0).tag(desc="number of extra fingers to compensate for edge effect. Defaults to 0")
    a=Float(0.05).tag(desc="width of fingers (um). same as gap generally.")
    p=Float(0.1).tag(desc="periodicity. this should be twice width for 50% metallization")
    W=Float(25.0)#1, 500, 25.0).tag(desc="height of finger. Equivalenbt to W")
    
    epsinf=Float(46*eps0)#eps0, 300*eps0, 46*eps0)
    Dvv=Float(2.4e-2)#0.001e-2, 5e-2, 2.4e-2)
    v=Float(3488.0)

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')

    _update=Bool(False).tag(private=True)
    
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

    f0=Float().tag(label="f0",
                unit="GHz",
                desc="Center frequency",
                reference="")

    @observe('a', 'v', 'p', 'df')
    def _get_f0(self, change):
        v,p=self.v, self.p*1e-6
        #p=g+w
        if self.finger_type=="double":
            lbda0=4*p
        else:
            lbda0=2*p
        self.f0=v/lbda0/1.0e9


    Ct=Float().tag(label="Ct",
                   unit="F",
                   desc="Total capacitance of IDT",
                   reference="Morgan page 16/145")

    @observe('epsinf', 'W', 'Np', 'df')
    def _get_Ct(self, change):
        W, epsinf, Np=self.W*1e-6, self.epsinf, self.Np
        if self.finger_type=="double":
            self.Ct=sqrt(2.0)*W*epsinf*Np
        else:
            self.Ct=W*epsinf*Np

    def _default_material(self):
        return 'LiNbYZ' #'GaAs'

if __name__=="__main__":
    a=IDT()
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