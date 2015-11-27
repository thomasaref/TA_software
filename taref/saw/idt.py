# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 11:08:19 2015

@author: thomasaref
"""
from taref.core.agent import Spy#, Agent
from taref.physics.fundamentals import (eps0, sqrt, pi, Delta, hbar, e, h, ndarray, array, eig, delete,
                                        sin, sinc_sq, linspace, zeros, absolute, cos, arange)
from taref.core.log import log_debug
from atom.api import Enum, Int, Float, observe, Bool, Property, Str, List, Range, Typed, Coerced

def Array(shape=1):
    return Coerced(ndarray, args=(shape,), coercer=array)
    
class IDT(Spy):
    """Theoretical description of IDT"""    
    @property
    def base_name(self):
        return "idt"
    
    def _default_main_params(self):
        return ["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct", 
                "material", "Dvv", "K2", "vf", "epsinf"]

    ft=Enum("double", "single").tag(desc="finger type of IDT", label="Finger type")

    @property
    def mult(self):
        return {"double" : 2.0, "single" : 1.0}[self.ft]

    Np=Int(7).tag(desc="number of finger pairs. this should be at least 1", low=1)
    
    ef=Int(0).tag(desc="number of extra fingers to compensate for edge effect.",
                    label="# of extra fingers")
    
    a=Float().tag(desc="width of fingers (um).",
                  unit="um",
                  update=["_update_lbda0_update_2", "_update_g", "_update_f0"])

    W=Float(25.0e-6).tag(desc="height of finger.", unit="um")

    g=Float().tag(desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz",
                  unit="um",
                  update=["_update_a_update_2", "_update_lbda0_update_2", "_update_f0"])

    eta=Float(0.5).tag(desc="metalization ratio",
                       update=["_update_a", "_update_g"])

    epsinf=Float(46*eps0).tag(desc="Capacitance of single finger pair per unit length")

    Dvv=Float(2.4e-2).tag(desc="coupling strength: K^2/2",
                      unit="%")

    K2=Float().tag(desc="coupling strength",
                      unit="%")

    vf=Float(3488.0).tag(desc="speed of SAW", unit=" m/s")

    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')

    f0=Float(5.0e9).tag(label="f0",
                unit="GHz",
                desc="Center frequency",
                reference="",
                update=["_update_lbda0", "_update_a", "_update_g"])

    lbda0=Float().tag(label="lbda0",
                unit="um",
                desc="Center wavelength",
                reference="")

    Ct=Float().tag(label="Ct",
                   unit="F",
                   desc="Total capacitance of IDT",
                   reference="Morgan page 16/145")

    #@Property
    #def p(self):
    #    return self.a+self.g
    #p.tag(desc="periodicity. this should be twice width for 50% metallization")
    
    def _update_K2(self, Dvv):
        return Dvv*2.0

    def _update_Dvv(self, K2):
        return K2/2.0
        
    def _update_eta(self, a, g):
         return a/(a+g)
      
    def _update_Ct(self, ft, W, epsinf, Np):
        m={"double" : 1.414213562373, "single" : 1.0}[ft]
        return m*W*epsinf*Np

    def _update_lbda0(self, vf, f0):
        return vf/f0
        
    def _update_lbda0_update_2(self, a, eta, ft):
        return a/eta*2.0*self.mult        
    
    def _update_g(self, a, eta):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => g=a*(1/eta-1)"""
        return a*(1.0/eta-1.0)

    def _update_a(self, eta, lbda0, ft):
        return eta*lbda0/(2.0*self.mult)

    def _update_a_update_2(self, eta, g):
        """eta=a/(a+g)
           => a=(a+g)*eta
           => (1-eta)*a=g*eta
           => a=g*eta/(1-eta)"""
        return g*eta/(1.0-eta)
    
    def _update_f0(self, vf, lbda0):
        return vf/lbda0

    def _observe_material(self, change):
        if self.material=="STquartz":
            self.epsinf=5.6*eps0
            self.Dvv=0.06e-2
            self.vf=3159.0
        elif self.material=='GaAs':
            self.epsinf=1.2e-10
            self.Dvv=0.035e-2
            self.vf=2900.0
        elif self.material=='LiNbYZ':
            self.epsinf=46*eps0
            self.Dvv=2.4e-2
            self.vf=3488.0
        elif self.material=='LiNb128':
            self.epsinf=56*eps0
            self.Dvv=2.7e-2
            self.vf=3979.0
        elif self.material=='LiNbYZX':
            self.epsinf=46*eps0
            self.Dvv=0.8e-2
            self.vf=3770.0
        else:
            print "Material not listed"

    def _default_a(self):
        return self.get_default("a")            

    def _default_g(self):
        return self.get_default("g")            

    def _default_lbda0(self):
        return self.get_default("lbda0")            

    def _default_K2(self):
        return self.get_default("K2")            

    def _default_Ct(self):
        return self.get_default("Ct")            

    def _default_material(self):
        return 'LiNbYZ' #'GaAs'
