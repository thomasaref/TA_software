# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:38:47 2015

@author: thomasaref

A simple text editor driver allowing one to load, edit and save text files
"""

from Atom_Base import Base
from atom.api import Str, observe, Unicode, Typed, ContainerList, Int, Float, Bool, List, Atom, Coerced, Instance
from Atom_Read_File import Read_TXT
from Atom_Save_File import Save_TXT
#from LOG_functions import log_info, log_debug, make_log_file, log_warning

class Text_Editor(Base):
    main_file=Unicode("idt.jdf").tag(private=True)
    dir_path=Unicode("/Users/thomasaref/Dropbox/Current stuff/TA_software").tag(private=True)
    data=Str().tag(discard=True, log=False, width="max", label="")
    read_file=Typed(Read_TXT).tag(width="max")
    save_file=Typed(Save_TXT).tag(width='max')

    @observe('read_file.read_event')
    def obs_read_event(self, change):
        self.data="".join(self.read_file.data["data"])

    @observe('save_file.save_event')
    def obs_save_event(self, change):
        self.save_file.direct_save(self.data, write_mode='w')

    def _default_read_file(self):
        return Read_TXT(main_file=self.main_file, dir_path=self.dir_path)

    def _default_save_file(self):
        return Save_TXT(main_file=self.read_file.main_file, dir_path=self.read_file.dir_path)

    def data_list(self):
        return self.data.split("\n")

