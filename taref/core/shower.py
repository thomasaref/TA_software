# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:38:54 2015

@author: thomasaref
"""

from enaml import imports
from enaml.qt.qt_application import QtApplication
from taref.core.log import log_debug

def shower(*agents):
    """a powerful showing function for any Atom object(s). Checks if object has a view_window property and otherwise uses a default.
    also provides a show control of the objects"""
    app = QtApplication()
    with imports():
        from chief_e import agentView, chiefView, basicView
    for n, a in enumerate(agents):
        view=getattr(a, "view_window", agentView(agent=a))
        view.name=getattr(a, "name", "agent_{0}".format(n))
        loc_chief=getattr(a, "chief", None)
        view.title=view.name
        view.show()
        if loc_chief is not None:
            if not loc_chief.show_all and n!=0:
                view.hide()
    if loc_chief is None:
        view=basicView(title="Show Control", name="show_control")
    else:
        if hasattr(loc_chief, "view_log"):
            if loc_chief.view_log.visible:
                loc_chief.view_log.show()
        if hasattr(loc_chief, "view_window"):
            view=loc_chief.view_window
        else:
            view=chiefView(title="Show Control", name="show_control", chief=loc_chief)
    view.show()
    app.start()

def find_windows(a, tl=[]):
    for name in a.members():
        member=getattr(a, name)
        if hasattr(member, "view_window"):
            tl.append(name)
            print tl
            find_windows(member, tl)

    return tl

#self.plot.view_window.show()
#        view=self.jdf.view_window
#        view.show()
#        view.hide()