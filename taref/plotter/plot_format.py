# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:51:21 2016

@author: thomasaref
"""
from taref.core.log import log_debug
from taref.plotter.plotter_backbone import PlotUpdate, plot_observe, colors_tuple, markers_tuple, colormap_names, SimpleSetter
from taref.core.universal import Array
from atom.api import Unicode, Enum, Bool, Float, Typed, cached_property, ContainerList, Int, Dict, Instance, Atom
from numpy import linspace, arange, asanyarray, append, amax, amin
from taref.core.shower import shower
from taref.core.atom_extension import get_all_tags, get_tag
from enaml import imports
with imports():
    from taref.core.interactive_e import InteractiveWindow

from matplotlib.collections import PolyCollection, LineCollection, QuadMesh, PathCollection
from matplotlib.lines import Line2D
from matplotlib.colorbar import Colorbar

class MPL_Format(SimpleSetter):
    """format class for those attributes with a direct correspondence to mpl attributes"""
    visible=Bool(True)#.tag(former="visible")
    _parent=Typed(PlotUpdate)

    def clt_values(self):
        if isinstance(self._parent.clt, dict):
            return self._parent.clt.values()
        return [self._parent.clt]

    def plot_set(self, param):
        for clt in self.clt_values():
            self.simple_set(clt, self, get_tag(self, param, "former", param))

    @plot_observe("visible")
    def plot_update(self, change):
        """set the clt's parameter to the obj's value using clt's set function"""
        self.plot_set(change["name"])

    def process_kwargs(self, kwargs):
        for arg in self.members():
            #for arg in get_all_tags(self, "former"):
            if not arg.startswith("_"):
            #if arg not in ("clt",):

                if arg in kwargs:
                    setattr(self, arg, kwargs[arg])
                key=get_tag(self, arg, "former", arg)
                kwargs[key]=kwargs.pop(arg, getattr(self, arg))
        return kwargs

class PlotFormat(PlotUpdate):
    """base class corresponding to one graph or collection on axes"""
    name=Unicode()
    append=Bool(True)
    remove=Bool(True)

    xcoord=Float()
    ycoord=Float()
    xind=Int()
    yind=Int()

    #visible=Bool(True).tag(former="visible")
    mpl=Typed(MPL_Format)
    xdata=Array()
    ydata=Array()

    def _default_mpl(self):
        return MPL_Format()

    def remove_collection(self):
        if self.remove:
            if self.clt is not None:
                self.clt.remove()
        #else:

    plot_type=Enum("line", "scatter", "multiline", "colormap", "vline", "hline", "polygon", "cross_cursor")

    def __init__(self, **kwargs):
        #plotter=kwargs.pop("plotter", None)
        #if plotter is None:
        #    plotter=None
        #self.mpl.plotter=plotter
        super(PlotFormat, self).__init__(**kwargs)
        self.plotter.plot_dict[self.name]=self

    clt=Typed(Line2D)

    @cached_property
    def view_window(self):
        with imports():
            from plot_format_e import Main
        view=Main(pltr=self.plotter)
        return view
    #interactive_window=InteractiveWindow()

def transformation(func):
    """decorator that assists with transfroming from one format to another"""
    def transform_func(self):
        self.remove_collection()
        new_form=func(self)
        new_form.update_plot()
        self.plotter.plot_dict[self.name]=new_form
        del self
    return transform_func

class MPL_Line(MPL_Format):
    """attribtues which have a direct correspondence to mpl attribtues"""
    alpha=Float(1.0)
    label=Unicode()
    color=Enum(*colors_tuple[1:])#.tag(former="c")
    linewidth=Float(2.0)#.tag(former="linewidth")
    linestyle=Enum('solid', 'dashed', 'dashdot', 'dotted')#.tag(former="linestyle")

    @plot_observe("alpha", "label", "linewidth", "linestyle", "color", update_legend=True)
    def line_update(self, change):
        self.plot_set(change["name"])

class LineFormat(PlotFormat):
    custom_color=ContainerList(default=[0.0, 1.0, 0.0, 1.0])

    def _default_plot_type(self):
        return "line"

    def _default_mpl(self):
        return MPL_Line(_parent=self)


    #@plot_observe("mpl.alpha", "mpl.label", "mpl.linewidth", "mpl.linestyle", "mpl.color", update_legend=True)
    #def line_update(self, change):
    #    self.plot_set(change["name"])

    #def set_color(self, param, color):
    #    getattr(self.clt,"set_"+param)(color)


