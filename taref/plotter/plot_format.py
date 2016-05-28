# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:51:21 2016

@author: thomasaref
"""
from taref.core.log import log_debug
from taref.plotter.plotter_backbone import PlotUpdate, plot_observe, colors_tuple, markers_tuple, colormap_names, simple_set, process_kwargs
from taref.core.universal import Array, name_generator
from atom.api import Unicode, Enum, Bool, Float, Typed, cached_property, ContainerList, Int, Dict, observe, ReadOnly
from numpy import linspace, arange, asanyarray, append, amax, amin, ndarray, nanmax, nanmin
from taref.core.shower import shower
from taref.core.atom_extension import get_all_tags, get_tag, set_tag, check_initialized, defaulter

from enaml import imports
with imports():
    from taref.core.interactive_e import InteractiveWindow

from matplotlib.collections import PolyCollection, LineCollection, QuadMesh, PathCollection
from matplotlib.lines import Line2D
from matplotlib.colorbar import Colorbar

#def defaulter(self, name, kwargs):
#    if name in kwargs:
#        return kwargs.pop(name)
#    default=self.get_member(name).default_value_mode
#    if default[0]==1:
#        return default[1]
#    elif default[0]==8:
#        return getattr(self, default[1])()
#    elif default[0]==5:
#        return default[1]()
#
#def name_generator(self, name, indict, suffix="__{0}"):
#    if name in indict:
#        name+=suffix.format(len(indict.keys()))
#    return name
def Array2():
    return Typed(ndarray)

class PlotFormat(PlotUpdate):
    """base class corresponding to one graph or collection on axes"""
    plot_name=ReadOnly()

    #def _default_plot_name(self):
    #    return self.plot_type

    #def _observe_plot_name(self, change):
    #    check_initialized(self, change)

    append=Bool(False)
    remove=Bool(False)

    xcoord=Float()
    ycoord=Float()
    xind=Int()
    yind=Int()

#    x_min=Float()
#    x_max=Float()
#    y_min=Float()
#    y_max=Float()
#
#    def _default_x_min(self):
#        return min(self.xdata)
#
#    def _default_x_max(self):
#        return max(self.xdata)
#
#    def _default_y_min(self):
#        return min(self.ydata)
#
#    def _default_y_max(self):
#        return max(self.ydata)

    def do_autolim(self):
        if self.plotter.auto_xlim:
            self.plotter.x_min=float(min((self.plotter.x_min, nanmin(self.xdata))))
            self.plotter.x_max=float(max((self.plotter.x_max, nanmax(self.xdata))))
        if self.plotter.auto_ylim:
            self.plotter.y_min=float(min((self.plotter.y_min, nanmin(self.ydata))))
            self.plotter.y_max=float(max((self.plotter.y_max, nanmax(self.ydata))))


    xdata=Array2()
    ydata=Array2()

    plot_type=Enum("line", "scatter", "multiline", "colormap", "vline", "hline", "polygon", "cross_cursor")

    clt=Typed(Line2D)

    visible=Bool(True).tag(former="visible")

    def clt_values(self):
        if isinstance(self.clt, dict):
            return self.clt.values()
        return [self.clt]

    def plot_set(self, param):
        for clt in self.clt_values():
            simple_set(clt, self, get_tag(self, param, "former", param))

    @plot_observe("visible")
    def plot_update(self, change):
        """set the clt's parameter to the obj's value using clt's set function"""
        self.plot_set(change["name"])

    def remove_collection(self):
        if self.remove:
            if self.clt is not None:
                self.clt.remove()

    def __init__(self, **kwargs):
        plot_name=defaulter(self, "plot_name", kwargs)
        plotter=kwargs["plotter"]
        #if plot_name in plotter.plot_dict:
        #    if self.remove:
        #        self.remove_collection()
        #    else:
        plot_name=name_generator(plot_name, plotter.plot_dict, kwargs.get("plot_type", self.plot_type))
        self.plot_name=plot_name

        super(PlotFormat, self).__init__(**kwargs)
        #if plot_name is None:
        #    plot_name=self.plot_type
        #if agent_name in Operative.agent_dict:
        #    agent_name="{name}__{num}".format(name=agent_name, num=len(Operative.agent_dict))
        #kwargs["name"]=agent_name
        #Operative.agent_dict[agent_name]=self
        #        plot_name+="__{0}".format(len(self.plotter.plot_dict.keys()))
        #self.plot_name=plot_name
        #set_tag(self, "plot_name", initialized=False)
        #if self.plot_name=="":
        #    self.plot_name=self.plot_type
        #if self.plot_name in self.plotter.plot_dict:
        #    if self.remove:
        #        self.remove_collection()
        #    else:
        #        self.plot_name+="__{0}".format(len(self.plotter.plot_dict.keys()))
        self.plotter.plot_dict[self.plot_name]=self
        #set_tag(self, "plot_name", initialized=True)

    @cached_property
    def view_window(self):
        with imports():
            from plot_format_e import Main
        view=Main(pltr=self.plotter)
        return view

