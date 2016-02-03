# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:53:23 2014

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.core.shower import shower
from taref.core.universal import sqze, Array
from taref.core.agent import SubAgent
from taref.core.atom_extension import private_property, get_tag, tag_Property

from numpy import angle, absolute, dtype, log10, meshgrid, arange, linspace, sin, cos, sqrt, ma, fabs, amax, amin
from matplotlib import cm
from numpy import shape, split, squeeze, array, transpose, concatenate, atleast_2d, ndim, argmin

from enaml import imports

from atom.api import Atom, Int, Enum, Float, List, Dict, Typed, Unicode, ForwardTyped, Bool, cached_property, observe, Value
from matplotlib.axes import Axes
from matplotlib.collections import PolyCollection, LineCollection#, QuadMesh, PathCollection
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from collections import OrderedDict

#import matplotlib
#matplotlib.use('GTKAgg')

from matplotlib import rcParams
rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 9

#rcParams['figure.figsize'] = 4.3, 4.2
rcParams['figure.dpi']=150
rcParams['xtick.major.width']=2
rcParams['lines.linewidth']=2
rcParams['xtick.major.size']=4
rcParams['axes.linewidth']=2
rcParams['ytick.major.width']=2
rcParams['ytick.major.size']=4

#adjust matplotlib base cursor
from matplotlib.backend_bases import cursors
from matplotlib.backends import backend_qt4
from PySide.QtCore import Qt
backend_qt4.cursord[cursors.POINTER] = Qt.CursorShape.CrossCursor


#rcParams['lines.antialiased']=False
#rcParams['patch.antialiased']=False
#rcParams['path.simplify']=False

#rcParams['lines.solid_joinstyle']='round'
#rcParams['lines.solid_capstyle']='round'

#from matplotlib.colors import colorConverter
#colors = [colorConverter.to_rgba(c) for c in ('r','g','b','c','y','m','k')]
#from matplotlib.ticker import MaxNLocator
#my_locator = MaxNLocator(6)
# Set up axes and plot some awesome science
#ax.yaxis.set_major_locator(my_locator)

mycolors=('auto', 'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange', 'darkblue', 'darkred')


