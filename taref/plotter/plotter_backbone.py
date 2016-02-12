# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:48:42 2016

@author: thomasaref
"""


from taref.core.log import log_debug
from atom.api import observe, Atom, Typed, Bool, cached_property, Float
from matplotlib import cm
from collections import OrderedDict
from matplotlib.axes import Axes
from matplotlib.figure import Figure

class PlotObserver(object):
    """decorator object that adds auto drawing of plot to observe"""
    def __init__(self, *args, **kwargs):
        self.args=args
        self.update_legend=kwargs.get("update_legend", False)

    def __call__(self, func):
        def new_func(obj, change):
            if change["type"]=="update":
                func(obj, change)
                obj.update_plot(self.update_legend)
        return observe(*self.args)(new_func)

def plot_observe( *args, **kwargs):
    return PlotObserver(*args, **kwargs)

class SimpleSetter(Atom):
    def simple_set(self, obj, param):
        getattr(obj, "set_"+param)(getattr(self, param))

class PlotMaster(SimpleSetter):
    figure=Typed(Figure)
    fig_height=Float(4.0)
    fig_width=Float(4.0)
    axes=Typed(Axes)
    auto_draw=Bool(True)
    show_legend=Bool(False)

    plot_dict=Typed(OrderedDict)

    horiz_fig=Typed(Figure)
    horiz_axe=Typed(Axes)
    vert_fig=Typed(Figure)
    vert_axe=Typed(Axes)

    def _default_figure(self):
        return Figure(figsize=(self.fig_height, self.fig_width))

    def _default_axes(self):
         axes=self.figure.add_subplot(111)
         axes.autoscale_view(True)
         return axes

    def draw(self):
        if self.figure.canvas!=None:
            self.figure.canvas.draw()
            self.get_member("plot_names").reset(self)

    def legend(self):
        lgnd=self.axes.legend()
        if lgnd is not None:
            lgnd.draggable()

    def legend_remove(self):
        if self.axes.legend_ is not None:
            self.axes.legend_.remove()


    def _default_plot_dict(self):
        plot_dict=OrderedDict()
        #xyfs["All"]=AllXYFormat(plotter=self, name="All")
        return plot_dict

    @cached_property
    def plot_names(self):
        return self.plot_dict.keys()

    def _default_horiz_fig(self):
        return Figure(figsize=(self.fig_width, 1.0))

    def _default_horiz_axe(self):
        h_axe=self.horiz_fig.add_subplot(111, sharex=self.axes)
        return h_axe

    def _default_vert_fig(self):
        return Figure(figsize=(1.0, self.fig_height))

    def _default_vert_axe(self):
        v_axe=self.vert_fig.add_subplot(111, sharey=self.axes)
        return v_axe

    def update_plot(self, update_legend=True):
        if self.auto_draw:
            self.draw()
        if update_legend:
            if self.show_legend:
                self.legend()

class PlotUpdate(SimpleSetter):
    plotter=Typed(PlotMaster)

    def update_plot(self, update_legend=True):
        self.plotter.update_plot(update_legend)



colormap_names=("jet", "rainbow", "nipy_spectral", u'cool', u'coolwarm', u'copper', 'cubehelix', u'flag', u'gist_earth', u'gist_gray',
                 u'gist_heat', u'gist_ncar', u'gist_rainbow', u'gist_stern', u'gist_yarg', u'gnuplot', u'gnuplot2', u'gray', u'hot', u'hsv',  u'ocean', u'pink', u'prism',
                 u'seismic', u'spectral', u'spring', u'summer', u'terrain', u'winter',)

cmaps = {'Perceptually Uniform Sequential' : ['viridis', 'inferno', 'plasma', 'magma'],
         'Sequential' : ['Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                      'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'],
         'Sequential (2)' : ['afmhot', 'autumn', 'bone', 'cool', 'copper', 'gist_heat', 'gray', 'hot', 'pink', 'spring', 'summer', 'winter'],
         'Diverging' : ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral','seismic'],
         'Qualitative' : ['Accent', 'Dark2', 'Paired', 'Pastel1','Pastel2', 'Set1', 'Set2', 'Set3'],
         'Miscellaneous' : ['gist_earth', 'terrain', 'ocean', 'gist_stern', 'brg', 'CMRmap', 'cubehelix','gnuplot', 'gnuplot2', 'gist_ncar',
                         'nipy_spectral', 'jet', 'rainbow','gist_rainbow', 'hsv', 'flag', 'prism']}

colors_tuple=('auto', 'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange', 'darkblue', 'darkred')

markers_tuple=(".", ",", "o", "v", "^", "<",">", "1", "2", "3", "4", "8", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_", "$2/3$")

if __name__=="__main__":
    a=PlotObserver("blah", "upd")
    print a.args
    print a.update_legend