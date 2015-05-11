# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 18:27:46 2015

@author: thomasaref
"""

#from Atom_Boss import master as m

from Atom_Plotter import Plotter
from numpy import loadtxt

data=loadtxt(
#'/Users/thomasaref/Dropbox/Current stuff/sample3/vna/sample3.s2p')
'/Users/thomasaref/Dropbox/Current stuff/SAW_useful/cavity_data/room_temp/vna/20140501_cc/sample3.txt')

p=Plotter()

p.add_line_plot("blah", "yname", data[:,3], 'xname', data[:,0]/1.0e9)
p.show()

