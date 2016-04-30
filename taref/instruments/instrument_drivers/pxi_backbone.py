# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 12:19:00 2016

@author: thomasaref
"""
from ctypes import WinDLL, create_string_buffer, c_long, byref

class Const_Lib(object):
    def __init__(self, com_lib, const_prefix=""):
        self.com_lib=com_lib
        self.const_prefix=const_prefix
        self.trans_dict={}

    def __getitem__(self, const_name):
        """gets constant value from a com_lib, e.g. the comtypes module"""
        return getattr(self.com_lib, self.const_prefix+const_name)

    def get_dict(self, prefix):
        return dict(zip([(name, getattr(self.com_lib, name)) for name in dir(self.com_lib) if name.starts_with(self.const_prefix+prefix)]))

class PXI_Backbone(object):
    """A backbone structure for working with PXI instruments, particularly Aeroflex instruments"""

    def __init__(self, lib_name, func_prefix=None, com_lib=None, const_prefix=None):
        """initialization sets the library, creates error_msg and creates an object stored in session"""
        self._lib = WinDLL(lib_name)
        if func_prefix is None:
            func_prefix=lib_name.split('_')[0]
            func_prefix.append('_')
        self.func_prefix=func_prefix
        if const_prefix is None:
            const_prefix=func_prefix
        self.clib=Const_Lib(com_lib=com_lib, const_prefix=const_prefix)
        self.const_prefix=const_prefix
        self.error_msg=create_string_buffer(256)
        self.session=self.get_func("CreateObject")

    def get_const(self, const_name):
        """gets constant value from a com_lib, e.g. the comtypes module"""
        return self.clib[const_name]

    def get_error_message(self):
        """utility function that stores last error message"""
        self.do_func('ErrorMessage_Get', self.session, self.error_msg, 256)
        return self.error_msg.value

    def error_check(self):
        """utility function for error checking"""
        if self.error_code==0:
            print "No error: {}".format(self.error_code)
            return
        msg=self.get_error_message(self.session)
        if self.error_code<0:
            raise Exception("{0}: {1}".format(self.error_code, msg))
        elif self.error_code>0:
            print "WARNING: {0}: {1}".format(self.error_code, msg)

    def do_func(self, func_name, *args):
        """basic execution of function from library using function prefix to simplify naming"""
        self.error_code=getattr(self._lib, self.func_prefix+func_name)(*args)
        self.error_check()

    def get_func(self, func_name, *args, **kwargs):
        """a utitilty method that creates a temporary reference for retrieving a value using a get type function. specify datatype by
        passing in dtype as a keywords argument (default to c_long)"""
        prefix=kwargs.pop('prefix', None)
        temp=kwargs.pop("dtype", c_long)()
        args=args+(byref(temp),)
        self.do_func(func_name, *args)
        if prefix is None:
            return temp.value
        else:
            if prefix not in self.trans_dict:
                self.trans_dict[prefix]=self.clib.get_dict(prefix)
        return self.trans_dict[prefix].get(temp.value, temp.value)


if __name__=="__main__":
    PXI_Backbone(lib_name='afSigGenDll_32.dll')