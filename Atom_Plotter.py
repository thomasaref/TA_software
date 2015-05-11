# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:53:23 2014

@author: thomasaref
"""

from LOG_functions import log_debug
#from chaco.plot import Plot
from chaco.array_plot_data import ArrayPlotData
from chaco.default_colormaps import jet
from numpy import angle, absolute, dtype, log10, meshgrid, arange, linspace
from numpy import split, squeeze, array, transpose, concatenate, atleast_2d, ndim
#from chaco.tools.api import PanTool, ZoomTool,  LegendTool #, LineInspector
import traits_enaml
#import enaml
from enaml.qt.qt_application import QtApplication
from atom.api import Atom, Int, Enum, Float, List, Dict, Typed, Unicode, ForwardTyped

#slow imports
Plot = None
PanTool=None
ZoomTool=None
LegendTool=None
PlotGraphicsContext=None



#from matplotlib import rcParams
#rcParams['axes.labelsize'] = 14
#rcParams['xtick.labelsize'] = 9
#rcParams['ytick.labelsize'] = 9
#rcParams['legend.fontsize'] = 9
#
#rcParams['figure.figsize'] = 7.3, 4.2
#rcParams['figure.dpi']=150
#rcParams['xtick.major.width']=2
#rcParams['lines.linewidth']=2
#rcParams['xtick.major.size']=4
#rcParams['axes.linewidth']=2
#rcParams['ytick.major.width']=2
#rcParams['ytick.major.size']=4
##rcParams['lines.solid_joinstyle']='round'
##rcParams['lines.solid_capstyle']='round'
#
## Example data
##import numpy as np
##t = np.arange(0.0, 1.0 + 0.01, 0.01)
##s = np.cos(4 * np.pi * t) + 2
#
## plot some awesome science
##fig.tight_layout(pad=0.1)  # Make the figure use all available whitespace
##fig.savefig('awesome_science.pdf')
#
##from matplotlib.ticker import MaxNLocator
##my_locator = MaxNLocator(6)
## Set up axes and plot some awesome science
##ax.yaxis.set_major_locator(my_locator)
#
#from matplotlib.figure import Figure
#fig1 = Figure()
#ax1 = fig1.add_subplot(111)
#ax1.plot([1, 2, 3])
##ax1.axhline(linewidth=4, color="g")
#
#fig2 = Figure()
#ax2 = fig2.add_subplot(111)
#ax2.plot([5, 2, 8, 1])
#
#figures = {
#    'one': fig1,
#    'two': fig2,
#}

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
                #print self.rend_list

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
        if self.xdata!=None:
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
        if self.xdata!=None:
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
     title=Unicode()
     xlabel=Unicode()
     ylabel=Unicode()

     xyfs=Dict()
     pd=Typed(ArrayPlotData, ())
     plot= ForwardTyped(lambda: Plot)
     color_index=Int()
     #figures=Dict(default=figures)
     plottables=Dict()

     overall_plot_type=Enum("XY plot", "img plot")
     value_scale=Enum('linear', 'log')
     index_scale=Enum('linear', 'log')

     def _observe_value_scale(self, change):
         if self.overall_plot_type=="XY plot":
             self.plot.value_scale=self.value_scale
             self.plot.request_redraw()

     def _observe_index_scale(self, change):
         if self.overall_plot_type=="XY plot":
             self.plot.index_scale=self.index_scale
             self.plot.request_redraw()

     def _default_plottables(self):
         return dict(plotted=[None])
        #tempdict=dict()
        #for instr in self.instruments:
            #tempdict[instr.name]=[]
        #    tempdict[instr.name]=instr.get_all_tags('plot', True, instr.plot_all, instr.all_params)
            #for key in instr.members().keys():
            #    if instr.get_tag(key, 'plot', instr.plot_all):
            #        tempdict[instr.name].append(key)
        #    if tempdict[instr.name]==[]:
        #        tempdict[instr.name]=instr.members().keys()
        #return tempdict



     def _observe_title(self, change):
         self.plot.title=self.title
         self.plot.request_redraw()

     def _observe_xlabel(self, change):
         self.plot.x_axis.title=self.xlabel
         self.plot.request_redraw()

     def _observe_ylabel(self, change):
         self.plot.y_axis.title=self.ylabel
         self.plot.request_redraw()

     def _default_xyfs(self):
         xyf=AllXYFormat(plotter=self)
         return {"All":xyf}

     def delete_all_plots(self):
         for key in self.plot.plots.keys():
                self.plot.delplot(key)
         self.color_index=0

     def _save(self):
         global PlotGraphicsContext
         if PlotGraphicsContext==None:
             from chaco.plot_graphics_context import PlotGraphicsContext
         win_size = self.plot.outer_bounds
         plot_gc = PlotGraphicsContext(win_size)#, dpi=300)
         plot_gc.render_component(self.plot)
         plot_gc.save("image_test.png")

     def set_data(self, zname, zdata):
        if zname not in self.pd.list_data():
            self.plottables['plotted'].append(zname)
        self.pd.set_data(zname, zdata)

     def get_data(self, zname, index=None, axis=0):
        data=self.pd.get_data(zname)
        if index==None:
            return data
        if axis==0:
            return atleast_2d(data)[index, :]
        return atleast_2d(data)[:, index]
        
     def add_poly_plot_old(self, n, verts, cn="green", polyname=""):
         nxarray, nyarray = transpose(verts)
         xname=polyname+"x" + str(n)
         yname=polyname+"y" + str(n)
         self.pd.set_data(xname, nxarray, coord='x') #coord='x' is likely redundant or a metadata tag
         self.pd.set_data(yname, nyarray, coord='y')
         self.plot.plot((xname, yname),
                          type="polygon",
                          face_color=cn, #colors[nsides],
                          hittest_type="poly")[0]

     def add_poly_plot(self, n, verts, cn="green", polyname=""):
        #for n,p in enumerate(self.polylist):
            log_debug("drawing polygon #: {0}".format(n))
            #npoints = p.verts #n_gon(center=p, r=2, nsides=nsides)
            nxarray, nyarray = transpose(verts)
            self.pd.set_data("x" + str(n), nxarray)
            self.pd.set_data("y" + str(n), nyarray)
            self.plot.plot(("x"+str(n), "y"+str(n)),
                          type="polygon",
                          face_color=cn, #colors[nsides],
                          hittest_type="poly")[0]

     def add_img_plot(self, zname, zdata, xname=None, xdata=None, yname=None,  ydata=None):
         self.add_data(zname=zname, zdata=zdata, xname=xname, xdata=xdata, yname=yname, ydata=ydata, overwrite=True, concat=False)
         print self.pd.get_data(zname)
         xyf=XYFormat(plotter=self)
         xyf.draw_img_plot(name='img_plot', zname=zname, xname=xname, yname=yname)
         self.xyfs.update(**{xyf.name: xyf})
         self.overall_plot_type="img plot"

     def add_line_plot(self, name, zname, zdata, xname=None, xdata=None):
        self.add_data(zname=zname, zdata=zdata, xname=xname, xdata=xdata, overwrite=True)
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

#     def append_data(self, name, zpoint, xpoint=None):
#         xyf=self.xyfs[name]
#         zdata=self.pd.get_data(xyf.zname)
#         zdata=append(zdata, zpoint)
#         self.pd.set_data(xyf.zname, zdata)
#         xdata=self.pd.get_data(xyf.xname)
#         if xpoint==None:
#             xpoint=max(xdata)+range(len(zpoint))+1
#         xdata=append(xdata, xpoint)
#         self.pd.set_data(xyf.xname, xdata)

     def _default_plot(self):
        global Plot, PanTool, ZoomTool, LegendTool
        if Plot==None:
            from chaco.plot import Plot
        if PanTool==None or ZoomTool==None or LegendTool==None:
            from chaco.tools.api import PanTool, ZoomTool,  LegendTool #, LineInspector

        plot=Plot(self.pd, padding=50, fill_padding=True,
                        bgcolor="white", use_backbuffer=True,  unified_draw=True)
        plot.tools.append(PanTool(plot, constrain_key="shift"))
        plot.overlays.append(ZoomTool(component=plot, tool_mode="box", always_on=False))
        plot.legend.tools.append(LegendTool(plot.legend, drag_button="right"))
        return plot

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
         
     def show(self):
        with traits_enaml.imports():
            from enaml_Plotter import PlotMain

        app = QtApplication()
        view = PlotMain(plotr=self)
        view.show()
        app.start()

if __name__=="__main__":
    a=Plotter()
    from numpy import exp, shape
    xs = linspace(0, 3, 3)
    ys = linspace(0, 4, 3)
    x, y = meshgrid(xs,ys)
    z = exp(-(x**2+y**2)/100)
    print z
    #zz= a.splitMultiD(z)
    #print zz
#    zz.append(array([[1],[2],[3]]))
#    print zz
#    print a.gatherMultiD(zz)
    args=([1,2,3], [4,5,6])
    a.add_data('x', args) #z=concatenate(atleast_2d(*args), axis=0)
    a.add_data('x', args) #z=concatenate(atleast_2d(*args), axis=0)

    #print a.get_data('z')
#    print concatenate((z, atleast_2d([7,8,9])))
    a.add_data('z', 7)#, axis=1)
    a.add_data('z', 7)#, axis=1)

    print a.get_data('z', 0)
    a.add_data('z', [11, 12], appen=True) #, axis=1)
    #a.gatherMultiD('z', 12, axis=1)
#    
    print a.get_data('z', 0)
    print a.get_data('z', 0, 1)
    a.add_data('z', [3,4,5,6], appen=False) #, axis=1)
    print a.get_data('z')    
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
    a.add_img_plot(zname="z", zdata=z)#, xname="x", xdata=xs, yname="y", ydata=ys)
    a.show()

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

