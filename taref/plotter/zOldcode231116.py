# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:02:51 2016

@author: thomasaref
"""

#def process_kwargs(self, kwargs):
#    """Goes through all_params and sets the attribute if it is included in kwargs, also popping it out of kwargs.
#    if the param is tagged with "former", the kwarg is added back using the value of the param. Returns the processed kwargs"""
#    for arg in get_all_params(self): #get_all_tags(self, "former"):
#        if arg in kwargs:
#            setattr(self, arg, kwargs[arg])
#        val=kwargs.pop(arg, None)
#        key=get_tag(self, arg, "former", False)
#        if key is not False:
#            if val is None:
#                val=getattr(self, arg)
#            kwargs[key]=val
#    return kwargs