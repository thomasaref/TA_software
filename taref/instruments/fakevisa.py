# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 00:16:29 2016

@author: thomasaref
"""

class session(object):
    def clear(self):
        print "clear"
    def close(self):
        print "close"
    def write(self, wstr):
        print "write"+wstr
    def ask(self, astr):
        print "ask"+astr
        return astr
    def read(self):
        print "read"
        return "read"

class fakevisa(object):
    @staticmethod
    def instrument(address):
        return session()