# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 21:15:11 2016

@author: thomasaref
"""

class Value(object):
    """a Value is quite similar to a property and is defined using a descriptor. The value has
    a default value, metadata and overwritable set and get functions"""

    slots=["value", "name", "metadata", "creation_counter", "creation_order"]
    creation_counter = 0

    def __init__(self, value=None):
        """initializes value, name and metadata"""
        self.value=value
        self.metadata={}
        self.name=None
        self.creation_order = Value.creation_counter
        Value.creation_counter+=1
    
    def tag(self, **kwargs):
        """a convenience function for adding metadata"""
        self.metadata.update(kwargs)
        return self

    def set_func(self, obj, value):
        """the default set_func just sets the value directly. overwritable in child classes"""
        self.value=value

    def get_func(self, obj, typ):
        """the default get_func just returns the value. overwritable in child classes"""
        return self.value

    #def namer(self, obj):
    #    """uses object searching to find own name. not needed if name is set externally"""
    #    if self.name is None:
    #        self.name=[name for name, mbr in obj.members().iteritems() if mbr==self][0]

    def defaulter(self, obj):
        """determines default value if value is None"""
        if self.value is None:
            def_func=getattr(obj, "_default_"+self.name, None)
            if def_func is None:
                self.value=self.def_func(*self.args, **self.kwargs)
            else:
                self.value=def_func()

    def __get__(self, obj, typ=None):
        #self.namer(obj)
        self.defaulter(obj)
        return self.get_func(obj, typ)

    def __set__(self, obj, value):
        #self.namer(obj)
        obj.notify(self, value)
        self.set_func(obj, value)

if __name__=="__main__":
    class test(object):
        a=Value().tag(g=2)
        
        def notify(self, obj, value):
            print self, obj, value
        
    b=test()
    c=test()
    print b.__dict__
    print type(b).__dict__
    print type(b).__dict__["a"].metadata
    print b.a, c.a
    b.a=2
    b.b=8
    print b.a, b.b, c.a
    