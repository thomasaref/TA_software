# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 00:26:05 2016

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons
from atom.api import Float, Enum
from taref.core.backbone import private_property

class Wafer_Labels(EBL_Polygons):
    """Draws letter number markings on full wafer using ABCD for quarters"""
    digit_height=Float(400.0e-6).tag(unit="um")
    lettering_width=Float(50.0e-6).tag(unit="um")

    @private_property
    def polylist(self):
        self.verts=[]
        for chip in self.jdf.wafer_coords.xy_locations:
            self.WaferDig(wafer_type=chip[0],x_dig=chip[1], y_dig=chip[2],
                          xr=chip[3]*1.0e-6, yr=chip[4]*1.0e-6,
                          wr=self.digit_height/2.0,
                          hr=self.lettering_width)
        return self.verts

    def _default_color(self):
        return "red"

    base_name="WAFER_LABELS"

class Digit(EBL_Polygons):
    digit_height=Float(300.0e-6).tag(unit="um")
    lettering_width=Float(40.0e-6).tag(unit="um")
    digit=Enum("A", "B", "C", "D", "1", "2", "3", "4", "5", "6", "7", "8", "9")

    @private_property
    def polylist(self):
        self.verts=[]
        self.Dig(dig_key=self.digit, xr=0.0, yr=0.0, wr=self.digit_height/2.0, hr=self.lettering_width)
        return self.verts

    def _default_color(self):
        return "red"

    base_name="DIGIT"

if __name__=="__main__":
    #a=Wafer_Labels()
    a=Digit()
    a.show()