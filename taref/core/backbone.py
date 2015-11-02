# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 21:52:51 2015

@author: thomasaref

A collection of functions for using taref's dynamic view. To maintain compatibility with Atom and object 
derived objects, these are defined as standalone functions. Get functions usually return some none_value even
if the value did not exist.
"""

from inspect import getmembers
from atom.api import Atom, List, Callable, Enum#, Int, Float, Callable, Unicode, Bool, List
from functools import wraps
from numpy import shape, ndarray
from enaml.application import deferred_call
from threading import Thread
from types import FunctionType

from taref.core.log import log_info

def get_member(obj, name):
    """returns a member if get_member exists and the attribute itself if it does not"""
    if hasattr(obj, "get_member"):
        return obj.get_member(str(name))
    return getattr(obj, str(name))

def members(obj):
    """returns members if defined, e.g. Atom class, or attributes whose names don't start with _"""
    if hasattr(obj, "members"):
        return obj.members()
    return dict([mem for mem in getmembers(obj) if mem[0][0]!="_"])

def get_metadata(obj, name):
    """returns the metadata of a member if it exists and generates an empty dictionary if it does not"""
    if isinstance(obj, Atom):
        member=obj.get_member(name)
        if member.metadata is None:
            member.metadata={}
        return member.metadata
    return {}

def set_tag(obj, name, **kwargs):
    """sets the tag of a member using Atom's built in tag functionality"""
    member=obj.get_member(name)
    member.tag(**kwargs)

def set_all_tags(obj, **kwargs):
    """set all parameters tags using keyword arguments"""
    for param in get_all_params(obj):
        set_tag(obj, param, **kwargs)

def get_tag(obj, name, key, none_value=None):
    """returns the tag key of a member name an returns none_value if it does not exist"""
    metadata=get_metadata(obj, name)
    return metadata.get(key, none_value)

def get_all_tags(obj, key, key_value=None, none_value=None, search_list=None):
    """returns a list of names of parameters with a certain key_value"""
    if search_list is None:
        search_list=members(obj)
    if key_value==None:
        return [x for x in search_list if none_value!=get_tag(obj, x, key, none_value)]
    return [x for x in search_list if key_value==get_tag(obj, x, key, none_value)]

def get_map(obj, name, value=None):
    """gets the mapped value specified by the property mapping and returns the attribute value if it doesn't exist"""
    if value is None:
        value=getattr(obj, name)
    if hasattr(obj, name+"_mapping"):
        return getattr(obj, name+"_mapping")[value]
    return value

def get_inv(obj, name, value):
    """returns the inverse mapped value (meant for an Enum)"""
    if hasattr(obj, name+"_mapping"):
        return {v:k for k, v in getattr(obj, name+"_mapping").iteritems()}[value]
    return value

def get_type(obj, name):
    """returns type of member with given name, with possible override via tag typer"""
    typer=type(get_member(obj, name))
    return get_tag(obj, name, "typer", typer)

