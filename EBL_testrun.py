# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 20:12:11 2015

@author: thomasaref
"""

from EBL_IDT import EBL_IDT
from EBL_SQUID import EBL_SQUID
from EBL_PADS import EBL_PADS, Al_PADS
from EBL_Item import EBL_Item

from atom.api import Typed, Enum

####general PADS
pads=EBL_PADS(name="_pads")

al_pads=Al_PADS(name="_Al_pads", chip=pads)


####single tilt IDTS
l_idt=EBL_IDT(name="_l_idt", qdt_type="IDT", hbox=30.0e-6, Np=37, x_ref=-200.0e-6)
r_idt=EBL_IDT(name="_r_idt", x_ref=300.0e-6, Np=37, qdt_type="IDT", hbox=30.0e-6)


#####df stepped IDTS
l_idt.ft="double"
r_idt.ft="double"
f0=4.0e9
l_idt.idt_type="stepped"
l_idt.Np=37
l_idt.x_ref=-300.0e-6
l_idt.o=10.0e-6
r_idt.Np=37
r_idt.x_ref=400.0e-6
r_idt.idt_type="stepped"
r_idt.o=10.0e-6

## 3rd harmonic   50%
if 1:
    l_idt.step_num=3
    r_idt.step_num=3
    l_idt.f0=f0/3
    r_idt.f0=f0/3
    l_idt.eta=0.5
    r_idt.eta=0.5
    print l_idt.a, l_idt.g, l_idt.eta, l_idt.a/(l_idt.g+l_idt.a), l_idt.Dvv, l_idt.epsinf

## 9 harmonic   50%
if 0:
    l_idt.step_num=9
    r_idt.step_num=9
    l_idt.f0=f0/9
    r_idt.f0=f0/9
    l_idt.eta=0.5
    r_idt.eta=0.5
    print l_idt.a, l_idt.g, l_idt.eta, l_idt.a/(l_idt.g+l_idt.a), l_idt.Dvv, l_idt.epsinf

## 11 harmonic   50%
if 0:
    l_idt.step_num=11
    r_idt.step_num=11
    l_idt.f0=f0/11
    r_idt.f0=f0/11
    l_idt.eta=0.5
    r_idt.eta=0.5
    print l_idt.a, l_idt.g, l_idt.eta, l_idt.a/(l_idt.g+l_idt.a), l_idt.Dvv, l_idt.epsinf

## 5 harmonic   20%
if 1:
    l_idt.step_num=5
    r_idt.step_num=5
    l_idt.f0=f0/5
    r_idt.f0=f0/5
    l_idt.eta=0.2
    r_idt.eta=0.2
    print l_idt.a, l_idt.g, l_idt.eta, l_idt.a/(l_idt.g+l_idt.a), l_idt.Dvv, l_idt.epsinf

## 7 harmonic   20%
if 0:
    l_idt.step_num=7
    r_idt.step_num=7
    l_idt.f0=f0/7
    r_idt.f0=f0/7
    l_idt.eta=0.2
    r_idt.eta=0.2
    print l_idt.a, l_idt.g, l_idt.eta, l_idt.a/(l_idt.g+l_idt.a), l_idt.Dvv, l_idt.epsinf

## single finger 3rd harmonic   20%
l_idt.ft="single"
r_idt.ft="single"

## single finger 3rd harmonic   20%
if 1:
    l_idt.step_num=3
    r_idt.step_num=3
    l_idt.f0=f0/3
    r_idt.f0=f0/3
    l_idt.eta=0.2
    r_idt.eta=0.2        
    print l_idt.a, l_idt.g, l_idt.eta, l_idt.a/(l_idt.g+l_idt.a), l_idt.Dvv, l_idt.epsinf

## single finger 5th harmonic   50%
if 1:
    l_idt.step_num=5
    r_idt.step_num=5
    l_idt.f0=f0/5
    r_idt.f0=f0/5
    l_idt.eta=0.5
    r_idt.eta=0.5        
    print l_idt.a, l_idt.g, l_idt.eta, l_idt.a/(l_idt.g+l_idt.a), l_idt.Dvv, l_idt.epsinf
#children=[l_idt, r_idt, al_pads]#, q_idt, pads, ]

if 1:
    q_idt=EBL_IDT(name="_EBL_Item_test", qdt_type="QDT", idt_type="basic", ft="single", eta=0.25, angle_x=0.2e-6)
    q_idt.a=0.1e-6
    q_idt.hbox=10e-6
    q_idt.o=10e-6
    q_idt.W=7e-6
    sqd=EBL_SQUID(name="sqd", y_ref=-20.0e-6, theta=90, gap=0.1e-6)
    #q_idt.show()
    l_idt.ft="single"
    r_idt.ft="single"
    
    l_idt.eta=0.25
    r_idt.eta=0.25
    l_idt.a=0.1e-6
    r_idt.a=0.1e-6
    l_idt.idt_type="basic"
    l_idt.Np=37
    l_idt.x_ref=-200.0e-6
    l_idt.o=10.0e-6
    r_idt.Np=37
    r_idt.x_ref=300.0e-6
    r_idt.idt_type="basic"
    r_idt.o=10.0e-6
    l_idt.W=7e-6
    r_idt.W=7e-6
    children=[ q_idt, sqd, l_idt, r_idt, al_pads]
if 0:
    r_idt.save_file.file_path="blah"
    r_idt.save_file.direct_save(r_idt)

#class IDT_SQUID(EBL_Item):
#    def _default_children(self):
#        return [q_idt, sqd]
#    
#    def _default_idt(self):
#        idt=EBL_IDT(name="IDT", main_params=["theta", "x_center", "y_center", "idt_type", "qdt_type", "ft",
#            "add_gate", "add_gnd", "add_teeth", "step_num",
#            "Np", "a", "g", "W", "o","f0", "eta", "ef", "wbox", "hbox", "material",
#            "trconnect_x", "trconnect_y", "trconnect_w", "trc_wbox", "trc_hbox",
#            "conn_h",  "idt_tooth", "v", "Dvv", "epsinf", "Ct", "p"])
#        idt.qdt_type="QDT"
#        return idt
#        
#    def _default_sqd(self):
#        sqd=EBL_SQUID(name="SQUID",
#              main_params=["theta", "x_center", "y_center", "squid_type",
#               "width", "height", "wb", "box_height", "w", "h", "gap", "finger_gap"])
#        sqd.y_center=-20.0
#        return sqd


class All_Show(EBL_Item):
    def _default_children(self):
        return children#=[l_idt, r_idt, al_pads]#, q_idt, pads, ]
            
a=All_Show(name="EBL_Item_test")            
a.show()