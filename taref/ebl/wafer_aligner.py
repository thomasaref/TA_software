# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 21:08:46 2016

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons
from taref.ebl.polygon_backbone import sP, rotate, sPoly, sTransform
from atom.api import Float, Typed, Int
from taref.core.atom_extension import private_property, reset_property


class Wafer_Width_Checker(EBL_Polygons):
    width=Float(1000.0e-6).tag(unit="um")
    height=Float(4000.0e-6).tag(unit="um")
    small_box=Float(200.0e-6).tag(unit="um")
    angle=Float(0.0).tag(unit=" degrees")

    def _default_plot_sep(self):
        return False

    @private_property
    def polylist(self):
        self.verts=[]
        reset_property(self, "_s_width_checker")
        self.verts.extend(rotate(self._s_width_checker, self.angle))
        return self.verts

    @private_property
    def _s_width_checker(self):
        return sP([(-self.width/2.0, -self.height/2.0),
                (-self.width/2.0, -self.small_box/2.0),
                (-self.width/2.0-self.small_box/2.0, -self.small_box/2.0),
                (-self.width/2.0-self.small_box/2.0, self.small_box/2.0),
                (-self.width/2.0, self.small_box/2.0),
                (-self.width/2.0, self.height/2.0),
                (self.width/2.0, self.height/2.0),
                (self.width/2.0, self.small_box/2.0),
                (self.width/2.0+self.small_box/2.0, self.small_box/2.0),
                (self.width/2.0+self.small_box/2.0, -self.small_box/2.0),
                (self.width/2.0, -self.small_box/2.0),
                (self.width/2.0, -self.height/2.0)])

    def _default_color(self):
        return "black"

    @private_property
    def base_name(self):
        return "W_WIDTH_CHECK"

class Wafer_Aligner(EBL_Polygons):
    flat_length=Float(32500.0e-6).tag(unit="um")
    linewidth=Float(500.0e-6).tag(unit="um")
    marker_width=Float(500.0e-6).tag(unit="um")
    num_marker=Int(5)
    width_checker=Typed(Wafer_Width_Checker)
    angle=Float(0.0).tag(unit=" degrees")

    def _default_width_checker(self):
        return Wafer_Width_Checker()

    @private_property
    def polylist(self):
        self.verts=[]
        reset_property(self, "_s_wafer_aligner")
        self.verts.extend(rotate(self._s_wafer_aligner, self.angle))
        return self.verts

    @private_property
    def _s_marker(self):
        """marker for aligning wafer"""
        return sP([(-self.marker_width/2.0-self.linewidth/2.0, -self.linewidth/2.0),
            (-self.marker_width/2.0, 0.0),
            (-self.marker_width/2.0-self.linewidth/2.0, self.linewidth/2.0),
            (self.marker_width/2.0+self.linewidth/2.0, self.linewidth/2.0),
            (self.marker_width/2.0, 0.0),
            (self.marker_width/2.0+self.linewidth/2.0, -self.linewidth/2.0)])

    @private_property
    def _s_wafer_aligner(self):
        vs=sP([(-self.flat_length/2.0, self.linewidth/2.0),
               (-self.flat_length/2.0, 3.0*self.linewidth/2.0),
               (self.flat_length/2.0, 3.0*self.linewidth/2.0),
               (self.flat_length/2.0, self.linewidth/2.0)])
        sP([(-self.flat_length/2.0, -self.linewidth/2.0),
               (-self.flat_length/2.0, -3.0*self.linewidth/2.0),
               (self.flat_length/2.0, -3.0*self.linewidth/2.0),
               (self.flat_length/2.0, -self.linewidth/2.0)], vs=vs)
        reset_property(self, "_s_marker")
        for n in range(self.num_marker):
            sTransform(self._s_marker, (n-self.num_marker/2)*self.flat_length/self.num_marker, vs=vs)
        sTransform(self._s_marker, -self.flat_length/2.0-self.linewidth/2.0, theta=90.0, vs=vs)
        sTransform(self._s_marker, self.flat_length/2.0+self.linewidth/2.0, theta=90.0, vs=vs)
        sP([(-self.flat_length/2.0-4.0*self.linewidth, -3.0*self.linewidth/2.0),
            (-self.flat_length/2.0-4.0*self.linewidth, 3.0*self.linewidth/2.0),
            (-self.flat_length/2.0-self.linewidth, 3.0*self.linewidth/2.0),
            (-self.flat_length/2.0-self.linewidth, -3.0*self.linewidth/2.0)], vs=vs)
        sP([(self.flat_length/2.0+4.0*self.linewidth, -3.0*self.linewidth/2.0),
            (self.flat_length/2.0+4.0*self.linewidth, 3.0*self.linewidth/2.0),
            (self.flat_length/2.0+self.linewidth, 3.0*self.linewidth/2.0),
            (self.flat_length/2.0+self.linewidth, -3.0*self.linewidth/2.0)], vs=vs)
        sPoly(self.width_checker, y_off=3.0*self.linewidth/2.0+self.width_checker.height/2.0, vs=vs)
        return sPoly(self.width_checker, y_off=-3.0*self.linewidth/2.0-self.width_checker.height/2.0, vs=vs)

    def _default_color(self):
        return "brown"

    @private_property
    def base_name(self):
        return "W_ALIGN"

if __name__=="__main__":
    #a=Wafer_Width_Checker()
    a=Wafer_Aligner()
    a.show()





