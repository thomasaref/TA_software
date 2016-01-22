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
    view=Main(instr=a)
    view.show()
    app.start()

from atom.api import Atom, Bool, Int, Typed, ContainerList
class subtest(Atom):
    tb=Bool()
    ti=Int().tag(label="MY INT")
    def _observe_tb(self, change):
        print change

    def _observe_ti(self, change):
        print change

class Test(Atom):
    tt=Typed(subtest, ())
    tb=Bool()
    ti=Int().tag(unit_factor=10, show_value=True, unit="dog", spec="spinbox")
    tl=ContainerList(default=[1,2,3])

    def _observe_tl(self, change):
        print change

    def _observe_tb(self, change):
        print change

    def _observe_ti(self, change):
        print change

t=Test()

show(t)