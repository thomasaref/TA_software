# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:26:23 2015

@author: thomasaref
"""
from LOG_functions import log_warning#, log_debug
#log_debug(1)
from Atom_Base import Base#, boss#, NoShowBase
from EBL_Boss import ebl_boss
from atom.api import Enum, Float, Int, observe, Property, Typed#, Str#, Typed, List, Unicode, Int, Atom, Range, Bool, observe
from EBL_Polyer import Polyer, P, R
#from Atom_Save_File import Save_DXF

#boss.save_factory=Save_DXF

class EBL_Base(Base):
    def _default_boss(self):
        ebl_boss.make_boss()
        return ebl_boss

class NoShow_EBL_Base(EBL_Base):
    def _default_show_base(self):
        return False


class EBL_Item(EBL_Base):

    polys=Typed(Polyer, ())
    x_center=Float(0.0).tag(desc="x coordinate of center of pattern. this should almost always be 0.0, which is centered (default).", unit="um")
    y_center=Float(0.0).tag(desc="y coordinate of center of pattern. this should almost always be 0.0, which is centered (default).", unit="um")

    all_color=Enum("green").tag(desc="set all colors")
    all_layer=Enum("Al").tag(desc='set all layers')   

#    def set_color(self, color="green"):
        
    def plot(self):
        for n,p in enumerate(self.polys.polylist):
            self.boss.plot.add_poly_plot(n=n, verts=p.get_verts(), cn=p.color, polyname=self.name)
        self.boss.plot.plot.request_redraw()    

    def CP(self, index=-1, x=0.0, y=0.0, **kwargs):
        self.polys.CP(index, x, y, **kwargs)

    def P(self, verts, **kwargs):
        """adds a polygon to the polylist with vertices given as a list of tuples"""
        self.polys.P(verts, **kwargs)
        
    def R(self, xr, yr, wr, hr, **kwargs):
        """Adds a rectangle with bottom left corner coordinates to polylist"""
        self.polys.R(xr, yr, wr, hr, **kwargs)

    def C(self, xr, yr, wr, hr, **kwargs):
        """Adds a centered rectangle to the polylist"""
        self.polys.R(xr-wr/2.0, yr-hr/2.0, wr, hr, **kwargs)

if __name__=="__main__":    
    a=EBL_Item(name="EBL_Item_test")
    a.polys.polylist=[R(), R(5), P([(0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1)])]
    a.P([(0,0), (0,25), (0.1,25), (0.1, 0), (5, -5), (10, -5), (10, -10), (5, -10), (5, -5.1)])
    a.P([(-0.3, -5), (-0.30,25), (-0.2,25), (-0.2, -5), (5, -10), (10, -10), (10, -15), (5, -15), (5, -10.1)])
    a.CP(x=2.0, y=2.0)
    a.show()
