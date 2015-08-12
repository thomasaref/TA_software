# -*- coding: utf-8 -*-
"""
Created on Fri Aug  7 17:32:20 2015

@author: thomasaref
"""

from enaml import imports
from enaml.qt.qt_application import QtApplication
from atom.api import Atom, Bool, Int, Str, Coerced, Instance, Float, Unicode, Enum, Callable, Typed, Range, FloatRange, ContainerList, List
from LOG_functions import log_debug
from numpy import array, ndarray

def show(a):
    app = QtApplication()
    with imports():
        from e_FundTemps import Main
    view=Main(instr=a)
    view.show()
    app.start() 

class testChief(Atom):
    busy=Bool()
    abort=Bool()
    progress=Int()

testchief=testChief()

class subtest(Atom):
    st_int=Int()
    st_str=Str()
    
class test(Atom):
    #Ints can have units, show_value, unit_factor and low/high limits
    t_int=Int().tag(unit="um", show_value=True, unit_factor=20, low=0, high=5)
    #Ints can be shown as spin boxes or int fields
    t_int_intfield=Int().tag(unit="um", show_value=True, unit_factor=20, low=0, high=5, spec="intfield")
    #Coerced of basic types have same behavior as basic type, e.g. this coerced int acts like the Int above
    t_coerced_int=Coerced(int).tag(unit="um", show_value=True, unit_factor=20, low=0, high=5, spec="intfield")
    
    #ranges are represented with sliders
    t_range=Range(0, 5, 1)
    t_floatrange=FloatRange(0.0, 5.0, 1.0)
    #You can include other classes
    t_typed=Typed(subtest, ())
    t_instance=Instance(subtest, ())
    
    #lists
    t_list=List(default=[1.2, 1.3, 1.4])
    t_containerlist=ContainerList(default=[1.2, 1.3, 1.4]).tag(unit="um")
    
    #how to do a numpy array
    t_coerced_arr=Coerced(ndarray, coercer=array)#.tag(private=7)

    #Floats can have units, show_value, unit_factor and low/high limits
    t_float=Float().tag(unit="GHz", show_value=True, unit_factor=0.2, low=-1.0, high=1)
    #A Bool demostrating the label functionality
    t_bool=Bool().tag(label="MY BOOL")
    
    
    #Unicode Field display    
    t_unicode=Unicode("blah")
    
    #Unicode Multiline Field disply
    t_unicode_multiline=Unicode("blah").tag(spec="multiline")
    
    #unmapped Enum
    t_enum=Enum("one", "two", "three")

    #mapped Enum
    @property
    def t_enum_map_mapping(self):
        return dict(one=1, two=2, three=3)
    
    t_enum_map=Enum("one","two","three")

    #attribute mapped enum
    @property
    def t_enum_attr_mapping(self):
        return dict(t_int=self.t_int, t_float=self.t_float, t_bool=self.t_bool)

    t_enum_attr=Enum("t_int","t_float","t_bool").tag(map_type="attribute")


    #Note: extra run features (extra args, run lockout, abort) only function if chief is defined    
    @Callable
    def a(self):
        from time import sleep
        log_debug("a_called")
        for n in range(5):
            log_debug(n)
            if self.abort:
                break
            sleep(0.4)
        log_debug("a_endded")

    @property    
    def chief(self):
        return testchief
        
    @property    
    def busy(self):
        return testchief.busy
        
    @property    
    def abort(self):
        return testchief.abort

a=test()
a.t_coerced_arr=[0.1, 0.2]

show(a)
