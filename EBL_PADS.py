# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 10:19:24 2014

@author: thomasaref
"""

from atom.api import Float, Enum, Int, Typed, ForwardTyped, observe
from EBL_Item import EBL_Item
from EBL_Polygons import horiz_refl, vert_refl, horizvert_refl, EBL_Polygons, rotate
from EBL_IDT import EBL_IDT
#from EBL_Combiner import EBL_Combiner

class EBL_test_pads(EBL_Item):
    contact_width=Float(125.0e-6).tag(unit="um", desc="width of contact")
    contact_height=Float(170.0e-6).tag(unit="um", desc="height of contact")
    bridge_gap_x=Float(20.0e-6).tag(unit="um", desc="horizontal gap between testpad electrodes")
    bridge_gap_y=Float(50.0e-6).tag(unit="um", desc="vertical gap between testpad electrodes")
    testpad_width=Float(400.0e-6).tag(unit="um", desc="overall width of testpad")
    testpad_height=Float(450.0e-6).tag(unit="um", desc="overall height of testpad")
    tp_bond_pad=Float(100.0e-6).tag(unit="um", desc="bonding area of testpad")

    def make_polylist(self):
        self.extend(self._s_testpad_TL)
        self.extend(horiz_refl(self._s_testpad_TL))
        self.extend(vert_refl(self._s_testpad_TL))
        self.extend(horizvert_refl(self._s_testpad_TL))

    @property
    def _s_testpad_TL(self):
        return self.sP([(-self.testpad_width/2.0, -self.testpad_height/2.0),
                  (-self.testpad_width/2.0, -self.testpad_height/2.0+self.tp_bond_pad),
                  (-self.contact_width/2.0, -self.contact_height/2.0),
                  (-self.contact_width/2.0, -self.bridge_gap_y/2.0),
                  (-self.bridge_gap_x/2.0, -self.bridge_gap_y/2.0),
                  (-self.bridge_gap_x/2.0, -self.contact_height/2.0),
                  (-self.testpad_width/2.0+self.tp_bond_pad, -self.testpad_height/2.0)])



class Al_PADS(EBL_Item):
    def _default_color(self):
        return "red"

    def _default_layer(self):
        return "Al_35nA"
        
    chip=Typed(EBL_Item)
    gndplane_side_gap=Float(30.0e-6).tag(unit='um', desc="side gap in ground plane")
    gndplane_gap=Float(80.0e-6).tag(unit='um', desc="gap in ground plane that lets SAW through")
    gndplane_big_gap=Float(60.0e-6).tag(unit='um', desc="gap in ground plane where qubit IDT resides")
    gndplane_width=Float(30.0e-6).tag(unit='um', desc="width of ground plane fingers that block SAW")
    
    gate_gap=Float(100.0e-6).tag(unit='um', desc="gap for gate CPW")
    gate_stop=Float(60.0e-6).tag(unit="cm")
    locpw=Float(0.0e-6).tag(unit='um', desc="local offset to cpw")

    def make_name_sug(self):
        self.name_sug="alpads"
        self.shot_mod_table="ALP"

    @property
    def gndplane_testgap(self):
        return self.chip.gndplane_testgap
    @property
    def end_cpw_x(self):
        return -self.chip.mb_c+self.chip.Au_sec-self.chip.overlap
    @property
    def idt_wbox(self):
        return self.chip.idt_wbox

    @property
    def l_idt_x(self):
        return self.chip.l_idt_x

    @property
    def r_idt_x(self):
        return self.chip.r_idt_x

    @property
    def w(self):
        return self.chip.w

    @property
    def gap(self):
        return self.chip.gap

    @property
    def ocpw(self):
        return self.chip.ocpw  #mb_c-self.chip.Au_sec+self.chip.overlap

    @property
    def Al_test_strip(self):
        self.P([(-self.gndplane_testgap/2.0, -self.yheight),
                   (self.gndplane_testgap/2.0, -self.yheight),
                   (self.gndplane_big_gap/2.0+self.gndplane_width, -self.w/2.0-self.gap),
                   (-self.gndplane_big_gap/2.0-self.gndplane_width, -self.w/2.0-self.gap)])
        self.P([(-self.gndplane_big_gap/2.0-self.gndplane_width, -self.w/2.0-self.gap),
                  (-self.gndplane_big_gap/2.0-self.gndplane_width, -self.gndplane_gap/2.0),
                  (-self.gndplane_big_gap/2.0, -self.gndplane_gap/2.0),
                  (-self.gndplane_big_gap/2.0, -self.w/2.0-self.gap)])
        self.P([(self.gndplane_big_gap/2.0+self.gndplane_width, -self.w/2.0-self.gap),
                  (self.gndplane_big_gap/2.0+self.gndplane_width, -self.gndplane_gap/2.0),
                  (self.gndplane_big_gap/2.0, -self.gndplane_gap/2.0),
                  (self.gndplane_big_gap/2.0, -self.w/2.0-self.gap)])
    @property
    def _s_CPW_strip_B(self):
        vs=self.sP([(self.locpw-self.w/2.0, self.end_cpw_x),
                    (self.locpw-self.w/2.0+self.w, self.end_cpw_x),
                    (self.locpw+self.qdt_gate_width/2.0, self.ocpw-self.w/2.0-self.gap), 
                    (self.locpw-self.qdt_gate_width/2.0, self.ocpw-self.w/2.0-self.gap)])
        vs=self.sP([(self.l_idt_x+self.idt_wbox, self.ocpw-self.w/2.0-self.gap),
                    (self.end_cpw_x, self.end_cpw_x),
                    (self.locpw-self.w/2.0-self.gap, self.end_cpw_x),
                    (self.locpw-self.w/2.0-self.gap+30.0e-6, self.end_cpw_x/2),
                    (self.locpw-self.w/2.0-self.gap+20.0e-6, self.end_cpw_x/4),

                    #(self.locpw-self.gate_gap/2.0, self.endcpw_x/2.0), #ocpw-self.w/2.0-self.gap-self.w-self.gap),
#                    (self.locpw-self.gate_gap/2.0-10.0e-6,self.ocpw-2*self.w/2.0-self.gap)
                    ], vs)
        vs=self.sP([(self.r_idt_x-self.idt_wbox, self.ocpw-self.w/2.0-self.gap),
                    (-self.end_cpw_x, self.end_cpw_x),
                    (self.locpw+self.w/2.0+self.gap, self.end_cpw_x),
                    (self.locpw+self.w/2.0+self.gap-30.0e-6, self.end_cpw_x/2),
                    (self.locpw+self.w/2.0+self.gap-0.0e-6, self.end_cpw_x/4),

                    ], vs)


#        vs=self.sP([(self.r_idt_x-self.idt_wbox,self.ocpw-self.w/2.0-self.gap),
#                    (-self.end_cpw_x, self.end_cpw_x),
#                    (self.locpw+self.w/2.0+self.gap, self.end_cpw_x),
#                    (self.locpw+self.gate_gap/2.0,self.ocpw-self.w/2.0-self.gap)
#                    ], vs)
        vs=self.sP([(self.locpw-self.gate_gap/2.0, self.ocpw-3*self.w/2.0-2*self.gap),
                    (self.locpw-self.gate_gap/2.0-10.0e-6, self.ocpw-3*self.w/2.0-self.gap),
                    (self.locpw-self.gate_gap/2.0-30.0e-6, self.ocpw-3*self.w/2.0-self.gap),
                    (self.locpw-self.gate_gap/2.0-40.0e-6, self.ocpw-3*self.w/2.0-2*self.gap),
                    ], vs)
        vs=self.sP([(self.locpw+self.gate_gap/2.0, self.ocpw-3*self.w/2.0-2*self.gap),
                    (self.locpw+self.gate_gap/2.0+10.0e-6, self.ocpw-3*self.w/2.0-self.gap),
                    (self.locpw+self.gate_gap/2.0+30.0e-6, self.ocpw-3*self.w/2.0-self.gap),
                    (self.locpw+self.gate_gap/2.0+40.0e-6, self.ocpw-3*self.w/2.0-2*self.gap),
                    ], vs)

        vs=self.sP([(self.locpw-self.gate_gap/2.0-40.0e-6, self.ocpw-3*self.w/2.0-2*self.gap),
                    (self.locpw-self.w/2.0, self.end_cpw_x), #self.ocpw-3*self.w/2.0-3*self.gap),
                    (self.locpw, self.end_cpw_x),#self.ocpw-3*self.w/2.0-3*self.gap),
                    (self.locpw, self.ocpw-3*self.w/2.0-2*self.gap),
                    ], vs)
        vs=self.sP([(self.locpw+self.gate_gap/2.0+40.0e-6, self.ocpw-3*self.w/2.0-2*self.gap),
                    (self.locpw+self.w/2.0, self.end_cpw_x), #self.ocpw-3*self.w/2.0-3*self.gap),
                    (self.locpw, self.end_cpw_x),#self.ocpw-3*self.w/2.0-3*self.gap),
                    (self.locpw, self.ocpw-3*self.w/2.0-2*self.gap),
                    ], vs)

        return vs

    qdt_gate_width=Float(14.0e-6).tag(unit="um")

    @property
    def _s_CPW_strip_T(self):
        vs=self.sP([(self.locpw-self.w/2.0, -self.end_cpw_x),
                    (self.locpw-self.w/2.0+self.w, -self.end_cpw_x),
                    (self.locpw+self.qdt_gate_width/2.0, self.gate_stop), 
                    (self.locpw-self.qdt_gate_width/2.0, self.gate_stop)])
                    
        vs=self.sP([(self.l_idt_x+self.idt_wbox,self.ocpw-self.w/2.0+self.gap+self.w),
                    (self.end_cpw_x, -self.end_cpw_x),
                    (self.locpw-self.w/2.0-self.gap, -self.end_cpw_x),
                    (self.locpw-self.gate_gap/2.0,self.ocpw-self.w/2.0+self.gap+self.w)
                    ], vs)
        vs=self.sP([(self.locpw-self.gate_gap/2.0, self.ocpw-self.w/2.0+self.gap+self.w),
                    (self.locpw-self.gate_gap/2.0-10.0e-6, self.ocpw+self.w/2.0),
                    (self.locpw-self.gate_gap/2.0-30.0e-6, self.ocpw+self.w/2.0),
                    (self.locpw-self.gate_gap/2.0-40.0e-6, self.ocpw-self.w/2.0+self.gap+self.w),
                    ], vs)

        vs=self.sP([(self.locpw+self.gate_gap/2.0, self.ocpw-self.w/2.0+self.gap+self.w),
                    (self.locpw+self.gate_gap/2.0+10.0e-6, self.ocpw+self.w/2.0),
                    (self.locpw+self.gate_gap/2.0+30.0e-6, self.ocpw+self.w/2.0),
                    (self.locpw+self.gate_gap/2.0+40.0e-6, self.ocpw-self.w/2.0+self.gap+self.w),
                    ], vs)
                    
        vs=self.sP([(self.r_idt_x-self.idt_wbox,self.ocpw-self.w/2.0+self.gap+self.w),
                    (-self.end_cpw_x, -self.end_cpw_x),
                    (self.locpw+self.w/2.0+self.gap, -self.end_cpw_x),
                    (self.locpw+self.gate_gap/2.0,self.ocpw-self.w/2.0+self.gap+self.w)
                    ], vs)

        return vs


    idt_conn_w=Float(300.0e-6).tag(unit="um")
    idt_conn_h=Float(25.0e-6).tag(unit="um")
    
    @property
    def _s_CPW_strip_L(self):
        vs=self.sP([(self.end_cpw_x, self.ocpw-self.w/2.0),
                        (self.end_cpw_x, self.ocpw-self.w/2.0+self.w),
                        (self.l_idt_x+self.idt_wbox, self.ocpw-self.w/2.0+self.w),
                        (self.l_idt_x+self.idt_wbox, self.ocpw-self.w/2.0)])
                        
        vs=self.sP([(self.end_cpw_x, self.ocpw-self.w/2.0+self.gap+self.w),
                        (self.end_cpw_x, -self.end_cpw_x),
                        #(self.end_cpw_x, -self.end_cpw_x),
                        (self.l_idt_x+self.idt_wbox, self.ocpw-self.w/2.0+self.gap+self.w)], vs)
        vs=self.sP([(self.end_cpw_x, self.ocpw-self.w/2.0-self.gap),
                        (self.end_cpw_x, self.end_cpw_x),
                        #(-self.mb_c, -self.mb_c),
                        (self.l_idt_x+self.idt_wbox, self.ocpw-self.w/2.0-self.gap)], vs)
        vs=self.sP([(self.l_idt_x+self.idt_wbox, self.ocpw-self.w/2.0),
                    (self.l_idt_x+self.idt_conn_w/2.0, self.ocpw-self.w/2.0-self.idt_conn_h),
                    (self.l_idt_x-self.idt_conn_w/2.0, self.ocpw-self.w/2.0-self.idt_conn_h),
                    (self.l_idt_x-self.idt_wbox, self.ocpw-self.w/2.0)], vs)
        vs=self.sP([(self.l_idt_x+self.idt_wbox, self.ocpw-self.w/2.0-self.gap),
                    (self.l_idt_x+self.idt_conn_w/2.0, self.ocpw-self.w/2.0-self.gap+self.idt_conn_h),
                    (self.l_idt_x-self.idt_conn_w/2.0, self.ocpw-self.w/2.0-self.gap+self.idt_conn_h),
                    (self.l_idt_x-self.idt_wbox, self.ocpw-self.w/2.0-self.gap)], vs)               
        return vs
        
    def make_idt_conn(self):
        #self.CT(0, 0, self.width/2.0, self.height/2.0)
        self.R(-self.width/2.0, -self.height/2.0, -self.Al_sec, -self.w)
        self.P([(-self.width/2.0, -self.height/2.0), (-self.width/2.0, self.height/2.0), (-3.0*self.width/2.0, -self.height/2.0)])

    @property
    def _s_CPW_strip_R(self):
        vs=self.sP([(-self.end_cpw_x, self.ocpw-self.w/2.0),
                        (-self.end_cpw_x, self.ocpw-self.w/2.0+self.w),
                        (self.r_idt_x-self.idt_wbox, self.ocpw-self.w/2.0+self.w),
                        (self.r_idt_x-self.idt_wbox, self.ocpw-self.w/2.0)])
        vs=self.sP([(-self.end_cpw_x, self.ocpw-self.w/2.0+self.gap+self.w),
                        (-self.end_cpw_x, -self.end_cpw_x),
                        #(self.mb_c, self.mb_c),
                        (self.r_idt_x-self.idt_wbox, self.ocpw-self.w/2.0+self.gap+self.w)], vs)
        vs=self.sP([(-self.end_cpw_x, self.ocpw-self.w/2.0-self.gap),
                        (-self.end_cpw_x, self.end_cpw_x),
                        #(self.mb_c, -self.mb_c),
                        (self.r_idt_x-self.idt_wbox, self.ocpw-self.w/2.0-self.gap)], vs)
        vs=self.sP([(self.r_idt_x-self.idt_wbox, self.ocpw-self.w/2.0),
                    (self.r_idt_x-self.idt_conn_w/2.0, self.ocpw-self.w/2.0-self.idt_conn_h),
                    (self.r_idt_x+self.idt_conn_w/2.0, self.ocpw-self.w/2.0-self.idt_conn_h),
                    (self.r_idt_x+self.idt_wbox, self.ocpw-self.w/2.0)], vs)
        vs=self.sP([(self.r_idt_x-self.idt_wbox, self.ocpw-self.w/2.0-self.gap),
                    (self.r_idt_x-self.idt_conn_w/2.0, self.ocpw-self.w/2.0-self.gap+self.idt_conn_h),
                    (self.r_idt_x+self.idt_conn_w/2.0, self.ocpw-self.w/2.0-self.gap+self.idt_conn_h),
                    (self.r_idt_x+self.idt_wbox, self.ocpw-self.w/2.0-self.gap)], vs) 
        return vs

    def make_polylist(self):
        self.extend(self._s_CPW_strip_L)
        self.extend(self._s_CPW_strip_R)
        self.extend(self._s_CPW_strip_T)
        self.extend(self._s_CPW_strip_B)



class EBL_PADS(EBL_Item):
    chip_height=Float(5000.0e-6).tag(unit='um', desc="the height of the chip (in um though would be more natural in mm) as defined by the dicing saw")
    chip_width=Float(5000.0e-6).tag(unit='um', desc="the width of the chip (in um though would be more natural in mm) as defined by the dicing saw")
    blade_width=Float(200.0e-6).tag(unit='um', desc="width of blade used to make dicing cuts")
    mb_x=Float(1500.0e-6).tag(unit="um")
    mb_y=Float(1500.0e-6).tag(unit="um")
    l_idt_x=Float(-300e-6).tag(unit="um")
    r_idt_x=Float(400e-6).tag(unit="um")
    idt_wbox=Float(160e-6).tag(unit="um")

    mb_c=Float(850.0e-6).tag(unit="um")
    w=Float(40.0e-6).tag(unit='um', desc= "width of the center strip. should be 50 Ohm impedance matched with gap (40 um)") #50
    gap=Float(120.0e-6).tag(unit='um', desc="gap of center strip. should be 50 Ohm impedance matched with w (120 um)") #180

    Au_sec=Float(250.0e-6).tag(unit="um")


    overlap=Float(50.0e-6).tag(unit="um")

    taper_length=Float(800.0e-6).tag(unit='um', desc="length of taper of from bondpad to center conductor")
    bond_pad=Float(200.0e-6).tag(unit='um', desc="size of bond pad. in general, this should be above 100 um")
    bond_pad_gap=Float(500.0e-6).tag(unit='um', desc="the bond pad gap should roughly match 50 Ohms but chip thickness effects may dominate")

    h_idt=Float(52.0e-6).tag(unit='um', desc="height of idt electrode one is trying to connect to.")

    yheight=Float(900.0e-6).tag(unit="um", desc="real y edge of chip")

    gndplane_testgap=Float(600.0e-6).tag(unit='um', desc="gap in ground plane for test structures")
    testx=Float(1100.0e-6).tag(unit='um', desc="xcoord of test structures")
    testy=Float(-1500.0e-6).tag(unit='um', desc="xcoord of test structures")
    
    ocpw=Float(0.0e-6).tag(unit='um', desc="offset of cpw")
    
    #Al_sec=Float(500.0e-6).tag(unit="um")
    width=Float(40.0e-6).tag(unit="um")
    height=Float(100.0e-6).tag(unit="um")
    M1_size=Float(500.0e-6).tag(unit="um", desc="size of marker 1")
    lbl_height=Float(500.0e-6).tag(unit="um", desc="label height (assumed above marker 1)")
    lbl_width=Float(1100.0e-6).tag(unit="um", desc="label width (label assumed above marker 1)")

    def make_name_sug(self):
        self.name_sug="tpads"
        self.shot_mod_table="TPD"

    def _default_layer(self):
        return "Au"

    @property
    def xbox(self):
        """width from center of pattern"""
        return self.chip_width/2.0-self.blade_width/2.0

    @property
    def ybox(self):
        """height from center of pattern"""
        return self.chip_height/2.0-self.blade_width/2.0
    
    
    @property
    def _s_markbox_BL(self):
        """returns a bottom left mark box with the right side open for a test structure"""
        return self.sP([(-self.mb_c, -self.mb_c),
                        (-self.xbox, -self.mb_c),
                        (-self.xbox, -self.ybox),
                        (-self.mb_c, -self.ybox),
                        (-self.mb_c, self.testy-self.gndplane_testgap/2.0),
                        (-self.mb_x-self.M1_size/2.0, self.testy-self.gndplane_testgap/2.0),
                        (-self.mb_x-self.M1_size/2.0, self.testy+self.gndplane_testgap/2.0),
                        (-self.mb_c, self.testy+self.gndplane_testgap/2.0)])

    @property
    def _s_labelbox_TL(self):
        """returns a top left label box with the right side open"""
        return self.sP([(-self.mb_c, self.mb_c),
                        (-self.xbox, self.mb_c),
                        (-self.xbox, self.ybox),
                        (-self.mb_c, self.ybox),
                        (-self.mb_c, self.mb_y+self.M1_size/2.0+self.lbl_height),
                        (-self.mb_x-self.lbl_width/2.0, self.mb_y+self.M1_size/2.0+self.lbl_height),
                        (-self.mb_x-self.lbl_width/2.0, self.mb_y+self.M1_size/2.0),
                        (-self.mb_x-self.M1_size/2.0, self.mb_y+self.M1_size/2.0),
                        (-self.mb_x-self.M1_size/2.0, self.mb_y-self.M1_size/2.0),
                        (-self.mb_x+self.M1_size/2.0, self.mb_y-self.M1_size/2.0),
                        (-self.mb_x+self.M1_size/2.0, self.mb_y+self.M1_size/2.0),
                        (-self.mb_c, self.mb_y+self.M1_size/2.0)])                        
                        
    @property
    def _s_bond_pad_TL(self):
        vs=self.sC(-self.xbox+self.bond_pad/2.0, self.ocpw, self.bond_pad, self.bond_pad)
        vs=self.sP([(-self.xbox+self.bond_pad+self.taper_length, self.ocpw-self.w/2.0),
                    (-self.xbox+self.bond_pad+self.taper_length, self.ocpw-self.w/2.0+self.w),
                    (-self.mb_c, self.ocpw-self.w/2.0+self.w),
                    (-self.mb_c, self.ocpw-self.w/2.0)], vs)
        vs=self.sT(-self.mb_c, self.ocpw-self.w/2.0, self.Au_sec, self.w, nt=4, vs=vs)
                
        vs=self.sT(-self.mb_c, self.ocpw+self.w/2.0+self.gap, self.Au_sec,
                   self.mb_c-self.ocpw-self.w/2.0-self.gap, nt=30, vs=vs)
        #vs=self.sT(-self.mb_c+self.Au_sec, self.mb_c-self.Au_sec, #-self.xbox+self.bond_pad+self.taper_length+self.mb_c,
        #               self.Au_sec, self.Au_sec, nt=10, ot="B", vs=vs)

        vs=self.sT(-self.mb_c, -self.mb_c, self.Au_sec,
                   self.mb_c-self.w/2.0-self.gap+self.ocpw, nt=30, vs=vs)

        vs=self.sP([(-self.xbox+self.bond_pad, -self.bond_pad/2.0+self.ocpw),
                (-self.xbox+self.bond_pad, self.bond_pad/2.0+self.ocpw),
                (-self.xbox+self.bond_pad+self.taper_length, self.ocpw+self.w/2.0),
                (-self.xbox+self.bond_pad+self.taper_length, self.ocpw-self.w/2.0)], vs)

        vs=self.sP([(-self.xbox, self.bond_pad/2.0+self.bond_pad_gap+self.ocpw),
                   (-self.xbox+self.bond_pad, self.bond_pad/2.0+self.bond_pad_gap+self.ocpw),
                   (-self.xbox+self.bond_pad,  self.mb_c),
                   (-self.xbox, self.mb_c)], vs)
        vs=self.sP([(-self.xbox+self.bond_pad, self.bond_pad/2.0+self.bond_pad_gap+self.ocpw),
                   (-self.xbox+self.bond_pad, self.mb_c),
                   (-self.xbox+self.bond_pad+self.taper_length, self.mb_c),
                   (-self.xbox+self.bond_pad+self.taper_length, self.w/2.0+self.gap+self.ocpw)], vs)
        vs=self.sP([(-(self.xbox-self.bond_pad-self.taper_length), self.w/2.0+self.gap+self.ocpw),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.mb_c),
                   (-self.mb_c, self.mb_c),
                   (-self.mb_c, self.w/2.0+self.gap+self.ocpw)], vs)
        vs=self.sP([(-self.xbox, -self.bond_pad/2.0-self.bond_pad_gap+self.ocpw),
                   (-(self.xbox-self.bond_pad), -self.bond_pad/2.0-self.bond_pad_gap+self.ocpw),
                   (-(self.xbox-self.bond_pad),  -self.mb_c),
                   (-self.xbox, -self.mb_c)], vs)
        vs=self.sP([(-(self.xbox-self.bond_pad), -self.bond_pad/2.0-self.bond_pad_gap+self.ocpw),
                   (-(self.xbox-self.bond_pad), -self.mb_c),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.mb_c),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.w/2.0-self.gap+self.ocpw)], vs)
        vs=self.sP([(-(self.xbox-self.bond_pad-self.taper_length), -self.w/2.0-self.gap+self.ocpw),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.mb_c),
                   (-self.mb_c, -self.mb_c),
                   (-self.mb_c, -self.w/2.0-self.gap+self.ocpw)], vs)
        return vs


    def make_polylist(self):
        self.make_bond_pads()
        self.extend(self._s_labelbox_TL)
        self.extend(self._s_markbox_BL)
        self.extend(horiz_refl(self._s_markbox_BL))
        self.extend(horizvert_refl(self._s_markbox_BL))
        #self.make_teststrip()
        #self.make_idt_conn()
        pass
    
    def make_bond_pads(self):
        self.ocpw=self.gap/2.0+self.w/2.0
        self.extend(self._s_bond_pad_TL)
        self.extend(horiz_refl(self._s_bond_pad_TL))
        self.ocpw=0        
        self.extend(rotate(horiz_refl(self._s_bond_pad_TL), 90))
        self.extend(vert_refl(rotate(horiz_refl(self._s_bond_pad_TL), 90)))
        self.ocpw=self.gap/2.0+self.w/2.0

    def _default_ocpw(self):
        return self.gap/2.0+self.w/2.0
    def _default_children(self):
        self.ocpw=self.gap/2.0+self.w/2.0
        return [
                #Al_PADS(chip=self),
                #EBL_IDT(name="quDT", qdt_type="QDT"),
                #EBL_IDT(name="IDT_L", qdt_type="IDT", hbox=30.0e-6, x_ref=-200e-6),#self.l_idt_x),
                #EBL_IDT(name="IDT_R", qdt_type="IDT", hbox=30.0e-6, x_ref=300e-6), #self.r_idt_x),
              EBL_test_pads(name="_BL_testpad", x_ref=-self.testx, y_ref=self.testy),
              EBL_test_pads(name="_BR_testpad", x_ref=self.testx, y_ref=self.testy),
              EBL_test_pads(name="_TR_testpad", x_ref=self.testx, y_ref=-self.testy)
              ]


if __name__=="__main__":
    #a=EBL_test_pads(name="EBL_Item_test")
#    a=EBL_mark_box(name="EBL_Item_test")
    a=EBL_PADS(name="EBL_Item_test")
    a.show()