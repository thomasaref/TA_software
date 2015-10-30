# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:35:45 2014

@author: thomasaref
"""
from Atom_Instrument import Instrument, InstrumentError
from Atom_Base import log
from atom.api import Typed, Callable, Unicode, Bool, Float
import visa


class GPIB_log(log):
    """updates log decorator to include GPIB string in log message"""
    def update_log(self, instr, kwargs):
        instr.update_log('RAN: {instr} {name}: {GPIB_string} {kwargs}'.format(
             instr=instr.label, name=self.f.func_name, kwargs=kwargs, GPIB_string=self.GPIB_string))

def GPIB_read(instr):
    """calls visa GPIB read"""
    return instr.session.read()
        
def GPIB_ask(instr, GPIB_string, **kwargs):
    """calls visa GPIB ask using GPIB_string and kwargs"""
    return instr.session.ask(GPIB_string.format(**kwargs))

def GPIB_write(instr, GPIB_string, **kwargs):
    """calls visa GPIB write using GPIB_string and kwargs"""
    instr.session.write(GPIB_string.format(**kwargs))
    
def ask_for_values(instr, GPIB_string, **kwargs):
    """calls visa GPIB ask_for_values using GPIB_string and kwargs"""
    return instr.session.ask_for_values(GPIB_string.format(**kwargs))

def GPIB_ask_it(GPIB_string):
    """returns custom GPIB_ask with GPIB_string encoded in GPIB_log object"""
    def GPIB_ask(instr, **kwargs):
        return instr.session.ask(GPIB_string.format(**kwargs))
    func=GPIB_log(GPIB_ask)
    func.GPIB_string=GPIB_string
    return func
    
def GPIB_write_it(GPIB_string, name):
    """returns custom GPIB_write with GPIB_string encoded in GPIB_log object"""
    def GPIB_write(instr, **kwargs):
        instr.session.write(GPIB_string.format(**kwargs))
    func=GPIB_log(GPIB_write)
    func.run_params.append(name)
    func.GPIB_string=GPIB_string
    return func


def start_GPIB(instr, address="", delay=0, timeout = 5, do_reset = False,
               do_selftest = False, lock = False, send_end = True,
               do_identify = True, do_clear=False):
    if address=="":
        raise InstrumentError("{0}: GPIB instruments need addresses.".format(object.name))
    instr.address=address
    instr.session=visa.instrument(address)
    #self.session = visa.instrument(self.address, lock = lock, timeout = timeout, send_end=send_end, values_format = visa.single) #values_format=visa.single | visa.big_endian)
    if do_clear:
        instr.clear(instr)
    if do_reset:
        instr.send('reset')
    if do_selftest:
        instr.receive('selftest')
    if do_identify:
        instr.receive('identify')#    object.update_log("GPIB instrument initialized at address {0}".format(object.address))


def GPIB_clear(instr):
    """calls visa GPIB clear"""
    instr.session.clear()

@GPIB_log
def GPIB_reset(instr):
    """send special GPIB command *RST"""
    GPIB_write(instr, "*RST")
GPIB_reset.GPIB_string="*RST"

@GPIB_log
def GPIB_selftest(instr):
    """perform selftest specified by special GPIB command *TST?"""
    tst=GPIB_ask(instr, "*TST?")
    if int(tst):
        raise InstrumentError("Instrument {0} did not pass the selftest. CODE: {1}".format(instr.name, tst))
GPIB_selftest.GPIB_string="*TST?"

def stop_GPIB(instr):
    """default GPIB stop is visa close"""
    instr.session.close()

class GPIB_Instrument(Instrument):
    """Extends Instrument definition to GPIB Instruments"""
    address=Unicode("GPIB0::22::INSTR").tag(sub=True, label = "GPIB Address")
    session=Typed(visa.Instrument)#, desc="visa session of the instrument")

    booter=Callable(start_GPIB)
    delay=Float(0).tag(sub=True, unit="s", desc="delay between GPIB commands")
    timeout=Float(5).tag(sub=True, unit="s", desc="timeout")
    do_reset = Bool(False).tag(sub=True)
    reset=Callable(GPIB_reset)
    lock = Bool(False).tag(sub=True)
    send_end = Bool(True).tag(sub=True)
    do_clear = Bool(True).tag(sub=True)
    clear=Callable(GPIB_clear).tag(value=True)
    do_identify=Bool(False).tag(sub=True)
    identify = Unicode().tag(GPIB_asks="*IDN?")
    do_selftest=Bool(False).tag(sub=True)
    selftest = Callable(GPIB_selftest) #Unicode().tag(GPIB_asks="*TST?")

    closer=Callable(stop_GPIB)

    def __init__(self, **kwargs):
        """updates __init__ so paramters with tags GPIB_writes and GPIB_asks are updated to set_cmd=GPIB_write and get_cmd=GPIB_ask respectively"""
        super(GPIB_Instrument, self).__init__(**kwargs)
        for name in self.all_params:
            GPIB_string=self.get_tag(name, 'GPIB_writes')
            if GPIB_string!=None:
                self.set_tag(name, set_cmd=GPIB_write_it(GPIB_string, name))
            GPIB_string=self.get_tag(name, 'GPIB_asks')
            if GPIB_string!=None:
                self.set_tag(name, get_cmd=GPIB_ask_it(GPIB_string))