mymarkers=(".", ",", "o", "v", "^", "<",">", "1", "2", "3", "4", "8", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_", "$2/3$")

class XYFormat(Atom):
    rend_list=List(default=[None, None, None]) #First is line, second is scatter #Typed(BaseXYPlot)
    name=Unicode()
    xname=Unicode()
    yname=Unicode()
    zname=Unicode()
    colormap=Enum("jet", "rainbow", "nipy_spectral")

    append=Bool(True)

    alpha=Float(1.0)
    label=Unicode().tag(refresh_legend=True)
    edgecolor=Enum(*mycolors).tag(refresh_legend=True)
    visible=Bool(True)
    facecolor=Enum(*mycolors).tag(refresh_legend=True)


    plot_type=Enum('line', 'scatter', 'colormap')
    linewidth=Float(2.0).tag(refresh_legend=True)
    marker = Enum(*mymarkers)
    marker_size = Float(30.0)
    linestyle=Enum('solid', 'dashed', 'dashdot', 'dotted').tag(refresh_legend=True)
    plotter=ForwardTyped(lambda: Plotter)

    clt=Value()

    @observe("alpha", "linestyle", "linewidth", "visible", "label")
    def changer(self, change):
        if change["type"]=="update":
            param=change["name"]
            refresh_legend=get_tag(self, param, "refresh_legend", False)
            if refresh_legend:
                temp=self.plotter.show_legend
                self.plotter.show_legend=False
            getattr(self.plotter.clts[self.name], "set_"+param)(getattr(self, param))
            if refresh_legend:
                self.plotter.show_legend=True
                self.plotter.show_legend=temp
            if self.plotter.auto_draw:
                self.plotter.draw()

    def _observe_marker_size(self, change):
        if change["type"]=="update":
                temp=self.plotter.show_legend
                self.plotter.show_legend=False
                self.plotter.clts[self.name].set_sizes([self.marker_size])
                self.plotter.show_legend=True
                self.plotter.show_legend=temp

#x b.clts["magabs"].set_cmap("rainbow")

    @observe("edgecolor", "colormap", "facecolor")
    def color_change(self, change):
        """intercepts auto case for coloring"""
        if change["type"]=="update":
            if self.edgecolor=="auto" or self.facecolor=="auto":
                temp=self.plotter.show_legend
                self.plotter.show_legend=False
                colormap=getattr(cm, self.colormap)
                length=len(self.plotter.clts[self.name].get_segments())
                colors = colormap(linspace(0, 1, length))
                self.plotter.clts[self.name].set_edgecolor(colors)
                self.plotter.show_legend=True
                self.plotter.show_legend=temp
            else:
                if change["name"]!="colormap":
                    self.changer(change)


class AllXYFormat(XYFormat):
    name=Unicode("All")

    def _observe_render_style(self, change):
        self.set_line_param('render_style', change)

    def _observe_plot_type(self, change):
        self.set_param('plot_type', change)

    def redraw_plot(self):
        for key, item in self.plotter.xyfs.iteritems():
            if key!="All":
                item.redraw_plot()

    def set_param(self, param, change, index=-1):
        if change['type']!='create':
            for key in self.plotter.xyfs.keys():
                if key!="All":
                    setattr(self.plotter.xyfs[key], change['name'], change['value'])

class mpl_drag_event(object):
    def __init__(self, pltr):
        self.pltr=pltr

    def __call__(self, event):

        xmin, xmax=self.pltr.axe.get_xlim()
        ymin, ymax=self.pltr.axe.get_ylim()
        if xmin!=self.pltr.x_min or xmax!=self.pltr.x_max:
            self.pltr.set_xlim(xmin, xmax)
        if ymin!=self.pltr.y_min or ymax!=self.pltr.y_max:
            self.pltr.set_ylim(ymin, ymax)
        if self.pltr.drawline==True:
            self.pltr.line_plot("dist", [self.pltr.xstart, event.xdata], [self.pltr.ystart, event.ydata], append=False,
                                xlim=(xmin, xmax), ylim=(ymin, ymax))
            self.pltr.draw()

class mpl_click_event(object):
    def __init__(self, pltr, x=None, y=None):
        self.pltr=pltr
        self.h_axe=self.pltr.horiz_axe
        self.v_axe=self.pltr.vert_axe
        self.data=self.pltr.alldata
        self.x=x
        self.y=y
        self.h_line=None
        self.v_line=None


    def __call__(self, event):
        if event.inaxes is not None:
            xpos=argmin(absolute(event.xdata-self.x))
            ypos=argmin(absolute(event.ydata-self.y))
            self.pltr.xcoord=event.xdata
            self.pltr.ycoord=event.ydata
            self.pltr.xind=xpos
            self.pltr.yind=ypos
            if self.h_line is None:
                self.min=amin(self.data)
                self.max=amax(self.data)
                self.h_line=self.h_axe.plot(self.data[ypos, :])[0]
                self.v_line=self.v_axe.plot(self.data[:, xpos], arange(201))[0]
            else:
                h_data=self.data[ypos, :]
                self.h_line.set_ydata(h_data)
                self.h_axe.set_ylim(min(h_data), max(h_data))
                v_data=self.data[:, xpos]
                self.v_line.set_xdata(v_data)
                self.v_axe.set_xlim(min(v_data), max(v_data))
            if self.pltr.horiz_fig.canvas!=None:
                self.pltr.horiz_fig.canvas.draw()
            if self.pltr.vert_fig.canvas!=None:
                self.pltr.vert_fig.canvas.draw()

            #xmin, xmax=self.pltr.axe.get_xlim()
            #ymin, ymax=self.pltr.axe.get_ylim()

            #self.pltr.line_plot("horiz", [xmin, xmax], [event.ydata, event.ydata], append=False,
                                #xlim=(xmin, xmax), ylim=(ymin, ymax))
            #self.pltr.draw()

        #xpos=argmin(absolute(event.xdata-self.x))
        #ypos=argmin(absolute(event.ydata-self.y))
        #log_debug(xpos, ypos)

        #['__doc__', '__init__', '__module__', '__str__', '_update_enter_leave', 'button', 'canvas', 'dblclick', 'guiEvent', 'inaxes', 'key', 'lastevent', 'name', 'step', 'x', 'xdata', 'y', 'ydata']
#        if event.dblclick:
#            x=event.xdata
#            y=event.ydata
#            xdist=(self.pltr.x_max-self.pltr.x_min)
#            ydist=(self.pltr.y_max-self.pltr.y_min)
#
#            self.pltr.set_xlim(x-xdist/2.0, x+xdist/2.0)#self.pltr.x_max-1.0*event.step*self.pltr.x_zoom_step)
#            self.pltr.set_ylim(y-ydist/2.0, y+ydist/2.0)#self.pltr.y_min+event.step*self.pltr.y_zoom_step, self.pltr.y_max-1.0*event.step*self.pltr.y_zoom_step)
#            self.pltr.draw()
#        else:
#            if self.x is None:
#                self.x=event.xdata
#                self.y=event.ydata
#                self.pltr.xstart=self.x
#                self.pltr.ystart=self.y
#                self.pltr.drawline=True
#            else:
#                self.pltr.xdist=event.xdata-self.x
#                self.pltr.ydist=event.ydata-self.y
#                self.x=None
#                self.y=None
#                self.pltr.drawline=False

class mpl_scroll_event(object):
    def __init__(self, pltr):
        self.pltr=pltr

    def __call__(self, event):
        x=(self.pltr.x_max+self.pltr.x_min)/2.0 #event.xdata
        y=(self.pltr.y_max+self.pltr.y_min)/2.0
        xdist=(self.pltr.x_max-self.pltr.x_min)*(1.0-event.step/5.0)
        ydist=(self.pltr.y_max-self.pltr.y_min)*(1.0-event.step/5.0)

        self.pltr.set_xlim(x-xdist/2.0, x+xdist/2.0)#self.pltr.x_max-1.0*event.step*self.pltr.x_zoom_step)
        self.pltr.set_ylim(y-ydist/2.0, y+ydist/2.0)#self.pltr.y_min+event.step*self.pltr.y_zoom_step, self.pltr.y_max-1.0*event.step*self.pltr.y_zoom_step)
        self.pltr.draw()

class Plotter(SubAgent):
    base_name="plot"
    plt_colors=['auto', 'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange']
    title=Unicode()
    xlabel=Unicode()
    xlabel_size=Float(14.0)

    def _observe_xlabel_size(self, change):
        self.changer(change, self.axe.xaxis.label.set_size, self.xlabel_size)

    ylabel=Unicode()
    ylabel_size=Float(14.0)

    def _observe_ylabel_size(self, change):
        self.changer(change, self.axe.yaxis.label.set_size, self.ylabel_size)

    x_scale=Enum('linear', 'log')
    y_scale=Enum('linear', 'log')

    x_min=Float()
    x_max=Float()
    y_min=Float()
    y_max=Float()

    alldata=Array()

    xdist=Float().tag(read_only=True)
    ydist=Float().tag(read_only=True)
    xcoord=Float()
    ycoord=Float()
    xind=Int()
    yind=Int()

    show_cs=Bool(False)
    drawline=Bool(False)
    xstart=Float()
    ystart=Float()

    @tag_Property()
    def total_dist(self):
        return sqrt(self.xdist**2+self.ydist**2)

    @observe("xdist", "ydist")
    def xydist_calc(self, change):
        if change["type"]=="update":
            self.get_member("total_dist").reset(self)

    autocolor=Bool(True)
    show_legend=Bool(False)
    append=Bool(True)
    auto_draw=Bool(False)
    tight_layout=Bool(False)

    def _observe_tight_layout(self, change):
        self.changer(change, self.fig.set_tight_layout, self.tight_layout)

    auto_xlim=Bool(True)
    auto_ylim=Bool(True)
    dpi=Int(150)

    def _observe_dpi(self, change):
        self.changer(change, self.fig.set_dpi, self.dpi)

    def activated(self):
        self.fig.canvas.mpl_connect('motion_notify_event', mpl_drag_event(self))
        self.fig.canvas.mpl_connect('motion_notify_event', mpl_click_event(self, arange(200), arange(200))) #button_press_event

        #self.fig.canvas.mpl_connect('button_press_event', mpl_click_event(self))
        self.fig.canvas.mpl_connect('scroll_event', mpl_scroll_event(self))

    xyfs=Typed(OrderedDict)

    def _default_xyfs(self):
        xyfs=OrderedDict()
        xyfs["All"]=AllXYFormat(plotter=self, name="All")
        return xyfs


    #color_index=Int()

    clts=Dict()

    @private_property
    def clts_keys(self):
        return self.clts.keys()

    @private_property
    def xyfs_keys(self):
        return self.xyfs.keys()

    @private_property
    def xyfs_items(self):
        return self.xyfs.values()

    fig=Typed(Figure).tag(private=True)
    axe=Typed(Axes).tag(private=True)

    fig_height=Float(1.3).tag(private=True)
    fig_width=Float(1.2).tag(private=True)


    horiz_fig=Typed(Figure).tag(private=True)
    horiz_axe=Typed(Axes).tag(private=True)
    vert_fig=Typed(Figure).tag(private=True)
    vert_axe=Typed(Axes).tag(private=True)


    def _default_fig(self):
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

    plot_type_list=["Line plot", "Scatter plot", "Colormap", "Polygon", "Text"]

    @private_property
    def plot_type_map(self):
        return {"Line plot" : self.line_plot,
                "Scatter plot" : self.scatter_plot,
                "Colormap" : self.colormap,
                "Polygon" : self.poly_plot,
                "Text" : self.add_text}



    def get_window_height(self):
        print self.view_window


    def changer(self, change, func, *args, **kwargs):
        if change["type"]=="update":
            func(*args, **kwargs)
            if self.auto_draw:
                self.draw()

    @observe("x_min", "x_max")
    def change_x_lim(self, change):
        self.changer(change, self.set_xlim, self.x_min, self.x_max)

    @observe("y_min", "y_max")
    def change_y_lim(self, change):
        self.changer(change, self.set_ylim, self.y_min, self.y_max)

    def _observe_x_scale(self, change):
        self.changer(change, self.axe.set_xscale, self.x_scale)

    def _observe_y_scale(self, change):
         self.changer(change, self.axe.set_yscale, self.y_scale)

    def _observe_title(self, change):
        self.changer(change, self.axe.set_title, self.title)

    def _observe_xlabel(self, change):
        self.changer(change, self.axe.set_xlabel, self.xlabel)

    def _observe_ylabel(self, change):
        self.changer(change, self.axe.set_ylabel, self.ylabel)

    def _observe_show_legend(self, change):
        if self.show_legend:
            self.changer(change, self.axe.legend().draggable)
        else:
            if self.axe.legend_ is not None:
                self.changer(change, self.axe.legend_.remove)


#    def delete_all_plots(self):
#         for key in self.plot.plots.keys():
#                self.plot.delplot(key)
#         self.color_index=0

#    def _save(self):
#         global PlotGraphicsContext
#         if PlotGraphicsContext==None:
#             from chaco.plot_graphics_context import PlotGraphicsContext
#         win_size = self.plot.outer_bounds
#         plot_gc = PlotGraphicsContext(win_size)#, dpi=300)
#         plot_gc.render_component(self.plot)
#         plot_gc.save("image_test.png")

    def line_plot(self, zname, zdata, *args, **kwargs):
        """Uses LineCollection for efficient plotting of lines.
           In kwargs, if raw=True, expects zdata is a list of lists of (x,y) tuples.
           else if no args are sent, auto calculates x data.
           otherwise assumes zdata is x data and args[0] is y data.
           In kwargs, if append=False, data overwrites existing data in self.clts
           If tuples, xlim or ylim are passed in kwargs, will use those for setting limits"""

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
            clt=self.clts.get(zname, None)
            if clt:
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
        if zname not in self.clts:
            clt=LineCollection(data, **kwargs)
            self.clts[zname]=clt
            self.axe.add_collection(self.clts[zname])
        else:
            self.clts[zname].set_verts(data)
            if kwargs!={}:
                self.clts[zname].set(**kwargs)
        if self.autocolor:
            self.clts[zname].set_array(arange(len(data)))
        if "color" in kwargs:
            self.clts[zname].set_array(None)
        if xlim is None or ylim is None: #try autosetting limits if xlim or ylim not specified
            data=sqze(sqze([item.get_segments() for item in self.clts.values() if isinstance(item, LineCollection)]))
            if xlim is None:
                xlim=(min(data, key = lambda t: t[0])[0], max(data, key = lambda t: t[0])[0])
            if ylim is None:
                ylim=(min(data, key = lambda t: t[1])[1], max(data, key = lambda t: t[1])[1])
        self.set_xlim(*xlim)
        self.set_ylim(*ylim)
        self.xyfs[zname]=XYFormat(plotter=self, name=zname, plot_type="line", label=kwargs.get("label", ""), edgecolor=kwargs.get("color", "blue"))

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

    def colormesh(self, zname, *args, **kwargs):
        self.remove_collection(zname)
        self.clts[zname]=self.axe.pcolormesh(*args, **kwargs)
        self.xyfs[zname]=XYFormat(plotter=self, name=zname)
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

    def set_data(self, zname=None, zdata=None, zcolor=None, plot_type="poly"):
         if zdata!=None:
             if plot_type is "poly":
                if zname not in self.clts: #plottables['plotted']:#self.pd.list_data():
                    clt=PolyCollection([], alpha=0.5, antialiased=True)#, rasterized=False, antialiased=False)
                    if zcolor is not None:
                        clt.set_color(colorConverter.to_rgba(zcolor))
                    self.clts[zname]=clt
                    self.axe.add_collection(self.clts[zname])
                self.clts[zname].set_verts(zdata)

             elif plot_type is "line":
                if zname not in self.clts:
                    clt=LineCollection(zdata)#, linewidths=(0.5, 1, 1.5, 2),
                                   #linestyles='solid', colors=("red", "blue", "green"))
                    if zcolor is not None:
                        clt.set_color(zcolor)
                    else:
                        clt.set_array(arange(len(zdata)))
                else:
                    self.clts[zname].set_verts(zdata)
                    #self.set_xlim(x.min(), x.max())
                    #self.set_ylim(ys.min(), ys.max())

             elif plot_type is "scatter":
                self.axe.scatter(zdata, zdata)
             elif plot_type is "colormap":
                self.axe.pcolormesh(x, y, z)

         if 0:
             x = arange(3)
             ys = array([x + i for i in arange(5)])
             #xdata=arange(len(getattr(self, zname)))

             data=[list(zip(x, y)) for y in ys]
             line_segments = LineCollection(data,
                                   linewidths=1,
                                   linestyles='solid',
                                   colors=mycolors)
             print data
             print len(data)
             #print line_segments.properties()
             #print line_segments.set_hatch("O")
             #print dir(self.axe)

             print [p.vertices for p in line_segments.get_paths()]#)
             print line_segments.get_segments()
             line_segments.set_array(arange(len(data)))

             x = arange(3)
             ys = array([x + i for i in arange(2)])
             #xdata=arange(len(getattr(self, zname)))

             data=[list(zip(x, y)) for y in ys]

             line_segments.set_verts(data)
             #self.axe.add_collection(line_segments, autolim=True)

             clt=self.axe.scatter(x,x)
             #clt.set_linestyle("solid")
             print dir(clt)
             print clt.get_paths()
         if 0:
            #clt=QuadMesh(0, 0, [1])


            n = 12
            x = linspace(-1.5, 1.5, n)
            y = linspace(-1.5, 1.5, n*2)
            X, Y = meshgrid(x, y)
            print X
            Qx = cos(Y) - cos(X)
            Qz = sin(Y) + sin(X)
            Qx = (Qx + 1.1)
            Z = sqrt(X**2 + Y**2)/5
            Z = (Z - Z.min()) / (Z.max() - Z.min())
            Zm = ma.masked_where(fabs(Qz) < 0.5*amax(Qz), Z)

            #ax = fig.add_subplot(121)
            #self.axe.set_axis_bgcolor("#bdb76b")
            clt=self.axe.pcolormesh(Z)
            #print dir(clt)
            self.axe.set_title('Without masked values')

            #ax = fig.add_subplot(122)
            #ax.set_axis_bgcolor("#bdb76b")
            #  You can control the color of the masked region:
            #cmap = cm.jet
            #cmap.set_bad('r', 1.0)
            #ax.pcolormesh(Qx,Qz,Zm, cmap=cmap)
            #  Or use the default, which is transparent:
            #col = self.axe.pcolormesh(Qx, Qz, Zm, shading='gouraud')
            #ax.set_title('With masked values')




    def add_text(self, text, x, y, **kwargs):
         """adds text at data location x,y"""
         self.axe.text(x, y, text, **kwargs)

    def remove_texts(self):
        """removes all texts from axes"""
        self.axe.texts=[]

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

#    def get_data(self, zname, index=None, axis=0):
#        data=[c.to_polygons() for c in self.clt.get_paths()]
#        if index==None:
#            return data
#        if axis==0:
#            return atleast_2d(data)[index, :]
#        return atleast_2d(data)[:, index]
#
#    def add_img_plot(self, zname, zdata, xname=None, xdata=None, yname=None,  ydata=None):
#         self.add_data(zname=zname, zdata=zdata, xname=xname, xdata=xdata, yname=yname, ydata=ydata, overwrite=True, concat=False)
#         print self.pd.get_data(zname)
#         xyf=XYFormat(plotter=self)
#         xyf.draw_img_plot(name='img_plot', zname=zname, xname=xname, yname=yname)
#         self.xyfs.update(**{xyf.name: xyf})
#         self.overall_plot_type="img plot"
#
#    def add_line_plot(self, name, zname, zdata, xname='', xdata=None):
#        #self.add_data(zname=zname, zdata=zdata, xname=xname, xdata=xdata, overwrite=True)
#        self.set_data(zname, zdata)
#        self.set_data(xname, xdata)
#        xyf=XYFormat(plotter=self)
#        zdata=self.get_data(zname)
#        #if 1: #zdata.ndim>1:
#        #    for i, arr in enumerate(self.splitMultiD(zdata, 0)):
#        #        self.add_line_plot(name+str(i), zname+str(i), squeeze(arr), xname, xdata )
#        #else:
#            #self.set_data(zname, zdata)
#            #if xname!=None and xdata!=None:
#            #    self.set_data(xname, xdata, coord='x')
#        xyf.draw_plot(name=name, zname=zname, xname=xname)
#        self.xyfs.update(**{xyf.name: xyf})
#        self.overall_plot_type="XY plot"
#
#    def splitMultiD(self, arr, axis=0):
#        if arr.ndim<2:
#            return atleast_2d(arr)
#        else:
#            return split(arr, arr.shape[axis], axis=axis)
#
#    def gatherMultiD(self, name, arrs, appen=None, concat=True, overwrite=False):
#         if not isinstance(arrs, tuple):
#             arrs=(arrs,)
#         if appen==None:
#             if shape(arrs)==(1,):
#                 appen=True
#             else:
#                 appen=False
#         orig=self.get_data(name)
#         if orig!=None and not overwrite:
#             arrs=(orig,)+arrs
#         if appen:
#             axis=1
#         else:
#             axis=0
#         print arrs[0]==atleast_2d(*arrs)
#         #if ndim(arrs[0])>1:
#         #    concat=False
#
#         if concat:
#             data=concatenate(atleast_2d(*arrs), axis)
#         self.set_data(name, data)
#
#    def add_data(self, zname, zdata, xname=None, xdata=None, yname=None, ydata=None, appen=None, concat=True, overwrite=False):
#         if xname!=None:
#             self.gatherMultiD(xname, xdata, appen=appen, overwrite=overwrite, concat=concat)
#         if yname!=None:
#             self.gatherMultiD(yname, ydata, appen=appen, overwrite=overwrite, concat=concat)
#         self.gatherMultiD(zname, zdata, appen=appen, overwrite=overwrite, concat=concat)

    @private_property
    def view_window(self):
        with imports():
            from taref.core.plotter_e import PlotMain
        return PlotMain(plotr=self)

if __name__=="__main__":
    a=Plotter()
    print a.colormesh
    #print Plotter.plot_dict
    #print dir(a.fig)
    #print #a.fig.tight_layout()#(pad=0.1)
    x = arange(3)+3
    ys = array([x + i for i in arange(5)])
    data=[list(zip(x, y)) for y in ys]
    #a.line_plot("blah", data)
    a.line_plot("blah", ys[0], label="1", color="red")
    a.scatter_plot("bob", x-4, ys[0]+10, label="2", color="blue")

    a.line_plot("bill", x-2, ys[0]+6, ys[1]+6, color="green", label="bob")#, color=("red", "blue", "green"))
    print a.clts["blah"].get_color()
    a.axe.legend()
    #a.set_xlim(x.min(), x.max())
    #a.set_ylim(ys.min(), ys.max())
    a.draw()
    shower(a)

    def plot_data(self, zname, **kwargs):
         """pass in an appropriate kwarg to get zdata for the zname variable back"""
         xmult=kwargs.pop("xmult", 1.0)
         zmult=kwargs.pop("zmult", 1.0)
         label=kwargs.pop("label", "")

         if "xlim" in kwargs:
             xlim(kwargs["xlim"])

         if "ylim" in kwargs:
             ylim(kwargs["ylim"])

         zunit=self.get_tag(zname, "unit")
         zunit_factor=self.get_tag(zname, "unit_factor", 1.0)

         if zunit is None:
             zlabel_str=zname
         else:
             zlabel_str="{0} [{1}]".format(zname, zunit)

         ylabel(kwargs.pop("ylabel", zlabel_str))

         add_legend=kwargs.pop("legend", False)

         title_str=kwargs.pop("title", None)
         xlabel_str=kwargs.pop("xlabel", None)

         if len(kwargs)==1:
             xname, xdata=kwargs.popitem()
             zdata=self.call_func(zname, **{xname:xdata})
             xunit=self.get_tag(xname, "unit")
             xunit_factor=self.get_tag(xname, "unit_factor", 1.0)
         else:
             xname="#"
             xdata=arange(len(getattr(self, zname)))
             xunit=None
             xunit_factor=1.0#self.get_tag(xname, "unit_factor", 1.0)

         if xlabel_str is None:
             if xunit is None:
                 xlabel_str=xname
             else:
                 xlabel_str="{0} [{1}]".format(xname, xunit)
         xlabel(xlabel_str)

         if title_str is None:
             title_str="{0} vs {1}".format(zname, xname)
         title(title_str)
         #print xdata.shape, zdata.shape
         plot(xdata/xunit_factor*xmult, zdata/zunit_factor*zmult, label=label)

         if add_legend:
             legend()
#    if not a.fig:
#        print "no fig!"
#    from numpy import exp, shape
#    xs = linspace(0, 8, 100)
#    ys = linspace(0, 4, 3)
#    x, y = meshgrid(xs,ys)
#    z = exp(-(x**2+y**2)/100)
#    zs=sin(xs)
#
#    #print a.fig.axes #as_list()
#    #a.fig.set_alpha(0.1)
#    from numpy import amin, amax
#    data=[((0,0), (0,-1), (3,1)), ((5,10), (6,11))]
#    print amin(data[0], 0), amax(data[0], 0)
#    a.set_data("mypoly", [((0,0), (0,-1), (3,1))])
#    a.show()
#    #print z
    #zz= a.splitMultiD(z)
    #print zz
#    zz.append(array([[1],[2],[3]]))
#    print zz
#    print a.gatherMultiD(zz)
    #args=([1,2,3], [4,5,6])
    #a.add_data('x', args) #z=concatenate(atleast_2d(*args), axis=0)
    #a.add_data('x', args) #z=concatenate(atleast_2d(*args), axis=0)

    #print a.get_data('z')
#    print concatenate((z, atleast_2d([7,8,9])))
    #a.add_data('z', 7)#, axis=1)
    #a.add_data('z', 7)#, axis=1)

    #print a.get_data('z', 0)
    #a.add_data('z', [11, 12], appen=True) #, axis=1)
    #a.gatherMultiD('z', 12, axis=1)
#
    #print a.get_data('z', 0)
    #print a.get_data('z', 0, 1)
    #a.add_data('z', [3,4,5,6], appen=False) #, axis=1)
    #print a.get_data('z')
#    a.gatherMultiD('z', (z, [7,8,9]))
#    print a.pd.get_data('z')
#    print a.get_data('z', 0)
#    print a.get_data('z', 0, 1)
#
#    a.gatherMultiD('z', ([10,11,12], [13,14,15]))
#    print a.pd.get_data('z')
#    print a.get_data('z', 0)
#    print a.get_data('z', 0, 1)
#    #a.add_line_plot("balh", "c", array([4,5,6]))
#    a.add_img_plot( "c", array([[4,5,6]]))
#    print a.xyfs['img_plot'].rend_list[2].index.get_data()[0].get_data()
    #a.xyfs['balh'].rend_list[0].index.set_data([4,5,6])
    #print a.xyfs['balh'].rend_list[0].index.get_data()



#    print array([[1,2,3]])
#    print atleast_2d([1,2,3])
#    print transpose(atleast_2d([1,2,3]))
#    #print split(xs, shape(xs)[0])
    #a.add_img_plot(zname="z", zdata=z)#, xname="x", xdata=xs, yname="y", ydata=ys)
    #a.add_line_plot("blah", zname="z", zdata=zs, xname='x', xdata=xs)
   # a.show()

        #cs=column_stack(arrs)
        #if axis==0:
        #    return transpose(cs)
        #return cs

#    b=array([[1,2,3], [4,5,6]])
#    print b
#    c=a.splitMultiD(b)
#    print c
#    print a.gatherMultiD(c)
#    d=array([1,2,3])
#    dd=a.splitMultiD(d)
#    print a.gatherMultiD(dd)


#    @staticmethod
#    def _pcolorargs(funcname, *args, **kw):
#        # This takes one kwarg, allmatch.
#        # If allmatch is True, then the incoming X, Y, C must
#        # have matching dimensions, taking into account that
#        # X and Y can be 1-D rather than 2-D.  This perfect
#        # match is required for Gouroud shading.  For flat
#        # shading, X and Y specify boundaries, so we need
#        # one more boundary than color in each direction.
#        # For convenience, and consistent with Matlab, we
#        # discard the last row and/or column of C if necessary
#        # to meet this condition.  This is done if allmatch
#        # is False.
#
#        allmatch = kw.pop("allmatch", False)
#
#        if len(args) == 1:
#            C = np.asanyarray(args[0])
#            numRows, numCols = C.shape
#            if allmatch:
#                X, Y = np.meshgrid(np.arange(numCols), np.arange(numRows))
#            else:
#                X, Y = np.meshgrid(np.arange(numCols + 1),
#                                   np.arange(numRows + 1))
#            C = cbook.safe_masked_invalid(C)
#            return X, Y, C
#
#        if len(args) == 3:
#            X, Y, C = [np.asanyarray(a) for a in args]
#            numRows, numCols = C.shape
#        else:
#            raise TypeError(
#                'Illegal arguments to %s; see help(%s)' % (funcname, funcname))
#
#        Nx = X.shape[-1]
#        Ny = Y.shape[0]
#        if len(X.shape) != 2 or X.shape[0] == 1:
#            x = X.reshape(1, Nx)
#            X = x.repeat(Ny, axis=0)
#        if len(Y.shape) != 2 or Y.shape[1] == 1:
#            y = Y.reshape(Ny, 1)
#            Y = y.repeat(Nx, axis=1)
#        if X.shape != Y.shape:
#            raise TypeError(
#                'Incompatible X, Y inputs to %s; see help(%s)' % (
#                funcname, funcname))
#        if allmatch:
#            if not (Nx == numCols and Ny == numRows):
#                raise TypeError('Dimensions of C %s are incompatible with'
#                                ' X (%d) and/or Y (%d); see help(%s)' % (
#                                    C.shape, Nx, Ny, funcname))
#        else:
#            if not (numCols in (Nx, Nx - 1) and numRows in (Ny, Ny - 1)):
#                raise TypeError('Dimensions of C %s are incompatible with'
#                                ' X (%d) and/or Y (%d); see help(%s)' % (
#                                    C.shape, Nx, Ny, funcname))
#            C = C[:Ny - 1, :Nx - 1]
#        C = cbook.safe_masked_invalid(C)
#        return X, Y, C