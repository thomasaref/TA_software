# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:53:23 2014

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.core.shower import shower
from taref.core.universal import sqze
from numpy import angle, absolute, dtype, log10, meshgrid, arange, linspace, sin, cos, sqrt, ma, fabs, amax
from matplotlib import cm, colors
from numpy import shape, split, squeeze, array, transpose, concatenate, atleast_2d, ndim
from enaml import imports
from atom.api import Atom, Int, Enum, Float, List, Dict, Typed, Unicode, ForwardTyped, Bool, cached_property, observe
from matplotlib.axes import Axes
from matplotlib import collections, transforms
from matplotlib.collections import PolyCollection, LineCollection, QuadMesh, PathCollection
from matplotlib.figure import Figure

#slow imports
Plot = None
PanTool=None
ZoomTool=None
LegendTool=None
PlotGraphicsContext=None

#import matplotlib
#matplotlib.use('GTKAgg')

from matplotlib import rcParams
rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 9

rcParams['figure.figsize'] = 7.3, 4.2
rcParams['figure.dpi']=150
rcParams['xtick.major.width']=2
rcParams['lines.linewidth']=2
rcParams['xtick.major.size']=4
rcParams['axes.linewidth']=2
rcParams['ytick.major.width']=2
rcParams['ytick.major.size']=4
#rcParams['lines.antialiased']=False
#rcParams['patch.antialiased']=False
#rcParams['path.simplify']=False

#rcParams['lines.solid_joinstyle']='round'
#rcParams['lines.solid_capstyle']='round'

from matplotlib.colors import colorConverter
colors = [colorConverter.to_rgba(c) for c in ('r','g','b','c','y','m','k')]
#from matplotlib.ticker import MaxNLocator
#my_locator = MaxNLocator(6)
# Set up axes and plot some awesome science
#ax.yaxis.set_major_locator(my_locator)

mycolors=[ 'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange']

class XYFormat(Atom):
    rend_list=List(default=[None, None, None]) #First is line, second is scatter #Typed(BaseXYPlot)
    name=Unicode()
    xname=Unicode()
    yname=Unicode()
    zname=Unicode()
    colormap=Enum("jet")

    line_color=Enum(*mycolors)
    plot_type=Enum('line', 'scatter', 'line+scatter')
    line_width=Float(1.0)
    marker = Enum('square', 'circle', 'triangle', 'inverted_triangle', 'plus', 'cross', 'diamond', 'dot', 'pixel')
    marker_size = Float(3.0)
    outline_color=Enum(*mycolors)
    outline_width=Float(1.0)
    inside_color=Enum(*mycolors)
    line_style=Enum('solid', 'dot dash', 'dash', 'dot', 'long dash')
    render_style=Enum('connectedpoints', 'hold', 'connectedhold')
    plotter=ForwardTyped(lambda: Plotter)


    def _default_name(self):
        return self.yname

    def set_param(self, param, change, index=-1):
        if change['type']!='create':
            setattr(self.rend_list[index], param, change['value'])

    def set_line_param(self, param, change):
        self.set_param(param, change, index=0)

    def set_scatter_param(self, param, change):
        self.set_param(param, change, index=1)

    def _observe_line_color(self, change):
        self.set_line_param('color', change)

    def _observe_marker_size(self, change):
        self.set_scatter_param('marker_size', change)

    def _observe_marker(self, change):
        self.set_scatter_param('marker', change)

    def _observe_line_width(self, change):
        self.set_line_param('line_width', change)

    def _observe_outline_width(self, change):
        self.set_scatter_param('line_width', change)

    def _observe_outline_color(self, change):
        self.set_scatter_param('outline_color', change)

    def _observe_inside_color(self, change):
        self.set_scatter_param('color', change)

    def _observe_line_style(self, change):
        self.set_line_param('line_style', change)

    def redraw_plot(self):
        self.draw_plot(name=self.name, zname=self.zname, xname=self.xname)

    def draw_img_plot(self, name, zname, xname=None, yname=None):
        self.plotter.delete_all_plots()
        self.name=name
        self.zname=zname
        #self.plotter.pd.set_data(zname, z)
        img_plot = self.plotter.plot.img_plot(self.zname,
                                              name="img_plot",
                    colormap=self.colormap)[0]
