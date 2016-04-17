# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 15:10:47 2016

@author: thomasaref
"""


from logging import debug, warning, info, WARNING, getLogger, StreamHandler, FileHandler, basicConfig, Formatter, INFO, DEBUG, log, addLevelName, INFO #, debug

basicConfig(format='%(asctime)s %(levelname)s %(lineno)s  @ %(message)s', level=DEBUG)

print DEBUG, INFO, WARNING
from time import time

log(9, "log")
tstart=time()
debug("hi")
info("info log")
warning("warning log")

print time()-tstart