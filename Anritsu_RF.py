# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 06:16:35 2014

@author: thomasaref
"""

#from traits.api import Array, Int, CFloat, String, Enum, Range, HasTraits, Bool, List, Instance, Event, on_trait_change, Button, CBool
#from traitsui.api import View, Item, VGroup, HGroup, Group, TextEditor
#from chaco.api import Plot, ArrayPlotData
#from enable.component_editor import ComponentEditor
from numpy import linspace, sin
from threading import Thread
import numpy as np
#import os
#import shutil
#from reasonable_data import Dataset, DataXY
from GPIB import GPIB_Instrument, start_GPIB
from atom.api import Enum, Float, Bool, Int

def start_Anritsu(instr, address):
    start_GPIB(instr, address)
    instr.hw_write("LO0;")
    instr.output = 'Off'
    instr.hw_set_output()
    instr.power = -30

def set_leveling(instr, leveling):
    if leveling:
        instr.hw_write("IL1;")
    else:
        instr.hw_write("LV0;")

class AnritsuRFPulser(GPIB_Instrument):
    output = Enum('Off', 'On').tag(mapping={"On": 1, "Off":0}, GPIB_writes="RF{output}")
    freq = Float().tag(label = 'Anritsu frequency', unit='Hz',
                 GPIB_writes="F1 {freq} HZ;")
    power = Float(label = 'Anritsu power',unit='dBm', GPIB_writes="LOG; PU0; L1 {power} DM;")
    voltage = Float( label = 'Anritsu voltage',unit='V', GPIB_writes="LIN; L1 {voltage} VT;")
    phase = Int().tag(label = 'Anritsu phase',unit='deg', GPIB_writes="PSO {phase} DG")
    leveling = Bool(True).tag(set_cmd=set_leveling)
    pulsing = Enum('Off', 'Internal', 'External')
    pulse_time = Float(scalar_input = True, label = 'Anritsu pulse time',unit='s')
    pulse_rate = Float(scalar_input=True, label='Anritsu pulse rate', unit='Hz')
    trigger_edge = Enum('Rising', 'Falling')

    @on_trait_change('pulsing, pulse_time, pulse_rate, trigger_edge')
    def hw_set_pulsing(self):
        mode = self.pulsing
        if mode == 'Off':
            self.hw_write("P0;")
        elif mode == 'Internal':
            self.hw_write("PC4;")
            self.hw_write("W1 %.0d NS;"%(1e9*self.pulse_time))
            self.hw_write("PMD1")
            self.hw_write("PTG1")
            self.hw_write("PR %f HZ"%(self.pulse_rate))
            self.hw_write("IP")
        elif mode == 'External':
            self.hw_write("PC4;")
            self.hw_write("W1 %.0d NS;"%(1e9*self.pulse_time))
            self.hw_write("PMD1")
            self.hw_write("PTG4")
            if self.trigger_edge == 'Rising':
                self.hw_write("PTR")
            elif self.trigger_edge == 'Falling':
                self.hw_write("PTF")
            self.hw_write("IP")

if __name__ == '__main__':
    a = AnritsuRFPulser("GPIB::8")