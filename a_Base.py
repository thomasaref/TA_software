# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 17:47:13 2014

@author: thomasaref
"""
from LOG_functions import log_info, log_debug
from atom.api import Atom, Instance, ContainerList, Unicode, Bool, Str, Float, Callable, Int, Typed, Enum, Dict, Coerced, Range, FloatRange, List
from types import FunctionType
from numpy import shape, ndarray
from Atom_Plotter import Plotter
from TA_Fundamentals import _func_log
from enaml.application import deferred_call
from threading import Thread
from a_Boss import boss #boss is imported to make it a singleton
        

def get_member(instr, name):
    try:
        return instr.get_member(str(name))
    except AttributeError,e:
        log_debug(e)
        return getattr(instr, name)

def get_metadata(instr, name):
    try:
        return instr.get_member(str(name)).metadata
    except AttributeError,e:
        #log_debug(e)
        return None
        
def get_tag(instr, name, key, none_value=None):
    """retrieves metadata associated with name if key is None.
    If key specified, returns metadata[key] or None if key is not in metadata"""
    metadata=get_metadata(instr, name)
    if metadata is None:
        return none_value
    return metadata.get(key, none_value)

def get_type(instr, name):
        """returns type of parameter with given name"""
        typer=type(get_member(instr, name))
        return get_tag(instr, name, "type", typer)

def get_main_params(instr):
    """ Generate a form specification for an instrument type."""
    try:
        main_params=instr.main_params
    except AttributeError,e:
        log_debug(e)
        try:
            main_params=instr.members()
        except AttributeError,e:
            log_debug(e)
            main_params=[name for name in dir(instr) if name[0]!='_'] 
    return main_params

def get_map(instr, name, key=None):
    """returns the mapped value (meant for an Enum). mapping is either a dictionary
        or a string giving the name of a property in the class"""
    if key is None:
        key=getattr(instr, name)
    return get_tag(instr, name, "mapping", {key:key})[key]
       
def code_caller(model, code, **kwargs):
    #try:
        result=code(model, **kwargs)
    #except RuntimeError, e:
    #    raise RuntimeError(e)
    #finally:
        try:
            deferred_call(setattr, model.boss, 'busy', False)
            deferred_call(setattr, model.boss, 'progress', 0)
            deferred_call(setattr, model.boss, 'abort', False)
        except RuntimeError:
            model.boss.busy=False
            model.boss.progress=0
            model.boss.abort=False
        return result
 
 
def do_it_if_needed(instr, code, **kwargs):
    if not instr.boss.busy:
        instr.boss.busy = True
        thread = Thread(target=code_caller, args=(instr, code), kwargs=kwargs)
        thread.start()


class func_log(_func_log):
    """decorator class to allow function logging"""
    def update_log(self, instr, kwargs):
        """update log function called by __call__. can be overwritten in subclasses to customize message"""
        log_info('RAN: {instr} {name}: {kwargs}'.format(
             instr=instr.name, name=self.f.func_name, kwargs=kwargs))

    def set_run_params(self, arg_count):
        self.run_params=list(self.f.func_code.co_varnames[1:arg_count])

    def __init__(self, f, instr=None):
        super(func_log, self).__init__(f)
        self.instr=instr

    def __call__(self, instr=None,  **kwargs):
        if instr is None:
            instr=self.instr
        for item in self.run_params:
            if item in kwargs.keys():
                setattr(instr, item, kwargs[item])
            else:
                value=getattr(instr, item)
                value=instr.set_value_check(item, value)
                kwargs[item]=value#getattr(instr, item)
        self.update_log(instr, kwargs)
        return do_it_if_needed(instr, self.f, **kwargs)

class BaseError(Exception):
    pass

class Base(Atom):
    """Base class. does lots of stuff
    Introduces tags:
       private: boolean, if attribute should be logged and watched, i.e. private=True items go into reserved_names
       sub: boolean, if attribute should be in main_params or not
       plot: boolean if attribute should be included inthe plot list
       full_interface: boolean, controls how fully attribute is displayed
       mapping: a dictionary for Enums do the value can be mapped. A default Enum mapping would be {value: value}
       type: an override so a particular type can be declared for the attribute which affects display. defaults to actual type via get_type
       low and high: limits numerical values so they stay within these limits. Auto declared for Ranges
       label: A more human friendly name of the attibute
       unit: the units the attribute is in
       inside_type: type inside containerlist"""

    name=Unicode().tag(private=True)
    desc=Unicode().tag(private=True)
    full_interface=Bool(False).tag(private=True) #checked by GUI but applies more to instrument
    plot_all=Bool(False).tag(private=True)
    view=Enum("Auto").tag(private=True)
    main_params=List().tag(private=True)
    
    @property
    def abort(self):
        return self.boss.abort

    @property
    def boss(self):
        """returns boss singleton instance. can be overwritten in subclasses to change boss"""
        boss.make_boss()
        return boss

    @property
    def base_name(self):
        """default base name of base if no name is given"""
        return "base"

    @property
    def reserved_names(self):
        """reserved names not to perform standard logging and display operations on,
           i.e. members that are tagged as private and will behave as usual Atom members"""
        return self.get_all_tags("private", True)
    @property
    def all_params(self):
        """all members that are not tagged as private, i.e. not in reserved_names and will behave as Bases"""
        return self.get_all_tags("private", False, False)

    @property
    def all_main_params(self):
        """all members in all_params that are not tagged as sub.
        Convenience property for more easily custom defining main_params in child classes"""
        return self.get_all_tags('sub', False, False, self.all_params)

    def _default_main_params(self):
        """defaults to all members in all_params that are not tagged as sub.
        Can be overwritten to allow some minimal custom layout control,
        e.g. order of presentation and which members are shown. Use self.all_main_params to get a list of
        all members that could be in main_params"""
        return self.all_main_params

    def copy(self):
        tempbase=type(self)()
        for name in self.all_params:
            setattr(tempbase, name, getattr(self, name))
        for name in self.reserved_names:
            setattr(tempbase, name, getattr(self, name))
        return tempbase

    def data_save(self, name, value):
        """shortcut to data saving"""
        self.boss.data_save(self, name, value)

    def draw_plot(self):
        """shortcut to plotting"""
        self.boss.draw_plot(self)

    def show(self):
        """uses boss GUI control by passing itself"""
        self.boss.show(base=self)

    def get_all_tags(self, key, key_value=None, none_value=None, search_list=None):
        """returns a list of names of parameters with a certain key_value"""
        if search_list is None:
            search_list=self.members().keys()
        if key_value==None:
            return [x for x in search_list if none_value!=self.get_tag(x, key, none_value)]
        return [x for x in search_list if key_value==self.get_tag(x, key, none_value)]

    def set_tag(self, name, **kwargs):
        """sets tag of parameter name using keywords arguments. Note that tags are shared between different instances of this class"""
        self.get_member(name).tag(**kwargs)

    def set_all_tags(self, **kwargs):
        """set all parameters tags using keyword arguments"""
        for param in self.all_params:
            self.set_tag(param, **kwargs)

    def func2log(self, name, cmdstr):
        """returns cmd associated with cmdstr in tag and converts it to a log if it isn't already.
          returns None if cmdstr is not in metadata"""
        cmd=self.get_tag(name, cmdstr)
        if not isinstance(cmd, func_log) and cmd is not None:
            cmd=func_log(cmd)
            self.set_tag(name, **{cmdstr:cmd})
        return cmd

    def get_run_params(self, name, key, notself=False, none_value=[]):
        """returns the run parameters of get_cmd and set_cmd. Used in GUI"""
        cmd=self.func2log(name, key)
        if cmd is None:
            return none_value
        else:
            run_params=cmd.run_params[:]
            if notself:
                if name in run_params:
                    run_params.remove(name)
            return run_params

    def _observe_plot_all(self, change):
        """if instrument full_interface changes, change all full_interface tags of parameters"""
        if change['type']!='create':
            self.set_all_tags(plot=self.plot_all)

    def _observe_full_interface(self, change):
        """if instrument full_interface changes, change all full_interface tags of parameters"""
        if change['type']!='create':
            self.set_all_tags(full_interface=self.full_interface)

    def get_tag(self, name, key, none_value=None):
        """retrieves metadata associated with name if key is None.
        If key specified, returns metadata[key] or None if key is not in metadata"""
        metadata=self.metadata(name)
        if metadata==None:
            return none_value
        return metadata.get(key, none_value)

    def metadata(self, name):
        """retrieves metadata dictionary of member with given name"""
        return self.get_member(str(name)).metadata

    def lowhigh_check(self, name, value):
        """can specify low and high tags to keep float or int within a range."""
        metadata=self.metadata(name)
        if metadata!=None:
            if 'low' in metadata.keys():
                if value<metadata['low']:
                    return metadata['low']
            if 'high' in metadata.keys():
                if value>metadata['high']:
                    return metadata['high']
        return value

    def get_type(self, name):
        """returns type of parameter with given name"""
        typer=type(self.get_member(name))
        if typer in (Coerced, Instance):
            typer=type(getattr(self, name))
        return self.get_tag(name, "type", typer)

    def get_map(self, name, key=None):
        """returns the mapped value (meant for an Enum). mapping is either a dictionary
        or a string giving the name of a property in the class"""
        #if get_type(self, name) in (List, ContainerList, list):
        #    key=getattr(self, name)[key]
        if key is None:
            key=getattr(self, name)
        return self.get_tag(name, "mapping")[key]
        
    def get_inv(self, name, value):
        """returns the inverse mapped value (meant for an Enum)"""
        self.gen_inv_map(name)
        return self.get_tag(name, 'inv_map')[value]

    def gen_inv_map(self, name):
        """generates the inverse map for a mapping if it doesn't exist (meant for an Enum)"""
        if self.get_tag(name, 'inv_map') is None:
            mapping=self.get_mapping(name) #self.get_tag(name, 'mapping', {getattr(self, name) : getattr(self, name)})
            self.set_tag(name, inv_map={v:k for k, v in mapping.iteritems()})

    def set_value_check(self, name, value):
        """coerces and checks value when setting. This has to be different from getting to allow Enum to map properly. Not working for List?"""
        value=self.coercer(name, value)
        if self.get_type(name)==Enum:
            return self.get_map(self, name, value) #self.get_tag(name, 'mapping', {value : value})[value]
        return value

    def coercer(self, name, value):
        """Attempts to coerce values to the correct type. There is a Coerced option in Atom but this doesn't allow distinguishing of types"""
        typer=self.get_type(name)
        if typer in (Float, Int, Range, FloatRange):
            value=self.lowhigh_check(name, value)
        if typer in [Float, FloatRange]:
            return float(value)
        elif typer in [Int, Range]:
            return int(value)
        elif typer==Bool:
           return bool(value)
        elif typer==ContainerList:
            return list(value)
        elif typer==Str:
            return str(value)
        elif typer==Unicode:
            return unicode(value)
        else:
           return value

    def set_log(self, name, value):
       """called when parameter of given name is set to value i.e. instr.parameter=value. Customized messages for different types. Also saves data"""
       if self.get_tag(name, 'log', True):
           label=self.get_tag(name, 'label', name)
           unit=self.get_tag(name, 'unit', "")
           
           if self.get_type(name)==ContainerList:
               log_info("Set {instr} {label} to {length} list {unit}".format(
                   instr=self.name, label=label, length=shape(getattr(self, name)), unit=unit))
           elif self.get_type(name)==ndarray:
               log_info("Set {instr} {label} to {length} array {unit}".format(
                   instr=self.name, label=label, length=shape(getattr(self, name)), unit=unit))
           elif self.get_type(name)==Callable:
               pass
           elif self.get_type(name)==Enum:
               log_info("Set {instr} {label} to {value} ({map_val}) {unit}".format(
                     instr=self.name, label=label, value=value,
                     map_val=self.get_map(name, value), unit=unit))
           elif self.get_type(name)==Dict:
               log_info("Set {instr} {label}".format(instr=self.name, label=label))
           elif self.get_type(name)==Str:
               log_info("Set {instr} {label} to {length} string".format(instr=self.name, label=label, length=len(value)))
           elif self.get_type(name) in (Float, FloatRange):
               unit_factor=self.get_tag(name, 'unit_factor', 1.0)
               log_info("Set {instr} {label} to {value} {unit}".format(
                                 instr=self.name, label=label, value=value/unit_factor, unit=unit))
           elif self.get_type(name) in (Int, Range):
               unit_factor=self.get_tag(name, 'unit_factor', 1)
               log_info("Set {instr} {label} to {value} {unit}".format(
                                 instr=self.name, label=label, value=value/unit_factor, unit=unit))
               
           else:
               log_info("Set {instr} {label} to {value} {unit}".format(
                                 instr=self.name, label=label, value=value, unit=unit))
       self.data_save(name, value)

    def __setattr__(self, name, value):
        """extends __setattr__ to allow logging and data saving and automatic sending if tag send_now is true.
        This is preferable to observing since it is called everytime the parameter value is set, not just when it changes."""
        if name in self.all_params:
            value=self.coercer(name, value)
        super(Base, self).__setattr__( name, value)
        if name in self.all_params:
            self.set_log( name, value)

    @property
    def unit_dict(self):
        return {"u" : 1.0e-6, "G" : 1.0e9}

    def __init__(self, **kwargs):
        """extends __init__ to set boss and add instrument to boss's instrument list.
        Also adds observers for ContainerList parameters so if item in list is changed via some list function other than setattr, notification is still given.
        Finally, sets all Callables to be log decorated if they weren't already."""
        super(Base, self).__init__(**kwargs)
        if "name" not in kwargs:
            self.name= "{basename}__{basenum}".format(basename=self.base_name, basenum=len(self.boss.bases))
        self.boss.bases.append(self)
            
        for key in self.all_params:
            typer=self.get_type(key)
            if typer==ContainerList:
                self.observe(key, self.value_changed)
            elif typer==Callable:
                func=getattr(self, key)
                if isinstance(func, FunctionType):
                    setattr(self, key, func_log(func, self))
            elif typer in [Range, FloatRange]:
                self.set_tag(key, low=self.get_member(key).validate_mode[1][0], high=self.get_member(key).validate_mode[1][1])
            elif typer in [Range, FloatRange, Int, Float]:
                if self.get_tag(key, "unit", False) and self.get_tag(key, "unit_factor", True):
                    unit=self.get_tag(key, "unit", "")[0]
                    if unit in self.unit_dict:
                        self.set_tag(key, unit_factor=self.unit_dict[unit])