#        z_shape=shape(self.plotter.pd.get_data(self.zname))
        #xdata=img_plot.index.get_data()[0].get_data()
        #ydata=img_plot.index.get_data()[1].get_data()
        if xname!=None:
            xdata=self.plotter.get_data(xname)
        else:
            xdata=img_plot.index.get_data()[0].get_data()
        if yname!=None:
            ydata=self.plotter.get_data(yname)
        else:
            ydata=img_plot.index.get_data()[1].get_data()
        img_plot.index.set_data(xdata,ydata)
        img_plot.request_redraw()
        self.rend_list[2]=img_plot

    def draw_plot(self, name, zname, zdata=None, xname='', xdata=None):
        if "img_plot" in self.plotter.plot.plots.keys():
            self.plotter.delete_all_plots()
        if "{0}_line".format(name) in self.plotter.plot.plots.keys():
            self.plotter.plot.delplot("{0}_line".format(name))
        if "{0}_scatter".format(name) in self.plotter.plot.plots.keys():
            self.plotter.plot.delplot("{0}_scatter".format(name))
        #if xname==None:
        #    xname="{0}_x0".format(zname)
        #    self.plotter.pd.set_data(xname, arange(len(self.plotter.pd.arrays[zname])))
        self.xname=xname
        self.zname=zname
        self.name=name
        if self.plot_type=='line':
            self.draw_line_plot()
        elif self.plot_type=='scatter':
            self.draw_scatter_plot()
        elif self.plot_type=='line+scatter':
            self.draw_line_plot()
            self.draw_scatter_plot()

#        if data.x_unit:
#            x_label = "{} [{}]".format(data.x_label, data.x_unit)
#        else:
#            x_label = data.x_label
#        if data.y_unit:
#            y_label = "{} [{}]".format(data.y_label, data.y_unit)
#        else:
#            y_label = data.y_label
#        plot.x_axis.title = x_label
#        plot.y_axis.title = y_label
#        plot.x_axis.tick_label_formatter = lambda x: '%.e'%x
#        plot.y_axis.tick_label_formatter = lambda x: '%.e'%x


    def draw_line_plot(self):
        renderer=self.plotter.plot.plot( self.zname ,
           name="{0}_line".format(self.name),
           type="line",
           line_width=self.line_width,
           color=self.line_color,
           render_style=self.render_style,
           value_scale=self.plotter.value_scale,
           index_scale=self.plotter.index_scale
           )[0]
        xdata=self.plotter.get_data(self.xname)
        if xdata!=None:
                renderer.index.set_data(xdata)
        renderer.request_redraw()
        self.rend_list[0]=renderer

    def draw_scatter_plot(self):
        renderer=self.plotter.plot.plot(self.zname,
           name="{0}_scatter".format(self.name), #self.zname,
           type="scatter", #self.xyformat.plot_type,
           line_width=self.line_width,
           color=self.inside_color,
           outline_color=self.outline_color,
           marker = self.marker,
           marker_size = self.marker_size,
           value_scale=self.plotter.value_scale,
           index_scale=self.plotter.index_scale
           )[0]
        xdata=self.plotter.get_data(self.xname)
        if xdata!=None:
                renderer.index.set_data(xdata)
        renderer.request_redraw()
        self.rend_list[1]=renderer

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

