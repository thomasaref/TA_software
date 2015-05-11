# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 11:08:19 2015

@author: thomasaref
"""
from Atom_Base import Slave
from atom.api import Enum, Int,Range, FloatRange 
class IDT(Slave):
    df=Enum(False, True).tag(desc="'double' for double fingered, 'single' for single fingered. defaults to double fingered")
    Np=Range(1, 1000, 7).tag(desc="number of finger pairs. this should be at least 1 and defaults to 36.")
    ef=Range(0, 100, 0).tag(desc="number of extra fingers to compensate for edge effect. Defaults to 0")
    a=Float(0.05).tag(desc="width of fingers (um). same as gap generally.")
    p=Float(0.1).tag(desc="periodicity. this should be twice width for 50% metallization)
    W=FloatRange(1, 500, 25.0).tag(desc="height of finger. Equivalenbt to W")
    
    epsinf=FloatRange(eps0, 300*eps0, 46*eps0)
    Dvv=FloatRange(0.001e-2, 5e-2, 2.4e-2)
    v=FloatRange()
    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')

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

    @observe('w', 'v', 'gap', 'df')
    def _get_f0(self, change):
        v,w, g=self.v, self.w*1e-6, self.gap*1e-6
        p=g+w
        if self.df:
            lbda0=4*p
        else:
            lbda0=2*p
        self.f0=v/lbda0/1.0e9


    Ct=Property().tag(label="Ct",
                   unit="F",
                   desc="Total capacitance of IDT",
                   reference="Morgan page 16/145")
    #@observe('epsinf', 'h', 'Np', 'df')
    def _get_Ct(self):
        W, epsinf, Np=self.h*1e-6, self.epsinf, self.Np
        if self.df:
            return sqrt(2.0)*W*epsinf*Np
        return W*epsinf*Np

#    idt=Instance(EBLIDT)

#    @observe("df, Np, ef, w, gap, offset, h, hbox, wbox, xidt, yidt, layer, trconnect")
#    def update_IDT(self):
#         self.idt=EBLIDT(df=self.df, Np=self.Np, ef=self.ef, w=self.w, gap=self.gap, offset=self.offset, h=self.h,
#                         hbox=self.hbox, wbox=self.wbox, xidt=self.xidt, yidt=self.yidt, layer=self.layer, trconnect=self.trconnect)


#    def _default_idt(self):
#        return EBLIDT(df=self.df, Np=self.Np, ef=self.ef, w=self.w, gap=self.gap, offset=self.offset, h=self.h,
#                         hbox=self.hbox, wbox=self.wbox, xidt=self.xidt, yidt=self.yidt, layer=self.layer, trconnect=self.trconnect)

    def _default_material(self):
        return 'LiNbYZ' #'GaAs'
