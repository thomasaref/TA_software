# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 19:42:13 2014

@author: thomasaref
"""
from atom.api import Bool, Callable, cached_property
from enaml import imports
from enaml.qt.qt_application import QtApplication
from taref.core.chief import Chief
from taref.core.log import log_info, make_log_file#, log_warning
from taref.core.backbone import private_property


class InstrumentChief(Chief):
    """Extends Chief to accomodate instruments, booting, closing, autosaves data, and adds a prepare and finish functions."""

    def _default_saving(self):
        return False #True

    @private_property
    def view_window2(self):
        pass

    @private_property
    def view2(self):
        return "Instrument"

    def show2(self):
        with imports():
            from enaml_Instrument import InstrMain
        try:
            app = QtApplication()
            view = InstrMain(boss=self)
            view.show()
            app.start()
        finally:
            self.close_all()
            if self.saving:
                self.save_file.flush_buffers()

    def close_all(self):
        for instr in self.agents:
            if instr.status=='Active':
                instr.close()

    def boot_all(self):
        for instr in self.agents:
            if instr.status=='Closed':
                instr.boot()

    def run_measurement(self):
        log_info("Measurement started")
        for func in self.full_run_func_list:
            func()
        log_info("Measurement finished")

    def make_boss(self, base_dir="C:\\Users\\Speedy\\Documents\\Thomas\\TA_test", divider="\\",
                  log_name="record", file_name="meas", setup_g_name="SetUp", save_g_name="Measurements"):
        self.BASE_DIR=base_dir #"/Users/thomasaref/Dropbox/Current stuff/TA_software"
        self.DIVIDER=divider #"/"
        self.LOG_NAME=log_name #"record"
        self.FILE_NAME=file_name #"meas"
        self.SETUP_GROUP_NAME=setup_g_name #"SetUp"
        self.SAVE_GROUP_NAME=save_g_name #"Measurements"
        #make_log_file(log_path=self.BASE_DIR+self.DIVIDER+self.LOG_NAME+".log", display=self.display)  #default log file


instrument_chief=InstrumentChief() #singleton creation of boss. imported to other modules so there is only one boss.
if __name__=="__main2__":
    instrument_chief.show()