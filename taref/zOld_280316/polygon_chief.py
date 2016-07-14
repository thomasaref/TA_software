# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 18:23:12 2015

@author: thomasaref
"""

from taref.core.chief import Chief, func_dict
from taref.core.save_file import Save_TXT
from taref.core.log import log_debug
from atom.api import Typed, Float, Enum, Callable, Dict, cached_property
from enaml import imports
from collections import OrderedDict
from taref.ebl.jdf import JDF_Top, JDF_Pattern, JDF_Assign, JDF_Array
from taref.ebl.polygon_backbone import sPoly,minx, maxx, miny, maxy
from taref.ebl.DXF_functions import save_dxf

class Polygon_Chief(Chief):
    jdf=Typed(JDF_Top)

    def _default_run_func_dict(self):
        return func_dict(self.plot_JDF, self.save_JDF_DXF, self.show_jdf)

    def activated(self):
        self.plot_JDF()

    @cached_property
    def other_windows(self):
        return ['jdf', 'plot']

    def show_jdf(self):
        self.jdf.view_window.show()

    def _default_jdf(self):
        jdf=JDF_Top()
        for n, p in enumerate(self.agents):
            if p.plot_sep:
                jdf.patterns.append(JDF_Pattern(num=n+1, name=p.name))
                jdf.sub_arrays.append(JDF_Array(array_num=n+1, assigns=[JDF_Assign(assign_type=["P({0})".format(n+1)],
                         short_name=p.name, pos_assign=[(1, 1)])]))
                jdf.main_arrays[0].assigns.append(JDF_Assign(assign_type=["A({0})".format(n+1)],
                         short_name=p.name, pos_assign=[(n+1, 1)]))
        jdf.input_jdf=jdf.jdf_produce()
        return jdf

    def plot_JDF(self):
        xmin=minx([])
        xmax=maxx([])
        ymin=miny([])
        ymax=maxy([])
        self.jdf.get_member("xy_offsets").reset(self.jdf)
        xy_off=self.jdf.xy_offsets
        for p in self.jdf.patterns:
            a=self.agent_dict[p.name]
            verts=[]
            for chip in xy_off.get(p.name, []):
                sPoly(a, x_off=chip[0]*1.0e-6, y_off=chip[1]*1.0e-6, vs=verts)
            self.plot.set_data(a.name, verts, a.color)
            xmin=min([minx(verts), xmin])
            xmax=max([maxx(verts), xmax])
            ymin=min([miny(verts), ymin])
            ymax=max([maxy(verts), ymax])
        self.plot.set_xlim(xmin, xmax)
        self.plot.set_ylim(ymin, ymax)
        self.plot.draw()

    def save_JDF_DXF(self):
        self.jdf.get_member("xy_offsets").reset(self.jdf)
        xy_off=self.jdf.xy_offsets
        verts=[]
        for p in self.jdf.patterns:
            a=self.agent_dict[p.name] #[agent for agent in self.agents if agent.name==p.name][0]
            for chip in xy_off.get(p.name, []):
                sPoly(a, x_off=chip[0]*1.0e-6, y_off=chip[1]*1.0e-6, vs=verts)
        save_dxf(verts, color="green", layer="PADS", file_path="marialasertest.dxf", write_mode="w")

    angle_x=Float(0.3e-6).tag(desc="shift in x direction when doing angle evaporation", unit="um")
    angle_y=Float(0.0e-6).tag(desc="shift in y direction when doing angle evaporation", unit="um")
    view_type=Enum("pattern", "angle")
    add_type=Enum("overwrite", "add")

    save_factory=Callable(Save_TXT)

    pattern_dict=Dict() #for plotting
    patterns=Typed(OrderedDict, ()) #for generating jdf

#    def do_plot(self):
#        for p in self.agents:
#            p.reset_property("polylist")
#            if p.plot_sep:
#                self.plot.set_data(p.name, p.polylist, p.color)
#            #self.pattern_dict[p.name]=dict(verts=p.verts[:], color=p.color, layer=p.layer, plot_sep=p.plot_sep)
#            p.make_name_sug()
#            p.save_file.main_file=p.name_sug+".dxf"
#
#        #for key in self.pattern_dict:
#        #    if self.pattern_dict[key]["plot_sep"]:
#        #        self.plot.set_data(key, self.pattern_dict[key]["verts"], self.pattern_dict[key]["color"])
#
#        xmin=min(b.xmin for b in self.agents)
#        xmax=max(b.xmax for b in self.agents)
#        ymin=min(b.ymin for b in self.agents)
#        ymax=max(b.ymax for b in self.agents)
#        self.plot.set_xlim(xmin, xmax)
#        self.plot.set_ylim(ymin, ymax)
#        self.plot.draw()

    def _default_show_all(self):
        return True

    @cached_property
    def view_window(self):
        with imports():
            from taref.ebl.polygon_chief_e import EBLView
        return EBLView(chief=self)

polygon_chief=Polygon_Chief()

if __name__=="__main__":
    polygon_chief.show()