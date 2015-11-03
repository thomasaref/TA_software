# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:45:30 2015

@author: thomasaref
"""

from atom.api import Atom

from taref.core.log import log_info, log_warning, make_log_file, log_debug#, SAVE_GROUP_NAME, SETUP_GROUP_NAME, log_debug
from atom.api import Atom, Bool, Typed, ContainerList, Callable, Dict, Float, Int, FloatRange, Range, Unicode, Str, List, Enum, Event, Instance
from Atom_Read_File import Read_File
from Atom_Save_File import Save_File, Save_HDF5
from Plotter import Plotter
from SHOW_functions import show

#import sys
from taref.core.backbone import do_it_if_needed



class Chief(Atom):
    """Overall control class that runs main code and handles files, saving and plotting"""
    name=Unicode("Chief")
    run=Callable()
    read_file=Typed(Read_File)
    read_event=Event()
    save_file=Typed(Save_File)
    saving=Enum(False, True, "No buffer")
    save_factory=Callable(Save_HDF5)
    agents=ContainerList()
    plot=Typed(Plotter, ())
    plots=ContainerList()

    BASE_DIR=Unicode("/Users/thomasaref/Dropbox/Current stuff/TA_software")
    DIVIDER=Unicode("/")
    LOG_NAME=Unicode("record")
    FILE_NAME=Unicode("meas")
    SETUP_GROUP_NAME=Unicode("SetUp")
    SAVE_GROUP_NAME=Unicode("Measurements")

    #display=Typed(StreamCatch, ()).tag(desc="a stream catch for the log window")

    busy = Bool(False).tag(desc="indicates function is running")
    abort = Bool(False).tag(desc="abort for use by agent functions")
    progress = Int(0).tag(desc="for progress bar")

    show_all=Bool(False).tag(desc="shows all agents on start up")

    def _observe_abort(self, change):
        if self.abort==True:
            log_info("abort fired")

    def run_measurement(self):
        log_info("Master started")
        do_it_if_needed(self.run)
        log_info("Master finished")

    @property
    def plottables(self):
        tempdict=dict()
        for instr in self.agents:
            tempdict[instr.name]=instr.get_all_tags('plot', True, False, instr.all_params)
            if tempdict[instr.name]==[]:
                tempdict[instr.name]=instr.main_params 
        return tempdict

    def _observe_saving(self, change):
        if change['type']!='create':
            if self.saving==True:
                self.full_save()
            elif self.saving==False:
                self.save_file.buffer_save=True

    def _default_read_file(self):
        return Read_File()

    def full_read(self):
        self.read_file.read()
        self.read_data_distribute()

    def _default_save_file(self):
        if self.saving==True:
            savefile=self.save_factory(buffer_save=False, base_dir=self.BASE_DIR, divider=self.DIVIDER,
                                       data_buffer={self.SAVE_GROUP_NAME:{}, self.SETUP_GROUP_NAME:{}})
            savefile.full_save(obj=self.run, old_log_path=self.BASE_DIR+self.DIVIDER+self.LOG_NAME)
            return savefile
        else:
            return self.save_factory(buffer_save=True, base_dir=self.BASE_DIR, divider=self.DIVIDER,
                                     data_buffer={self.SAVE_GROUP_NAME:{}, self.SETUP_GROUP_NAME:{}})

    def draw_plot(self):
       pass

    @property
    def old_log_path(self):
        return self.BASE_DIR+self.DIVIDER+self.LOG_NAME

    def full_save(self):
        self.save_file.full_save(obj=self.run, old_log_path=self.old_log_path)

    def data_save(self, instr, name, value):
        if not instr.get_tag(name, 'discard', False) and self.saving!="No buffer":
            if instr.get_tag(name, 'save', False):
                group_name=self.SAVE_GROUP_NAME
            else:
                group_name=self.SETUP_GROUP_NAME
            label=instr.get_tag(name, 'label', name)
            if instr.get_type(name) in (Float, Int, Range, FloatRange, ContainerList, Unicode, Str, float, int, basestring, list, List):
                self.save_file.data_save(data=value, name=label, group_name=group_name)
            elif instr.get_type(name) in (Callable,):
                pass
            elif instr.get_type(name) in (Bool, Enum, bool):
                self.save_file.data_save(data=str(value), name=label, group_name=group_name)
            else:
                log_warning("No save format!")

    def show(self):
        try:
            show(*self.agents)
        finally:
            if self.saving==True:
                self.save_file.flush_buffers()

    def read_data_distribute(self):
        log_warning("read_data_distribute not tested!")
        for key, item in self.read_file.data.iteritems():
            target=filter(lambda x: x.name==key, self.agents)
            if target!=[]:
                for subkey, subitem in item.iteritems():
                    if subkey in target[0].all_params:
                        setattr(target[0], subkey, subitem)
                    else:
                        log_warning("target base does not have target param!")
            else:
                log_warning("target base not found!")

    def make_chief(self, base_dir="/Users/thomasaref/Dropbox/Current stuff/TA_software", divider="/",
                  log_name="record", file_name="meas", setup_g_name="SetUp", save_g_name="Measurements", save_log=False):
        self.BASE_DIR=base_dir #"/Users/thomasaref/Dropbox/Current stuff/TA_software"
        self.DIVIDER=divider #"/"
        self.LOG_NAME=log_name #"record"
        self.FILE_NAME=file_name #"meas"
        self.SETUP_GROUP_NAME=setup_g_name #"SetUp"
        self.SAVE_GROUP_NAME=save_g_name #"Measurements"
        if save_log==True:
            make_log_file(log_path=self.BASE_DIR+self.DIVIDER+self.LOG_NAME+".log", display=self.display)  #default log file

chief=Chief()

if __name__=="__main__":
    print chief.agents
    print chief.plottables
    print chief.saving
    chief.show()
