# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 11:23:43 2015

@author: thomasaref
"""

from atom.api import Atom, Unicode, Enum, observe, cached_property
from time import strftime, localtime
from taref.core.log import log_debug
from enaml import imports
#from taref.core.backbone import private_property

class Filer(Atom):
    """A generic filing system where a primary directory path and file path are composed of a base directory,
    main directory, divider and main file. The main directory defaults to 'S' followed by the year month day
    and time of saving. A function of do_save (to be implemented by children classes that save) is also present."""

    base_dir=Unicode("/Users/thomasaref/Dropbox/Current stuff/TA_software")
    main_dir=Unicode()
    file_name=Unicode("meas")
    file_suffix=Unicode("txt")
    divider=Unicode("/")
    log_name=Unicode("record")
    comment=Unicode()

    quality=Enum("discard", "less interesting", "interesting", "")

    @cached_property
    def log_suffix(self):
        return "log"

    @cached_property
    def main_file(self):
        return self.file_name+"."+self.file_suffix

    @main_file.setter
    def set_main_file(self, mf_str):
        self.file_name, dot, self.file_suffix=mf_str.rpartition(".")

    def _default_main_dir(self):
        return strftime("S%Y_%m_%d_%H%M%S", localtime())

    @cached_property
    def file_path(self):
        return self.dir_path+self.divider+self.main_file

    @file_path.setter
    def set_file_path(self, fp_str):
        self.dir_path, div, file_name=fp_str.rpartition(self.divider)
        self.file_name, div, self.file_suffix=file_name.partition(".")

    @cached_property
    def log_path(self):
        return self.dir_path+self.divider+self.log_name+"."+self.log_suffix

    @observe("file_name", "file_suffix", "divider", "quality", 
         "base_dir", "quality", "main_dir", "log_name", "log_suffix")
    def update_properties(self, change):
        log_debug(change)
        #if change['type']=='update':
        for name in ("dir_path", "main_file", "file_path", "log_path"):
                self.get_member(name).reset(self)

    @cached_property
    def dir_path(self):
        if self.quality=="":
            return self.base_dir+self.divider+self.main_dir
        return self.base_dir+self.divider+self.quality+self.divider+self.main_dir

    @dir_path.setter
    def set_dir_path(self, dp_str):
        dir_str, div, self.main_dir=dp_str.rpartition(self.divider)
        log_debug(dir_str.rpartition(self.divider))

        base_dir, div, quality=dir_str.rpartition(self.divider)
        if quality in self.get_member("quality").items:
            self.base_dir=base_dir
            self.quality=quality
        else:
            self.base_dir=dir_str
            self.quality=""
            
    @cached_property
    def view_window(self):
        with imports():
            from taref.core.filer_e import FilerMain
        return FilerMain(filer=self)

if __name__=="__main__":
    from taref.core.shower import show
    f=Filer()
    show(f)
