# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 20:44:22 2015

@author: thomasaref
"""

from taref.core.log import log_info, log_warning, make_log_file, remove_log_file, getLogger


log_info("balh")

log_info("yoy")
log_warning("yay")

logger=getLogger()

print logger.handlers[1].stream.log_str

for item in logger.handlers[2].buffer:
    print item

make_log_file("/Users/thomasaref/Documents/TA_software/test_code/ztestlog2.txt", mode='w')
remove_log_file()

log_info(2)

make_log_file("/Users/thomasaref/Documents/TA_software/test_code/ztestlog2.txt", mode='a')

#remove_log_file()
#with open("/Users/thomasaref/Documents/TA_software/test_code/ztestlog2.txt", "r") as f:
#    print f.read()

def show_log():
    from enaml.qt.qt_application import QtApplication
    from enaml import imports
    app = QtApplication()
    with imports():
        from t_log_e import Main# as LogWindow
    view=Main()
    view.show()
    app.start()

show_log()
if 0:
    log_info("balh")

    log_info("yoy")
    log_warning("yay")
    make_log_file("/Users/thomasaref/Documents/TA_software/test_code/ztestlog2.txt", mode='w')

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
