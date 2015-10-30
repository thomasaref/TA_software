# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:18:55 2015

@author: ekstromm
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 18:22:21 2015

@author: thomasaref
"""

from EBL_IDT import EBL_IDT
#dir_path="""Z:\\PhD\\Fabrication\\EBL\\DXF_Python\\"""
dir_path="""/Users/thomasaref/Dropbox/Current stuff/EBL_271015_Maria/"""

idt=EBL_IDT(name="idt", qdt_type="IDT", hbox=20.0e-6, Np=37)
idt.ft="double"
#idt.f0=4.5e9
idt.a=190.0e-9
print idt.f0, idt.g
idt.idt_type="basic"
idt.Np=37
idt.hbox=20.0e-6
idt.W=46.0e-6
idt.gate_distance=10.0e-6

## IDT 46 um
if 1:
    idt.full_EBL_save(dir_path=dir_path)

idt.hbox=1.0e-6
if 1:
    idt.Np=5
    idt.a=135.0e-9
    idt.qdt_type="QDT"
    idt.full_EBL_save(dir_path=dir_path)

if 1:
    idt.Np=5
    idt.a=160.0e-9
    idt.qdt_type="QDT"
    idt.full_EBL_save(dir_path=dir_path)

if 1:
    idt.Np=5
    idt.a=165.0e-9
    idt.qdt_type="QDT"
    idt.full_EBL_save(dir_path=dir_path)
    

#idt=EBL_IDT(name="idt", qdt_type="IDT", hbox=20.0e-6, Np=37)
idt.qdt_type="IDT"
idt.ft="double"
#idt.f0=4.5e9
idt.a=190.0e-9
print idt.f0, idt.g
idt.idt_type="basic"
idt.Np=37
idt.hbox=20.0e-6
idt.W=35.0e-6
idt.gate_distance=10.0e-6

## 3rd harmonic   50%
if 1:
    #print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    #idt.show()
    idt.full_EBL_save(dir_path=dir_path)
    #print idt.chief.patterns

idt.hbox=1.0e-6

if 1:
    idt.Np=7
    idt.a=150.0e-9
    idt.qdt_type="QDT"
    idt.full_EBL_save(dir_path=dir_path)

if 1:
    idt.Np=7
    idt.a=168.0e-9
    idt.qdt_type="QDT"
    idt.full_EBL_save(dir_path=dir_path)

if 1:
    idt.Np=7
    idt.a=170.0e-9
    idt.qdt_type="QDT"
    idt.full_EBL_save(dir_path=dir_path)    