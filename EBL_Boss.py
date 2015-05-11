# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 18:23:12 2015

@author: thomasaref
"""

from Atom_Boss import Boss
from Atom_Save_File import Save_DXF
from LOG_functions import log_info
from enaml import imports
from enaml.qt.qt_application import QtApplication

class EBL_Boss(Boss):
    def _default_save_factory(self):
        return Save_DXF

    def run_measurement(self):
        log_info("EBL Master started")
        self.run()
        log_info("EBL Master finished")

    def show(self):
        with imports():
            from enaml_Boss import MasterMain
        try:
            app = QtApplication()
            view = MasterMain(boss=self)
            view.show()
            app.start()
        finally:
            if self.saving:
                self.save_file.flush_buffers()

ebl_boss=EBL_Boss()