def transformation(func):
    """decorator that assists with transfroming from one format to another"""
    def transform_func(self):
        self.remove_collection()
        new_form=func(self)
        new_form.update_plot()
        self.plotter.plot_dict[self.plot_name]=new_form
        del self
    return transform_func

class LineFormat(PlotFormat):
    custom_color=ContainerList(default=[0.0, 1.0, 0.0, 1.0])

    def _default_plot_type(self):
        return "line"

    alpha=Float(1.0).tag(former="alpha")
    label=Unicode().tag(former="label")
    color=Enum(*colors_tuple[1:]).tag(former="color")
    linewidth=Float(2.0).tag(former="linewidth")
    linestyle=Enum('solid', 'dashed', 'dashdot', 'dotted').tag(former="linestyle")

    @plot_observe("alpha", "label", "linewidth", "linestyle", "color", update_legend=True)
    def line_update(self, change):
        self.plot_set(change["name"])


class Line2DFormat(LineFormat):
    def line_plot(self, *args, **kwargs):
        kwargs=process_kwargs(self, kwargs)
        self.remove_collection()
        if len(args)==1:
            y=args[0]
            x=arange(len(y))
        elif len(args)==2:
            x=args[0]
            y=args[1]
        self.xdata=x
        self.ydata=y
        self.clt=self.plotter.axes.plot(*args, **kwargs)[0]
        self.do_autolim()

    def alter_xy(self, *args):
        """appends points x and y if 2 args are passed and just y and len of xdata if one args is passed"""
        #if len(args)==1:
        #    y=args[0]
        #    x=None #range(len(self.xdata))
        #elif len(args)==2:
        #    print "arg 2"
        x=args[0]
        y=args[1]
        #print x.shape, y.shape
        #if self.append:
        #    if x is None:
        #        x=len(self.xdata)
        #    self.xdata=append(self.xdata, x)
        #    self.ydata=append(self.ydata, y)
        #else:
        #    if x is None:
        #        x=self.clt.get_xdata()
        self.xdata=x
        self.ydata=y
        self.clt.set_xdata(self.xdata)
        self.clt.set_ydata(self.ydata)
        #self.plotter.set_xlim(min(self.xdata), max(self.xdata))
        #self.plotter.set_ylim(min(self.ydata), max(self.ydata))
        self.update_plot(update_legend=False)
        #fig=self.clt.get_figure()

        #if fig.canvas is not None:
        #    fig.canvas.draw()

    @transformation
    def line2scatter(self):
        sf=ScatterFormat(plot_name=self.plot_name, plotter=self.plotter)
        sf.scatter_plot(self.xdata, self.ydata)
        return sf

