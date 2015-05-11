# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 19:42:13 2014

@author: thomasaref
"""
from atom.api import Bool, Callable
from enaml import imports
from enaml.qt.qt_application import QtApplication
from Atom_Boss import Boss
from LOG_functions import log_info#, log_warning

def pass_factory():
    def do_nothing():
        pass
    return do_nothing

class InstrumentBoss(Boss):
    """Extends Master to accomodate instruments, booting, closing, autosaves data, and adds a prepare and finish functions."""
    prepare=Callable(factory=pass_factory)
    finish=Callable(factory=pass_factory)
    wants_abort=Bool(False) #not implemented

    #def _default_save_file(self):
    #    return Save_HDF5(buffer_save=False)

    def _default_saving(self):
        return True
        
    def show(self):
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
        for instr in self.bases:
            if instr.status=='Active':
                instr.close()

    def boot_all(self):
        for instr in self.bases:
            if instr.status=='Closed':
                instr.boot()

    def run_measurement(self):
        log_info("Measurement started")
        self.prepare()
        self.run()
        self.finish()
        log_info("Measurement finished")

instrumentboss=InstrumentBoss() #singleton creation of boss. imported to other modules so there is only one boss.
if __name__=="__main__":
    instrumentboss.saving=False
    instrumentboss.show()        