def get_reserved_names(obj):
    """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
    return get_all_tags(obj, "private", True)

def get_all_params(obj):
    """all members that are not tagged as private, i.e. not in reserved_names and will behave as agents"""
    return get_all_tags(obj, key="private", key_value=False, none_value=False)

def get_all_main_params(obj):
    """all members in all_params that are not tagged as sub.
     Convenience function for more easily custom defining main_params in child classes"""
    return get_all_tags(obj, 'sub', False, False, get_all_params(obj))

def get_main_params(obj):
    """returns main_params if it exists and all possible main params if it does not"""
    if hasattr(obj, "main_params"):
        return obj.main_params
    return get_all_main_params(obj)

def get_attr(obj, name, none_value=None):
    """returns the attribute if the obj has it and the none_value if it does not"""
    if hasattr(obj, str(name)):
        return getattr(obj, name)
    return none_value

def lowhigh_check(obj, name, value):
    """can specify low and high tags to keep float or int within a range."""
    if type(value) in (float, int):
        metadata=get_metadata(obj, name)
        if 'low' in metadata:
            if value<metadata['low']:
                return metadata['low']
        if 'high' in metadata:
            if value>metadata.get['high']:
                return metadata['high']
    return value

def data_save(obj, name, value):
    """data saving. does nothing if data_save is not defined"""
    if hasattr(obj, "data_save"):
        obj.datasave(name, value)

def set_log(obj, name, value):
   """called when parameter of given name is set to value i.e. instr.parameter=value. Customized messages for different types. Also saves data"""
   if get_tag(obj, name, 'log', True):
       label=get_tag(obj, name, 'label', name)
       unit=get_tag(obj, name, 'unit', "")
       obj_name=get_attr(obj, "name", "NO_NAME")
       if get_type(obj, name)==Enum:
           log_info("Set {instr} {label} to {value} ({map_val})".format(
                 instr=obj_name, label=label, value=value,
                 map_val=get_map(obj, name, value)))
       #elif get_type(obj, name) in (Callable, type(dummyf)):
       #    log_info("Set {instr} {label} to {length} list".format(
       #        instr=obj_name, label=label, length=shape(getattr(obj, name))))
       elif type(value)==list:
           log_info("Set {instr} {label} to {length} list".format(
               instr=obj_name, label=label, length=shape(getattr(obj, name))))
       elif type(value)==ndarray:
           log_info("Set {instr} {label} to {length} array".format(
               instr=obj_name, label=label, length=shape(value)))
       elif type(value)==dict:
           log_info("Set {instr} {label}".format(instr=obj_name, label=label))
       elif type(value)==basestring:
           log_info("Set {instr} {label} to {length} string".format(instr=obj_name, label=label, length=len(value)))
       elif type(value)==float:
           unit_factor=get_tag(obj, name, 'unit_factor', 1.0)
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=value/unit_factor, unit=unit))
       elif type(value)==int:
           unit_factor=get_tag(obj, name, 'unit_factor', 1)
           log_info("Set {instr} {label} to {value} {unit}".format(
                             instr=obj_name, label=label, value=value/unit_factor, unit=unit))
       else:
           log_info("Set {instr} {label} to {value}".format(
                             instr=obj_name, label=label, value=value, unit=unit))
   data_save(obj, name, value)

unit_dict=dict(u=1.0e-6, m=1.0e-3, c=1.0e-2,
              G=1.0e9, M=1.0e6, k=1.0e3)

class Backbone(Atom):
    """Class combining primary functions for viewer operation"""
    main_params=List().tag(private=True, desc="main parameters: allows control over what is displayed and in what order")

    def get_metadata(self, name):
        return get_metadata(self, name)

    def set_tag(self, name, **kwargs):
        set_tag(self, name, **kwargs)

    def set_all_tags(self, **kwargs):
        set_all_tags(self, **kwargs)

    def get_tag(self, name, key, none_value=None):
        return get_tag(self, name, key, none_value)

    def get_all_tags(self, key, key_value=None, none_value=None, search_list=None):
        return get_all_tags(self, key, key_value, none_value, search_list)

    def get_type(self, name):
        return get_type(self, name)

    @property
    def reserved_names(self):
        return get_reserved_names(self)

    @property
    def all_params(self):
        return get_all_params(self)
        
    @property
    def all_main_params(self):
        return get_all_main_params(self)
        
    def _default_main_params(self):
        """defaults to all members in all_params that are not tagged as sub.
        Can be overwritten to allow some minimal custom layout control,
        e.g. order of presentation and which members are shown. Use get_all_main_params to get a list of
        all members that could be in main_params"""
        return self.all_main_params

    def lowhigh_check(self, name, value):
        return lowhigh_check(self, name, value)
        
    def set_log(self, name, value):
        set_log(self, name, value)

    def get_map(self, name, item=None):
        return get_map(self, name=name, item=item)

    @property
    def unit_dict(self):
        return unit_dict

def get_run_params(f, include_self=False):
    """returns names of parameters a function will call"""
    if hasattr(f, "run_params"):
        argnames=f.run_params
    else:
        argcount=f.func_code.co_argcount
        argnames=list(f.func_code.co_varnames[0:argcount])
    if not include_self and "self" in argnames:
        argnames.remove("self")
    return argnames

def code_caller(topdog, code, **kwargs):
    result=code(**kwargs)
    try:
        deferred_call(setattr, topdog, 'busy', False)
        deferred_call(setattr, topdog, 'progress', 0)
        deferred_call(setattr, topdog, 'abort', False)
    except RuntimeError:
        topdog.busy=False
        topdog.progress=0
        topdog.abort=False
    return result

def do_it_if_needed(topdog, code, **kwargs):
    if not topdog.busy:
        topdog.busy = True
        thread = Thread(target=code_caller, args=(topdog, code), kwargs=kwargs)
        thread.start()

def run_func(obj, name, **kwargs):
    """runs a function which is an attribute of an object. Auto-includes the obj itself depending on the types of function
    if kwargs are specified, it will set the attribtues of an object to those values (names need to match).
    if the object boss has the GUI threadsafe method do_it_if_needed, it will preferentially call that over the function itself"""
    f=getattr(obj, name)
    run_params=get_run_params(f)
    if get_type(obj, name) in (Callable, FunctionType):
        kwargs["self"]=obj
    for item in run_params:
        if item in kwargs:
            setattr(obj, item, kwargs[item])
        else:
            value=getattr(obj, item)
            value=set_value_map(obj, item, value)
            kwargs[item]=value
    do_it_if_needed(obj.chief, f, **kwargs)

def updater(fn):
    """a decorator to stop infinite recursion. also stores run_params as an attribute"""
    @wraps(fn)
    def updfunc(self, change):
        if not hasattr(updfunc, "callblock"):
            updfunc.callblock=""
        if change["name"]!=updfunc.callblock: # and change['type']!='create':
            updfunc.callblock=change["name"]
            fn(self, change)
            updfunc.callblock=""
    updfunc.run_params=get_run_params(fn)
    return updfunc

def log_func(fn):
    """a decorator that logs when a function is run. also stores run_params as an attribute"""
    @wraps(fn)
    def logf(*args, **kwargs):
        log_info("RAN: {name}".format(name=fn.func_name))
        fn(*args, **kwargs)
    logf.run_params=get_run_params(fn, True)
    return logf

#def get_args(obj, name):
#    f=getattr(obj, name)
#    run_params=get_run_params(f, True)
#    arglist=[]
#    if "self" in run_params:
#        if get_type(obj, name) in (Callable, FunctionType):
#            arglist.append(obj)
#        run_params.remove("self")
#    arglist.extend([getattr(obj, an) for an in run_params])
#    return arglist

def set_value_map(obj, name, value):
    """checks floats and ints for low/high limits and automaps an Enum when setting. Not working for List?"""
    value=lowhigh_check(obj, name, value)
    if get_type(obj, name)==Enum:
        return get_map(obj, name, value)
    return value


#
#    def copy(self):
#        tempbase=type(self)()
#        for name in self.all_params:
#            setattr(tempbase, name, getattr(self, name))
#        for name in self.reserved_names:
#            setattr(tempbase, name, getattr(self, name))
#        return tempbase
#




if __name__=="__main__":
    class to(object):
        a=5
        b=4.3
        c="hey"
        d=True

        @log_func
        def ff(self, a=2):
            print self, a
            print "a f says hello"


    class tA(Atom):
        a=Int(5)
        b=Float(4.3)
        c=Unicode("hey")
        d=Bool(True)
        f=Enum(1,2,3)
        g=Enum("a", "b")

        @Callable
        @log_func
        def ff(self, a=2):
            print self, a
            print "b f says hello"


    a=to()
    b=tA()
    print get_member(a, "a"), get_member(b, "a")
    print members(a), members(b)
    set_tag(a,"a", bill=5, private=True)
    set_tag(b,"a", bill="five", sub=True)
    set_all_tags(a, bob=7)
    set_all_tags(b, bob="seven")
    print get_metadata(a, "a"), get_metadata(b, "a")
    print get_tag(a, "a", "bill"), get_tag(b, "a", "bill")
    print get_all_tags(a, "bill"), get_all_tags(a, "bill", "five"),  get_all_tags(b, "bill", "five")
    print b.f, get_map(b, "f"), get_mapping(b, "f"), get_inv(b, "f", 2)
    print b.g, get_map(b, "g"), get_mapping(b, "g"), get_inv(b, "f", 2)
    print get_type(a, "a"), get_type(b, "a")
    print get_reserved_names(a), get_reserved_names(b)
    print get_all_params(a), get_all_params(b)
    print get_all_main_params(a), get_main_params(b)
    print get_main_params(a), get_main_params(b)
    print get_attr(a, "a", "yes"), get_attr(b, "aa", "yes")

    @log_func
    def ff(self, a=2):
        print self, a
        print "f says hello"
    a.gg=ff
    a.ff(), b.ff(b), a.gg(a)
    print get_run_params(ff), get_run_params(a.ff), get_run_params(a.gg)
    print b.a, a.a
    run_func(b, "ff", a=1), run_func(a, "ff", a=1), run_func(a, "gg")
    print b.a, a.a




    #print ff.func_code.co_argcount
    #print list(ff.func_code.co_varnames[0:ff.func_code.co_argcount])

#def get_args(obj, name):
#    f=getattr(obj, name)
#    run_params=get_run_params(f, True)
#    arglist=[]
#    if "self" in run_params:
#        arglist.append(obj)
#        run_params.remove("self")
#    arglist.extend([getattr(obj, an) for an in run_params])
#    return arglist
    #   Enum, Range, FloatRange, Int, Float, Callable, Unicode, Bool, List

#
#
#    def add_plot(self, name=''):
#        if name=="" or name in (p.name for p in self.boss.plots):
#            name="plot{}".format(len(self.boss.plots))
#            self.boss.plots.append(Plotter(name=name))
#
#    def add_line_plot(self, name):
#        xname=self.get_tag(name, 'xdata')
#        if xname==None:
#            xdata=None
#        else:
#            xdata=getattr(self, xname)
#        self.boss.plots[0].add_plot(name, yname=name, ydata=getattr(self, name), xname=xname, xdata=xdata)
#        self.boss.plots[0].title=self.name
#        if xname==None:
#            self.boss.plots[0].xlabel="# index"
#        else:
#            self.boss.plots[0].xlabel=self.get_tag(xname, "plot_label", xname)
#        self.boss.plots[0].ylabel=self.get_tag(name, "plot_label", name)
#
#    def add_img_plot(self, name):
#        xname=self.get_tag(name, 'xdata')
#        yname=self.get_tag(name, 'ydata')
#        if xname!=None and yname!=None:
#            xdata=getattr(self, xname)
#            ydata=getattr(self, yname)
#        else:
#            xdata=None
#            ydata=None
#        self.boss.plot_list[0].add_img_plot(name, zname=name, zdata=getattr(self, name), xname=xname, yname=yname, xdata=xdata, ydata=ydata)
#        self.boss.plot_list[0].title=self.name
#        if xname==None:
#            self.boss.plot_list[0].xlabel="# index"
#        else:
#            self.boss.plot_list[0].xlabel=self.get_tag(xname, "plot_label", xname)
#        if yname==None:
#            self.boss.plot_list[0].ylabel="# index"
#        else:
#            self.boss.plot_list[0].ylabel=self.get_tag(yname, "plot_label", yname)

#def set_attr(obj, name, value):
#    """a logging lowhigh checker for arbitrary classes. useful?"""
#    log_it=False
#    if name in get_all_params(obj) and isinstance(obj, (backbone, SubAgent)):
#        log_it=True
#        value=lowhigh_check(obj, name, value)
#    setattr(obj, name, value)
#    if log_it:
#        set_log(obj, name, value)