def line_plot(plotter, *args, **kwargs):
    plot_name=kwargs.pop("plot_name", None)
    pl0t=Line2DFormat(plot_name=plot_name, plotter=plotter)
    pl0t.line_plot(*args, **kwargs)
    return pl0t


class VaxisLine(LineFormat):
    def _default_plot_type(self):
        return "vline"

    def axvline(self, *args, **kwargs):
        kwargs=process_kwargs(self, kwargs)
        self.remove_collection()
        self.clt=self.plotter.axes.axvline(*args, **kwargs)

def vline_plot(plotter, *args, **kwargs):
    plot_name=kwargs.pop("plot_name", "")
    pl0t=VaxisLine(plot_name=plot_name, plotter=plotter)
    pl0t.axvline(*args, **kwargs)
    return pl0t

class HaxisLine(LineFormat):
    def _default_plot_type(self):
        return "hline"

    def axhline(self, y, **kwargs):
        kwargs=process_kwargs(self, kwargs)
        self.remove_collection()
        self.clt=self.plotter.axes.axhline(y, **kwargs)

def hline_plot(plotter, *args, **kwargs):
    plot_name=kwargs.pop("plot_name", "")
    pl0t=HaxisLine(plot_name=plot_name, plotter=plotter)
    pl0t.axhline(*args, **kwargs)
    return pl0t

class CrossCursor(LineFormat):
    clt=Dict(default={"h_line":None, "v_line":None, "h_axe":None, "v_axe" : None})

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
        kwargs=process_kwargs(self, kwargs)
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

class ScatterFormat(LineFormat):
    clt=Typed(PathCollection)

    marker = Enum(*markers_tuple)
    marker_size = Float(1.0).tag(former="s")

    facecolor=Enum(*colors_tuple[1:]).tag(former="facecolor")
    edgecolor=Enum(*colors_tuple[1:]).tag(former="edgecolor")

    @plot_observe("facecolor", "edgecolor", update_legend=True)
    def scatter_update(self, change):
        self.plot_set(change["name"])

    @plot_observe("marker_size", update_legend=True)
    def marker_size_update(self, change):
        self.clt.set_sizes([self.marker_size])

    @plot_observe("marker", update_legend=True)
    def marker_update(self, change):
        self.scatter_plot()

    def _default_plot_type(self):
        return "scatter"

    def scatter_plot(self, *args, **kwargs):
        kwargs=process_kwargs(self, kwargs)
        self.remove_collection()
        if len(args)==1:
            self.ydata=args[0]
            self.xdata=arange(len(self.ydata))
        elif len(args)==2:
            self.xdata=args[0]
            self.ydata=args[1]
        self.clt=self.plotter.axes.scatter(self.xdata, self.ydata, **kwargs)
        self.do_autolim()

    @transformation
    def scatter2line(self):
        lf=Line2DFormat(plot_name=self.plot_name, plotter=self.plotter)
        lf.line_plot(self.xdata, self.ydata)
        return lf

def scatter_plot(plotter, *args, **kwargs):
    plot_name=kwargs.pop("plot_name", "")
    pl0t=ScatterFormat(plot_name=plot_name, plotter=plotter)
    pl0t.scatter_plot(*args, **kwargs)
    return pl0t

