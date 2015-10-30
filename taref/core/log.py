# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:09:54 2015

@author: thomasaref

A collection of logging related functions. Configures logging to be output
points it at a stream and a memory handler and starts logging.
"""

from logging import debug as log_debug, warning as log_warning, info as log_info
from logging import getLogger, StreamHandler, FileHandler, basicConfig, DEBUG, Formatter#, INFO
from logging.handlers import MemoryHandler
from atom.api import Atom, Unicode, Int

#configure logging
MEMBUFFER=30
LOGFORMATTER='%(asctime)s - %(filename)s (line %(lineno)d) <%(funcName)s> %(levelname)s:  %(message)s'
LOGLEVEL=DEBUG #INFO

basicConfig(format=LOGFORMATTER, level=LOGLEVEL)

class StreamCatch(Atom):
    """a stream catching class for use with the log window"""

    screen_width=Int(1920)
    screen_height=Int(1102)
    log_height=Int(100)
    log_width=Int()

    def _default_log_width(self):
        return self.screen_width

    @property
    def initial_position(self):
        return (0, self.screen_height-self.log_height)

    @property
    def initial_size(self):
        return (self.log_width, self.log_height)

    log_str=Unicode()

    def write(self,str):
        self.log_str=str+self.log_str

    def redirect_stdout(self, visible):
        import sys
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

log_debug("Started logging")

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
        memory_handler.target.flush()
        memory_handler.target.close()
        memory_handler.target=None
        return old_log_file_path

if __name__=="__main__":
    log_info("yoy")
    log_warning("yay")
    make_log_file("/Users/thomasaref/Documents/TA_software/ztestlog2.txt", mode='w')

    log_info(2)
    log_info(3)
    log_info(4)
    log_info(5)
    remove_log_file()
    #dir_path, divider, log_name=memory_handler.target.baseFilename.rpartition("/")
    #print dir_path, divider, log_name #memory_handler.target.baseFilename.split(log_name)
    log_info(6)
    make_log_file("/Users/thomasaref/Documents/TA_software/ztestlog2.txt")

    log_info(7)
    log_info(8)
    log_info(9)
    log_info(10)
    #
    #make_log_file("/Users/thomasaref/Documents/TA_software/ztestlog3.txt")

    log_info("yo")
    log_warning("yay")
