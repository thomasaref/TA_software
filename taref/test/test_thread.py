# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 19:07:30 2016

@author: thomasaref
"""

from enaml.application import Application
from threading import Thread

def code_caller(topdog, code, *args, **kwargs):
    result=code(*args, **kwargs)
    try:
        deferred_call(setattr, topdog, 'busy', False)
        deferred_call(setattr, topdog, 'progress', 0)
        deferred_call(setattr, topdog, 'abort', False)
    except RuntimeError:
        topdog.busy=False
        topdog.progress=0
        topdog.abort=False
    return result

def do_it_if_needed(topdog, code, *args, **kwargs):
    if not topdog.busy:
        topdog.busy = True
        thread = Thread(target=code_caller, args=(topdog, code)+args, kwargs=kwargs)
        thread.start()

def safe_setatt(obj, name, value):
    if Application.instance() is None:
        setattr(obj, name, value)


def cocall(code, *args, **kwargs):
    if Application.instance is None:
        return code(*args, **kwargs)
    else: