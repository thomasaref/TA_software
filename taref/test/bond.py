# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 21:09:31 2016

@author: thomasaref
"""

class Bond(object):
    _reserved_names=("_reserved_names", "members", "get_member")
    def __init__(self):
        self._members={}
        for name in dir(self.__class__):
            if name.startswith("_") and name not in self._reserved_names:
                self._reserved_names+=(name,)
            if name not in self._reserved_names:
                attr=getattr(self.__class__, name)
                if isinstance(attr, property):
                    setattr(self, "_"+name, None)
                self._members[name]=attr
        for name in dir(self):
            if name.startswith("_"):
                self._reserved_names+=(name,)
            if name not in self._reserved_names:
                attr=getattr(self, name)
                self._members[name]=attr
                        
    def members(self):
        return self._members
        
    def get_member(self, name):
        return self._members.get(name, None)
        
class Test(Bond):
    def __init__(self):
        self.a=0
        super(Test, self).__init__()
        
    def __setattr__(self, name, value):
        if name not in self._reserved_names and name!="_members":
            print name+" set to "+str(value)
        super(Test, self).__setattr__(name, value)
        
a=Test()
print a._members
a.a=2
print a._members

#mydict={"aard":5}
#def a_get(self):
#    return mydict["aard"]
#def a_set(self, value):
#    print "yo" #mydict["aard"]=value
#
#class myproperty(object):
#    def __init__(self, name, cached=True):
#        self.cached=cached
#        def fget(self):
#            return mydict["aard"]
#        self.fget=fget
#        def set_cmd(self, value):
#            mydict["bard"]=value
#        self.set_cmd=set_cmd
#        def get_cmd(self):
#            return 10
#        self.get_cmd=get_cmd
#    def __call__(self):
#        return self.get_cmd(self)
#
#    
#def new_prop(def_func):
#    def get_na(self):
#        if get_na.value is None:
#            get_na.value=def_func(self)
#        return get_na.value
#    get_na.value=None
#
#    def set_na(self, value):
#        get_na.value=value
#    return property(get_na, set_na)
#    
#class Test(Bond):
#    #c=myproperty("blah")
#
#    #def __3setattr__(self, name, value):
#    #    if not name.startswith("_"):
#    #        if isinstance(getattr(self, name), myproperty):
#    #            getattr(self, name).set_cmd(self, value)
#    #    else:
#    #        super(Test, self).__setattr__(name, value)
#        #self.set_cmd(value)
#    @new_prop
#    def a(self):
#        return None#"hi"
#t=Test()
#from atom.api import Atom, cached_property
#from timeit import repeat
#class T2(Atom):
#    @cached_property
#    def a(self):
#        return "hi"
#t2=T2()
