# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 11:36:10 2016

@author: thomasaref
"""

from taref.core.agent import Agent
from taref.physics.fundamentals import (eps0, sqrt, pi, Delta, hbar, e, h, ndarray, array, eig, delete,
                                        sin, sinc_sq, linspace, zeros, absolute, cos, arange)
from taref.core.extra_setup import tagged_property, property_func
from atom.api import Float, Int
from taref.core.universal import Array
from numpy.linalg import eigvalsh, eigvals
from taref.saw.idt import IDT

def unitize(obj, param):
    unit_factor=get_tag(obj, param, "unit_factor")
    if unit_factor is not None:
        return getattr(obj, param)/unit_factor
    unit_func=get_tag(obj, param, "unit_func")
    if unit_func is not None:
        return unit_func.inv(getattr(obj, param))
    return getattr(obj, param)

class Qubit(Agent):
    """Theoretical description of qubit"""

    def latex_table(self, param_list=None):
        if param_list is None:
            param_list=self.main_params
        lt = [[self.name,  r"Value",  r"Expression", r"Comment"],]
        for param in param_list:
            lt.append([get_tag(self, param, "label", param),  get_tag(self, param, format_str, r"{0}").format(unitize(self, param)),
                       get_tag(self, param, "expression", r"{}"), get_tag(self, param, "comment", r"{}")])

              [r"Overlap length, $W$"                    ,  r"{0} $\mu$m".format(qdt.W/1.0e-6)  ],
              [r"finger width, $a_q$"                    ,  r"{0} nm".format(qdt.a/1.0e-9)      ],
              [r"DC Junction Normal Resistance"          ,  r"{0} k$\Omega$".format(qdt.Rn)     ],
              [r"Metallization ratio"                    ,  r"{0}\%".format(qdt.eta)            ],
              [r"Coupling at IDT center frequency"""     ,  r"{0} GHz".format(qdt.G_f0/1.0e9)   ],
              [r"Coupling adjusted by $sinc^2$"            ,  r"{0} GHz".format(qdt.G_f)          ],
              [r"loop width"                             ,  r"{0} um".format(qdt.loop_width)    ],
              [r"loop height"                            ,  r"{0} um".format(qdt.loop_height)   ],
             ]
tx.make_table(qubit_values, r"|p{5 cm}|p{3 cm}|")

tx.add(r"\subsection{IDT values}")
idt_values=[[r"Talking/Listening IDTs"             ,  r"Value"                                 ],
            [r"Finger type"                        ,  r"{0}".format(idt.ft)                    ],
            [r"Number of finger pairs, $N_{p}$"    ,  r"{0}".format(idt.Np)                    ],
            [r"Overlap length, $W$"                ,  r"{0} $\mu$m".format(idt.W/1.0e-6)       ],
            [r"finger width, $a$"                  ,  r"{0} nm".format(idt.a/1.0e-9)           ],
            [r"Metallization ratio"                ,  r"{0}\%".format(idt.eta)                 ]
           ]
tx.make_table(idt_values, r"|p{5 cm}|p{3 cm}|")

tx.add(r"\subsection{Calculated qubit values}")
calc_qubit=[[r"Calculated values qubit"            ,  r"Value"                                     ,  r"Expression"                          , r"Comment"                     ],
            [r"Center frequency"                   ,  r"{0} GHz".format(qdt.f0)                    ,  r"$v/(8a_q)$"                          , r"speed over wavelength"       ],
            [r"Gap $\Delta(0)$"                    ,  r"200e-6 eV"                                 ,  r"$1.764 k_B T_c$"                     , r"BCS"                         ],
            [r"Critical current, $I_c$"            ,  r"{0} nA".format(qdt.Ic/1.0e-9)              ,  r"$\dfrac{\pi \Delta(0)}{2e}$"         , r"Ambegaokar Baratoff formula" ],
            [r"$E_{Jmax}$"                         ,  r"{0} GHz".format(qdt.Ejmax)                 ,  r"$\dfrac{\hbar I_c}{2e R_n}$"         , r"{}"                          ],
            [r"Capacitance from fingers $C_q$"     ,  r"{0} fF".format(qdt.Ct/1.0e-15)             ,  r"$\sqrt{2} W N_{pq} \epsilon_\infty$" , r"Morgan chp 1"                ],
            [r"\(E_c\)"                            ,  r"{0} MHz".format(qdt.Ec)                    ,  r"$\dfrac{e^2}{2 C}$"                  , r"Charging energy"             ],
            [r"Ejmax/Ec"                           ,  r"{0}".format(qdt.EjmaxdivEc)                ,  r"Ejmax/Ec"                            , r"transmon limit"              ],
            [r"Estimated max frequency of qubit"   ,  r"{0} GHz".format(qdt.fq_max)                ,  r"{}"                                  , r"full transmon expression"    ],
            [r"Estimated max frequency of qubit"   ,  r"{0} GHz".format(qdt.fq_max_full)           ,  r"{}"                                  , r"full transmon expression"    ],
            [r"Estimated flux/flux0"               ,  r"{0}".format(qdt.flux_over_flux0)           ,  r"{}"                                  , r"full transmon expression"    ],
            [r"loop area"                          ,  r"{0} $\mu$m$^2$".format(qdt.loop_height)    ,  r"{}"                                  , r"Area"                        ],
            [r"$E_J$"                              ,  r"{0} GHz".format(qdt.Ejmax/1.0e9)           ,  r"$\dfrac{\hbar I_c}{2e R_n}$"         , r"{}"                          ],
            [r"Ej/Ec"                              ,  r"{0}".format(qdt.EjdivEc)                   ,  r"Ej/Ec"                               , r"transmon limit"              ],
            [r"Working frequency"                  ,  r"{0} GHz".format(qdt.fq)                    ,  r"$v/(8a_q)$"                          , r"speed over wavelength"       ],
           ]
