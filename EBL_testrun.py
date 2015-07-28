# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 20:12:11 2015

@author: thomasaref
"""

from EBL_IDT import EBL_IDT
from EBL_SQUID import EBL_SQUID
from EBL_PADS import EBL_PADS, Al_PADS
from EBL_Polygons import EBL_Polygons, sPoly, full_EBL_save
#from EBL_Item import EBL_Item
from EBL_JDF import gen_jdf_quarter_wafer, jdf_qw_swap

from atom.api import Typed, Enum

dir_path="""/Users/thomasaref/Dropbox/Current stuff/TA_software/discard/"""
####general PADS
pads=EBL_PADS(name="sPads")

al_pads=Al_PADS(name="sAl_pads", chip=pads)

idt=EBL_IDT(name="idt", qdt_type="IDT", hbox=30.0e-6, Np=37)

class LR_IDT(EBL_Polygons):
    """combines and offsets IDTs"""
    def make_polylist(self):
        self.Poly(idt, x_off=-200.0e-6)
        self.Poly(idt, x_off=300.0e-6)
lr_idt=LR_IDT(name="LR_IDT")        
####single tilt IDTS
#r_idt=EBL_IDT(name="_r_idt", x_ref=300.0e-6, Np=37, qdt_type="IDT", hbox=30.0e-6)

if 0:
    pads.full_EBL_save(dir_path)
    al_pads.full_EBL_save(dir_path)

#####df stepped IDTS
idt.ft="double"
f0=4.5e9
idt.idt_type="stepped"
idt.Np=37
idt.o=10.0e-6

## 3rd harmonic   50%
if 0:
    idt.step_num=3
    idt.f0=f0/3
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 9 harmonic   50%
if 0:
    idt.step_num=9
    idt.f0=f0/9
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 11 harmonic   50%
if 0:
    idt.step_num=11
    idt.f0=f0/11
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 5 harmonic   20%
if 0:
    idt.step_num=5
    idt.f0=f0/5
    idt.eta=0.2
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 7 harmonic   20%
if 0:
    idt.step_num=7
    idt.f0=f0/7
    idt.eta=0.2
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    
## single finger 3rd harmonic   20%
idt.ft="single"
#r_idt.ft="single"

## single finger 3rd harmonic   20%
if 0:
    idt.step_num=3
    idt.f0=f0/3
    idt.eta=0.2
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    
## single finger 5th harmonic   50%
if 0:
    idt.step_num=5
    idt.f0=f0/5
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    
## 3rd harmonic, double basic
if 0:
    #idt.step_num=3
    idt.idt_type="basic"
    idt.ft="double"

    idt.f0=f0/3
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    print idt.chief.patterns

## 3rd harmonic, single basic
if 0:
    #idt.step_num=3
    idt.idt_type="basic"
    idt.ft="single"

    idt.f0=f0/3
    idt.eta=0.5
    print idt.a, idt.g, idt.eta, idt.a/(idt.g+idt.a), idt.Dvv, idt.epsinf
    idt.full_EBL_save(dir_path=dir_path)
    

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
if 0:
    b=gen_jdf_quarter_wafer(idt.chief.patterns)
    print b.jdf_produce()

if 0:
    idt.plot_sep=False
    lr_idt.show()
    idt.plot_sep=True

if 1:
    jdf_data="""JOB/W 'IDT', 4, -4.2

;distributed main array for quarter wafer A, For exposure on YZ-cut LiNbO3, Cop+ZEP., q-wafer D

GLMPOS P=(-40000, 4000), Q=(-4000,40000)
PATH
ARRAY (-42500, 8, 5000)/(42500, 8, 5000)
	CHMPOS M1=(1500, 1500)
	ASSIGN A(1) -> ((7,1),(8,5),(6,2),(3,5),(5,8),(6,7)) ;stpIDTd37s3a290e50
	ASSIGN A(2) -> ((8,1),(2,6),(7,2),(4,5),(6,8),(7,7)) ;stpIDTd37s9a872e50
	ASSIGN A(3) -> ((5,2),(8,6),(5,3),(5,5),(7,8)) ;stpIDTd37s11a1065e50
	ASSIGN A(4) -> ((8,2),(1,7),(6,3),(6,5),(8,8)) ;stpIDTd37s5a193e20
	ASSIGN A(5) -> ((4,3),(8,7),(7,3),(7,5),(7,6)) ;stpIDTd37s7a271e20
	ASSIGN A(6) -> ((8,3),(1,8),(4,4),(3,6),(2,7)) ;stpIDTs37s3a232e20
	ASSIGN A(7) -> ((3,4),(2,8),(5,4),(4,6),(3,7)) ;stpIDTs37s5a968e50
	ASSIGN A(8) -> ((8,4),(3,8),(6,4),(5,6),(4,7)) ;IDTd37e0a290h0
	ASSIGN A(9) -> ((2,5),(4,8),(7,4),(6,6),(5,7)) ;IDTs37e0a581h0
AEND

1: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(1) -> ((1,1), (2,1), TID0) ;stpIDTd37s3a290e50
AEND

2: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(2) -> ((1,1), (2,1), TID1) ;stpIDTd37s9a872e50
AEND

3: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(3) -> ((1,1), (2,1), TID2) ;stpIDTd37s11a1065e50
AEND

4: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(4) -> ((1,1), (2,1), TID3) ;stpIDTd37s5a193e20
AEND

5: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(5) -> ((1,1), (2,1), TID4) ;stpIDTd37s7a271e20
AEND

6: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(6) -> ((1,1), (2,1), TIS5) ;stpIDTs37s3a232e20
AEND

7: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(7) -> ((1,1), (2,1), TIS6) ;stpIDTs37s5a968e50
AEND

8: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(8) -> ((1,1), (2,1), ID7) ;IDTd37e0a290h0
AEND

9: ARRAY (-300, 2, 700)/(0, 1, 0)
	ASSIGN P(9) -> ((1,1), (2,1), IS8) ;IDTs37e0a581h0
AEND

PEND

LAYER 1
P(1) 'stpIDTd37s3a290e50.v30' (0,0)
P(2) 'stpIDTd37s9a872e50.v30' (0,0)
P(3) 'stpIDTd37s11a1065e50.v30' (0,0)
P(4) 'stpIDTd37s5a193e20.v30' (0,0)
P(5) 'stpIDTd37s7a271e20.v30' (0,0)
P(6) 'stpIDTs37s3a232e20.v30' (0,0)
P(7) 'stpIDTs37s5a968e50.v30' (0,0)
P(8) 'IDTd37e0a290h0.v30' (0,0)
P(9) 'IDTs37e0a581h0.v30' (0,0)

STDCUR 2
SHOT A,8
RESIST 155

@ 'stpIDTd37s3a290e50.jdi'
@ 'stpIDTd37s9a872e50.jdi'
@ 'stpIDTd37s11a1065e50.jdi'
@ 'stpIDTd37s5a193e20.jdi'
@ 'stpIDTd37s7a271e20.jdi'
@ 'stpIDTs37s3a232e20.jdi'
@ 'stpIDTs37s5a968e50.jdi'
@ 'IDTd37e0a290h0.jdi'
@ 'IDTs37e0a581h0.jdi'

END 1


"""

    print jdf_qw_swap(jdf_data, "D")