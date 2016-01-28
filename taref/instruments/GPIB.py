# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:35:45 2014

@author: thomasaref
"""
from taref.instruments.instrument import Instrument, InstrumentError, booter, closer
from taref.core.log import log_debug
from taref.core.atom_extension import tag_Callable, get_tag, set_tag
from atom.api import Typed, Callable, Unicode, Bool, Float
#import visa
from taref.instruments.fakevisa import fakevisa as visa



#class GPIB_Callable(tag_Callable):
#    default_kwargs=dict(log_message='GPIB RAN: {0} {1}: "+GPIB_string))

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
    GPIB_ask.log_message="GPIB ASK: {0} {1}: "+GPIB_string
    #GPIB_ask.GPIB_string=GPIB_string
    return GPIB_ask

def GPIB_write_it(GPIB_string, name):
    """returns custom GPIB_write with GPIB_string encoded in GPIB_log object"""
    def GPIB_write(instr, **kwargs):
        instr.session.write(GPIB_string.format(**kwargs))
    GPIB_write.log_message="GPIB ASK: {0} {1}: "+GPIB_string
    #func.run_params.append(name)
    #func.GPIB_string=GPIB_string
    return GPIB_write

class GPIB_Instrument(Instrument):
    """Extends Instrument definition to GPIB Instruments"""
    #session=Typed(visa.Instrument).tag(private=True, desc="visa session of the instrument")
    base_name="GPIB_Instrument"

    @booter
    def start_GPIB(self, address, delay, timeout, reset, selftest, lock, send_end, identify, clear):
        if address=="":
            raise InstrumentError("{0}: GPIB instruments need addresses.".format(object.name))
        self.address=address
        self.session=visa.instrument(address)
        #self.session = visa.instrument(self.address, lock = lock, timeout = timeout, send_end=send_end, values_format = visa.single) #values_format=visa.single | visa.big_endian)
        if get_tag(self, "clear", "do", False):
            self.clear()
        if get_tag(self, "reset", "do", False):
            self.reset()
        if get_tag(self, "selftest", "do", False):
            self.selftest()
        if get_tag(self, "identify", "do", False):
            self.receive('identify')#    object.update_log("GPIB instrument initialized at address {0}".format(object.address))

    address=Unicode("GPIB0::22::INSTR").tag(sub=True, label = "GPIB Address")
    delay=Float(0).tag(sub=True, unit=" s", desc="delay between GPIB commands")
    timeout=Float(5).tag(sub=True, unit=" s", desc="timeout")

    @tag_Callable(sub=True)
    def reset(self):
        """send special GPIB command *RST"""
        GPIB_write(self, "*RST")
    #GPIB_reset.GPIB_string="*RST"

    lock = Bool(False).tag(sub=True)
    send_end = Bool(True).tag(sub=True)

    @tag_Callable(sub=True)
    def clear(self):
        """calls visa GPIB clear"""
        self.session.clear()
    #clear=Callable(GPIB_clear).tag(value=True)

    identify = Unicode().tag(sub=True, GPIB_asks="*IDN?", do=True, read_only=True)

    @tag_Callable(sub=True)
    def selftest(self):
        """perform selftest specified by special GPIB command *TST?"""
        tst=GPIB_ask(self, "*TST?")
        if int(tst):
            raise InstrumentError("Instrument {0} did not pass the selftest. CODE: {1}".format(self.name, tst))
    #GPIB_selftest.GPIB_string="*TST?"

    @closer
    def stop_GPIB(self):
        """default GPIB stop is visa close"""
        self.session.close()

    def extra_setup(self, param, typer):
        super(GPIB_Instrument, self).extra_setup(param, typer)
        GPIB_string=get_tag(self, param, 'GPIB_writes')
        if GPIB_string!=None:
            set_tag(self, param, set_cmd=GPIB_write_it(GPIB_string, param))
        GPIB_string=get_tag(self, param, 'GPIB_asks')
        if GPIB_string!=None:
            set_tag(self, param, get_cmd=GPIB_ask_it(GPIB_string))

if __name__=="__main__":
    t=GPIB_Instrument()
    t.boot(reset=True)
    t.show(t)
