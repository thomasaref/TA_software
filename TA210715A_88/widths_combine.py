# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:36:21 2016

@author: thomasaref
"""

from D0514_highfrq1sidelobe import a as d0514
from D0316_S4A1_coupling_midpeak import a as d0316
from D0506_lowfrq34sidelobe import a as d0506
from D0509_lowfrq2sidelobe import a as d0509
from D0503_lowfrq1sidelobe import a as d0503

pl=d0514.widths_plot()#.show()
d0316.widths_plot(pl=pl)#.show()
d0506.widths_plot(pl=pl)#.show()
d0509.widths_plot(pl=pl)#.show()
d0503.widths_plot(pl=pl)#.show()

pl=d0514.center_plot()#.show()
d0316.center_plot(pl=pl)#.show()
d0506.center_plot(pl=pl)#.show()
d0509.center_plot(pl=pl)#.show()
d0503.center_plot(pl=pl)#.show()

#pl=d0514.magabsfilt_colormesh()
#d0316.magabsfilt_colormesh(pl=pl)#.show()
#d0506.magabsfilt_colormesh(pl=pl)#.show()
#d0509.magabsfilt_colormesh(pl=pl)#.show()
d0503.magabsfilt_colormesh(pl=pl).show()

