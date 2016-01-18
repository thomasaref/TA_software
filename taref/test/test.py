# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:20:53 2016

@author: thomasaref
"""

from atom.api import Atom, Float, Unicode, Typed

class Test(Atom):
    a=Unicode()

    def _observe_a(self, change):
        print change

    @property
    def view(self):
        return "test"
        from enaml import imports
        with imports():
            from taref.test.test_e import TestCont
        return TestCont(test=self)

a=Test()

#from taref.core.log import log_debug
class Boss(Atom):
    agent=Typed(Test)

b=Boss()
b.agent=a

def shower(*agents):
    """a powerful showing function for any Atom object(s). Checks if object has a view_window property and otherwise uses a default.
    also provides a show control of the objects"""
    from enaml import imports
    from enaml.qt.qt_application import QtApplication
    app = QtApplication()
    with imports():
        from taref.test.test_e import Main#, LogWindow

    #loc_chief=None
    for n, a in enumerate(agents):
        #if hasattr(a, "view_window"):
        #    view=a.view_window
        #else:
        #    view=agentView(agent=a)
        #if hasattr(a, "name"):
        #    view.name=a.name
        #else:
        #    view.name="agent_{0}".format(n)
        #if hasattr(a, "chief"):
        #    loc_chief=a.chief
        #view.title=view.name
        view=Main(boss=b)
        view.show()
#        if loc_chief is not None:
#            if loc_chief.show_all or n==0:
#                view.visible=True
#    if loc_chief is None:
#        view=basicView(title="Show Control", name="show_control")
#    else:
#        if hasattr(loc_chief, "view_window"):
#            view=loc_chief.view_window
#        else:
#            view=chiefView(title="ShowControl", name="show_control", chief=loc_chief)
    #view.show()
    app.start()
shower(a)