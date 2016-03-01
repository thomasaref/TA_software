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
from taref.physics.fundamentals import h

class TA53_Read(Read_HDF5):
    def _default_folder(self):
        return Folder(base_dir="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A53_cooldown022915", quality="", main_dir="Data_0228")

class TA53_Fund(Agent):
    fridge_atten=Float(60)
    fridge_gain=Float(45)


qdt=QDT()
qdt.material='LiNbYZ'
qdt.ft="double"
qdt.Np=5
qdt.Rn=5200.0 #(5600.0+5100.0)/2.0
qdt.W=7.0e-6
qdt.a=96.0e-9
qdt.eta=0.5
qdt.flux_factor=0.302 #0.2945,
qdt.voltage=1.21
qdt.offset=0.02
qdt.Ec=0.8e9*h


idt=IDT(material='LiNbYZ',
        ft="double",
        Np=81,
        W=7.0e-6,
        eta=0.5,
        a=96.0e-9)

if __name__=="__main__":
    print get_tag(qdt, "a", "unit")
    print qdt.latex_table()
    from taref.plotter.fig_format import Plotter
    from taref.physics.fundamentals import sinc, sinc_sq
    b=Plotter()
    from numpy import linspace, pi, absolute, sqrt, sin
    freq=linspace(1e9, 10e9, 1000)
    #qdt.ft="single"
    #qdt.get_member("mult").reset(qdt)
    #qdt.get_member("lbda0").reset(qdt)

    print qdt.f0, qdt.G_f0
    if 0:
        #G_f=(1.0/sqrt(2.0))*0.5*qdt.Np*qdt.K2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-qdt.f0)/qdt.f0))
        #b.line_plot("sinc", freq, G_f, label="sinc/sqrt(2)")
        #G_f=0.5*qdt.Np*qdt.K2*qdt.f0*absolute(sinc(qdt.Np*pi*(freq-qdt.f0)/qdt.f0))
        #b.line_plot("sinc2", freq, G_f, label="sinc")
        Np=9
        K2=0.048
        f0=2*5.45e9

        G_f=0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*sin(pi*(freq-f0)/f0)))**2
        b.line_plot("sine_sq", freq, G_f, label="sine_sq")
        G_f=0.5*Np*K2*f0*sinc_sq(Np*pi*(freq-f0)/f0)
        b.line_plot("sinc_sq", freq, G_f, label="sinc_sq")

        G=1.0e9
        R=1/(1+(2*(freq-f0)/G)**2)
        b.line_plot("Rsq", freq, 0.5*Np*K2*f0*R, label="R_sq")

        b.vline_plot("listen", 4.475e9, alpha=0.3, color="black")
        b.vline_plot("listent", 4.55e9, alpha=0.3, color="black")
        b.vline_plot("listenb", 4.4e9, alpha=0.3, color="black")
    if 1:
        Np=9
        K2=0.048
        f0=5.45e9
        freq=4.48e9
        G_f=0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*sin(pi*(freq-f0)/f0)))**2
        b.scatter_plot("blah", 180e6/2.0, 2*G_f)

        Np=9
        K2=0.048
        f0=2*5.45e9
        freq=4.48e9
        G_f=0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*sin(pi*(freq-f0)/f0)))**2
        b.scatter_plot("blah2", 90e6/2.0, 2*G_f)

        Np=3
        K2=0.048
        f0=2*5.45e9
        freq=4.48e9
        G_f=0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*sin(pi*(freq-f0)/f0)))**2
        b.scatter_plot("blah3", 170e6/2.0, 2.0*G_f, color="green")

        b.line_plot("one", [100e6, 50e6, 30e6], [100e6, 50e6, 30e6])
        Np=20
        K2=0.0007
        f0=4.480000001e9
        freq=4.48e9
        G_f=0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*sin(pi*(freq-f0)/f0)))**2
        b.scatter_plot("bla5", 66e6/2.0, G_f)



    if 0:
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

    if 0:
        from numpy import pi, linspace, sin, amax, argmin, argmax
        Np=qdt.Np
        f0=5.45e9*2 #qdt.f0 #5.35e9
        freq=linspace(4e9, 5e9, 1000)

        def R_full(f_listen=4.3e9):
            w_listen=2*pi*f_listen
            epsinf=qdt.epsinf
            W=qdt.W
            Dvv=qdt.Dvv
            w0=2*pi*f0

            fq=linspace(4e9, 5e9, 1000)

            wq=2.0*pi*fq

            X=Np*pi*(f_listen-f0)/f0
            Ga0=3.11*w0*epsinf*W*Dvv*Np**2
            C=sqrt(2.0)*Np*W*epsinf
            L=1/(C*(wq**2.0))

            Ga=Ga0*(sin(X)/X)**2.0
            Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)

            #b.line_plot("Ba", fq, Ba)
            #b.line_plot("Ga", fq, Ga)
            #print Ga, Ba, w_listen*C
            return Ga/(Ga+1.0j*Ba+1.0j*w_listen*C+1.0/(1.0j*w_listen*L))
        #R=Ga/(Ga+1j*w_listen*C+1/(1j*w_listen*L))
            #b.line_plot("semiclassical", fq, absolute(R)**2, label=str(f_listen))
        #b.line_plot("semiclassical", fq, Ba)

        temp=[]
        t2=[]
        qfreq=[]
        for f in freq:
            X2=36*pi*(f-4.4e9)/4.4e9
            wrap=(sin(X2)/X2)**2
            R=absolute(R_full(f))**2
            #qfreq.append(freq[argmax(R)])
            #imax=argmax(R)
            #print imax
            #f1=freq[argmin(absolute(R[:imax]-0.5))]
            #f2=freq[argmin(absolute(R[imax:]-0.5))]
            #t2.append(f2-f1)
            temp.append(R)

        #b.line_plot("coup", freq, t2)
        #b.line_plot("R", freq, absolute(R_full(freq))**2)
        b.colormesh("R_full", freq, freq, temp)
        #R_full(4.2500001e9)
        #R_full(4.3000001e9)
        #R_full(4.3500001e9)
        #fq=linspace(4e9, 5e9, 1000)
        #X=Np*pi*(fq-f0)/f0
        #Ga=(sin(X)/X)**2.0
        #Ba=(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
        #b.line_plot("Ga", fq, Ga)
        #b.line_plot("Ba", fq, Ba)
        #sqrt(1/(C))/2*p
        #b.line_plot("semiclassical", fq, absolute(R)/amax(absolute(R)))
    b.show()
    qdt.show()
