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
    bridge_gap_y=Float(15.0)
    
   def makeQubit(self):
        """Draws qubit depending on object parameters"""
        self.polylist=[] #list of polygons that make up IDT pattern
        #self.xbox=self.chip_width/2.0-self.blade_width/2.0 #set width of from center of pattern
        #self.ybox=self.chip_height/2.0-self.blade_width/2.0 #set height from center of pattern
        #self.y_center=self.h_idt/2.0+self.w/2.0
        #self.gap=self.h_idt

        #self.cpw_stop_x_r=self.idtR_x #self.x_center+self.w/2+self.gap
        #self.cpw_stop_x_l=self.idtL_x#self.x_center-self.w/2-self.gap
        #self.cpw_stop_y_t=self.y_center+self.w/2+self.gap
        #self.cpw_stop_y_b=self.y_center-self.w/2-self.gap

        if self.qubit_type=='transmon':
            self.new_transmon()
        elif self.qubit_type=='bridge':
            self.bridge()
        elif self.qubit_type=='TestPads':
            self.testpads(self)
        else:
            print "not correct qubit type"
#            pass #self.singleIDT()
    def makeQubitBridge(self):
        self.qubit_type='bridge'
        self.makeQubit()

    def makeTestPads(self):
        self.qubit_type='TestPads'
        self.makeQubit()

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

    def bridge(self):
        #self.contact_width=125.0
        #self.contact_height=170.0
        #self.bridge_gap_x=20.0
        #self.bridge_gap_y=50.0
        self.bridge_TL()
        self.bridge_TR()
        self.bridge_BL()
        self.bridge_BR()
        self.drawdfqubitbottom()

    def drawdfqubitbottom(self):



        #extend center fingers
        w=0.1
        h=2.0
        hbox=8.0
        connx=1.0
        wbox=15.0
        wboxh=10.0
        #Top connection rect
#        self.xr=self.x_center
#        self.yr=self.y_center+hbox/2.0+wboxh/2.0
#        self.hr=wboxh
#        self.wr=wbox
#        self.writecenterrect()
        self.rect(self.x_center-wbox/2.0, self.y_center+hbox/2.0, wbox, wboxh )

        #Bottom connection rect
        #self.xr=self.x_center
        #self.yr=self.y_center-hbox/2.0-wboxh/2.0
        #self.hr=wboxh
        #self.wr=wbox
        self.rect(self.x_center-wbox/2.0, self.y_center-hbox/2.0, wbox, -wboxh)

        #self.xr=self.x_center-w
        #self.yr=self.y_center+hbox/2.0-h/2.0
        #self.hr=h
        #self.wr=w
        self.rect(self.x_center-w-w/2.0, self.y_center+hbox/2.0, w, -h)
        #self.writecenterrect()
        #self.xr=self.x_center+w
        #self.yr=self.y_center-h/2.0
        #self.writecenterrect()
        self.rect(self.x_center+w-w/2.0, self.y_center+hbox/2.0, w, -h)

        #extend bottom fingers
        #self.xr=self.x_center-w
        #self.yr=self.y_center-hbox/2.0+h/2.0
        #self.hr=h
        #self.wr=w
        #self.writecenterrect()
        self.rect(self.x_center-w-w/2.0, self.y_center-hbox/2.0, w, h)

        #self.xr=self.x_center+w
        #self.yr=self.y_center+h/2.0
        #self.writecenterrect()
        self.rect(self.x_center+w-w/2.0, self.y_center-hbox/2.0, w, h)

        #write top squid touch
        #self.xr=self.x_center
        #self.yr=self.y_center+hbox/2.0-h-w/2
        #self.hr=w
        #self.wr=connx
        #self.writecenterrect()
        self.rect(self.x_center-connx/2.0, self.y_center+hbox/2.0-h, connx, -w)

        #write bottom squid touch
        #self.xr=self.x_center
        #self.yr=self.y_center-hbox/2.0+h+w/2.0
        #self.hr=w
        #self.wr=connx
        #self.writecenterrect()
        self.rect(self.x_center-connx/2.0, self.y_center-hbox/2.0+h, connx, w)

    def bridge_TL(self):
        self.poly([(self.x_center-self.contact_width/2.0, self.y_center+self.contact_height/2.0),
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
    a=EBL_Qubit()
    print a.get_all_tags('good_value')
