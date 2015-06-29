# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 23:15:33 2015

@author: thomasaref
"""

from atom.api import Atom, Float, Coerced
from enaml import imports
from enaml.qt.qt_application import QtApplication
from Atom_Base import get_type

def show(self):
        with imports():
            from e_Boss import AtomMain
        app = QtApplication()
        view = AtomMain(instr=self)
        view.show()
        app.start()

class Test2(object):
    d=4
    def _show(self):
        show(self)

    def __setattr__(self, name, value):
        """extends __setattr__ to allow logging and data saving and automatic sending if tag send_now is true.
        This is preferable to observing since it is called everytime the parameter value is set, not just when it changes."""
        #if name in self.all_params:
        #    value=self.coercer(name, value)
        super(Test2, self).__setattr__(name, value)
        print "set {name} to {value}".format(name=name, value=value)
        #if name in self.all_params:
        #    self.set_log( name, value)

    main_params=['d']
class Test(Atom):
    b=Float().tag(unit="bbb", label="blahhafd", low=0.0)
    c=Coerced(int)#.tag()
    d=4

    def _observe_c(self, change):
        print change
    #@property
    #def main_params(self):
    #    return ['c']

    def show(self, abase=None):
        with imports():
            from e_Boss import AtomMain
        #try:
        app = QtApplication()
        view = AtomMain(instr=self)
        view.show()
        app.start()
        #finally:
            #if self.saving:
             #   self.save_file.flush_buffers()

a=Test2()
a.d=9
a._show()
print a.d