#                setattr(self, key, getattr(self, key)*self.get_tag(key, "unit_factor", 1.0))
            elif typer==Enum:
                items=self.get_member(key).items
                mapping=self.get_tag(key, 'mapping')
                map_type=self.get_tag(key, 'map_type')
                if mapping is None:
                    try:
                    
                        #log_debug(items)
                        #log_debug([hasattr(self, item) for item in items])
                        #log_debug([getattr(self, item) for item in items])
                        map_type="attribute"
                        mapping=dict(zip(items, [getattr(self, item) for item in items]))
                    except (AttributeError, TypeError):
                        #print e
                        map_type="default"
                        mapping=dict(zip(items, items))
                elif isinstance(mapping, basestring): #define a mapping as a property
                    map_type="property"
                    mapping=getattr(self, mapping)
                elif not isinstance(mapping, dict):
                    raise TypeError("mapping must be dict or str")
                self.set_tag(key, mapping=mapping, map_type=map_type)
                
    def value_changed(self, change):
        """observer for ContainerLists to handle updates not covered by setattr"""
        if change['type'] not in ('create', 'update'):
            self.set_log(change['name'], list(change['value']))

    def add_plot(self, name=''):
        if name=="" or name in (p.name for p in self.boss.plots):
            name="plot{}".format(len(self.boss.plots))
            self.boss.plots.append(Plotter(name=name))

    def add_line_plot(self, name):
        xname=self.get_tag(name, 'xdata')
        if xname==None:
            xdata=None
        else:
            xdata=getattr(self, xname)
        self.boss.plots[0].add_plot(name, yname=name, ydata=getattr(self, name), xname=xname, xdata=xdata)
        self.boss.plots[0].title=self.name
        if xname==None:
            self.boss.plots[0].xlabel="# index"
        else:
            self.boss.plots[0].xlabel=self.get_tag(xname, "plot_label", xname)
        self.boss.plots[0].ylabel=self.get_tag(name, "plot_label", name)

    def add_img_plot(self, name):
        xname=self.get_tag(name, 'xdata')
        yname=self.get_tag(name, 'ydata')
        if xname!=None and yname!=None:
            xdata=getattr(self, xname)
            ydata=getattr(self, yname)
        else:
            xdata=None
            ydata=None
        self.boss.plot_list[0].add_img_plot(name, zname=name, zdata=getattr(self, name), xname=xname, yname=yname, xdata=xdata, ydata=ydata)
        self.boss.plot_list[0].title=self.name
        if xname==None:
            self.boss.plot_list[0].xlabel="# index"
        else:
            self.boss.plot_list[0].xlabel=self.get_tag(xname, "plot_label", xname)
        if yname==None:
            self.boss.plot_list[0].ylabel="# index"
        else:
            self.boss.plot_list[0].ylabel=self.get_tag(yname, "plot_label", yname)

class NoShowBase(Base):
    @property
    def base_name(self):
        """default base name of base if no name is given"""
        return "_base"

if __name__=="__main__":
    #class bt(Base):
    #    df=Int()
    a=Base(name="blah")
    print a.reserved_names
    print a.all_params
    print a.main_params
    print a.get_tag("desc", "bob")
    print a.get_all_tags("private", True, False)
    print a.get_all_tags("private", True, True)
    a.show()
    #print a.metadata("blah")