tx.make_table(calc_qubit, r"|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|")

tx.add(r"\subsection{Calculated IDT values}")
calc_idt=[[r"Calculated values IDT"          ,  r"Value"                            ,  r"Expression"                          , r"Comment"                ],
          [r"Center frequency"               ,  r"{0} GHz".format(idt.f0)           ,  r"$v/(8a)$"                            , r"speed over wavelength"  ],
          [r"Capacitance from fingers, $C$"  ,  r"{0} fF".format(idt.Ct/1.0e-15)    ,  r"$\sqrt{2} W N_{p} \epsilon_\infty$"  , r"Morgan chp 1"           ],
          [r"$Ga0$"                          ,  r"{0} $\Omega$".format(1.0/idt.Ga_0) ,  r"$\dfrac{1}{G_{a0}}$"                  , r"Electrical impedance"  ],
         ]
          #[r"F width at half max"            ,  r"115"                 ,  r"Ejmax/Ec"                            , r"transmon limit"         ]]

    base_name="qubit"
    #def _default_main_params(self):
    #    return ["ft", "f0", "lbda0", "a", "g", "eta", "Np", "ef", "W", "Ct",
    #            "material", "Dvv", "K2", "vf", "epsinf",
    #            "Rn", "Ic", "Ejmax", "Ej", "Ec", "EjmaxdivEc", "EjdivEc",
    #            "fq", "fq_max", "fq_max_full", "flux_over_flux0", "G_f0", "G_f",
   #             "ng", "Nstates", "EkdivEc"]

    loop_width=Float(1.0e-6).tag(desc="loop width of SQUID", unit="um", format_str=r"{0} $\mu$m")
    loop_height=Float(1.0e-6).tag(desc="loop height of SQUID", unit="um", format_str=r"{0} $\mu$m")

    @tagged_property(desc="Area of SQUID loop", unit="um^2", unit_factor=1.0e-12, format_str=r"{0} $\mu$m$^2$",
                     expression="$width \times height$", comment="Loop width times loop height")
    def loop_area(self, loop_width, loop_height):
        return loop_width*loop_height

    Cq=Float(1.0e-12).tag(desc="shunt capacitance", unit="fF")

    Rn=Float(10.0e3).tag(desc="Normal resistance of SQUID", unit="kOhm")

    @tagged_property(desc="critical current of SQUID", unit="nA")
    def Ic(self, Rn):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Rn

    @Ic.fget.setter
    def _get_Rn(self, Ic):
        """Ic*Rn=pi*Delta/(2.0*e) #Ambegaokar Baratoff formula"""
        return pi*Delta/(2.0*e)/Ic

    @tagged_property(desc="""Max Josephson Energy""", unit="GHz", unit_factor=1.0e9*h)
    def Ejmax(self, Ic):
        """Josephson energy"""
        return hbar*Ic/(2.0*e)

    @Ejmax.fget.setter
    def _get_Ic(self, Ejmax):
        """inverse Josephson energy"""
        return Ejmax*(2.0*e)/hbar

    @tagged_property(desc="Charging Energy", unit="GHz", unit_factor=1.0e9*h)
    def Ec(self, Cq):
        """Charging energy"""
        return e**2/(2.0*Cq)

    @Ec.fget.setter
    def _get_Ejmax(self, Ec, EjmaxdivEc):
        return EjmaxdivEc*Ec

    @tagged_property(desc="Maximum Ej over Ec")
    def EjmaxdivEc(self, Ejmax, Ec):
        return Ejmax/Ec

    flux_over_flux0=Float()

    @tagged_property(unit="GHz", unit_factor=1.0e9*h)
    def Ej(self, Ejmax, flux_over_flux0):
        return Ejmax*absolute(cos(pi*flux_over_flux0))

    @tagged_property(desc="Ej over Ec")
    def EjdivEc(self, Ej, Ec):
        return Ej/Ec

    @tagged_property(unit="GHz", unit_factor=1.0e9*h)
    def fq_max(self, Ejmax, Ec):
        return sqrt(8.0*Ejmax*Ec)

    @tagged_property(unit="GHz", unit_factor=1.0e9*h)
    def fq_max_full(self, Ejmax, Ec):
        return  h*self._get_fq(Ejmax, Ec)

    @tagged_property(desc="""Operating frequency of qubit""", unit="GHz")
    def fq(self, Ej, Ec):
        return self._get_fq(Ej, Ec)

    def _get_fq(self, Ej, Ec):
        E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
        E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
        return (E1-E0)/h

    def _get_Ej(self, fq, Ec):
        """h*fq=sqrt(8.0*Ej*Ec) - Ec"""
        return ((h*fq+Ec)**2)/(8.0*Ec)




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
    t=Qubit()
    t.show()