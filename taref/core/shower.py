# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:38:54 2015

@author: thomasaref
"""
#from taref.core.log import log_debug
from taref.core.atom_extension import get_view

def shower(*agents, **kwargs):
    """a powerful showing function for any Atom object(s) specified in agents.
    Checks if object has a view_window property and otherwise uses a default view.
    also provides a show control of the objects which can be modified with kwargs"""
    from enaml import imports
    from enaml.qt.qt_application import QtApplication
    app = QtApplication()
    with imports():
        from taref.core.agent_e import AutoAgentView, basicView #, chiefView
    for n, agent in enumerate(agents):
        view=get_view(agent, AutoAgentView(agent=agent), "window_{0}".format(n))
        view.show()
    chief_view=kwargs.pop("chief_view", basicView)
    kwargs["chief_cls"]=kwargs.get("chief_cls", agents[0])
    kwargs["title"]=kwargs.get("title", "Show Control")
    kwargs["name"]=kwargs.get("name", "show_control")
    view=chief_view(**kwargs)
    view.show()
    app.start()