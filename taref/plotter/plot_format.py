# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:51:21 2016

@author: thomasaref
"""
from taref.core.log import log_debug
from taref.plotter.plotter_backbone import PlotUpdate, plot_observe
from taref.core.universal import Array
from atom.api import Unicode, Enum, Bool, Float, Typed, cached_property, ContainerList
from numpy import linspace, arange, asanyarray#, array
from taref.core.shower import shower
from enaml import imports
with imports():
    from taref.core.interactive import InteractiveWindow
    from enaml.widgets.color_dialog import ColorDialog


from matplotlib.collections import PolyCollection, LineCollection, QuadMesh, PathCollection
from matplotlib.lines import Line2D

class PlotFormat(PlotUpdate):
    """base class corresponding to one graph or collection on axes"""
    name=Unicode()
    append=Bool(True)
    visible=Bool(True)

    xdata=Array()
    ydata=Array()

    plot_type=Enum("line", "scatter", "multiline", "colormap", "vline", "hline", "polygon")

    def __init__(self, **kwargs):
        super(PlotFormat, self).__init__(**kwargs)
        self.plotter.plot_dict[self.name]=self

    def remove_collection(self):
        if self.clt is not None:
            self.clt.remove()

    def plot_set(self, param):
        self.simple_set(self.clt, param)

    @plot_observe("visible")
    def plot_update(self, change):
        """set the clt's parameter to the obj's value using clt's set function"""
        self.plot_set(change["name"])

    @cached_property
    def view_window(self):
        with imports():
            from plot_format_e import Main
        view=Main(pltr=a.plotter)
        return view
    interactive_window=InteractiveWindow()

def transformation(func):
    """decorator that assists with transfroming from one format to another"""
    def transform_func(self):
        self.remove_collection()
        new_form=func(self)
        new_form.update_plot()
        self.plotter.plot_dict[self.name]=new_form
        del self
    return transform_func

class LineFormat(PlotFormat):
    clt=Typed(Line2D)
    alpha=Float(1.0)
    label=Unicode()
    color=Enum(*PlotUpdate.colors_tuple[1:])
    linewidth=Float(2.0)
    linestyle=Enum('solid', 'dashed', 'dashdot', 'dotted')
    custom_color=ContainerList(default=[0.0, 1.0, 0.0, 1.0])

    def _default_plot_type(self):
        return "line"

    @plot_observe("alpha", "label", "linewidth", "linestyle", update_legend=True)
    def line_update(self, change):
        self.plot_set(change["name"])

    def set_color(self, param, color):
        getattr(self.clt,"set_"+param)(color)

    @plot_observe("color", update_legend=True)
    def color_update(self, change):
        self.plot_set(change["name"])

    def line_plot(self, *args, **kwargs):
        self.remove_collection()
        if len(args)==1:
            y=args[0]
            x=arange(len(y))
        elif len(args)==2:
            x=args[0]
            y=args[1]
        self.xdata=x
        self.ydata=y
        self.clt=self.plotter.axes.plot(x,y, **kwargs)[0]

    @transformation
    def line2scatter(self):
        sf=ScatterFormat(name=self.name, plotter=self.plotter)
        sf.scatter_plot(self.xdata, self.ydata)
        return sf

class VaxisLine(LineFormat):
    def _default_plot_type(self):
        return "vline"

    def axvline(self, x, **kwargs):
        self.remove_collection()
        self.clt=self.plotter.axes.axvline(x, **kwargs)

class HaxisLine(LineFormat):
    def _default_plot_type(self):
        return "hline"

    def axhline(self, y, **kwargs):
        self.remove_collection()
        self.clt=self.plotter.axes.axhline(y, **kwargs)

class ScatterFormat(LineFormat):
    clt=Typed(PathCollection)
    facecolor=Enum(*PlotUpdate.colors_tuple[1:])
    edgecolor=Enum(*PlotUpdate.colors_tuple[1:])
    marker = Enum(*PlotUpdate.markers_tuple)
    marker_size = Float(30.0)

    def _default_plot_type(self):
        return "scatter"

    @plot_observe("marker_size", update_legend=True)
    def marker_size_update(self, change):
        self.clt.set_sizes([self.marker_size])

    @plot_observe("facecolor", "edgecolor", update_legend=True)
    def scatter_update(self, change):
        self.plot_set(change["name"])

    @plot_observe("marker", update_legend=True)
    def marker_update(self, change):
        self.scatter_plot()

    def scatter_plot(self, *args, **kwargs):
        self.remove_collection()
        if len(args)==1:
            self.ydata=args[0]
            self.xdata=arange(len(self.ydata))
        elif len(args)==2:
            self.xdata=args[0]
            self.ydata=args[1]
        self.clt=self.plotter.axes.scatter(self.xdata, self.ydata, marker=self.marker)

    @transformation
    def scatter2line(self):
        lf=LineFormat(name=self.name, plotter=self.plotter)
        lf.line_plot(self.xdata, self.ydata)
        return lf

