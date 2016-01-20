# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:38:54 2015

@author: thomasaref
"""

from enaml import imports
from enaml.qt.qt_application import QtApplication
from taref.core.log import log_debug

def get_view(obj, default_view, default_name):
    view=getattr(obj, "view_window", default_view)
    view.name=getattr(obj, "name", default_name)
    if view.title=="":
        view.title=view.name
    return view

def shower(*agents):

    """a powerful showing function for any Atom object(s). Checks if object has a view_window property and otherwise uses a default.
    also provides a show control of the objects"""
    app = QtApplication()
    with imports():
        from taref.core.chief_e import agentView, basicView #, chiefView
    for n, agent in enumerate(agents):
        view=get_view(agent, agentView(agent=agent), "window_{0}".format(n))
        view.show()
#        if hasattr(agent, "agent_dict"):
#            for other_agent in agent.agent_dict.values():
#                if other_agent not in agents:
#                    view=get_view(other_agent, agentView(agent=other_agent), "unnamed_agent")
#                    view.initialize()
    view=basicView(title="Show Control", name="show_control", chief_cls=type(agents[0]))
    view.show()
    app.start()


def shower2(*agents):
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