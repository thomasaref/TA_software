# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 18:23:12 2015

@author: thomasaref
"""

from a_Chief import Chief
from Atom_Save_File import Save_TXT
from LOG_functions import log_info
from atom.api import Typed, Float, Enum, Callable, Dict
from enaml import imports
from collections import OrderedDict
#from enaml import imports
#from enaml.qt.qt_application import QtApplication#

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
            self.pattern_dict[p.name]=dict(verts=p.verts[:], color=p.color, layer=p.layer, plot_sep=p.plot_sep)
            p.make_name_sug()
            p.save_file.main_file=p.name_sug+".dxf"

        for key in self.pattern_dict:
            if self.pattern_dict[key]["plot_sep"]:
                self.plot.set_data(key, self.pattern_dict[key]["verts"], self.pattern_dict[key]["color"])

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
            from e_Show import EBLView
        return EBLView(chief=self)

polygon_chief=Polygon_Chief()

#class EBL_Boss(Chief):
#    plot=Typed(Plotter, ())
#    
#    def _default_show_agents(self):
#        return True
#
#    def _default_save_factory(self):
#        return Save_DXF
#
#    def run_measurement(self):
#        log_info("EBL Master started")
#        self.run()
#        log_info("EBL Master finished")

 #   def show(self, base=None): #needs some work
 #       """stand alone for showing instrument. Shows a modified boss view that has the instrument as a dockpane"""
 #       with imports():
 #           from EBL_enaml import EBMain
 #       app = QtApplication()
 #       view = EBMain(base=base, boss=self)
 #       view.show()
 #       app.start()
#    def show(self):
#        with imports():
#            from enaml_Boss import MasterMain
#        try:
#            app = QtApplication()
#            view = MasterMain(boss=self)
#            view.show()
#            app.start()
#        finally:
#            if self.saving:
#                self.save_file.flush_buffers()

#ebl_boss=EBL_Boss()