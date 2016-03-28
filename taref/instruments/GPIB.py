# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:35:45 2014

@author: thomasaref
"""
from taref.instruments.instrument import Instrument, InstrumentError, booter, closer
from taref.core.log import log_debug, log_info
from taref.core.atom_extension import tag_Callable, get_tag, set_tag, log_func, private_property
from atom.api import Unicode, Bool, Float, Typed
#import visa
from taref.instruments.fakevisa import fakevisa as visa
from time import sleep

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

def GPIB_ask_it(GPIB_string, name):
    """returns custom GPIB_ask with GPIB_string encoded in GPIB_log object"""
    def GPIB_ask(instr, **kwargs):
        return instr.session.ask(GPIB_string.format(**kwargs))
    GPIB_ask=log_func(GPIB_ask, name)
    GPIB_ask.log_message="GPIB ASK: {0} {1}: "+GPIB_string
    GPIB_ask.run_params.append(name)
    #GPIB_ask.GPIB_string=GPIB_string
    return GPIB_ask

def GPIB_write_it(GPIB_string, name):
    """returns custom GPIB_write with GPIB_string encoded in GPIB_log object"""
    def GPIB_write(instr, **kwargs):
        instr.session.write(GPIB_string.format(**kwargs))
    GPIB_write=log_func(GPIB_write, name)
    GPIB_write.log_message="GPIB WRITE: {0} {1}: "+GPIB_string
    GPIB_write.run_params.append(name)
    #func.GPIB_string=GPIB_string
    return GPIB_write

def start_GPIB(instr, address, delay, timeout, reset, selftest, lock, send_end, identify, clear):
    if address=="":
        raise InstrumentError("{0}: GPIB instruments need addresses.".format(instr.name))
    instr.address=address
    instr.session=visa.instrument(address)
    #self.session = visa.instrument(self.address, lock = lock, timeout = timeout, send_end=send_end, values_format = visa.single) #values_format=visa.single | visa.big_endian)
    if get_tag(instr, "clear", "do", False):
        instr.clear()
    if get_tag(instr, "reset", "do", False):
        instr.reset()
    if get_tag(instr, "selftest", "do", False):
        instr.selftest()
    if get_tag(instr, "identify", "do", False):
        instr.receive('identify')
    log_info("GPIB instrument {name} initialized at address {address}".format(name=instr.name, address=address))

class GPIB_Instrument(Instrument):
    """Extends Instrument definition to GPIB Instruments"""
    #session=Typed(visa.Instrument).tag(private=True, desc="visa session of the instrument")
    base_name="GPIB_Instrument"

    @tag_Callable(sub=True, desc="function for test page which sends a commands, waits and gets a response")
    def command_response(self):
        if get_tag(self, "command", "do", False):
            self.send("command")
        if get_tag(self, "resp_delay", "do", False):
            sleep(self.resp_delay)
        if get_tag(self, "response", "do", False):
            self.receive("response")

    command=Unicode().tag(sub=True, GPIB_writes="{command}", send_now=False, do=True)
    resp_delay=Float(0.0).tag(sub=True, unit2="s", desc="delay between command and response", do=True)
    response=Unicode().tag(sub=True, get_cmd=GPIB_read, spec="multiline", do=True)

    @booter
    def booter(self, address, delay, timeout, reset, selftest, lock, send_end, identify, clear):
        start_GPIB(self, self.address, self.delay, self.timeout, self.reset, self.selftest, self.lock, self.send_end, self.identify, self.clear)

    address=Unicode("GPIB0::22::INSTR").tag(sub=True, label = "GPIB Address")
    delay=Float(0).tag(sub=True, unit2="s", desc="delay between GPIB commands")
    timeout=Float(5).tag(sub=True, unit2="s", desc="timeout")

    @tag_Callable(sub=True)
    def reset(self):
        """send special GPIB command *RST"""
        GPIB_write(self, "*RST")


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
    def closer(self):
        """default GPIB stop is visa close"""
        self.session.close()

    def extra_setup(self, param, typer):
        super(GPIB_Instrument, self).extra_setup(param, typer)
        GPIB_string=get_tag(self, param, 'GPIB_writes')
        if GPIB_string!=None:
            do=get_tag(self, param, "do", False)
            set_tag(self, param, set_cmd=GPIB_write_it(GPIB_string, param), do=do)
        GPIB_string=get_tag(self, param, 'GPIB_asks')
        if GPIB_string!=None:
            do=get_tag(self, param, "do", False)
            set_tag(self, param, get_cmd=GPIB_ask_it(GPIB_string, param), do=do)

    @private_property
    def view_window(self):
        from enaml import imports
        with imports():
            from taref.instruments.instrument_e import GPIB_InstrumentView
        return GPIB_InstrumentView(instr=self)


#    def __init__(self, **kwargs):
#        super(GPIB_Instrument, self).__init__(**kwargs)
#        GPIB_string=get_tag(self, "command", 'GPIB_writes')
#        set_tag(self, "command", set_cmd=GPIB_write_it(GPIB_string, "command"))

if __name__=="__main__":
    t=GPIB_Instrument()
    t.boot(reset=True)
    t.show(t)
