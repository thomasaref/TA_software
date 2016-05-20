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
        self.trans_dict={bool: {True : -1, False : 0} }
        self.revrs_dict={bool: {-1 : True, 0 : False}}

    def __getitem__(self, const_name):
        """gets constant value from a com_lib, e.g. the comtypes module"""
        return getattr(self.com_lib, self.const_prefix+const_name)

    def __call__(self, const_name, prefix=None):
        if prefix is not None:
            const_name=prefix+const_name
        return self[const_name]

    def get_map(self, value, prefix):
        if isinstance(prefix, basestring):
            return self.get_dict(prefix)[value].partition(prefix)[2]
        return self.get_dict(prefix)[value]

    def set_value(self, key, prefix):
        if isinstance(prefix, basestring):
            return self.set_dict(prefix)[self.const_prefix+prefix+key]
        return self.set_dict(prefix)[key]

    def get_dict(self, prefix):
        if prefix not in self.revrs_dict:
            self.gen_dicts(prefix)
        return self.revrs_dict[prefix]

    def set_dict(self, prefix):
        if prefix not in self.trans_dict:
            self.gen_dicts(prefix)
        return self.trans_dict[prefix]

    def gen_dicts(self, prefix):
        self.trans_dict[prefix]=dict([(name, getattr(self.com_lib, name))
               for name in dir(self.com_lib) if self.id_attrs(name, prefix)])
        self.revrs_dict[prefix]=dict([(v, k) for k,v in self.trans_dict[prefix].iteritems()])

    def id_attrs(self, name, prefix):
        full_prefix=self.const_prefix+prefix
        if name.startswith(full_prefix):
            if name.split(full_prefix)[1][0].isupper():
                return True
        return False

    def searcher(self, search_name):
        return [name for name in dir(self.com_lib) if search_name in name]

class PXI_Backbone(object):
    """A backbone structure for working with PXI instruments, particularly Aeroflex instruments"""
    
    def __init__(self, lib_name, func_prefix=None, com_lib=None, const_prefix=None, *args, **kwargs):
        """initialization sets the library, creates error_msg and creates an object stored in session"""
        self.address=str(type(self))
        self._lib = WinDLL(lib_name)
        if func_prefix is None:
            func_prefix=lib_name.split('_')[0]
            func_prefix+='_'
        self.func_prefix=func_prefix
        if const_prefix is None:
            const_prefix=func_prefix
        self.clib=Const_Lib(com_lib=com_lib, const_prefix=const_prefix)
        self.error_msg=create_string_buffer(256)
        self.session=self.create_object(*args, **kwargs)


    def create_object(self):
        ses=c_long()
        self.do_func_no_session("CreateObject", byref(ses))
        return ses.value

    def get_error_message(self):
        """utility function that stores last error message"""
        self.do_func('ErrorMessage_Get', self.error_msg, 256)
        return self.error_msg.value

    def error_check(self):
        """utility function for error checking"""
        if self.error_code==0:
            #print "[{name}] No error: {code}".format(name=self.address, code=self.error_code)
            return
        msg=self.get_error_message()
        err_msg="[{name}] {code}: {msg}".format(name=self.address, code=self.error_code, msg=msg)
        if self.error_code>0:
            print "WARNING: "+err_msg
            return
        raise Exception("ERROR: "+err_msg)
            
    def do_func_no_session(self, func_name, *args):
        """basic execution of function"""
        self.error_code=getattr(self._lib, self.func_prefix+func_name)(*args)
        self.error_check()

    def do_func(self, func_name, *args):
        """basic execution of function from library using function prefix to simplify naming.
        auto includes session as first argument"""
        self.do_func_no_session(func_name, self.session, *args)

    def get_func(self, func_name, *args, **kwargs):
        """a utitilty method that creates a temporary reference for retrieving a value using a get type function. specify datatype by
        passing in dtype as a keywords argument (default to c_long)"""
        prefix=kwargs.pop('prefix', None)
        temp=kwargs.pop("dtype", c_long)()
        args=args+(byref(temp),)
        self.do_func(func_name, *args)
        if prefix is None:
            return temp.value
        return self.clib.get_map(temp.value, prefix)

    def set_func(self, func_name, *args, **kwargs):
        """a utitilty method that creates a temporary reference for retrieving a value using a get type function. specify datatype by
        passing in dtype as a keywords argument (default to c_long)"""
        prefix=kwargs.pop('prefix', None)
        temp=None
        if prefix is not None:
            temp=self.clib.set_value(args[-1], prefix)
            args=args[:-1]+(temp,)
        self.do_func(func_name, *args)
        return args

def pp(base_name, dtype=None, prefix=None, get_suffix="_Get", set_suffix="_Set"):
    """A utility function for making properties that have both a set and get function"""
    if dtype is None:
        def get_func(self):
            return self.get_func(base_name+get_suffix, prefix=prefix)
        def set_func(self, value):
            self.set_func(base_name+set_suffix, value, prefix=prefix)
    else:
        def get_func(self):
            return self.get_func(base_name+get_suffix, dtype=dtype, prefix=prefix)
        def set_func(self, value):
            self.set_func(base_name+set_suffix, dtype(value), prefix=prefix)
    return property(get_func, set_func)

if __name__=="__main__":
    PXI_Backbone(lib_name='afSigGenDll_32.dll')