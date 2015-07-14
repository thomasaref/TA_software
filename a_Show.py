# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 20:42:21 2015

@author: thomasaref
"""

from enaml.qt.qt_application import QtApplication
#from atom.api import Atom
from enaml import imports

#from a_Backbone import get_attr

#from LOG_functions import log_info, log_warning, make_log_file, log_debug#, SAVE_GROUP_NAME, SETUP_GROUP_NAME, log_debug
#from atom.api import Atom, Bool, Typed, ContainerList, Callable, Dict, Float, Int, FloatRange, Range, Unicode, Str, List, Enum, Event, Instance
#from Atom_Read_File import Read_File
#from Atom_Save_File import Save_File, Save_HDF5
#from Plotter import Plotter

def show_alone(agent):
    app = QtApplication()
    view=agent.view
    view.show()
    app.start()

def show(*agents):
    app = QtApplication()
    for n, a in enumerate(agents):
        if hasattr(a, "view"):
            view=a.view
        else:
            with imports():
                from e_Show import defaultView
            view=defaultView(agent=a)
        if hasattr(a, "name"):
            #view.title=a.name
            view.name=a.name
        else:
            view.name="agent_{0}".format(n)
        view.show()
    with imports():
        from e_Show import showView
    view=showView(title="ShowControl", name="show_control")
    view.show()
    app.start()

if __name__=="__main__":
    from atom.api import Atom, Unicode

    class test(Atom):
        """example test class with view defined"""
        a=Unicode("blah")

        @property
        def view(self):
            with imports():
                from e_Show import Main
            return Main(test=self)

    class test2(Atom):
        """example test class without view defined"""
        a=Unicode("bob")

    a=test()
    #show(a)
    b=test2()
    c=test2()
    show(a,b, c)

