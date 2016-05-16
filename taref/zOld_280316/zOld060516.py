# -*- coding: utf-8 -*-
"""
Created on Fri May  6 16:07:54 2016

@author: thomasaref
"""


#def mult_unit_maker(unit_factor):
#    def mult_unit_func(value):
#        return value*unit_factor
#    return mult_unit_func
#
#def inv_mult_unit_maker(unit_factor):
#    def inv_mult_unit_func(value):
#        return value/unit_factor
#    return inv_mult_unit_func
#
#def dB_maker():
#    return dB
#
#def inv_dB_maker():
#    return inv_dB

#class unit_func(object):
#    def __init__(self, unit="", format_str=None, coercer=float, output_unit=""):
#        self.unit=unit
#        if format_str is None:
#            format_str=r"{0} "+unit
#        else:
#            format_str=r"{0} "+format_str
#        self.format_str=format_str
#        self.coercer=coercer
#        self.output_unit=output_unit
#
#    def __call__(self, value):
#        return self.func(self.coercer(value))
#
#    def inv(self, value):
#        if value is None:
#            return value
#        return self.inv_func(self.coercer(value))
#
#
#class mult_unit(unit_func):
#    def __init__(self, unit_factor=None, unit="", format_str=None, coercer=float, output_unit=""):
#        self.unit_factor=unit_factor
#        super(mult_unit, self).__init__(unit=unit, format_str=format_str, coercer=coercer, output_unit=output_unit)
#
#    def __call__(self, value):
#        if self.unit_factor is None:
#            return value
#        return super(mult_unit, self).__call__(value)
#
#    def inv(self, value):
#        if self.unit_factor is None:
#            return value
#        return super(mult_unit, self).inv(value)
#
#    def func(self, value):
#        return value*self.unit_factor
#
#    def inv_func(self, value):
#        return value/self.unit_factor
#
#class dB_unit(unit_func):
#    def func(self, value):
#        return dB(value)
#
#    def inv_func(self, value):
#        return inv_dB(value)
#
#class inv_dB_unit(unit_func):
#    def func(self, value):
#        return inv_dB(value)
#
#    def inv_func(self, value):
#        return dB(value)
#
#class dBm_unit(mult_unit):
#    def func(self, value):
#        return 0.001*inv_dB_pwr(value)/self.unit_factor
#
#    def inv_func(self, value):
#        return dB_pwr(value*self.unit_factor/0.001)
#
#class inv_dBm_unit(mult_unit):
#    def inv_func(self, value):
#        return 0.001*inv_dB_pwr(value)/self.unit_factor
#
#    def func(self, value):
#        return dB_pwr(value*self.unit_factor/0.001)
#
#def dBm_Float(value=-100.0):
#    unit_f=dBm_unit(unit="dBm", output_unit="mW", unit_factor=0.001)
#    uvalue=unit_f(value)
#    return Float(uvalue).tag(unit="dBm", unit_func=unit_f)
#
#def mW_Float(value=1.0e-10):
#    return Float(value).tag(unit="mW", unit_func=inv_dBm_unit(unit="mW", output_unit="dBm", unit_factor=0.001))



#def generate_unit_dict():
#    PREFIX_DICT={"f":1.0e-15, "p":1.0e-12, "n":1.0e-9, "u":1.0e-6, "m":1.0e-3, "c":1.0e-2, "":1.0,
#           "k":1.0e3, "M":1.0e6, "G":1.0e9, "T" : 1.0e12 }
#
#    unit_dict={"%": mult_unit(unit_factor=1.0/100.0, unit="%", format_str=r"$\%$"),
#               "dB": dB_unit(unit="dB"),
#               "inv_dB": inv_dB_unit(unit="inv dB"),
#               }
#    for unit in ("m", "Hz", "W", "F", "Ohm"):
#        if  unit=="Ohm":
#            unit_format = "$\Omega$"
#        else:
#            unit_format = unit
#        for prefix, unit_factor in PREFIX_DICT.iteritems():
#            if prefix=="u":
#                if unit=="Ohm":
#                    format_str="$\mu \Omega$"
#                else:
#                    format_str="$\mu$"+unit_format
#            else:
#                format_str=prefix+unit_format
#            unit_dict[prefix+unit]= mult_unit(unit_factor=unit_factor, unit=prefix+unit, format_str=format_str)
#    return unit_dict
#
#
#myUNIT_DICT=generate_unit_dict()
##for key in myUNIT_DICT:
##    print myUNIT_DICT[key].unit, myUNIT_DICT[key](1.0), myUNIT_DICT[key].inv(1.0)
#
#def united(obj, name, value=None, inv=False):
#    if value is None:
#        value=getattr(obj, name)
#    unit_func=get_tag(obj, name, "unit_func")
#    if unit_func is None:
#        return value
#    if inv:
#        return unit_func.inv(value)
#    return unit_func(value)
#
#PREFIX_DICT={"f":1.0e-15, "p":1.0e-12, "n":1.0e-9, "u":1.0e-6, "m":1.0e-3, "c":1.0e-2,
#           "k":1.0e3, "M":1.0e6, "G":1.0e9, "T" : 1.0e12 }
#
#
#UNIT_DICT={"n":1.0e-9, "u":1.0e-6, "m":1.0e-3, "c":1.0e-2,
#           "G":1.0e9, "M":1.0e6, "k":1.0e3,
#           "%":1.0/100.0,
#           "nm":1.0e-9, "um":1.0e-6, "mm":1.0e-3, "cm":1.0e-2, "km":1.0e3,
#           "GHz":1.0e9, "MHz":1.0e6, "kHz":1.0e3,
#           "mW" : 1.0e-3,
#           "fF" : 1.0e-15,
#           "kOhm" : 1.0e3
#           #"dB":dB_func(), "inv_dB":inv_dB_func(),
#}

