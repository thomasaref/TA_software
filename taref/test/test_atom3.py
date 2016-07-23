# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 13:14:30 2016

@author: thomasaref
"""

class Value(object):
    def tag(self, **kwargs):
        self.metadata.update(kwargs)
        return self

    def __init__(self, value=0):
        self.value=value
        self.metadata={}
        self.name=None

    def set_func(self, obj, value):
        self.value=value

    def get_func(self, obj, typ):
        return self.value

    def namer(self, obj):
        if self.name is None:
            self.name=[name for name, mbr in obj.members().iteritems() if mbr==self][0]

    def defaulter(self, obj):
        if self.value is None:
            def_func=getattr(obj, "_default_"+self.name, None)
            if def_func is None:
                self.value=self.def_func(*self.args, **self.kwargs)
            else:
                self.value=def_func()

    def __get__(self, obj, typ):
        self.namer(obj)
        self.defaulter(obj)
        return self.get_func(obj, typ)

    def __set__(self, obj, value):
        self.namer(obj)
        obj.notify(self, value)
        self.set_func(obj, value)

class TypedValue(Value):
    typer=None

    def validate(self, value):
        if value is None:
            return True
        return type(value)==self.typer

    def defaulter(self, obj):
        if self.value is None:
            def_func=getattr(obj, "_default_"+self.name, None)
            if def_func is None:
                value=self.def_func()
            else:
                value=def_func()
            if not self.validate(value):
                raise Exception("Wrong type")
            self.value=value

    def __set__(self, obj, value):
        self.namer(obj)
        obj.notify(self, value)
        if not self.validate(value):
            raise Exception("Wrong type")
        self.set_func(obj, value)

class Int(TypedValue):
    typer=int

class Coerced(Value):
    def __init__(self, typer, args=(), kwargs={}, factory=None, coercer=None):
        super(Coerced, self).__init__(value=None)
        if factory is not None:
            self.def_func=factory
        else:
            factory = lambda: coercer(*args, **kwargs)
            self.def_func=factory
        self.coercer=coercer or typer

    def get_func(self, obj, typ):
        self.defaulter(obj)
        return self.value

    def set_func(self, obj, value):
        self.value=self.coercer(value)

class Typed(TypedValue):
    def __init__(self, typer, args=None, kwargs=None, factory=None):
        super(Typed, self).__init__(value=None)
        if factory is not None:
            self.def_func=factory
        elif args is not None or kwargs is not None:
            args = args or ()
            kwargs = kwargs or {}
            self.def_func = lambda: typer(*args, **kwargs)
        else:
            self.def_func = lambda: None
        self.typer=typer

class Obj(object):
    def __getattribute__(self, name):
        #cval=super(Obj, self).__getattribute__(name)
        if name in ("get_member", "get_ins_member", "get_cls_member", "__dict__"):
            return super(Obj, self).__getattribute__(name)
        cval=self.get_member(name)
        if isinstance(cval, Value):
            return cval.__get__(self, name)
        return super(Obj, self).__getattribute__(name)

    def notify(self, mbr, value):
        print "set", mbr.name, value

    def get_member(self, name):
        mbr=self.get_ins_member(name)
        if mbr is None:
            return self.get_cls_member(name)
        return mbr

    @classmethod
    def get_cls_member(cls, name):
        return cls.__dict__.get(name, None)

    def get_ins_member(self, name):
        return self.__dict__.get(name, None)

    def members(self):
        tdict=self.ins_members()
        tdict.update(self.cls_members()) #[(name, member) for name, member in self.__dict__.items() if isinstance(member, Value)])
        return tdict

    @classmethod
    def cls_members(cls):
        return dict([(name, member) for name, member in cls.__dict__.items() if isinstance(member, Value)])

    def ins_members(self):
        return dict([(name, member) for name, member in self.__dict__.items() if isinstance(member, Value)])

    def __setattr__(self, name, value):
        cval=self.get_ins_member(name)
        if isinstance(cval, Value):
            cval.__set__(self, value)
        else:
            super(Obj, self).__setattr__(name, value)

class Test(Obj):
    c=Int(20)
    d=Coerced(int, (2,))
    f=Typed(int, (21,))

    def _default_d(self):
        return 4

if __name__=="__main__":
    a=Test()
    a.a=Int(3)
    print a.d
    a.d=2
    print a.f
    a.f=3
    print a.get_member("f").typer
    #print a.a
    #print a.c, a.d
    #a.c=3
    #a.a=1
    #print a.members()
    #print a.cls_members()
    #print a.ins_members()
    #print a.get_member("a").name

    #print a.a, a.members()
    #print getattr(a, "d", "b")
    #a.a=5
    #print a.a, a.c, a.__dict__, a.members()
    #print a.cls_members(), a.get_cls_member("c")
