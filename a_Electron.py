# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:03:26 2015

@author: thomasaref
"""
from functools import wraps
from atom.api import Atom, Unicode, Bool, Enum, List

from a_Nucleus import show
from a_Proton import (get_member, members, get_metadata, set_all_tags, set_tag, get_tag, get_all_tags, 
      get_reserved_names, get_all_params, get_all_main_params, get_main_params, get_type)


def list_recursion(mylist, index=0):
    """a test of list recursion"""
    item=mylist[index]
    print index, item
    if isinstance(item, list):
        return list_recursion(item)
    return

def updater(fn):
    """a decorator to stop infinite recursion"""
    @wraps(fn)
    def myfunc(self, change):
        if not hasattr(myfunc, "callblock"):
            myfunc.callblock=""
        if change["name"]!=myfunc.callblock: # and change['type']!='create':
            myfunc.callblock=change["name"]
            fn(self, change)
            myfunc.callblock=""
    return myfunc

class to(object):
    a=2
    b="hi"
    
    def __setattr__(self, name, value):
        super(to, self).__setattr__(name, value)
        if name in get_all_params(self):
            print "set {name} to {value}".format(name=name, value=value)        

c=to()    
print get_member(c, "a")
print members(c)
print get_metadata(c, "a")
set_all_tags(c, bill="chicken")
set_tag(c, "a", bill="cow")
print get_tag(c, "a", "bill", "moose")
print get_all_tags(c, "bill")
print get_reserved_names(c)
print get_all_params(c)
print get_all_main_params(c)
print get_main_params(c)
for key in members(c):
    print key, get_type(c, key)
show(c)
print c.b, c.a

#from a_Boss import boss
#
#class Electron(Atom):
#    name=Unicode().tag(private=True)
#    desc=Unicode().tag(private=True)
#    full_interface=Bool(False).tag(private=True) #checked by GUI but applies more to instrument
#    plot_all=Bool(False).tag(private=True)
#    view=Enum("Auto").tag(private=True)
#    main_params=List().tag(private=True)
#
#    @property
#    def abort(self):
#        """shortcut to boss' abort control"""
#        return self.boss.abort
#
#    @property
#    def boss(self):
#        """returns boss singleton instance. can be overwritten in subclasses to change boss"""
#        return boss
#
#    @property
#    def base_name(self):
#        """default base name of base if no name is given"""
#        return "base"
#
#    @property
#    def reserved_names(self):
#        """reserved names not to perform standard logging and display operations on,
#           i.e. members that are tagged as private and will behave as usual Atom members"""
#        return get_reserved_names(self) #get_all_tags("private", True)
#
#    @property
#    def all_params(self):
#        return get_all_params(self)
#
#    @property
#    def all_main_params(self):
#        return get_all_main_params(self)
#
#    def _default_main_params(self):
#        """defaults to all members in all_params that are not tagged as sub.
#        Can be overwritten to allow some minimal custom layout control,
#        e.g. order of presentation and which members are shown. Use self.all_main_params to get a list of
#        all members that could be in main_params"""
#        return self.all_main_params
#
#    def copy(self):
#        tempbase=type(self)()
#        for name in self.all_params:
#            setattr(tempbase, name, getattr(self, name))
#        for name in self.reserved_names:
#            setattr(tempbase, name, getattr(self, name))
#        return tempbase
#
#    def data_save(self, name, value):
#        """shortcut to data saving"""
#        self.boss.data_save(self, name, value)
#
#    def draw_plot(self):
#        """shortcut to plotting"""
#        self.boss.draw_plot(self)
#
#    def show(self):
#        """uses boss GUI control by passing itself"""
#        self.boss.show(base=self)
#
#    def get_all_tags(self, key, key_value=None, none_value=None, search_list=None):
#        """returns a list of names of parameters with a certain key_value"""
#        if search_list is None:
#            search_list=self.members()
#        if key_value==None:
#            return [x for x in search_list if none_value!=self.get_tag(x, key, none_value)]
#        return [x for x in search_list if key_value==self.get_tag(x, key, none_value)]
#
#    def set_tag(self, name, **kwargs):
#        """sets tag of parameter name using keywords arguments. Note that tags are shared between different instances of this class"""
#        self.get_member(name).tag(**kwargs)
#
#    def set_all_tags(self, **kwargs):
#        """set all parameters tags using keyword arguments"""
#        for param in self.all_params:
#            self.set_tag(param, **kwargs)
#
#    def func2log(self, name, cmdstr):
#        """returns cmd associated with cmdstr in tag and converts it to a log if it isn't already.
#          returns None if cmdstr is not in metadata"""
#        cmd=self.get_tag(name, cmdstr)
#        if not isinstance(cmd, func_log) and cmd is not None:
#            cmd=func_log(cmd)
#            self.set_tag(name, **{cmdstr:cmd})
#        return cmd
#
#    def get_run_params(self, name, key, notself=False, none_value=[]):
#        """returns the run parameters of get_cmd and set_cmd. Used in GUI"""
#        cmd=self.func2log(name, key)
#        if cmd is None:
#            return none_value
#        else:
#            run_params=cmd.run_params[:]
#            if notself:
#                if name in run_params:
#                    run_params.remove(name)
#            return run_params
#
#    def _observe_plot_all(self, change):
#        """if instrument plot_all changes, change all plot tags of parameters"""
#        if change['type']!='create':
#            set_all_tags(self, plot=self.plot_all)
#
#    def _observe_full_interface(self, change):
#        """if instrument full_interface changes, change all full_interface tags of parameters"""
#        if change['type']!='create':
#            self.set_all_tags(full_interface=self.full_interface)
#
#    def get_tag(self, name, key, none_value=None):
#        """retrieves metadata associated with name if key is None.
#        If key specified, returns metadata[key] or None if key is not in metadata"""
#        metadata=self.get_metadata(name)
#        if metadata==None:
#            return none_value
#        return metadata.get(key, none_value)
#
#    def get_metadata(self, name):
#        """retrieves metadata dictionary of member with given name"""
#        metadata=self.get_member(str(name)).metadata
#        if metadata:
#            return metadata
#        return {}
#
#    def lowhigh_check(self, name, value):
#        """can specify low and high tags to keep float or int within a range."""
#        metadata=self.metadata(name)
#        if metadata!=None:
#            if 'low' in metadata.keys():
#                if value<metadata['low']:
#                    return metadata['low']
#            if 'high' in metadata.keys():
#                if value>metadata['high']:
#                    return metadata['high']
#        return value
#
#    def get_type(self, name):
#        """returns type of parameter with given name"""
#        typer=type(self.get_member(name))
#        if typer in (Coerced, Instance, Typed):
#             typer=type(getattr(self, name))typer=get_member.validate_mode[1][1]
#        return self.get_tag(name, "type", typer)
#
#    def get_map(self, name, key=None):
#        """returns the mapped value (meant for an Enum). mapping is either a dictionary
#        or a string giving the name of a property in the class"""
#        #if get_type(self, name) in (List, ContainerList, list):
#        #    key=getattr(self, name)[key]
#        if key is None:
#            key=getattr(self, name)
#        return self.get_tag(name, "mapping")[key]
#
#    def get_inv(self, name, value):
#        """returns the inverse mapped value (meant for an Enum)"""
#        self.gen_inv_map(name)
#        return self.get_tag(name, 'inv_map')[value]
#
#    def gen_inv_map(self, name):
#        """generates the inverse map for a mapping if it doesn't exist (meant for an Enum)"""
#        if self.get_tag(name, 'inv_map') is None:
#            mapping=self.get_mapping(name) #self.get_tag(name, 'mapping', {getattr(self, name) : getattr(self, name)})
#            self.set_tag(name, inv_map={v:k for k, v in mapping.iteritems()})
#
#    def set_value_check(self, name, value):
#        """coerces and checks value when setting. This has to be different from getting to allow Enum to map properly. Not working for List?"""
#        value=self.coercer(name, value)
#        if self.get_type(name)==Enum:
#            return self.get_map(self, name, value) #self.get_tag(name, 'mapping', {value : value})[value]
#        return value
#
#    def coercer(self, name, value):
#        """Attempts to coerce values to the correct type. There is a Coerced option in Atom but this doesn't allow distinguishing of types"""
#        typer=self.get_type(name)
#        if typer in (Float, Int, Range, FloatRange):
#            value=self.lowhigh_check(name, value)
#        if typer in [Float, FloatRange]:
#            return float(value)
#        elif typer in [Int, Range]:
#            return int(value)
#        elif typer==Bool:
#           return bool(value)
#        elif typer==ContainerList:
#            return list(value)
#        elif typer==Str:
#            return str(value)
#        elif typer==Unicode:
#            return unicode(value)
#        else:
#           return value
#
#    def set_log(self, name, value):
#       """called when parameter of given name is set to value i.e. instr.parameter=value. Customized messages for different types. Also saves data"""
#       if self.get_tag(name, 'log', True):
#           label=self.get_tag(name, 'label', name)
#           unit=self.get_tag(name, 'unit', "")
#
#           if self.get_type(name)==ContainerList:
#               log_info("Set {instr} {label} to {length} list {unit}".format(
#                   instr=self.name, label=label, length=shape(getattr(self, name)), unit=unit))
#           elif self.get_type(name)==ndarray:
#               log_info("Set {instr} {label} to {length} array {unit}".format(
#                   instr=self.name, label=label, length=shape(getattr(self, name)), unit=unit))
#           elif self.get_type(name)==Callable:
#               pass
#           elif self.get_type(name)==Enum:
#               log_info("Set {instr} {label} to {value} ({map_val}) {unit}".format(
#                     instr=self.name, label=label, value=value,
#                     map_val=self.get_map(name, value), unit=unit))
#           elif self.get_type(name)==Dict:
#               log_info("Set {instr} {label}".format(instr=self.name, label=label))
#           elif self.get_type(name)==Str:
#               log_info("Set {instr} {label} to {length} string".format(instr=self.name, label=label, length=len(value)))
#           elif self.get_type(name) in (Float, FloatRange):
#               unit_factor=self.get_tag(name, 'unit_factor', 1.0)
#               log_info("Set {instr} {label} to {value} {unit}".format(
#                                 instr=self.name, label=label, value=value/unit_factor, unit=unit))
#           elif self.get_type(name) in (Int, Range):
#               unit_factor=self.get_tag(name, 'unit_factor', 1)
#               log_info("Set {instr} {label} to {value} {unit}".format(
#                                 instr=self.name, label=label, value=value/unit_factor, unit=unit))
#
#           else:
#               log_info("Set {instr} {label} to {value} {unit}".format(
#                                 instr=self.name, label=label, value=value, unit=unit))
#       self.data_save(name, value)
#
#    def __setattr__(self, name, value):
#        """extends __setattr__ to allow logging and data saving and automatic sending if tag send_now is true.
#        This is preferable to observing since it is called everytime the parameter value is set, not just when it changes."""
#        if name in self.all_params:
#            value=self.coercer(name, value)
#        super(Base, self).__setattr__( name, value)
#        if name in self.all_params:
#            self.set_log( name, value)
#
#    @property
#    def unit_dict(self):
#        return {"u" : 1.0e-6, "G" : 1.0e9}
#
#            
#    def log_changes(self, change):
#        self.set_log(change["name"], change["value"])
#        
#    def __init__(self, **kwargs):
#        """extends __init__ to set boss and add instrument to boss's instrument list.
##        Also adds observers for ContainerList parameters so if item in list is changed via some list function other than setattr, notification is still given.
##        Finally, sets all Callables to be log decorated if they weren't already."""
#        self.boss.make_boss()
#        super(Electron, self).__init__(**kwargs)
#        if "name" not in kwargs:
#            self.name= "{basename}__{basenum}".format(basename=self.base_name, basenum=len(self.boss.bases))
#        self.boss.bases.append(self)
#        for key in self.all_params:
#            typer=self.get_type(key)
#            self.observe(key, self.log_changes)
#            if typer==Callable:
#                func=getattr(self, key)
##                if isinstance(func, FunctionType):
##                    setattr(self, key, func_log(func, self))
#            elif typer in [Range, FloatRange]:
#                self.set_tag(key, low=self.get_member(key).validate_mode[1][0], high=self.get_member(key).validate_mode[1][1])
#            elif typer in [Int, Float]:
#                if self.get_tag(key, "unit", False) and self.get_tag(key, "unit_factor", True):
#                    unit=self.get_tag(key, "unit", "")[0]
#                    if unit in self.unit_dict:
#                        self.set_tag(key, unit_factor=self.unit_dict[unit])
#            elif typer==Enum:
#                items=self.get_member(key).items
#                mapping=self.get_tag(key, 'mapping')
#                map_type=self.get_tag(key, 'map_type')
#                if mapping is None:
#                    try:
#                        map_type="attribute"
#                        mapping=dict(zip(items, [getattr(self, item) for item in items]))
#                    except (AttributeError, TypeError):
#                        map_type="default"
#                        mapping=dict(zip(items, items))
#                elif isinstance(mapping, basestring): #define a mapping as a property
#                    map_type="property"
#                    mapping=getattr(self, mapping)
#                elif not isinstance(mapping, dict):
#                    raise TypeError("mapping must be dict or str")
#                self.set_tag(key, mapping=mapping, map_type=map_type)
#
#    def value_changed(self, change):
#        """observer for ContainerLists to handle updates not covered by setattr"""
#        if change['type'] not in ('create', 'update'):
#            self.set_log(change['name'], list(change['value']))
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


