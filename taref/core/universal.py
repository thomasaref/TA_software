# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 05:27:20 2016

@author: thomasaref

Universal functions useful in many instances
"""

from itertools import chain
from numpy import ndarray, array
from atom.api import Coerced, Typed
from collections import OrderedDict

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
#    for line in text_list:
#        print unicode(line)
    #temp_str=u"\n".join(text_list)
    #print temp_str[21440:21460]
    #temp_str.encode('utf8') #foo.encode('utf8')
    with open(file_path, mode) as f:
        f.write("\n".join(text_list))

def Array(shape=1):
    #return Coerced(ndarray, args=(shape,), coercer=array)#.tag(typer=list)
    return Typed(ndarray, args=(shape,))

def Complex(default=0.0+0.0j):
    return Coerced(complex, (default,))

def ODict(default=None):
    if default is None:
        return Typed(OrderedDict, ())
    return Typed(OrderedDict, (default,))

def do_nothing(*args, **kwargs):
        pass

def pass_factory(*args, **kwargs):
    def do_nothing(*args, **kwargs):
        pass
    return do_nothing

def msg(*args):
    return ", ".join([unicode(arg) for arg in args])

def name_generator(name, indict,  default_value="NO_NAME", suffix="{name}__{num}"):
    """checks indict to see if name is in it and generates a new name based on length of indict if it is"""
    if name is None:
        name=default_value
    if name in indict:
        name="{name}__{num}".format(name=name, num=len(indict))
    return name
