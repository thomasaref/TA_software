# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 13:56:33 2015

@author: thomasaref
"""
from LOG_functions import log_info, log_warning, SAVE_GROUP_NAME, SETUP_GROUP_NAME, log_debug
from atom.api import Atom, Bool, Typed, ContainerList, Callable, Dict, Float, Int, FloatRange, Range, Unicode, Str, List, Enum
from Atom_Read_File import Read_File
from Atom_Save_File import Save_File, Save_HDF5
from Atom_Plotter import Plotter
import enaml
from enaml.qt.qt_application import QtApplication

class Master(Atom):
    """Overall control class that runs main code and handles files, saving and plotting"""
    run=Callable()
    read_file=Typed(Read_File, ())
    save_file=Typed(Save_File)
    saving=Enum(False, True, "No buffer")
    save_factory=Callable(Save_HDF5)
    instruments=ContainerList()
    plot=Typed(Plotter, ())
    plot_list=ContainerList()
    plottables=Dict()

    def run_measurement(self):
        log_info("Master started")
        self.run()
        log_info("Master finished")

    def _default_plottables(self):
        tempdict=dict()
        for instr in self.instruments:
            #tempdict[instr.name]=[]
            tempdict[instr.name]=instr.get_all_tags('plot', True, instr.plot_all, instr.all_params)
            #for key in instr.members().keys():
            #    if instr.get_tag(key, 'plot', instr.plot_all):
            #        tempdict[instr.name].append(key)
            if tempdict[instr.name]==[]:
                tempdict[instr.name]=instr.members().keys()
        return tempdict

#    def _observe_save_file(self, change):
#        if change['type']=='create':
#            if not self.save_file.buffer_save:
#                self.saving=True

    def _observe_saving(self, change):
        if change['type']!='create':
            if self.saving==True:
                self.full_save(self.run)
            elif self.saving==False:
                self.save_file.buffer_save=True

    def _default_save_file(self):
        if self.saving==True:
            savefile=self.save_factory(buffer_save=False)
            savefile.full_save(self.run)
            return savefile
        else:
            return self.save_factory(buffer_save=True)

    def draw_plot(self):
       pass

    def full_save(self):
        self.save_file.full_save(self.run)

    def data_save(self, instr, name, value):
        if not instr.get_tag(name, 'discard', False) and self.saving!="No buffer":
            if instr.get_tag(name, 'save', False):
                group_name=SAVE_GROUP_NAME
            else:
                group_name=SETUP_GROUP_NAME
            label=instr.get_tag(name, 'label', name)
            if instr.get_type(name) in (Float, Int, Range, FloatRange, ContainerList, Unicode, Str):
                self.save_file.data_save(data=value, name=label, group_name=group_name)
            elif instr.get_type(name) in (List, Callable):
                pass
            elif instr.get_type(name) in (Bool, Enum):
                self.save_file.data_save(data=str(value), name=label, group_name=group_name)
            else:
                log_warning("No save format!")

    def show(self):
        with enaml.imports():
            from enaml_Boss import MasterMain
        try:
            app = QtApplication()
            view = MasterMain(boss=self)
            view.show()
            app.start()
        finally:
            if self.saving:
                self.save_file.flush_buffers()

master=Master()
#master.save_file=Save_File()
#master.save_file.test_logger()
#print master.logger
if __name__=="__main__":
    print master.instruments
    print master.plottables
    print master.saving
    #master.show()
