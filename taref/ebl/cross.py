# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 00:51:53 2016

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons
from atom.api import Float, Property
from taref.ebl.polygon_backbone import horiz_refl, vert_refl, horizvert_refl, sP
from taref.core.backbone import private_property

class Cross(EBL_Polygons):
    """draws a cross of given height, width and line width)"""
    height=Float(100.0e-6).tag(unit="um")
    linewidth=Float(4.0e-6).tag(unit="um")
    width=Float(100.0e-6).tag(unit="um")

    @private_property
    def polylist(self):
        self.verts=[]
        self.Cross(0.0, 0.0, self.width, self.height, self.linewidth)
        return self.verts

    def _default_color(self):
        return "red"

    @private_property
    def base_name(self):
        return "CROSS"

class Symmetric_Cross(Cross):
    """links width and height together so they are always the same"""
    @Property
    def width(self):
        return self.height

    @width.setter
    def set_width(self, value):
        self.height=value

    def _observe_height(self, change):
        if change["type"]=="update":
            self.get_member("width").reset(self)

class Inverse_Cross(Cross):
    @private_property
    def polylist(self):
        """makes inverse cross through reflections"""
        self.verts=[]
        self.reset_property("_s_crossbox_TL")
        self.verts.extend(self._s_crossbox_TL)
        self.verts.extend(horiz_refl(self._s_crossbox_TL))
        self.verts.extend(vert_refl(self._s_crossbox_TL))
        self.verts.extend(horizvert_refl(self._s_crossbox_TL))
        return self.verts

    @private_property
    def _s_crossbox_TL(self):
        """returns top left part of test pad"""
        return sP([(-self.width/2.0, self.linewidth/2.0),
                (-self.linewidth/2.0, self.linewidth/2.0),
                (-self.linewidth/2.0, self.height/2.0),
                (-self.width/2.0, self.height/2.0)])

class Symmetric_Inverse_Cross(Inverse_Cross):
    """links width and height together so they are always the same"""
    @Property
    def width(self):
        return self.height

    @width.setter
    def set_width(self, value):
        self.height=value

    def _observe_height(self, change):
        if change["type"]=="update":
            self.get_member("width").reset(self)

#class Marker_Cross(Symmetric_Cross):
#    """Draws marker crosses"""
#    @property
#    def base_name(self):
#        return "MARKER_CROSS"

#class GLM_Cross(Symmetric_Cross):
#    """Draws GLM marker crosses for P and Q"""
#    def _default_height(self):
#        return 1000.0e-6
#
#    def _default_linewidth(self):
#        return 20.0e-6
#
#    @property
#    def base_name(self):
#        return "GLM_CROSS"

#class Alignment_Cross_Horiz(Cross):
#    """Draws wide alignment cross"""
#    def _default_height(self):
#        return 100.0e-6
#
#    def _default_width(self):
#        return 1000.0e-6
#
#    @property
#    def base_name(self):
#        return "ALIGNMENT_CROSS_HORIZ"
#
#class Alignment_Cross_Vert(Cross):
#    """Draws tall alignment cross"""
#    def _default_height(self):
#        return 1000.0e-6
#
#    def _default_width(self):
#        return 100.0e-6
#
#    @property
#    def base_name(self):
#        return "ALIGNMENT_CROSS_VERT"

if __name__=="__main__":
    #a=Inverse_Cross()
    a=Symmetric_Inverse_Cross()
    a.show()
    a=Cross()
    a.height=4.0e-6
    print a.height, a.width
    a.width=3.0e-6
    print a.height, a.width

    b=Symmetric_Cross()
    b.height=4.0e-6
    print b.height, b.width
    b.width=3.0e-6
    print b.height, b.width
