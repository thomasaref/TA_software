# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 16:46:27 2014

@author: thomasaref
"""
from atom.api import Float, Int, Enum, Callable, Unicode, Str

from GPIB import start_GPIB, GPIB_Instrument, GPIB_read
from numpy import linspace
from time import sleep


def start_Yoko(instr):
    start_GPIB(instr, address="", delay=0.05, timeout = 3, reset = False, do_selftest = False,
               lock = False, send_end = False, do_identify = False, clear=False)
    sleep(0.05)#yoko crashes if this pause isn't after the clear
    instr.header.send("Off")

def ramp(instr, ramp_end, ramp_steps, sleep_time):
    instr.receive("voltage")
    for v in linspace(instr.voltage, ramp_end, ramp_steps):
        instr.send("voltage", v) #float("{0:.4f}".format(v))
        sleep(sleep_time)


class Yoko(GPIB_Instrument):
    booter=Callable(start_Yoko)
    command=Unicode().tag(GPIB_writes="{command}")
    response=Str().tag(get_cmd=GPIB_read)

    voltage=Float(0.0).tag(label="Voltage", unit="V",
                        GPIB_writes="PRS;SA{:.4e};PRE;RU1",
                        GPIB_asks="OD")

    output=Enum("Off", "On").tag(mapping={'Off':0, 'On':1},
                                  GPIB_writes="O{0};E")

    header=Enum("On", "Off").tag(mapping={'Off':0, 'On':1},
                      GPIB_writes="H{0}")

    ramp=Callable(ramp).tag(label="Ramp")
    ramp_end=Float(0).tag(unit="V", label="Ramp End")
    sleep_time=Float(0.5).tag(sub=True, unit="s", label="Step Time")
    ramp_steps=Int(3).tag(label="Ramp Steps")

    def _default_label(self):
        return 'Yoko Voltage Source'

if __name__=="__main__":
    a=Yoko(address="GPIB0::10::INSTR")
    a.show()
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
