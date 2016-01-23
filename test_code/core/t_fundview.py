# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 19:53:12 2016

@author: thomasaref
"""

def show(a):
    from enaml import imports
    from enaml.qt.qt_application import QtApplication
    app = QtApplication()
    with imports():
        from t_FundView_e import Main
    view=Main(vmodel=a)
    view.show()
    app.start()

from atom.api import Atom, Bool, Int, Typed, ContainerList, Coerced, Enum, cached_property

class subtest(Atom):
    view="field"
    tb=Bool()
    ti=Int().tag(label="MY INT")
    def _observe_tb(self, change):
        print change

    def _observe_ti(self, change):
        print change

class Test(Atom):
    tt=Typed(subtest, ())
    tc=Coerced(int)
    tb=Bool()
    ti=Int().tag(unit_factor=10, show_value=True, unit="dog", spec="sinbox")
    tl=ContainerList(default=[0,True,3,5,6,True, False, False, 3, 4, 5, 6]).tag(no_spacer=True)
    te=Enum("tc","ti").tag(spec="attribute")
    
    @cached_property
    def te_mapping(self):
        return {"tc":self.tc, "ti":self.ti}
    def _observe_tc(self, change):
        print change

    def _observe_tb(self, change):
        print change

    def _observe_ti(self, change):
        print change

t=Test()

show(t)