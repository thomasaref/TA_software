# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:09:54 2015

@author: thomasaref

A collection of logging related functions. Configures logging to output and stream and starts it.
"""

from logging import debug as log_debug, warning as log_warning, info as log_info
from logging import getLogger, StreamHandler, FileHandler, basicConfig, DEBUG, Formatter, INFO
move=None


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
logger.addHandler(display_handler)

log_debug("Started logging")


def get_log_stream():
    logger=getLogger()
    return logger.handlers[1].stream.log_str
#display
#LOG_NAME="record"
#BASE_PATH="/Users/thomasaref/Dropbox/Current stuff/TA_enaml"
#DIVIDER="/"
#LOG_PATH=BASE_PATH+DIVIDER+LOG_NAME
#FILE_NAME="meas"
SETUP_GROUP_NAME="SetUp"
SAVE_GROUP_NAME="Measurements"

def make_log_file(log_path=None, mode='w', logger=getLogger()):
    """Adds a file handler if it does not exist"""
    if len(logger.handlers)<=2:
        file_handler = FileHandler(filename=log_path, mode=mode)#, delay=True)
        file_handler.setLevel(LOGLEVEL)
        file_handler.setFormatter(Formatter(LOGFORMATTER))
        logger.addHandler(file_handler)

#make_log_file()  #default log file

def move_files_and_log(new_path, old_path, log_name, logger = getLogger()):
    """moves the entire directory from old_path to new_path and
       setups the log file for appended logging"""
    if len(logger.handlers)>1:
        remove_log_file(logger)
    if move is None:
        from shutil import move
    move(old_path, new_path)
    make_log_file(new_path+log_name+".log", mode='a')

def log_flush(logger=getLogger()):
    """flushes the log file"""
    file_handler=logger.handlers[2]
    file_handler.flush()

def remove_log_file(logger=getLogger()):
    """closes the log file and removes it from the file handles"""
    file_handler=logger.handlers[2]
    file_handler.flush()
    file_handler.close()
    logger.removeHandler(file_handler)

def move_log_file(new_log_file, old_log_file, logger=getLogger()):
    """closes old_log_file, moves it to new_log_file and begins new appending there"""
    if len(logger.handlers)>1:
        remove_log_file(logger)
    if move is None:
        from shutil import move
    move(old_log_file, new_log_file)
    make_log_file(new_log_file, mode='a')


if __name__=="__main__":
    log_info("yo")
    log_warning("yay")
