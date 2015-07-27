# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 20:12:11 2015

@author: thomasaref
"""

from EBL_IDT import EBL_IDT
from EBL_SQUID import EBL_SQUID
from EBL_PADS import EBL_PADS, Al_PADS
from EBL_Polygons import EBL_Polygons
#from EBL_Item import EBL_Item
from EBL_JDF import gen_jdf_quarter_wafer

from atom.api import Typed, Enum

dir_path="""/Users/thomasaref/Dropbox/Current stuff/TA_software/discard/"""
####general PADS
pads=EBL_PADS(name="pads")

al_pads=Al_PADS(name="Al_pads", chip=pads)

idt=EBL_IDT(name="idt", qdt_type="IDT", hbox=30.0e-6, Np=37)

class LR_IDT(EBL_Polygons):
    """combines and offsets IDTs"""
    def make_polylist(self):
        self.Poly(idt, x_off=-200.0e-6)
        self.Poly(idt, x_off=300.0e-6)
lr_idt=LR_IDT(name="LR_IDT")        
####single tilt IDTS
#r_idt=EBL_IDT(name="_r_idt", x_ref=300.0e-6, Np=37, qdt_type="IDT", hbox=30.0e-6)


#####df stepped IDTS
idt.ft="double"
f0=4.5e9
idt.idt_type="stepped"
idt.Np=37
idt.o=10.0e-6

## 3rd harmonic   50%
if 1:
    idt.step_num=3
    idt.f0=f0/3
    idt.eta=0.5
    idt.verts=[]
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns
## 9 harmonic   50%
if 1:
    idt.step_num=9
    idt.f0=f0/9
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.verts=[]
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 11 harmonic   50%
if 1:
    idt.step_num=11
    idt.f0=f0/11
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.verts=[]
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 5 harmonic   20%
if 1:
    idt.step_num=5
    idt.f0=f0/5
    idt.eta=0.2
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.verts=[]
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 7 harmonic   20%
if 1:
    idt.step_num=7
    idt.f0=f0/7
    idt.eta=0.2
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.verts=[]
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## single finger 3rd harmonic   20%
idt.ft="single"
#r_idt.ft="single"

## single finger 3rd harmonic   20%
if 1:
    idt.step_num=3
    idt.f0=f0/3
    idt.eta=0.2
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.verts=[]
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## single finger 5th harmonic   50%
if 1:
    idt.step_num=5
    idt.f0=f0/5
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.verts=[]
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 3rd harmonic, double basic
if 1:
    #idt.step_num=3
    idt.idt_type="basic"
    idt.ft="double"

    idt.f0=f0/3
    idt.eta=0.5
    idt.verts=[]
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    print idt.verts
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 3rd harmonic, single basic
if 1:
    #idt.step_num=3
    idt.idt_type="basic"
    idt.ft="single"

    idt.f0=f0/3
    idt.eta=0.5
    idt.verts=[]
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.make_polylist()
    idt.make_name_sug()
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns


if 0:
    qdt=EBL_IDT(name="qdt", qdt_type="QDT", idt_type="basic", ft="single", eta=0.25, angle_x=0.2e-6)
    qdt.a=0.1e-6
    qdt.hbox=10e-6
    qdt.o=10e-6
    qdt.W=7e-6
    sqd=EBL_SQUID(name="sqd", y_ref=-20.0e-6, theta=90, gap=0.1e-6)
    #q_idt.show()
    idt.ft="single"
    
    idt.eta=0.25
    idt.a=0.1e-6
    idt.idt_type="basic"
    idt.Np=37

    idt.o=10.0e-6
    idt.W=7e-6

b=gen_jdf_quarter_wafer(idt.chief.patterns, idt.chief.pattern_list)
print b.jdf_produce()

if 0:
    #lr_idt.chief.do_plot()
    #a.full_EBL_save()
    idt.plot_sep=False
    lr_idt.show()
    idt.plot_sep=True
    #pads.save_file.file_path="paddytest.dxf"
    #pads.save_file.direct_save(pads)
    #children=[al_pads, pads]
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


#class All_Show(EBL_Item):
#    def _default_children(self):
#        return children#=[l_idt, r_idt, al_pads]#, q_idt, pads, ]
#            
#a=All_Show(name="EBL_Item_test")            
#a.show()