#def get_display(obj, name):
#    disp_unit=get_tag(obj, name, "display_unit")
#    return disp_unit.show_unit(getattr(obj, name)*disp_unit)

class tag_Property(tag_Callable):
    """disposable decorator class that returns a cached Property tagged with kwargs"""
    default_kwargs=dict(cached=True)

    def __call__(self, func):
        cached=self.kwargs.pop("cached")
        return Property(func, cached=cached).tag(**self.kwargs)

def fset_maker(fget):
    """creates set function from list of functions"""
    def setit(obj, value):
        for fset in fget.fset_list:
            setattr(obj, fset.pname, fset(obj, value))
    return setit

def property_func(func, **kwargs):
    new_func=LogFunc(**kwargs)(func)
    new_func.fset_list=[]
    def setter(set_func):
        s_func=LogFunc(**kwargs)(set_func)
        s_func.pname=s_func.func_name.split("_get_")[1]
        new_func.fset_list.append(s_func)
        return s_func
    new_func.setter=setter
    return new_func

class set_Property(Property):
    def fset_maker(self):
        def fset_clt(obj, value):
            for fset in fset_clt.fset_list:
                setattr(obj, fset.pname, fset(obj, value))
        fset_clt.fset_list=[]
        return fset_clt

    def setter(self, func):
        fset=self.fset
        if fset is None:
            fset=super(tom_Property, self).setter(self.fset_maker())
        fset.fset_list.append(func)
        return super(tom_Property, self).setter(fset)

class tagged_property(tag_Property):


    def __call__(self, func=None):
        self.fset=self.fset_maker()
        return super(tagged_property, self).__call__(property_func(func, **self.kwargs))
def fset_maker(fget):
    """creates set function from list of functions"""
    def setit(obj, value):
        for fset in fget.fset_list:
            setattr(obj, fset.pname, fset(obj, value))
    return setit

def dictify_fget(private_param, dicty, key):
    def getit(obj):
        temp=getattr(obj, private_param)
        if temp is None:
            return dicty.get(getattr(obj, key), temp)
        return temp
    return getit

def dictify_fset(private_param):
    def setit(obj, value):
        return value
        #setattr(obj, private_param, value)
        #obj.get_member(param).reset(obj)
    setit.pname=private_param
    return setit

class BackboneAtomMeta(AtomMeta):
    def __new__(meta, name, bases, dct):
        update_dict={} #dict(_name=Unicode().tag(private=True))
        for param, itm in dct.items():
            if isinstance(itm, Property): #hasattr(value, "propify"):
                if itm.metadata is not None:
                    if not itm.metadata.get("private", False):
                        dictify=itm.metadata.get("dictify", False)
                        if dictify:
                            private_param="_"+param
                            update_dict[private_param]=Value().tag(private=True)
                            key=itm.metadata["key"]
                            get_f=LogFunc(**itm.metadata)(dictify_fget(private_param, dictify, key))
                            get_f.fset_list=getattr(itm.fget, "fset_list", [])
                            itm.getter(get_f)
                            set_f=LogFunc(**itm.metadata)(dictify_fset(private_param))
                            itm.fget.fset_list.append(set_f)
                        func_name=param+"_f"
                        update_dict[func_name]=itm.fget
                        if getattr(itm.fget, 'fset_list', [])!= []:
                            itm.setter(fset_maker(itm.fget))
        dct.update(update_dict)
        return AtomMeta.__new__(meta, name, bases, dct)


