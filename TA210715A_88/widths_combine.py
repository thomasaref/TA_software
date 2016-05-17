# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:36:21 2016

@author: thomasaref
"""

from D0514_highfrq1sidelobe import a as d0514
from D0316_S4A1_coupling_midpeak import a as d0316

pl=d0514.widths_plot()#.show()
d0316.widths_plot(pl=pl)#.show()
pl=d0514.magabsfilt_colormesh()
d0316.magabsfilt_colormesh(pl=pl).show()