from numpy.linalg import eigvalsh, eigvals

class QDT(IDT):
    """Theoretical description of IDT and qubit, called QDT"""    

    def _default_main_params(self):
        return ["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct", 
                "material", "Dvv", "K2", "vf", "epsinf", 
                "Rn", "Ic", "Ejmax", "Ej", "Ec", "EjmaxdivEc", "EjdivEc",
                "fq", "fq_max", "fq_max_full", "flux_over_flux0", "G_f0", "G_f", 
                "ng", "Nstates", "EkdivEc"]

    @property
    def base_name(self):
        return "qdt"

    Ic=Float().tag(desc="critical current of SQUID",
                   unit="nA")
    
    Rn=Float(10.0e3).tag(desc="Normal resistance of SQUID",
                         unit="kOhm")
    
    Ejmax=Float().tag(desc="""Max Josephson Energy""",
                       unit="GHz", unit_factor=1.0e9*h)
                       
    Ec=Float(1.0).tag(desc="""Charging Energy""", 
                      unit="GHz", unit_factor=1.0e9*h,
                      update=["_update_fq_max", "_update_fq_max_full", "_update_fq",
                              "_update_Ej_update_2", '_update_EjdivEc', '_update_EjmaxdivEc'])

    fq=Float().tag(desc="""Operating frequency of qubit""",
                           unit="GHz")

    EjmaxdivEc=Float().tag(desc="Maximum Ej over Ec")

    EjdivEc=Float().tag(desc="Ej over Ec")

    fq_max=Float().tag(unit="GHz", unit_factor=1.0e9*h)

    fq_max_full=Float().tag(unit="GHz", unit_factor=1.0e9*h)

    Ej=Float().tag(unit="GHz", unit_factor=1.0e9*h)

    flux_over_flux0=Float()
    
    def _update_EjmaxdivEc(self, Ejmax, Ec):
        return Ejmax/Ec
        
    def _update_EjdivEc(self, Ej, Ec):
        return Ej/Ec
    
    def _update_fq_max(self, Ejmax, Ec):
        return sqrt(8.0*Ejmax*Ec)
        
    def _update_fq_max_full(self, Ejmax, Ec):
        return  h*self._update_fq(Ejmax, Ec) 

    def _update_Ej(self, Ejmax, flux_over_flux0):
        return Ejmax*absolute(cos(pi*flux_over_flux0))
    
    def _update_Ej_update_2(self, fq, Ec):
        """h*fq=sqrt(8.0*Ej*Ec) - Ec"""
        return ((h*fq+Ec)**2)/(8.0*Ec)
        
    def _update_fq(self, Ej, Ec):
        E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
        E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
        return (E1-E0)/h
    
    def _update_Ic(self, Rn):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Rn

    def _update_Rn(self, Ic):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Ic

    def _update_Ejmax(self, Ic):
        """Josephson energy"""
        return hbar*Ic/(2.0*e)

    def _update_Ec(self, Ct):
        """Charging energy"""
        return e**2/(2.0*Ct)

    def _default_Ec(self):
        return self.get_default("Ec")            

    def _default_Ej(self):
        return self.get_default("Ej")            

    def _default_Ejmax(self):
        return self.get_default("Ejmax")            

    def _default_Ic(self):
        return self.get_default("Ic")            

    def _default_fq(self):
        return self.get_default("fq")            

    def _default_fq_max(self):
        return self.get_default("fq_max")            

    def _default_fq_max_full(self):
        return self.get_default("fq_max_full")            

    def _default_EjmaxdivEc(self):
        return self.get_default("EjmaxdivEc")            

    def _default_EjdivEc(self):
        return self.get_default("EjdivEc")            


    G_f0=Float().tag(desc="""Coupling at IDT center frequency""", unit="GHz")
    G_f=Float().tag(desc="""Coupling adjusted by sinc^2""", unit="GHz")                    
    
    def _update_G_f0(self, Np, K2, f0):
        return 0.45*Np*K2*f0

    def _update_G_f(self, G_f0, Np, fq, f0):
        return G_f0*sinc_sq(Np*pi*(fq-f0)/f0)
        
    def _default_G_f0(self):
        return self.get_default("G_f0")
        
    def _default_G_f(self):
        return self.get_default("G_f")

    ng=Float(0.5).tag(desc="charge on gate line")
    Nstates=Int(50).tag(desc="number of states to include in mathieu approximation. More states is better approximation")
    order=Int(3)
    EkdivEc=Array().tag(unit=" Ec")

    def indiv_EkdivEc(self, ng, Ec, Ej, Nstates, order):
        NL=2*Nstates+1
        A=zeros((NL, NL))
        for b in range(0,NL):
            A[b, b]=4.0*Ec*(b-Nstates-a)**2
            if b!=NL-1:
                A[b, b+1]= -Ej/2.0
            if b!=0:
                A[b, b-1]= -Ej/2.0
        w,v=eig(A)
        print w, v
        #for n in range(order):
            
        

    def update_EkdivEc(self, ng, Ec, Ej, Nstates, order):
        """calculates transmon energy level with N states (more states is better approximation)
        effectively solves the mathieu equation but for fractional inputs (which doesn't work in scipy.special.mathieu_a)"""