class ColormeshFormat(PlotFormat):
    clt=Typed(QuadMesh)
    zdata=Array2()

    cmap=Enum(*colormap_names).tag(former="cmap")

    @plot_observe("cmap")
    def colormap_update(self, change):
        self.plot_set(change["name"])
        self.set_colorbar()

    @plot_observe("plotter.selected")
    def colorbar_update(self, change):
        if self.plotter.selected==self.plot_name:
            self.set_colorbar()

    def get_colorbar(self):
        if self.plotter.colorbar is None:
            self.plotter.colorbar=self.plotter.figure.colorbar(self.clt)
        return self.plotter.colorbar

    def set_colorbar(self):
        self.get_colorbar().update_bruteforce(self.clt)

    def set_clim(self, vmin, vmax):
        self.vmin=float(vmin)
        self.vmax=float(vmax)
        self.clt.set_clim(vmin, vmax)
        self.set_colorbar()

    @plot_observe("vmin", "vmax")
    def clim_update(self, change):
        self.set_clim(self.vmin, self.vmax)

    vmin=Float()
    vmax=Float()

    def _default_plot_type(self):
        return "colormap"

    h_line=Typed(Line2D)
    v_line=Typed(Line2D)


    cs_alpha=Float(1.0)
    cs_color=Enum(*colors_tuple[1:])
    cs_linewidth=Float(2.0)
    cs_linestyle=Enum('solid', 'dashed', 'dashdot', 'dotted')

    def cs_set(self, param):
        getattr(self.h_line, "set_"+param[3:])(getattr(self, param))
        getattr(self.v_line, "set_"+param[3:])(getattr(self, param))

    @observe("cs_alpha", "cs_linewidth", "cs_linestyle", "cs_color")
    def cs_update(self, change):
        if change["type"]=="update":
            self.cs_set(change["name"])
            if self.plotter.horiz_fig.canvas!=None:
                self.plotter.horiz_fig.canvas.draw()
            if self.plotter.vert_fig.canvas!=None:
                self.plotter.vert_fig.canvas.draw()

    def do_autolim(self):
        if self.plotter.auto_zlim:
            self.set_clim(nanmin(self.zdata), nanmax(self.zdata))
        super(ColormeshFormat, self).do_autolim()

    def pcolormesh(self, *args, **kwargs):
        kwargs=process_kwargs(self, kwargs)
        self.remove_collection()
        if len(args) == 1:
            #if isinstance(args[0], tuple):
            #    self.zdata=zeros(args[0])
            #else:
            self.zdata=asanyarray(args[0])
            numRows, numCols = self.zdata.shape
            self.xdata=arange(numCols)
            self.ydata=arange(numRows)
        #elif len(args)==2:
        #    args=args+(zeros((len(self.xdata)-1, len(self.ydata)-1)),)
        #    self.xdata, self.ydata, self.zdata= [asanyarray(a) for a in args]
        elif len(args) == 3:
            self.xdata, self.ydata, self.zdata = [asanyarray(a) for a in args]
        self.clt=self.plotter.axes.pcolormesh(self.xdata, self.ydata, self.zdata, **kwargs)
        self.do_autolim()
        #if self.plotter.auto_xlim:
        #    self.plotter.set_xlim(min(self.xdata), max(self.xdata))
        #if self.plotter.auto_ylim:
        #    self.plotter.set_ylim(min(self.ydata), max(self.ydata))
        #if self.plotter.auto_xlim:
        #    self.plotter.x_min=float(min((self.plotter.x_min, min(self.xdata))))
        #    self.plotter.x_min=float(max((self.plotter.x_min, max(self.xdata))))

            #self.plotter.set_xlim(min(self.xdata), max(self.xdata))
        #if self.plotter.auto_ylim:
        #    self.plotter.y_min=float(min((self.plotter.y_min, min(self.ydata))))
        #    self.plotter.y_min=float(max((self.plotter.y_min, max(self.ydata))))


    count=Int()
    def append_xy(self, z, index=None, axis=1):
        """appends points x and y if 2 args are passed and just y and len of xdata if one args is passed"""
        if index is None:
            index=self.count
            self.count+=1
        if axis==1:
            self.zdata[ : , index ]=z
        else:
            self.zdata[index, :]=z
        self.clt.set_array(self.zdata.ravel())
        self.set_clim(amin(self.zdata), amax(self.zdata))
        #print dir(self.clt)
        #print dir(self.clt.get_axes())
        #print self.clt.get_axes().get_xlim()
        #print help(self.clt.get_axes().update_datalim)
        #print help(self.clt.set_axis)
        #self.clt.set_xdata(self.xdata)
        #self.pcolormesh(self.xdata, self.ydata, self.zdata)
        self.update_plot(update_legend=False)
        #fig=self.clt.get_figure()
        #if fig.canvas is not None:
        #    fig.canvas.draw()


    @transformation
    def colormap2horizlines(self):
        mlf=MultiLineFormat(plot_name=self.plot_name, plotter=self.plotter)
        mlf.multiline_plot([zip(self.xdata, self.zdata[n, :])for n in range(self.ydata.shape[0])])
        mlf.ydata=self.ydata
        mlf.autocolor_set("color")
        return mlf

    @transformation
    def colormap2vertlines(self):
        mlf=MultiLineFormat(plot_name=self.plot_name, plotter=self.plotter)
        mlf.multiline_plot([zip(self.ydata, self.zdata[:, n])for n in range(self.xdata.shape[0])])
        mlf.ydata=self.xdata
        mlf.autocolor_set("color")
        return mlf

