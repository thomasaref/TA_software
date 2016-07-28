# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:28:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read_NP
from taref.plotter.api import scatter
npr=TA88_Read_NP(file_path=r"/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/discard/S2016_07_28_171620/meas.txt",
                 show_data_str=True)
data=npr.read()
scatter(data[:, 0], data[:, 1]).show()