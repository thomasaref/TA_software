# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 22:39:58 2016

@author: thomasaref
"""

def get_view(obj, default_view, default_name="NO_NAME"):
    view=getattr(obj, "view_window", default_view)
    view.name=getattr(obj, "name", default_name)
    if view.title=="":
        view.title=view.name
    return view
