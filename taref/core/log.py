# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:09:54 2015

@author: thomasaref

A collection of logging related functions. Configures logging to be output
points it at a stream and a memory handler and starts logging.
"""

from logging import warning, info, getLogger, StreamHandler, FileHandler, basicConfig, Formatter, INFO, DEBUG, log, addLevelName, INFO #, debug
from logging.handlers import MemoryHandler
from atom.api import Atom, Unicode, Int, cached_property
from sys import exc_info
from os.path import basename
import sys

#redefine DEBUG level so doesn't catch debug warnings from IPythonConsole in enaml

MYDEBUG=DEBUG+1
addLevelName(MYDEBUG, "MYDEBUG")
#configure logging
MEMBUFFER=30
LOGFORMATTER='%(asctime)s %(levelname)s  @ %(message)s'
LOGLEVEL=MYDEBUG #INFO #DEBUG

basicConfig(format=LOGFORMATTER, level=LOGLEVEL)

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
    n=kwargs.pop("n", 1)
    fb=f_top(n)
    return "{0} {1} {2}: {3}".format(fb.f_lineno, basename(fb.f_code.co_filename),
              fb.f_code.co_name, ", ".join([str(arg) for arg in args]))

def new_log_func(func):
    """redefines func so args are incorporated into message and name and line of execution are correct"""
    def new_func(*args, **kwargs):
        n=kwargs.pop("n", 2) #0
        if func is log:
            func(MYDEBUG, msg(*args, **{"n":n}), **kwargs)
        else:
            func(msg(*args, **{"n":n}), **kwargs)
    return new_func

log_debug=new_log_func(log)
log_info=new_log_func(info)
log_warning=new_log_func(warning)

class StreamCatch(Atom):
    """a stream catching class for use with the log window"""

    screen_width=Int(1920)
    screen_height=Int(1102)
    log_height=Int(100)
    log_width=Int()

    def _default_log_width(self):
        return self.screen_width

    @cached_property
    def initial_position(self):
        return (0, self.screen_height-self.log_height)

    @cached_property
    def initial_size(self):
        return (self.log_width, self.log_height)

    log_str=Unicode()

    def write(self, instr):
        self.log_str+=instr#+self.log_str

    def redirect_stdout(self, visible):
        if visible:
            sys.stdout=self
            sys.stderr=self
        else:
            sys.stdout=sys.__stdout__ #old_stdout
            sys.stderr=sys.__stderr__

#adds a stream catcher for display and a memory handler for saving
log_stream=StreamCatch()
logger=getLogger()
display_handler=StreamHandler(stream=log_stream)
display_handler.setLevel(LOGLEVEL)
display_handler.setFormatter(Formatter(LOGFORMATTER))
display_handler.name="StreamCatch"
logger.addHandler(display_handler)

memory_handler=MemoryHandler(MEMBUFFER)
memory_handler.setLevel(LOGLEVEL)
memory_handler.setFormatter(Formatter(LOGFORMATTER))
memory_handler.name="MemoryLog"
logger.addHandler(memory_handler)

log_info("Started logging")

def make_log_file(log_path, mode='a'):
    """Points memory handler at a particular file to save the log."""
    file_handler = FileHandler(filename=log_path, mode=mode)
    file_handler.setLevel(LOGLEVEL)
    file_handler.setFormatter(Formatter(LOGFORMATTER))
    memory_handler.setTarget(file_handler)

def remove_log_file():
    """closes the log file and removes memory_handler from pointing at it"""
    if memory_handler.target:
        old_log_file_path=memory_handler.target.baseFilename
        memory_handler.flush()
        memory_handler.target.flush()
        memory_handler.target.close()
        memory_handler.target=None
        return old_log_file_path