#        if type(ng) not in (int, float):
#            d=zeros((order, len(ng)))
#        elif type(Ec) not in (int, float):
#            d=zeros((order, len(Ec)))
#        elif type(Ej) not in (int, float):
#            d=zeros((order, len(Ej)))
        if type(ng) in (int, float):
            ng=array([ng])
        d1=[]
        d2=[]
        d3=[]
        Ej=Ej/Ec            
        Ec=1.0#/4.0
        for a in ng:
            NL=2*Nstates+1
            A=zeros((NL, NL))
            for b in range(0,NL):
                A[b, b]=4.0*Ec*(b-Nstates-a)**2
                if b!=NL-1:
                    A[b, b+1]= -Ej/2.0
                if b!=0:
                    A[b, b-1]= -Ej/2.0
            #w,v=eig(A)
            w=eigvalsh(A)
            d=w[0:order]
#            d1.append(min(w))#/h*1e-9)
#            w=delete(w, w.argmin())
#            d2.append(min(w))#/h*1e-9)
#            w=delete(w, w.argmin())
#            d3.append(min(w))#/h*1e-9)
        
        return array([array(d1), array(d2), array(d3)]).transpose()

    def sweepEc():
        Ecarr=Ej/EjoverEc
        E01a=sqrt(8*Ej*Ecarr)-Ecarr
        data=[]
        for Ec in Ecarr: 
            d1, d2, d3= EkdivEc(ng=ng, Ec=Ec, Ej=Ej, N=50)
            E12=d3[0]-d2[0]
            E01=d2[0]-d1[0]
            anharm2=(E12-E01)#/E01
            data.append(anharm2)
        Ctr=e**2/(2.0*Ecarr*h*1e9)
        return E01a, Ctr, data, d1, d2, d3
        
    def get_plot_data(self, zname, **kwargs):
         """pass in an appropriate kwarg to get zdata for the zname variable back"""
         arg=kwargs.keys()[0]
         func_name=[upd for upd in self.get_tag(arg, "update") if upd.split("_update_")[1]==zname][0]
         func=getattr(self, func_name)
         f=func.im_func
         for name in f.argnames:
             if name not in kwargs:
                 kwargs[name]=getattr(self, name)
         return func(**kwargs)

    def plot_data(self, zname, **kwargs):
         """pass in an appropriate kwarg to get zdata for the zname variable back"""
         xmult=kwargs.pop("xmult", 1.0)
         zmult=kwargs.pop("zmult", 1.0)  
         label=kwargs.pop("label", "")
         
         if "xlim" in kwargs:
             xlim(kwargs["xlim"])

         if "ylim" in kwargs:
             ylim(kwargs["ylim"])

         zunit=self.get_tag(zname, "unit")
         zunit_factor=self.get_tag(zname, "unit_factor", 1.0)
         
         if zunit is None:
             zlabel_str=zname
         else:
             zlabel_str="{0} [{1}]".format(zname, zunit)

         ylabel(kwargs.pop("ylabel", zlabel_str))

         add_legend=kwargs.pop("legend", False)
             
         title_str=kwargs.pop("title", None)
         xlabel_str=kwargs.pop("xlabel", None)

         if len(kwargs)==1:
             xname, xdata=kwargs.popitem()
             zdata=self.get_plot_data(zname, **{xname:xdata})
             xunit=self.get_tag(xname, "unit")
             xunit_factor=self.get_tag(xname, "unit_factor", 1.0)
         else:
             xname="#"
             xdata=arange(len(getattr(self, zname)))
             xunit=None
             xunit_factor=self.get_tag(xname, "unit_factor", 1.0)
             
         if xlabel_str is None:
             if xunit is None:
                 xlabel_str=xname
             else:
                 xlabel_str="{0} [{1}]".format(xname, xunit)
         xlabel(xlabel_str)
         
         if title_str is None:
             title_str="{0} vs {1}".format(zname, xname)
         title(title_str)
         print xdata.shape, zdata.shape
         plot(xdata*xunit_factor*xmult, zdata*zunit_factor*zmult, label=label)
         
         if add_legend:
             legend()
        
