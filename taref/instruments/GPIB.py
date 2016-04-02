# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 22:35:45 2014

@author: thomasaref
"""
from taref.instruments.instrument import InstrumentError, booter, closer
from taref.instruments.string_instrument import String_Instrument, writer, reader, asker
from taref.core.log import log_debug, log_info
from taref.core.atom_extension import tag_Callable, get_tag#, set_tag, log_func, private_property
from atom.api import Unicode, Bool, Float, Value
import visa
#from taref.instruments.fakevisa import fakevisa as visa
#from time import sleep

#def GPIB_read(instr):
#    """calls visa GPIB read"""
#    return instr.session.read()
#
#def GPIB_ask(instr, GPIB_string, **kwargs):
#    """calls visa GPIB ask using GPIB_string and kwargs"""
#    return instr.session.ask(GPIB_string.format(**kwargs))
#
#def GPIB_write(instr, GPIB_string, **kwargs):
#    """calls visa GPIB write using GPIB_string and kwargs"""
#    instr.session.write(GPIB_string.format(**kwargs))
#
#def ask_for_values(instr, GPIB_string, **kwargs):
#    """calls visa GPIB ask_for_values using GPIB_string and kwargs"""
#    return instr.session.ask_for_values(GPIB_string.format(**kwargs))

#def GPIB_ask_it(GPIB_string, name):
#    """returns custom GPIB_ask with GPIB_string encoded in GPIB_log object"""
#    def GPIB_ask(instr, **kwargs):
#        return instr.session.ask(GPIB_string.format(**kwargs))
#    GPIB_ask=log_func(GPIB_ask, name)
#    GPIB_ask.log_message="GPIB ASK: {0} {1}: "+GPIB_string
#    GPIB_ask.run_params.append(name)
#    #GPIB_ask.GPIB_string=GPIB_string
#    return GPIB_ask
#
#def GPIB_write_it(GPIB_string, name):
#    """returns custom GPIB_write with GPIB_string encoded in GPIB_log object"""
#    def GPIB_write(instr, **kwargs):
#        instr.session.write(GPIB_string.format(**kwargs))
#    GPIB_write=log_func(GPIB_write, name)
#    GPIB_write.log_message="GPIB WRITE: {0} {1}: "+GPIB_string
#    GPIB_write.run_params.append(name)
#    #func.GPIB_string=GPIB_string
#    return GPIB_write
def GPIB_lock(instr, timeout=None, requested_key=None):
    if timeout is None:
        return instr.session.lock(requested_key=requested_key)
    return instr.session.lock(timeout=timeout, requested_key=requested_key)
    
def start_GPIB(instr, address, #delay, timeout, 
                   reset, selftest, #send_end,
                   identify, clear,
               resource_manager, session, access_key):
    if address=="":
        raise InstrumentError("{0}: GPIB instruments need addresses.".format(instr.name))
    instr.address=address
    instr.resource_manager=visa.ResourceManager()
    
    instr.session=instr.resource_manager.open_resource(address) #visa.instrument(address)
    #self.session = visa.instrument(self.address, lock = lock, timeout = timeout, send_end=send_end, values_format = visa.single) #values_format=visa.single | visa.big_endian)
    if get_tag(instr, "access_key", "do", False):
        instr.access_key=GPIB_lock(instr)
        instr.lock=True
    if get_tag(instr, "clear", "do", False):
        instr.clear()
    if get_tag(instr, "reset", "do", False):
        instr.reset()
    if get_tag(instr, "selftest", "do", False):
        instr.selftest()
    if get_tag(instr, "identify", "do", False):
        instr.receive('identify')
    log_info("GPIB instrument {name} initialized at address {address}".format(name=instr.name, address=address))



class GPIB_Instrument(String_Instrument):
    """Extends Instrument definition to GPIB Instruments"""
    #session=Typed(visa.Instrument).tag(private=True, desc="visa session of the instrument")
    base_name="GPIB_Instrument"
    session=Value().tag(private=True, desc="a link to the session of the instrument. useful particularly for dll-based instruments")
    resource_manager=Value().tag(private=True, desc='a link to the resource_manager')
    
    @booter
    def booter(self, address, GPIB_delay, timeout, reset, selftest, send_end, identify, clear,
               resource_manager, session, access_key):
        start_GPIB(self, address, #self.GPIB_delay, self.timeout,
        reset, selftest, #send_end,
        identify, clear, resource_manager, session, access_key)

    address=Unicode("GPIB0::22::INSTR").tag(sub=True, label = "GPIB Address")
    GPIB_delay=Float(3).tag(sub=True, unit2="s", desc="delay between GPIB commands")
    #timeout=Float(5).tag(sub=True, unit2="s", desc="timeout")

    @tag_Callable(sub=True, do=False)
    def reset(self):
        """send special GPIB command *RST"""
        self.writer("*RST")

    @tag_Callable(sub=False, do=True)
    def excl_lock(self):
        self.session.excl_lock()
        
    @tag_Callable(sub=False, do=True)        
    def unlock(self):
        if self.lock:
            self.session.unlock()
            self.lock=False
    
    access_key=Unicode().tag(sub=True, do=False, no_spacer=True)    
    lock = Bool(False).tag(sub=False)
    send_end = Bool(True).tag(sub=True)

    @tag_Callable(sub=True, do=False)
    def clear(self):
        """calls visa GPIB clear"""
        self.session.clear()

    identify = Unicode().tag(sub=True, get_str="*IDN?", do=True, read_only=True, no_spacer=True)

    @tag_Callable(sub=True)
    def selftest(self):
        """perform selftest specified by special GPIB command *TST?"""
        tst=self.asker("*TST?")
        if int(tst):
            raise InstrumentError("Instrument {0} did not pass the selftest. CODE: {1}".format(self.name, tst))

    @closer
    def closer(self):
        """default GPIB stop is visa close"""
        self.unlock()
        self.session.close()
        self.resource_manager.close()
    
    @reader
    def reader(self):
        """calls visa GPIB read"""
        return self.session.read()

    @asker
    def asker(self, ask_string):
        """calls visa GPIB ask"""
        return self.session.ask(ask_string)

    @writer
    def writer(self, write_string):
        """calls visa GPIB write"""
        self.session.write(write_string)

    def ask_for_values(self, ask_string):
        """calls visa GPIB ask_for_values using GPIB_string and kwargs"""
        return self.session.ask_for_values(ask_string)

#    @private_property
#    def view_window(self):
#        from enaml import imports
#        with imports():
#            from taref.instruments.instrument_e import GPIB_InstrumentView
#        return GPIB_InstrumentView(instr=self)


#    def __init__(self, **kwargs):
#        super(GPIB_Instrument, self).__init__(**kwargs)
#        GPIB_string=get_tag(self, "command", 'GPIB_writes')
#        set_tag(self, "command", set_cmd=GPIB_write_it(GPIB_string, "command"))

if __name__=="__main__":
    t=GPIB_Instrument()
    t.boot(reset=True)
    t.show(t)