#def log_func(func, pname=None, threaded=False):
#    """logging decorator for Callables that logs call if tag log!=False"""
#    func_name=func.func_name
#    if pname is None:
#        pname=func_name
#
#    log_message=getattr(func, "log_message", "RAN: {0} {1}")
#    @wraps(func)
#    def new_func(self, *args, **kwargs):
#        """logs the call of an instance method and autoinserts kwargs"""
#        if get_tag(self, pname, "log", False):
#            log_debug(log_message.format(getattr(self, "name", ""), func_name), n=2)
#        if len(args)==0:
#            members=get_all_params(self)#.members().keys()
#            for param in get_run_params(new_func):
#                if param in members:
#                    if param in kwargs:
#                        try:
#                            setattr(self, param, kwargs[param])
#                        except TypeError:
#                            set_tag(self, param, do=kwargs[param])
#                    else:
#                        if param in get_property_names(self):
#                            self.get_member(param).reset(self)
#                        value=getattr(self, param)
#                        value=set_value_map(self, param, value)
#                        kwargs[param]=value
#        if threaded: #doesn't return value from thread
#            names=[thread.name for thread in self.thread_list if pname in thread.name]
#            return self.add_thread("{0} {1}".format(pname, len(names)), func, *((self,)+args), **kwargs)
#        else:
#            return func(self, *args, **kwargs)
#    new_func.pname=pname
#    new_func.run_params=get_run_params(func)
#    return new_func

def call_func(obj, name, **kwargs):
    """calls a func using keyword assignments. If name corresponds to a Property, calls the get func.
    otherwise, if name_mangled func "_get_"+name exists, calls that. Finally calls just the name if these are not the case"""
    if name in get_property_names(obj):
        return obj.get_member(name).fget(obj, **kwargs)
    elif name in get_all_params(obj) and hasattr(obj, "_get_"+name):
        return getattr(obj, "_get_"+name)(obj, **kwargs)
    return getattr(obj, name)(obj, **kwargs)


#
#def property_func(func, **kwargs):
#    new_func=LogFunc(**kwargs)(func)
#    new_func.fset_list=[]
#    def setter(set_func):
#        s_func=LogFunc(**kwargs)(set_func)
#        s_func.pname=s_func.func_name.split("_get_")[1]
#        new_func.fset_list.append(s_func)
#        return s_func
#    new_func.setter=setter
#    return new_func

#class set_Property(Property):
#    def fset_maker(self):
#        def fset_clt(obj, value):
#            for fset in fset_clt.fset_list:
#                setattr(obj, fset.pname, fset(obj, value))
#        fset_clt.fset_list=[]
#        return fset_clt
#
#    def setter(self, func):
#        fset=self.fset
#        if fset is None:
#            fset=super(tom_Property, self).setter(self.fset_maker())
#        fset.fset_list.append(func)
#        return super(tom_Property, self).setter(fset)

#class tagged_property(tag_Property):
#
#
#    def __call__(self, func=None):
#        self.fset=self.fset_maker()
#        return super(tagged_property, self).__call__(property_func(func, **self.kwargs))
#def fset_maker(fget):
#    """creates set function from list of functions"""
#    def setit(obj, value):
#        for fset in fget.fset_list:
#            setattr(obj, fset.pname, fset(obj, value))
#    return setit

#def property_func(func, **kwargs):
#    new_func=LogFunc(**kwargs)(func)
#    new_func.fset_list=[]
#    def setter(set_func):
#        s_func=LogFunc(**kwargs)(set_func)
#        s_func.pname=s_func.func_name.split("_get_")[1]
#        new_func.fset_list.append(s_func)
#        return s_func
#    new_func.setter=setter
#    return new_func
#
#class tagged_property(tag_Property):
#    def __call__(self, func):
#        return super(tagged_property, self).__call__(property_func(func, **self.kwargs))

def dict_property(**kwargs):
    def do_nothing(obj):
        pass
    return tagged_property(**kwargs)(do_nothing)

#class dict_property(tagged_property):
#    def __init__(self, key, dictify, **kwargs):
#        fget=self.dictify_fget(dictify, key)
#
#    def dictify_fget(self, private_param, dicty, key):
#        def getit(obj):
#            temp=getattr(obj, private_param)
#            if temp is None:
#                return dicty.get(getattr(obj, key), temp)
#            return temp
#        return getit
#
#    def dictify_fset(param, private_param):
#        def setit(obj, value):
#            return value
#        setit.pname=private_param
#        return setit


#class dict_Property(tag_Property):
#    def __call__(self, func):
#        new_func=super(dict_property, self).__call__(func)

def Ga_f(Ga_0, Np, f, f0):
    """sinc squared behavior of real part of IDT admittance"""
    return Ga_0*sinc_sq(Np*pi*(f-f0)/f0)

