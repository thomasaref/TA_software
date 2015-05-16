# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:21:06 2015

@author: thomasaref
"""

from Atom_Filer import Filer
from LOG_functions import log_warning, log_info
from atom.api import Dict, Event
from enaml import imports
from enaml.qt.qt_application import QtApplication
#from Atom_Save_File import Save_HDF5, Save_NP, Save_TXT, Save_DXF

class Read_File(Filer):
    data=Dict()
    read_event=Event()   

    def read(self):
        self.do_read()
        self.read_event()
        return self.data

    def do_read(self):
        log_warning("do_read not implemented!")

 #   def _observe_read_event(self, change):
 #       print change
    def show(self):
        """stand alone for showing filer."""
#        if save_file==None:
#            if self.file_type=='HDF5':
#                save_file=Save_HDF5(base_dir=self.base_dir, main_dir=self.main_dir, main_file=self.main_file, divider=self.divider, 
#                                    log_file=self.log_file, file_path=self.file_path, dir_path=self.dir_path, log_path=self.log_path)
#            elif self.file_type=='dxf':
#                save_file=Save_DXF(base_dir=self.base_dir, main_dir=self.main_dir, main_file=self.main_file, divider=self.divider, 
#                                    log_file=self.log_file, file_path=self.file_path, dir_path=self.dir_path, log_path=self.log_path)
#            elif self.file_type=='text data':
#                save_file=Save_NP(base_dir=self.base_dir, main_dir=self.main_dir, main_file=self.main_file, divider=self.divider, 
#                                    log_file=self.log_file, file_path=self.file_path, dir_path=self.dir_path, log_path=self.log_path)
#            else:
#                save_file=Save_TXT(base_dir=self.base_dir, main_dir=self.main_dir, main_file=self.main_file, divider=self.divider, 
#                                    log_file=self.log_file, file_path=self.file_path, dir_path=self.dir_path, log_path=self.log_path)
        with imports():
            from enaml_Filer import ReadBoxMain
        app = QtApplication()
        view = ReadBoxMain(read_file=self)
        view.show()
        app.start()

#from DXF_functions import readdxflayer
from HDF5_functions import read_hdf5
from numpy import loadtxt

class Read_HDF5(Read_File):
    """extends Read_File for HDF5 format files"""
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
        
if __name__=="__main__":
    #a=Read_File()
    #a.read()
    a=Read_HDF5()
    a.show()