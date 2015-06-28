# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:26:23 2015

@author: thomasaref
"""
from LOG_functions import log_warning#, log_debug
#log_debug(1)
from Atom_Base import Base#, boss#, NoShowBase
from EBL_Boss import ebl_boss
from atom.api import Enum, Float, Int, observe, Property, Typed, Callable#, Str#, Typed, List, Unicode, Int, Atom, Range, Bool, observe
from EBL_Polyer import Polyer, P, R, V
from numpy import sin, cos, pi
from Atom_Save_File import Save_TXT

#boss.save_factory=Save_DXF

class EBL_Base(Base):
    @property    
    def boss(self):
        ebl_boss.make_boss(save_log=False)
        return ebl_boss

class NoShow_EBL_Base(EBL_Base):
    def _default_show_base(self):
        return False


class EBL_Item(EBL_Base):
    testsavefile=Typed(Save_TXT, ())
    polys=Typed(Polyer, ()).tag(private=True)
    x_center=Float(0.0).tag(desc="x coordinate of center of pattern. this should almost always be 0.0, which is centered (default).", unit="um")
    y_center=Float(0.0).tag(desc="y coordinate of center of pattern. this should almost always be 0.0, which is centered (default).", unit="um")

    all_color=Enum("green").tag(desc="set all colors")
    all_layer=Enum("Al").tag(desc='set all layers')   
    
    theta=Float(0.0).tag(desc="angle to rotate in degrees")

    angle_x=Float(0.3).tag(desc="shift in x direction when doing angle evaporation")
    angle_y=Float().tag(desc="shift in y direction when doing angle evaporation")
    view_type=Enum("pattern", "angle")
    
    add_type=Enum("overwrite", "add")
    
    xmin=Float()#.tag(private=True)
    xmax=Float()#.tag(private=True)
    ymin=Float()#.tag(private=True)
    ymax=Float()#.tag(private=True)
    
    
    #def auto_lim(self):
    #    self.set_xlim(self.polys.xlim)
    #    self.set_ylim(self.polys.ylim)

    def set_xlim(self, xmin, xmax):
        self.boss.plot.set_xlim(xmin, xmax)

    def set_ylim(self, ymin, ymax):
        self.boss.plot.set_ylim(ymin, ymax)

    def make_polylist(self):
        pass #self.polys.polylist=[]

    @Callable
    def plot(self):
        if self.add_type=="overwrite":
            self.polys.polylist=[]
        if self.view_type=="angle":
            self.make_polylist()
            self.polys.offset_verts(x=self.angle_x, y=self.angle_y)
            tpolylist=self.polys.polylist
            self.make_polylist()
            self.polys.polylist.extend(tpolylist)
        else:            
            self.make_polylist()
        self.rotate(self.theta)
        self.polys.offset_verts(self.x_center, self.y_center)
        self.set_data()

        self.xmin=self.polys.xmin
        self.xmax=self.polys.xmax
        self.ymin=self.polys.ymin
        self.ymax=self.polys.ymax
        
        xmin=min(b.xmin for b in self.boss.bases)
        xmax=max(b.xmax for b in self.boss.bases)
        ymin=min(b.ymin for b in self.boss.bases)
        ymax=max(b.ymax for b in self.boss.bases)
        
        self.set_xlim(xmin, xmax)
        self.set_ylim(ymin, ymax)
        self.draw()
        
    def set_data(self):
        self.boss.plot.set_data(self.name, self.polys.get_verts())

    def draw(self):
        self.boss.plot.draw()


    def copyP(self, index=-1, x=0.0, y=0.0, **kwargs):
        self.polys.copyP(index, x, y, **kwargs)

    def sP(self, verts, polyer=None, **kwargs):
        if polyer==None:
            polyer=Polyer()
        polyer.P(verts, **kwargs)
        return polyer
        
    def sR(self, xr, yr, wr, hr, polyer=None, **kwargs):
        if polyer==None:
            polyer=Polyer()
        polyer.R(xr, yr, wr, hr, polyer=None, **kwargs)
        return polyer
        
    def sC(self, xr, yr, wr, hr, polyer=None, **kwargs):
        if polyer==None:
            polyer=Polyer()
        polyer.C(xr, yr, wr, hr, polyer=Polyer(), **kwargs)
        return polyer

    def P(self, verts, **kwargs):
        """adds a polygon to the polylist with vertices given as a list of tuples"""
        self.polys.P(verts, **kwargs)
        
    def R(self, xr, yr, wr, hr, **kwargs):
        """Adds a rectangle with bottom left corner coordinates to polylist"""
        self.polys.R(xr, yr, wr, hr, **kwargs)

    def C(self, xr, yr, wr, hr, **kwargs):
        """Adds a centered rectangle to the polylist"""
        self.polys.R(xr-wr/2.0, yr-hr/2.0, wr, hr, **kwargs)

    def rotate(self, theta=0.0):
        theta=theta/180.0*pi
        self.polys.rotate(theta)

    def horiz_refl(self):
        self.polys.horiz_refl()
    
    def vert_refl(self):
        self.polys.vert_refl()

    do_rotate=Callable(rotate)
    do_horiz_refl=Callable(horiz_refl)
    do_vert_refl=Callable(vert_refl)
                
                
if __name__=="__main__":  
    a=EBL_Item(name="EBL_Item_test")
    a.polys.polylist=[R(), R(5), P([(0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1)])]
    a.P([(0,0), (0,25), (0.1,25), (0.1, 0), (5, -5), (10, -5), (10, -10), (5, -10), (5, -5.1)])
    a.P([(-0.3, -5), (-0.30,25), (-0.2,25), (-0.2, -5), (5, -10), (10, -10), (10, -15), (5, -15), (5, -10.1)])
    #a.CP(x=2.0, y=2.0)
    a.show()
