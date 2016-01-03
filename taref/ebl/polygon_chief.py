# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 18:23:12 2015

@author: thomasaref
"""

from taref.core.chief import Chief
from taref.core.save_file import Save_TXT
from taref.core.log import log_debug
from atom.api import Typed, Float, Enum, Callable, Dict
from enaml import imports
from collections import OrderedDict
from taref.ebl.jdf import JDF_Top, JDF_Pattern, JDF_Assign, JDF_Array
from taref.ebl.polygon_backbone import sPoly,minx, maxx, miny, maxy

class Polygon_Chief(Chief):
    jdf=Typed(JDF_Top)
    
    def _default_jdf(self):
        jdf=JDF_Top()
        #assign_list=[]
        for n, p in enumerate(self.agents):
            if p.plot_sep:
                jdf.patterns.append(JDF_Pattern(num=n+1, name=p.name))
                jdf.sub_arrays.append(JDF_Array(array_num=n+1, assigns=[JDF_Assign(assign_type=["P({0})".format(n+1)],
                         short_name=p.name, pos_assign=[(1, 1)])]))
                #assign_list.append("P({0})".format(n+1))
                jdf.main_arrays[0].assigns.append(JDF_Assign(assign_type=["A({0})".format(n+1)],
                         short_name=p.name, pos_assign=[(n+1, 1)]))
        jdf.input_jdf=jdf.jdf_produce()                 
        #jdf.main_arrays[0].assigns.append(JDF_Assign(assign_type=assign_list, pos_assign=[(1,1), (1,2)]))
        #jdf.main_arrays[0].x_step=20
        #jdf.main_arrays[0].y_step=20
                
        return jdf

    def plot_JDF(self):
        xmin=minx([])
        xmax=maxx([])
        ymin=miny([])
        ymax=maxy([])
        
        xy_off=self.jdf.xy_offsets
        for p in self.jdf.patterns:
            a=self.agent_dict[p.name] #[agent for agent in self.agents if agent.name==p.name][0]
            
            #log_debug(self.jdf.arrays[0].xy_offset())
            #x_start, x_step, y_start, y_step=self.jdf.arrays[0].x_start, self.jdf.arrays[0].x_step, self.jdf.arrays[0].y_start, self.jdf.arrays[0].y_step
            #log_debug([#assign.xy_offset(self.jdf.arrays[0].x_start, self.jdf.arrays[0].x_step, 
                       #                 self.jdf.arrays[0].y_start, self.jdf.arrays[0].y_step)
            #            assign.pos_assign for assign in self.jdf.arrays[0].assigns if p.num in assign.P_nums])
            #offset_list=[assign.xy_offset(self.jdf.arrays[0].x_start, self.jdf.arrays[0].x_step, 
            #                            self.jdf.arrays[0].y_start, self.jdf.arrays[0].y_step)
            #             for assign in self.jdf.arrays[0].assigns if p.num in assign.P_nums]
            if a.plot_sep:
                verts=[]
                for chip in xy_off.get(p.name, []):
                    sPoly(a, x_off=chip[0]*1.0e-6, y_off=chip[1]*1.0e-6, vs=verts)
                      
            #for chip in self.jdf.wafer_coords.xy_locations:
            #    verts=sWaferDig(wafer_type=chip[0],x_dig=chip[1], y_dig=chip[2], xr=chip[3]*1.0e-6, yr=chip[4]*1.0e-6, wr=10.0e-6, hr=2.0e-6, vs=verts)
            #self.plot.set_data("labels", verts, "k")

            #for offsets in offset_list:
            #    for oxy in offsets:
            #        #log_debug(offset)
            #        verts=sPoly(a, x_off=oxy[0]*1.0e-6, y_off=oxy[1]*1.0e-6, vs=verts)
                    #log_debug(verts)
            self.plot.set_data(a.name, verts, a.color)
            xmin=min([minx(verts), xmin])
            xmax=max([maxx(verts), xmax])
            ymin=min([miny(verts), ymin])
            ymax=max([maxy(verts), ymax])
        
        self.plot.set_xlim(xmin, xmax)
        self.plot.set_ylim(ymin, ymax)
        self.plot.draw()
            
        
    angle_x=Float(0.3e-6).tag(desc="shift in x direction when doing angle evaporation", unit="um")
    angle_y=Float(0.0e-6).tag(desc="shift in y direction when doing angle evaporation", unit="um")
    view_type=Enum("pattern", "angle")
    add_type=Enum("overwrite", "add")

    save_factory=Callable(Save_TXT)

    pattern_dict=Dict() #for plotting
    patterns=Typed(OrderedDict, ()) #for generating jdf

    def do_plot(self):
        for p in self.agents:
            p.verts=[]
            p.make_polylist()
            if p.plot_sep:
                self.plot.set_data(p.name, p.verts, p.color)
            #self.pattern_dict[p.name]=dict(verts=p.verts[:], color=p.color, layer=p.layer, plot_sep=p.plot_sep)
            p.make_name_sug()
            p.save_file.main_file=p.name_sug+".dxf"

        #for key in self.pattern_dict:
        #    if self.pattern_dict[key]["plot_sep"]:
        #        self.plot.set_data(key, self.pattern_dict[key]["verts"], self.pattern_dict[key]["color"])

        xmin=min(b.xmin for b in self.agents)
        xmax=max(b.xmax for b in self.agents)
        ymin=min(b.ymin for b in self.agents)
        ymax=max(b.ymax for b in self.agents)
        self.plot.set_xlim(xmin, xmax)
        self.plot.set_ylim(ymin, ymax)
        self.plot.draw()

    def _default_show_all(self):
        return True

    @property
    def view_window(self):
        with imports():
            from taref.ebl.polygon_chief_e import EBLView
        return EBLView(chief=self)

polygon_chief=Polygon_Chief()

if __name__=="__main__":
    polygon_chief.show()