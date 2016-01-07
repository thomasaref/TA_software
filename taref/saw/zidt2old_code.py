# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 22:02:10 2016

@author: thomasaref
"""

    def get_argnames(self, func_name):
        update_func=getattr(self, func_name)
        var_name=func_name.split(_UPDATE_PREFIX_)[1]
        f=update_func.im_func
        argcount=f.func_code.co_argcount
        argnames=list(f.func_code.co_varnames[0:argcount])
        if "self" in argnames:
            argnames.remove("self")
        f.argnames=argnames
        f.var_name=var_name
        return update_func

#        updates=[attr[0] for attr in getmembers(self) if attr[0].startswith(_UPDATE_PREFIX_)]
#        for func_name in updates:
#            self.get_argnames(func_name)
#        for name, item in self.property_dict.iteritems():
#            if item.fget is None and hasattr(self, "_update_"+name):
#                item.getter(self.get_func(getattr(self, "_update_"+name)))
#            if item.fset is None:
#                upd_list=get_tag(self, name, "update", [])
#                if upd_list!=[]:
#                    item.setter(self.set_func(name, upd_list))

    def set_func(self, name, update_list):
        upd_funcs=[getattr(self, func_name) for func_name in update_list]
        argnames_list=[upd_f.im_func.argnames for upd_f in upd_funcs]
        argnames_list=[[arg for arg in argnames if arg!=name] for argnames in argnames_list]
        var_names=[upd_f.im_func.var_name for upd_f in upd_funcs]
        def setit(self, value):
            for n, update_func in enumerate(upd_funcs):
                argvalues=[getattr(self, arg) for arg in argnames_list[n]]
                kwargs=dict(zip(argnames_list[n], argvalues))
                kwargs[name]=value
                setattr(self, var_names[n], update_func(**kwargs))
        return setit

    def get_func(self, update_func):
        argnames=update_func.im_func.argnames
        prop_names=[name for name in self.property_dict.keys() if name in argnames]
        def getit(self):
            for name in prop_names:
                self.get_member(name).reset(self)
            args= [getattr(self, arg) for arg in argnames]
            return update_func(*args)
        return getit
    #@observe("a", "eta", "f0", "lbda0", "g", "Np", "Ga_f", "Ga_0", "C")
    def changer(self, change):
        log_debug(change)
        if change["type"]=="update":
            for update_name in get_tag(self, change["name"], "update", []):
                update_func=getattr(self, update_name)
                var_name=update_func.im_func.var_name
                argnames=update_func.im_func.argnames
                argvalues=[getattr(self, arg) for arg in argnames]
                setattr(self, var_name, update_func(*argvalues))
        #if change["type"]!="create":
            #for item in self.property_dict.values():
            #    item.reset(self)
#    def set_func(self, name, update_list):
#        upd_funcs=[getattr(self, func_name) for func_name in update_list]
#        argnames_list=[upd_f.im_func.argnames for upd_f in upd_funcs]
#        argnames_list=[[arg for arg in argnames if arg!=name] for argnames in argnames_list]
#        var_names=[upd_f.im_func.var_name for upd_f in upd_funcs]
#        def setit(self, value):
#            for n, update_func in enumerate(upd_funcs):
#                argvalues=[getattr(self, arg) for arg in argnames_list[n]]
#                kwargs=dict(zip(argnames_list[n], argvalues))
#                kwargs[name]=value
#                setattr(self, var_names[n], update_func(**kwargs))
#        return setit

_UPDATE_PREFIX_="_update_"

class property_f(object):
    """A logging wrapper that is compatible with both functions or Callables.
    Auto sets self in the function call to self.obj if it has been set
    for easier use of Callables"""
    def __init__(self, func):
        self.func=func
        self.log=True
        name_list=self.func.func_name.split("_get_")
        if name_list[0]=="":
            self.name=name_list[1]
        else:
            self.name=name_list[0]
        self.run_params=[param for param in get_run_params(func) if param!="self"]
        self.fset_list=[]

    def setter(self, func):
        s_func=property_f(func)
        self.fset_list.append(s_func)
        return s_func

    def fset_maker(self, obj):
        def setit(obj, value):
            for fset in self.fset_list:
                argvalues=[self.param_decider(obj, param, value) 
                                 for param in fset.run_params]
                setattr(obj, fset.name, fset(obj, *argvalues))                
        return setit

    def param_decider(self, obj, param, value):
        if param==self.name:
            return value
        return getattr(obj, param)
        
    def __call__(self, *args, **kwargs):
        """call logs the call if desired and autoinserts kwargs and obj"""
        if self.log:
            log_info(kwargs)
        if self.obj is not None:
            for item in self.run_params:
                if item in kwargs:
                    setattr(self.obj, item, kwargs[item])
                else:
                    value=getattr(self.obj, item)
                    value=set_value_map(self.obj, item, value)
                    kwargs[item]=value
            #do_it_if_needed(obj.chief, f, **kwargs)
            return self.func(self.obj, *args, **kwargs)
        return self.func(*args, **kwargs)

        #for param in self.all_params:
        #    print param, getattr(self, param)

#def get_run_params(f, include_self=False):
#    """returns names of parameters a function will call"""
#    if hasattr(f, "run_params"):
#        argnames=f.run_params
#    else:
#        argcount=f.func_code.co_argcount
#        argnames=list(f.func_code.co_varnames[0:argcount])
#    if not include_self and "self" in argnames:
#        argnames.remove("self")
#    return argnames

#def run_func(obj, name, **kwargs):
#    """runs a function which is an attribute of an object. Auto-includes the obj itself depending on the types of function
#    if kwargs are specified, it will set the attribtues of an object to those values (names need to match).
#    if the object boss has the GUI threadsafe method do_it_if_needed, it will preferentially call that over the function itself"""
#    f=getattr(obj, name)
#    run_params=get_run_params(f)
#    if get_type(obj, name) in (Callable, FunctionType):
#        kwargs["self"]=obj
#    for item in run_params:
#        if item in kwargs:
#            setattr(obj, item, kwargs[item])
#        else:
#            value=getattr(obj, item)
#            value=set_value_map(obj, item, value)
#            kwargs[item]=value
#    do_it_if_needed(obj.chief, f, **kwargs)
#
#def updater(fn):
#    """a decorator to stop infinite recursion. also stores run_params as an attribute"""
#    @wraps(fn)
#    def updfunc(self, change):
#        if not hasattr(updfunc, "callblock"):
#            updfunc.callblock=""
#        if change["name"]!=updfunc.callblock: # and change['type']!='create':
#            updfunc.callblock=change["name"]
#            fn(self, change)
#            updfunc.callblock=""
#    updfunc.run_params=get_run_params(fn)
#    return updfunc

#def log_func(fn):
#    """a decorator that logs when a function is run. also stores run_params as an attribute"""
#    @wraps(fn)
#    def logf(*args, **kwargs):
#        log_info("RAN: {name}".format(name=fn.func_name))
#        fn(*args, **kwargs)
#    logf.run_params=get_run_params(fn, True)
#    return logf

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



#
#    def copy(self):
#        tempbase=type(self)()
#        for name in self.all_params:
#            setattr(tempbase, name, getattr(self, name))
#        for name in self.reserved_names:
#            setattr(tempbase, name, getattr(self, name))
#        return tempbase
#

#def tomobserve(*pairs):
#    obshandle=observe(*pairs)
#    return TomHandler(obshandle, pairs)
#
#from atom.atom import ObserveHandler
#
#class TomHandler(ObserveHandler):
#    def __init__(self, obshandle, pairs):
#        self.inputpairs=pairs
#        self.pairs = obshandle.pairs
#        self.func = obshandle.func
#        self.funcname = obshandle.funcname
#        
#    def __call__(self, func):
#        """ Called to decorate the function."""
#        func=updater(func)
#        func.pairs=self.inputpairs
#        return super(TomHandler, self).__call__(func)


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

