# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:54:58 2016

@author: thomasaref
"""

from taref.plotter.plotter_backbone import PlotUpdate, plot_observe
from atom.api import Typed, Bool, Unicode, Float, Enum, Int, cached_property
from collections import OrderedDict
from numpy import shape, linspace, arange

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.collections import PolyCollection, LineCollection

class Fig(PlotUpdate):
    figure=Typed(Figure)
    horiz_fig=Typed(Figure)
    horiz_axe=Typed(Axes)
    vert_fig=Typed(Figure)
    vert_axe=Typed(Axes)

    fig_height=Float(1.0)
    fig_width=Float(1.0)

    tight_layout=Bool(False)
    dpi=Int(150)

    auto_draw=Bool(False)

    def fig_set(self, param):
        self.simple_set(self.figure, param)

    @plot_observe("tight_layout", "dpi")
    def figure_update(self, change):
        self.fig_set(change["name"])

    def _default_figure(self):
         return Figure(figsize=(self.fig_height, self.fig_width))

    def _default_axe(self):
         axe=self.fig.add_subplot(111)
         axe.autoscale_view(True)
         return axe

    def _default_horiz_fig(self):
        return Figure(figsize=(self.fig_width, 1.0))

    def _default_horiz_axe(self):
        h_axe=self.horiz_fig.add_subplot(111, sharex=self.axe)
        return h_axe

    def _default_vert_fig(self):
        return Figure(figsize=(1.0, self.fig_height))

    def _default_vert_axe(self):
        h_axe=self.vert_fig.add_subplot(111, sharey=self.axe)
        return h_axe



    def draw(self):
        if self.fig.canvas!=None:
            self.fig.canvas.draw()
            self.get_member("clts_keys").reset(self)

    def set_xlim(self, xmin, xmax):
        self.x_min=xmin
        self.x_max=xmax
        self.axe.set_xlim(xmin, xmax)

    def set_ylim(self, ymin, ymax):
        self.y_min=ymin
        self.y_max=ymax
        self.axe.set_ylim(ymin, ymax)

    #@private_property
    #def view_window(self):
    #    with imports():
    #        from taref.core.plotter_e import PlotMain
    #    return PlotMain(plotr=self)

class Axe(PlotUpdate):
    axes=Typed(Axes)

    xlabel=Unicode()
    xlabel_size=Float(14.0)
    ylabel=Unicode()
    ylabel_size=Float(14.0)

    xscale=Enum('linear', 'log')
    yscale=Enum('linear', 'log')

    x_min=Float()
    x_max=Float()
    y_min=Float()
    y_max=Float()

    auto_xlim=Bool(True)
    auto_ylim=Bool(True)

    show_legend=Bool(False)

    def axes_set(self, param):
        getattr(self.axes, "set_"+param)(getattr(self, param))

    @plot_observe("xscale", "yscale", "title", "xlabel", "ylabel")
    def axes_update(self, change):
        self.axes_set(change["name"])

    @plot_observe("xlabel_size")
    def xlabel_update(self, change):
        self.axes.xaxis.label.set_size(self.xlabel_size)

    @plot_observe("ylabel_size")
    def ylabel_update(self, change):
        self.axes.yaxis.label.set_size(self.ylabel_size)

    @plot_observe("x_min", "x_max")
    def x_lim_update(self, change):
        self.set_xlim(self.x_min, self.x_max)

    @plot_observe("y_min", "y_max")
    def y_lim_update(self, change):
        self.set_ylim(self.y_min, self.y_max)

    def legend(self):
        self.axes.legend().draggable()

    def legend_remove(self):
        if self.axes.legend_ is not None:
            self.axe.legend_.remove()

    @plot_observe("show_legend")
    def legend_update(self, change):
        if self.show_legend:
            self.legend()
        else:
            self.legend_remove()

    xyfs=Typed(OrderedDict)

    def _default_xyfs(self):
        xyfs=OrderedDict()
        xyfs["All"]=AllXYFormat(plotter=self, name="All")
        return xyfs

    @cached_property
    def xyfs_keys(self):
        return self.xyfs.keys()

    @cached_property
    def xyfs_items(self):
        return self.xyfs.values()

    def line_plot(self, zname, zdata, *args, **kwargs):
        """Uses LineCollection for efficient plotting of lines.
           In kwargs, if raw=True, expects zdata is a list of lists of (x,y) tuples.
           else if no args are sent, auto calculates x data.
           otherwise assumes zdata is x data and args[0] is y data.
           In kwargs, if append=False, data overwrites existing data in self.clts
           If tuples, xlim or ylim are passed in kwargs, will use those for setting limits"""

        xyf=self.xyfs.get(zname, None)
        if xyf is None:
            xyf=XYFormat(plotter=self, name=zname, plot_type="line")
        clt=xyf.clt

        xlim=kwargs.pop("xlim", None)
        ylim=kwargs.pop("ylim", None)

        if "color" in kwargs:
            if kwargs["color"]=="auto":
                kwargs.pop("color")
                self.autocolor=True
            else:
                self.autocolor=False
        data=[]
        self.append=kwargs.pop("append", self.append)
        if self.append:
            if clt is not None:
                data=clt.get_segments()
        data_shape=len(shape(zdata))
        if data_shape>2:
            data.extend(zdata)
        else:
            if data_shape==2:
                x=zdata[0]
                y=zdata[1]
                data.append(list(zip(x,y)))
            elif args==():
                x=arange(len(zdata))
                y=zdata
                data.append(list(zip(x,y)))
            else:
                x=zdata
                data.extend([list(zip(x,y)) for y in args])
        if clt is None:
            clt=LineCollection(data, **kwargs)
            self.axe.add_collection(clt)
        else:
            clt.set_verts(data)
            if kwargs!={}:
                clt.set(**kwargs)
        if self.autocolor:
            clt.set_array(arange(len(data)))
        if "color" in kwargs:
            clt.set_array(None)
#        if xlim is None or ylim is None: #try autosetting limits if xlim or ylim not specified
#            data=sqze(sqze([item.get_segments() for item in self.clts.values() if isinstance(item, LineCollection)]))
#            if xlim is None:
#                xlim=(min(data, key = lambda t: t[0])[0], max(data, key = lambda t: t[0])[0])
#            if ylim is None:
#                ylim=(min(data, key = lambda t: t[1])[1], max(data, key = lambda t: t[1])[1])
#        self.set_xlim(*xlim)
#        self.set_ylim(*ylim)
        xyf.clt=clt
        self.xyfs[zname]=xyf #XYFormat(plotter=self, name=zname, plot_type="line", label=kwargs.get("label", ""), edgecolor=kwargs.get("color", "blue"))

    def scatter_plot(self, zname, *args, **kwargs):
        self.append=kwargs.pop("append", self.append)
        if not self.append:
            self.remove_collection(zname)
        self.clts[zname]=self.axe.scatter(*args, **kwargs)
        self.xyfs[zname]=XYFormat(plotter=self, name=zname, plot_type="scatter", label=kwargs.get("label", ""), edgecolor=kwargs.get("color", "blue"))

    def remove_collection(self, zname):
        if zname in self.clts:
            self.clts[zname].remove()
            self.clts.pop(zname)
            self.xyfs[zname].clt.remove()
            self.xyfs.pop(zname)

    def colormesh(self, zname, *args, **kwargs):
        self.remove_collection(zname)
        clt=self.axe.pcolormesh(*args, **kwargs)
        self.xyfs[zname]=XYFormat(plotter=self, name=zname, clt=clt)
        self.alldata=args[0]
        #self.line_plot(zname+"lines", arange(len(args[0][0])), *args[0])
        #self.xyfs[zname+"lines"]=XYFormat(plotter=self, name=zname+"lines")
        #log_debug(args[0])
    def axvline(self, zname, x, **kwargs):
        self.remove_collection(zname)
        self.axe.axvline(x, **kwargs)

    def poly_plot(self, zname, zdata, zcolor=None):
        if zname not in self.clts:
            clt=PolyCollection(zdata, alpha=0.5, antialiased=True)
            if zcolor is not None:
                clt.set_color(zcolor) #colorConverter.to_rgba(zcolor))
            self.clts[zname]=clt
            self.axe.add_collection(self.clts[zname])
        else:
            self.clts[zname].set_verts(zdata)

    def add_text(self, text, x, y, **kwargs):
         """adds text at data location x,y"""
         self.axe.text(x, y, text, **kwargs)

    def remove_texts(self):
        """removes all texts from axes"""
        self.axe.texts=[]