def colormesh_plot(plotter, *args, **kwargs):
    plot_name=kwargs.pop("plot_name", None)
    pl0t=ColormeshFormat(plot_name=plot_name, plotter=plotter)
    pl0t.pcolormesh(*args, **kwargs)
    #pl0t.colorbar
    return pl0t

class MultiLineFormat(LineFormat, ColormeshFormat):
    clt=Typed(LineCollection)
    color=Enum(*colors_tuple)

    def _default_plot_type(self):
        return "multiline"

    @plot_observe("color")
    def color_update(self, change):
        param=change["plot_name"]
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
        kwargs=process_kwargs(self, kwargs)
        self.xdata=[arg[0] for arg in args[0][0]]
        self.zdata=[[vert[1] for vert in line] for line in args[0]]
        self.clt=LineCollection(args[0])
        self.plotter.axes.add_collection(self.clt)

    @transformation
    def vertlines2colormap(self):
        cmf=ColormeshFormat(plot_name=self.plot_name, plotter=self.plotter)
        cmf.pcolormesh(self.ydata, self.xdata, self.zdata.transpose())
        return cmf

    @transformation
    def horizlines2colormap(self):
        cmf=ColormeshFormat(plot_name=self.plot_name, plotter=self.plotter)
        cmf.pcolormesh(self.xdata, self.ydata, self.zdata)
        return cmf

def multiline_plot(plotter, *args, **kwargs):
    plot_name=kwargs.pop("plot_name", "")
    pl0t=MultiLineFormat(plot_name=plot_name, plotter=plotter)
    pl0t.multiline_plot(*args, **kwargs)
    return pl0t

if __name__=="__main__":
    from taref.plotter.plotter_backbone import PlotMaster
    pm=PlotMaster(show_cross_section=True)
    from numpy import meshgrid, sqrt, array, full, NaN, zeros
    n = 300
    x = linspace(-1.5, 1.5, n)
    y = linspace(-1.5, 1.5, n*2)
    print pm
    #a=scatter_plot(pm, "blah",  x)
    #shower(a)
    X, Y = meshgrid(x, y)
    Z = sqrt(X**2 + Y**2)

    a=ColormeshFormat( plotter=pm)

    #a.pcolormesh(x, y, Z)

    a.pcolormesh(linspace(-1.5, 1.5, n+1), linspace(-1.5, 1.5, n*2+1), zeros((600,300)))
    shower(a)
    #a.visible=False


    b=ScatterFormat( plot_name="scatter", plotter=pm)
    b.scatter_plot([100,200,300], [100,200,300])
    data=list([zip([100, 200, 300],[100*q, 200*q, 300*q]) for q in range(3)])
    #c=MultiLineFormat( plot_name="lines", plotter=pm)
    #c.multiline_plot(data)

    #dd=VaxisLine(plot_name="vline", plotter=pm)
    #dd.axvline(30)
    #d=LineFormat(plot_name="lin", plotter=pm)
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
