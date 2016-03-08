# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:51:21 2016

@author: thomasaref
"""
from taref.core.log import log_debug
from taref.plotter.plotter_backbone import PlotUpdate, plot_observe, colors_tuple, markers_tuple, colormap_names
from taref.core.universal import Array
from atom.api import Unicode, Enum, Bool, Float, Typed, cached_property, ContainerList, Int, Dict, Instance
from numpy import linspace, arange, asanyarray
from taref.core.shower import shower
from taref.core.atom_extension import get_all_tags, get_tag
from enaml import imports
with imports():
    from taref.core.interactive_e import InteractiveWindow



from matplotlib.collections import PolyCollection, LineCollection, QuadMesh, PathCollection
from matplotlib.lines import Line2D
from matplotlib.colorbar import Colorbar

class PlotFormat(PlotUpdate):
    """base class corresponding to one graph or collection on axes"""
    name=Unicode()
    append=Bool(True)

    xcoord=Float()
    ycoord=Float()
    xind=Int()
    yind=Int()

    visible=Bool(True).tag(former="visible")

    xdata=Array()
    ydata=Array()

    plot_type=Enum("line", "scatter", "multiline", "colormap", "vline", "hline", "polygon", "cross_cursor")

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

    def process_kwargs(self, kwargs):
        for arg in get_all_tags(self, "former"):
            if arg in kwargs:
                setattr(self, arg, kwargs[arg])
            key=get_tag(self, arg, "former", arg)
            kwargs[key]=kwargs.pop(arg, getattr(self, arg))
        return kwargs

    @cached_property
    def view_window(self):
        with imports():
            from plot_format_e import Main
        view=Main(pltr=self.plotter)
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
    alpha=Float(1.0).tag(former="alpha")
    label=Unicode().tag(former="label")
    color=Enum(*colors_tuple[1:]).tag(former="c")
    linewidth=Float(2.0).tag(former="linewidth")
    linestyle=Enum('solid', 'dashed', 'dashdot', 'dotted').tag(former="linestyle")
    custom_color=ContainerList(default=[0.0, 1.0, 0.0, 1.0])

    def _default_plot_type(self):
        return "line"

    @plot_observe("alpha", "label", "linewidth", "linestyle", "color", update_legend=True)
    def line_update(self, change):
        self.plot_set(change["name"])

    def set_color(self, param, color):
        getattr(self.clt,"set_"+param)(color)


class Line2DFormat(LineFormat):
    def line_plot(self, *args, **kwargs):
        kwargs=self.process_kwargs(kwargs)
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

def line_plot(plotter, name, *args, **kwargs):
    pl0t=Line2DFormat(name=name, plotter=plotter)
    pl0t.line_plot(*args, **kwargs)
    return pl0t


class VaxisLine(LineFormat):
    def _default_plot_type(self):
        return "vline"

    def axvline(self, x, **kwargs):
        kwargs=self.process_kwargs(kwargs)
        self.remove_collection()
        self.clt=self.plotter.axes.axvline(x, **kwargs)

def vline_plot(plotter, name, x, **kwargs):
    pl0t=VaxisLine(name=name, plotter=plotter)
    pl0t.axvline(x, **kwargs)
    return pl0t

class HaxisLine(LineFormat):
    def _default_plot_type(self):
        return "hline"

    def axhline(self, y, **kwargs):
        kwargs=self.process_kwargs(kwargs)
        self.remove_collection()
        self.clt=self.plotter.axes.axhline(y, **kwargs)

def hline_plot(plotter, name, y, **kwargs):
    pl0t=HaxisLine(name=name, plotter=plotter)
    pl0t.axhline(y, **kwargs)
    return pl0t

class CrossCursor(LineFormat):
    clt=Dict(default={"h_line":None, "v_line":None, "h_axe":None, "v_axe" : None})

    def _default_name(self):
        return "cross_cursor"

    def _default_plot_type(self):
        return "cross_cursor"

    def _default_alpha(self):
        return 0.8

    def _default_color(self):
        return "black"

    def _default_linewidth(self):
        return 0.5

    def _default_linestyle(self):
        return "dashed"

    def remove_collection(self):
        for item in self.clt.values():
            if item is not None:
                item.remove()

    def add_cursor(self, x, y, **kwargs):
        kwargs=self.process_kwargs(kwargs)
        self.remove_collection()
        self.clt=dict(h_line=self.plotter.axes.axhline(y, **kwargs),
                      v_line=self.plotter.axes.axvline(x, **kwargs),
                      v_axe=self.plotter.vert_axe.axhline(y, **kwargs),
                      h_axe=self.plotter.horiz_axe.axvline(x, **kwargs))

    def move_cursor(self, x, y):
        self.clt["v_line"].set_xdata([x,x])
        self.clt["h_line"].set_ydata([y,y])
        self.clt["h_axe"].set_xdata([x,x])
        self.clt["v_axe"].set_ydata([y,y])


    @plot_observe("alpha", "label", "linewidth", "linestyle", "color")
    def line_update(self, change):
        self.plot_set(change["name"])

    def plot_set(self, param):
        for item in self.clt.values():
            self.simple_set(item, param)

    def set_color(self, param, color):
        for item in self.clt.values():
            getattr(item,"set_"+param)(color)

#def cross_cursor(plotter, name, x, y, **kwargs):
#    pl0t=CrossCursor(name=name, plotter=plotter)
#    pl0t.add_cursor(x, y, **kwargs)
#    return pl0t


class ScatterFormat(LineFormat):
    clt=Typed(PathCollection)
    facecolor=Enum(*colors_tuple[1:]).tag(former="facecolor")
    edgecolor=Enum(*colors_tuple[1:]).tag(former="edgecolor")
    marker = Enum(*markers_tuple).tag(former="marker")
    marker_size = Float(30.0).tag(former="s")

    substitution_dict={"marker_size" : "s", "color" : "c"}

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
        kwargs=self.process_kwargs(kwargs)
        self.remove_collection()
        if len(args)==1:
            self.ydata=args[0]
            self.xdata=arange(len(self.ydata))
        elif len(args)==2:
            self.xdata=args[0]
            self.ydata=args[1]
        self.clt=self.plotter.axes.scatter(self.xdata, self.ydata, **kwargs)

    @transformation
    def scatter2line(self):
        lf=LineFormat(name=self.name, plotter=self.plotter)
        lf.line_plot(self.xdata, self.ydata)
        return lf

def scatter_plot(plotter, name, *args, **kwargs):
    pl0t=ScatterFormat(name=name, plotter=plotter)
    pl0t.scatter_plot(*args, **kwargs)
    return pl0t


class ColormeshFormat(PlotFormat):
    clt=Typed(QuadMesh)
    cmap=Enum(*colormap_names).tag(former="cmap")
    zdata=Array()
    vmin=Float()
    vmax=Float()

    colorbar=Instance(Colorbar)

    def set_clim(self, vmin, vmax):
        self.clt.set_clim(vmin, vmax)

    @plot_observe("vmin", "vmax")
    def clim_update(self, change):
        self.set_clim(self.vmin, self.vmax)

    def _default_colorbar(self):
        self.plotter.figure.colorbar(self.clt)

    @plot_observe("cmap")
    def colormap_update(self, change):
        self.plot_set(change["name"])

    def _default_plot_type(self):
        return "colormap"

    def pcolormesh(self, *args, **kwargs):
        kwargs=self.process_kwargs(kwargs)
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
        mlf.autocolor_set("color")
        return mlf

    @transformation
    def colormap2vertlines(self):
        mlf=MultiLineFormat(name=self.name, plotter=self.plotter)
        mlf.multiline_plot([zip(self.ydata, self.zdata[:, n])for n in range(self.xdata.shape[0])])
        mlf.ydata=self.xdata
        mlf.autocolor_set("color")
        return mlf

def colormesh(plotter, name, *args, **kwargs):
    pl0t=ColormeshFormat(name=name, plotter=plotter)
    pl0t.pcolormesh(*args, **kwargs)
    pl0t.colorbar
    return pl0t

class MultiLineFormat(LineFormat, ColormeshFormat):
    clt=Typed(LineCollection)
    color=Enum(*colors_tuple)

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
        kwargs=self.process_kwargs(kwargs)
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

def multiline_plot(plotter, name, *args, **kwargs):
    pl0t=MultiLineFormat(name=name, plotter=plotter)
    pl0t.multiline_plot(*args, **kwargs)
    return pl0t

#class AllXYFormat(MultiLineFormat):
#    name=Unicode("All")



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
