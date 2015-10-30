# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 18:22:21 2015

@author: thomasaref
"""

from EBL_IDT import EBL_IDT
dir_path="""/Users/thomasaref/Dropbox/Current stuff/EBL_271015_Maria/"""

idt=EBL_IDT(name="idt", qdt_type="IDT", hbox=30.0e-6, Np=37)
idt.ft="double"
#idt.f0=4.5e9
idt.a=96.0e-9
print idt.f0, idt.g
idt.idt_type="basic"
idt.Np=37
idt.hbox=20.0e-6
#idt.gate_distance=
#idt.gate

## IDT with 37 fingers
if 0:
    #print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    #idt.show()
    idt.full_EBL_save(dir_path=dir_path)
    #print idt.chief.patterns

if 1:
    idt.Np=7
    idt.qdt_type="QDT"
    idt.add_gate=False
    idt.add_gnd=False
    idt.show()
    idt.full_EBL_save(dir_path=dir_path)
