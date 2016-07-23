# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 10:31:25 2016

@author: thomasaref
"""
class Value(object):
    __slots__=["value", "metadata", "typer"]
    def __init__(self, value):
        self.value=value
        self.metadata={}
        if value is None:
            self.typer=None
        else:
            self.typer=type(value)

    def tag(self, **kwargs):
        self.metadata.update(kwargs)
        return self


def test_f(obj):
    print obj

def test_f2():
    print "hi"



class Big(object):
    def get_tag(self, name, key, none_value=None):
        member=self.get_member(name)
        if member is None:
            return none_value
        return member.metadata.get(key, none_value)

    def set_tag(self, name, **kwargs):
        self.__members__[name].tag(**kwargs)

    def get_member(self, name):
        return self.__members__.get(name, None)

    def notify(self, name, value):
        print name, value

    def set_attr(self, name, value):
        setattr(self, name, value)
        if name in self.__members__:
            return self.get_member(name)

    def __setattr__(self, name, value):
        if not name.startswith("_") and not name.endswith("_"):
            if not hasattr(self, "__members__"):
                self.__members__={}
            cval=self.__members__.pop(name, None)
            if cval is None:
                cval=Value(value)
            else:
                if type(value)!=cval.typer:
                    raise Exception("Wrong type")
                cval.value=value
            self.__members__[name]=cval
            self.notify(name, value)
        super(Big, self).__setattr__(name, value)

    def __getattribute__(self, name):
        cval=None
        if not name.startswith("_") and not name.endswith("_"):
            cval=self.__members__.get(name, None)
        if cval is None:
            return super(Big, self).__getattribute__(name)
        return cval.value

class Test(Big):
    def __init__(self, a=1):
        self.a=a
        self._b=5
        self.set_tag("a", private=True)

if __name__=="__main__":
    a=Test()
    a.set_attr("d", 5.0).tag(g=3)
    print a.a, a._b
    print a.get_tag("a", "private")
    print a.get_tag("d", "g")
    print a.__members__
    print a.get_member("a").typer
    a.a=10
    print a.a, a._b
    a._b="1"
    a.b_="1"
    a.c=test_f
    a.c(3)
    print a.__members__
    a.c=test_f2
    a.c()
    a.c="d"