# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 10:19:24 2014

@author: thomasaref
"""

from atom.api import Float, Enum, Int, Typed
from EBL_Item import EBL_Item
from EBL_Combiner import EBL_Combiner
    
class EBL_test_pads(EBL_Item):
    contact_width=Float(125.0e-6).tag(unit="um", desc="width of contact")
    contact_height=Float(170.0e-6).tag(unit="um", desc="height of contact")
    bridge_gap_x=Float(20.0e-6).tag(unit="um", desc="horizontal gap between testpad electrodes")
    bridge_gap_y=Float(50.0e-6).tag(unit="um", desc="vertical gap between testpad electrodes")
    testpad_width=Float(400.0e-6).tag(unit="um", desc="overall width of testpad")
    testpad_height=Float(450.0e-6).tag(unit="um", desc="overall height of testpad")
    tp_bond_pad=Float(100.0e-6).tag(unit="um", desc="bonding area of testpad")

    def make_polylist(self):
        self._testpad_TL()
        self._testpad_TR()
        self._testpad_BL()
        self._testpad_BR()

    @property
    def _s_testpad_TL(self):
        return self.sP([(-self.testpad_width/2.0, -self.testpad_height/2.0),
                  (-self.testpad_width/2.0, -self.testpad_height/2.0+self.tp_bond_pad),
                  (-self.contact_width/2.0, -self.contact_height/2.0),
                  (-self.contact_width/2.0, -self.bridge_gap_y/2.0),
                  (-self.bridge_gap_x/2.0, -self.bridge_gap_y/2.0),
                  (-self.bridge_gap_x/2.0, -self.contact_height/2.0),
                  (-self.testpad_width/2.0+self.tp_bond_pad, -self.testpad_height/2.0)])

    def _testpad_TL(self):
        self.polys.extend(self._s_testpad_TL)

    def _testpad_TR(self):
        polyer=self._s_testpad_TL
        polyer.horiz_refl()
        self.polys.extend(polyer)

    def _testpad_BL(self):
        polyer=self._s_testpad_TL
        polyer.vert_refl()
        self.polys.extend(polyer)

    def _testpad_BR(self):
        polyer=self._s_testpad_TL
        polyer.horiz_refl()
        polyer.vert_refl()
        self.polys.extend(polyer)

class EBL_mark_box(EBL_Item):
    M1_size=Float(500.0e-6).tag(unit="um", desc="size of marker 1")
    lbl_height=Float(500.0e-6).tag(unit="um", desc="label height (assumed above marker 1)")
    lbl_width=Float(1100.0e-6).tag(unit="um", desc="label width (label assumed above marker 1)")

    mark_box_outer_width=Float(900.0e-6).tag(unit="um", desc="width of outer part of mark box")
    mark_box_inner_width=Float(700.0e-6).tag(unit="um", desc="width of inner part of mark box")

    mark_box_outer_height=Float(900.0e-6).tag(unit="um", desc="height of outer part of mark box")
    mark_box_inner_height=Float(700.0e-6).tag(unit="um", desc="height of inner part of mark box")

    mark_box_type=Enum("marklabel_box_TL", "mark_box_TL", "mark_box_TR", "mark_box_BL", "mark_box_BR")

    def _default_x_center(self):
        return -1500.0e-6
        
    def _default_y_center(self):
        return 1500.0e-6
        
    def make_polylist(self):
        getattr(self, self.mark_box_type)()
        
    def marklabel_box_TL(self):
        self.polys.extend(self._s_marklabel_box_TL)
        
    @property    
    def _s_marklabel_box_TL(self):
        polyer=self.sP([(-self.mark_box_outer_width, self.mark_box_outer_height),
                   (self.mark_box_inner_width, self.mark_box_outer_height),
                   (self.mark_box_inner_width, -self.mark_box_inner_height),
                   (self.M1_size/2.0, -self.mark_box_inner_height),
                   (self.M1_size/2.0, self.M1_size/2.0),
                   (self.lbl_width/2.0, self.M1_size/2.0),
                   (self.lbl_width/2.0, self.M1_size/2.0+self.lbl_height),
                   (-self.lbl_width/2.0, self.M1_size/2.0+self.lbl_height),
                   (-self.lbl_width/2.0, self.M1_size/2.0),
                   (-self.M1_size/2.0, self.M1_size/2.0),
                   (-self.M1_size/2.0, -self.mark_box_inner_height),
                   (-self.mark_box_outer_width, -self.mark_box_inner_height)])
        polyer.P([(self.M1_size/2.0, -self.mark_box_inner_height),
                   (self.M1_size/2.0, -self.M1_size/2.0),
                   (-self.M1_size/2.0, -self.M1_size/2.0),
                   (-self.M1_size/2.0, -self.mark_box_inner_height)])
        return polyer

    def mark_box_TL(self):
        self.polys.extend(self._s_mark_box_TL)
        
    @property
    def _s_mark_box_TL(self):
        polyer2=self.sP([(-self.mark_box_outer_width, self.mark_box_outer_height),
                   (self.mark_box_inner_width, self.mark_box_outer_height),
                   (self.mark_box_inner_width, -self.mark_box_inner_height),
                   (self.M1_size/2.0, -self.mark_box_inner_height),
                   (self.M1_size/2.0, self.M1_size/2.0),
                   (-self.M1_size/2.0, self.M1_size/2.0),
                   (-self.M1_size/2.0, -self.mark_box_inner_height),
                   (-self.mark_box_outer_width, -self.mark_box_inner_height)])
        polyer2.P([(self.M1_size/2.0, -self.mark_box_inner_height),
                   (self.M1_size/2.0, -self.M1_size/2.0),
                   (-self.M1_size/2.0, -self.M1_size/2.0),
                   (-self.M1_size/2.0, -self.mark_box_inner_height)])
        return polyer2

    def mark_box_BL(self):
        polyer=self._s_mark_box_TL
        polyer.vert_refl()
        self.polys.extend(polyer)
        
    def mark_box_TR(self):
        polyer=self._s_mark_box_TL
        polyer.horiz_refl()
        self.polys.extend(polyer)
        
    def mark_box_BR(self):
        polyer=self._s_mark_box_TL
        polyer.horiz_refl()
        polyer.vert_refl()
        self.polys.extend(polyer)

class EBL_IDT_connect(EBL_Item):
    idt_tooth=Float(4.0e-6).tag(unit='um', desc="tooth size on CPW connection to aid contact")
    idt_numteeth=Int(5) #52 um, 12.5 um
    w=Float(40.0e-6).tag(unit='um', desc= "width of the center strip. should be 50 Ohm impedance matched with gap (40 um)") #50
    gap=Float(120.0e-6).tag(unit='um', desc="gap of center strip. should be 50 Ohm impedance matched with w (120 um)") #180
    h_idt=Float(52.0e-6).tag(unit='um', desc="height of idt electrode one is trying to connect to.")

    IDT_conn_type=Enum("IDT_connect_R", "IDT_connect_L")

    def make_polylist(self):
        getattr(self, self.IDT_conn_type)()
        
    def IDT_connect_R(self):
        self.polys.extend(self._s_IDT_connect_R)

    def IDT_connect_L(self):
        polyp=self._s_IDT_connect_R
        polyp.horiz_refl()
        self.polys.extend(polyp)
        
    @property
    def _s_IDT_connect_R(self):
        idt_conn=self.idt_tooth*(2*self.idt_numteeth-1)
        polyer=self.sP([(0.0, self.w/2.0+self.gap/2.0),
                   (idt_conn+self.h_idt, self.w/2.0+self.gap/2.0),
                   (idt_conn, self.h_idt/2.0),
                   (0.0, self.h_idt/2.0)])
        polyer.P([(0.0, -self.w/2.0-self.gap/2.0),
                   (idt_conn+self.h_idt, -self.w/2.0-self.gap/2.0),
                   (idt_conn, -self.h_idt/2.0),
                   (0.0, -self.h_idt/2.0)])
        for i in range(self.idt_numteeth):
            polyer.R(2*i*self.idt_tooth, self.h_idt/2.0, self.idt_tooth, -self.idt_tooth )
            polyer.R(2*i*self.idt_tooth, -self.h_idt/2.0, self.idt_tooth, self.idt_tooth ) 
        return polyer

class EBL_test_strip(EBL_Item):
    w=Float(40.0e-6).tag(unit='um', desc= "width of the center strip. should be 50 Ohm impedance matched with gap (40 um)") #50
    gap=Float(120.0e-6).tag(unit='um', desc="gap of center strip. should be 50 Ohm impedance matched with w (120 um)") #180
    h_idt=Float(52.0e-6).tag(unit='um', desc="height of idt electrode one is trying to connect to.")

    ybox=Float(2400.0e-6).tag(unit="um", desc="real y edge of chip") #self.chip_height/2.0-self.blade_width/2.0 #set height from center of pattern

    yheight=Float(900.0e-6).tag(unit="um", desc="real y edge of chip")
    
    gndplane_gap=Float(80.0e-6).tag(unit='um', desc="gap in ground plane that lets SAW through")
    gndplane_big_gap=Float(60.0e-6).tag(unit='um', desc="gap in ground plane where qubit IDT resides")
    gndplane_width=Float(30.0e-6).tag(unit='um', desc="width of ground plane fingers that block SAW")
    gndplane_testgap=Float(500.0e-6).tag(unit='um', desc="gap in ground plane for test structures")
    gndplane_side_gap=Float(30.0e-6).tag(unit='um', desc="side gap in ground plane")

    def make_polylist(self):
        self.test_strip()
    def test_strip(self)          :
        self.R(-self.gndplane_testgap/2.0, -self.ybox, self.gndplane_testgap, self.ybox-self.yheight)
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

class EBL_CPW(EBL_Item): 
    taper_length=Float(800.0e-6).tag(unit='um', desc="length of taper of from bondpad to center conductor")
    xbox=Float(2400.0e-6).tag(unit="um", desc="real x edge of chip") #self.chip_width/2.0-self.blade_width/2.0 #set width of from center of pattern
    ybox=Float(2400.0e-6).tag(unit="um", desc="real y edge of chip") #self.chip_height/2.0-self.blade_width/2.0 #set height from center of pattern

    bond_pad=Float(200.0e-6).tag(unit='um', desc="size of bond pad. in general, this should be above 100 um")
    bond_pad_gap=Float(500.0e-6).tag(unit='um', desc="the bond pad gap should roughly match 50 Ohms but chip thickness effects may dominate")

    w=Float(40.0e-6).tag(unit='um', desc= "width of the center strip. should be 50 Ohm impedance matched with gap (40 um)") #50
    gap=Float(120.0e-6).tag(unit='um', desc="gap of center strip. should be 50 Ohm impedance matched with w (120 um)") #180

    taper_length=Float(800.0e-6).tag(unit='um', desc="length of taper of from bondpad to center conductor")
    cpw_stop_x_l=Float(-200.0e-6+27.7e-6/2.0).tag(unit='um', desc="x coordinate of left idt")
    cpw_stop_x_r=Float(300.0e-6-27.7e-6/2.0).tag(unit='um', desc="x coordinate of right idt")
    idt_y=Float(0.0e-6).tag(unit='um', desc="y coordinateof IDT")

    gate_extension=Float(100.0e-6).tag(unit='um', desc="length gate extends into CPW")

    mark_box_x=Float(-900.0e-6)
    mark_box_y=Float(900.0e-6)
    
    gndplane_gap=Float(80.0e-6).tag(unit='um', desc="gap in ground plane that lets SAW through")
    gndplane_big_gap=Float(60.0e-6).tag(unit='um', desc="gap in ground plane where qubit IDT resides")
    gndplane_width=Float(30.0e-6).tag(unit='um', desc="width of ground plane fingers that block SAW")
    gndplane_testgap=Float(500.0e-6).tag(unit='um', desc="gap in ground plane for test structures")
    gndplane_side_gap=Float(30.0e-6).tag(unit='um', desc="side gap in ground plane")

    def make_polylist(self):
        self.cpw_L_strip()
        self.cpw_L_top()
        self.cpw_L_bottom()

    def cpw_L_strip(self):
        self.R(-self.xbox, -self.bond_pad/2.0, self.bond_pad, self.bond_pad)
        self.P([(-(self.xbox-self.bond_pad), -self.bond_pad/2.0),
                   (-(self.xbox-self.bond_pad), self.bond_pad/2.0),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.w/2.0),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.w/2.0)])
        self.P([(-(self.xbox-self.bond_pad-self.taper_length), -self.w/2.0),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.w/2.0),
                   (self.cpw_stop_x_l, self.w/2.0),
                   (self.cpw_stop_x_l, -self.w/2.0)])

    def cpw_L_top(self):
        self.P([(-self.xbox, self.bond_pad/2.0+self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad), self.bond_pad/2.0+self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad),  self.mark_box_y),
                   (-self.xbox, self.mark_box_y)])
        self.P([(-(self.xbox-self.bond_pad), self.bond_pad/2.0+self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad), self.mark_box_y),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.mark_box_y),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.w/2.0+self.gap)])
        self.P([(-(self.xbox-self.bond_pad-self.taper_length), self.w/2.0+self.gap),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.mark_box_y),
                   (self.mark_box_x, self.mark_box_y),
                   (-self.gndplane_big_gap/2.0-self.gndplane_width-self.gndplane_side_gap, self.w/2.0+self.gap)])

    def cpw_L_bottom(self):
        self.P([(-self.xbox, -self.bond_pad/2.0-self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad), -self.bond_pad/2.0-self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad),  -self.mark_box_y),
                   (-self.xbox, -self.mark_box_y)])

        self.P([(-(self.xbox-self.bond_pad), -self.bond_pad/2.0-self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad), -self.mark_box_y),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.mark_box_y),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.w/2.0-self.gap),])
        self.P([(-(self.xbox-self.bond_pad-self.taper_length), -self.w/2.0-self.gap),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.mark_box_y),
                   (self.mark_box_x, -self.mark_box_y),
                   (-self.gndplane_big_gap/2.0-self.gndplane_width-self.gndplane_side_gap, -self.w/2.0-self.gap),])    
                   
class EBL_PADSALL(EBL_Combiner):
    BL_testpad=Typed(EBL_test_pads)
    BR_testpad=Typed(EBL_test_pads)
    
    TL_mark_box=Typed(EBL_mark_box)
    TR_mark_box=Typed(EBL_mark_box)
    BL_mark_box=Typed(EBL_mark_box)
    BR_mark_box=Typed(EBL_mark_box)

    L_IDT_conn=Typed(EBL_IDT_connect)
    R_IDT_conn=Typed(EBL_IDT_connect)
    
    test_strip=Typed(EBL_test_strip)
    L_CPW=Typed(EBL_CPW)

    def _default_L_CPW(self):
        return EBL_CPW(y_center=80.0e-6)

    def _default_test_strip(self):
        return EBL_test_strip()

    def _default_L_IDT_conn(self):
        return EBL_IDT_connect(name="_L_IDT_conn", IDT_conn_type="IDT_connect_L", x_center=-200.0e-6+27.7e-6/2.0)

    def _default_R_IDT_conn(self):
        return EBL_IDT_connect(name="_R_IDT_conn", IDT_conn_type="IDT_connect_R", x_center=300.0e-6-27.7e-6/2.0)
        
    def _default_TL_mark_box(self):
        return EBL_mark_box(name="_TL_mark_box", mark_box_type="marklabel_box_TL", x_center=-1500e-6, y_center=1500e-6)

    def _default_BL_mark_box(self):
        return EBL_mark_box(name="_BL_mark_box", x_center=-1500e-6, y_center=-1500e-6, mark_box_type="mark_box_BL")
    

    def _default_BR_mark_box(self):
        return EBL_mark_box(name="_BR_mark_box", mark_box_type="mark_box_BR", x_center=1500e-6, y_center=-1500e-6)

    def _default_TR_mark_box(self):
        return EBL_mark_box(name="_TR_mark_box", mark_box_type="mark_box_TR", x_center=1500e-6, y_center=1500e-6)
        
    def _default_BL_testpad(self):
        return EBL_test_pads(name="_BL_testpad", x_center=-500.0e-6, y_center=-1500.0e-6)

    def _default_BR_testpad(self):
        return EBL_test_pads(name="_BR_testpad", x_center=500.0e-6, y_center=-1500.0e-6)
        
    subitems=Enum("BL_testpad", "BR_testpad",  "BL_mark_box", "TL_mark_box", "TR_mark_box", "BR_mark_box", 
                    "L_IDT_conn", "R_IDT_conn", "test_strip", "L_CPW").tag(no_spacer=True)

        




                  
class EBL_PADS(EBL_Item):
    #testpad_BL=Typed(EBL_test_pads, kwargs=dict(x_center=-500.0, y_center=-1500.0))
    #testpad_BR=Typed(EBL_test_pads, kwargs=dict(x_center=500.0, y_center=-1500.0))

    xbox=Float(2400.0).tag(unit="um", desc="real x edge of chip") #self.chip_width/2.0-self.blade_width/2.0 #set width of from center of pattern
    ybox=Float(2400.0).tag(unit="um", desc="real y edge of chip") #self.chip_height/2.0-self.blade_width/2.0 #set height from center of pattern

    """handles everything related to drawing pads."""
    pad_type=Enum('gated').tag(desc="pad types are gate")
    bond_pad=Float(200.0).tag(unit='um', desc="size of bond pad. in general, this should be above 100 um")
    bond_pad_gap=Float(500.0).tag(unit='um', desc="the bond pad gap should roughly match 50 Ohms but chip thickness effects may dominate")
    chip_height=Float(5000.0).tag(unit='um', desc="the height of the chip (in um though would be more natural in mm) as defined by the dicing saw")
    chip_width=Float(5000.0).tag(unit='um', desc="the width of the chip (in um though would be more natural in mm) as defined by the dicing saw")
    blade_width=Float(200.0).tag(unit='um', desc="width of blade used to make dicing cuts")

    w=Float(40.0).tag(unit='um', desc= "width of the center strip. should be 50 Ohm impedance matched with gap (40 um)") #50
    gap=Float(120.0).tag(unit='um', desc="gap of center strip. should be 50 Ohm impedance matched with w (120 um)") #180
    h_idt=Float(52.0).tag(unit='um', desc="height of idt electrode one is trying to connect to.")

    taper_length=Float(800.0).tag(unit='um', desc="length of taper of from bondpad to center conductor")
    idtL_x=Float(-200.0+27.7/2.0).tag(unit='um', desc="x coordinate of left idt")
    idtR_x=Float(300.0-27.7/2.0).tag(unit='um', desc="x coordinate of right idt")
    idt_y=Float(0.0).tag(unit='um', desc="y coordinateof IDT")

    gndplane_gap=Float(80.0).tag(unit='um', desc="gap in ground plane that lets SAW through")
    gndplane_big_gap=Float(60.0).tag(unit='um', desc="gap in ground plane where qubit IDT resides")
    gndplane_width=Float(30.0).tag(unit='um', desc="width of ground plane fingers that block SAW")
    gndplane_testgap=Float(500.0).tag(unit='um', desc="gap in ground plane for test structures")
    gndplane_side_gap=Float(30.0).tag(unit='um', desc="side gap in ground plane")

    gate_extension=Float(100.0).tag(unit='um', desc="length gate extends into CPW")
    idt_tooth=Float(4.0).tag(unit='um', desc="tooth size on CPW connection to aid contact")
    idt_numteeth=Int(5) #52 um, 12.5 um
    xbox=Float() #self.chip_width/2.0-self.blade_width/2.0 #set width of from center of pattern
    ybox=Float() #self.chip_height/2.0-self.blade_width/2.0 #set height from center of pattern
    #y_center=Float() #self.h_idt/2.0+self.w/2.0
    cpw_stop_x_r=Float()#self.idtR_x #self.x_center+self.w/2+self.gap
    cpw_stop_x_l=Float() #self.idtL_x#self.x_center-self.w/2-self.gap
    cpw_stop_y_t=Float() #self.y_center+self.w/2+self.gap
    cpw_stop_y_b=Float() #self.y_center-self.w/2-self.gap
    test_w=Float(500.0)
    
    #@property
    #def pad_type_mapped(self):
    #    return self.get_map("pad_type")

    def make_polylist(self):
        """Draws PADS depending on object parameters"""
        self.xbox=self.chip_width/2.0-self.blade_width/2.0 #set width of from center of pattern
        self.ybox=self.chip_height/2.0-self.blade_width/2.0 #set height from center of pattern
        self.y_center=self.gap/2.0+self.w/2.0

        self.cpw_stop_x_r=self.idtR_x #self.x_center+self.w/2+self.gap
        self.cpw_stop_x_l=self.idtL_x#self.x_center-self.w/2-self.gap
        self.cpw_stop_y_t=self.y_center+self.w/2+self.gap
        self.cpw_stop_y_b=self.y_center-self.w/2-self.gap

        self.get_map("pad_type")()
        #self.pad_type_mapped()

    def gated(self):
        self.mark_box_TL()
        self.mark_box_BL()
        self.mark_box_TR()
        self.mark_box_BR()
        self.cpw_L()
        self.cpw_R()
        self.cpw_T()
        self.tst_B()
        self.IDT_connect_R()
        self.IDT_connect_L()
        self.testpdr()

    def tst_B(self):
        self.test()
        self.test()
        self.test_strip()

    def testpads(self):
        self.contact_width=125.0
        self.contact_height=170.0
        self.bridge_gap_x=20.0
        self.bridge_gap_y=50.0
        self.testpad_width=400.0
        self.testpad_height=450.0
        self.poly([(self.xcenter-self.testpad_width, self.ycenter+self.testpad_height/2.0),
                   (self.x_center-self.contact_width/2.0, self.y_center+self.testpad_height/2.0),
                   (self.x_center-self.bridge_gap_x/2.0, self.y_center+self.contact_height/2.0)
                   (self.x_center-self.contact_width/2.0, self.y_center+self.contact_height/2.0)
                   ])

    def IDT_connect_R(self):
        idt_conn=self.idt_tooth*(2*self.idt_numteeth-1)
        self.poly([(self.idtR_x, self.y_center-self.w/2.0),
                   (self.idtR_x+idt_conn+self.h_idt, self.y_center-self.w/2.0),
                   (self.idtR_x+idt_conn, self.h_idt/2.0),
                   (self.idtR_x, self.h_idt/2.0)])
        self.poly([(self.idtR_x, self.y_center-self.w/2.0-self.gap),
                   (self.idtR_x+idt_conn+self.h_idt, self.y_center-self.w/2.0-self.gap),
                   (self.idtR_x+idt_conn, -self.h_idt/2.0),
                   (self.idtR_x, -self.h_idt/2.0)])
        for i in range(self.idt_numteeth):
            self.rect(self.idtR_x+2*i*self.idt_tooth, self.h_idt/2.0, self.idt_tooth, -self.idt_tooth )
            self.rect(self.idtR_x+2*i*self.idt_tooth, -self.h_idt/2.0, self.idt_tooth, self.idt_tooth )

    def IDT_connect_L(self):
        idt_conn=self.idt_tooth*(2*self.idt_numteeth-1)
        self.poly([(self.idtL_x, self.y_center-self.w/2.0),
                   (self.idtL_x-idt_conn-self.h_idt, self.y_center-self.w/2.0),
                   (self.idtL_x-idt_conn, self.h_idt/2.0),
                   (self.idtL_x, self.h_idt/2.0)])
        self.poly([(self.idtL_x, self.y_center-self.w/2.0-self.gap),
                   (self.idtL_x-idt_conn-self.h_idt, self.y_center-self.w/2.0-self.gap),
                   (self.idtL_x-idt_conn, -self.h_idt/2.0),
                   (self.idtL_x, -self.h_idt/2.0)])
        for i in range(self.idt_numteeth):
            self.rect(self.idtL_x-2*i*self.idt_tooth, self.h_idt/2.0, -self.idt_tooth, -self.idt_tooth )
            self.rect(self.idtL_x-2*i*self.idt_tooth, -self.h_idt/2.0, -self.idt_tooth, self.idt_tooth )

    def test_strip(self)          :
        self.rect(self.x_center-self.gndplane_testgap/2.0, -self.ybox, self.gndplane_testgap, self.ybox-self.mark_box_y)
        self.poly([(self.x_center-self.gndplane_testgap/2.0, -self.mark_box_y),
                   (self.x_center+self.gndplane_testgap/2.0, -self.mark_box_y),
                   (self.x_center+self.gndplane_big_gap/2.0+self.gndplane_width, self.y_center-self.w/2.0-self.gap),
                   (self.x_center-self.gndplane_big_gap/2.0-self.gndplane_width, self.y_center-self.w/2.0-self.gap)])
        self.poly([(self.x_center-self.gndplane_big_gap/2.0-self.gndplane_width, self.y_center-self.w/2.0-self.gap),
                  (self.x_center-self.gndplane_big_gap/2.0-self.gndplane_width, -self.gndplane_gap/2.0),
                  (self.x_center-self.gndplane_big_gap/2.0, -self.gndplane_gap/2.0),
                  (self.x_center-self.gndplane_big_gap/2.0, self.y_center-self.w/2.0-self.gap)])
        self.poly([(self.x_center+self.gndplane_big_gap/2.0+self.gndplane_width, self.y_center-self.w/2.0-self.gap),
                  (self.x_center+self.gndplane_big_gap/2.0+self.gndplane_width, -self.gndplane_gap/2.0),
                  (self.x_center+self.gndplane_big_gap/2.0, -self.gndplane_gap/2.0),
                  (self.x_center+self.gndplane_big_gap/2.0, self.y_center-self.w/2.0-self.gap)])




    def cpw_T(self):
        self.cpw_T_strip()
        self.cpw_T_left()
        self.cpw_T_right()

    def cpw_T_strip(self):
        self.rect(self.x_center-self.bond_pad/2.0, self.ybox, self.bond_pad, -self.bond_pad)
        self.poly([(self.x_center-self.bond_pad/2.0, (self.ybox-self.bond_pad)),
                   (self.x_center+self.bond_pad/2.0, (self.ybox-self.bond_pad)),
                   (self.x_center+self.w/2.0, (self.ybox-self.bond_pad-self.taper_length)),
                   (self.x_center-self.w/2.0, (self.ybox-self.bond_pad-self.taper_length))])
        self.poly([(self.x_center-self.w/2.0, (self.ybox-self.bond_pad-self.taper_length)),
                   (self.x_center+self.w/2.0, (self.ybox-self.bond_pad-self.taper_length)),
                   (self.x_center+self.gndplane_width/2.0, self.cpw_stop_y_t-self.gate_extension),
                   (self.x_center-self.gndplane_width/2.0, self.cpw_stop_y_t-self.gate_extension)])

    def cpw_T_right(self):
        self.poly([( self.x_center+self.bond_pad/2.0+self.bond_pad_gap, self.ybox),
                   ( self.x_center+self.bond_pad/2.0+self.bond_pad_gap, self.ybox-self.bond_pad),
                   ( -self.mark_box_x, self.ybox-self.bond_pad),
                   ( -self.mark_box_x, self.ybox)])
        self.poly([((self.x_center+self.bond_pad/2.0+self.bond_pad_gap, self.ybox-self.bond_pad)),
                   (-self.mark_box_x, (self.ybox-self.bond_pad)),
                   (-self.mark_box_x, (self.ybox-self.bond_pad-self.taper_length)),
                   (self.x_center+self.w/2.0+self.gap, (self.ybox-self.bond_pad-self.taper_length))])
        self.poly([(self.x_center+self.w/2.0+self.gap, (self.ybox-self.bond_pad-self.taper_length)),
                   (-self.mark_box_x, (self.ybox-self.bond_pad-self.taper_length)),
                   (-self.mark_box_x, self.cpw_stop_y_t),
                   (self.x_center+self.gndplane_big_gap/2.0, self.cpw_stop_y_t)])
        self.poly([(self.x_center+self.gndplane_big_gap+self.gndplane_width, self.y_center+self.w/2.0+self.gap),
                  (self.x_center+self.gndplane_big_gap/2.0+self.gndplane_width, self.gndplane_gap/2.0),
                  (self.x_center+self.gndplane_big_gap/2.0, self.gndplane_gap/2.0),
                  (self.x_center+self.gndplane_big_gap/2, self.y_center+self.w/2.0+self.gap)])

    def cpw_T_left(self):
        self.poly([( self.x_center-self.bond_pad/2.0-self.bond_pad_gap, self.ybox),
                   ( self.x_center-self.bond_pad/2.0-self.bond_pad_gap, self.ybox-self.bond_pad),
                   ( self.mark_box_x, self.ybox-self.bond_pad),
                   ( self.mark_box_x, self.ybox)])
        self.poly([((self.x_center-self.bond_pad/2.0-self.bond_pad_gap, self.ybox-self.bond_pad)),
                   (self.mark_box_x, (self.ybox-self.bond_pad)),
                   (self.mark_box_x, (self.ybox-self.bond_pad-self.taper_length)),
                   (self.x_center-self.w/2.0-self.gap, (self.ybox-self.bond_pad-self.taper_length))])
        self.poly([(self.x_center-self.w/2.0-self.gap, (self.ybox-self.bond_pad-self.taper_length)),
                   (self.mark_box_x, (self.ybox-self.bond_pad-self.taper_length)),
                   (self.mark_box_x, self.cpw_stop_y_t),
                   (self.x_center-self.gndplane_big_gap/2.0, self.cpw_stop_y_t)])
        self.poly([(self.x_center-self.gndplane_big_gap-self.gndplane_width, self.y_center+self.w/2.0+self.gap),
                  (self.x_center-self.gndplane_big_gap/2.0-self.gndplane_width, self.gndplane_gap/2.0),
                  (self.x_center-self.gndplane_big_gap/2.0, self.gndplane_gap/2.0),
                  (self.x_center-self.gndplane_big_gap/2.0, self.y_center+self.w/2.0+self.gap)])


    def cpw_L(self):
        self.cpw_L_strip()
        self.cpw_L_top()
        self.cpw_L_bottom()

    def cpw_L_strip(self):
        self.rect(-self.xbox, self.y_center-self.bond_pad/2.0, self.bond_pad, self.bond_pad)
        self.poly([(-(self.xbox-self.bond_pad), self.y_center-self.bond_pad/2.0),
                   (-(self.xbox-self.bond_pad), self.y_center+self.bond_pad/2.0),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.y_center+self.w/2.0),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.y_center-self.w/2.0)])
        self.poly([(-(self.xbox-self.bond_pad-self.taper_length), self.y_center-self.w/2.0),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.y_center+self.w/2.0),
                   (self.cpw_stop_x_l, self.y_center+self.w/2.0),
                   (self.cpw_stop_x_l, self.y_center-self.w/2.0)])

    def cpw_L_top(self):
        self.poly([(-self.xbox, self.y_center+self.bond_pad/2.0+self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad), self.y_center+self.bond_pad/2.0+self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad),  self.mark_box_y),
                   (-self.xbox, self.mark_box_y)])
        self.poly([(-(self.xbox-self.bond_pad), self.y_center+self.bond_pad/2.0+self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad), self.mark_box_y),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.mark_box_y),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.y_center+self.w/2.0+self.gap)])
        self.poly([(-(self.xbox-self.bond_pad-self.taper_length), self.y_center+self.w/2.0+self.gap),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.mark_box_y),
                   (self.mark_box_x, self.mark_box_y),
                   (self.x_center-self.gndplane_big_gap/2.0-self.gndplane_width-self.gndplane_side_gap, self.y_center+self.w/2.0+self.gap)])

    def cpw_L_bottom(self):
        self.poly([(-self.xbox, self.y_center-self.bond_pad/2.0-self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad), self.y_center-self.bond_pad/2.0-self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad),  -self.mark_box_y),
                   (-self.xbox, -self.mark_box_y)])

        self.poly([(-(self.xbox-self.bond_pad), self.y_center-self.bond_pad/2.0-self.bond_pad_gap),
                   (-(self.xbox-self.bond_pad), -self.mark_box_y),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.mark_box_y),
                   (-(self.xbox-self.bond_pad-self.taper_length), self.y_center-self.w/2.0-self.gap),])
        self.poly([(-(self.xbox-self.bond_pad-self.taper_length), self.y_center-self.w/2.0-self.gap),
                   (-(self.xbox-self.bond_pad-self.taper_length), -self.mark_box_y),
                   (self.mark_box_x, -self.mark_box_y),
                   (self.x_center-self.gndplane_big_gap/2.0-self.gndplane_width-self.gndplane_side_gap, self.y_center-self.w/2.0-self.gap),])

    def cpw_R(self):
        self.cpw_R_strip()
        self.cpw_R_top()
        self.cpw_R_bottom()

    def cpw_R_strip(self):
        self.rect(self.xbox, self.y_center-self.bond_pad/2.0, -self.bond_pad, self.bond_pad)
        self.poly([((self.xbox-self.bond_pad), self.y_center-self.bond_pad/2.0),
                   ((self.xbox-self.bond_pad), self.y_center+self.bond_pad/2.0),
                   ((self.xbox-self.bond_pad-self.taper_length), self.y_center+self.w/2.0),
                   ((self.xbox-self.bond_pad-self.taper_length), self.y_center-self.w/2.0)])
        self.poly([((self.xbox-self.bond_pad-self.taper_length), self.y_center-self.w/2.0),
                   ((self.xbox-self.bond_pad-self.taper_length), self.y_center+self.w/2.0),
                   (self.cpw_stop_x_r, self.y_center+self.w/2.0),
                   (self.cpw_stop_x_r, self.y_center-self.w/2.0)])

    def cpw_R_top(self):
        self.poly([(self.xbox, self.y_center+self.bond_pad/2.0+self.bond_pad_gap),
                   ((self.xbox-self.bond_pad), self.y_center+self.bond_pad/2.0+self.bond_pad_gap),
                   ((self.xbox-self.bond_pad),  self.mark_box_y),
                   (self.xbox, self.mark_box_y)])
        self.poly([((self.xbox-self.bond_pad), self.y_center+self.bond_pad/2.0+self.bond_pad_gap),
                   ((self.xbox-self.bond_pad), self.mark_box_y),
                   ((self.xbox-self.bond_pad-self.taper_length), self.mark_box_y),
                   ((self.xbox-self.bond_pad-self.taper_length), self.y_center+self.w/2.0+self.gap)])
        self.poly([((self.xbox-self.bond_pad-self.taper_length), self.y_center+self.w/2.0+self.gap),
                   ((self.xbox-self.bond_pad-self.taper_length), self.mark_box_y),
                   (-self.mark_box_x, self.mark_box_y),
                   (self.x_center+self.gndplane_big_gap/2.0+self.gndplane_width+self.gndplane_side_gap, self.y_center+self.w/2.0+self.gap)])

    def cpw_R_bottom(self):
        self.poly([(self.xbox, self.y_center-self.bond_pad/2.0-self.bond_pad_gap),
                   ((self.xbox-self.bond_pad), self.y_center-self.bond_pad/2.0-self.bond_pad_gap),
                   ((self.xbox-self.bond_pad),  -self.mark_box_y),
                   (self.xbox, -self.mark_box_y)])

        self.poly([((self.xbox-self.bond_pad), self.y_center-self.bond_pad/2.0-self.bond_pad_gap),
                   ((self.xbox-self.bond_pad), -self.mark_box_y),
                   ((self.xbox-self.bond_pad-self.taper_length), -self.mark_box_y),
                   ((self.xbox-self.bond_pad-self.taper_length), self.y_center-self.w/2.0-self.gap),])
        self.poly([((self.xbox-self.bond_pad-self.taper_length), self.y_center-self.w/2.0-self.gap),
                   ((self.xbox-self.bond_pad-self.taper_length), -self.mark_box_y),
                   (-self.mark_box_x, -self.mark_box_y),
                   (self.x_center+self.gndplane_big_gap/2.0+self.gndplane_width+self.gndplane_side_gap, self.y_center-self.w/2.0-self.gap),])

    def rect(self, xr, yr, wr, hr):
        """Adds a rectangle with bottom left corner coordinates to polylist"""
        self.R(xr, yr, wr, hr)

    def poly(self, verts):
        self.P(verts)

if __name__=="__main__":
    #a=EBL_test_pads(name="EBL_Item_test")
#    a=EBL_mark_box(name="EBL_Item_test")
    a=EBL_PADSALL(name="EBL_Item_test")
    a.show()