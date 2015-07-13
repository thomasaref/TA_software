# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:45:30 2015

@author: thomasaref
"""

from enaml import imports
from enaml.qt.qt_application import QtApplication
from atom.api import Atom

from LOG_functions import log_info, log_warning, make_log_file, log_debug#, SAVE_GROUP_NAME, SETUP_GROUP_NAME, log_debug
from atom.api import Atom, Bool, Typed, ContainerList, Callable, Dict, Float, Int, FloatRange, Range, Unicode, Str, List, Enum, Event, Instance
from Atom_Read_File import Read_File
from Atom_Save_File import Save_File, Save_HDF5
from Plotter import Plotter


import sys
from a_Backbone import get_tag, get_type, get_all_tags, do_it_if_needed, get_attr, get_all_params, get_main_params, get_name
    
def chief_show(chief, agent):
    with imports():
            from e_Backbone import ChiefMain
    app = QtApplication()
    view = ChiefMain(boss=chief, agent=agent)
    view.show()
    app.start()

def show_alone(agent):
    app = QtApplication()
    view=agent.viewprop
    view.show()
    app.start()
    
def show_old( agent):
    with imports():
            from e_Backbone import AtomMain
    app = QtApplication()
    #view = AtomMain( agent=agent)
    #view.show()
    myview=agent.viewprop
    myview.title=get_attr(agent, "name", "boog")
    myview.show()
    app.start()
    
class StreamCatch(Atom):
    log_str=Unicode()

    def write(self,str):
        self.log_str=str+self.log_str

    def flush(self):
        pass

    def redirect_stdout(self, visible):
        if visible:
            sys.stdout=self
            sys.stderr=self
        else:
            sys.stdout=sys.__stdout__ #old_stdout
            sys.stderr=sys.__stderr__


            
class Chief(Atom):
    """Overall control class that runs main code and handles files, saving and plotting"""
    name=Unicode("Base Control")
    run=Callable()
    read_file=Typed(Read_File)
    read_event=Event()
    save_file=Typed(Save_File)
    saving=Enum(False, True, "No buffer")
    save_factory=Callable(Save_HDF5)
    agents=ContainerList()
    visible_agents=ContainerList()
    plot=Typed(Plotter, ())
    plots=ContainerList()
    BASE_DIR=Unicode("/Users/thomasaref/Dropbox/Current stuff/TA_software")
    DIVIDER=Unicode("/")
    LOG_NAME=Unicode("record")
    FILE_NAME=Unicode("meas")
    SETUP_GROUP_NAME=Unicode("SetUp")
    SAVE_GROUP_NAME=Unicode("Measurements")
    display=Typed(StreamCatch, ())

    busy = Bool(False)
    abort = Bool(False)
    progress = Int(0)
    
    show_agents=Bool(False)
 
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
            tempdict[get_name(instr)]=get_all_tags(instr, 'plot', True, get_attr(instr, "plot_all", False), get_all_params(instr))
            if tempdict[get_name(instr)]==[]:
                tempdict[get_name(instr)]=get_main_params(instr) #members().keys()
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
        if not get_tag(instr, name, 'discard', False) and self.saving!="No buffer":
            if get_tag(instr, name, 'save', False):
                group_name=self.SAVE_GROUP_NAME
            else:
                group_name=self.SETUP_GROUP_NAME
            label=get_tag(instr, name, 'label', name)
            if get_type(instr, name) in (Float, Int, Range, FloatRange, ContainerList, Unicode, Str, float, int, basestring, list, List):
                self.save_file.data_save(data=value, name=label, group_name=group_name)
            elif get_type(instr, name) in (Callable,):
                pass
            elif get_type(instr, name) in (Bool, Enum, bool):
                self.save_file.data_save(data=str(value), name=label, group_name=group_name)
            else:
                log_warning("No save format!")

    def show(self, agent=None):
        try:
            chief_show(self, agent)
        finally:
            if self.saving:
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

    def make_boss(self, base_dir="/Users/thomasaref/Dropbox/Current stuff/TA_software", divider="/",
                  log_name="record", file_name="meas", setup_g_name="SetUp", save_g_name="Measurements", save_log=False):
        self.BASE_DIR=base_dir #"/Users/thomasaref/Dropbox/Current stuff/TA_software"
        self.DIVIDER=divider #"/"
        self.LOG_NAME=log_name #"record"
        self.FILE_NAME=file_name #"meas"
        self.SETUP_GROUP_NAME=setup_g_name #"SetUp"
        self.SAVE_GROUP_NAME=save_g_name #"Measurements"
        if save_log==True:
            make_log_file(log_path=self.BASE_DIR+self.DIVIDER+self.LOG_NAME+".log", display=self.display)  #default log file

boss=Chief()

def show(agent):
    chief=boss
    boss.agents.append(agent)
    chief_show(chief, agent)

#master.save_file=Save_File()
#master.save_file.test_logger()
#print master.logger
if __name__=="__main__":
    print boss.agents
    print boss.plottables
    print boss.saving
    boss.show()
   