class ColormeshFormat(PlotFormat):
    clt=Typed(QuadMesh)
    colormap=Enum(*PlotUpdate.colormap_names)
    zdata=Array()

    @plot_observe("colormap")
    def colormap_update(self, change):
        self.clt.set_cmap(self.colormap)

    def _default_plot_type(self):
        return "colormap"

    def pcolormesh(self, *args, **kwargs):
        self.remove_collection()
        if len(args) == 1:
            self.zdata=asanyarray(args[0])
            numRows, numCols = self.zdata.shape
            self.xdata=arange(numCols)
            self.ydata=arange(numRows)
        elif len(args) == 3:
            self.xdata, self.ydata, self.zdata = [asanyarray(a) for a in args]
        self.clt=self.plotter.axes.pcolormesh(self.xdata, self.ydata, self.zdata, **kwargs)

    @transformation
    def colormap2horizlines(self):
        mlf=MultiLineFormat(name=self.name, plotter=self.plotter)
        mlf.multiline_plot([zip(self.xdata, self.zdata[n, :])for n in range(self.ydata.shape[0])])
        mlf.ydata=self.ydata
        return mlf

    @transformation
    def colormap2vertlines(self):
        mlf=MultiLineFormat(name=self.name, plotter=self.plotter)
        mlf.multiline_plot([zip(self.ydata, self.zdata[:, n])for n in range(self.xdata.shape[0])])
        mlf.ydata=self.xdata
        return mlf

class MultiLineFormat(LineFormat, ColormeshFormat):
    clt=Typed(LineCollection)
    color=Enum(*PlotUpdate.colors_tuple)

    def _default_plot_type(self):
        return "multiline"

    @plot_observe("color")
    def color_update(self, change):
        param=change["name"]
        value=getattr(self, param)
        if value=="auto":
            self.autocolor_set(param)
        else:
            self.plot_set(param)

    @plot_observe("colormap")
    def colormap_update(self, change):
        self.clt.set_cmap(self.colormap)
        if self.color=="auto":
            self.autocolor_set("color")

    def autocolor_set(self, param):
        colormap=self.clt.get_cmap()
        length=len(self.clt.get_segments())
        colors = colormap(linspace(0, 1, length))
        getattr(self.clt, "set_"+param)(colors)

    def multiline_plot(self, *args, **kwargs):
        self.xdata=[arg[0] for arg in args[0][0]]
        self.zdata=[[vert[1] for vert in line] for line in args[0]]
        self.clt=LineCollection(args[0])
        self.plotter.axes.add_collection(self.clt)

    @transformation
    def vertlines2colormap(self):
        cmf=ColormeshFormat(name=self.name, plotter=self.plotter)
        cmf.pcolormesh(self.ydata, self.xdata, self.zdata.transpose())
        return cmf

    @transformation
    def horizlines2colormap(self):
        cmf=ColormeshFormat(name=self.name, plotter=self.plotter)
        cmf.pcolormesh(self.xdata, self.ydata, self.zdata)
        return cmf

class AllXYFormat(MultiLineFormat):
    name=Unicode("All")



#    def set_param(self, param, change, index=-1):
#        if change['type']!='create':
#            for key in self.plotter.xyfs.keys():
#                if key!="All":
#                    setattr(self.plotter.xyfs[key], change['name'], change['value'])

if __name__=="__main__":
    from taref.plotter.plotter_backbone import PlotMaster
    pm=PlotMaster()
    from numpy import meshgrid, sqrt
    n = 300
    x = linspace(-1.5, 1.5, n)
    y = linspace(-1.5, 1.5, n*2)
    X, Y = meshgrid(x, y)
    Z = sqrt(X**2 + Y**2)

    a=ColormeshFormat(name="colormesh", plotter=pm)
    a.pcolormesh(Z)
    #a.visible=False


    b=ScatterFormat( name="scatter", plotter=pm)
    b.scatter_plot([100,200,300], [100,200,300])
    data=list([zip([100, 200, 300],[100*q, 200*q, 300*q]) for q in range(3)])
    #c=MultiLineFormat( name="lines", plotter=pm)
    #c.multiline_plot(data)

    #dd=VaxisLine(name="vline", plotter=pm)
    #dd.axvline(30)
    #d=LineFormat(name="lin", plotter=pm)
    #d.line_plot([100,200,300], [100,200,300])
    #d.line2scatter()
    shower(a)
#    from enaml.qt.qt_application import QtApplication
#    from enaml import imports
#    with imports():
#        from plot_format_e import Main
#
#    app = QtApplication()
#    view=Main(pltr=a.plotter, fig=a.plotter.figure)
#    view.show()
#    app.start()
