# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 11:10:14 2015

@author: thomasaref
"""

from TestInstrument import Test_Instrument
from Atom_InstrumentBoss import instrumentboss as inboss


# if you really want to turn off auto saving for instruments use these lines
inboss.saving=False
#from Atom_HDF5 import Save_HDF5
#boss.save_hdf5=Save_HDF5(buffer_save=True)

a=Test_Instrument(name="blah")
b=Test_Instrument(name="bob", view="Field")



def measfunc():
    a.voltage=3

inboss.run=measfunc
#print a.plot_keys
print inboss.plottables
print a.get_tag('v3', 'low')
#boss.save_hdf5.buffer_save=True  #you can enable buffered saving using this line. Data will not save until you hit the save button or close the window

inboss.boot_all()  # this line boots all instruments
inboss.show()