if __name__=="__main__":
    from matplotlib.pyplot import plot, show, xlabel, ylabel, title, xlim, ylim, legend

    #a=IDT()
    #a=IDT(Np=9)
    a=QDT()
    
    a.Rn=5.9e3
    a.Np=5
    a.W=7.0e-6
    a.fq=4.5e9
    
    print a.get_metadata("Ct")
    #a.Np=9
    #a.f0=4.500001e9
    #print a._update_K2.argnames
    for param in a.all_params:
        print param, a.get_tag(param, "update")
    #print a.get_plot_data("EkdivEc", ng=0.5)
    if 0:
        a.plot_data("EkdivEc", Ej=linspace(0.0, 1.0*a.Ejmax, 100))
        show()
        a.plot_data("EkdivEc", ng=linspace(0.0, 1.0, 100))
        show()
    
    #a.f0=4.500001e9
    #a.f0=4.500001e9

    #print a.search_update("a")
    #a.G_f0=1.0
    #fq=linspace(4.0e9, 11.0e9, 2001)
    #G_f=a.get_plot_data("G_f", fq=fq)
    #plot(fq, G_f)
   # a.plot_data("G_f", fq=linspace(4.0e9, 11.0e9, 2001),
   #              legend=True, label="G f",
   #             ylabel="G_F [Hz]", xmult=1/1.0e9, zmult=1/1.0e9)

    #show()
    
    #a.f=linspace(4.0e9, 11.0e9, 2001)
    #a.observe(("G_f0", "Np", "f", "f0"), a._update_G_f)
    #print dir(a.test_func.im_func)
    
    #print a.f
    #print a.get_tag("f", "sweep")
    #a.plotty("G_f", f=linspace(4.0e9, 11.0e9, 2001))
    #show()
    #a.Rn=(7.62e3+7.96e3)/2.0
    #f=
