# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 10:53:08 2016

@author: thomasaref
"""

from sys import exc_info
from os.path import basename

def f_top_finder(fb):
    """recursive top frame finder"""
    if fb.f_back is None:
        return fb
    return f_top_finder(fb.f_back)

def f_top_limited(fb, n=100):
    """limited recursion top frame finder"""
    for m in range(n):
        if fb.f_back is None:
            return fb
        fb=fb.f_back
    return fb

def f_top(n=100):
    """returns the top frame after n steps"""
    try:
        raise Exception
    except:
        fb=exc_info()[2].tb_frame.f_back
    return f_top_limited(fb, n)

def msg(*args, **kwargs):
    """log msg that accepts multiple args with file info"""
    n=kwargs.pop("n", 100)
    fb=f_top(n)
    return "{0} {1} {2}: {3}".format(fb.f_lineno, basename(fb.f_code.co_filename),
              fb.f_code.co_name, ", ".join([str(arg) for arg in args]))

def new_log_func(func):
    """redefines func so args are incorporated into message and name and line of execution are correct"""
    def new_func(*args, **kwargs):
        n=kwargs.pop("n", 100)
        #fb=f_top(n)
        #if func is log:
        #    func(MYDEBUG, "{0} {1} {2}: {3}".format(fb.f_lineno, basename(fb.f_code.co_filename),
        #          fb.f_code.co_name, ", ".join([str(arg) for arg in args])), **kwargs)
        #print fb.f_lineno, fb, fb.f_back, fb.f_code.co_filename, fb.f_code.co_name
        print msg(*args, **dict(n=n))
    return new_func


def other_msg():
    locals_dict={}
    from sys import _getframe
    frame=_getframe()
    try:
        locals_dict=(frame.f_back.f_locals)
    finally:
        del frame
    #if hasattr(chief_cls, "code_window"):
    #    file_location=locals_dict.pop("__file__", "")
    #    with open(file_location) as f:
    #        showfile=f.read()

def myfunc(a):
    print a

myfunc2=new_log_func(myfunc)

#myfunc2("yay")

class Test(object):
    def in_func(self):
        myfunc2("yo", n=2)

if __name__=="__main__":
    t=Test()
    t.in_func()