# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 11:23:43 2015

@author: thomasaref
"""

#from taref.core.log import log_debug
from atom.api import Atom, Unicode, Enum, observe, cached_property, Bool, Typed
from time import strftime, localtime
from enaml import imports
from enaml.widgets.api import FileDialogEx
with imports():
    from taref.filer.filer_e import FilerExt, FilerMain, DirectoryExt, FolderMain

class Folder(Atom):
    """A generic directory system where a primary directory path is composed of a base directory, main directory,
    divider and quality (which can be optional). The main directory defaults to 'S' followed by the year month day and time of saving.
    show_details and show_simple give some control over the GUI display"""

    base_dir=Unicode("/Users/thomasaref/Dropbox/Current stuff/testDll")
    main_dir=Unicode()
    divider=Unicode("/")
    quality=Enum("discard", "less interesting", "interesting", "")
    show_details=Bool(True)
    show_simple=Bool(True)

    def _default_main_dir(self):
        return strftime("S%Y_%m_%d_%H%M%S", localtime())

    @observe("divider", "quality", "base_dir", "main_dir")
    def update_properties(self, change):
        for name in ("dir_path",):
            self.get_member(name).reset(self)

    @cached_property
    def dir_path(self):
        if self.quality=="":
            return self.base_dir+self.divider+self.main_dir
        return self.base_dir+self.divider+self.quality+self.divider+self.main_dir

    @dir_path.setter
    def set_dir_path(self, dp_str):
        dir_str, div, self.main_dir=dp_str.rpartition(self.divider)
        base_dir, div, quality=dir_str.rpartition(self.divider)
        if quality in self.get_member("quality").items:
            self.base_dir=base_dir
            self.quality=quality
        else:
            self.base_dir=dir_str
            self.quality=""

    @cached_property
    def view(self):
        return DirectoryExt

    @cached_property
    def view_window(self):
        return FolderMain(filer=self)

class Filer(Atom):
    """A generic filing system which extends Folder giving a file name and suffix from which a main_file (combining the two) and a full file_path is constructed"""
    folder=Typed(Folder)
    file_name=Unicode("meas")
    file_suffix=Unicode()
    show_data_str=Bool(False)

    def _default_folder(self):
        return Folder()

    #log_name=Unicode("record")
    #log_suffix=Unicode(".log")
    #comment=Unicode()

    @cached_property
    def main_file(self):
        return self.file_name+self.file_suffix

    @main_file.setter
    def set_main_file(self, mf_str):
        self.file_name, dot, file_suffix=mf_str.rpartition(".")
        self.file_suffix=dot+file_suffix

    @cached_property
    def file_path(self):
        return self.folder.dir_path+self.folder.divider+self.main_file

    @cached_property
    def nosuffix_file_path(self):
        return self.folder.dir_path+self.folder.divider+self.file_name

    @file_path.setter
    def set_file_path(self, fp_str):
        self.folder.dir_path, div, self.main_file=fp_str.rpartition(self.folder.divider)

    #@cached_property
    #def log_path(self):
    #    return self.dir_path+self.divider+self.log_name+self.log_suffix

    @observe("file_name", "file_suffix", "folder.dir_path")#, "log_name", "log_suffix")
    def update_properties(self, change):
        for name in ("main_file", "file_path", "nosuffix_file_path"):
            self.get_member(name).reset(self)

    def browse_clicked(self):
        path = FileDialogEx.get_open_file_name(current_path=self.file_path)
        if path:
            self.file_path = path

    @cached_property
    def view(self):
        return FilerExt

    @cached_property
    def view_window(self):
        return FilerMain(filer=self)

if __name__=="__main__":
    from taref.core.shower import shower
    a=Folder()
    f=Filer()
    from atom.api import Typed
    class Test(Atom):
        f=Typed(Filer).tag(no_spacer=True)
        a=Typed(Folder).tag(no_spacer=True)
    t=Test(f=f, a=a)
    shower(a, f, t)
