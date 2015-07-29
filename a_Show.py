# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 20:42:21 2015

@author: thomasaref
"""

from enaml.qt.qt_application import QtApplication
from atom.api import Atom, Unicode, Bool, List, Typed
from enaml import imports

#from a_Backbone import get_attr

#from LOG_functions import log_info, log_warning, make_log_file, log_debug#, SAVE_GROUP_NAME, SETUP_GROUP_NAME, log_debug
#from atom.api import Atom, Bool, Typed, ContainerList, Callable, Dict, Float, Int, FloatRange, Range, Unicode, Str, List, Enum, Event, Instance
#from Atom_Read_File import Read_File
#from Atom_Save_File import Save_File, Save_HDF5
#from Plotter import Plotter

#def show_alone(agent):
#    app = QtApplication()
#    view=agent.view
#    view.show()
#    app.start()

class Chief(Atom):
    save_file=Unicode()
    name=Unicode()
    show_all=Bool(False)
    plots=List(default=["a", "b"])
    log_str=Unicode("blarg")
    
    def _observe_log_str(self, change):
        print change

chief=Chief()
 
#def get_attr(obj, name, default_value):
#    if hasattr(obj, name):
#        return getattr(obj, name)
#    return default_value
#    
#def get_name(agent, default_name="agent_", n=0):
#    if hasattr(a, "name"):
#        return a.name
#    return default_name.format(n)

def show(*agents):
    app = QtApplication()
    with imports():
        from e_Show import defaultView, showView, basicView#, LogWindow
    loc_chief=None
    for n, a in enumerate(agents):
        if hasattr(a, "view_window"):
            view=a.view_window
        else:
            view=defaultView(agent=a)
        if hasattr(a, "name"):
            view.name=a.name
        else:
            view.name="agent_{0}".format(n)
        if hasattr(a, "chief"):
            loc_chief=a.chief
        view.title=view.name
        view.show()
        if loc_chief is not None:
            if chief.show_all or n==0:
                view.visible=True
    if loc_chief is None:
        view=basicView(title="Show Control", name="show_control")
    else:
        if hasattr(loc_chief, "view_window"):
            view=loc_chief.view_window
        else:
            view=showView(title="ShowControl", name="show_control", chief=loc_chief)
        #view.logw=LogWindow()#log_str=chief.log_str)
        #view.logw.show()

    view.show()

    app.start()
if __name__=="__main__":
    from atom.api import Atom, Unicode

    class test(Atom):
        """example test class with view defined"""
        a=Unicode("blah")
        name=Unicode("testy")

        @property
        def chief(self):
            return chief
            
        @property
        def view(self):
            return "field"
            
        @property
        def view_window(self):
            with imports():
                from e_UserTemps import Main
            return Main(test=self)

    class test2(Atom):
        """example test class without view defined"""
        a=Unicode("bob")
        b=Typed(test, ())
        @property
        def initial_size(self):
            return (300,300)
            

    a=test()
    #show(a)
    b=test2()
    c=test2()
    show(a, b, c)


#
