# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:36:21 2016

@author: thomasaref
"""

from D0514_highfrq1sidelobe import a as d0514
from D0316_S4A1_coupling_midpeak import a as d0316
from D0506_lowfrq34sidelobe import a as d0506
from D0509_lowfrq2sidelobe import a as d0509
from D0503_lowfrq1sidelobe import a as d0503
from numpy import sqrt, linspace
from atom.api import FloatRange
from taref.plotter.fitter import LineFitter2
from taref.plotter.api import line
from taref.core.api import tag_property

pl=d0514.widths_plot()#.show()
d0316.widths_plot(pl=pl)#.show()
d0506.widths_plot(pl=pl)#.show()
d0509.widths_plot(pl=pl)#.show()
d0503.widths_plot(pl=pl)#.show()


class Fitter(LineFitter2):
            f0=FloatRange(4.0, 6.0, d0514.qdt.f0/1e9).tag(tracking=True)
            alpha=FloatRange(0.0, 2.0, 1.0).tag(tracking=True)

            def _default_plotter(self):
                line(*self.data, plot_name=self.plot_name, plotter=pl)
                return pl

            def _default_plot_name(self):
                return "myplot"

            @tag_property(private=True)
            def data(self):
                frq=linspace(3e9,7e9, 1000)
                return frq/1e9, self.alpha*1e9*sqrt(d0514.qdt._get_coupling(f=frq, f0=1e9*self.f0)/d0514.qdt.max_coupling)**2

fit=Fitter()
fit.plotter

pl=d0514.center_plot()#.show()
d0316.center_plot(pl=pl)#.show()
d0506.center_plot(pl=pl)#.show()
d0509.center_plot(pl=pl)#.show()
d0503.center_plot(pl=pl)#.show()

#pl=d0514.magabsfilt_colormesh()
#d0316.magabsfilt_colormesh(pl=pl)#.show()
#d0506.magabsfilt_colormesh(pl=pl)#.show()
#d0509.magabsfilt_colormesh(pl=pl)#.show()
d0503.magabsfilt_colormesh(pl=pl).show()

