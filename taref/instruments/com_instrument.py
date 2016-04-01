# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 22:11:23 2016

@author: zebra
"""

from taref.instruments.string_instrument import String_Instrument
from taref.core.atom_extension import set_tag, get_tag, log_func, get_all_tags

#def pass_ask_it(instr, name):
#    """get pass function. used as place holder."""
#    def pass_ask(instr, **kwargs):
#        return getattr(instr, name)
#    pass_ask=log_func(pass_ask, name)
#    pass_ask.log_message="PASS ASK: {0} {1}: "+name
#    return pass_ask
#    
#def pass_write_it(instr, name):
#    """send pass function. used as place holder"""
#    def pass_write(instr, **kwargs):
#        setattr(instr, name, kwargs[name])
#    pass_write=log_func(pass_write, name)
#    pass_write.log_message="PASS WRITE: {0} {1}: "+name
#    pass_write.run_params.append(name)
#    return pass_write 
   
class COM_Instrument(String_Instrument):
    """Instrument specialization to deal with COM drivers"""
    def COM_ask_it(self, name, aka):
        """returns custom COM_ask using alias aka"""
        obj, param, index=self.get_ptr(aka)
        if index is None:
            def COM_ask(self, **kwargs):
                return getattr(obj, param) #instr.session.ask(GPIB_string.format(**kwargs))
        else:
            def COM_ask(self, **kwargs):
                return getattr(obj, param)[index] #instr.session.ask(GPIB_string.format(**kwargs))
        COM_ask=log_func(COM_ask, name)
        COM_ask.log_message="COM ASK: {0} {1}: "+name
        return COM_ask
    
    def COM_write_it(self, name, aka):
        """returns custom COM_write with using alias aka"""
        obj, param, index=self.get_ptr(aka)
        if index is None:
            def COM_write(self, **kwargs):
                setattr(obj, param, kwargs[name])
        else:
            def COM_write(self, **kwargs):
                getattr(obj, param)[index]=kwargs[name]
        COM_write=log_func(COM_write, name)
        COM_write.log_message="COM WRITE: {0} {1}: "+name
        COM_write.run_params.append(name)
        return COM_write

    def get_ptr(self, name):
        """gets pointer to obj and param from alias. can handle multiple dots in path but not brackets.
        param can be indexed with an integer"""
        name_list=name.split(".")
        param=name_list[-1]
        index=None
        if "[" in param:
            param, div, index=param.partition("]")[0].partition("[")
            index=int(index)
        obj=self
        for x in name_list[1:-1]:
            obj = getattr(obj, x)
        return obj, param, index
    
    def extra_setup(self, param, typer):
        aka = get_tag(self, param, "aka")
        if aka!=None:
            do=get_tag(self, param, "do", False)
            readwrite=get_tag(self, param, "ReadWrite", "Both")
            if readwrite in ("Both", "Write"):
                set_tag(self, param, set_cmd=param+"={"+param+"}", do=do)
            if readwrite in ("Both", "Read"):
                set_tag(self, param, get_str=param, do=do)  
        super(String_Instrument, self).extra_setup(param, typer)
    
    def postboot(self):
        for param in get_all_tags(self, "aka"):
            aka = get_tag(self, param, "aka")
            if get_tag(self, param, "set_cmd") is not None:
                set_tag(self, param, set_cmd=self.COM_write_it(param, aka))
            if get_tag(self, param, "get_cmd") is not None:
                set_tag(self, param, get_cmd=self.COM_ask_it(param, aka))
        for param in self.all_params:
            if get_tag(self, param, 'get_cmd') is not None:
                log_debug(param)
                self.receive(param)        

#def VNA_ask_it(self, VNA_string, name):
#    """returns custom GPIB_ask with GPIB_string encoded in GPIB_log object"""
#    def na_ask(self, **kwargs):
#        return self.VNA_ask(VNA_string.format(**kwargs))
#    na_ask=log_func(na_ask, name)
#    na_ask.log_message="VNA ASK: {0} {1}: "+VNA_string
#    na_ask.run_params.append(name)
#    return na_ask
#
#def VNA_write_it(instr, VNA_string, name):
#    """returns custom GPIB_write with GPIB_string encoded in GPIB_log object"""
#    def VNA_write(instr, **kwargs):
#        instr.VNA.write(VNA_string.format(**kwargs))
#    VNA_write=log_func(VNA_write, name)
#    VNA_write.log_message="GPIB WRITE: {0} {1}: "+VNA_string
#    VNA_write.run_params.append(name)
#    return VNA_write