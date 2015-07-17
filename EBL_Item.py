# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:26:23 2015

@author: thomasaref
"""
from LOG_functions import log_warning#, log_debug
#log_debug(1)
from a_Agent import Spy, Agent#, boss#, NoShowBase
from EBL_Boss import ebl_boss
from atom.api import Enum, Float, Typed, Callable, observe, Unicode#, Str#, Typed, List, Unicode, Int, Atom, Range, Bool, observe
from EBL_Polygons import EBL_Polygons
from Atom_Save_File import Save_DXF
from a_BeamerGen import BeamerGen

class EBL_Item(Agent, EBL_Polygons):
    save_file=Typed(Save_DXF, ()).tag(no_spacer=True)
    angle_x=Float(0.3e-6).tag(desc="shift in x direction when doing angle evaporation", unit="um")
    angle_y=Float(0.0e-6).tag(desc="shift in y direction when doing angle evaporation", unit="um")
    view_type=Enum("pattern", "angle")
    add_type=Enum("overwrite", "add")
    name_sug=Unicode().tag(no_spacer=True)
    shot_mod_table=Unicode()
    bmr=Typed(BeamerGen).tag(private=True)
    
    @observe('save_file.save_event')
    def obs_save_event(self, change):
        self.save_file.direct_save(self, write_mode='w')

    #def _default_read_file(self):
    #    return Read_TXT(main_file=self.main_file, dir_path=self.dir_path)

    #def _default_save_file(self):
    #    return Save_TXT(main_file=self.read_file.main_file, dir_path=self.read_file.dir_path)
    
    def full_EBL_save(self):
        print "saving to file"
        self.save_file.direct_save(self)
        self.bmr=BeamerGen(file_name=self.name_sug, mod_table_name = self.shot_mod_table, bias=-0.009, base_path=self.filer.dir_path+self.filer.divider, 
                           extentLLy=-150, extentURy=150)
        self.bmr.gen_flow()
        self.jdf.add_pattern(self.name, self.shot_mod_table)
  
    def make_name_sug(self):
        name_sug=""
        self.name_sug=name_sug
    
    @property    
    def boss(self):
        ebl_boss.make_boss(save_log=False)
        return ebl_boss
    
    def set_xlim(self, xmin, xmax):
        self.boss.plot.set_xlim(xmin, xmax)

    def set_ylim(self, ymin, ymax):
        self.boss.plot.set_ylim(ymin, ymax)

#    def children_predraw(self):
#        self.make_polylist()
#        for c in self.children:
#            c.predraw()
#            #self.extend(c.verts)

    def set_data(self):
        self.boss.plot.set_data(self.name, self.verts, self.color)
        for c in self.children:
            c.set_data()
        
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
            self.make_verts()
            self.offset(x=self.angle_x, y=self.angle_y)
            tverts=self.verts[:]
            self.make_verts()
            self.extend(tverts)
        else:            
            self.make_verts()
        self.set_data()
        self.make_name_sug()
        self.save_file.main_file=self.name_sug+".dxf"
        
    @Callable
    def plot(self):
        self.predraw()
        self.draw()
        
    def draw(self):

        if self.children!=[]:
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
