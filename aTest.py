# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 23:15:33 2015

@author: thomasaref
"""

from atom.api import Atom, Float, Coerced
from enaml import imports
from enaml.qt.qt_application import QtApplication

class Test(Atom):
    b=Float()
    c=Coerced(int)
    d=4
    
    @property
    def main_params(self):
        return ['c']
        
    def show(self, base=None):
        with imports():
            from enaml_Boss import AtomMain
        #try:
        app = QtApplication()
        view = AtomMain(instr=self)
        view.show()
        app.start()
        #finally:
            #if self.saving:
             #   self.save_file.flush_buffers()
        
a=Test()
a.show()