# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 16:09:54 2015

@author: thomasaref
"""

import logging
from logging import debug as log_debug, warning as log_warning, info as log_info
import shutil
#configure logging
LOGFORMATTER='%(asctime)s - %(filename)s (line %(lineno)d) <%(funcName)s> %(levelname)s:  %(message)s'
LOGLEVEL=logging.DEBUG
logging.basicConfig(format=LOGFORMATTER, level=LOGLEVEL)
#LOG_NAME="record"
#BASE_PATH="/Users/thomasaref/Dropbox/Current stuff/TA_enaml"
#DIVIDER="/"
#LOG_PATH=BASE_PATH+DIVIDER+LOG_NAME
#FILE_NAME="meas"
SETUP_GROUP_NAME="SetUp"
SAVE_GROUP_NAME="Measurements"

def make_log_file(log_path, mode='w', logger=logging.getLogger()):
    """makes a log file and adds the handler"""
    file_handler = logging.FileHandler(filename=log_path, mode=mode)#, delay=True)
    file_handler.setLevel(LOGLEVEL)
    formatter = logging.Formatter(LOGFORMATTER)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

#make_log_file()  #default log file

def move_files_and_log(new_path, old_path, log_name, logger = logging.getLogger()):
    """moves the entire directory from old_path to new_path and
       setups the log file for appended logging"""
    if len(logger.handlers)>1:
        remove_log_file(logger)
    shutil.move(old_path, new_path)
    make_log_file(new_path+log_name+".log", mode='a')

def log_flush(logger=logging.getLogger()):
    """flushes the log file"""
    file_handler=logger.handlers[1]
    file_handler.flush()

def remove_log_file(logger=logging.getLogger()):
    """closes the log file and removes it from the file handles"""
    file_handler=logger.handlers[1]
    file_handler.flush()
    file_handler.close()
    logger.removeHandler(file_handler)

def move_log_file(new_log_file, old_log_file, logger=logging.getLogger()):
    """closes old_log_file, moves it to new_log_file and begins new appending there"""
    if len(logger.handlers)>1:
        remove_log_file(logger)
    shutil.move(old_log_file, new_log_file)
    make_log_file(new_log_file, mode='a')



log_debug("Started logging")

if __name__=="__main__":
    log_info("yo")
    log_warning("yay")
