# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:37:40 2015

@author: thomasaref
Just a handy stand alone for testing GPIB instruments
"""

from taref.instruments.GPIB import GPIB_Instrument, InstrumentError
from atom.api import Unicode, Float, Enum, Int, Bool
from taref.core.atom_extension import private_property, safe_log_debug
from time import sleep
from taref.core.log import log_debug

log_debug('hji')


def get_voltage(self):
    """gets voltage,  header on or off, and overload"""
    result=self.asker('OD')
    if result[0] not in ('N', 'E'):
        header=0
    else:
        header=1
    if result[0]=='E':
        overload=True
    else:
        overload=False
    mode='V'
    if header==1:
        mode=result[3]
        result=result[4:]
    voltage=float(result)
    pt_idx=result.find('.')
    if result[-4:-2]=='-3': 
        #V_range={'-33':2, '-34':3, '+02':4, '+03':5, '+04':6}[result[-4:-2]+str(result.find('.'))]
        if pt_idx==3:
            V_range=2 #10 mV
        else:
            V_range=3 #100 mV
    else:
        if pt_idx==2:
            V_range=4 #1 V 
        elif pt_idx==3:
            V_range=5 #10 V
        else:
            V_range=6 #30 V
    return dict(voltage=voltage, header=header, overload=overload, mode=mode, V_range=V_range)
    
def ramp(self, voltage, ramp_steps, sleep_time, ramp_time_left, ramp_rate):
    """ramps from current voltage to voltage"""
    target_V=voltage
    current_V=self.do_receive('voltage')
    if target_V>{'30 V' : 30, '10 V' : 10, '1 V' : 1, '100 mV' : 0.1, '10 mV' : 0.01}[self.V_range]:
        raise InstrumentError('Set voltage is outside range!')
    ramp_steps=int(abs(current_V-target_V)/(ramp_rate*sleep_time+1.0e-6))
    self.nosend_safeset(ramp_steps=ramp_steps)
    for v in self.lins(current_V, target_V, ramp_steps):
        self.writer('S{} E'.format(v)) #float("{0:.4f}".format(v))
        rtl=abs(target_V-v)/ramp_rate
        self.nosend_safeset(voltage=v, ramp_time_left=rtl)
        sleep(sleep_time)

def get_status(self):
    result=self.asker('OC')
    result=bin(int(result.split('=')[1]))
    #print result
    #print [i for i in result]
    return int(result[2])
    
            
class Yoko(GPIB_Instrument):
    """Yokogawa voltage source"""
    base_name='Yoko'

    @private_property
    def main_params(self):
        return ['output', 'voltage', 'V_range', 'current_limit', 'mode', 'header', 'overload']        

    def postboot(self):
        self.wait_loop(self.resp_delay)
        self.synchronize() 
    
    def synchronize(self):
        self.wait_loop(self.resp_delay)
        self.receive('voltage')
        self.wait_loop(self.resp_delay)
        self.receive('output')
        
    def _default_resp_delay(self):
        return 0.05
        
    identify = Unicode().tag(sub=True, get_str="OS", do=True, read_only=True, no_spacer=True)   
    
    output=Enum("Off", "On").tag(mapping={'Off':0, 'On':1}, set_str="O{output} E", get_cmd=get_status)       

    V_range=Enum('10 mV', '100 mV', '1 V', '10 V', '30 V').tag(mapping={'30 V' : 6, '10 V' : 5, '1 V' : 4,
                                                                        '100 mV' : 3, '10 mV' : 2},
                                                                        set_str='R{V_range} E', get_cmd=get_voltage)
    def _default_V_range(self):
        return '10 V'

    voltage=Float(0.0).tag(unit2='V', get_cmd=get_voltage, set_cmd=ramp, log=False)
    sleep_time=Float(0.1).tag(sub=True, unit2=" s", label="Step Time", low=0.0, high=0.5)
    ramp_steps=Int(100).tag(sub=True, label="Ramp Steps", read_only=True)
    ramp_rate=Float(0.03).tag(desc='voltage ramp rate per second', sub=True, low=0.0, high=1.0)
    ramp_time_left=Float(0.0).tag(desc='estimated time before voltage ramp is complete', sub=True, read_only=True, log=False)

    header=Enum('On', "Off").tag(mapping={'Off':0, 'On':1}, set_str="H{header}", get_cmd=get_voltage)
    overload=Bool(False).tag(read_only=True, get_cmd=get_voltage)
    mode=Enum('Voltage').tag(mapping={'Voltage' : 'V'}, get_cmd=get_voltage)
    
    current_limit=Int(120).tag(low=5, high=120, desc='current limit in mA', set_str='LA{current_limit}')
    
    #current mode
    #voltage_limit=Int(30).tag(low=1, high=30, set_str='LV{voltage_limit}')
    


if __name__=="__main__":
    from taref.plotter.fig_format import Plotter
    a=Yoko(address='GPIB0::1::INSTR')
    #b=Yoko(address='GPIB0::1::INSTR')
    from time import time
    from numpy import append
    #b=Plotter()
    #b.line_plot("voltage", [a.voltage])

    from atom.api import Atom, Typed, observe, List
    class Watch(Atom):
        yok=Typed(Yoko)
        plot=Typed(Plotter, ())
        #tstart=Float(time())
        xdata=List()
        ydata=List()
        #def _default_plot(self):
         #       return self.plot.line_plot('voltage', [self.tstart], [yok.voltage])

        @observe("yok.voltage")
        def update_plot(self, change):
            if change["type"]=="create":
                self.plot.line_plot('voltage', [0], [self.yok.voltage])
            elif change["type"]=="update":
                xdata=self.plot.plot_dict['voltage'].clt.get_xdata()
                xdata=append(xdata, len(xdata))
                self.plot.plot_dict['voltage'].clt.set_xdata(xdata)
                ydata=self.plot.plot_dict['voltage'].clt.get_ydata()
                ydata=append(ydata, self.yok.voltage)
                self.plot.plot_dict['voltage'].clt.set_ydata(ydata)
                self.plot.draw()

    a.boot()
    b=Watch(yok=a)
    
    a.show()
