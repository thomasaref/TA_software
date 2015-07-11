# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:26:23 2015

@author: thomasaref
"""
from LOG_functions import log_warning#, log_debug
#log_debug(1)
from a_Agent import Spy, Agent#, boss#, NoShowBase
from EBL_Boss import ebl_boss
from atom.api import Enum, Float, Typed, Callable#, Str#, Typed, List, Unicode, Int, Atom, Range, Bool, observe
from EBL_Polygons import EBL_Polygons
from Atom_Save_File import Save_TXT

class EBL_Item(Agent, EBL_Polygons):
    testsavefile=Typed(Save_TXT, ()).tag(no_spacer=True)
    angle_x=Float(0.3).tag(desc="shift in x direction when doing angle evaporation")
    angle_y=Float().tag(desc="shift in y direction when doing angle evaporation")
    view_type=Enum("pattern", "angle")
    add_type=Enum("overwrite", "add")
    
    
    @property    
    def boss(self):
        ebl_boss.make_boss(save_log=False)
        return ebl_boss
    
    def set_xlim(self, xmin, xmax):
        self.boss.plot.set_xlim(xmin, xmax)

    def set_ylim(self, ymin, ymax):
        self.boss.plot.set_ylim(ymin, ymax)

    def children_predraw(self):
        self.make_polylist()
        for c in self.children:
            c.predraw()
            self.extend(c.verts)

    def make_polylist(self):
        self.P([(0,0)])

    @Callable
    def do_offset(self, x_ref=0, y_ref=0):
        self.offset(x_ref, y_ref)
        self.draw()

    @Callable
    def do_clear_verts(self):
        self.clear_verts()
        self.draw()
        
    def predraw(self):
        if self.add_type=="overwrite":
            self.verts=[]
        if self.view_type=="angle":
            self.children_predraw()
            self.offset(x=self.angle_x, y=self.angle_y)
            tverts=self.verts[:]
            self.children_predraw()
            self.extend(tverts)
        else:            
            self.children_predraw()
        self.rotate(self.theta)
        self.offset(self.x_ref, self.y_ref)
        
    @Callable
    def plot(self):
        self.predraw()
        self.draw()
        
    def draw(self):
        self.boss.plot.set_data(self.name, self.verts)

        if 0: #self.children!=[]:
            xmin=min(b.xmin for b in self.children)
            xmax=max(b.xmax for b in self.children)
            xmin=min(self.xmin, xmin)        
            xmax=max(self.xmax, xmax)        
            ymin=min(b.ymin for b in self.children)
            ymax=max(b.ymax for b in self.children)
            ymin=min(self.ymin, ymin)        
            ymax=max(self.ymax, ymax)        
        else:
            xmin=self.xmin
            xmax=self.xmax
            ymax=self.ymax
            ymin=self.ymin

        self.set_xlim(xmin, xmax)

        self.set_ylim(ymin, ymax)

        self.boss.plot.draw()


    @Callable
    def do_rotate(self, theta=0.0):
        self.rotate(theta)
        self.draw()
        
    @Callable
    def do_horiz_refl(self):
        self.horiz_refl()
        self.draw()

    @Callable
    def do_vert_refl(self):
        self.vert_refl()
        self.draw()
                
if __name__=="__main__":  
    a=EBL_Item(name="EBL_Item_test")
    print a.xmin
#    print a.sP([(0,0), (1,0), (0,1)])
#    print a.sR(0,0,1,1)
#    print a.sC(0,0,1,1)

#    print a.verts
#    print a.xmax
    a.show()