class Line2DFormat(LineFormat):
    def line_plot(self, *args, **kwargs):
        kwargs=self.mpl.process_kwargs(kwargs)

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

    def append_xy(self, *args):
        """appends points x and y if 2 args are passed and just y and len of xdata if one args is passed"""
        if len(args)==1:
            y=args[0]
            x=len(self.xdata)
        elif len(args)==2:
            x=args[0]
            y=args[1]
        self.xdata=append(self.xdata, x)
        self.ydata=append(self.ydata, y)
        self.clt.set_xdata(self.xdata)
        self.clt.set_ydata(self.ydata)
        fig=self.clt.get_figure()
        if fig.canvas is not None:
            fig.canvas.draw()


    @transformation
    def line2scatter(self):
        sf=ScatterFormat(name=self.name, plotter=self.plotter)
        sf.scatter_plot(self.xdata, self.ydata)
        return sf

def line_plot(plotter, name, *args, **kwargs):
    kwargs.pop("plotter", None)
    print plotter
    pl0t=Line2DFormat(name=name, plotter=plotter)

    #pl0t.mpl.plotter=plotter
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

    def _default_mpl(self):
        return MPL_Line(_parent=self, alpha=0.8, color="black", linewidth=0.5, linestyle="dashed")

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

    #def set_color(self, param, color):
    #    for item in self.clt.values():
    #        getattr(item,"set_"+param)(color)

#def cross_cursor(plotter, name, x, y, **kwargs):
#    pl0t=CrossCursor(name=name, plotter=plotter)
#    pl0t.add_cursor(x, y, **kwargs)
#    return pl0t

class MPL_Scatter(MPL_Line):
    """attributes which have a direct correspondence to mpl scatter plot attributes"""
    facecolor=Enum(*colors_tuple[1:]).tag(former="facecolor")
    edgecolor=Enum(*colors_tuple[1:]).tag(former="edgecolor")

    @plot_observe("facecolor", "edgecolor", update_legend=True)
    def scatter_update(self, change):
        self.plot_set(change["name"])

class ScatterFormat(LineFormat):
    clt=Typed(PathCollection)

    marker = Enum(*markers_tuple)
    marker_size = Float(30.0).tag(former="s")

    @plot_observe("marker_size", update_legend=True)
    def marker_size_update(self, change):
        self.clt.set_sizes([self.marker_size])

    @plot_observe("marker", update_legend=True)
    def marker_update(self, change):
        self.scatter_plot()

    def _default_mpl(self):
        return MPL_Scatter(_parent=self)

    def _default_plot_type(self):
        return "scatter"

    def process_kwargs(self, kwargs):
        for arg in ("marker", "marker_size"):
            if arg in kwargs:
                setattr(self, arg, kwargs[arg])
            key=get_tag(self, arg, "former", arg)
            kwargs[key]=kwargs.pop(arg, getattr(self, arg))
        return self.mpl.process_kwargs(kwargs)

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

class MPL_Colormesh(MPL_Format):
    cmap=Enum(*colormap_names)

    @plot_observe("cmap")
    def colormap_update(self, change):
        self.plot_set(change["name"])

class ColormeshFormat(PlotFormat):
    clt=Typed(QuadMesh)
    zdata=Array()
    vmin=Float()
    vmax=Float()

    colorbar=Instance(Colorbar)

    def _default_mpl(self):
        return MPL_Colormesh(_parent=self)

    def set_clim(self, vmin, vmax):
        self.clt.set_clim(vmin, vmax)

    @plot_observe("vmin", "vmax")
    def clim_update(self, change):
        self.set_clim(self.vmin, self.vmax)

    def _default_colorbar(self):
        self.plotter.figure.colorbar(self.clt)

    def _default_plot_type(self):
        return "colormap"

    def process_kwargs(self, kwargs):
        #for arg in ("clim2",):
        #    if arg in kwargs:
        #        setattr(self, arg, kwargs[arg])
        #    print arg
        #    key=get_tag(self, arg, "former", arg)
        #    kwargs[key]=kwargs.pop(arg, getattr(self, arg))
        return self.mpl.process_kwargs(kwargs)

    def pcolormesh(self, *args, **kwargs):
        kwargs=self.process_kwargs(kwargs)
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
        print self.zdata.shape
        #self.pcolormesh(self.xdata, self.ydata, self.zdata)
        fig=self.clt.get_figure()
        if fig.canvas is not None:
            fig.canvas.draw()


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
    from numpy import meshgrid, sqrt, array, full, NaN, zeros
    n = 300
    x = linspace(-1.5, 1.5, n)
    y = linspace(-1.5, 1.5, n*2)
    print pm
    #a=scatter_plot(pm, "blah",  x)
    #shower(a)
    X, Y = meshgrid(x, y)
    Z = sqrt(X**2 + Y**2)

    a=ColormeshFormat(name="colormesh", plotter=pm)
    a.pcolormesh(linspace(-1.5, 1.5, n+1), linspace(-1.5, 1.5, n*2+1), zeros((600,300)))
    shower(a)
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
