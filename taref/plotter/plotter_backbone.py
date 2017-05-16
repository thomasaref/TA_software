# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:48:42 2016

@author: thomasaref
"""
#from taref.core.log import log_debug

from matplotlib import rcParams
print rcParams
#rcParams["figure.figsize"]=[9.0, 3.0]
rcParams["font.size"]=8
rcParams['axes.labelsize'] = 8
rcParams['xtick.labelsize'] = 8
rcParams['ytick.labelsize'] = 8
rcParams['legend.fontsize'] = 8

rcParams['xtick.major.width']=1
rcParams['lines.linewidth']=1
rcParams['xtick.major.size']=3
rcParams['axes.linewidth']=1
rcParams['ytick.major.width']=1
rcParams['ytick.major.size']=3

from atom.api import observe, Atom, Typed, Bool, cached_property, Float, Unicode, Instance, Int
from collections import OrderedDict
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.colorbar import Colorbar


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

class PlotMaster(Atom):
    """base plot class contains figure, axes, plot_dict"""
    figure=Typed(Figure)
    fig_height=Float(4.5)
    fig_width=Float(4.5)
    colorbar=Instance(Colorbar)

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

    nrows=Int(1)
    ncols=Int(1)
    nplot=Int(1)
    
    def new_axes(self, *args, **kwargs):
        self.axes=self.figure.add_axes(*args, **kwargs)
        return self.axes
        
    def _observe_nplot(self, change):
        if change["type"]!="create":
            self.axes=self.figure.add_subplot(self.nrows, self.ncols, self.nplot)

    def _default_figure(self):
        return plt.figure(figsize=(self.fig_height, self.fig_width))

    def _default_axes(self):
         axes=self.figure.add_subplot(self.nrows, self.ncols, self.nplot)
         #axes.autoscale_view(True)
         return axes

    def draw(self):
        if self.figure.canvas!=None:
            self.figure.canvas.draw()
            self.get_member("plot_names").reset(self)

    def legend(self, *args, **kwargs):
        """adds the legend and makes it draggable if it does not exist"""
        self.legend_remove()
        lgnd=self.axes.legend(*args, **kwargs)
        if lgnd is not None:
            lgnd.draggable(state=True)

    def legend_remove(self):
        """removes the legend if it exists"""
        if self.axes.legend_ is not None:
            self.axes.legend_.remove()

    @cached_property
    def plot_names(self):
        return self.plot_dict.keys()

    def _default_horiz_fig(self):
        return plt.figure(figsize=(self.fig_width, 1.0))

    def _default_horiz_axe(self):
        h_axe=self.horiz_fig.add_subplot(111)#, sharex=self.axes)
        return h_axe

    def _default_vert_fig(self):
        return plt.figure(figsize=(1.0, self.fig_height))

    def _default_vert_axe(self):
        v_axe=self.vert_fig.add_subplot(111)#, sharey=self.axes)
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

#Spectral, coolwarm Set1 brg_r
colormap_names=("RdBu_r", "RdBu", "spectral", "spectral_r", "Spectral", "Spectral_r",
                "coolwarm", "coolwarm_r", "Set1", "Set1_r", "gist_ncar", "gist_ncar_r",
                "jet", "jet_r", "bwr", "bwr_r",  "brg",  "brg_r",
                "seismic", "seismic_r", "nipy_spectral", "nipy_spectral_r",
                "summer",  "Wistia_r", "pink_r",  "Set2", "Set3",  "Dark2", "prism",
                "PuOr_r", "afmhot_r", "terrain_r", "PuBuGn_r", "RdPu",  "gist_yarg_r", "Dark2_r", "YlGnBu",
                "RdYlBu", "hot_r", "gist_rainbow_r", "gist_stern", "PuBu_r", "cool_r", "cool", "gray", "copper_r", "Greens_r",
                "GnBu", "spring_r", "gist_rainbow", "gist_heat_r", "Wistia", "OrRd_r", "CMRmap", "bone", "gist_stern_r",
                "RdYlGn", "Pastel2_r", "spring", "terrain", "YlOrRd_r", "Set2_r", "winter_r", "PuBu", "RdGy_r",
                "rainbow", "flag_r",  "RdPu_r", "gist_yarg", "BuGn", "Paired_r", "hsv_r",  "cubehelix", "Greens",
                "PRGn", "gist_heat",  "Paired", "hsv", "Oranges_r", "prism_r", "Pastel2", "Pastel1_r", "Pastel1",
                "gray_r",   "gnuplot2_r", "gist_earth", "YlGnBu_r", "copper", "gist_earth_r", "Set3_r",
                "OrRd", "gnuplot_r", "ocean_r",  "gnuplot2", "PuRd_r", "bone_r", "BuPu", "Oranges", "RdYlGn_r", "PiYG",
                "CMRmap_r", "YlGn", "binary_r", "gist_gray_r", "Accent", "BuPu_r", "gist_gray", "flag", "BrBG",
                "Reds", "summer_r", "GnBu_r", "BrBG_r", "Reds_r", "RdGy", "PuRd", "Accent_r", "Blues", "autumn_r",
                "autumn", "cubehelix_r", "ocean", "PRGn_r", "Greys_r", "pink", "binary", "winter", "gnuplot",
                "RdYlBu_r", "hot", "YlOrBr", "rainbow_r", "Purples_r", "PiYG_r", "YlGn_r", "Blues_r", "YlOrBr_r"
                , "Purples",  "Greys", "BuGn_r", "YlOrRd", "PuOr", "PuBuGn", "afmhot")

colormap_names2=(u"bwr", "jet", "rainbow", "nipy_spectral", u'cool', u'coolwarm', u'copper', 'cubehelix', u'flag', u'gist_earth', u'gist_gray',
                 u'gist_heat', u'gist_ncar', u'gist_rainbow', u'gist_stern', u'gist_yarg', u'gnuplot', u'gnuplot2', u'gray', u'hot', u'hsv',  u'ocean', u'pink', u'prism',
                 u'seismic', u'spectral', u'spring', u'summer', u'terrain', u'winter', 'viridis', 'inferno', 'plasma', 'magma')

cmaps = {'Perceptually Uniform Sequential' : ['viridis', 'inferno', 'plasma', 'magma'],
         'Sequential' : ['Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                      'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'],
         'Sequential (2)' : ['afmhot', 'autumn', 'bone', 'cool', 'copper', 'gist_heat', 'gray', 'hot', 'pink', 'spring', 'summer', 'winter'],
         'Diverging' : ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral','seismic'],
         'Qualitative' : ['Accent', 'Dark2', 'Paired', 'Pastel1','Pastel2', 'Set1', 'Set2', 'Set3'],
         'Miscellaneous' : ['gist_earth', 'terrain', 'ocean', 'gist_stern', 'brg', 'CMRmap', 'cubehelix','gnuplot', 'gnuplot2', 'gist_ncar',
                         'nipy_spectral', 'jet', 'rainbow','gist_rainbow', 'hsv', 'flag', 'prism']}

colors_tuple=('auto', 'blue', 'red', 'green', 'purple',  'black', 'darkgray', 'cyan', 'magenta', 'orange', 'darkblue', 'darkred', "white")

markers_tuple=(".", ",", "o", "v", "^", "<",">", "1", "2", "3", "4", "8", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_", "$2/3$")

if __name__=="__main__":
    a=plot_observe("blah", "upd")
    print a.args
    print a.update_legend
