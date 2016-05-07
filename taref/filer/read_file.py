# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:21:06 2015

@author: thomasaref
"""

from taref.core.log import log_info#, log_debug
from taref.filer.filer import Filer
from atom.api import Dict, Event, Typed, Unicode, cached_property, Atom, observe, Bool, List
from taref.core.api import tag_callable
from taref.core.universal import read_text
#from DXF_functions import readdxflayer
from taref.filer.HDF5_functions import read_hdf5, group
from numpy import loadtxt


from enaml import imports
with imports():
    from taref.filer.read_file_e import ReadFileExt, ReadFileMain

class Read_File(Filer):
    read_event=Event()

    def _default_show_details(self):
        return False

    def _default_show_simple(self):
        return False

    @tag_callable(button_label="Read")
    def file_action(self):
        self.read()

    @cached_property
    def data_str(self):
        return unicode(self.data)

    def log_read(self):
        log_info("read not implemented! file not read: {0}".format(self.file_path))

    def browse_clicked(self):
        super(Read_File, self).browse_clicked()
        self.read()

    def read(self):
        self.log_read()
        self.get_member("data_str").reset(self)
        self.read_event()
        return self.data

    @cached_property
    def view(self):
        return ReadFileExt

    @cached_property
    def view_window(self):
        """stand alone for showing filer."""
        return ReadFileMain(agent=self)



class Read_HDF5(Read_File):
    """extends Read_File for HDF5 format files"""
    data=Typed(group)

    def _default_file_suffix(self):
        return ".hdf5"

    def log_read(self):
        log_info("Read data from hdf5 file: {0}".format(self.file_path))

    def read(self):
        self.data=read_hdf5(self.file_path)
        return super(Read_HDF5, self).read()

class Read_NP(Read_File):
    """Reads data using numpy's loadtxt"""
    data=Dict()

    def _default_file_suffiz(self):
        return ".txt"

    def log_read(self):
        log_info("Read data from numpy text file: {0}".format(self.file_path))

    def read(self):
        self.data={"data":loadtxt(self.file_path)}
        return super(Read_HDF5, self).read()

class Read_DXF(Read_File):
    def _default_file_suffix(self):
        return ".dxf"


#    """reads a layer of an autocad dxf file"""
#    def read(self, layer="Al"):
#        """reads dxf file in and places polygons in polylist"""
#        polylist=readdxflayer(self.file_path, inlayer=layer)
#        self.data["data"]=polylist
#        return self.data

class Read_TXT(Read_File):
    """extends Read_File for text files"""
    data=List()

    def _default_file_suffix(self):
        return ".txt"

    def log_read(self):
        log_info("Read data from text file: {0}".format(self.file_path))

    def read(self):
        self.data=read_text(self.file_path)
        return super(Read_TXT, self).read()

    @cached_property
    def data_str(self):
        return "\n".join(self.data)

if __name__=="__main__":
    class Read_Extension_Test(Read_File):
        """a test class for extending Read_File"""
        data=Dict()

        def read(self):
            self.data={"file_path": self.file_path}
            return super(Read_Extension_Test, self).read()

    class Read_Test(Atom):
        """a test class for having Read file as a child"""
        read_file=Typed(Read_Extension_Test).tag(label="").tag(no_spacer=True)
        data=Unicode().tag(discard=True, log=False, no_spacer=True, label="", spec="multiline")

        def _default_read_file(self):
            return Read_File(show_details=False, show_simple=True)

        @observe("read_file.read_event")
        def change_data(self, change):
            print change
            self.data=self.read_file.data_str

    a=Read_Extension_Test()
    b=Read_Test(read_file=a)
    print a.read()
    #print a.data
    #print a.data_str
    #a=Read_TXT(file_path="/Users/thomasaref/Dropbox/Current stuff/TA_software/idt2.jdf")
    #a=Read_HDF5()
    from taref.core.shower import shower
    shower(a, b)