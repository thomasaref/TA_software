# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 10:37:40 2015

@author: thomasaref
"""

from Atom_GPIB import GPIB_Instrument, GPIB_read
from atom.api import Unicode, Str

class GPIB_tester(GPIB_Instrument):
    """A useful GPIB tester for random instruments. Input command strings in commands and receive strings in response"""
    command=Unicode().tag(full_interface=True, GPIB_writes="{command}")
    response=Str().tag(get_cmd=GPIB_read)

if __name__=="__main__":
    a=GPIB_tester(name='GPIB tester', address="GPIB0::20::INSTR")
    a.show()