#    def _observe_material(self, change):
#        if self.material=="STquartz":
#            self.epsinf=5.6*eps0
#            self.Dvv=0.06e-2
#            self.vf=3159.0
#        elif self.material=='GaAs':
#            self.epsinf=1.2e-10
#            self.Dvv=0.035e-2
#            self.vf=2900.0
#        elif self.material=='LiNbYZ':
#            self.epsinf=46*eps0
#            self.Dvv=2.4e-2
#            self.vf=3488.0
#        elif self.material=='LiNb128':
#            self.epsinf=56*eps0
#            self.Dvv=2.7e-2
#            self.vf=3979.0
#        elif self.material=='LiNbYZX':
#            self.epsinf=46*eps0
#            self.Dvv=0.8e-2
#            self.vf=3770.0
#        else:
#            print "Material not listed"

#from functools import wraps

#def attr_name(func):
#    """determines parameter name by parsing '_get_'"""
#    name_list=func.func_name.split("_get_")
#    if name_list[0]=="":
#        name=name_list[1]
#    else:
#        name=name_list[0]
#    return name



#class tagged_property(tag_Property):
#    def __call__(self, func):
#        new_func=LogFunc(**self.kwargs)(func)
#        return super(tagged_property, self).__call__(new_func)




#def property_func(func):
#    name_list=func.func_name.split("_get_")
#    if name_list[0]=="":
#        name=name_list[1]
#    else:
#        name=name_list[0]
#    new_func=log_func(func, name)
#    new_func.fset_list=[]
#    def setter(set_func):
#        s_func=property_func(set_func)
#        new_func.fset_list.append(s_func)
#        return s_func
#    new_func.setter=setter
#    return new_func



#def param_decider(obj, value, param, pname):
#    if param==pname:
#        return value
#    return getattr(obj, param)

#def fset_maker(obj, fget, name):
#    def setit(obj, value):
#        for fset in fget.fset_list:
#            argvalues=[param_decider(obj, value, param, name) for param in fset.run_params]
#            setattr(obj, fset.pname, fset(obj, *argvalues))
#    return setit

#def _setup_property_fs(self, param, typer):
#    """sets up property_f's pointing obj at self and setter at functions decorated with param.fget.setter"""
#    if typer==Property:
#        fget =getattr(self.get_member(param), "fget")
#        if hasattr(fget, "fset_list"):
#            if getattr(fget, "fset_list") != []:
#                self.get_member(param).setter(fset_maker(self, fget, param))
#            else:
#                def do_nothing_set(obj, value):
#                    pass
#                self.get_member(param).setter(do_nothing_set)
    #display_unit=get_tag(self, param, "display_unit")
    #if display_unit is not None:# and get_tag(self, param, "unit_factor") is None and get_tag(self, param, "unit_func") is None:
    #    unit_dict=getattr(self, "unit_dict", UNIT_DICT)
    #    if display_unit in unit_dict:
    #        set_tag(self, param, display_unit=unit_dict[display_unit])

#def auto_param(func):
#    @wraps(func)
#    def new_func(self, *args, **kwargs):
#        for param in new_func.run_params[len(args):]:
#            if param not in kwargs:
#                kwargs[param]=getattr(self, param)
#        return func(self, *args, **kwargs)
#    new_func.run_params=get_run_params(func, skip=1)
#    return new_func

import sys

def f_top_finder(fb):
    """A recursive top frame finder"""
    if fb.f_back is None:
        return fb
    return f_top_finder(fb.f_back)

def f_top_limited(fb, n=100):
    """A limited recursion top frame finder"""
    for m in range(n):
        if fb.f_back is None:
            return fb
        fb=fb.f_back
    return fb

def f_top(n=100):
    """returns the top frame after n steps. n defaults to 100"""
    try:
        raise Exception
    except:
        fb=exc_info()[2].tb_frame.f_back
    return f_top_limited(fb, n)

def msg(*args, **kwargs):
    """log msg that accepts multiple args with file info"""
    n=kwargs.pop("n", 1)
    fb=f_top(n)
    return "{0} {1} {2}: {3}".format(fb.f_lineno, basename(fb.f_code.co_filename),
              fb.f_code.co_name, ", ".join([str(arg) for arg in args]))

    def write(self, in_str):
        self.log_str+=in_str

    def redirect_stdout(self, visible):
        if visible:
            sys.stdout=self
            sys.stderr=self
        else:
            sys.stdout=sys.__stdout__ #old_stdout
            sys.stderr=sys.__stderr__


            fb=f_top()
            if hasattr(chief_cls, "code_window"):
                file_location=fb.f_code.co_filename
                with open(file_location) as f:
                    showfile=f.read()
                view=chief_cls.code_window
                view.show_code.text=showfile
                view.show()
                view.send_to_back()
                if not show_code:
                    view.hide()

            locals_dict=dict(([(key, item) for key, item in fb.f_locals.items() if not key.startswith("_")]))
            view=chief_cls.interactive_window
            view.input_dict=locals_dict
            view.show()
            view.send_to_back()
            if not show_ipy:
                view.hide()
