# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 06:09:54 2016

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons
from atom.api import Float, Property, Int
from taref.core.backbone import private_property

class Rectangle(EBL_Polygons):
    """draws a box of given height and width"""
    height=Float(100.0e-6).tag(unit="um")
    width=Float(100.0e-6).tag(unit="um")

    @private_property
    def polylist(self):
        self.verts=[]
        self.C(0.0, 0.0, self.width, self.height)
        return self.verts

    def _default_color(self):
        return "red"

    base_name="RECTANGLE"

class Square(Rectangle):
    """links width and height together so they are always the same"""
    @Property
    def width(self):
        return self.height

    @width.setter
    def set_width(self, value):
        self.height=value

    base_name="SQUARE"

class Dashed_Line_Horiz(EBL_Polygons):
    num_dashes=Int(10)
    linewidth=Float(100.0e-6).tag(unit="um")
    length=Float(100000.0e-6).tag(unit="um")

    @private_property
    def polylist(self):
        self.verts=[]
        rect_width=self.length/(2.0*self.num_dashes)
        correct=rect_width*(2*self.num_dashes-1)
        for tn in range(self.num_dashes):
            self.C(-correct/2.0+2*tn*rect_width, 0.0, rect_width, self.linewidth)
        return self.verts

    def _default_color(self):
        return "blue"

    base_name="DASHED_LINE_HORIZ"

if __name__=="__main__":
    a=Dashed_Line_Horiz()
    #print a.chief.jdf.output_jdf
    a.show()