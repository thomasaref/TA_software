# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 11:23:43 2015

@author: thomasaref
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 11:22:03 2014

@author: thomasaref
"""
from atom.api import Atom, Unicode, Enum, observe
from time import strftime, localtime
#from LOG_functions import log_info, log_warning
from enaml import imports

class Filer(Atom):
    """A generic filing system where a primary directory path and file path are composed of a base directory,
    main directory, divider and main file. The main directory defaults to 'S' followed by the year month day
    and time of saving. A function of do_save (to be implemented by children classes that save) is also present."""

    base_dir=Unicode("/Users/thomasaref/Dropbox/Current stuff/TA_software")
    main_dir=Unicode()
    main_file=Unicode()
    file_name=Unicode("meas")
    divider=Unicode("/")
    log_name=Unicode("record")

    file_path=Unicode()
    dir_path=Unicode()
    log_path=Unicode()

    file_type=Enum("HDF5", "text", "dxf", "text data")

    comment=Unicode()
    log_str=Unicode("not implemented")

    def _default_main_file(self):
        if self.file_type=="HDF5":
            return self.file_name+".hdf5"
        elif self.file_type in ("text", "text data"):
            return self.file_name+".txt"
        elif self.file_type=="dxf":
            return self.file_name+".dxf"
        else:
            return self.file_name

    def _default_main_dir(self):
        return strftime("S%Y_%m_%d_%H%M%S", localtime())

    def _default_file_path(self):
        return self.dir_path+self.divider+self.main_file

    def _default_log_path(self):
        return self.dir_path+self.divider+self.log_name+".log"

    @observe( "dir_path", "log_name", 'divider')
    def log_path_changed(self, change):
        if change['type']!='create':
            self.log_path=self.dir_path+self.divider+self.log_name+".log"

    @observe( "dir_path", "main_file", 'divider')
    def file_path_changed(self, change):
        if change['type']!='create':
            self.file_path=self.dir_path+self.divider+self.main_file

    quality=Enum("discard", "less interesting", "interesting")

    @observe( "base_dir", "main_dir", 'divider', 'quality')
    def dir_path_changed(self, change):
        if change['type']!='create':
            self.dir_path=self.base_dir+self.divider+self.quality+self.divider+self.main_dir

    def _default_dir_path(self):
        return self.base_dir+self.divider+self.quality+self.divider+self.main_dir

    @property
    def view_window(self):
        with imports():
            from e_Filer import FilerMain
        return FilerMain(filer=self)
        
if __name__=="__main__":
    from a_Show import show
    f=Filer(file_type="text")
    show(f)
