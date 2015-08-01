# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:09:54 2015

@author: thomasaref

A collection of logging related functions. Configures logging to output and stream and starts it.
"""

from logging import debug as log_debug, warning as log_warning, info as log_info
from logging import getLogger, StreamHandler, FileHandler, basicConfig, DEBUG, Formatter, INFO
from logging.handlers import MemoryHandler
from shutil import move


#configure logging
LOGFORMATTER='%(asctime)s - %(filename)s (line %(lineno)d) <%(funcName)s> %(levelname)s:  %(message)s'

if 1:
    LOGLEVEL=DEBUG
else:
    LOGLEVEL=INFO

basicConfig(format=LOGFORMATTER, level=LOGLEVEL)

from atom.api import Atom, Unicode, Int

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

    def flush(self):
        pass

    def redirect_stdout(self, visible):
        import sys
        if visible:
            sys.stdout=self
            sys.stderr=self
        else:
            sys.stdout=sys.__stdout__ #old_stdout
            sys.stderr=sys.__stderr__

log_stream=StreamCatch()
logger=getLogger()
display_handler=StreamHandler(stream=log_stream)
display_handler.setLevel(LOGLEVEL)
display_handler.setFormatter(Formatter(LOGFORMATTER))
display_handler.name="StreamCatch"
logger.addHandler(display_handler)

memory_handler=MemoryHandler(30)
memory_handler.setLevel(LOGLEVEL)
memory_handler.setFormatter(Formatter(LOGFORMATTER))
memory_handler.name="MemoryLog"
logger.addHandler(memory_handler)

log_debug("Started logging")

def make_log_file(log_path, overwrite=False):
    """Points memory handler at a particular file. Overwrites file if overwrite is True"""
    if overwrite:
        with open(log_path, mode="w"):
            pass
    file_handler = FileHandler(filename=log_path)
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

def move_log_file(new_log_file_path):
    """closes old_log_file, moves it to new_log_file and continues appending there.
       creates log_file if it didn't exist before"""
    old_log_file_path=remove_log_file()
    if old_log_file_path:
        move(old_log_file_path, new_log_file_path)
    make_log_file(new_log_file_path)

if __name__=="__main__":
    log_info("yoy")
    log_warning("yay")
    make_log_file("/Users/thomasaref/Documents/TA_software/ztestlog2.txt", overwrite=True)

    log_info(2)
    log_info(3)
    log_info(4)
    log_info(5)
    #remove_log_file()
    #dir_path, divider, log_name=memory_handler.target.baseFilename.rpartition("/")
    #print dir_path, divider, log_name #memory_handler.target.baseFilename.split(log_name)
    log_info(6)
    log_info(7)
    log_info(8)
    log_info(9)
    log_info(10)
    #make_log_file("/Users/thomasaref/Documents/TA_software/ztestlog2.txt")

    move_log_file("/Users/thomasaref/Documents/TA_software/ztestlog3.txt")

    log_info("yo")
    log_warning("yay")
