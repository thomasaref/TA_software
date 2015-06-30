# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 13:56:33 2015

@author: thomasaref
"""
from LOG_functions import log_info, log_warning, make_log_file, log_debug#, SAVE_GROUP_NAME, SETUP_GROUP_NAME, log_debug
from atom.api import Atom, Bool, Typed, ContainerList, Callable, Dict, Float, Int, FloatRange, Range, Unicode, Str, List, Enum, Event, Instance
from Atom_Read_File import Read_File
from Atom_Save_File import Save_File, Save_HDF5
from Plotter import Plotter
from enaml import imports
from enaml.qt.qt_application import QtApplication
from enaml.application import deferred_call
from threading import Thread
import sys

def show(self):
    with imports():
            from e_Boss import AtomMain
    app = QtApplication()
    view = AtomMain(instr=self)
    view.show()
    app.start()

def show_boss(self, instr=None):
    with imports():
        from e_Boss import BossMain
    app = QtApplication()
    view = BossMain(myinstr=instr, boss=self)
    view.show()
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

def code_caller(self, code, **kwargs):
    result=code(self)
    try:
        deferred_call(setattr, self, 'busy', False)
        deferred_call(setattr, self, 'progress', 0)
        deferred_call(setattr, self, 'abort', False)
    except RuntimeError:
        self.busy=False
        self.progress=0
        self.abort=False
    return result
 
 
def do_it_if_needed(self, code, **kwargs):
    if not self.busy:
        self.busy = True
        thread = Thread(target=code_caller, args=(self, code), kwargs=kwargs)
        thread.start()
            
class Boss(Atom):
    """Overall control class that runs main code and handles files, saving and plotting"""
    name=Unicode("Base Control")
    run=Callable()
    read_file=Typed(Read_File)
    read_event=Event()
    save_file=Typed(Save_File)
    saving=Enum(False, True, "No buffer")
    save_factory=Callable(Save_HDF5)
    bases=ContainerList()
    visible_bases=ContainerList()
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
    
    show_bases=Bool(False)
 
    def _observe_abort(self, change):
        if self.abort==True:
            log_info("abort fired")
            
    def run_measurement(self):
        log_info("Master started")
        do_it_if_needed(self, self.run)
        log_info("Master finished")
    
    @property
    def plottables(self):
        tempdict=dict()
        for instr in self.bases:
            tempdict[instr.name]=instr.get_all_tags('plot', True, instr.plot_all, instr.all_params)
            if tempdict[instr.name]==[]:
                tempdict[instr.name]=instr.main_params #members().keys()
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
            if instr.get_type(name) in (Float, Int, Range, FloatRange, ContainerList, Unicode, Str):
                self.save_file.data_save(data=value, name=label, group_name=group_name)
            elif instr.get_type(name) in (List, Callable):
                pass
            elif instr.get_type(name) in (Bool, Enum):
                self.save_file.data_save(data=str(value), name=label, group_name=group_name)
            else:
                log_warning("No save format!")

    def show(self, base=None):
        try:
            show_boss(self, base)
        finally:
            if self.saving:
                self.save_file.flush_buffers()

    def read_data_distribute(self):
        log_warning("read_data_distribute not tested!")
        for key, item in self.read_file.data.iteritems():
            target=filter(lambda x: x.name==key, self.bases)
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

boss=Boss()
#master.save_file=Save_File()
#master.save_file.test_logger()
#print master.logger
if __name__=="__main__":
    print boss.bases
    print boss.plottables
    print boss.saving
    boss.show()
