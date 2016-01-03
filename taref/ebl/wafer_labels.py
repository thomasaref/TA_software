# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 00:26:05 2016

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons
from atom.api import Float

class Wafer_Labels(EBL_Polygons):
    """Draws letter number markings on full wafer using ABCD for quarters"""
    digit_height=Float(300.0e-6).tag(unit="um")
    lettering_width=Float(40.0e-6).tag(unit="um")
    
    def make_polylist(self):
        for chip in self.chief.jdf.wafer_coords.xy_locations:
            self.WaferDig(wafer_type=chip[0],x_dig=chip[1], y_dig=chip[2],
                          xr=chip[3]*1.0e-6, yr=chip[4]*1.0e-6,
                          wr=self.digit_height/2.0,
                          hr=self.lettering_width)

    def _default_color(self):
        return "red"
        
    @property
    def base_name(self):
        return "WAFER_LABELS"