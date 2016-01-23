# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 05:27:20 2016

@author: thomasaref

Universal functions useful in many instances
"""

from itertools import chain
from numpy import ndarray, array
from atom.api import Coerced

def sqze(*args):
    if len(args)==1:
        return list(chain.from_iterable(args[0]))
    return list(chain.from_iterable(args))

def cap_case(name, splitter="-", replacement=" "):
    """Auto captializes name while replacing splitter by replacement"""
    return replacement.join(s.capitalize() for s in name.split(splitter))


def read_text(file_path):
    """reads a text file and returns the string list with spaces stripped and newlines removed"""
    with open(file_path, "r") as f:
        str_list=[line.split("\n")[0].strip() for line in f]
    return str_list

def write_text(file_path, text_list, mode="w"):
    """writes a list of text to a file with newlines appended. default is to overwrite file"""
    with open(file_path, mode) as f:
        f.write("\n".join(text_list))

def Array(shape=1):
    return Coerced(ndarray, args=(shape,), coercer=array)


def pass_factory():
    def do_nothing():
        pass
    return do_nothing

def msg(*args):
    return ", ".join([unicode(arg) for arg in args])
