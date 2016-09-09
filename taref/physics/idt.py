# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 01:07:15 2016

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.physics.fundamentals import sinc_sq, pi, eps0
from taref.physics.legendre import lgf, lgf_arr#, lgf_fixed
from taref.core.agent import Agent
from atom.api import Float, Int, Enum, Value, Property, Typed
from taref.core.api import private_property, log_callable, get_tag, SProperty, log_func, t_property, s_property, sqze, Complex, Array, tag_callable
from numpy import arange, linspace, sqrt, imag, real, sin, cos, interp, array, matrix, eye, absolute, exp, ones, squeeze, log10, fft, float64, int64, cumsum
#from matplotlib.pyplot import plot, show, xlabel, ylabel, title, xlim, ylim, legend
from numpy.linalg import inv
from scipy.signal import hilbert
from taref.plotter.api import line, Plotter, scatter
from taref.physics.surface_charge import Rho
from enaml import imports
with imports():
    from taref.physics.idt_e import IDTView


class IDT(Rho):
    """Theoretical description of IDT"""
    base_name="IDT"

    def _default_f(self):
        """default f is 0.01Hz off from f0"""
        return self.f0-0.01

    Ga0_mult=SProperty().tag(desc="single: $2.87=1.694^2$, double: $3.11=(1.247 \sqrt{2})^2$", expression=r"$c_{Ga}(f)$", label=r"$G_a$ multiplier")
    @Ga0_mult.getter
    def _get_Ga0_mult(self, f, f0, ft_mult, eta, epsinf, ft):
        alpha=self._get_alpha(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf)
        if ft=="single":
            return alpha**2
        return (alpha*2.0*cos(pi*f/(4.0*f0)))**2

    couple_mult=SProperty().tag(desc="single: 0.71775. double: 0.54995, f dependent", label="coupling multiplier", expression=r"$c_g(f)$")
    @couple_mult.getter
    def _get_couple_mult(self, f, f0, ft_mult, eta, epsinf, Ct_mult):
        Ga0_mult=self._get_Ga0_mult(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf)
        return Ga0_mult/(4.0*Ct_mult)

    couple_factor=SProperty().tag(unit="GHz", label="Qubit coupling ($f$) (no sinc)", expression=r"$\Gamma/2\pi \approx c_g(f) f_0 K^2 N_p$", desc="frequency dependent")
    @couple_factor.getter
    def _get_couple_factor(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np):
        """coupling for one positive finger as function of frequency"""
        couple_mult=self._get_couple_mult(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult)
        return couple_mult*f0*K2*Np

    couple_factor0=SProperty().tag(unit="GHz", label="Qubit coupling ($f_0$)", expression=r"$\Gamma/2\pi \approx c_g(f_0) f_0 K^2 N_p$" )
    @couple_factor0.getter
    def _get_couple_factor0(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np):
        """coupling at center frequency, in Hz (2 pi removed)"""
        return self._get_couple_factor(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)

    Np=Float(9).tag(desc="\# of finger pairs", low=0.5, expression=r"$N_p$", label="\# of finger pairs")

    ef=Int(0).tag(desc="for edge effect compensation",
                    label="\# of extra fingers", low=0)

    W=Float(25.0e-6).tag(desc="IDT width", unit="um", label="IDT width")

    Ct=SProperty().tag(unit="fF", label="IDT capacitance", expression=r"$C_t$", desc="Total capacitance of IDT", reference="Morgan page 16/145")
    @Ct.getter
    def _get_C(self, epsinf, Ct_mult, W, Np):
        """Morgan page 16, 145"""
        return Ct_mult*W*epsinf*Np

    @Ct.setter
    def _get_epsinf(self, Ct, Ct_mult, W, Np):
        """reversing capacitance to extract eps infinity"""
        return Ct/(Ct_mult*W*Np)

    Ga0=SProperty().tag(desc="Conductance at center frequency", expression=r"$G_{a0}$", label="Center conductance")
    @Ga0.getter
    def _get_Ga0(self, f0, ft_mult, eta, epsinf, ft, W, Dvv, Np):
        """Ga0 from morgan"""
        Ga0_mult=self._get_Ga0_mult(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, ft=ft)
        return Ga0_mult*2.0*pi*f0*epsinf*W*Dvv*(Np**2)

    X=SProperty().tag(label="relative frequency", expression=r"$X=N_p \pi (f-f_0)/f_0$")
    @X.getter
    def _get_X(self, Np, f, f0):
        """standard normalized frequency dependence"""
        return Np*pi*(f-f0)/f0

    couple_type=Enum("sinc sq", "giant atom", "df giant atom", "full expr", "full sum")

    coupling=SProperty().tag(desc="""Coupling adjusted by sinc sq""", unit="GHz", expression=r"$\Gamma(f)/2 \pi$", label="full qubit coupling")
    @coupling.getter
    def _get_coupling(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np):
        if self.couple_type=="full sum" or self.S_type=="RAM":
            return self.get_fix("coupling", f)
        gX=self._get_X(Np=Np, f=f, f0=f0)
        gamma=self._get_couple_factor(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        if self.couple_type=="full expr":
            return gamma*((1.0/Np)*sin(gX)/sin(gX/Np))**2
        gamma0=self._get_couple_factor(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        if self.couple_type=="giant atom":
            return gamma0*(1.0/Np*sin(gX)/sin(gX/Np))**2
        elif self.couple_type=="df giant atom":
            return gamma0*(sqrt(2.0)*cos(pi*f/(4*f0))*1.0/Np*sin(gX)/sin(gX/Np))**2
        return gamma0*(sin(gX)/gX)**2.0

    #@log_callable()
    def fixed_reset(self):
        """resets fixed properties in proper order"""
        super(IDT, self).fixed_reset()
        self.get_member("fixed_P").reset(self)
        self.get_member("fixed_X").reset(self)
        self.get_member("fixed_Asum").reset(self)
        self.get_member("fixed_coupling").reset(self)
        self.get_member("fixed_Lamb_shift").reset(self)
        self.get_member("fixed_Ga").reset(self)
        self.get_member("fixed_Ba").reset(self)
        self.get_member("fixed_S").reset(self)

    @private_property
    def fixed_X(self):
        return self._get_X(f=self.fixed_freq)

    @private_property
    def fixed_w(self):
        return 2.0*pi*self.fixed_freq

    def get_fix(self, name, f):
        return interp(f, self.fixed_freq, getattr(self, "fixed_"+name))

    @private_property
    def fixed_coupling(self):
        if self.S_type=="RAM":
            return self.fixed_P[1]/(2.0*self.Ct)/(2.0*pi)
        gamma0=self.f0*self.K2*self.Np/(4*self.Ct_mult)
        if self.couple_type=="full sum":
            return gamma0*(self.fixed_alpha)**2*absolute(self.fixed_Asum)**2
        f, X, Np=self.fixed_freq, self.fixed_X, self.Np
        gamma=self._get_couple_factor(f=f)
        if self.couple_type=="full expr":
            return gamma*((1.0/Np)*sin(X)/sin(X/Np))**2
        gamma0=self._get_couple_factor(f=f0)
        if self.couple_type=="giant atom":
            return gamma0*(1.0/Np*sin(X)/sin(X/Np))**2
        elif self.couple_type=="df giant atom":
            return gamma0*(sqrt(2.0)*cos(pi*f/(4*f0))*1.0/Np*sin(X)/sin(X/Np))**2
        return gamma0*(sin(X)/X)**2.0

    dloss1=Float(0.0)
    dloss2=Float(0.0)

    #propagation_loss=SProperty()
    #@propagation_loss.getter
    #def _get_propagation_loss(self, f, f0, dloss1, dloss2):
    #    return exp(-f/f0*dloss1-dloss2*(f/f0)**2)

    @t_property(sub=True)
    def polarity(self, Np, ft):
        if ft=="single":
            return arange(int(Np))+0.5
        return array(sqze(zip(arange(Np)+0.5, arange(Np)+0.75)))

    @t_property(sub=True)
    def g_arr(self, polarity):
        return ones(len(polarity))

    Asum=SProperty().tag(sub=True)
    @Asum.getter
    def _get_Asum(self, f, f0, Np, dloss1, dloss2, g_arr, polarity):
        return 1.0/Np*array([sum([g_arr[i]*exp(2.0j*pi*frq/f0*n-frq/f0*dloss1*n-n*dloss2*(frq/f0)**2)
               for i, n in enumerate(polarity)]) for frq in f])

    @private_property
    def fixed_Asum(self):
        return self._get_Asum(f=self.fixed_freq)

    @private_property
    def fixed_Lamb_shift(self):
        if self.S_type=="RAM":
            return -self.fixed_P[2]/(2.0*self.Ct)/(2.0*pi)
        if self.Lamb_shift_type=="formula":
            X, Np=self.fixed_X, self.Np
            gamma0=self._get_couple_factor(f=f0)
            if self.couple_type=="sinc^2":
                return -gamma0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
            if self.couple_type=="giant atom":
                return gamma0*(1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
        return imag(hilbert(self.fixed_coupling))

    max_coupling=SProperty().tag(desc="""Coupling at IDT center frequency""", unit="GHz",
                     label="Coupling at center frequency", tex_str=r"$\gamma_{f0}$")
    @max_coupling.getter
    def _get_max_coupling(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np):
        return self._get_coupling(f=f0+0.001, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)

    Lamb_shift_type=Enum("hilbert", "formula")

    Lamb_shift=SProperty().tag(desc="""Lamb shift""", unit="GHz", expression=r"$B_a/\omega C$", label="Lamb shift")
    @Lamb_shift.getter
    def _get_Lamb_shift(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np):
        """returns Lamb shift"""
        if self.couple_type=="full sum" or self.S_type=="RAM":
            return self.get_fix("Lamb_shift", f)
        if self.Lamb_shift_type=="formula":
            gamma0=self._get_couple_factor(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
            gX=self._get_X(Np=Np, f=f, f0=f0)
            if self.couple_type=="sinc^2":
                return -gamma0*(sin(2.0*gX)-2.0*gX)/(2.0*gX**2.0)
            if self.couple_type=="giant atom":
                return gamma0*(1.0/Np)**2*2*(Np*sin(2*gX/Np)-sin(2*gX))/(2*(1-cos(2*gX/Np)))
        cpl=self._get_coupling(f=self.fixed_freq, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        yp=imag(hilbert(cpl))
        return interp(f, self.fixed_freq, yp)

    #ZL=Float(50.0)
    #ZL_imag=Float(0.0)
    #GL=Float(1/50.0)
    dL=Float(0.0)
    YL=Complex(1.0/50.0)

    S_type=Enum("simple", "simpleP", "RAM")

    @private_property
    def fixed_S(self):
        if self.S_type=="simple":
            return self._get_simple_S(f=self.fixed_freq)
        P=self.fixed_P[0]
        return self.PtoS(*P, YL=self.YL)

    simple_S=SProperty().tag(sub=True)
    @simple_S.getter
    def _get_simple_S(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np, Ct, YL, dL, vf, L_IDT):
        Ga=self._get_Ga(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        Ba=self._get_Ba(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        w=2*pi*f
        GL=real(YL)
        k=2*pi*f/vf
        jkL=1.0j*k*L_IDT
        P33plusYL=Ga+1.0j*Ba+1.0j*w*Ct-1.0j/w*dL+YL
        S11=S22=-Ga/P33plusYL*exp(-jkL)
        S12=S21=exp(-jkL)+S11
        S13=S23=S32=S31=1.0j*sqrt(2.0*Ga*GL)/P33plusYL*exp(-jkL/2.0)
        S33=(YL-Ga+1.0j*Ba+1.0j*w*Ct-1.0j/w*dL)/P33plusYL
        return (S11, S12, S13,
                S21, S22, S23,
                S31, S32, S33)

    simple_P=SProperty().tag(sub=True)
    @simple_P.getter
    def _get_simple_P(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np, Ct, dL, vf, L_IDT):
        Ga=self._get_Ga(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        Ba=self._get_Ba(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        w=2*pi*f
        k=2*pi*f/vf
        jkL=1.0j*k*L_IDT
        P11=P22=0.0
        P12=P21=exp(-jkL)
        P13=P23= -1.0j*sqrt(Ga/2.0)
        P31=P32=-2.0*P13
        P33=Ga+1.0j*Ba+1.0j*w*Ct-1.0j/w*dL
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32, P33), Ga, Ba

    def PtoS(self, P11, P12, P13,
             P21, P22, P23,
             P31, P32, P33, YL=1/50.0):
         YLplusP33=YL+P33
         sqrtYL=sqrt(YL)
         S11=P11-P13*P31/YLplusP33
         S12=P12-P13*P32/YLplusP33
         S13=2.0*sqrtYL*P13/YLplusP33
         S21=P21-P23*P31/YLplusP33
         S22=P22-P23*P32/YLplusP33
         S23=-P31*sqrtYL*P23/YLplusP33
         S31=-P31*sqrtYL/YLplusP33
         S32=-P32*sqrtYL/YL+P33
         S33=(YL-P33)/YLplusP33
         return (S11, S12, S13,
                 S21, S22, S23,
                 S31, S32, S33)

    rs=Complex()

    ts=SProperty()
    @ts.getter
    def _get_ts(self, rs):
        return sqrt(1.0-absolute(rs)**2)

    Gs=SProperty().tag(desc="Inglebrinsten's approximation of $\Gamma_S$ (Morgan)", expression=r"$\Gamma_S \approx (\Delta v/v)/\epsilon_\infty$")
    @Gs.getter
    def _get_Gs(self, Dvv, epsinf):
        return Dvv/epsinf

    Y0=SProperty().tag(desc="Datta's characteristic SAW impedance", expression=r"$Y_0=\pi f W \epsilon_\infty / (\Delta v/v)$", label="Characteristic impedance")
    @Y0.getter
    def _get_Y0(self, f, Dvv, epsinf, W):
        return pi*f*W*epsinf/Dvv

    L_IDT=SProperty().tag(desc="length of IDT", unit="um", expression=r"$L_{IDT}=N_{IDT}p$", label="IDT length")
    @L_IDT.getter
    def _get_L_IDT(self, N_IDT, p):
        return N_IDT*p

    N_IDT=SProperty().tag(desc="total number of IDT fingers", label="Total IDT fingers", expression=r"$N_{IDT}=2 c_{ft} N_p$")
    @N_IDT.getter
    def _get_N_IDT(self, ft_mult, Np):
        return 2*ft_mult*Np#+ft_mult*(Np+1)

    def _get_RAM_P_one_f(self, f, Dvv, epsinf, W, vf,  rs, p, N_IDT, alpha, ft, Np, f0, dloss1, dloss2):
        Y0=self._get_Y0(f=f, Dvv=Dvv, epsinf=epsinf, W=W)
        k=2*pi*f/vf-1.0j*(f/f0*dloss1+dloss2*(f/f0)**2)
        ts = sqrt(1.0-absolute(rs)**2)
        A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
                           [-rs,             exp(1.0j*k*p)]])#.astype(complex128)
        AN=A**int(N_IDT)
        AN11, AN12, AN21, AN22= AN[0,0], AN[0,1], AN[1,0], AN[1,1]
        P11=-AN21/AN22
        P21=AN11-AN12*AN21/AN22
        P12=1.0/AN22
        P22=AN12/AN22
        D = -1.0j*alpha*Dvv*sqrt(Y0)
        B = matrix([(1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0), (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)])

        if ft=="single":
            P32=D*(B*A*inv(eye(2)-A**2)*(eye(2)-A**(2*int(Np)))*matrix([[0],
                                                                   [1.0/AN[1,1]]]))[0] #geometric series
        else:
            P32=D*(B*(A**2+A**3)*inv(eye(2)-A**4)*(eye(2)-A**(4*int(Np)))*matrix([[0],
                                                                          [1.0/AN[1,1]]]))[0] #geometric series
        P31=P32
        P13=P23=-P31/2.0
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32)



    @log_func
    def _get_RAM_P(self, W, rs, Np, vf, Dvv, epsinf, Ct, p, N_IDT, ft, f0, dloss1, dloss2):
        frq, alpha=self.fixed_freq, self.fixed_alpha
        print "start P"
        P=[self._get_RAM_P_one_f(f=f, Dvv=Dvv, epsinf=epsinf, W=W, vf=vf, rs=rs, p=p,
                                 N_IDT=N_IDT, alpha=alpha[i], ft=ft, Np=Np, f0=f0, dloss1=dloss1, dloss2=dloss2) for i, f in enumerate(frq)]
        print "P_done"

        (P11, P12, P13,
         P21, P22, P23,
         P31, P32)=[array(P_ele) for P_ele in zip(*P)]
        print "P_done 2"
        Ga=squeeze(2.0*absolute(P13)**2)
        Ba=-imag(hilbert(Ga))
        P33=Ga+1.0j*Ba+2.0j*pi*f*Ct
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32, P33), Ga, Ba


#    @log_func
#    def _get_RAM_P(self, f, W, rs, Np, vf, Dvv, epsinf, alpha, C, p, N_IDT, ft):
#        """returns A^N, the matrix representing mechanical reflections and transmission"""
#        #rho=alpha*Dvv #epsinf
#        Y0=self._get_Y0(f=f, Dvv=Dvv, epsinf=epsinf, W=W)
#        #N=2*Np+2*(Np+1)
##        lbda0=vf/f0
##        p=lbda0/4.0 #2*80.0e-9
#        k=2*pi*f/vf
#        ts = sqrt(1-absolute(rs)**2)
#        A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
#                           [-rs,             exp(1.0j*k*p)]])#.astype(complex128)
#        AN=A**int(N_IDT)
#        AN11, AN12, AN21, AN22= AN[0,0], AN[1,0], AN[0,1], AN[1,1]
#        P11=-AN21/AN22
#        P21=AN11-AN12*AN21/AN22
#        P12=1.0/AN22
#        P22=AN12/AN22
#        D = -1.0j*alpha*Dvv*sqrt(Y0)
#        B = matrix([(1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0), (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)])
#
#        if ft=="single":
#            P32=D*(B*A*inv(eye(2)-A**2)*(eye(2)-A**(Np+1))*matrix([[0],
#                                                                   [1.0/AN[1,1]]]))[0] #geometric series
#        else:
#            P32=D*(B*(A**2+A**3)*inv(eye(2)-A**4)*(eye(2)-A**(2*Np+2))*matrix([[0],
#                                                                          [1.0/AN[1,1]]]))[0] #geometric series
#            P32=D*(B*(A**2+A**3)*inv(eye(2)-A**4)*(eye(2)-A**(2*Np+2))*matrix([[0],
#                                                                          [1.0/AN[1,1]]]))[0] #geometric series
#        P31=P32
#        P13=P23=-P31/2.0
#        Ga=2.0*absolute(P13)**2
#        Ba=imag(hilbert(Ga))
#        P33=Ga+1.0j*Ba+2.0j*pi*f*C
#        return (P11, P12, P13,
#                P21, P22, P23,
#                P31, P32, P33), Ga, Ba

    @private_property
    def fixed_P(self):
        if self.S_type=="RAM":

            return self._get_RAM_P()
        return self._get_simple_P(f=self.fixed_freq)

    Ga=SProperty().tag(desc="Ga adjusted for frequency f")
    @Ga.getter
    def _get_Ga(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np, Ct):
        gamma=self._get_coupling(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        return gamma*2*Ct*2*pi

    @private_property
    def fixed_Ga(self):
        return self.fixed_P[1]
        return self._get_Ga(f=self.fixed_freq)

    Ba=SProperty()
    @Ba.getter
    def _get_Ba(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np, Ct):
        ls=self._get_Lamb_shift(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
        return -ls*2*Ct*2*pi

    @private_property
    def fixed_Ba(self):
        return self.fixed_P[2]
        return self._get_Ba(f=self.fixed_freq)

    @private_property
    def view_window(self):
        return IDTView(agent=self)

#from functools import wraps
#
#class idt_plot(tag_callable):
#    def __call__(self, func):
#        @wraps(func)
#        def new_plot(self, *args, **kwargs):
#            self.idt=kwargs.pop("idt", self.idt)
#            if self.idt is None:
#                self.idt=IDT()
#            return func(self, *args, **kwargs)
#        return super(idt_plot, self).__call__(new_plot)

#def idt_process(kwargs):
#    idt=kwargs.pop("idt", None)
#    if idt is None:
#        return IDT()
#    return idt
def metallization_couple(pl="metalization", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.eta=0.5
    #idt.ft="single"
    idt.couple_type="full sum"
    idt.fixed_reset()
    pl=line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)[0]
    idt.eta=0.6
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.6", color="red", linewidth=0.3, label="0.6", **kwargs)
    idt.eta=0.4
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.4", color="green", linewidth=0.3, label="0.4", **kwargs)
    idt.eta=0.5
    return pl
#metallization_couple()#.show()
def metallization_Lamb(pl="metalization", **kwargs):
    idt=idt_process(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.eta=0.5
    #idt.ft="single"
    idt.couple_type="full sum"
    idt.fixed_reset()
    pl=line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)[0]
    idt.eta=0.6
    idt.fixed_reset()
    #line(idt.fixed_freq/idt.f0, idt.fixed_Lamb_shift/idt.max_coupling, plotter=pl, linewidth=0.3, color="purple")
    line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.6", color="red", linewidth=0.3, label="0.6", **kwargs)
    idt.eta=0.4
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.4", color="green", linewidth=0.3, label="0.4", **kwargs)
    idt.eta=0.5
    return pl
#metallization_Lamb().show()

def center_coupling_vs_eta(pl="f0_vs_eta", **kwargs):
    idt=idt_process(kwargs)
    eta=linspace(0.0, 1.0, 100)
    idt.ft="single"
    #idt.N_legendre=1000
    alpha=idt._get_alpha(f=idt.f0, eta=eta, N_legendre=1000)
    pl=line(eta, alpha, plotter=pl)[0]
    alpha=idt._get_alpha(f=3*idt.f0, eta=eta, N_legendre=1000)
    line(eta, alpha, plotter=pl, color="red")
    alpha=idt._get_alpha(f=5*idt.f0, eta=eta, N_legendre=1000)
    line(eta, alpha, plotter=pl, color="green")
    return pl #line(eta, idt._get_alpha(f=3*idt.f0, eta=eta))[0]

#center_coupling_vs_eta().show()
@IDT.add_func
def couple_comparison(pl="couple_compare", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    #idt.Np=21
    #idt.ft="single"
    #idt.rs=-0.05j
    #idt.dloss2=0.1*5e6
    #idt.eta=0.7

    idt.S_type="RAM"
    pl=line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="cyan", linewidth=0.3, label=idt.couple_type, **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()
    idt.couple_type="sinc^2"
    pl=line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, linewidth=0.3, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="df giant atom"
    line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="green", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, (idt._get_coupling(frq)), plotter=pl, color="black", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full sum"
    line(frq/idt.f0, (idt._get_coupling(frq)), plotter=pl, color="purple", linewidth=0.3, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling/max coupling (dB)"
    #pl.set_ylim(-30, 1.0)
    pl.legend()
    return pl

def fix_couple_comparison(pl="fix couple", **kwargs):
    idt=idt_process(kwargs)
    idt.couple_type="sinc^2"
    idt.fixed_reset()
    frq=linspace(0e9, 10e9, 10000)
    pl, pf=line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, linewidth=0.3, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="df giant atom"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="green", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full expr"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="black", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full sum"
    idt.fixed_reset()
    line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, color="purple", linewidth=0.3, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling/max coupling (dB)"
    pl.set_ylim(-30, 1.0)
    pl.legend()
    return pl
@IDT.add_func
def Lamb_shift_comparison(pl="ls_comp", **kwargs):
    idt=IDT.process_kwargs(kwargs)

    #idt.rs=-0.01j
    #idt.dloss2=0.1*1e6
    #idt.eta=0.4
    frq=linspace(0e9, 10e9, 10000)

    idt.S_type="RAM"
    #print idt.fixed_Lamb_shift
    #print imag(hilbert(idt.fixed_coupling))
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="cyan", linewidth=0.3, label=idt.couple_type, **kwargs)
    #pl.show()
    idt.S_type="simple"
    idt.fixed_reset()

    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc^2"
    #idt=IDT(Lamb_shift_type="formula", couple_type="sinc^2")
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, linewidth=0.3, label="sinc^2", **kwargs)
    #a=IDT(Lamb_shift_type="formula", couple_type="giant atom")
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    #a=IDT(Lamb_shift_type="hilbert", couple_type="sinc^2")
    idt.Lamb_shift_type="hilbert"
    idt.couple_type="sinc^2"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="green", linewidth=0.3, label="h(sinc^2)")
    #a=IDT(Lamb_shift_type="hilbert", couple_type="giant atom")
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="black", linewidth=0.3, label="h(giant atom)")
    idt.couple_type="full sum"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="purple", linewidth=0.3, label="h(full sum)")

    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift/max coupling"
    pl.set_ylim(-1e9, 1e9)
    pl.legend()

    #line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl

def Lamb_shift_check(pl="ls_check", **kwargs):
    idt=idt_process(kwargs)
    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc^2"
    frq=linspace(0e9, 10e9, 10000)
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, linewidth=0.3, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="red", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="df giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="green", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="black", linewidth=0.3, label=idt.couple_type)
    idt.couple_type="full sum"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="purple", linewidth=0.3, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift/max coupling (dB)"
    pl.set_ylim(-1.0, 1.0)
    pl.legend()

    #line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl

def formula_comparison(pl=None, **kwargs):
    a=IDT()
    frq=linspace(3e9, 7e9, 10000)
    print a._get_coupling(frq)
    print a.max_coupling
    pl, pf=line(frq, a._get_coupling(frq)/a.max_coupling, plotter=pl, linewidth=1.0, **kwargs)
    line(frq, a._get_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="red", linewidth=1.0)
    #line(frq, coup, color="purple", plotter=pl, linewidth=0.3)
    line(frq, a._get_full_coupling(frq)/a.max_coupling, plotter=pl, color="green", linewidth=0.3)
    line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl
if 0:
    idt=IDT()
    element_factor_plot(idt=idt)#.show()

    Lamb_shift_comparison(idt=idt)

    couple_comparison(idt=idt)#.show()

    fix_couple_comparison(idt=idt)#.show()

    Lamb_shift_check(idt=idt).show()

#formula_comparison()#.show()

#element_factor_plot(idt=idt).show()
if __name__=="__main__":
    #a=IDT(dloss1=0.0, dloss2=0.0, eta=0.6, ft="double")
    a=IDT(material='LiNbYZ',
          ft="double",
          a=80.0e-9, #f0=5.35e9,
          Np=9,
          #Rn=3780.0, #(3570.0+4000.0)/2.0, Ejmax=h*44.0e9,
          W=25.0e-6,
          eta=0.5,)
          #flux_factor=0.515, #0.2945, #0.52,
          #voltage=1.21,
          #offset=-0.07)
    #print a.fixed_P
    a.fixed_reset()
    a.S_type="RAM"
    Lamb_shift_comparison()#.show()
    couple_comparison().show()
    #print a.fixed_P
    #print squeeze(a.fixed_coupling)
    a.show()
    a.f=a.f0
    print a.fixed_polarity
    print a.alpha
    print a.fixed_element_factor
    print a._get_element_factor(a.f0)
    from scipy.signal import hilbert
    from numpy import imag, real, sin, cos, exp, array, absolute


    frq=linspace(1e9, 10e9, 10000)

    X=a._get_X(f=frq)
    Np=a.Np
    f0=a.f0

    if 0:
        def Asum(N, k1=0.0, k2=0.0):
            return array([sum([exp(2.0j*pi*f/f0*n-f/f0*k1-k2*(f/f0)**2) for n in range(N)]) for f in frq])

        def Asum2(M):
            return array([sum([exp(2j*pi*M*f/f0)*exp(2j*pi*f/f0*m) for m in range(-M, M+1)]) for f in frq])

        def Asum3(M, k=1.0):
            return array([sum([exp(2j*pi*f/f0*m) for m in range(-M, M+1)]) for f in frq])

        def Asum4(M):
            return array([sum([2*cos(2*pi*f/f0*m) for m in range(0, M+1)]) for f in frq])-1

        def Asum5(M, g=0.9, g2=1.0):
            return array([g*2*cos(2*pi*f/f0*M) for f in frq])+array([g2*2*cos(2*pi*f/f0*(M-1)) for f in frq])+Asum4(M-2)

        def Asum6(g=1.0):
            return array([(g*exp(-2j*pi*f/f0*4)+exp(-2j*pi*f/f0*3)+exp(-2j*pi*f/f0*2)+exp(-2j*pi*f/f0*1)+1.0
            +exp(2j*pi*f/f0*1)+exp(2j*pi*f/f0*2)+exp(2j*pi*f/f0*3)+g*exp(2j*pi*f/f0*4)) for f in frq])

        def Asum7(g=1.0):
            return array([(g+exp(2j*pi*f/f0*1)+exp(2j*pi*f/f0*2)+exp(2j*pi*f/f0*3)+exp(2j*pi*f/f0*4)
            +exp(2j*pi*f/f0*5)+exp(2j*pi*f/f0*6)+exp(2j*pi*f/f0*7)+g*exp(2j*pi*f/f0*8)) for f in frq])

        A=Asum(9, k1=0.05, k2=0.05)
        A2=Asum2(4)
        A3=Asum3(4)
        A4=Asum4(4)
        A5=Asum5(4, 1.2, 1.0)
        A6=Asum6(0.5)
        A7=Asum7(0.5)

        pl=Plotter()
        #line(frq/1e9, real(A), plotter=pl)
        #line(frq/1e9, imag(A), plotter=pl, color="red")

        #line(frq/1e9, real(A2), plotter=pl, color="green", linewidth=0.5)
        #line(frq/1e9, imag(A2), plotter=pl, color="black", linewidth=0.5)

        line(frq/1e9, sin(pi*9*frq/f0)/sin(pi*frq/f0), plotter=pl)

        line(frq/1e9, real(A3), plotter=pl, color="green", linewidth=0.5)
        line(frq/1e9, imag(A3), plotter=pl, color="black", linewidth=0.5)

        line(frq/1e9, A4, plotter=pl, color="red", linewidth=0.5)
        #line(frq/1e9, A5, plotter=pl, color="purple", linewidth=0.5)
        line(frq/1e9, real(A6), plotter=pl, color="darkgray", linewidth=0.5)
        line(frq/1e9, imag(A6), plotter=pl, color="darkgray", linewidth=0.5)

        #pl.show()
        pl=Plotter()

        line(frq/1e9, 1/81.0*absolute(A)**2, plotter=pl, color="black")
        #line(frq/1e9, 1/81.0*absolute(sin(pi*9*frq/f0)/sin(pi*frq/f0))**2, plotter=pl, color="green", linewidth=0.4)
        #line(frq/1e9, 1/81.0*absolute(A5)**2, plotter=pl, color="blue", linewidth=0.5)
        line(frq/1e9, 1/81.0*absolute(A6)**2, plotter=pl, color="red", linewidth=0.5)
        line(frq/1e9, 1/81.0*absolute(A7)**2, plotter=pl, color="purple", linewidth=0.5)

        #line(frq/1e9, 1/9.0*absolute(A6), plotter=pl, color="red", linewidth=0.5)

        #line(frq/1e9, 1/9.0*absolute(A7), plotter=pl, color="purple", linewidth=0.5)

        pl.show()

    frq=linspace(0, 40e9, 10000)

    X=a._get_X(f=frq)
    Np=a.Np
    f0=a.f0

    #coup=(sqrt(2)*cos(pi*frq/(4*f0))*(1.0/Np)*sin(X)/sin(X/Np))**2
    coup=(sin(X)/X)**2

    #coup=(1.0/Np*sin(X)/sin(X/Np))**2


    element_factor_plot(a)
    pl=Plotter()
    line(frq, a._get_coupling(frq)/a.max_coupling, plotter=pl, linewidth=1.0)
    line(frq, a._get_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="red", linewidth=1.0)
    line(frq, coup, color="purple", plotter=pl, linewidth=0.3)
    line(frq, a._get_full_coupling(frq)/a.max_coupling/1.247**2/2, plotter=pl, color="green", linewidth=0.3)
    line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling/1.247**2/2, plotter=pl, color="black", linewidth=0.3)

    #hb=hilbert(coup) #a._get_coupling(frq))
    #line(frq, real(hb), plotter=pl, color="green", linewidth=0.3)
    #line(frq, imag(hb), plotter=pl, color="black", linewidth=0.3)
    #Baa= (1+cos(X/(4*Np)))*(1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
    Baa=-(sin(2.0*X)-2.0*X)/(2.0*X**2)
    #Baa= (1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
    line(frq, Baa, plotter=pl, color="cyan", linewidth=0.3)

    pl.show()

    b=IDT(ft="single")
    a.ft_mult=5
    print a.mu_mult, a.ft_mult, b.mu_mult, b.ft_mult
    print a.couple_mult, b.couple_mult
    a.ft="single"
    a.ft_mult=None
    print a.mu_mult, a.ft_mult, b.mu_mult, b.ft_mult
    print a.couple_mult, b.couple_mult

    print a.epsinf, a.C
    a.epsinf=4e-10
    print a.C
    a.C=7.1e-14
    print a.epsinf, a.C

    print a._get_C(W=35)



    #log_debug(a.K2, b.K2)
    #a.Dvv=5
    #a.K2=4
    #for name in a.all_params:
    #    print name, getattr(a, name)
    #a.a=90e-9
    #for name in a.all_params:
    #    print name, getattr(a, name)

    #print a._get_Dvv(4)
    #print a.K2_f(2)
    #log_debug(a.get_member("K2").fget.fset_list)
    #log_debug(a.get_member("K2").fset(a, 3))
    #log_debug(a.get_member("K2").fset)

    #print a.K2, b.K2
#    for param in a.all_params:
#        print get_tag(a, param, "unit")
        #print a.call_func("eta", a=0.2e-6, g=0.8e-6)#, vf=array([500.0, 600.0]), lbda0=array([0.5e-6, 0.6e-6]))
        #a.plot_data("f0", lbda0=linspace(0.1e-6, 1.0e-6, 10000))
        #print a.get_tag("lbda0", "unit_factor")
    a.show()
    if 0:
        print a.K2, a.Dvv
        #print dir(a.get_member("K2").fget.fset)
        a.K2=5
        a.Dvv=5
        print a.K2
        shower(a)
        #print a.K2, a.Dvv
        #print a.K2, a.Dvv


    if 0:
        print a.property_dict
        print a.get_member("p").fget()#.func_code.co_varnames#(a, 1, 1)
        #print a.p()
        #a.eta=0.6
        print a.p
        a.a=5e-6
        print a.p
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