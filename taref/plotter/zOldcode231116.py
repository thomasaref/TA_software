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


#def defaulter(self, name, kwargs):
#    if name in kwargs:
#        return kwargs.pop(name)
#    default=self.get_member(name).default_value_mode
#    if default[0]==1:
#        return default[1]
#    elif default[0]==8:
#        return getattr(self, default[1])()
#    elif default[0]==5:
#        return default[1]()
#
#def name_generator(self, name, indict, suffix="__{0}"):
#    if name in indict:
#        name+=suffix.format(len(indict.keys()))
#    return name


    #def _default_plot_name(self):
    #    return self.plot_type

    #def _observe_plot_name(self, change):
    #    check_initialized(self, change)

        #if plot_name in plotter.plot_dict:
        #    if self.remove:
        #        self.remove_collection()
        #    else:

        #if plot_name is None:
        #    plot_name=self.plot_type
        #if agent_name in Operative.agent_dict:
        #    agent_name="{name}__{num}".format(name=agent_name, num=len(Operative.agent_dict))
        #kwargs["name"]=agent_name
        #Operative.agent_dict[agent_name]=self
        #        plot_name+="__{0}".format(len(self.plotter.plot_dict.keys()))
        #self.plot_name=plot_name
        #set_tag(self, "plot_name", initialized=False)
        #if self.plot_name=="":
        #    self.plot_name=self.plot_type
        #if self.plot_name in self.plotter.plot_dict:
        #    if self.remove:
        #        self.remove_collection()
        #    else:
        #        self.plot_name+="__{0}".format(len(self.plotter.plot_dict.keys()))
