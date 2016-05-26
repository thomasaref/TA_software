# -*- coding: utf-8 -*-
"""
Created on Wed May 25 11:19:18 2016

@author: Morran or Lumi
"""
class CommunicationError(Exception):
    pass

class InstrumentWorker(object):
    def __init__(self, **kwargs):
        self.fake_dict=kwargs
        
    def log(self, msg):
        print msg
        
    def getValue(self, name):
        return self.fake_dict[name]