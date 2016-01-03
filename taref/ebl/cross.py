# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 00:51:53 2016

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons
from atom.api import Float, Property

class Cross(EBL_Polygons):
    """draws a cross of given height, width and line width)"""
    height=Float(100.0e-6).tag(unit="um")
    linewidth=Float(4.0e-6).tag(unit="um")
    width=Float(100.0e-6).tag(unit="um")
    
    def make_polylist(self):
        self.Cross(0.0, 0.0, self.width, self.height, self.linewidth)

    def _default_color(self):
        return "red"
        
    @property
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
