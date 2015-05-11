# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:53:23 2014

@author: thomasaref
"""

from chaco.api import ArrayPlotData, Plot, PlotGraphicsContext, jet#, # BaseXYPlot#, marker_trait#, PlotAxis, GridDataSource, GridMapper, DataRange2D, CMapImagePlot, \
    #VPlotContainer, ImageData, DataRange1D, LinearMapper, ColorBar, jet, HPlotContainer
from numpy import array, mod, angle, absolute, dtype, log10, shape, zeros, meshgrid, empty, nan, append, arange, shape, linspace
from chaco.tools.api import PanTool, ZoomTool,  LegendTool, LineInspector
import traits_enaml
from enaml.qt.qt_application import QtApplication


from atom.api import Atom, Int, Enum, Float, List, Dict, Typed, Property, observe, Unicode, ForwardTyped


def dB(x):
    return 20*log10(absolute(x))

def magphase(y, response="Mag"):
        if dtype("complex128")==y.dtype:
            if response=="Phase":
                return angle(y)
            elif response=="Mag (dB)":
                return dB(y)
            else:
                return absolute(y)
        return y
mycolors=[ 'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange']

class XYZFormat(Atom):
    rend_list=List()
    name=Unicode()
    xname=Unicode()
    yname=Unicode()
    zname=Unicode()
    plotter=ForwardTyped(lambda: Plotter)
    colormap=Enum(jet)

    def _default_xboundsmin(self):
        if self.xname=="":
            return 0
        else:
            return min(self.plotter.pd.get_data(self.xname))

    @observe('xboundsmin', 'xboundsmax', 'yboundsmin', 'yboundsmax')
    def observexboundsmin(self, change):
        print change
        if change['type']!='create':
            #self.plotter.plot.xbounds=(self.xboundsmin, self.xboundsmax)
            #print self.rend_list[0].index..set_data()get_data()[0].set_data(linspace(0,300, 601))
            z_shape=shape(self.plotter.pd.get_data(self.zname))
            self.rend_list[0].index.set_data(linspace(self.xboundsmin, self.xboundsmax, z_shape[1]),
                                             linspace(self.yboundsmin, self.yboundsmax, z_shape[0]))

    def draw_img_plot(self, name, zname, zdata, xname=None, yname=None, xdata=None, ydata=None):
        self.plotter.pd.set_data(zname, zdata)
        self.name=name
        self.zname=zname
        #if xbounds==None:
        #    xbounds=(0, shape(zdata)[1])
        #if ybounds==None:
        #    ybounds=(0, shape(zdata)[0])

        img_plot = self.plotter.plot.img_plot(self.zname,
                                              name=self.name,
                    colormap=self.colormap)[0]
#        z_shape=shape(self.plotter.pd.get_data(self.zname))
        if xname!=None and yname!=None:
            if xdata!=None and ydata!=None:
                self.plotter.pd.set_data(xname, xdata)
                self.plotter.pd.set_data(yname, ydata)
            x=self.plotter.pd.get_data(xname)
            y=self.plotter.pd.get_data(yname)
            img_plot.index.set_data(x,y)
        img_plot.request_redraw()
        self.rend_list=[img_plot]



class XYFormat(Atom):
    rend_list=List(default=[None, None, None]) #First is line, second is scatter #Typed(BaseXYPlot)
    name=Unicode()
    xname=Unicode()
    yname=Unicode()
    zname=Unicode()
    colormap=Enum(jet)

    line_color=Enum(*mycolors) #'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange')
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
          #  if self.rend_list[index]!=None:
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
        self.draw_plot(name=self.name, yname=self.yname, xname=self.xname)

    def draw_img_plot(self, name, zname, xname=None, yname=None):
        self.plotter.delete_all_plots()
        self.name=name
        self.zname=zname
        img_plot = self.plotter.plot.img_plot(self.zname,
                                              name="img_plot",
                    colormap=self.colormap)[0]
#        z_shape=shape(self.plotter.pd.get_data(self.zname))
        if xname!=None and yname!=None:
            x=self.plotter.pd.get_data(xname)
            y=self.plotter.pd.get_data(yname)
            img_plot.index.set_data(x,y)
        img_plot.request_redraw()
        self.rend_list[2]=img_plot

    def draw_plot(self, name, yname, xname=None, ydata=None, xdata=None):
        if "img_plot" in self.plotter.plot.plots.keys():
            self.plotter.delete_all_plots()
        if "{0}_line".format(name) in self.plotter.plot.plots.keys():
            self.plotter.plot.delplot("{0}_line".format(name))
        if "{0}_scatter".format(name) in self.plotter.plot.plots.keys():
            self.plotter.plot.delplot("{0}_scatter".format(name))
        if xname==None:
            xname="{0}x0".format(yname)
            self.plotter.pd.set_data(xname, arange(len(self.plotter.pd.arrays[yname])))
        self.xname=xname
        self.yname=yname
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
        renderer=self.plotter.plot.plot((self.xname, self.yname ),
           name="{0}_line".format(self.name),
           type="line",
           line_width=self.line_width,
           color=self.line_color,
           render_style=self.render_style,
           value_scale=self.plotter.value_scale,
           index_scale=self.plotter.index_scale
           )[0]
        renderer.request_redraw()
        self.rend_list[0]=renderer

    def draw_scatter_plot(self):
        renderer=self.plotter.plot.plot((self.xname, self.yname ),
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

#from atom.api import Coerced
#from numpy import ndarray
#
#class stringfunc(Atom):
#    _d=Dict()
#    xdata=Coerced(ndarray, array)
#    eq=Unicode("sin(x)")
#    ydata=Coerced(ndarray, array)
#
#    def _default_dict(self):
#        d = dict(x=self.xdata)
#        exec "from scipy import *" in d
#        exec "from scipy.special import *" in d
#
#    def _default_ydata(self):
#        return eval(self.eq, self._d)
#
#    def _observe_eq(self, change):
#        try:
#            self.ydata = eval(self.eq, self._d)
#        except:
#            pass
#

class Plotter(Atom):
     title=Unicode()
     xlabel=Unicode()
     ylabel=Unicode()

     value_scale=Enum('linear', 'log')
     index_scale=Enum('linear', 'log')
#     plot_keys=Dict({"Line Plot":{}, "Image Plot":{}})
    # xyz=Typed(XYZFormat)
     xyfs=Dict()
    # xyformat=Typed(XYFormat, ())
     pd=Typed(ArrayPlotData, ())
     plot=Typed(Plot)
     color_index=Int()

     def _observe_value_scale(self, change):
         self.plot.value_scale=self.value_scale
         self.plot.request_redraw()

     def _observe_index_scale(self, change):
         self.plot.index_scale=self.index_scale
         self.plot.request_redraw()

     def _observe_title(self, change):
         self.plot.title=self.title
         self.plot.request_redraw()

     def _observe_xlabel(self, change):
         self.plot.x_axis.title=self.xlabel
         self.plot.request_redraw()

     def _observe_ylabel(self, change):
         self.plot.y_axis.title=self.ylabel
         self.plot.request_redraw()

  #   def _default_xyz(self):
  #       xyz=XYZFormat()
  #       xyz.plotter=self
  #       return xyz

     def _default_xyfs(self):
         xyf=AllXYFormat()
         xyf.plotter=self
        #xyf.name='All'
         return {"All":xyf}
#     #plot_add=Button()
#     xkey=Enum(values='xvalues')
#     xvalues=List()
#     zkey=Enum(values='zvalues')
#     zvalues=List()
#     unit=Dict()
#     xtitle=Property(depends_on='xkey, xunit')
#     ytitle=Property(depends_on='zkey, zunit')
#     title=Property(depends_on='zkey, xkey')
#
     def delete_all_plots(self):
         for key in self.plot.plots.keys():
                self.plot.delplot(key)
         self.color_index=0

#     def delete_plot(self, key):
#         self.plot.delplot(key)

#     def _get_xtitle(self):
#         return '{0} ({1})'.format(self.xkey, self.unit[self.xkey])
#
#     def _get_ytitle(self):
#         return '{0} ({1})'.format(self.zkey, self.unit[self.zkey])
#
#     def _get_title(self):
#         return '{0} vs {1}'.format(self.zkey, self.xkey)
#
#     def point_plot(self, z, zkey='z', x=None, xkey='x', plot_name="Line Plot", appender=True):
#         measurement=self.plot_keys[plot_name]
#         #print z, zkey, x, xkey, appender, measurement
#         if zkey not in measurement.keys():
#             measurement[zkey]=0
#             appender=False
#         self.zname="{0}{1}".format(zkey, measurement[zkey])
#         if appender==False:
#             self.pd.set_data(self.zname, z)
#         else:
#             arr=self.pd.get_data(self.zname)
#             arr=append(arr, z)
#             self.pd.set_data(self.zname, arr)
#         measurement[zkey]=measurement[zkey]+1
#
#         if x!=None: #if no x passed, assumes x data is already specified
#             if xkey not in measurement.keys():
#                 measurement[xkey]=0
#             xname="{0}{1}".format(xkey, measurement[xkey])
#             self.pd.set_data(xname, x)
#             measurement[xkey]=measurement[xkey]+1
#             self.xname=xname
#
#         if appender==False:
#             self.add_plot()
#
#     def dataset_plot(self, z, zkey="z", zunit="", plot_name="Line Plot"):
#         #print z, zkey, xkey, plot_name, xunit, zunit
#         #self.xtitle='{0} ({1})'.format(xkey, xunit)
#         #print zkey, xkey, zunit, xunit
#         self.unit[zkey]=zunit
#         #self.unit[xkey]=xunit
#
##         self.ytitle='{0} ({1})'.format(zkey, zunit)
##         self.title='{0} vs {1}'.format(zkey, xkey)
#         measurement=self.plot_keys[plot_name]
#         if zkey not in measurement.keys():
#             measurement[zkey]=0
#         self.zname="{0}{1}".format(zkey, measurement[zkey])
#         self.pd.set_data(self.zname, z)
#         measurement[zkey]=measurement[zkey]+1
#
#         if self.zkey==zkey:
#                 self.add_plot()
#
##         if x!=None: #if no x passed, assumes x data is already specified
##             if xkey not in measurement.keys():
##                 measurement[xkey]=0
##             xname="{0}{1}".format(xkey, measurement[xkey])
##             self.pd.set_data(xname, x)
##             measurement[xkey]=measurement[xkey]+1
##             self.xname=xname
##         else:
##         if xkey=="":
##                 xname=xname="{0}x0".format(zkey)
##                 self.pd.set_data(xname, arange(len(z)))
##                 self.xname=xname
##                 self.add_plot()
##         else:
##             if xkey not in measurement.keys():
##                 measurement[xkey]=0
##                 xname="{0}{1}".format(xkey, measurement[xkey])
##                 self.pd.set_data(xname, arange(len(z)))
###             measurement[xkey]=measurement[xkey]+1
##             else:
##                 if measurement[xkey]<measurement[zkey]:
##                     xname="{0}{1}".format(xkey, measurement[xkey])
##                     self.pd.set_data(xname, arange(len(z)))
##             xname="{0}{1}".format(xkey, measurement[xkey])
##             self.xname=xname
##             if zkey==self.zkey:
##                 self.add_plot()
##         self.zvalues=measurement.keys()
#         #self.xvalues=measurement.keys()
#        # if self.xkey==None:
#        #     self.xkey=xkey
#        # if zkey!=xkey and self.zkey==None:
#        #     self.zkey=zkey
#
#         #            self.pd.list_data()
#     @observe('zkey, xkey')
#     def zkey_changed(self):
#         for key in self.plot.plots.keys():
#                self.plot.delplot(key)
#         self.color_index=0
#
#         for item in self.pd.list_data():
#             if self.zkey in item:
#                 self.add_plot()
#
#     def add_plot(self):#, xtitle="", ytitle="", title=""):
#        self.xname="{0}{1}".format(self.xkey, self.color_index)
#        self.zname="{0}{1}".format(self.zkey, self.color_index)
#        #print self.pd.list_data()
#        if self.xname not in self.pd.list_data():
#            self.pd.set_data(self.xname, arange(len(self.pd.arrays[self.zname])))
#        if self.zname not in self.pd.list_data():
#            self.pd.set_data(self.zname, arange(len(self.pd.arrays[self.xname])))
#        if self.zname not in self.plot.plots.keys():
#            #print [xtitle, ytitle]
#            #print self.pd.arrays
#            if self.xyformat.color=="transparent" or self.xyformat.color==(1.0, 1.0, 1.0, 1.0) :
#                    color=self.xyformat.mycolors[mod(self.color_index, len(self.xyformat.mycolors))]
#            else:
#                color=self.xyformat.color
#                #if self.color_index<len(self.xkeys):
#                #    xkey='x'+str(self.xkeys[self.color_index])
#                #else:
#                #    xkey='x'+str(self.xkeys[0])
#            self.plot.plot((self.xname, self.zname),
#                               name=self.zname,
#                               type=self.xyformat.plot_type,
#                               line_width=self.xyformat.line_width,
#                               color=color,
#                               outline_color=self.xyformat.outline_color,
#                               marker = self.xyformat.marker,
#                               marker_size = self.xyformat.marker_size)
#            try:
#                self.plot.x_axis.title=self.xtitle
#                self.plot.y_axis.title=self.ytitle
#                self.plot.title=self.title
#            except:
#                KeyError
#            self.color_index=self.color_index+1
#            self.plot.request_redraw()
#           # print self.pd.list_data()
#
     def _save(self):
        win_size = self.plot.outer_bounds
        plot_gc = PlotGraphicsContext(win_size)#, dpi=300)
        plot_gc.render_component(self.plot)
        plot_gc.save("image_test.png")

     def set_data(self, yname, ydata):
        self.pd.set_data(yname, ydata)

     def add_img_plot2(self):
         from numpy import linspace, exp
         xs = linspace(0, 10, 600)
         ys = linspace(0, 5, 300)
         x, y = meshgrid(xs,ys)
         z = exp(-(x**2+y**2)/100)
         self.add_img_plot(z, xs, ys)
     def add_img_plot(self, zname, zdata, xname=None, yname=None, xdata=None, ydata=None):
         self.set_data(zname, zdata)
         if xname!=None and yname!=None:
             if xdata!=None and ydata!=None:
                 self.set_data(xname, xdata)
                 self.set_data(yname, ydata)
         xyf=XYFormat()
         xyf.plotter=self
         xyf.draw_img_plot(name=zname, zname=zname, xname=xname, yname=yname)
         self.xyfs.update(**{xyf.name: xyf})
#         self.pd.set_data("imagedata", z)
#         img_plot = self.plot.img_plot("imagedata",
#                       xbounds=(0, 10),
#                        ybounds=(0, 5),
#                    colormap=jet)[0]
#         img_plot.request_redraw()

     def add_plot(self, name, yname, ydata, xname=None, xdata=None):
        xyf=XYFormat(plotter=self)
        self.set_data(yname, ydata)
        if xname!=None and xdata!=None:
            self.set_data(xname, xdata)
        xyf.draw_plot(name=name, yname=yname, xname=xname)
        self.xyfs.update(**{xyf.name: xyf})

     def append_data(self, name, ypoint, xpoint=None):
         xyf=self.xyfs[name]

         ydata=self.pd.get_data(xyf.yname)
         ydata=append(ydata, ypoint)
         self.pd.set_data(xyf.yname, ydata)
         xdata=self.pd.get_data(xyf.xname)
         if xpoint==None:
             xpoint=max(xdata)+range(len(ypoint))+1
         xdata=append(xdata, xpoint)
         self.pd.set_data(xyf.xname, xdata)

     def _default_plot(self):
        plot=Plot(self.pd, padding=50, fill_padding=True,
                        bgcolor="white", use_backbuffer=True,  unified_draw=True)
        plot.tools.append(PanTool(plot, constrain_key="shift"))
        plot.overlays.append(ZoomTool(component=plot, tool_mode="box", always_on=False))
        plot.legend.tools.append(LegendTool(plot.legend, drag_button="right"))
        return plot

     def show(self):
        with traits_enaml.imports():
            from enaml_Plotter import PlotMain

        app = QtApplication()
        view = PlotMain(plotr=self)
        view.show()
        app.start()
#
#     def _plot_add_fired(self):
#         if self.color_index==0:
#             self.dataset_plot( [3,2,5,6], zkey="z", plot_name="Line Plot")
#         else:
#             #self.dataset_plot( [8,9,4,2], zkey="z")
#             arr2=[3,2,5,6]
#             arr3=[7,8,9,10]
#             point=arr2[self.color_index]
#             arr=self.pd.get_data("z0")
#             arr=append(arr, point)
#             self.pd.set_data("z0", arr)
#             arr3=[7,8,9,10]
#             point=arr3[self.color_index]
#             arr=self.pd.get_data("x0")
#             arr=append(arr, point)
#             self.pd.set_data("x0", arr)
#         #print self.pd.arrays
#         self.color_index+=1
#         #self.point_plot( [1,2], zkey="z", x=[1,2, 3], xkey="x", plot_name="Line Plot")
##         if self.color_index==0:
##             self.point_plot( point, zkey="z", x=[1, 2, 3], xkey="x", plot_name="Line Plot")
##         else:
##             self.point_plot( point, zkey="z", plot_name="Line Plot")


if __name__=="__main__":
    with traits_enaml.imports():
        from enaml_Plotter import PlotMain

    app = QtApplication()
    view = PlotMain(plotr=Plotter())
    view.show()
    app.start()

from chaco.api import PlotAxis, GridDataSource, GridMapper, DataRange2D, CMapImagePlot, \
    VPlotContainer, ImageData, DataRange1D, LinearMapper, ColorBar, Plot, ArrayPlotData, jet,\
    HPlotContainer
from enable.component_editor import ComponentEditor
from numpy import squeeze, transpose
#from chaco.tools.api import PanTool, ZoomTool, LineInspector
import h5py
from numpy import amin, amax


class ImagePlot(Atom):
    # container for all plots
    container = Typed(HPlotContainer)

    # Plot components within this container:
    color_plot = Typed(CMapImagePlot)
    vertical_cross_plot = Typed(Plot)
    horizontal_cross_plot = Typed(Plot)
    colorbar = Typed(ColorBar)

    # plot data
    pd_all = Typed(ArrayPlotData)
    #pd_horiz=Instance(ArrayPlotData)
    #pd_vert=Instance(ArrayPlotData)
    #private data storage
    _imag_index=Typed(GridDataSource)
    _image_value=Typed(ImageData)

    def __init__(self, x,y,z):
        super(ImagePlot, self).__init__()
        self.pd_all = ArrayPlotData(imagedata = z)
        #self.pd_horiz = ArrayPlotData(x=x, horiz=z[4, :])
        #self.pd_vert = ArrayPlotData(y=y, vert=z[:,5])

        self._imag_index = GridDataSource(xdata=x, ydata=y, sort_order=("ascending","ascending"))
        index_mapper = GridMapper(range=DataRange2D(self._imag_index))
        self._imag_index.on_trait_change(self._metadata_changed,
                                          "metadata_changed")
        self._image_value = ImageData(data=z, value_depth=1)
        color_mapper = jet(DataRange1D(self._image_value))

        self.color_plot= CMapImagePlot(
            index=self._imag_index,
            index_mapper=index_mapper,
            value=self._image_value,
            value_mapper=color_mapper,
            padding=20,
            use_backbuffer=True,
            unified_draw=True)

        #Add axes to image plot
        left = PlotAxis(orientation='left',
                        title= "Frequency (GHz)",
                        mapper=self.color_plot.index_mapper._ymapper,
                        component=self.color_plot)

        self.color_plot.overlays.append(left)

        bottom = PlotAxis(orientation='bottom',
                        title= "Time (us)",
                        mapper=self.color_plot.index_mapper._xmapper,
                        component=self.color_plot)
        self.color_plot.overlays.append(bottom)

        self.color_plot.tools.append(PanTool(self.color_plot,
                                           constrain_key="shift"))
        self.color_plot.overlays.append(ZoomTool(component=self.color_plot,
                                            tool_mode="box", always_on=False))

        #Add line inspector tool for horizontal and vertical
        self.color_plot.overlays.append(LineInspector(component=self.color_plot,
                                               axis='index_x',
                                               inspect_mode="indexed",
                                               write_metadata=True,
                                               is_listener=True,
                                               color="white"))

        self.color_plot.overlays.append(LineInspector(component=self.color_plot,
                                               axis='index_y',
                                               inspect_mode="indexed",
                                               write_metadata=True,
                                               color="white",
                                               is_listener=True))

        myrange = DataRange1D(low=amin(z),
                              high=amax(z))
        cmap=jet
        self.colormap = cmap(myrange)

        # Create a colorbar
        cbar_index_mapper = LinearMapper(range=myrange)
        self.colorbar = ColorBar(index_mapper=cbar_index_mapper,
                                 plot=self.color_plot,
                                 padding_top=self.color_plot.padding_top,
                                 padding_bottom=self.color_plot.padding_bottom,
                                 padding_right=40,
                                 resizable='v',
                                 width=30)#, ytitle="Magvec (mV)")

        #create horizontal line plot
        self.horiz_cross_plot = Plot(self.pd_horiz, resizable="h")
        self.horiz_cross_plot.height = 100
        self.horiz_cross_plot.padding = 20
        self.horiz_cross_plot.plot(("x", "horiz"))#,
                             #line_style="dot")
#        self.cross_plot.plot(("scatter_index","scatter_value","scatter_color"),
#                             type="cmap_scatter",
#                             name="dot",
#                             color_mapper=self._cmap(image_value_range),
#                             marker="circle",
#                             marker_size=8)

        self.horiz_cross_plot.index_range = self.color_plot.index_range.x_range

        #create vertical line plot
        self.vert_cross_plot = Plot(self.pd_vert, width = 140, orientation="v",
                                resizable="v", padding=20, padding_bottom=160)
        self.vert_cross_plot.plot(("y", "vert"))#,
#                             line_style="dot")
       # self.vert_cross_plot.xtitle="Magvec (mV)"
 #       self.vertica_cross_plot.plot(("vertical_scatter_index",
 #                              "vertical_scatter_value",
 #                              "vertical_scatter_color"),
 #                            type="cmap_scatter",
 #                            name="dot",
 #                            color_mapper=self._cmap(image_value_range),
 #                            marker="circle",
  #                           marker_size=8)

        self.vert_cross_plot.index_range = self.color_plot.index_range.y_range

        # Create a container and add components
        self.container = HPlotContainer(padding=40, fill_padding=True,
                                        bgcolor = "white", use_backbuffer=False)
        inner_cont = VPlotContainer(padding=0, use_backbuffer=True)
        inner_cont.add(self.horiz_cross_plot)
        inner_cont.add(self.color_plot)
        self.container.add(self.colorbar)
        self.container.add(inner_cont)
        self.container.add(self.vert_cross_plot)

    def _metadata_changed(self, old, new):
        """ This function takes out a cross section from the image data, based
        on the line inspector selections, and updates the line and scatter
        plots."""

        #self.cross_plot.value_range.low = self.minz
        #self.cross_plot.value_range.high = self.maxz
        #self.cross_plot2.value_range.low = self.minz
        #self.cross_plot2.value_range.high = self.maxz
        if self._imag_index.metadata.has_key("selections"):
            x_ndx, y_ndx = self._imag_index.metadata["selections"]
            if y_ndx and x_ndx:
#                xdata, ydata = self._image_index.get_data()
#                xdata, ydata = xdata.get_data(), ydata.get_data()
                self.pd_horiz.set_data("horiz", self._image_value.data[y_ndx,:])
                self.pd_vert.set_data("vert", self._image_value.data[:,x_ndx])
#                    scatter_index=array([xdata[x_ndx]]),
#                    scatter_index2=array([ydata[y_ndx]]),
#                    scatter_value=array([self._image_value.data[y_ndx, x_ndx]]),
#                    scatter_value2=array([self._image_value.data[y_ndx, x_ndx]]),
#                    scatter_color=array([self._image_value.data[y_ndx, x_ndx]]),
#                    scatter_color2=array([self._image_value.data[y_ndx, x_ndx]])
#                )
#        else:
#            self.pd.update_data({"scatter_value": array([]),
#                "scatter_value2": array([]), "line_value": array([]),
#                "line_value2": array([])})


#if __name__ == "__main__":

#    filename="/Users/thomasaref/Dropbox/Dad stuff/sample3/digitizer/lt/sample3_digitizer_f_sweep_t_300mk_100nspulse.hdf5"
#
#    with h5py.File(filename, 'r') as f:
#
#        time=f["Traces"]["d - AvgTrace - t"][:]
#        Magvec=f["Traces"]["d - AvgTrace - Magvec"][:]
#        frequency=f["Data"]["Data"][:]
#    #    for name in f["Data"]:
#    #        print name
#
#    time=squeeze(time)
#    Magvec=squeeze(Magvec)
#    frequency=squeeze(frequency)
#
#    x = time[:,0]*1.0e6
#    y = frequency[0,:]/1.0e9
#    z=transpose(Magvec*1000.0)
#
#    ip=ImagePlot(xs,ys,z)
#    ip.configure_traits()

#class Image_Plot(Atom):
#    plot_control=Instance(Plot_Control)
#    xtitle=DelegatesTo('plot_control')
#    ytitle=DelegatesTo('plot_control')
#    ztitle=DelegatesTo('plot_control')
#    request_redraw=DelegatesTo('plot_control')
#    #ykeys=DelegatesTo('plot_control')
#    container = Typed(HPlotContainer)
#    color_plot = Typed(CMapImagePlot)
#    plot=Instance(Plot)
#    vertical_cross_plot = Typed(Plot)
#    horizontal_cross_plot = Typed(Plot)
#    colorbar = Typed(ColorBar)
#    pd_all = Instance(ArrayPlotData)
#    _image_index=Instance(GridDataSource)
#    _image_value=Instance(ImageData)
#    data=Dict()
#
#    pd=Instance(ArrayPlotData)
#
#    traits_view = View(Group(Item('container', editor=ComponentEditor(), show_label=False),
#                             orientation='horizontal'),
#        width=1000, height=700, resizable=True, title="Chaco Plot")
#
#    def _xtitle_changed(self):
#        self.horiz_cross_plot.x_axis.title=self.xtitle
#        self.plot.x_axis.title=self.xtitle
#
#    def _ytitle_changed(self):
#        self.vert_cross_plot.y_axis.title=self.ytitle
#        self.plot.y_axis.title=self.ytitle
#
#    def _request_redraw_fired(self):
#        self.color_plot.request_redraw()
#        self.horiz_cross_plot.request_redraw()
#        self.vert_cross_plot.request_redraw()
#
#    def __init__(self, data, plot_control):
#        super(Image_Plot, self).__init__()
#        self.plot_control=plot_control
#        z=zeros((len(data['y']['0']), len(data['x']['0'])))
#        z[:] = nan
#        for key, item in data['z'].iteritems():
#            z[int(key)]=item
#        x=data['x']['0']
#        y=data['y']['0']
#        self.pd = ArrayPlotData(z=z, x=x, y=y, horiz=z[0, :], vert=z[:, 0])
#        self.plot=Plot(self.pd, padding=50, fill_padding=True,
#                        bgcolor="white", use_backbuffer=True,  unified_draw=True)
#        xgrid, ygrid = meshgrid(x, y)
#
#        color_plot=self.plot.img_plot('z', name="img_plot", xbounds=xgrid, ybounds=ygrid)[0]
#        self._image_index = color_plot.index #GridDataSource(xdata=x, ydata=y, sort_order=("ascending","ascending"))
#        self._image_index.on_trait_change(self._metadata_changed, "metadata_changed")
#        self._image_value=color_plot.value
#        self.value_range=DataRange1D(self._image_value)
#        color_plot.color_mapper = jet(self.value_range)
#        color_plot.tools.append(PanTool(color_plot,
#                                           constrain_key="shift"))
#        color_plot.overlays.append(ZoomTool(component=color_plot,
#                                            tool_mode="box", always_on=False))
#
#        color_plot.overlays.append(LineInspector(component=color_plot,
#                                               axis='index_x',
#                                               inspect_mode="indexed",
#                                               write_metadata=True,
#                                               is_listener=True,
#                                               color="white"))
#
#        color_plot.overlays.append(LineInspector(component=color_plot,
#                                               axis='index_y',
#                                               inspect_mode="indexed",
#                                               write_metadata=True,
#                                               color="white",
#                                               is_listener=True))
#
#        cbar_index_mapper = LinearMapper(range=self.value_range)
#        self.colorbar = ColorBar(index_mapper=cbar_index_mapper,
#                                 plot=color_plot,
#                                 padding_top=color_plot.padding_top,
#                                 padding_bottom=color_plot.padding_bottom,
#                                 padding_right=40,
#                                 resizable='v',
#                                 width=30)#, ytitle="Magvec (mV)")
#
#        #create horizontal line plot
#        self.horiz_cross_plot = Plot(self.pd, resizable="h", height=100, padding=50)
#        self.horiz_cross_plot.plot(("x", "horiz"))#,
#        self.horiz_cross_plot.index_range = color_plot.index_range.x_range
#
#        #create vertical line plot
#        self.vert_cross_plot = Plot(self.pd, width = 100, orientation="v",
#                                resizable="v", padding=50, padding_bottom=250)
#        self.vert_cross_plot.plot(("y", "vert"))
#        self.vert_cross_plot.index_range = color_plot.index_range.y_range
#        #self.vert_cross_plot.x_axis.tick_label_formatter = lambda x: '%.2g'%x
#        self.color_plot=color_plot
#
#        self.container = HPlotContainer(padding=40, fill_padding=True,
#                                        bgcolor = "white", use_backbuffer=False)
#        inner_cont = VPlotContainer(padding=0, use_backbuffer=True)
#        inner_cont.add(self.horiz_cross_plot)
#        inner_cont.add(self.plot)
#        self.container.add(self.colorbar)
#        self.container.add(inner_cont)
#        self.container.add(self.vert_cross_plot)
#        #self.vert_cross_plot.y_axis.title="Frequency"
#        #self.horiz_cross_plot.x_axis.title="Time (us)"
#
#    def _metadata_changed(self, old, new):
#        if self._image_index.metadata.has_key("selections"):
#            x_ndx, y_ndx = self._image_index.metadata["selections"]
#            if y_ndx and x_ndx:
#                self.pd.set_data("horiz", self._image_value.data[y_ndx,:])
#                self.pd.set_data("vert", self._image_value.data[:,x_ndx])
#
#class Line_Plot(HasTraits):
#    plot_control=Instance(Plot_Control)
#    request_redraw=DelegatesTo('plot_control')
#    new_plot=DelegatesTo('plot_control')
#    xtitle=DelegatesTo('plot_control')
#    ytitle=DelegatesTo('plot_control')
#    title=DelegatesTo('plot_control')
#    show_legend=DelegatesTo('plot_control')
#    xyformat=DelegatesTo('plot_control')
#    plot=Instance(Plot)
#    keymap=DelegatesTo('plot_control') #Dict()
#    color_index=Int()
#    mycolors=List([ 'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange'])
#    value_scale=DelegatesTo('plot_control')
#    index_scale=DelegatesTo('plot_control')
#    xcomplex=DelegatesTo('plot_control')
#    ycomplex=DelegatesTo('plot_control')
#
#    xkeys=DelegatesTo('plot_control')
#    zkeys=DelegatesTo('plot_control')
#    xindices=DelegatesTo('plot_control')
#    zindices=DelegatesTo('plot_control')
#    pd = Instance(ArrayPlotData)
#
#    def _value_scale_changed(self):
#         #if self.color_index!=0:
#             self.plot.value_scale = self.value_scale
#             self.plot.request_redraw()
#
#    def _index_scale_changed(self):
#         #if self.color_index!=0:
#             self.plot.index_scale = self.index_scale
#             self.plot.request_redraw()
#
#    def _show_legend_changed(self):
#        self.plot.legend.visible = self.show_legend
#        self.plot.request_redraw()
#
#    def _title_changed(self):
#        self.plot.title = self.title
#        self.plot.request_redraw()
#
#    def _xtitle_changed(self):
#        self.plot.x_axis.title=self.xtitle
#        self.plot.request_redraw()
#
#    def _ytitle_changed(self):
#        self.plot.y_axis.title=self.ytitle
#        self.plot.request_redraw()
#
#    def _request_redraw_fired(self):
#        self.plot.request_redraw()
#
#    def _new_plot_fired(self):
#        for key in self.plot.plots.keys():
#            self.remove_plot(key)
#        self.color_index=0
#        for n, name in enumerate(self.zkeys):
#            key='z'+str(name)
#            self.add_plot(key)
#
#    def _zkeys_changed(self,  name, old, new):
#        #print self.pd.list_data()
#        n=0
#        for key in self.pd.list_data():
#            if int(key[1:]) in new:
#                self.add_plot(key)
#                n=n+1
#            else:
#                self.remove_plot(key)
#
##        for key, plot in self.plot.plots.iteritems():
##            if int(key[1:]) in new:
##                if self.xyformat.t_color=="transparent" or self.xyformat.t_color==(1.0, 1.0, 1.0, 1.0) :
##                    color=self.mycolors[mod(n, len(self.mycolors))]
##                else:
##                    color=self.xyformat.t_color
##                plot[0].color=color
##                #plot[0].outline_color=self.xyformat.outline_color,
##                n=n+1
##
##            else:
##               plot[0].color="none"
#               #plot[0].outline_color="none"
#
#    def add_plot(self, key, z, xkey='x0', x=None):
#        if key not in self.plot.plots.keys() and key[0]!='x':
#            if self.xyformat.t_color=="transparent" or self.xyformat.t_color==(1.0, 1.0, 1.0, 1.0) :
#                color=self.mycolors[mod(self.color_index, len(self.mycolors))]
#            else:
#                color=self.xyformat.t_color
#
#            if x!=None:
#                self.pd.set_data(xkey, x)
#            self.pd.set_data(key, z)
#
#            #if self.color_index<len(self.xkeys):
#            #    xkey='x'+str(self.xkeys[self.color_index])
#            #else:
#            #    xkey='x'+str(self.xkeys[0])
#            self.plot.plot((xkey, key),
#                           name=key,
#                           type=self.xyformat.plot_type,
#                           line_width=self.xyformat.line_width,
#                           color=color,
#                           outline_color=self.xyformat.outline_color,
#                           marker = self.xyformat.marker,
#                           marker_size = self.xyformat.marker_size)
#            self.color_index=self.color_index+1
#
#    def remove_plot(self, key):
#        if key in self.plot.plots.keys():
#            self.plot.delplot(key)
#
#    def __init__(self, data, plot_control, *args, **kws):
#        super(Line_Plot, self).__init__(*args, **kws)
#        self.plot_control=plot_control
#        self.pd = ArrayPlotData()
#
#        for name, arr in sorted(data['z'].iteritems()):
#                self.pd.set_data('z'+str(name), arr)
#
#        for name, arr in sorted(data['x'].iteritems()):
#                self.pd.set_data('x'+str(name), arr)
#
#        plot = Plot(self.pd, padding=50, fill_padding=True,
#                        bgcolor="white", use_backbuffer=True)
#
#        # Attach some tools to the plot
#        plot.tools.append(PanTool(plot))
#        zoom = ZoomTool(component=plot, tool_mode="box", always_on=False)
#        plot.overlays.append(zoom)
#        plot.legend.tools.append(LegendTool(plot.legend, drag_button="right"))
#        self.plot=plot
#
#        for n, item in enumerate(self.zkeys):
#                key='z'+str(item)
#                if self.xyformat.t_color=="transparent" or self.xyformat.t_color==(1.0, 1.0, 1.0, 1.0) :
#                    color=self.mycolors[mod(n, len(self.mycolors))]
#                else:
#                    color=self.xyformat.t_color
#                if n<len(self.xkeys):
#                    xkey='x'+str(self.xkeys[n])
#                else:
#                    xkey='x'+str(self.xkeys[0])
#                #n=n+1
#                #self.pd.set_data(key, magphase(self._image_value.data[int(item)], self.ycomplex))
#                self.plot.plot((xkey, key),
#                                name=key,
#                                type=self.xyformat.plot_type,
#                                line_width=self.xyformat.line_width,
#                                color=color,
#                                outline_color=self.xyformat.outline_color,
#                                marker = self.xyformat.marker,
#                                marker_size = self.xyformat.marker_size)
#        self.plot.value_scale = self.value_scale
#        self.plot.index_scale= self.index_scale
#
#
#    traits_view = View(Item('plot', style='custom',editor=ComponentEditor(),
#                             show_label=False),
#                    resizable=True, title="Chaco Plot",
#                    width=800, height=700, #kind='modal',
#                    buttons=[OKButton, CancelButton]
#                    )