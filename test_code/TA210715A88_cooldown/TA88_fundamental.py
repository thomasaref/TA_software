# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:08:41 2016

@author: thomasaref
"""

from taref.saw.qdt import QDT
from taref.saw.idt import IDT
from taref.core.atom_extension import get_tag
from taref.filer.read_file import Read_HDF5
from taref.filer.filer import Folder
from taref.core.agent import Agent
from atom.api import Float

class TA88_Read(Read_HDF5):
    def _default_folder(self):
        return Folder(base_dir="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216", quality="", main_dir="Data_0221")

class TA88_Fund(Agent):
    fridge_atten=Float(60)
    fridge_gain=Float(45)


qdt=QDT(material='LiNbYZ',
        ft="double",
        a=80.0e-9,
        Np=9,
        Rn=3780.0, #(3570.0+4000.0)/2.0,
        W=25.0e-6,
        eta=0.5,
        flux_factor=0.2945,
        voltage=1.21,
        offset=0.0)

idt=IDT(material='LiNbYZ',
        ft="double",
        Np=36,
        W=25.0e-6,
        eta=0.5,
        a=96.0e-9)

if __name__=="__main__":
    print get_tag(qdt, "a", "unit")
    print qdt.latex_table()
    from taref.plotter.fig_format import Plotter
    from taref.physics.fundamentals import sinc, sinc_sq
    b=Plotter()
    from numpy import linspace, pi, absolute
    freq=linspace(1e9, 10e9, 100)
    #qdt.ft="single"
    #qdt.get_member("mult").reset(qdt)
    #qdt.get_member("lbda0").reset(qdt)

    print qdt.f0, qdt.G_f0
    G_f=0.45*qdt.Np*qdt.K2*2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-2*qdt.f0)/qdt.f0/2.0))
    b.line_plot("sinc", freq, G_f)
    b.show()
    qdt.show()
