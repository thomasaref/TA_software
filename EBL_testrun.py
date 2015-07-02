# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 20:12:11 2015

@author: thomasaref
"""

from EBL_IDT import EBL_IDT
from EBL_SQUID import EBL_SQUID
from EBL_Item import EBL_Item

from atom.api import Typed, Enum, Callable

class EBL_Combiner(EBL_Item):
    idt=Typed(EBL_IDT)
    sqd=Typed(EBL_SQUID)   
    
    def _default_idt(self):
        idt=EBL_IDT(name="IDT", main_params=["theta", "x_center", "y_center", "idt_type", "qdt_type", "ft",
            "add_gate", "add_gnd", "add_teeth", "step_num",
            "Np", "a", "g", "W", "o","f0", "eta", "ef", "wbox", "hbox", "material",
            "trconnect_x", "trconnect_y", "trconnect_w", "trc_wbox", "trc_hbox",
            "conn_h",  "idt_tooth", "v", "Dvv", "epsinf", "Ct", "p"])
        idt.qdt_type="QDT"
        return idt
        
    def _default_sqd(self):
        sqd=EBL_SQUID(name="SQUID",
              main_params=["theta", "x_center", "y_center", "squid_type",
               "width", "height", "wb", "box_height", "w", "h", "gap", "finger_gap"])
        sqd.y_center=-20.0
        return sqd
        
    subitems=Enum("idt", "sqd")

    def make_polylist(self):
        for item in self.get_member("subitems").items:
            subitem=self.get_map("subitems", item)
            subitem.predraw()            
            #subitem.polys.polylist=[]
            #subitem.make_polylist()
            #subitem.rotate()
            #subitem.polys.offset_verts(subitem.x_center, subitem.y_center)
            self.polys.extend(subitem.polys)
            
    def _default_main_params(self):
        return ["plot", "view_type", "offset_verts", "rotate", "horiz_refl", "vert_refl", "clear_polylist"]
            
a=EBL_Combiner(name="EBL_Item_test")            
#a.plot(a)
#b.plot(b)
a.show()