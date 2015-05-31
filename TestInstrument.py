# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 06:04:52 2014

@author: thomasaref

Tests and demonstrates various functionality of Instruments defined by Atom_Base
"""

from Atom_Instrument import Instrument
from atom.api import Float, Int, Unicode, Bool, Enum, ContainerList, List, Callable, Range, FloatRange
from LOG_functions import log_info
def get_inttry(instr, booltry, voltage):
    """get_cmds first parameter must be the instrument itself. get_cmds must return a value.
       Sub parameters in the instrument are matched to names defined in the function i.e. voltage corresponds to instr.voltage"""
    print "You called get_inttry on instrument {name} with sub parameters booltry={booltry} and voltage={voltage}. This function returns 3.2".format(
            name=instr.name, booltry=booltry, voltage=voltage)
    return 3.2

def set_inttry(instr, inttry, voltage):
    """the first parameter of set_cmds must be the intrument itself.
    The second parameter must be the value getting set i.e. since we are setting inttry the second parameter must be inttry"""
    print "You called set_inttry on instrument {name} with sub parameter voltage={voltage}".format(name=instr.name, voltage=voltage)

def set_strtry(instr, strtry):
    print "You sent {0} to strtry".format(strtry)

def testenum(instr, enumtry, booltry):
    print enumtry, booltry

def get_enum(instr):
    return 2

def testgrp(instr):
    return {'booltry':True, 'inttry':3}

def testlist(instr):
    return [1,2,3,4,5,6]

def calltest(instr, inttry):
    print "call test ran"

def boot_func1(instr, voltage):
    """define a boot func outside the main code. first parameter should always be the instrument itself"""
    print "You called boot_func1 on instrument {name} with sub parameter voltage={voltage}".format(name=instr.name, voltage=voltage)

def external_func(instr, voltage): #functions should have the instrument as thier first parameter
    print "You ran external_func"
    for a in range(0,1,3):
        print a, voltage

class Test_Instrument(Instrument):
    view=Enum("Auto", "Field").tag(private=True) #this demonstrates how to overwrite the view option to allow use of custom enaml layouts
    #plot_all=Bool(False)
    v2=Range(0,10,1)
    v3=FloatRange(0.1, 10.0, 3.0).tag(precision=1000)
    booter=Callable(boot_func1).tag(private=True) #overwriting booter to allow new boot function
    voltage=Float().tag(unit="V", label="Voltage", sub=True) #demonstrates a Float sub parameter with label and unit
    inttry=Int().tag(set_cmd=set_inttry, get_cmd=get_inttry)
    strtry=Unicode().tag(set_cmd=set_strtry)
    booltry=Bool().tag(sub=True)
    enumtry=Enum('a', 'b').tag(mapping={'a':1, 'b':2}, set_cmd=testenum, get_cmd=get_enum) #Enums must specifiy a mapping in tag. The parameters of Enum must match the keys in mapping giving the ordering of keys with the first value being the default
    listtry=ContainerList(default=[0, 2,3,4,5,6,7,8,9]).tag(get_cmd=testlist) #ContainerLists are used to hold data arrays. A default must be given.
    grptry=List(default=['booltry', 'inttry']).tag(get_cmd=testgrp) #Lists hold the names of items united by a common set_cmd or get_cmd

    def internal_func(self, inttry): #functions can also be declared internally though they should still be declared a Callable (or decorated with log)
       print "you ran internal_func with sub paramater inttry={inttry}".format(inttry=inttry) #type(self).voltage.metadata['get_cmd'](3,4) #print "yowza"

    calltry=Callable(internal_func) #this shows how to define an internal function as a Callable (so it appears in the GUI)

    calltry1=Callable(external_func) #allows functions that neither set or get values to be defined. This shows how to do it for a function declared outside the class

if __name__=="__main__":

    a=Test_Instrument(name="Tom") #instruments should be given names
    b=Test_Instrument(name="Bob", view="Field") #shows how to call a custom view of an instrument
#    a.boss.buffer_save=True
    #log_info('what')
    a.boss.saving=False #'No buffer'

    #def temp_run():
    #    pass
    #a.boss.run=temp_run
    a.boot() #functions can be called via code or via the GUI
    a.send('inttry', 3)
    a.calltry(a, inttry=4)
    a.voltage='9' #automatic coercing changes a string to a float
    a.inttry=4
    a.inttry=4 #even though value is not changed, setting of attribute is still logged and associated set_cmd is fired
    a.strtry='blah'
    a.booltry=True
    a.enumtry='b'
    a.send('enumtry')
    a.listtry=[1,2,3]
    a.listtry.append(2)
    a.listtry=[1,2,3]
    a.calltry1(a, voltage=8)
#    a.send_now=True
#    a.send_now=False
#    a.inttry=4
#    a.receive('enumtry')
##    a.receive('voltage')
    a.receive('listtry')
    #a.boss.saving=True
    a.show() #used to show the instrument in a GUI
    #a.boss.save_hdf5.flush_buffers()
