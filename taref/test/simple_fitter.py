# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 18:26:01 2016

@author: thomasaref
"""

from matplotlib.pyplot import plot, ylim
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from numpy import array, linspace
from atom.api import Atom, FloatRange, Typed, observe, cached_property, Float
from enaml.qt.qt_application import QtApplication
from enaml import imports
with imports():
    from simple_fitter_e import Main

xdata=array([1,2,3])
ydata=array([4,5,6])
ymin=min(ydata)
ymax=max(ydata)
line=plot(xdata, ydata)[0]

class Fitter(Atom):
    a=FloatRange(0.0, 10.0, 1.0)
    b=Float(2.0).tag(low=0.0, high=10.0)

    figure=Typed(Figure)
    fit_line=Typed(Line2D)

    def _default_fit_line(self):
        return plot(self.xfit, self.yfit)[0]

    def _default_figure(self):
        return self.fit_line.figure

    @cached_property
    def xfit(self):
        return linspace(0, 4, 20)


    @cached_property
    def yfit(self):
        return self.b*self.xfit+self.a

    @observe("a", "b")
    def change_parameters(self, change):
        if change["type"]=="update":
            self.get_member("yfit").reset(self)
            self.fit_line.set_ydata(self.yfit)
            self.draw()

    def autoscale_y(self):
        ylim(min(min(self.yfit), ymin), max(max(self.yfit), ymax))
        self.draw()

    def draw(self):
        if self.figure.canvas!=None:
            self.figure.canvas.draw()

fit=Fitter()

app = QtApplication()
view=Main(fitter=fit)
view.show()
app.start()
