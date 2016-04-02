# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:37:40 2015

@author: thomasaref
Just a handy stand alone for testing GPIB instruments
"""

from taref.instruments.GPIB import GPIB_Instrument
from atom.api import Unicode, Float, Enum


class GPIB_tester(GPIB_Instrument):
    """A useful GPIB tester for random instruments. Input command strings in command and receive strings in response"""
    function=Unicode().tag(get_str='SENSE:FUNCTION?')
    data=Float().tag(get_str='SENSE:DATA?')
    
    funct=Enum('DC Voltage', 'Frequency', '4 Probe Resistance').tag(set_str="SENSE:FUNC {funct}",
                                                                    get_str="SENSE:FUNC?",
                                                                     mapping={'DC Voltage' : '"VOLT:DC"\n',
                                                                              'Frequency' : '"FREQ"\n',
                                                                              '4 Probe Resistance' : '"FRES"\n'})
    GPIB_Instrument.access_key.tag(do=True)
#    command=Unicode().tag(full_interface=True, GPIB_writes="{command}")
#    response=Str().tag(get_cmd=GPIB_read)

if __name__=="__main__":
    a=GPIB_tester(name='GPIB tester', address='GPIB0::16::INSTR')
    a.boot()
    print a.access_key
    print type(a.access_key)
    print dir(a.access_key)
    print a.resource_manager
    print type(a.resource_manager)
    print dir(a.resource_manager)
    print a.session
    print type(a.session)
    print dir(a.session)
    print a.session.session
    #b=a.resource_manager.open_resource('GPIB0::16::INSTR')
    #b.lock(requested_key=a.access_key)
    #print b.ask('*IDN?')
    #print b.lock_state
    #b.unlock()
    #print b.lock_state
    #a.unlock()
    
    
    a.show()
    #[attr for attr in a.visa_attributes_classes if 'RM_SESSION' in attr.visa_name]