#if __name__=="__main__":
#    class test(object):
#        b=4
#        c=2
#
#        #@property
#        def f(self):
#            return 7
#        f.metadata=dict(mapping={7:1})
#
#
#    a=test()
#    print members(a)
#    print get_member(a, "c")
#    print get_metadata(a, "c")
#    metadata=get_metadata(a, "c")
#    metadata.update(money="power", foo="bar")
#    print get_metadata(a, "c")
#    print get_tag(a, "c", "h", True)
#    print get_map(a, "c", {2:3})
#    print get_map(a, "f")
#
#    print list_recursion([[["a", "d"],[ 1,2]], "b", "c"])
#
#    from atom.api import Int, observe, Coerced, Typed, Instance
#
#    class test(Atom):
#        a=Int().tag(money="time")
#        b=Int()
#        #c=Coerced(float, coercer=int)
#        c=Instance(float, ())
##        Instance
#
#        def _observe_a(self, change):
#            print change
#
#        def _observe_b(self, change):
#            print change
#
#        @observe('a')
#        @updater
#        def update_b(self, change):
#            self.b=self.a+1
#
#        @observe('b')
#        @updater
#        def update_a(self, change):
#            self.a=self.b+1

    #a=test()
    #print get_metadata(a, "a")
    #Coerced type get_member.validate_mode[1][1]
    #print get_member(a, "c").validate_mode
    #print
    #a.a=4
    #a.a=9
    #a.b=3