class Plotter(Atom):
    name=Unicode()
    title=Unicode("yoyoyoyoyo")
    xlabel=Unicode("yo")
    ylabel=Unicode()
    x_scale=Enum('linear', 'log')
    y_scale=Enum('linear', 'log')

    x_min=Float()
    x_max=Float()
    y_min=Float()
    y_max=Float()

    autocolor=Bool(True)

    xyfs=Dict()
    color_index=Int()

    clts=Dict()
    fig=Typed(Figure)
    axe=Typed(Axes)

    plottables=Dict()
    overall_plot_type=Enum("XY plot", "img plot")

    def _default_axe(self):
         axe=self.fig.add_subplot(111)
         axe.autoscale_view(True)
         return axe

    def _default_fig(self):
         return Figure()

    @observe("x_min", "x_max")
    def change_x_lim(self, change):
        if change["type"]=="update":
            self.set_xlim(self.x_min, self.x_max)
            self.draw()

    @observe("y_min", "y_max")
    def change_y_lim(self, change):
        if change["type"]=="update":
            self.set_ylim(self.y_min, self.y_max)
            self.draw()

    def _observe_x_scale(self, change):
        self.axe.set_xscale(self.x_scale)
        if change["type"]=="update":
            self.draw()

    def _observe_y_scale(self, change):
         self.axe.set_yscale(self.y_scale)
         if change["type"]=="update":
            self.draw()

    def _default_plottables(self):
         return dict(plotted=[None])

    def _observe_title(self, change):
        self.axe.set_title(self.title)
        if change["type"]=="update":
            self.draw()
    def _observe_xlabel(self, change):
        self.axe.set_xlabel(self.xlabel)
        if change["type"]=="update":
            self.draw()

    def _observe_ylabel(self, change):
        self.axe.set_ylabel(self.ylabel)
        if change["type"]=="update":
            self.draw()

    def _default_xyfs(self):
         xyf=AllXYFormat(plotter=self)
         return {"All":xyf}

    def delete_all_plots(self):
         for key in self.plot.plots.keys():
                self.plot.delplot(key)
         self.color_index=0

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
        log_debug(len(shape(zdata)))# in (int, float))
        xlim=kwargs.pop("xlim", None)
        ylim=kwargs.pop("ylim", None)

        if "color" in kwargs:
            if kwargs["color"]=="auto":
                kwargs.pop("color")
                self.autocolor=True
            else:
                self.autocolor=False
        data=[]
        if kwargs.pop("append", True):
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

    def scatter_plot(self, zname, *args, **kwargs):
        self.clts[zname]=self.axe.scatter(*args, **kwargs)

    def remove_collection(self, zname):
        if zname in self.clts:
            self.clts[zname].remove()

    def colormap(self, zname, *args, **kwargs):
        self.clts[zname]=self.axe.pcolormesh(*args, **kwargs)

    def poly_plot(self, zname, zdata, zcolor=None):
        if zname not in self.clts:
            clt=PolyCollection(zdata, alpha=0.5, antialiased=True)
            if zcolor is not None:
                clt.set_color(colorConverter.to_rgba(zcolor))
            self.clts[zname]=clt
            self.axe.add_collection(self.clts[zname])
        else:
            self.clts[zname].set_verts(zdata)

    def set_data(self, zname=None, zdata=None, zcolor=None, plot_type="poly"):
         if zdata!=None:
             if plot_type is "poly":
                if zname not in self.clts: #plottables['plotted']:#self.pd.list_data():
                    clt=PolyCollection(zdata, alpha=0.5, antialiased=True)#, rasterized=False, antialiased=False)
                    if zcolor is not None:
                        clt.set_color(colorConverter.to_rgba(zcolor))
                    self.clts[zname]=clt
                    self.axe.add_collection(self.clts[zname], autolim=True)
                else:
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
        self.axe.texts=[]

    def draw(self):
        log_debug("draw called")
        if self.fig.canvas!=None:
            self.fig.canvas.draw()

    def set_xlim(self, xmin, xmax):
        self.x_min=xmin
        self.x_max=xmax
        self.axe.set_xlim(xmin, xmax)

    def set_ylim(self, ymin, ymax):
        self.y_min=ymin
        self.y_max=ymax
        self.axe.set_ylim(ymin, ymax)

    def get_data(self, zname, index=None, axis=0):
        data=[c.to_polygons() for c in self.clt.get_paths()]
        if index==None:
            return data
        if axis==0:
            return atleast_2d(data)[index, :]
        return atleast_2d(data)[:, index]

    def add_img_plot(self, zname, zdata, xname=None, xdata=None, yname=None,  ydata=None):
         self.add_data(zname=zname, zdata=zdata, xname=xname, xdata=xdata, yname=yname, ydata=ydata, overwrite=True, concat=False)
         print self.pd.get_data(zname)
         xyf=XYFormat(plotter=self)
         xyf.draw_img_plot(name='img_plot', zname=zname, xname=xname, yname=yname)
         self.xyfs.update(**{xyf.name: xyf})
         self.overall_plot_type="img plot"

    def add_line_plot(self, name, zname, zdata, xname='', xdata=None):
        #self.add_data(zname=zname, zdata=zdata, xname=xname, xdata=xdata, overwrite=True)
        self.set_data(zname, zdata)
        self.set_data(xname, xdata)
        xyf=XYFormat(plotter=self)
        zdata=self.get_data(zname)
        #if 1: #zdata.ndim>1:
        #    for i, arr in enumerate(self.splitMultiD(zdata, 0)):
        #        self.add_line_plot(name+str(i), zname+str(i), squeeze(arr), xname, xdata )
        #else:
            #self.set_data(zname, zdata)
            #if xname!=None and xdata!=None:
            #    self.set_data(xname, xdata, coord='x')
        xyf.draw_plot(name=name, zname=zname, xname=xname)
        self.xyfs.update(**{xyf.name: xyf})
        self.overall_plot_type="XY plot"

    def splitMultiD(self, arr, axis=0):
        if arr.ndim<2:
            return atleast_2d(arr)
        else:
            return split(arr, arr.shape[axis], axis=axis)

    def gatherMultiD(self, name, arrs, appen=None, concat=True, overwrite=False):
         if not isinstance(arrs, tuple):
             arrs=(arrs,)
         if appen==None:
             if shape(arrs)==(1,):
                 appen=True
             else:
                 appen=False
         orig=self.get_data(name)
         if orig!=None and not overwrite:
             arrs=(orig,)+arrs
         if appen:
             axis=1
         else:
             axis=0
         print arrs[0]==atleast_2d(*arrs)
         #if ndim(arrs[0])>1:
         #    concat=False

         if concat:
             data=concatenate(atleast_2d(*arrs), axis)
         self.set_data(name, data)

    def add_data(self, zname, zdata, xname=None, xdata=None, yname=None, ydata=None, appen=None, concat=True, overwrite=False):
         if xname!=None:
             self.gatherMultiD(xname, xdata, appen=appen, overwrite=overwrite, concat=concat)
         if yname!=None:
             self.gatherMultiD(yname, ydata, appen=appen, overwrite=overwrite, concat=concat)
         self.gatherMultiD(zname, zdata, appen=appen, overwrite=overwrite, concat=concat)

    @cached_property
    def view_window(self):
        with imports():
            from Plotter_e import PlotMain
        return PlotMain(plotr=self)

if __name__=="__main__":
    a=Plotter()
    print dir(a.fig)
    print #a.fig.tight_layout()#(pad=0.1)
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

