# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 12:42:53 2016

@author: thomasaref
"""

from taref.core.api import Agent, tag_property#, log_debug
from taref.filer.read_file import Read_HDF5
from atom.api import Float, Typed, Unicode, Callable
from taref.filer.filer import Folder
from taref.filer.save_file import Save_TXT

class Lyzer(Agent):
    base_name="lyzer"
    fridge_atten=Float(60)
    fridge_gain=Float(45)

    @tag_property()
    def net_loss(self):
        return self.fridge_gain-self.fridge_atten+self.rt_gain-self.rt_atten


    rd_hdf=Typed(Read_HDF5)
    save_folder=Typed(Folder)

    save_file=Typed(Save_TXT)
    save_code=Typed(Save_TXT)

    read_data=Callable().tag(sub=True)


    def _default_save_folder(self):
        return Folder(base_dir="/Users/thomasaref/Dropbox/Current stuff/test_data/tex_processed", main_dir="overall")

    def _default_save_file(self):
        return Save_TXT(folder=self.save_folder, file_name="file_names", file_suffix=".txt", fixed_mode=True, write_mode="a")

    def _default_save_code(self):
        return Save_TXT(folder=self.save_file.folder, file_name=self.save_file.file_name+"_code", file_suffix=".py", fixed_mode=True)

    def save_plots(self, pl_list):
        names="\n".join([pl.fig_name for pl in pl_list])
        #self.save_file.file_name=self.name+"_file_names"
        self.save_file.save(names, write_mode="w", flush_buffer=True)
        for pl in pl_list:
            pl.savefig(self.save_folder.dir_path_d, pl.fig_name)

    rt_atten=Float(40)
    rt_gain=Float(23*2)

    offset=Float(-0.035)
    flux_factor=Float(0.2925)

    def _default_offset(self):
        return self.qdt.offset

    def _default_flux_factor(self):
        return self.qdt.flux_factor

    comment=Unicode().tag(read_only=True, spec="multiline")

