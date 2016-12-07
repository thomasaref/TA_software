# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:01:52 2016

@author: thomasaref

Testing combining multiple plots for a paper
"""

from numpy import meshgrid, sqrt, linspace, array, full, NaN, zeros
from taref.plotter.api import colormesh, scatter, line, Plotter
from taref.plotter.plot_format import ColormeshFormat
from matplotlib.pyplot import colorbar, pcolormesh, plot, figure

n = 300
x = linspace(-1.5, 1.5, n)
y = linspace(-1.5, 1.5, n*2)
X, Y = meshgrid(x, y)
Z = sqrt(X**2 + Y**2)


#pl="fig2"

fig=figure()
ax=fig.add_subplot(2, 1, 1)
clt=pcolormesh(Z) #, nrows=2, ncols=1, nplot=1, pl=pl, pf_too=True,
                 #vmin=0.0, vmax=2.0, auto_zlim=False, cmap="afmhot",
                 #auto_ylim=False, y_min=0, y_max=600,
                 #auto_xlim=False, x_min=0, x_max=300)

#pl.xlabel="blah"
#pl.ylabel="yarg"

#pl.axes.yaxis.labelpad=-10
plot( array([0, 300]), array([0, 600]))

cbr=colorbar(clt, ax=ax, label="$S_{33}$")
cbr.set_label("$|S_{11}|$", size=6, labelpad=-5)
#print dir(cbr)
cbr.set_ticks([0, 2])#linspace(0.995, 1.002, 2))
ax.set_xticks(linspace(0, 300, 4))
ax.set_yticks(linspace(0, 600, 2))

ax=fig.add_subplot(2, 2, 3)

clt=pcolormesh(x, y, Z, ) #pl=pl, pf_too=True, auto_zlim=True,
                      #         auto_xlim=True, x_min=0.65, x_max=1.5,
                      #         auto_ylim=True, vmin=0.0, vmax=0.02)
colorbar(clt, ax=ax)
#pl.axes.set_xticks(linspace(0.7, 1.5, 2))
ax=fig.add_subplot(2, 2, 4)

plot(x, 'o')
#                xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}| \times 100$", pl=pl,)
                  #auto_ylim=False, y_min=100*0, y_max=100*0.015, marker_size=3.0,
                  #auto_xlim=False, x_min=-30, x_max=10)#.show()
#pl.axes.set_xticks(linspace(-30, 10, 5))

#a.save_plots([pl])
fig.tight_layout()
pl=Plotter(figure=fig)
pl.plot_dict["blah"]=ColormeshFormat(plotter=pl)
pl.show()



