# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 13:45:52 2015

@author: thomasaref
"""

from Atom_Base import Base
from atom.api import Unicode, Str, Typed, observe, ContainerList
from Atom_Read_File import Read_HDF5
from Atom_Save_File import Save_TXT
from numpy import linspace, shape, ascontiguousarray

class DataRead(Base):
    main_read_file=Unicode("Qubit_hunt1").tag(private=True)
    out_file=Unicode("blah").tag(private=True)    
    dir_path=Unicode("/Users/thomasaref/Dropbox/Current stuff/Logbook/Data_0612").tag(private=True)
    data=Str().tag(discard=True, log=False, width="max", label="")
    read_file=Typed(Read_HDF5).tag(width="max")
    save_file=Typed(Save_TXT).tag(width='max')

    #@observe('read_file.read_event')
    #def obs_read_event(self, change):
    #    self.data="".join(str(self.read_file.data))

    @observe('save_file.save_event')
    def obs_save_event(self, change):
        self.save_file.direct_save(self.data, write_mode='w')

    def _default_read_file(self):
        return Read_HDF5(main_file=self.main_read_file+".hdf5", dir_path=self.dir_path)

    def _default_save_file(self):
        return Save_TXT(main_file=self.out_file+".txt", dir_path=self.read_file.dir_path)

    def data_list(self):
        return self.data.split("\n")

class VNAYokoSweep(DataRead):
    Yoko=ContainerList().tag(inside_type=float, plot=True)
    VNA=ContainerList().tag(inside_type=float, xdata='Yoko', plot=True)        
    
    @observe('read_file.read_event')
    def obs_read_event(self, change):
        startYoko=self.read_file.data["Step config"]['Yokogawa - Voltage']['Step items']["data"][0][3]
        stopYoko=self.read_file.data["Step config"]['Yokogawa - Voltage']['Step items']["data"][0][4]
        stepYoko=self.read_file.data["Step config"]['Yokogawa - Voltage']['Step items']["data"][0][8]
        self.Yoko=ascontiguousarray(linspace(startYoko, stopYoko, stepYoko), dtype=float) #self.data="".join(str(self.read_file.data))
        self.VNA=ascontiguousarray(self.read_file.data["Traces"]['Rohde&Schwarz Network Analyzer - S21']['data'], dtype=float)
        #print type(self.Yoko[0]), type(self.VNA[0])

a=VNAYokoSweep()
#b=a.boss
#

a.show()
if 1:
    a.read_file.read()
    #print a.read_file.data.keys()
    #print a.read_file.data["Step config"]['Yokogawa - Voltage']['Step items']["data"] #['Rohde&Schwarz Network Analyzer - S21'].keys()
    print shape(a.read_file.data["Traces"]['Rohde&Schwarz Network Analyzer - S21']['data'])#[0][0]
    print a.read_file.data["Traces"]['Rohde&Schwarz Network Analyzer - S21']['data'][5,:,10]
    print shape(a.VNA)
    print type(a.VNA[5][1][10]), a.VNA[5][1][10]
    
    startYoko=a.read_file.data["Step config"]['Yokogawa - Voltage']['Step items']["data"][0][3]
    stopYoko=a.read_file.data["Step config"]['Yokogawa - Voltage']['Step items']["data"][0][4]
    stepYoko=a.read_file.data["Step config"]['Yokogawa - Voltage']['Step items']["data"][0][8]
    #print startYoko, stopYoko, stepYoko
    a.add_line_plot('VNA')