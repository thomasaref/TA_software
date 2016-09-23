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

    def _default_Ga_type(self):
        return "giant atom"

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
            return self.fixed_RAM_P #_get_RAM_P()
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
        return array([r if absolute(r)<0.9 else 0.9j for r in rs])

        #if absolute(rs)>=1.0:
        #    return 0.9999j
        #return rs

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
        return self._get_RAM_P(frq=self.fixed_freq, alpha=alpha, Y0=Y0, rs=rs)

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

        #print alpha, rs, Y0, f0, dloss1, dloss2, W, Np, ft, vf, Dvv, epsinf, L_IDT, N_IDT
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

if __name__=="__main__":
    a=IDT()
    a.show()
