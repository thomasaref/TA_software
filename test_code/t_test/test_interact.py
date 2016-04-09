# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 19:30:11 2016

@author: thomasaref
"""

from taref.test.interact import Interact
from atom.api import Atom, Float, Typed
from enaml.qt.qt_application import QtApplication

class Test(Atom):
    a=Float()

    def _observe_a(self, change):
        print change

    interact=Interact()#starter="start", stopper="stop")

    #def _default_b(self):
    #    print "creating inter"
    #    return Interact(starter="start", stopper="stop")
    def astart(self):
        self.interact.make_input_code()
    def stop(self):
        pass

b=Test()
a=Test()

a.astart()
print b.interact.input_code
#a.stop()
#a..exec_code()
#print b.b.file_reader.preamble, b.b.file_reader.postamble

#print b.b.file_reader.local_name
#print b.b.locals_dict

app=QtApplication()
view=b.interact.interact_window
view.show()
app.start()