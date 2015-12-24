# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 18:23:12 2015

@author: thomasaref
"""

from taref.core.chief import Chief
from taref.core.save_file import Save_TXT
#from taref.core.log import log_info
from atom.api import Typed, Float, Enum, Callable, Dict
from enaml import imports
from collections import OrderedDict

class Polygon_Chief(Chief):
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