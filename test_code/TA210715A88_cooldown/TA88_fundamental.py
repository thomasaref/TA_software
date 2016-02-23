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
    from numpy import linspace, pi, absolute, sqrt
    freq=linspace(1e9, 10e9, 1000)
    #qdt.ft="single"
    #qdt.get_member("mult").reset(qdt)
    #qdt.get_member("lbda0").reset(qdt)

    print qdt.f0, qdt.G_f0
    if 0:
        G_f=(1.0/sqrt(2.0))*0.5*qdt.Np*qdt.K2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-qdt.f0)/qdt.f0))
        b.line_plot("sinc", freq, G_f, label="sinc/sqrt(2)")
        G_f=0.5*qdt.Np*qdt.K2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-qdt.f0)/qdt.f0))
        b.line_plot("sinc2", freq, G_f, label="sinc")
        G_f=0.5*qdt.Np*qdt.K2*qdt.f0*sinc_sq(qdt.Np*pi*(freq-qdt.f0)/qdt.f0)
        b.line_plot("sinc_sq", freq, G_f, label="sinc_sq")
        b.vline_plot("listen", 4.475e9, alpha=0.3, color="black")
        b.vline_plot("listent", 4.55e9, alpha=0.3, color="black")
        b.vline_plot("listenb", 4.4e9, alpha=0.3, color="black")
    if 1:
        freq=4.475e9
        f0=linspace(5e9, 6e9, 1000)
        G_f=(1.0/sqrt(2.0))*0.5*qdt.Np*qdt.K2*f0*absolute(sinc(qdt.Np*pi*(freq-f0)/f0))
        b.line_plot("sinc", f0, G_f, label="sinc/sqrt(2)")
        G_f=0.5*qdt.Np*qdt.K2*f0*absolute(sinc(qdt.Np*pi*(freq-f0)/f0))
        b.line_plot("sinc2", f0, G_f, label="sinc")
        G_f=0.5*qdt.Np*qdt.K2*f0*sinc_sq(qdt.Np*pi*(freq-f0)/f0)
        b.line_plot("sinc_sq", f0, G_f, label="sinc_sq")
        b.vline_plot("theory", 5.45e9, alpha=0.3, color="black", label="theory")
        #b.vline_plot("listent", 4.55e9, alpha=0.3, color="black")
        #b.vline_plot("listenb", 4.4e9, alpha=0.3, color="black")

    b.show()
    qdt.show()
