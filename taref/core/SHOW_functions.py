# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:38:54 2015

@author: thomasaref
"""

from enaml import imports
from enaml.qt.qt_application import QtApplication

def show(*agents):
    """a powerful showing function for any Atom object(s). Checks if object has a view_window property and otherwise uses a default.
    also provides a show control of the objects"""
    app = QtApplication()
    with imports():
        from e_Chief import agentView, chiefView, basicView#, LogWindow
    loc_chief=None
    for n, a in enumerate(agents):
        if hasattr(a, "view_window"):
            view=a.view_window
        else:
            view=agentView(agent=a)
        if hasattr(a, "name"):
            view.name=a.name
        else:
            view.name="agent_{0}".format(n)
        if hasattr(a, "chief"):
            loc_chief=a.chief
        view.title=view.name
        view.show()
        if loc_chief is not None:
            if loc_chief.show_all or n==0:
                view.visible=True
    if loc_chief is None:
        view=basicView(title="Show Control", name="show_control")
    else:
        if hasattr(loc_chief, "view_window"):
            view=loc_chief.view_window
        else:
            view=chiefView(title="ShowControl", name="show_control", chief=loc_chief)
    view.show()
    app.start()

