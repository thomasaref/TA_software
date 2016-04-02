# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:37:40 2015

@author: thomasaref
Just a handy stand alone for testing GPIB instruments
"""

from taref.instruments.GPIB import GPIB_Instrument
from atom.api import Unicode, Float, Enum, Int, Bool
from taref.core.atom_extension import set_tag, get_tag, safe_setattr, tag_Callable
print GPIB_Instrument.identify.metadata
from time import sleep
#b=GPIB_Instrument()
#print b.get_member('identify').metadata

class GPIB_tester(GPIB_Instrument):
    """A useful GPIB tester for random instruments. Input command strings in command and receive strings in response"""
    def __init__(self, **kwargs):
        super(GPIB_tester, self).__init__(**kwargs)
        #set_tag(self, "identify", do=False)
    
#    def postboot(self):
#        """postboot turns off header. yoko crashes if no pause"""
#        sleep(self.resp_delay)
#        if get_tag(self, "header", "do", False):
#            self.header.send()
#     
    #status =OC       
    def _default_resp_delay(self):
        return 0.05
        
    identify = Unicode().tag(sub=True, get_str="OS", do=True, read_only=True, no_spacer=True)   
    
    output=Enum("Off", "On").tag(mapping={'Off':0, 'On':1}, set_str="O{output} E")       
    V_range=Enum('10 mV', '100 mV', '1 V', '10 V', '30 V').tag(mapping={'30 V' : 6,
                                                                        '10 V' : 5,
                                                                        '1 V' : 4,
                                                                        '100 mV' : 3,
                                                                        '10 mV' : 2}, set_str='R{V_range} E')
    def _default_V_range(self):
        return '10 V'
                                                                   
    header=Enum('On', "Off").tag(mapping={'Off':0, 'On':1}, set_str="H{header}", sub=True)
    
    def ramp(self, voltage, ramp_steps, sleep_time):
        current_V=self.get_voltage()
        for v in self.loop(current_V, self.voltage, ramp_steps):
            self.writer('S{} E'.format(v)) #float("{0:.4f}".format(v))
            sleep(sleep_time)
    sleep_time=Float(0.1).tag(sub=True, unit=" s", label="Step Time")
    ramp_steps=Int(100).tag(sub=True, label="Ramp Steps")

    #_nostep_voltage=Float(0.0).tag(private=True)
    
    @tag_Callable()
    def get_voltage(self, header):
        result=self.asker('OD')
        with self.nosend_context('header'):
            if result[0] not in ('N', 'E'):
                safe_setattr(self, 'header', 'Off')
            else:
                safe_setattr(self, 'header', 'On')
            print result[0]
            if result[0]=='E':
                safe_setattr(self, 'overload', True)
            else:
                safe_setattr(self, 'overload', False)
        #with self.nosend_context('voltage'):
        if self.header=='On':
            print result[1:3]
            return float(result[4:])
        else:
            return float(result)

    voltage=Float(0.0).tag(unit2='V', get_cmd=get_voltage, set_cmd=ramp)
                
    #voltage set_st='S{voltage} E'
    overload=Bool(False).tag(read_only=True) #Enum('Normal', 'Overload').tag(mapping={})
    current_limit=Int(120).tag(low=5, high=120, desc='current limit in mA', set_str='LA{current_limit}')
    
    #current mode
    #voltage_limit=Int(30).tag(low=1, high=30, set_str='LV{voltage_limit}')
    
#print GPIB_Instrument.identify.metadata
#print b.get_member('identify').metadata

if __name__=="__main__":
    a=GPIB_tester(name='GPIB tester', address='GPIB0::1::INSTR')
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
