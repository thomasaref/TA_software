# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 15:18:25 2015

@author: thomasaref
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 13:15:45 2015

@author: thomasaref
"""
from EBL_Item import EBL_Item
from atom.api import Enum, Float
    
class EBL_SQUID(EBL_Item):
    box_height=Float(3.0).tag(desc="height of connecting box", unit="um", good_value=20.0)
    box_width=Float(10.0).tag(desc="width of connecting box", unit="um")
    height=Float(10.0).tag(desc="height of total qubit", unit="um")
    width=Float(10).tag(desc="width of total qubit", unit="um")
    gap=Float(0.2).tag(desc="gap for making two angle lithography", unit="um")
    w=Float(0.1).tag(desc="width of electrode fingers", unit="um")
    h=Float(1.0).tag(desc="height of electrode fingers", unit="um")
    ew=Float(1.0).tag(desc="connecting electrode width", unit="um")
    edge_dist=Float(5.0).tag(desc="distance from edge to connecting electrodes", unit="um")

    finger_gap=Float(3.0).tag(desc="gap between fingers")
    wb=Float(0.2).tag(desc="width of bottom fingers")
    
    contact_width=Float(125.0)
    contact_height=Float(170.0)
    bridge_gap_x=Float(20.0)
    bridge_gap_y=Float(15.0)
    testpad_width=Float(400.0)
    testpad_height=Float(450.0)

    orientation=Enum("Vertical", "Horizontal")
            
    squid_type=Enum('two_finger', 'bridge').tag(desc="")

    def make_polylist(self):
        """Draws IDT depending on object parameters"""
        self.get_map("squid_type")()
        if self.orientation=="Horizontal":
            self.rotate(90.0)

    def _default_main_params(self):
        return ["plot", "view_type", "squid_type", "orientation", "angle_x", "angle_y", "offset_verts", "rotate", "horiz_refl", "vert_refl", "clear_polylist", 
        "width", "height", "wb", "box_height", "w", "h", "gap", "finger_gap"]

   #def testpads(self):
   #     self.P([(-self.testpad_width, self.testpad_height/2.0),
   #                (self.x_center-self.contact_width/2.0, self.testpad_height/2.0),
   #                (self.x_center-self.bridge_gap_x/2.0, self.contact_height/2.0),
   #                (self.x_center-self.contact_width/2.0, self.contact_height/2.0)
   #                ])

 
    def bridge(self):
        self._bridge_TL()
        self._bridge_TR()
        self._bridge_BL()
        self._bridge_BR()
        #self.drawdfqubitbottom()

    def _new_transmon(self):
        self.P([(-self.width/2.0, self.gap/2.0),
                   (self.x_center-self.width/2.0-self.w, self.gap/2.0),
                   (self.x_center-self.width/2.0-self.w, self.gap/2.0+self.h+self.height),
                   (self.width/2.0+self.w, self.gap/2.0+self.h+self.height),
                   (self.width/2.0+self.w, self.gap/2.0),
                   (self.width/2.0, self.gap/2.0),
                   (self.width/2.0, self.h+self.gap/2.0),
                   (self.x_center-self.width/2.0, self.h+self.gap/2.0)])

        self.P([(self.x_center-self.width/2.0, -self.gap/2.0),
                   (self.x_center-self.width/2.0-self.w, -self.gap/2.0),
                   (self.x_center-self.width/2.0-self.w, -self.gap/2.0-self.h-self.height),
                   (self.width/2.0+self.w, -self.gap/2.0-self.h-self.height),
                   (self.width/2.0+self.w, -self.gap/2.0),
                   (self.width/2.0, -self.gap/2.0),
                   (self.width/2.0, -self.h-self.gap/2.0),
                   (self.x_center-self.width/2.0, -self.h-self.gap/2.0)])


    def _s_bridge_TL(self):
        contact_width=125.0
        #contact_height=170.0
        bridge_gap_x=20.0
        bridge_gap_y=50.0

        overlap=7.0
        free_space=13.0
        conn_x=4.0
        conn_w=6.0
        conn_h=0.5
        conn_y=12.0
        #TL bridge contact
        return self.sP([(-self.contact_width/2.0, bridge_gap_y/2.0+overlap),
                   (self.x_center-bridge_gap_x/2.0, bridge_gap_y/2.0+overlap),
                   (self.x_center-bridge_gap_x/2.0, bridge_gap_y/2.0-free_space),
                   (self.x_center-conn_x/2.0-conn_w, conn_y/2.0+conn_h),
                   (self.x_center-conn_x/2.0, conn_y/2.0+conn_h),
                   (self.x_center-conn_x/2.0, conn_y/2.0),
                   (self.x_center-conn_x/2.0-conn_w, conn_y/2.0),
                   (self.x_center-contact_width/2.0, bridge_gap_y/2.0-free_space)])
         
    def _bridge_TL(self):
        self.polys.extend(self._s_bridge_TL())
        
    def _bridge_TR(self):
        polyer=self._s_bridge_TL()
        polyer.horiz_refl()
        self.polys.extend(polyer)

    def _bridge_BL(self):
        polyer=self._s_bridge_TL()
        polyer.vert_refl()
        self.polys.extend(polyer)

    def _bridge_BR(self):
        polyer=self._s_bridge_TL()
        polyer.horiz_refl()
        polyer.vert_refl()
        self.polys.extend(polyer)

        
    def _new_transmon_H(self):
        self._new_transmon()
        self.rotate(90)

    def bridge3(self):
        self.bridge2()
        self.drawdfqubitbottom2attach()
        
    def bridge2(self):
        self.drawdfqubitbottom2()
 
    def drawdfqubitbottom2attach(self):
        hboxt=0.5
        boxh=7.0
        gap=0.3

        self.poly([(self.x_center-gap/2.0, -boxh/2.0),
                   (gap/2.0, -boxh/2.0),
                   (gap/2.0, -boxh/2.0-hboxt),
                   (self.x_center-gap/2.0, -boxh/2.0-hboxt)])

    def drawdfqubitbottom2(self):
        wboxt=9.0
        hboxt=0.5
        boxh=7.0
        gap=0.3
        fwidth=0.2
        fedge=1.0
        flength=2.0    
        
        #main body of contact
        self.poly([(self.x_center-wboxt/2.0, boxh/2.0+hboxt),
                   (self.x_center-gap/2.0, boxh/2.0+hboxt),
                   (self.x_center-gap/2.0, boxh/2.0),
                   (self.x_center-wboxt/2.0, boxh/2.0)])
        self.poly([(self.x_center-wboxt/2.0, -boxh/2.0),
                   (self.x_center-gap/2.0, -boxh/2.0),
                   (self.x_center-gap/2.0, -boxh/2.0-hboxt),
                   (self.x_center-wboxt/2.0, -boxh/2.0-hboxt)])
        self.poly([(gap/2.0, boxh/2.0+hboxt),
                   (wboxt/2.0, boxh/2.0+hboxt),
                   (wboxt/2.0, boxh/2.0),
                   (gap/2.0, boxh/2.0)])
        self.poly([(gap/2.0, -boxh/2.0),
                   (wboxt/2.0, -boxh/2.0),
                   (wboxt/2.0, -boxh/2.0-hboxt),
                   (gap/2.0, -boxh/2.0-hboxt)])
                   
           #fingers contanting main body
        self.poly([(self.x_center-wboxt/2.0+fedge, -boxh/2.0-hboxt),
                   (self.x_center-wboxt/2.0+fedge+fwidth, -boxh/2.0-hboxt),
                   (self.x_center-wboxt/2.0+fedge+fwidth, -boxh/2.0-hboxt-flength),
                   (self.x_center-wboxt/2.0+fedge, -boxh/2.0-hboxt-flength)])

        self.poly([(wboxt/2.0-fedge, -boxh/2.0-hboxt),
                   (wboxt/2.0-fedge-fwidth, -boxh/2.0-hboxt),
                   (wboxt/2.0-fedge-fwidth, -boxh/2.0-hboxt-flength),
                   (wboxt/2.0-fedge, -boxh/2.0-hboxt-flength)])

        self.poly([(self.x_center-wboxt/2.0+fedge, boxh/2.0+hboxt),
                   (self.x_center-wboxt/2.0+fedge+fwidth, boxh/2.0+hboxt),
                   (self.x_center-wboxt/2.0+fedge+fwidth, boxh/2.0+hboxt+flength),
                   (self.x_center-wboxt/2.0+fedge, boxh/2.0+hboxt+flength)])

        self.poly([(wboxt/2.0-fedge, boxh/2.0+hboxt),
                   (wboxt/2.0-fedge-fwidth, boxh/2.0+hboxt),
                   (wboxt/2.0-fedge-fwidth, boxh/2.0+hboxt+flength),
                   (wboxt/2.0-fedge, boxh/2.0+hboxt+flength)])

        #teeth on main body        
        sqt_x=self.x_center-wboxt/2.0
        sqt_y=boxh/2.0
        idt_tooth=0.3

        idt_numteeth=int(wboxt/(2*idt_tooth))
        idt_conn=idt_tooth*(2*idt_numteeth-1)
        sqt_x=self.x_center-idt_conn/2.0
        sqt_y=-boxh/2.0
        sqt_y_top=boxh/2.0 #self.yidt-self.offset/2.0-self.h/2.0-self.trconnect_y-self.trconnect_w

        for i in range(idt_numteeth):
            if i!=7:
                self.rect(sqt_x+2*i*idt_tooth, sqt_y, idt_tooth, idt_tooth )                    
                self.rect(sqt_x+2*i*idt_tooth, sqt_y_top, idt_tooth, -idt_tooth )                   
        

    def drawdfqubitbottom(self):
        w=0.1
        h=2.0
        hbox=8.0
        connx=1.0
        wbox=15.0
        wboxh=10.0
        self.rect(self.x_center-wbox/2.0, hbox/2.0, wbox, wboxh )
        self.rect(self.x_center-wbox/2.0, -hbox/2.0, wbox, -wboxh)

        self.rect(self.x_center-w-w/2.0, hbox/2.0, w, -h)
        self.rect(w-w/2.0, hbox/2.0, w, -h)

        self.rect(self.x_center-w-w/2.0, -hbox/2.0, w, h)

        self.rect(w-w/2.0, -hbox/2.0, w, h)
        self.rect(self.x_center-connx/2.0, hbox/2.0-h, connx, -w)

        self.rect(self.x_center-connx/2.0, -hbox/2.0+h, connx, w)

    def two_finger(self):
        self.P([(-self.width/2.0, self.height/2.0),
                   (self.width/2.0, self.height/2.0),
                   (self.width/2.0, self.height/2.0-self.box_height),
                   (self.finger_gap/2.0+self.w/2.0, self.height/2.0-self.box_height),
                   (self.finger_gap/2.0+self.w/2.0, self.gap/2.0),
                   (self.finger_gap/2.0-self.w/2.0, self.gap/2.0),
                   (self.finger_gap/2.0-self.w/2.0, self.h+self.gap/2.0),
                   (-self.finger_gap/2.0+self.w/2.0, self.h+self.gap/2.0),
                   (-self.finger_gap/2.0+self.w/2.0, self.gap/2.0),
                   (-self.finger_gap/2.0-self.w/2.0, self.gap/2.0),
                   (-self.finger_gap/2.0-self.w/2.0, self.height/2.0-self.box_height),
                   (-self.width/2.0, self.height/2.0-self.box_height)])
        self.P([(-self.width/2.0, -self.height/2.0),
                   (self.width/2.0, -self.height/2.0),
                   (self.width/2.0, -self.height/2.0+self.box_height),
                   (self.finger_gap/2.0+self.wb/2.0, -self.height/2.0+self.box_height),
                   (self.finger_gap/2.0+self.wb/2.0, -self.gap/2.0),
                   (self.finger_gap/2.0-self.wb/2.0, -self.gap/2.0),
                   (self.finger_gap/2.0-self.wb/2.0, -self.h-self.gap/2.0),
                   (-self.finger_gap/2.0+self.wb/2.0, -self.h-self.gap/2.0),
                   (-self.finger_gap/2.0+self.wb/2.0, -self.gap/2.0),
                   (-self.finger_gap/2.0-self.wb/2.0, -self.gap/2.0),
                   (-self.finger_gap/2.0-self.wb/2.0, -self.height/2.0+self.box_height),
                   (-self.width/2.0, -self.height/2.0+self.box_height)])

    def transmon(self):
        self.top_box()
        self.bottom_box()
        self.bottom_electrode()
        self._top_electrode_R()
        self._top_electrode_L()

    def bottom_electrode(self):
        self.P([(self.x_center-self.edge_dist/2.0-self.w, -self.height/2.0+self.box_height),
                   (self.edge_dist/2.0+self.w, -self.height/2.0+self.box_height),
                   (self.edge_dist/2.0+self.w, -self.gap/2.0),
                   (self.x_center-self.edge_dist/2.0-self.w, -self.gap/2.0)
                   ])

    def _s_top_electrode_L(self):
        return self.sP([(self.x_center-self.box_width/2.0+self.edge_dist, self.height/2.0-self.box_height),
                   (self.x_center-self.box_width/2.0+self.edge_dist, self.gap/2.0+self.h),
                   (self.x_center-self.edge_dist/2.0, self.gap/2.0+self.h),
                   (self.x_center-self.edge_dist/2.0, self.gap/2.0),
                   (self.x_center-self.edge_dist/2.0+self.w, self.gap/2.0),
                   (self.x_center-self.edge_dist/2.0+self.w, self.gap/2.0+self.h+self.ew),
                   (self.x_center-self.box_width/2.0+self.ew+self.edge_dist, self.gap/2.0+self.h+self.ew),
                    (self.x_center-self.box_width/2.0+self.ew+self.edge_dist, self.height/2.0-self.box_height),
                   ])

    def _top_electrode_L(self):
        self.polys.extend(self._s_top_electrode_L())

    def _top_electrode_R(self):
        polyer=self._s_top_electrode_L()
        polyer.horiz_refl()
        self.polys.extend(polyer)
        
    def top_box(self):
        self.P([(self.x_center-self.box_width/2.0, self.height/2.0),
                   (self.box_width/2.0, self.height/2.0),
                   (self.box_width/2.0, self.height/2.0-self.ew),
                   (self.box_width/2.0-self.edge_dist, self.height/2.0-self.box_height),
                   (self.x_center-self.box_width/2.0+self.edge_dist, self.height/2.0-self.box_height),
                   (self.x_center-self.box_width/2.0, self.height/2.0-self.ew)])

    def bottom_box(self):
        self.P([(self.x_center-self.width/2.0, -self.height/2.0),
                   (self.width/2.0, -self.height/2.0),
                   (self.width/2.0, -self.height/2.0+self.box_height),
                   (-self.width/2.0, -self.height/2.0+self.box_height)])
  
    
if __name__=="__main__":
    a=EBL_SQUID(name="EBL_Item_test")
    a.show()

#    def _s_bridge_TL(self):
#        return self.sP([(-self.contact_width/2.0, self.contact_height/2.0),
#                   (-self.bridge_gap_x/2.0, self.contact_height/2.0),
#                   (-self.box_width/2.0+self.edge_dist, self.box_height/2.0-self.edge_dist),
#                   (-self.box_width/2.0, self.box_height/2.0-self.edge_dist)
#                   ])