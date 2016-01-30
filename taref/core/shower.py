# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 12:38:54 2015

@author: thomasaref
"""
#from taref.core.log import log_debug
from taref.core.shower_backbone import get_view_window
from taref.core.agent import SubAgent


def shower(*agents, **kwargs):
    """a powerful showing function for any Atom object(s) specified in agents.
    Checks if object has a view_window property and otherwise uses a default view.
    also provides a show control of the objects which can be modified with kwargs"""
    from enaml import imports
    from enaml.qt.qt_application import QtApplication
    from enaml.application import Application


    start_it=False
    if Application.instance() is None:
        app = QtApplication()
        start_it=True

    with imports():
        from taref.core.agent_e import AutoAgentView
    for n, agent in enumerate(agents):
        view=get_view_window(agent, AutoAgentView(agent=agent), "window_{0}".format(n))
        view.show()

    if start_it:
        chief_cls=kwargs.pop("chief_cls", agents[0] if agents!=() else SubAgent)

        if hasattr(chief_cls, "interactive_window"):
            locals_dict={}
            from sys import _getframe
            frame=_getframe()
            try:
                locals_dict=(frame.f_back.f_locals)
            finally:
                del frame

            file_location=locals_dict.pop("__file__", "")
            with open(file_location) as f:
                showfile=f.read()
            locals_dict=dict(([(key, item) for key, item in locals_dict.items() if not key.startswith("_")]))

            view=chief_cls.interactive_window
            view.input_dict=locals_dict
            view.runtxt.text=showfile
            view.show()


        chief_view=getattr(chief_cls, "chief_window", SubAgent.chief_window)
        chief_view.chief_cls=chief_cls
        for key in kwargs:
            setattr(chief_view, key, kwargs[key])
        chief_view.show()

        app.start()


if __name__=="__main__":
    shower()