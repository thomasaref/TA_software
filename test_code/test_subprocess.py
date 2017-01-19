# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 01:37:36 2016

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.physics.fundamentals import sinc_sq, pi
from taref.core.backbone import get_tag

from atom.api import Atom, Float, Int, Property, observe
from inspect import getmembers

_UPDATE_PREFIX_="_update_"


class A(Atom):
    f0=Float(4.5e9)
    Np=Int(10)
    Ga_0=Float(1)
    f=Float(4.4e9)
    C=Property()
    eta=Float(0.5)
    a=Property().tag(update=["_update_lbda0_update_2"])
    g=Property().tag(update=["_update_a_update_2"])
    vf=Float(3488.0).tag(desc="speed of SAW", unit=" m/s")
    lbda0=Property().tag(update=["_update_f0"])
    Ga_f=Property()

    def get_argnames(self, func_name):
        update_func=getattr(self, func_name)
        var_name=func_name.split(_UPDATE_PREFIX_)[1]
        f=update_func.im_func
        argcount=f.func_code.co_argcount
        argnames=list(f.func_code.co_varnames[0:argcount])
        if "self" in argnames:
            argnames.remove("self")
        return update_func, var_name, argnames
        
    def __init__(self, **kwargs):
        members=self.members()
        updates=[attr[0] for attr in getmembers(self) if attr[0].startswith(_UPDATE_PREFIX_)]
        for func_name in updates:
            update_func, var_name, argnames=self.get_argnames(func_name)
            if var_name in members:
                item=members[var_name]
                if type(item) in (Property,):
                    if item.fget is None:
                        item.getter(self.get_func(argnames, update_func))
                    if item.fset is None:
                        upd_list=get_tag(self, var_name, "update", [])
                        if upd_list!=[]:
                            item.setter(self.set_func(var_name, upd_list))
        super(A, self).__init__(**kwargs)

    def set_func(self, name, update_list):
        upd_funcs, var_names, argnames_list=zip(*[self.get_argnames(func_name) for func_name in update_list])
        for argnames in argnames_list:
            argnames.remove(name)
        def setit(self, value):
            for n, update_func in enumerate(upd_funcs):
                argvalues=[getattr(self, arg) for arg in argnames_list[n]]
                kwargs=dict(zip(argnames_list[n], argvalues))
                kwargs[name]=value
                setattr(self, var_names[n], update_func(**kwargs))
        return setit

    def get_func(self, argnames, update_func):
        def getit(self):
            args= [getattr(self, arg) for arg in argnames]
            return update_func(*args)
        return getit

    def _update_eta(self, a, g):
         return a/(a+g)
      
    def _update_Ct(self, ft, W, epsinf, Np):
        m={"double" : 1.414213562373, "single" : 1.0}[ft]
        return m*W*epsinf*Np

    def _update_lbda0(self, vf, f0):
        return vf/f0

    def _update_f0(self, vf, lbda0):
        return vf/lbda0
 
    @observe("a", "eta", "f0", "lbda0", "g", "Np", "Ga_f", "Ga_0", "C")
    def changer(self, change):
        log_debug(change)
        
    @observe("eta", "ft")
    def set_lbda0_2(self, change):
        self.lbda0=self._update_lbda0_update_2(self.a, self.eta)

#    @eta.getter
#    def get_eta(self):
#        return self._eta
#        
#    @eta.setter
#    def set_eta(self, eta):
#        self._eta=eta
#        self.lbda0=self._update_lbda0_update_2(self.a, self._eta)
#        
    def _update_lbda0_update_2(self, a, eta):
        return a/eta*2.0*2#ft#self.mult        
    
    def _update_g(self, a, eta):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => g=a*(1/eta-1)"""
        return a*(1.0/eta-1.0)
        
    def _update_a(self, eta, lbda0):
        return eta*lbda0/(2.0*2.0)
#
    def _update_a_update_2(self, eta, g):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => a=g*eta/(1-eta)"""
        return g*eta/(1.0-eta)


    def _update_Ga_f(self, Ga_0, Np, f, f0):
        return Ga_0*sinc_sq(Np*pi*(f-f0)/f0)

    #def _update_C(self, Np):
    #    return Np

a=A(a=3e-6)

a.a=5e-6
show(a)
#a.get_member("lbda0").setter(a.set_func("lbda0"))
#a.lbda0=1.0e-6

if 0:
    print a.f0
    print a.a, a.f0
    a.a=0.5e-6
    print a.eta, a.a, a.g, a.f0
    a.eta=0.1
    print a.eta, a.a, a.g 
    a.g=0.5e-6
    print a.eta, a.a, a.g 
    print a.lbda0, a.f0
    
    print a.Ga_f
#print a.C
#print a.Ga_f    

#import subprocess
#from taref.core.tex import read_tex
##subprocess.check_output(["open", "test.pdf"])
#
#lines=read_tex("test.tex")
#for n, line in enumerate(lines):
#    print n, line
#    
#lines[6]="man"
#
#for n, line in enumerate(lines):
#    print n, line
#
#with open("test.tex", "w") as f:
#    f.write("\n".join(lines))
#    
#subprocess.call(["/usr/texbin/pdflatex", "/Users/thomasaref/Documents/TA_software/test.tex"])# "/Users/thomasaref/Documents/TA_software/test.tex"])
#subprocess.call(["open", "/Users/thomasaref/Documents/TA_software/test.pdf"])

#subprocess.check_output(['latexmk', '--pdf' '--interaction=nonstopmode', "test.tex"])
#output = subprocess.Popen(["pdflatex", "test.tex"]).communicate()[0]
#print output