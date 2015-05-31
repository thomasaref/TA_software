# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:09:54 2015

@author: thomasaref
"""

#import logging
from logging import debug as log_debug, warning as log_warning, info as log_info
from logging import getLogger, StreamHandler, FileHandler, basicConfig, DEBUG, Formatter
import shutil
#configure logging
LOGFORMATTER='%(asctime)s - %(filename)s (line %(lineno)d) <%(funcName)s> %(levelname)s:  %(message)s'
LOGLEVEL=DEBUG
basicConfig(format=LOGFORMATTER, level=LOGLEVEL)
#LOG_NAME="record"
#BASE_PATH="/Users/thomasaref/Dropbox/Current stuff/TA_enaml"
#DIVIDER="/"
#LOG_PATH=BASE_PATH+DIVIDER+LOG_NAME
#FILE_NAME="meas"
SETUP_GROUP_NAME="SetUp"
SAVE_GROUP_NAME="Measurements"

def make_log_file(log_path, mode='w', display=None, logger=getLogger()):
    """Adds a stream and file handler if they do not exist"""
    if len(logger.handlers)<=1:
        display_handler=StreamHandler(stream=display)
        display_handler.setLevel(LOGLEVEL)
        display_handler.setFormatter(Formatter(LOGFORMATTER))
        logger.addHandler(display_handler)

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
    shutil.move(old_path, new_path)
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
    shutil.move(old_log_file, new_log_file)
    make_log_file(new_log_file, mode='a')

log_debug("Started logging")

if __name__=="__main__":
    log_info("yo")
    log_warning("yay")
