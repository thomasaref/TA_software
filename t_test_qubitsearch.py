# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:47:37 2015

@author: thomasaref
"""

from Atom_Read_File import Read_HDF5

a=Read_HDF5(file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/T_testy5_2.hdf5")

a.read()

print a.data["Traces"].keys()
print a.data

#z=a.data["Traces"]["Agilent VNA - S21"].data

#yoko=a.data["Data"]["Data"].data
# ['Juliana Yoko - Voltage', 'Yokogawa 7651 DC Source - GPIB: 4, Juliana Yoko at localhost', 'Voltage', 'V', 'V', 1.0, 0.0, 1.0, inf, -inf, 0.0, 0.0, '')], datatype=<type 'numpy.void'>)), (u'Data', group([(u'Channel names', dataset( data=[('Juliana Yoko - Voltage', '')], datatype=<type 'numpy.void'>)), (u'Data', dataset( data=[[[  5.00000000e+00]]
#
# [[  4.99900007e+00]]
#
# [[  4.99800014e+00]]
#
# ..., 
# [[  2.00000009e-03]]
#
# [[  1.00000005e-03]]
#
# [[  0.00000000e+00]]], datatype=<type 'numpy.ndarray'>)),