#    G=zeros(frq.shape)
#    from numpy import shape
#    print frq.shape
#    print shape(frq)
#    print shape(G)
#    for n, f in enumerate(frq):
#        a.f=f
#        G[n]=a.G_f
    #print a._update_Ic.pairs
    #f=a.get_tag("f", "sweep")
    #plot(f/1.0e9, a.G_f_func(f=f))
    #show()

    a.show()

#from scipy.constants import epsilon_0 as eps0
#from numpy import sqrt

#class IDT(EBL_Base):
#    df=Enum("single", "double").tag(desc="'double' for double fingered, 'single' for single fingered. defaults to double fingered")
#    Np=Int(36).tag(desc="number of finger pairs. this should be at least 1 and defaults to 36.")
#    ef=Int(0).tag(desc="number of extra fingers to compensate for edge effect. Defaults to 0")
#    a=Float(0.096).tag(unit="um", desc="width of fingers (um). same as gap generally. Adjusting relative to gap is equivalent to adjusting the bias in Beamer")
#    gap=Float(0.096).tag(unit="um", desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz")
#    offset=Float(0.5).tag(unit="um", desc="gap between electrode and end of finger. The vertical offset of the fingers. Setting this to zero produces a shorted reflector")
#    W=Float(25.5).tag(unit="um", desc="height of finger")
#    hbox=Float(20.0).tag(desc="height of electrode box")
#    wbox=Float(30.0).tag(desc="width of electrode box. Setting to 0.0 (default) makes it autoscaling so it matches the width of the IDT")
#
#    epsinf=Float()
#    Dvv=Float()
#    v=Float()
#    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')
#
#    def _observe_material(self, change):
#        if self.material=="STquartz":
#            self.epsinf=5.6*eps0
#            self.Dvv=0.06e-2
#            self.v=3159.0
#        elif self.material=='GaAs':
#            self.epsinf=1.2e-10
#            self.Dvv=0.035e-2
#            self.v=2900.0
#        elif self.material=='LiNbYZ':
#            self.epsinf=46*eps0
#            self.Dvv=2.4e-2
#            self.v=3488.0
#        elif self.material=='LiNb128':
#            self.epsinf=56*eps0
#            self.Dvv=2.7e-2
#            self.v=3979.0
#        elif self.material=='LiNbYZX':
#            self.epsinf=46*eps0
#            self.Dvv=0.8e-2
#            self.v=3770.0
#        else:
#            log_warning("Material not listed")
#
#    f0=Float().tag(label="f0",
#                unit="GHz",
#                desc="Center frequency",
#                reference="")
#
#    @observe('w', 'v', 'gap', 'df')
#    def _get_f0(self, change):
#        v,a, g=self.v, self.a*1e-6, self.gap*1e-6
#        p=g+a
#        if self.df:
#            lbda0=4*p
#        else:
#            lbda0=2*p
#        self.f0=v/lbda0/1.0e9
#
#
#    Ct=Property().tag(label="Ct",
#                   unit="F",
#                   desc="Total capacitance of IDT",
#                   reference="Morgan page 16/145")
#    #@observe('epsinf', 'h', 'Np', 'df')
#    def _get_Ct(self):
#        W, epsinf, Np=self.h*1e-6, self.epsinf, self.Np
#        if self.df=="double":
#            return sqrt(2.0)*W*epsinf*Np
#        return W*epsinf*Np
#
#    def _default_material(self):
#        return 'LiNbYZ' #'GaAs'