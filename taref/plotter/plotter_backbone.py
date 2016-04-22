# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:48:42 2016

@author: thomasaref
"""


from taref.core.log import log_debug
from taref.core.atom_extension import get_all_tags, get_tag, get_all_params
from atom.api import observe, Atom, Typed, Bool, cached_property, Float, Unicode
#from matplotlib import cm
from collections import OrderedDict
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

class plot_observe(object):
    """decorator object that adds auto drawing of plot to observe decorator"""
    def __init__(self, *args, **kwargs):
        """if kwarg update_legend is true, will update legend,
            if kwarg immediate_update is true, will perform on create"""
        self.args=args
        self.update_legend=kwargs.get("update_legend", False)
        self.immediate_update=kwargs.get("immediate_update", False)

    def __call__(self, func):
        def new_func(obj, change):
            if change["type"]=="update":
                func(obj, change)
                obj.update_plot(self.update_legend)
            elif change["type"]=="create":
                if self.immediate_update:
                    func(obj, change)
        return observe(*self.args)(new_func)

def simple_set(clt, mpl, param, set_str="set_"):
    """utility function that uses clt set_ function to set param"""
    getattr(clt, set_str+param)(getattr(mpl, param))

def process_kwargs(self, kwargs):
    """Goes through all_params and sets the attribute if it is included in kwargs, also popping it out of kwargs.
    if the param is tagged with "former", the kwarg is added back using the value of the param. Returns the processed kwargs"""
    for arg in get_all_params(self): #get_all_tags(self, "former"):
        if arg in kwargs:
            setattr(self, arg, kwargs[arg])
        val=kwargs.pop(arg, None)
        key=get_tag(self, arg, "former", False)
        if key is not False:
            if val is None:
                val=getattr(self, arg)
            kwargs[key]=val
    return kwargs

class PlotMaster(Atom):
    """base plot class contains figure, axes, plot_dict"""
    figure=Typed(Figure)
    fig_height=Float(4.0)
    fig_width=Float(4.0)
    axes=Typed(Axes)
    auto_draw=Bool(True)
    show_legend=Bool(False)

    plot_dict=Typed(OrderedDict, ()).tag(desc="dict of plots contained in figure")

    horiz_fig=Typed(Figure)
    horiz_axe=Typed(Axes)
    vert_fig=Typed(Figure)
    vert_axe=Typed(Axes)

    selected=Unicode()

    show_cross_section=Bool(False)

    def _default_figure(self):
        return plt.figure(figsize=(self.fig_height, self.fig_width))

    def _default_axes(self):
         axes=self.figure.add_subplot(111)
         axes.autoscale_view(True)
         return axes

    def draw(self):
        if self.figure.canvas!=None:
            self.figure.canvas.draw()
            self.get_member("plot_names").reset(self)

    def legend(self):
        """adds the legend and makes it draggable if it does not exist"""
        lgnd=self.axes.legend()
        if lgnd is not None:
            lgnd.draggable(state=True)

    def legend_remove(self):
        """removes the legen if it exists"""
        if self.axes.legend_ is not None:
            self.axes.legend_.remove()

    @cached_property
    def plot_names(self):
        return self.plot_dict.keys()

    def _default_horiz_fig(self):
        return plt.figure(figsize=(self.fig_width, 1.0))

    def _default_horiz_axe(self):
        h_axe=self.horiz_fig.add_subplot(111, sharex=self.axes)
        return h_axe

    def _default_vert_fig(self):
        return plt.figure(figsize=(1.0, self.fig_height))

    def _default_vert_axe(self):
        v_axe=self.vert_fig.add_subplot(111, sharey=self.axes)
        return v_axe

    def update_plot(self, update_legend=True):
        if self.auto_draw:
            self.draw()
        if update_legend:
            if self.show_legend:
                self.legend()

class PlotUpdate(Atom):
    """a base clase that contains a plotter object and defines the update plot method (shortcut to plotter method)"""
    plotter=Typed(PlotMaster)

    def update_plot(self, update_legend=True):
        self.plotter.update_plot(update_legend=update_legend)


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
    a=plot_observe("blah", "upd")
    print a.args
    print a.update_legend
