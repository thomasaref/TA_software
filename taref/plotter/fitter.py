# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:04:56 2016

@author: thomasaref
"""

from taref.core.agent import Operative
from taref.core.api import get_all_tags, get_tag
#from taref.core.atom_extension import tag_property
from taref.plotter.plotter import line, Plotter
from atom.api import Typed, Unicode
from taref.core.universal import ODict

class LineFitter2(Operative):
    base_name="line_fitter"

    plotter=Typed(Plotter).tag(private=True)
    plot_name=Unicode().tag(private=True)
    data_dict=ODict().tag(private=True)

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        super(LineFitter2, self).extra_setup(param, typer)
        self.observe(param, self.update_plot)

    def _default_plotter2(self):
        if self.plot_name=="":
            self.plot_name=self.name
        pl=Plotter(name=self.name)
        for param in get_all_tags(self, "plot"):
            print param
            pl, pf=line(*getattr(self, param), plot_name=get_tag(self, param, "plot"), plotter=pl)
            self.data_dict[param]=pf.plot_name
        return pl

    def update_plot(self, change):
        if change["type"]=="update":
            #for param, plot_name in self.data_dict.iteritems():
            #    print param, plot_name
            self.get_member("data").reset(self)
                #self.plotter.plot_dict[plot_name].clt.set_xdata(getattr(self, param)[0])
                #self.plotter.plot_dict[plot_name].clt.set_ydata(getattr(self, param)[1])
                #self.plotter.draw()

            self.plotter.plot_dict[self.plot_name].alter_xy(*getattr(self,"data"))

class LineFitter(Operative):
    base_name="line_fitter"

    plotter=Typed(Plotter).tag(private=True)
    plot_name=Unicode().tag(private=True)
    data_dict=ODict().tag(private=True)

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        super(LineFitter, self).extra_setup(param, typer)
        self.observe(param, self.update_plot)

    def _default_plotter(self):
        if self.plot_name=="":
            self.plot_name=self.name
        pl=Plotter(name=self.name)
        for param in get_all_tags(self, "plot"):
            print param
            pl, pf=line(*getattr(self, param), plot_name=get_tag(self, param, "plot"), plotter=pl, pf_too=True)
            self.data_dict[param]=pf.plot_name
        return pl

    def update_plot(self, change):
        if change["type"]=="update":
            for param, plot_name in self.data_dict.iteritems():
                #print param, plot_name
                self.get_member(param).reset(self)
                #self.plotter.plot_dict[plot_name].clt.set_xdata(getattr(self, param)[0])
                #self.plotter.plot_dict[plot_name].clt.set_ydata(getattr(self, param)[1])
                #self.plotter.draw()

                self.plotter.plot_dict[plot_name].alter_xy(*getattr(self,param))


if __name__=="__main__":
    a=LineFitter()
    print get_tag(a, "plotter", "private")
#    class Fitter(LineFitter):
#        Ejmax=FloatRange(0.001, 100.0, 40.0).tag(tracking=True)
#        offset=FloatRange(0.0, 100.0, 18.0).tag(tracking=True)
#
#        @tag_Property(private=True)
#        def data(self):
#            return a.flux_parabola(linspace(-1,1,100), self.offset, a.flux_factor, self.Ejmax*h, a.Ec)
