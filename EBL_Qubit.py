# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 13:15:45 2015

@author: thomasaref
"""
from EBL_Item import EBL_Item
from atom.api import Enum, Float

class EBL_Qubit(EBL_Item):
    qubit_type=Enum('transmon', 'bridge', 'TestPads').tag(desc="")
    box_height=Float(20.0).tag(desc="height of connecting box", unit="um", good_value=20.0)
    box_width=Float(20.0).tag(desc="width of connecting box", unit="um")
    height=Float(2.0).tag(desc="height of total qubit", unit="um")
    width=Float(1.7).tag(desc="width of total qubit", unit="um")
    gap=Float(0.35).tag(desc="gap for making two angle lithography", unit="um")
    w=Float(0.1).tag(desc="width of electrode fingers", unit="um")
    h=Float(0.9).tag(desc="height of electrode fingers", unit="um")
    ew=Float(1.0).tag(desc="connecting electrode width", unit="um")
    edge_dist=Float(5.0).tag(desc="distance from edge to connecting electrodes", unit="um")

    contact_width=Float(125.0)
    contact_height=Float(170.0)
    bridge_gap_x=Float(20.0)
    bridge_gap_y=Float(15.0) #50
    testpad_width=Float(400.0)
    testpad_height=Float(450.0)

    orientation=Enum("Vertical", "Horizontal")

    def makeQubit(self):
        """Draws IDT depending on object parameters"""
        self.polys.polylist=[] #list of polygons that make up IDT pattern
        self.sdQubit()

        if self.qubit_type=='transmon':
            self.new_transmon()
        elif self.qubit_type=='bridge':
            self.bridge()
        elif self.qubit_type=='TestPads':
            self.testpads(self)
        else:
            print "not correct qubit type"


    def testpads(self):
        self.P([(self.xcenter-self.testpad_width, self.ycenter+self.testpad_height/2.0),
                   (self.x_center-self.contact_width/2.0, self.y_center+self.testpad_height/2.0),
                   (self.x_center-self.bridge_gap_x/2.0, self.y_center+self.contact_height/2.0)
                   (self.x_center-self.contact_width/2.0, self.y_center+self.contact_height/2.0)
                   ])

    def bridge(self):
        self.bridge_TL()
        self.bridge_TR()
        self.bridge_BL()
        self.bridge_BR()
        self.drawdfqubitbottom()

    def bridge_TL(self):
        self.P([(self.x_center-self.contact_width/2.0, self.y_center+self.contact_height/2.0),
                   (self.x_center-self.bridge_gap_x/2.0, self.y_center+self.contact_height/2.0),
                   (self.x_center-self.box_width/2.0+self.edge_dist, self.y_center+self.box_height/2.0-self.edge_dist),
                   (self.x_center-self.box_width/2.0, self.y_center+self.box_height/2.0-self.edge_dist)
                   ])

    def bridge_TR(self):
        self.poly([(self.x_center+self.contact_width/2.0, self.y_center+self.contact_height/2.0),
                   (self.x_center+self.bridge_gap_x/2.0, self.y_center+self.contact_height/2.0),
                   (self.x_center+self.box_width/2.0-self.edge_dist, self.y_center+self.box_height/2.0-self.edge_dist),
                   (self.x_center+self.box_width/2.0, self.y_center+self.box_height/2.0-self.edge_dist)
                   ])


    def bridge_BL(self):
        self.poly([(self.x_center-self.contact_width/2.0, self.y_center-self.contact_height/2.0),
                   (self.x_center-self.bridge_gap_x/2.0, self.y_center-self.contact_height/2.0),
                   (self.x_center-self.box_width/2.0+self.edge_dist, self.y_center-self.box_height/2.0+self.edge_dist),
                   (self.x_center-self.box_width/2.0, self.y_center-self.box_height/2.0+self.edge_dist)
                   ])

    def bridge_BR(self):
        self.poly([(self.x_center+self.contact_width/2.0, self.y_center-self.contact_height/2.0),
                   (self.x_center+self.bridge_gap_x/2.0, self.y_center-self.contact_height/2.0),
                   (self.x_center+self.box_width/2.0-self.edge_dist, self.y_center-self.box_height/2.0+self.edge_dist),
                   (self.x_center+self.box_width/2.0, self.y_center-self.box_height/2.0+self.edge_dist)
                   ])

    def new_transmon(self):
        self.poly([(self.x_center-self.width/2.0, self.y_center+self.gap/2.0),
                   (self.x_center-self.width/2.0-self.w, self.y_center+self.gap/2.0),
                   (self.x_center-self.width/2.0-self.w, self.y_center+self.gap/2.0+self.h+self.height),
                   (self.x_center+self.width/2.0+self.w, self.y_center+self.gap/2.0+self.h+self.height),
                   (self.x_center+self.width/2.0+self.w, self.y_center+self.gap/2.0),
                   (self.x_center+self.width/2.0, self.y_center+self.gap/2.0),
                   (self.x_center+self.width/2.0, self.y_center+self.h+self.gap/2.0),
                   (self.x_center-self.width/2.0, self.y_center+self.h+self.gap/2.0)])

        self.poly([(self.x_center-self.width/2.0, self.y_center-self.gap/2.0),
                   (self.x_center-self.width/2.0-self.w, self.y_center-self.gap/2.0),
                   (self.x_center-self.width/2.0-self.w, self.y_center-self.gap/2.0-self.h-self.height),
                   (self.x_center+self.width/2.0+self.w, self.y_center-self.gap/2.0-self.h-self.height),
                   (self.x_center+self.width/2.0+self.w, self.y_center-self.gap/2.0),
                   (self.x_center+self.width/2.0, self.y_center-self.gap/2.0),
                   (self.x_center+self.width/2.0, self.y_center-self.h-self.gap/2.0),
                   (self.x_center-self.width/2.0, self.y_center-self.h-self.gap/2.0)])

    def transmon(self):
        self.top_box()
        self.bottom_box()
        self.bottom_electrode()
        self.top_electrode_R()
        self.top_electrode_L()

    def bottom_electrode(self):
        self.poly([(self.x_center-self.edge_dist/2.0-self.w, self.y_center-self.height/2.0+self.box_height),
                   (self.x_center+self.edge_dist/2.0+self.w, self.y_center-self.height/2.0+self.box_height),
                   (self.x_center+self.edge_dist/2.0+self.w, self.y_center-self.gap/2.0),
                   (self.x_center-self.edge_dist/2.0-self.w, self.y_center-self.gap/2.0)
                   ])


    def top_electrode_R(self):
        self.poly([(self.x_center+self.box_width/2.0-self.edge_dist, self.y_center+self.height/2.0-self.box_height),
                   (self.x_center+self.box_width/2.0-self.edge_dist, self.y_center+self.gap/2.0+self.h),
                   (self.x_center+self.edge_dist/2.0, self.y_center+self.gap/2.0+self.h),
                   (self.x_center+self.edge_dist/2.0, self.y_center+self.gap/2.0),
                   (self.x_center+self.edge_dist/2.0-self.w, self.y_center+self.gap/2.0),
                   (self.x_center+self.edge_dist/2.0-self.w, self.y_center+self.gap/2.0+self.h+self.ew),
                   (self.x_center+self.box_width/2.0-self.ew-self.edge_dist, self.y_center+self.gap/2.0+self.h+self.ew),
                    (self.x_center+self.box_width/2.0-self.ew-self.edge_dist, self.y_center+self.height/2.0-self.box_height),
                   ])

    def top_electrode_L(self):
        self.poly([(self.x_center-self.box_width/2.0+self.edge_dist, self.y_center+self.height/2.0-self.box_height),
                   (self.x_center-self.box_width/2.0+self.edge_dist, self.y_center+self.gap/2.0+self.h),
                   (self.x_center-self.edge_dist/2.0, self.y_center+self.gap/2.0+self.h),
                   (self.x_center-self.edge_dist/2.0, self.y_center+self.gap/2.0),
                   (self.x_center-self.edge_dist/2.0+self.w, self.y_center+self.gap/2.0),
                   (self.x_center-self.edge_dist/2.0+self.w, self.y_center+self.gap/2.0+self.h+self.ew),
                   (self.x_center-self.box_width/2.0+self.ew+self.edge_dist, self.y_center+self.gap/2.0+self.h+self.ew),
                    (self.x_center-self.box_width/2.0+self.ew+self.edge_dist, self.y_center+self.height/2.0-self.box_height),
                   ])

    def top_box(self):
        self.poly([(self.x_center-self.box_width/2.0, self.y_center+self.height/2.0),
                   (self.x_center+self.box_width/2.0, self.y_center+self.height/2.0),
                   (self.x_center+self.box_width/2.0, self.y_center+self.height/2.0-self.ew),
                   (self.x_center+self.box_width/2.0-self.edge_dist, self.y_center+self.height/2.0-self.box_height),
                   (self.x_center-self.box_width/2.0+self.edge_dist, self.y_center+self.height/2.0-self.box_height),
                   (self.x_center-self.box_width/2.0, self.y_center+self.height/2.0-self.ew)])

    def bottom_box(self):
        self.poly([(self.x_center-self.width/2.0, self.y_center-self.height/2.0),
                   (self.x_center+self.width/2.0, self.y_center-self.height/2.0),
                   (self.x_center+self.width/2.0, self.y_center-self.height/2.0+self.box_height),
                   (self.x_center-self.width/2.0, self.y_center-self.height/2.0+self.box_height)])


  
    
if __name__=="__main__":
    a=EBL_Qubit(name="EBL_Item_test")
    print a.get_all_tags('good_value')
    a.bridge_TL()
    a.show()
