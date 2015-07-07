# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:45:30 2015

@author: thomasaref
"""

from enaml import imports
from enaml.qt.qt_application import QtApplication

def show(obj):
    with imports():
            from e_Electron import AtomMain
    app = QtApplication()
    view = AtomMain(elect=obj)
    view.show()
    app.start()