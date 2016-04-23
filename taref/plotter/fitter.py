# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 14:04:56 2016

@author: thomasaref
"""

from taref.core.agent import Operative
from taref.core.atom_extension import tag_Property
from taref.plotter.plotter import line

class LineFitter(Operative):
    base_name="line_fitter"

    def extra_setup(self, param, typer):
        """adds log_changes observer to all params"""
        super(LineFitter, self).extra_setup(param, typer)
        self.observe(param, self.update_plot)

    @tag_Property(private=True)
    def plotter(self):
        return self.plot_and_format[0]

    @tag_Property(private=True)
    def plot_name(self):
        return self.plot_and_format[1].plot_name

    @tag_Property(private=True)
    def plot_and_format(self):
        return line(self.data, plot_name=self.name)

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
