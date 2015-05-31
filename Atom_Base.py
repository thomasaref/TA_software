# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 17:47:13 2014

@author: thomasaref
"""

from LOG_functions import log_info, log_debug, make_log_file
from atom.api import Atom, Instance, ContainerList, Unicode, Bool, Str, Float, Callable, List, Int, Typed, Enum, Dict, Coerced, Range, FloatRange
from Atom_Boss import Boss, boss #master is imported to make it a singleton (all slaves (aka instruments) have the same master)
from types import FunctionType
from enaml import imports #import enaml
from enaml.qt.qt_application import QtApplication
from numpy import shape, ndarray
from Atom_Plotter import Plotter
from TA_Fundamentals import _func_log

class log(_func_log):
    """decorator class to allow function logging"""
    def update_log(self, instr, kwargs):
        """update log function called by __call__. can be overwritten in subclasses to customize message"""
        log_info('RAN: {instr} {name}: {kwargs}'.format(
             instr=instr.name, name=self.f.func_name, kwargs=kwargs))

    def set_run_params(self, arg_count):
        self.run_params=list(self.f.func_code.co_varnames[1:arg_count])

    def __call__(self, instr,  **kwargs):
        for item in self.run_params:
            if item in kwargs.keys():
                setattr(instr, item, kwargs[item])
            else:
                value=getattr(instr, item)
                value=instr.set_value_check(item, value)
                kwargs[item]=value#getattr(instr, item)
        self.update_log(instr, kwargs)
        return self.f(instr, **kwargs)

class BaseError(Exception):
    pass

class Base(Atom):
    """Base class. does lots of stuff
    Introduces tags:
       private: boolean, if attribute should be logged and watched, i.e. private=True items go into reserved_names
       sub: boolean, if attribute should be in main_params or not
       plot: boolean if attribute should be included inthe plot list
       full_interface: boolean, controls how fully attriabute is displayed
       mapping: a dictionary for Enums do the value can be mapped. A default Enum mapping would be {value: value}
       type: an override so a particular type can be declared for the attribute which affects display. defaults to actual type via get_type
       low and high: limits numerical values so they stay within these limits. Auto declared for Ranges
       label: A more human friendly name of the attibute
       unit: the units the attribute is in
       inside_type: type inside containerlist"""

    boss=Typed(Boss).tag(private=True)
    name=Unicode().tag(private=True)
    desc=Unicode().tag(private=True)
    all_params=List().tag(private=True)
    main_params=List().tag(private=True)
    #sub_params=List() #remove?
    reserved_names=List().tag(private=True)
    #showing=Bool(False) #remove?
    full_interface=Bool(False).tag(private=True) #checked by GUI but applies more to instrument
    plot_all=Bool(False).tag(private=True)
    show_base=Bool(True).tag(private=True) #boolean that controls if base appears in boss toolbar
    view=Enum("Auto").tag(private=True)

    #plot_keys=List() #remove?

    def _default_reserved_names(self):
        """reserved names not to perform standard logging and display operations on. can be overwritten in child classes"""
        #return Slave.members().keys()
        return self.get_all_tags("private", True)

    def _default_all_params(self):
        """defaults to all parameters added to child class which are not in reserved names"""
        return self.get_all_tags("private", False, False)
        #all_params=self.members().keys()[:]
        #for item in self.reserved_names:
        #    all_params.remove(item)
        #return all_params

    def _default_main_params(self):
        """defaults to all parameters that are not tagged as sub. Can be overwritten to allow custom layout"""
        return self.get_all_tags('sub', False, False, self.all_params)
        #main_params=[]
        #for item in self.all_params:
        #    if not self.get_tag(item, 'sub', False):
        #        main_params.append(item)
        #return main_params

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

    def show(self): #needs some work
        """stand alone for showing instrument. Shows a modified boss view that has the instrument as a dockpane"""
        with imports():
            from enaml_Boss import BossMain
        app = QtApplication()
        view = BossMain(base=self, boss=self.boss)
        view.show()
        app.start()

    def get_all_tags(self, key, key_value=None, none_value=None, search_list=None):
        """returns a list of names of parameters with a certain key_value"""
        if search_list==None:
            search_list=self.members().keys()
        #tag_params=[]#self.members().keys()[:]
        if key_value==None:
            return filter(lambda x: none_value!=self.get_tag(x, key, none_value), search_list)
        return filter(lambda x: key_value==self.get_tag(x, key, none_value), search_list)
        ##print self.members().keys()[key_value==self.get_tag(item, key, none_value)]
        #for item in self.members().keys():#all_params:
        #    if key_value==self.get_tag(item, key, none_value):
        #        tag_params.append(item)
        #return tag_params

#    def get_tag2(self, name, key, none_value=None):
#        """gets tag key of parameter name and returns none_value if tag does not exist. very useful function"""
#        try:
#            return self.get_member(name).metadata[key]
#        except:
#            return none_value

    def set_tag(self, name, **kwargs):
        """sets tag of parameter name using keywords arguments"""
        self.get_member(name).tag(**kwargs)

    def set_all_tags(self, **kwargs):
        """set all parameters tags using set tag"""
        for param in self.all_params:
            self.set_tag(param, **kwargs)

    def func2log(self, name, cmdstr):
        """returns cmd associated with cmdstr in tag and converts it to a log if it isn't already.
          returns None if cmdstr is not in metadata"""
        cmd=self.get_tag(name, cmdstr)
        if not isinstance(cmd, log) and cmd!=None:
            cmd=log(cmd)
            self.set_tag(name, **{cmdstr:cmd})
        return cmd

    def get_run_params(self, name, key, notself=False, none_value=[]):
        """returns the run parameters of get_cmd and set_cmd. Used in GUI"""
        cmd=self.func2log(name, key)
        if cmd==None:
            return none_value
        else:
            run_params=cmd.run_params[:]
            if notself==True:
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
        """retrieves metadata associated with name if key is None. If key specified, returns metadata[key] or None if key is not in metadata"""
        metadata=self.metadata(name) #getattr(type(self), name).metadata
        #if key==None:
        #    return metadata
        if metadata==None:
            return none_value
        return metadata.get(key, none_value)

    def metadata(self, name):
        return self.get_member(str(name)).metadata
            #try:
            #    return metadata[key]
            #except KeyError:
            #    return None

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
        if typer in (Coerced, Typed, Instance):
            typer=type(getattr(self, name))
        return self.get_tag(name, "type", typer)

    def set_value_check(self, name, value):
        """coerces and checks value when setting. This has to be different from getting to allow Enum to map properly. Not working for List?"""
        value=self.coercer(name, value)
        if self.get_type(name)==Enum:
            return self.get_tag(name, 'mapping', {value : value})[value]
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
                     map_val=self.get_tag(name, 'mapping', {value:value})[value], unit=unit))
           elif self.get_type(name)==Dict:
               log_info("Set {instr} {label}".format(instr=self.name, label=label))
           elif self.get_type(name)==Str:
               log_info("Set {instr} {label} to {length} string".format(instr=self.name, label=label, length=len(value)))
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

    #def set_boss(self):
    #    self.boss=master

    def _default_boss(self):
        boss.make_boss()
        return boss
#        boss.BASE_DIR="/Users/thomasaref/Dropbox/Current stuff/TA_software"
#        boss.DIVIDER="/"
#        boss.LOG_NAME="record"
#        boss.FILE_NAME="meas"
#        boss.SETUP_GROUP_NAME="SetUp"
#        boss.SAVE_GROUP_NAME="Measurements"
#        make_log_file(log_path=boss.BASE_DIR+boss.DIVIDER+boss.LOG_NAME+".log", display=boss.display)  #default log file
#        return boss

    def __init__(self, **kwargs):
        """extends __init__ to set boss and add instrument to boss's instrument list.
        Also adds observers for ContainerList parameters so if item in list is changed via some list function other than setattr, notification is still given.
        Finally, sets all Callables to be log decorated if they weren't already."""
        super(Base, self).__init__(**kwargs)
        #self.set_boss()
        if self.name=="":
            self.name="base{}".format(len(self.boss.bases))
        if self.show_base:
            self.boss.bases.append(self)
       # plot_keys=[]
        for key in self.all_params:
            if self.get_type(key)==ContainerList:
                self.observe(key, self.value_changed)
            if self.get_type(key)==Callable:
                func=getattr(self, key)
                if isinstance(func, FunctionType):
                    setattr(self, key, log(func))
            if self.get_type(key) in [Range, FloatRange]:
                self.set_tag(key, low=self.get_member(key).validate_mode[1][0], high=self.get_member(key).validate_mode[1][1])

    def value_changed(self, change):
        """observer for ContainerLists to handle updates not covered by setattr"""
        if change['type'] not in ('create', 'update'):
            self.set_log(change['name'], list(change['value']))

    def add_plot(self):
        self.boss.plot_list.append(Plotter())

    def add_line_plot(self, name):
        xname=self.get_tag(name, 'xdata')
        if xname==None:
            xdata=None
        else:
            xdata=getattr(self, xname)
        self.boss.plot_list[0].add_plot(name, yname=name, ydata=getattr(self, name), xname=xname, xdata=xdata)
        self.boss.plot_list[0].title=self.name
        if xname==None:
            self.boss.plot_list[0].xlabel="# index"
        else:
            self.boss.plot_list[0].xlabel=self.get_tag(xname, "plot_label", xname)
        self.boss.plot_list[0].ylabel=self.get_tag(name, "plot_label", name)

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


if __name__=="__main__":
    #class bt(Base):
    #    df=Int()
    a=Base(name="blah")
    print a.reserved_names
    print a.all_params
    print a.main_params
    print a.boss==boss
    print boss.bases
    print a.get_tag("desc", "bob")
    print a.get_all_tags("private", True, False)
    print a.get_all_tags("private", True, True)
    a.show()
    #print a.metadata("blah")
