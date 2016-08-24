# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:17:56 2016

@author: thomasaref
"""
from .value import Value
from collections import OrderedDict

def members(self, search="all"):
    """returns members as an ordered dictionary in order of creation.
    'all' returns all members, 'instance' returns instance members only
    and 'class' returns class members only"""
    ins_dict=OrderedDict(sorted([(name, member) for name, member in self.__dict__.iteritems() if isinstance(member, Value)],
                                 key = lambda mbr: mbr[1].creation_order))
    if search=="instance":
        return ins_dict
    cls_dict=OrderedDict(sorted([(name, member) for name, member in type(self).__dict__.iteritems() if isinstance(member, Value)],
                           key = lambda mbr: mbr[1].creation_order))
    if search=="class":
        return cls_dict
    cls_dict.update(ins_dict)
    return cls_dict

def get_member(self, name, search="all"):
    if search=="all":
        mbr=type(self).__dict__.get(name, None)
        return self.__dict__.get(name, mbr)
    elif search=="instance":
        return self.__dict__.get(name, None)
    elif search=="class":
        return type(self).__dict__.get(name, None)

class Object(object):
    """Objects activate the use of Values as both class and instance variables"""
    def __getattribute__(self, name):
        if name!="__dict__":
            cval=get_member(self, name)
            if isinstance(cval, Value):
                if cval.name is None:
                    cval.name=name
                return cval.__get__(self)
        return super(Object, self).__getattribute__(name)

    def notify(self, mbr, value):
        print "set", mbr.name, value

    def get_member(self, name, search="all"):
        return get_member(self, name, search=search)

    def members(self, search="all"):
        return members(self, search=search)

    def __setattr__(self, name, value):
        cval=get_member(self, name)
        if isinstance(cval, Value):
            if cval.name is None:
                cval.name=name
            cval.__set__(self, value)
        else:
            super(Object, self).__setattr__(name, value)
