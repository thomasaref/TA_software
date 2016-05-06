# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:04:56 2016

@author: thomasaref
"""

from taref.core.agent import Operative
#from taref.core.atom_extension import tag_property
from taref.plotter.plotter import line, Plotter
from atom.api import Typed, Unicode

class LineFitter(Operative):
    base_name="line_fitter"

    plotter=Typed(Plotter).tag(private=True)
    plot_name=Unicode().tag(private=True)

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        super(LineFitter, self).extra_setup(param, typer)
        self.observe(param, self.update_plot)

    #@tag_Property(private=True)
    #def plotter(self):
    #    return self.plot_and_format[0]

    def _default_plotter(self):
        if self.plot_name=="":
            self.plot_name=self.name
        pl, pf=line(self.data, plot_name=self.plot_name)
        self.plot_name=pf.plot_name
        return pl

    #@tag_Property(private=True)
    #def plot_name(self):
    #    return self.plot_and_format[1].plot_name

    #@tag_Property(private=True)
    #def plot_and_format(self):
    #    if self.plotter is None:
    #        line(self.data, plot_name=self.name)

    def update_plot(self, change):
        if change["type"]=="update":
            self.get_member("data").reset(self)
            self.plotter.plot_dict[self.plot_name].alter_xy(self.data)


if __name__=="__main__":
    from taref.core.api import get_tag
    a=LineFitter()
    print get_tag(a, "plotter", "private")
#    class Fitter(LineFitter):
#        Ejmax=FloatRange(0.001, 100.0, 40.0).tag(tracking=True)
#        offset=FloatRange(0.0, 100.0, 18.0).tag(tracking=True)
#
#        @tag_Property(private=True)
#        def data(self):
#            return a.flux_parabola(linspace(-1,1,100), self.offset, a.flux_factor, self.Ejmax*h, a.Ec)
