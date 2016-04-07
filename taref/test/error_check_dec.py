# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 17:23:48 2016

@author: thomasaref
"""

def msg(ec):
    return "the error={}".format(ec)

def error_check(func):
    def new_func(*args, **kwargs):
        error_code=func(*args, **kwargs)
        if error_code==0:
            return
        if error_code<0:
            raise Exception(msg(error_code))
        else:
            print "Warning: "+msg(error_code)
    return new_func


@error_check
def get_freq():
    print "we got the freq on"
    return 1


get_freq()