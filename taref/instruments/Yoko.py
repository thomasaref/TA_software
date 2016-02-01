# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 16:46:27 2014

@author: thomasaref
"""
from atom.api import Float, Int, Enum, Unicode
from taref.core.atom_extension import tag_Callable, set_tag, get_tag
from taref.instruments.instrument import booter
from taref.instruments.GPIB import  GPIB_Instrument, GPIB_read, start_GPIB
from numpy import linspace
from time import sleep

class Yoko(GPIB_Instrument):
    base_name="Yoko"

    def _default_delay(self):
        return 0.05

    def _default_timeout(self):
        return 3

    def __init__(self, **kwargs):
        super(Yoko, self).__init__(**kwargs)
        set_tag(self, "identify", do=False)

    @booter
    def booter(self, address, delay, timeout, reset, selftest, lock, send_end, identify, clear, header):
        start_GPIB(self, address, delay, timeout, reset, selftest,
                   lock, send_end, identify, clear)
        sleep(0.05)#yoko crashes if this pause isn't after the clear
        if get_tag(self, "header", "do", False):
            self.header.send()


    voltage=Float(0.0).tag(label="Voltage", unit="V",
                        GPIB_writes="PRS;SA{:.4e};PRE;RU1",
                        GPIB_asks="OD")

    output=Enum("Off", "On").tag(mapping={'Off':0, 'On':1}, GPIB_writes="O{0};E")

    header=Enum("Off", "On").tag(mapping={'Off':0, 'On':1}, GPIB_writes="H{0}")

    @tag_Callable(label="Ramp")
    def ramp(self, ramp_end, ramp_steps, sleep_time):
        self.receive("voltage")
        for v in linspace(self.voltage, ramp_end, ramp_steps):
            self.send("voltage", v) #float("{0:.4f}".format(v))
            sleep(sleep_time)
    ramp_end=Float(0).tag(sub=True, unit=" V", label="Ramp End")
    sleep_time=Float(0.5).tag(sub=True, unit=" s", label="Step Time")
    ramp_steps=Int(3).tag(sub=True, label="Ramp Steps")



if __name__=="__main__":
    a=Yoko(address="GPIB0::10::INSTR")
    print get_tag(a, "voltage", "set_cmd")
    from taref.core.shower import shower
    shower(a)
    #a.ramp_steps=3
    #a.ramp()
    #a.voltage.send(0.0)
    #a.send("voltage=0.2")
    #time.sleep(0.05)
    #Simple ramp example
    #a.receive("voltage")
    #time.sleep(0.05)
    #for v in np.linspace(a.voltage.value, 1, 10):
    #        a.voltage.send(v) #float("{0:.4f}".format(v))
    #        time.sleep(0.5)

    #a.ramp=True

    #a.session.write("O1;E")
    #a.write("O1;E")
    #print a.ask("OD")
