# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:21:06 2015

@author: thomasaref
"""

from taref.core.filer import Filer
from taref.core.log import log_warning, log_info
from atom.api import Dict, Event, Typed, Unicode
from enaml import imports

class Read_File(Filer):
    data=Dict()
    read_event=Event()
    data_str=Unicode().tag(discard=True, log=False, no_spacer=True, label="", spec="multiline")

    def read(self):
        self.do_read()
        self.read_event()
        return self.data

    def do_read(self):
        log_warning("do_read not implemented!")

    @property
    def view(self):
        return "Read_File"

    @property        
    def view_window(self):
        """stand alone for showing filer."""
        with imports():
            from taref.core.filer_e import ReadBoxMain
        return ReadBoxMain(read_file=self)

#from DXF_functions import readdxflayer
from HDF5_functions import read_hdf5, group
from numpy import loadtxt

class Read_HDF5(Read_File):
    """extends Read_File for HDF5 format files"""
    data=Typed(group)
    def _default_file_type(self):
        return "HDF5"

    def do_read(self):
        self.data=read_hdf5(self.file_path)
        log_info("Read data from hdf5 file: {0}".format(self.file_path))

class Read_NP(Read_File):
    """Reads data using numpy's loadtxt"""
    def _default_file_type(self):
        return "text data"

    def do_read(self):
        self.data={"data":loadtxt(self.file_path)}
        log_info("Read data from numpy text file: {0}".format(self.file_path))

class Read_DXF(Read_File):
    def _default_file_type(self):
        return "dxf"

    
#    """reads a layer of an autocad dxf file"""
#    def read(self, layer="Al"):
#        """reads dxf file in and places polygons in polylist"""
#        polylist=readdxflayer(self.file_path, inlayer=layer)
#        self.data["data"]=polylist
#        return self.data

class Read_TXT(Read_File):
    """extends Read_File for text files"""
    def _default_file_type(self):
        return "text"

    def do_read(self):
        """reads a text file"""
        templist=[]
        with open(self.file_path, 'r') as f:
            for line in f:
                templist.append(line)
        log_info("Read data from text file: {0}".format(self.file_path))
        self.data_distributor(templist)

    def data_distributor(self, templist):
        self.data["data"]=templist
    
    def _observe_read_event(self, change):
        self.data_str="".join(self.data["data"])   
        
if __name__=="__main__":
    #a=Read_File()
    #a.read()
    a=Read_TXT(file_path="/Users/thomasaref/Dropbox/Current stuff/TA_software/idt2.jdf")
    #a=Read_HDF5()
    from taref.core.SHOW_functions import show
    show(a)