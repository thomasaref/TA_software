# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:53:23 2014

@author: thomasaref
"""

from taref.plotter.plotter_backbone import mycolors
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

from matplotlib import rcParams
rcParams['axes.labelsize'] = 14
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['legend.fontsize'] = 9

#rcParams['figure.figsize'] = 4.3, 4.2
#rcParams['figure.dpi']=150
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

class testproxy(Atom):
    plotter=ForwardTyped(lambda: Plotter, ())

from taref.plotter.fig_format import Fig
class Plotter(SubAgent):
    base_name="plot"
    plt_colors=mycolors #['auto', 'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange']

    title=Unicode()



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

    def activated(self):
        pass
        #self.fig.canvas.mpl_connect('motion_notify_event', mpl_drag_event(self))
        #self.fig.canvas.mpl_connect('motion_notify_event', mpl_click_event(self, arange(200), arange(200))) #button_press_event

        #self.fig.canvas.mpl_connect('button_press_event', mpl_click_event(self))
        #self.fig.canvas.mpl_connect('scroll_event', mpl_scroll_event(self))

    xyfs=Typed(OrderedDict)

    def _default_xyfs(self):
        xyfs=OrderedDict()
        xyfs["All"]=AllXYFormat(plotter=self, name="All")
        return xyfs

    @private_property
    def xyfs_keys(self):
        return self.xyfs.keys()

    @private_property
    def xyfs_items(self):
        return self.xyfs.values()

    fig=Typed(Figure).tag(private=True)
    axe=Typed(Axes).tag(private=True)

    plot_type_list=["Line plot", "Scatter plot", "Colormap", "Polygon", "Text"]

    @private_property
    def plot_type_map(self):
        return {"Line plot" : self.line_plot,
                "Scatter plot" : self.scatter_plot,
                "Colormap" : self.colormap,
                "Polygon" : self.poly_plot,
                "Text" : self.add_text}





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
#    print a.clts["blah"].get_color()
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