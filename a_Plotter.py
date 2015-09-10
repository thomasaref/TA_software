# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:53:23 2014

@author: thomasaref
"""

from LOG_functions import log_debug
from numpy import angle, absolute, dtype, log10, meshgrid, arange, linspace, sin, mean, amax, amin
from numpy import split, squeeze, array, transpose, concatenate, atleast_2d, ndim, shape
from enaml import imports
from enaml.qt.qt_application import QtApplication
from atom.api import Atom, Int, Enum, Float, List, Dict, Typed, Unicode, ForwardTyped
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib.figure import Figure
from matplotlib.axes import Axes



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
#import  matplotlib.pyplot as plt # import plot
from h5py import File

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp.hdf5"
with File(file_path, 'r') as f:
    Magvec=f["Traces"]["Agilent VNA - S21"][:]
    yoko=f["Data"]["Data"][:]
    f0, fstep=squeeze(f["Traces"]['Agilent VNA - S21_t0dt'][:])
print shape(Magvec)
Magvec=Magvec[:,0,-500:]+1j*Magvec[:,1,-500:]
#Magvec=Magvec-mean(Magvec[:, 50:60], axis=1, keepdims=True)
Magvec=transpose(transpose(Magvec)-Magvec[:, 431]) #, axis=1, keepdims=True))

def dB(x):
    return 20*log10(absolute(x))
    
Magvec=dB(Magvec)
print amax(Magvec), amin(Magvec)
yoko=squeeze(yoko)

l=shape(Magvec)[0]
freq=linspace(f0, f0+fstep*(l-1), l)

#fig, ax4 = plt.subplots(1,1)
segs=[]
segs.append(list(zip(freq, Magvec[:, 1])))
#segs.append(list(zip(freqb, Magvecb[:, 1])))

#col = LineCollection(segs)#, offsets=offs)
#ax4.add_collection(col, autolim=True)
#col.set_color(colors)
#ax4.autoscale_view()
#ax4.set_title('Reflection')
#ax4.set_xlabel('Frequency (Hz)')
#ax4.set_ylabel('S11 (dB)')

#plt.show()
#line2D= plt.plot([0,12])
#print line2D[0].get_data()
#fig, ax2 = plt.subplots(1,1)
#print isinstance(ax2, Axes)
#print dir(fig), dir(ax2)
# The same data as above, but fill the curves.
#from matplotlib import collections, transforms

#col = collections.PolyCollection([((0,0), (0,1), (1,1), (1,0)), ((0,0), (0,1), (1,1), (1,0))])#,
                                #transOffset=ax2.transData)
#print dir(col)#.properties()#get_xy()      
#print [c.to_polygons() for c in col.get_paths()]
#print help(col.update)

#col.set_verts([((1,1), (1,2), (3,1))])
#print [c.to_polygons() for c in col.get_paths()]

#trans = transforms.Affine2D().scale(fig.dpi/72.0)
#col.set_transform(trans)  # the points to pixels transform
#ax2.add_collection(col, autolim=True)
#col.set_color(colors)


#ax2.autoscale_view()
#ax2.set_title('PolyCollection using offsets')

#plt.show()

#fig1 = Figure()
#ax1 = fig1.add_subplot(111)
#print type(ax1)
#ax1.plot([1, 2, 3])
#ax1.axhline(linewidth=4, color="g")

#fig2 = Figure()
#ax2 = fig2.add_subplot(111)
#ax2.plot([5, 2, 8, 1])

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
    colormap=Enum("jet")

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
     xlabel=Unicode()
     ylabel=Unicode()

     xyfs=Dict()
     #pd=Typed(ArrayPlotData, ())
     plot= ForwardTyped(lambda: Plot)
     color_index=Int()
     clts=Dict()
     fig=Typed(Figure)
     axe=Typed(Axes)
     #clt=Typed(PolyCollection)
     plottables=Dict()

     overall_plot_type=Enum("XY", "img", "polygon")
     value_scale=Enum('linear', 'log')
     index_scale=Enum('linear', 'log')

     #def _default_clt(self):
     #    return PolyCollection([((0,0), (0,0))], alpha=0.6, antialiased=True)#, rasterized=False, antialiased=False)
     
     def _default_axe(self):
         axe=self.fig.add_subplot(111)
         axe.autoscale_view(True)
         return axe
         
     def _default_fig(self):
         return Figure()

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

     def _observe_title(self, change):
         self.axe.set_title(self.title)
         #self.plot.request_redraw()

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

     def set_data(self, zname, zdata, zcolor):
         if zdata!=None:
             if self.overall_plot_type=="polygon":
                if zname not in self.clts: #plottables['plotted']:#self.pd.list_data():
                    clt=PolyCollection(zdata, alpha=0.5, antialiased=True)#, rasterized=False, antialiased=False)
                    clt.set_color(colorConverter.to_rgba(zcolor))                
                    self.clts[zname]=clt
                    self.axe.add_collection(self.clts[zname], autolim=True)
                else:                
                    self.clts[zname].set_verts(zdata)
             if self.overall_plot_type=="XY":
                 if zname not in self.clts:
                     clt = LineCollection(zdata)#, offsets=offs)
                     clt.set_color(colors)
                     print dir(clt)
                     self.clts[zname]=clt
                     self.axe.add_collection(self.clts[zname], autolim=True)
                     self.axe.autoscale_view()
                 else:
                     self.clts[zname].set_segments(zdata)
             if self.overall_plot_type=="img":
                 if zname not in self.clts:
                     #print dir(self.axe)
                     self.axe.imshow( Magvec, vmin=-100, vmax=amax(Magvec), aspect="auto", origin="lower")# cmap='RdBu')#,
                     self.axe.set_title('pcolorfast')
                     #self.axe.colorbar()
     def draw(self):
         if self.fig.canvas!=None:
             #trans = transforms.Affine2D().scale(self.fig.dpi/72.0)
             #self.clt.set_transform(trans)  # the points to pixels transform
             #self.clt.set_color(colors)
         
             #self.axe.autoscale_view(True)
             self.fig.canvas.draw()

     def set_xlim(self, xmin, xmax):
         self.axe.set_xlim(xmin, xmax)

     def set_ylim(self, ymin, ymax):
         self.axe.set_ylim(ymin, ymax)
         
     def get_data(self, zname, index=None, axis=0):
        data=[c.to_polygons() for c in self.clt.get_paths()]
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
            log_debug("data set")            
            self.plot.plot(("x"+str(n), "y"+str(n)),
                          type="polygon",
                          face_color=cn, #colors[nsides],
                          hittest_type="poly"
                          )[0]
            log_debug("plot occured")

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

#     def _default_plot(self):
#        global Plot, PanTool, ZoomTool, LegendTool
#        if Plot==None:
#            from chaco.plot import Plot
#        if PanTool==None or ZoomTool==None or LegendTool==None:
#            from chaco.tools.api import PanTool, ZoomTool,  LegendTool #, LineInspector
#
#        plot=Plot(self.pd, padding=50, fill_padding=True,
#                        bgcolor="white", use_backbuffer=True,  unified_draw=True)#, use_downsampling=True)
#        plot.tools.append(PanTool(plot, constrain_key="shift"))
#        plot.overlays.append(ZoomTool(component=plot, tool_mode="box", always_on=False))
#        plot.legend.tools.append(LegendTool(plot.legend, drag_button="right"))
#        return plot

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
        with imports():
            from e_Plotter import PlotMain
        app = QtApplication()
        view = PlotMain(plotr=self)
        view.show()
        app.start()

if __name__=="__main__":
    a=Plotter()
    a.overall_plot_type="img"
    a.set_data("my_line", segs, "blue")
    a.show()
    

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
    #print z
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

