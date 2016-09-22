# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 01:07:15 2016

@author: thomasaref
"""

from taref.core.log import log_debug
from taref.physics.fundamentals import pi
from atom.api import Float, Int, Enum
from taref.core.api import private_property, log_callable, get_tag, SProperty, log_func, t_property, s_property, sqze, Complex, Array, tag_callable
from numpy import arange, linspace, sqrt, imag, real, sin, cos, interp, array, matrix, eye, absolute, exp, log, ones, squeeze, log10, fft, float64, int64, cumsum
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

    Y0_type=Enum("formula", "center")
    df_type=Enum("formula", "center")
    mus_type=Enum("formula", "center")
    Ga_type=Enum("sinc", "giant atom", "full sum")
    Ba_type=Enum("hilbert", "formula")
    rs_type=Enum("formula", "constant")


    def _default_fixed_freq_max(self):
        return 200.0*self.f0

    def _default_f(self):
        """default f is 0.01Hz off from f0"""
        return self.f0-0.01

    Np=Float(9).tag(desc="\# of finger pairs", low=0.5, expression=r"$N_p$", label="\# of finger pairs")

    ef=Int(0).tag(desc="for edge effect compensation",
                    label="\# of extra fingers", low=0)

    W=Float(25.0e-6).tag(desc="IDT width", unit="um", label="IDT width")

    Ct=SProperty().tag(unit="fF", label="IDT capacitance", expression=r"$C_t$", desc="Total capacitance of IDT", reference="Morgan page 16/145")
    @Ct.getter
    def _get_Ct(self, epsinf, Ct_mult, W, Np):
        """Morgan page 16, 145"""
        return Ct_mult*W*epsinf*Np

    @Ct.setter
    def _get_epsinf(self, Ct, Ct_mult, W, Np):
        """reversing capacitance to extract eps infinity"""
        return Ct/(Ct_mult*W*Np)

    Ga0_approx=SProperty().tag(desc="Conductance at center frequency", expression=r"$G_{a0} = c_{Ga0} \omega_0 \epsilon_\infty W N_p^2 \Delta v/v$", label="Center conductance")
    @Ga0_approx.getter
    def _get_Ga0_approx(self, f0, epsinf, ft, W, Dvv, Np):
        """Ga0 from morgan"""
        Ga0_mult={"single" : 2.872, "double" : 3.111}[ft]
        return Ga0_mult*2.0*pi*f0*epsinf*W*Dvv*(Np**2)

    X=SProperty().tag(label="relative frequency", expression=r"$X=N_p \pi (f-f_0)/f_0$")
    @X.getter
    def _get_X(self, Np, f, f0):
        """standard normalized frequency dependence"""
        return Np*pi*(f-f0)/f0

    @log_func
    def sinc(self, f, f0, Np):
        X=Np*pi*(f-f0)/f0
        return sin(X)/X

    @log_func
    def sinc_sq_ls(self, f, f0, Np):
        X=Np*pi*(f-f0)/f0
        return -(sin(2.0*X)-2.0*X)/(2.0*X**2.0)

    @log_func
    def giant_atom(self, f, f0, Np):
        X=Np*pi*(f-f0)/f0
        return 1.0/Np*sin(X)/sin(X/Np)

    @log_func
    def giant_atom_ls(self, f, f0, Np):
        X=Np*pi*(f-f0)/f0
        return (1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))

    def hilbert_ls(self, cpl):
        return imag(hilbert(cpl))

    @log_func
    def df_corr(self, f, f0):
        return sqrt(2.0)*cos(pi*f/(4*f0))

    mus=SProperty().tag(desc="Datta voltage coefficient", expression=r"$\mu=j \alpha \Delta v/v$", label="Voltage coeffecient (one finger)")
    @mus.getter
    def _get_mus(self, f, f0, ft_mult, eta, epsinf, Dvv):
        alpha=self._get_alpha(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf)
        return 1.0j*alpha*Dvv

    mus0=SProperty().tag(desc="Datta voltage coefficient", expression=r"$\mu_0=j \alpha_0 \Delta v/v$", label="Voltage coeffecient (center frequency, one finger)")
    @mus0.getter
    def _get_mus0(self, f0, ft_mult, eta, epsinf, Dvv):
        return self._get_mus(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Dvv=Dvv)

    Y0=SProperty().tag(desc="Datta's characteristic SAW impedance", expression=r"$Y_0=\pi f W \epsilon_\infty / (\Delta v/v)$", label="Characteristic impedance")
    @Y0.getter
    def _get_Y0(self, f, Dvv, epsinf, W):
        return pi*f*W*epsinf/Dvv

    Y00=SProperty().tag(desc="Datta's characteristic SAW impedance", expression=r"$Y_0=\pi f_0 W \epsilon_\infty / (\Delta v/v)$", label="Characteristic impedance (center frequency)")
    @Y00.getter
    def _get_Y00(self, f0, Dvv, epsinf, W):
        return self._get_Y0(f=f0, Dvv=Dvv, epsinf=epsinf, W=W) #pi*f0*W*epsinf/Dvv

    Ga=SProperty().tag(desc="Ga adjusted for frequency f")
    @Ga.getter
    def _get_Ga(self, f, f0, ft_mult, eta, epsinf, Dvv, Np, W):
        if self.S_type=="RAM":
            return self.get_fix("Ga", f)

        if self.Y0_type=="center":
            Y0=self._get_Y00(f0=f0, Dvv=Dvv, epsinf=epsinf, W=W)
        else:
            Y0=self._get_Y0(f=f, Dvv=Dvv, epsinf=epsinf, W=W)

        if self.mus_type=="center":
            mus=self._get_mus0(f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Dvv=Dvv)
        else:
            mus=self._get_mus(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Dvv=Dvv)

        if self.df_type=="center" or self.ft=="single":
            df_corr=1.0
        else:
            df_corr=self.df_corr(f=f, f0=f0)
        if self.ft=="double":
            df_corr*=sqrt(2.0)

        if self.Ga_type=="sinc":
            cpl_form=Np*self.sinc(f=f, f0=f0, Np=Np)
        elif self.Ga_type=="giant atom":
            cpl_form=Np*self.giant_atom(f=f, f0=f0, Np=Np)

        if self.Ga_type=="full sum":
            mu=mus*self._get_Asum(f=f, f0=f0, Np=Np)
        else:
            mu=mus*df_corr*cpl_form

        return 2.0*Y0*absolute(mu)**2

    Ga0=SProperty().tag(desc="Ga (center frequency)")
    @Ga0.getter
    def _get_Ga0(self, f0, Np, W, Dvv, epsinf, eta, ft_mult):
        return self._get_Ga(f=f0+0.001, f0=f0, Np=Np, W=W, Dvv=Dvv, epsinf=epsinf, eta=eta, ft_mult=ft_mult)

    @private_property
    def fixed_Ga(self):
        return self.fixed_P[1]
        #return self._get_Ga(f=self.fixed_freq)

    Ba=SProperty()
    @Ba.getter
    def _get_Ba(self, f, f0, ft_mult, eta, epsinf, W, Dvv, Np):
        if self.Ga_type=="full sum" or self.S_type=="RAM":
            return self.get_fix("Ba", f)
        if self.Ba_type=="formula":
            Ga0=self._get_Ga0(f0=f0, Np=Np, W=W, Dvv=Dvv, epsinf=epsinf, eta=eta, ft_mult=ft_mult)
            if self.Ga_type=="sinc":
                return -Ga0*self.sinc_sq_ls(f=f, f0=f0, Np=Np) #(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
            if self.Ga_type=="giant atom":
                return -Ga0*self.giant_atom_ls(f=f, f0=f0, Np=Np) #(1.0/Np)**2*2*(Np*sin(2*gX/Np)-sin(2*gX))/(2*(1-cos(2*gX/Np)))
        Ga=self._get_Ga(f=self.fixed_freq, f0=f0, Np=Np, W=W, Dvv=Dvv, epsinf=epsinf, eta=eta, ft_mult=ft_mult)
        yp=-imag(hilbert(Ga))
        return interp(f, self.fixed_freq, yp)

    @private_property
    def fixed_Ba(self):
        return self.fixed_P[2]
        #return self._get_Ba(f=self.fixed_freq)

    @private_property
    def fixed_P(self):
        if self.S_type=="RAM":
            return self._get_RAM_P()
        return self._get_simple_P(f=self.fixed_freq)

    simple_P=SProperty().tag(sub=True)
    @simple_P.getter
    def _get_simple_P(self, f, f0, ft_mult, eta, epsinf, W, Dvv, Np, Ct, dL, vf, L_IDT):
        Ga=self._get_Ga(f=f, f0=f0, Np=Np, W=W, Dvv=Dvv, epsinf=epsinf, eta=eta, ft_mult=ft_mult)
        Ba=self._get_Ba(f=f, f0=f0, Np=Np, W=W, Dvv=Dvv, epsinf=epsinf, eta=eta, ft_mult=ft_mult)
        w=2*pi*f
        k=2*pi*f/vf
        jkL=1.0j*k*L_IDT
        P11=P22=0.0
        P12=P21=exp(-jkL)
        P13=P23= 1.0j*sqrt(Ga/2.0)*exp(-jkL/2.0)
        P31=P32=-2.0*P13
        P33=Ga+1.0j*Ba+1.0j*w*Ct-1.0j/w*dL
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32, P33), Ga, Ba

    coupling=SProperty().tag(desc="""Coupling adjusted by sinc sq""", unit="GHz", expression=r"$\Gamma(f)/2 \pi$", label="full qubit coupling")
    @coupling.getter
    def _get_coupling(self, f, f0, ft_mult, eta, epsinf, Dvv, Ct_mult, Np, W):
         Ga=self._get_Ga(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Dvv=Dvv, Np=Np, W=W)
         Ct=self._get_Ct(epsinf=epsinf, Ct_mult=Ct_mult, W=W, Np=Np)
         return Ga/(2*Ct)/(2*pi)

    Lamb_shift=SProperty().tag(desc="""Lamb shift""", unit="GHz", expression=r"$B_a/\omega C$", label="Lamb shift")
    @Lamb_shift.getter
    def _get_Lamb_shift(self, f, f0, ft_mult, eta, epsinf, W, Dvv, Np, Ct_mult):
        """returns Lamb shift"""
        Ba=self._get_Ba(f=f, f0=f0, Np=Np, W=W, Dvv=Dvv, epsinf=epsinf, eta=eta, ft_mult=ft_mult)
        Ct=self._get_Ct(epsinf=epsinf, Ct_mult=Ct_mult, W=W, Np=Np)
        return -Ba/(2*Ct)/(2*pi)

    Ga0_mult=SProperty().tag(desc="single: $2.87=1.694^2$, double: $3.11=(1.247 \sqrt{2})^2$", expression=r"$c_{Ga}(f)$", label=r"$G_a$ multiplier")
    @Ga0_mult.getter
    def _get_Ga0_mult(self, f0, Np, W, ft_mult, eta, epsinf, Dvv):
        Ga0=self._get_Ga0(f0=f0, Np=Np, W=W, epsinf=epsinf, eta=eta, ft_mult=ft_mult)
        return Ga0/(2.0*pi*f0*W*epsinf*Dvv*Np**2)

    max_coupling=SProperty().tag(desc="""Coupling at IDT center frequency""", unit="GHz",
                     label="Coupling at center frequency", tex_str=r"$\gamma_{f0}$")
    @max_coupling.getter
    def _get_max_coupling(self, f, f0, ft_mult, eta, epsinf, Ct_mult, Dvv, Np, W):
        return self._get_coupling(f=f0+0.001, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, Dvv=Dvv, Np=Np, W=W)

    max_coupling_approx=SProperty().tag(unit="GHz", label="Qubit coupling ($f$) (no sinc)", expression=r"$\Gamma/2\pi \approx c_g(f) f_0 K^2 N_p$", desc="frequency dependent")
    @max_coupling_approx.getter
    def _get_max_coupling_approx(self, f0, K2, Np, ft):
        cpl_mult={"single" : 0.71775, "double" : 0.54995}[ft]
        return cpl_mult*f0*K2*Np

    def fixed_reset(self):
        """resets fixed properties in proper order"""
        super(IDT, self).fixed_reset()
        self.get_member("fixed_P").reset(self)
        self.get_member("fixed_RAM_P").reset(self)
        self.get_member("fixed_X").reset(self)
        self.get_member("fixed_Asum").reset(self)
        self.get_member("fixed_Ga").reset(self)
        self.get_member("fixed_Ba").reset(self)
        self.get_member("fixed_coupling").reset(self)
        self.get_member("fixed_Lamb_shift").reset(self)
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
        return self.fixed_Ga/(2*self.Ct)/(2*pi)

    @private_property
    def fixed_Lamb_shift(self):
        return -self.fixed_Ba/(2.0*self.Ct)/(2.0*pi)

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

    @log_func
    def _get_Asum(self, f, f0, Np, dloss1, dloss2, g_arr, polarity):
        return 1.0/Np*array([sum([g_arr[i]*exp(2.0j*pi*frq/f0*n-frq/f0*dloss1*n-n*dloss2*(frq/f0)**2)
               for i, n in enumerate(polarity)]) for frq in f])

    @private_property
    def fixed_Asum(self):
        return self._get_Asum(f=self.fixed_freq)


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
    def _get_simple_S(self, f, f0, ft_mult, eta, epsinf, W, Dvv, Np, Ct, YL, dL, vf, L_IDT):
        Ga=self._get_Ga(f=f, f0=f0, Np=Np, W=W, Dvv=Dvv, epsinf=epsinf, eta=eta, ft_mult=ft_mult)
        Ba=self._get_Ba(f=f, f0=f0, Np=Np, W=W, Dvv=Dvv, epsinf=epsinf, eta=eta, ft_mult=ft_mult)
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

    def _get_rs(self, f):
        h=30e-9
        lbda=self._get_lbda(f=f)
        rs=(-1.7/100-0.24*h/lbda)*1.0j
        if absolute(rs)>=1.0:
            return 0.9999j
        return rs

    ts=SProperty()
    @ts.getter
    def _get_ts(self, rs):
        return sqrt(1.0-absolute(rs)**2)

    Gs=SProperty().tag(desc="Inglebrinsten's approximation of $\Gamma_S$ (Morgan)", expression=r"$\Gamma_S \approx (\Delta v/v)/\epsilon_\infty$")
    @Gs.getter
    def _get_Gs(self, Dvv, epsinf):
        return Dvv/epsinf



    L_IDT=SProperty().tag(desc="length of IDT", unit="um", expression=r"$L_{IDT}=N_{IDT}p$", label="IDT length")
    @L_IDT.getter
    def _get_L_IDT(self, N_IDT, p):
        return N_IDT*p

    N_IDT=SProperty().tag(desc="total number of IDT fingers", label="Total IDT fingers", expression=r"$N_{IDT}=2 c_{ft} N_p$")
    @N_IDT.getter
    def _get_N_IDT(self, ft_mult, Np):
        return 2*ft_mult*Np#+ft_mult*(Np+1)


    def _get_RAM_P_one_f(self, f, p, N_IDT, L_IDT, f0, alpha, rs, Y0, dloss1, dloss2,
                         W, Np,  ft,
                         vf, Dvv, epsinf):
        #k=2*pi*f/vf#-1.0j*(f/f0*dloss1+dloss2*(f/f0)**2) 0.19 f/1e9 + 0.88 (f/1e9)**2 dB/us*1e6/3488 *log(10.0)/20.0
        k=2*pi*f/vf-1.0j*(dloss1*f/1e9 + dloss2*(f/1e9)**2)*1e6/3488*log(10.0)/20.0
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
        I = eye(2)
        if ft=="single":
            P32_base=(inv(I-A**2)*(I-A**(2*int(Np))))*matrix([[0],
                                                            [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-p)/2.0)]]) #geometric series
        else:
            P32_base=((I+A)*inv(I-A**4)*(I-A**(4*int(Np))))*matrix([[0],
                                                                  [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-2.0*p)/2.0)]])
        P31=P32=D*(B*P32_base)
        P13=P23=-P31/2.0
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32)

    @private_property
    def fixed_RAM_P(self):
        if self.Y0_type=="center":
            Y0=self.Y00
        else:
            Y0=self._get_Y0(f=self.fixed_freq)
        if self.mus_type=="center":
            alpha=self.alpha0
        else:
            alpha=self._get_alpha(f=self.fixed_freq)
        if self.rs_type=="constant":
            rs=self.rs
        else:
            rs=self._get_rs(f=self.fixed_freq)
        return self._get_RAM_P(frq=self.fixed_frq, alpha=alpha, Y0=Y0, rs=rs)

#    @private_property
#    def fixed_Y0(self):
#        return self._get_Y0(f=self.fixed_freq)
#
#    @private_property
#    def fixed_rs(self):
#        return self._get_rs(f=self.fixed_freq)

    @log_func
    def _get_RAM_P(self, frq, f0, alpha, rs, Y0, dloss1, dloss2,
                   W, Np, ft,
                   vf, Dvv, epsinf):
        if Y0 is None:
            Y0=pi*f0*W*epsinf/Dvv

        Ct_mult={ "single" : 1.0, "double" : sqrt(2)}[ft]
        Ct=Ct_mult*W*epsinf*Np

        ft_mult={"double" : 2.0, "single" : 1.0}[ft]
        lbda0=vf/f0
        p=lbda0/(2*ft_mult)
        N_IDT=2*ft_mult*Np
        L_IDT=Np*lbda0

        if isinstance(alpha, float):
            alpha=ones(len(frq))*alpha
        if isinstance(rs, complex):
            rs=ones(len(frq))*rs
        if isinstance(Y0, float):
            Y0=ones(len(frq))*Y0
        print "start P"
        P=[self._get_RAM_P_one_f(f=f, Dvv=Dvv, epsinf=epsinf, W=W, vf=vf, rs=rs[i], Y0=Y0[i], p=p,
                            N_IDT=N_IDT, alpha=alpha[i], ft=ft, Np=Np, f0=f0, dloss1=dloss1, dloss2=dloss2, L_IDT=L_IDT) for i, f in enumerate(frq)]
        print "P_done"

        (P11, P12, P13,
         P21, P22, P23,
         P31, P32)=[squeeze(P_ele) for P_ele in zip(*P)]
        print "P_done 2"
        Ga=2.0*absolute(P13)**2
        Ba=-imag(hilbert(Ga))
        P33=Ga+1.0j*Ba+2.0j*pi*frq*Ct
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32, P33), Ga, Ba, Ct

    @private_property
    def view_window(self):
        return IDTView(agent=self)

def metallization_couple(pl="metallization_couple", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.N_fixed=100000
    #idt.fixed_freq_max=20.0*idt.f0
    idt.eta=0.5
    #idt.ft="single"
    #idt.S_type="RAM"
    idt.couple_type="full expr"
    idt.fixed_reset()
    line(idt.fixed_freq/idt.f0, idt.fixed_coupling, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)

    pl=line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)
    idt.eta=0.6
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.6", color="red", linewidth=0.3, label="0.6", **kwargs)
    idt.eta=0.4
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("coupling", frq), plotter=pl, plot_name="0.4", color="green", linewidth=0.3, label="0.4", **kwargs)
    idt.eta=0.5
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling"
    pl.legend()
    return pl
#metallization_couple()#.show()
def metallization_Lamb(pl="metallization_lamb", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    idt.eta=0.5
    idt.N_fixed=100000
    #idt.fixed_freq_max=20.0*idt.f0

    #idt.ft="single"
    idt.couple_type="full expr"
    #idt.Lamb_shift_type="hilbert"
    idt.fixed_reset()
    pl=line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.5", color="blue", linewidth=0.3, label="0.5", **kwargs)
    idt.eta=0.6
    idt.fixed_reset()
    #line(idt.fixed_freq/idt.f0, idt.fixed_Lamb_shift/idt.max_coupling, plotter=pl, linewidth=0.3, color="purple")
    line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.6", color="red", linewidth=0.3, label="0.6", **kwargs)
    idt.eta=0.4
    idt.fixed_reset()
    line(frq/idt.f0, idt.get_fix("Lamb_shift", frq), plotter=pl, plot_name="0.4", color="green", linewidth=0.3, label="0.4", **kwargs)
    idt.eta=0.5
    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift"
    pl.legend()
    return pl
#metallization_Lamb()#.show()

def sinc_check(pl="sinc_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="sinc"#, "giant atom", "full sum"
    idt.Ba_type="formula"
    idt.rs_type="constant"
    frq=linspace(0e9, 10e9, 10000)
    idt.fixed_freq_max=20.0*idt.f0
    pl=line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, label=idt.Ga_type, color="red",  **kwargs)
    X=idt.Np*pi*(frq-idt.f0)/idt.f0
    line(frq/idt.f0, (sin(X)/X)**2, plotter=pl, label=idt.Ga_type, color="green", **kwargs)
    line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    idt.Ba_type="hilbert"
    line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    line(frq/idt.f0, -imag(hilbert(idt._get_Ga(frq)/idt.Ga0_approx)), plotter=pl, label=idt.Ga_type, **kwargs)
    print idt.Ga0, idt.Ga0_approx
    print idt.Ga0_mult
    print idt.max_coupling, idt.max_coupling_approx
    return pl
#sinc_check().show()

def giant_atom_check(pl="giant_atom_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="giant atom"#, "full sum"
    idt.Ba_type="formula"
    idt.rs_type="constant"
    frq=linspace(0e9, 10e9, 10000)
    idt.fixed_freq_max=20.0*idt.f0
    pl=line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    line(frq/idt.f0, idt._get_coupling(frq)/idt.max_coupling_approx, plotter=pl, label=idt.Ga_type, color="red",  **kwargs)
    X=idt.Np*pi*(frq-idt.f0)/idt.f0
    Np=idt.Np
    line(frq/idt.f0, (sin(X)/X)**2, plotter=pl, label=idt.Ga_type, color="purple", **kwargs)

    line(frq/idt.f0, (1.0/Np*sin(X)/sin(X/Np))**2, plotter=pl, label=idt.Ga_type, color="green", **kwargs)
    line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    idt.Ba_type="hilbert"
    line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    line(frq/idt.f0, -imag(hilbert(idt._get_Ga(frq)/idt.Ga0_approx)), plotter=pl, label=idt.Ga_type, **kwargs)
    print idt.Ga0, idt.Ga0_approx
    print idt.Ga0_mult
    print idt.max_coupling, idt.max_coupling_approx
    return pl
#giant_atom_check().show()

def sinc_variety_check(pl="sinc_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.Y0_type="center"
    idt.df_type="center"
    idt.mus_type="center"
    idt.Ga_type="sinc"#, "giant atom", "full sum"
    idt.Ba_type="formula"
    frq=linspace(0e9, 10e9, 10000)
    idt.fixed_freq_max=20.0*idt.f0
    pl=line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    idt.Y0_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, color="red", **kwargs)
    idt.Y0_type="center"
    idt.df_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, color="green", **kwargs)
    idt.df_type="center"
    idt.mus_type="formula"
    line(frq/idt.f0, idt._get_Ga(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, color="purple", **kwargs)

    X=idt.Np*pi*(frq-idt.f0)/idt.f0
    line(frq/idt.f0, (sin(X)/X)**2, plotter=pl, label=idt.Ga_type, color="blue", **kwargs)
    #line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    #idt.Ba_type="hilbert"
    #line(frq/idt.f0, idt._get_Ba(frq)/idt.Ga0_approx, plotter=pl, label=idt.Ga_type, **kwargs)
    #line(frq/idt.f0, -imag(hilbert(idt._get_Ga(frq)/idt.Ga0_approx)), plotter=pl, label=idt.Ga_type, **kwargs)
    #print idt.Ga0, idt.Ga0_approx
    #print idt.Ga0_mult
    #print idt.max_coupling, idt.max_coupling_approx
    return pl
sinc_variety_check().show()

def couple_comparison(pl="couple_compare", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    #idt.Np=21
    #idt.ft="single"
    #idt.rs=-0.05j
    #idt.dloss2=0.1*5e6
    #idt.eta=0.7
    #idt.N_fixed=100000
    idt.fixed_freq_max=20.0*idt.f0
    #idt.S_type="RAM"
    #pl=line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="cyan", linewidth=0.5, label=idt.S_type, **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()
    idt.Ga_type="sinc"
    pl=line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, linewidth=0.5, label=idt.couple_type, **kwargs)
    idt.Ga_type="giant atom"
    line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="red", linewidth=0.5, label=idt.couple_type)
    idt.couple_type="df giant atom"
    line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="green", linewidth=0.5, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, (idt._get_coupling(frq)), plotter=pl, color="black", linewidth=0.5, label=idt.couple_type)
    #idt.couple_type="full sum"
    #line(frq/idt.f0, (idt._get_coupling(frq)), plotter=pl, color="purple", linewidth=0.5, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling"
    pl.set_ylim(0.0, 1.3e9)
    pl.legend()
    return pl
couple_comparison().show()
def RAM_comparison(pl="RAM_compare", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    #idt2=IDT.process_kwargs(kwargs)

    frq=linspace(0.01e9, 10e9, 10000)
    idt.fixed_freq_max=2.0*idt.f0

    def _get_RAM_P_one_f(self, f, Dvv, epsinf, W, vf,  rs, p, N_IDT, alpha, ft, Np, f0, dloss1, dloss2, L_IDT):
        #Y0=self._get_Y0(f=f, Dvv=Dvv, epsinf=epsinf, W=W)
        #rs=self._get_rs(f=f)
        #print rs
        k=2*pi*f/vf#-1.0j*(f/f0*dloss1+dloss2*(f/f0)**2)
        ts = sqrt(1.0-absolute(rs)**2)
        A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
                           [-rs,             exp(1.0j*k*p)]])#.astype(complex128)
        #AN=A**int(N_IDT)
        #AN11, AN12, AN21, AN22= AN[0,0], AN[0,1], AN[1,0], AN[1,1]
        #P11=-AN21/AN22
        #P21=AN11-AN12*AN21/AN22
        #P12=1.0/AN22
        #P22=AN12/AN22
        #D = -1.0j*alpha*Dvv*sqrt(Y0)
        #B = matrix([(1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0), (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)])
        I = eye(2)

        P1=(I+A)
        P2=inv(I-A**4)*(I-A**(4*int(Np)))
        return 1/sqrt(2)*absolute(P1[1,1]*exp(-1.0j*k*p/2.0))*absolute(P2[1,1])**2 ##, P2

    #idt.Np=37
    #idt.ft="single"
    #idt.couple_type="full expr"
    #pl=line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, linewidth=0.5, label=idt.couple_type, **kwargs)
    #data=[_get_RAM_P_one_f(idt, f=f, Dvv=idt.Dvv, epsinf=idt.epsinf, W=idt.W, vf=idt.vf, rs=idt.rs, p=idt.p,
    #                             N_IDT=idt.N_IDT, alpha=idt.alpha0, ft=idt.ft, Np=idt.Np, f0=idt.f0, dloss1=idt.dloss1, dloss2=idt.dloss2, L_IDT=idt.L_IDT) for f in frq]
    #data=array(data)
    #print data.shape
    #line(frq, array(data), pl=pl, color="green")
    Np=idt.Np
    gX=idt._get_X(f=frq)
    #line(frq, 1/81.0*(sqrt(2.0)*cos(pi*frq/(4.0*idt.f0))*sin(gX)/sin(gX/Np))**2, pl=pl)#.show()
    #line(frq, 2.0*cos(pi*frq/(4.0*idt.f0)), pl=pl).show()
    print idt.f0, idt.Dvv, idt.epsinf, idt.W, idt.vf,  idt.rs, idt.p, idt.N_IDT, idt.alpha, idt.ft, idt.Np, idt.f0, idt.dloss1, idt.dloss2, idt.L_IDT
    #idt.S_type="RAM"
    idt.couple_type="full expr"
    idt.fixed_reset()

    #P=idt._get_RAM_P()
    gamma=idt._get_couple_factor(f=idt.fixed_freq)
    line(idt.fixed_freq, idt._get_couple_factor(f=idt.fixed_freq), plotter=pl, color="red", linewidth=0.5, label=idt.ft)#.show()
    line(idt.fixed_freq, gamma, plotter=pl, color="blue", linewidth=0.5, label=idt.ft).show()

    #line(idt.fixed_freq, gamma*2*idt.Ct*2*pi*P[1], plotter=pl, color="red", linewidth=0.5, label=idt.ft)#.show()
    #line(idt.fixed_freq, P[2], plotter=pl, color="green", linewidth=0.5, label=idt.ft)
    idt.S_type="simple"
    #idt.ft="double"
    idt.couple_type="df giant atom" #"full expr"
    idt.fixed_reset()
    line(idt.fixed_freq, gamma*2*idt.Ct*2*pi*idt._get_Ga(idt.fixed_freq)/idt.Ga0, plotter=pl, color="blue", linewidth=0.5, label=idt.ft).show()
    line(idt.fixed_freq, idt._get_Ba(idt.fixed_freq), plotter=pl, color="black", linewidth=0.5, label=idt.ft).show()

    #idt.Np=37
    #idt.fixed_freq_max=20.0*idt.f0

    #idt2.ft="single"

    #idt.fixed_reset()
    line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="red", linewidth=0.5, label=idt.ft)
    idt.ft="single"
    idt.fixed_reset()
    line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, color="green", linewidth=0.5, label=idt.ft)
    idt.S_type="simple"
    idt.ft="double"
    idt.couple_type="full expr"
    idt.fixed_reset()
    pl=line(frq/idt.f0, idt._get_coupling(frq), plotter=pl, linewidth=0.5, label=idt.couple_type, **kwargs)

    pl.xlabel="frequency/center frequency"
    pl.ylabel="coupling"
    #pl.set_ylim(-30, 1.0)
    pl.legend()
    return pl
#RAM_comparison().show()
#couple_comparison()#.show()
def fix_couple_comparison(pl="fix couple", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.fixed_freq_max=20.0*idt.f0
    idt.couple_type="sinc sq"
    idt.fixed_reset()
    frq=linspace(0e9, 10e9, 10000)
    pl=line(frq/idt.f0, 10*log10(idt.get_fix("coupling", frq)/idt.max_coupling), plotter=pl, linewidth=0.3, label=idt.couple_type, **kwargs)
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

#fix_couple_comparison().show()
def Lamb_shift_comparison(pl="ls_comp", **kwargs):
    idt=IDT.process_kwargs(kwargs)

    #idt.rs=-0.01j
    #idt.dloss2=0.1*1e6
    #idt.eta=0.4
    frq=linspace(0e9, 10e9, 10000)
    #idt.N_fixed=100000
    idt.fixed_freq_max=20.0*idt.f0

    idt.S_type="RAM"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(f=frq), plotter=pl, color="cyan", linewidth=0.5, label=idt.S_type, **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()

    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc sq"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, linewidth=0.5, label="sinc^2", **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="red", linewidth=0.5, label=idt.couple_type)

    idt.Lamb_shift_type="hilbert"
    idt.couple_type="df giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="green", linewidth=0.5, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="black", linewidth=0.5, label=idt.couple_type)
    #idt.couple_type="full sum"
    #line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="purple", linewidth=0.5, label=idt.couple_type)

    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift"
    pl.set_ylim(-1e9, 1e9)
    pl.legend(loc="lower right")
    return pl

#Lamb_shift_comparison()#.show()

def hilbert_check(pl="hilbert", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    frq=linspace(0e9, 10e9, 10000)
    #idt.N_fixed=100000
    idt.fixed_freq_max=20.0*idt.f0
    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc sq"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, linewidth=1.0, label="sinc^2", **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="red", linewidth=1.0, label=idt.couple_type)
    idt.Lamb_shift_type="hilbert"
    idt.couple_type="sinc sq"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="green", linewidth=0.5, label="h(sinc^2)")
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq), plotter=pl, color="black", linewidth=0.5, label="h(giant atom)")

    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift"
    pl.set_ylim(-1e9, 1e9)
    pl.legend(loc="lower right")
    return pl

#hilbert_check().show()

def Lamb_shift_check(pl="ls_check", **kwargs):
    idt=IDT.process_kwargs(kwargs)
    idt.fixed_freq_max=20.0*idt.f0
    frq=linspace(0e9, 10e9, 10000)

    idt.S_type="RAM"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(f=frq)/idt.max_coupling, plotter=pl, color="cyan", linewidth=0.5, label=idt.S_type, **kwargs)
    idt.S_type="simple"
    idt.fixed_reset()

    idt.Lamb_shift_type="formula"
    idt.couple_type="sinc sq"
    pl=line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, linewidth=0.5, label=idt.couple_type, **kwargs)
    idt.couple_type="giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="red", linewidth=0.5, label=idt.couple_type)
    idt.couple_type="df giant atom"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="green", linewidth=0.5, label=idt.couple_type)
    idt.couple_type="full expr"
    line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="black", linewidth=0.5, label=idt.couple_type)
    #idt.couple_type="full sum"
    #line(frq/idt.f0, idt._get_Lamb_shift(frq)/idt.max_coupling, plotter=pl, color="purple", linewidth=0.5, label=idt.couple_type)
    pl.xlabel="frequency/center frequency"
    pl.ylabel="Lamb shift/max coupling (dB)"
    pl.set_ylim(-1.0, 1.0)
    pl.legend(loc="lower right")

    #line(frq, a._get_full_Lamb_shift(frq)/a.max_coupling, plotter=pl, color="black", linewidth=0.3)
    return pl

#Lamb_shift_check().show()
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
    #a.Y0_type="center"
    #a.mus_type="center"
    #a.df_type="center"
    #print a.f0
    #Y0, mus/Dvv, df_corr, cpl_form
    #2.0*/a.K2*absolute(mus/Dvv *Dvv *df_corr*1.0)**2
    #(mus/Dvv*df_corr)**2  Dvv*(Np**2)

    #print 2*pi*a.f0*a.W*a.epsinf/a.K2
    print a.Ga0, a.Ga0_approx
    print a.Ga0_mult
    print a.max_coupling, a.max_coupling_approx
    #a.S_type="RAM"

if __name__=="__main2__":

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