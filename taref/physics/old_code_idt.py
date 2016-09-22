# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 17:52:51 2016

@author: thomasaref
"""

#        if self.couple_type=="full sum" or self.S_type=="RAM":
#            return self.get_fix("coupling", f)
#        gX=self._get_X(Np=Np, f=f, f0=f0)
#        gamma=self._get_couple_factor(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
#        if self.couple_type=="full expr":
#            return gamma*((1.0/Np)*sin(gX)/sin(gX/Np))**2
#        gamma0=self._get_couple_factor(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
#        if self.couple_type=="giant atom":
#            return gamma0*(1.0/Np*sin(gX)/sin(gX/Np))**2
#        elif self.couple_type=="df giant atom":
#            return gamma0*(sqrt(2.0)*cos(pi*f/(4*f0))*1.0/Np*sin(gX)/sin(gX/Np))**2
#        return gamma0*(sin(gX)/gX)**2.0


    #def _get_Ga(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np, Ct):
    #    gamma=self._get_coupling(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
    #    return gamma*2*Ct*2*pi

#        if self.couple_type=="full sum" or self.S_type=="RAM":
#            return self.get_fix("Lamb_shift", f)
#        if self.Lamb_shift_type=="formula":
#            Ga0=self._get_Ga0()
#            gamma0=self._get_couple_factor(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
#            gX=self._get_X(Np=Np, f=f, f0=f0)
#            if self.couple_type=="sinc^2":
#                return -gamma0*(sin(2.0*gX)-2.0*gX)/(2.0*gX**2.0)
#            if self.couple_type=="giant atom":
#                return gamma0*(1.0/Np)**2*2*(Np*sin(2*gX/Np)-sin(2*gX))/(2*(1-cos(2*gX/Np)))
#        cpl=self._get_coupling(f=self.fixed_freq, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)
#        yp=imag(hilbert(cpl))
#        return interp(f, self.fixed_freq, yp)




#    Ga_mult=SProperty().tag(desc="single: $2.87=1.694^2$, double: $3.11=(1.247 \sqrt{2})^2$", expression=r"$c_{Ga}(f)$", label=r"$G_a$ multiplier")
#    @Ga_mult.getter
#    def _get_Ga_mult(self, f, f0, ft_mult, eta, epsinf, ft):
#        alpha=self._get_alpha(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf)
#        if ft=="single":
#            return alpha**2
#        return (alpha*2.0*cos(pi*f/(4.0*f0)))**2

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

#    couple_mult=SProperty().tag(desc="single: 0.71775. double: 0.54995, f dependent", label="coupling multiplier", expression=r"$c_g(f)$")
#    @couple_mult.getter
#    def _get_couple_mult(self, f, f0, ft_mult, eta, epsinf, Ct_mult):
#        Ga0_mult=self._get_Ga0_mult(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf)
#        return Ga0_mult/(4.0*Ct_mult)
#
#    couple_factor=SProperty().tag(unit="GHz", label="Qubit coupling ($f$) (no sinc)", expression=r"$\Gamma/2\pi \approx c_g(f) f_0 K^2 N_p$", desc="frequency dependent")
#    @couple_factor.getter
#    def _get_couple_factor(self, f, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np):
#        """coupling for one positive finger as function of frequency"""
#        couple_mult=self._get_couple_mult(f=f, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult)
#        return couple_mult*f0*K2*Np
#
#    couple_factor0=SProperty().tag(unit="GHz", label="Qubit coupling ($f_0$)", expression=r"$\Gamma/2\pi \approx c_g(f_0) f_0 K^2 N_p$" )
#    @couple_factor0.getter
#    def _get_couple_factor0(self, f0, ft_mult, eta, epsinf, Ct_mult, K2, Np):
#        """coupling at center frequency, in Hz (2 pi removed)"""
#        return self._get_couple_factor(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, Ct_mult=Ct_mult, K2=K2, Np=Np)

        if self.S_type=="RAM":
            return self.fixed_P[1]/(2.0*self.Ct)/(2.0*pi)
        gamma0=self.f0*self.K2*self.Np/(4*self.Ct_mult)
        if self.couple_type=="full sum":
            return gamma0*(self.fixed_alpha)**2*absolute(self.fixed_Asum)**2
        f, X, Np=self.fixed_freq, self.fixed_X, self.Np
        gamma=self._get_couple_factor(f=f)
        if self.couple_type=="full expr":
            return gamma*((1.0/Np)*sin(X)/sin(X/Np))**2
        f0=self.f0
        gamma0=self._get_couple_factor(f=f0)
        if self.couple_type=="giant atom":
            return gamma0*(1.0/Np*sin(X)/sin(X/Np))**2
        elif self.couple_type=="df giant atom":
            return gamma0*(sqrt(2.0)*cos(pi*f/(4*f0))*1.0/Np*sin(X)/sin(X/Np))**2
        return gamma0*(sin(X)/X)**2.0

                if self.S_type=="RAM":
            return -self.fixed_P[2]/(2.0*self.Ct)/(2.0*pi)
        if self.Lamb_shift_type=="formula":
            X, Np, f0=self.fixed_X, self.Np, self.f0
            gamma0=self._get_couple_factor(f=f0)
            if self.couple_type=="sinc^2":
                return -gamma0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
            if self.couple_type=="giant atom":
                return gamma0*(1.0/Np)**2*2*(Np*sin(2*X/Np)-sin(2*X))/(2*(1-cos(2*X/Np)))
        return imag(hilbert(self.fixed_coupling))

        #Ga0_mult=self._get_Ga0_mult(f=f0, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, ft=ft)
    def _get_RAM_P_one_f(self, f, Dvv, epsinf, W, vf,  rs, p, N_IDT, alpha, ft, Np, f0, dloss1, dloss2, L_IDT):
        #alpha=self._get_alpha(f=f, f0=f0, ft_mult=self.ft_mult, eta=self.eta, epsinf=epsinf)
        gamma=self._get_couple_factor(f=f, f0=f0, ft_mult=self.ft_mult, eta=self.eta, epsinf=epsinf, Ct_mult=self.Ct_mult, K2=self.K2, Np=Np)

        Y0=self._get_Y0(f=f, Dvv=Dvv, epsinf=epsinf, W=W)
        rs=0.0j #self._get_rs(f=f)
        #print rs
        k=2*pi*f/vf#-1.0j*(f/f0*dloss1+dloss2*(f/f0)**2)
        ts = sqrt(1.0-absolute(rs)**2)
        A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
                           [-rs,             exp(1.0j*k*p)]])#.astype(complex128)
        AN=A**int(N_IDT)
        AN11, AN12, AN21, AN22= AN[0,0], AN[0,1], AN[1,0], AN[1,1]
        P11=-AN21/AN22
        P21=AN11-AN12*AN21/AN22
        P12=1.0/AN22
        P22=AN12/AN22
        D = -1.0j*alpha*Dvv*sqrt(Y0) #/(2.0*Np)
        #D = -1.0j*sqrt(self.Ga0)/(2.0*Np)#*alpha*Dvv*sqrt(Y0)

        B = matrix([(1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0), (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)])
        #B0 = (1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0)
        #B1 = (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)

        I = eye(2)
        if ft=="single":
            P32=D*(B*inv(I-A**2)*(I-A**(2*int(Np)))*matrix([[0],
                                                            [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-p)/2.0)]]))[0] #geometric series
        else:
            P32_base=((I+A)*inv(I-A**4)*(I-A**(4*int(Np))))*matrix([[0],
                                                                  [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-2.0*p)/2.0)]])
            P32=D*(B*P32_base)
            #P32=D*(B0*P32_base[0,0]+B1*P32_base[1,0])
            #P32=D*B*((I+A)*inv(I-A**4)*(I-A**(4*int(Np))))*matrix([[0],
            #                                                      [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-2.0*p)/2.0)]]))[0] #geometric series
        P31=P32
        P13=P23=-P31/2.0
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32)
    @log_func
    def _get_RAM_P(self, W, rs, Np, vf, Dvv, epsinf, Ct, p, N_IDT, ft, f0, dloss1, dloss2, L_IDT):
        frq, alpha=self.fixed_freq, self.fixed_alpha
        print "start P"
        P=[self._get_RAM_P_one_f(f=f, Dvv=Dvv, epsinf=epsinf, W=W, vf=vf, rs=rs, p=p,
                                 N_IDT=N_IDT, alpha=alpha[i], ft=ft, Np=Np, f0=f0, dloss1=dloss1, dloss2=dloss2, L_IDT=L_IDT) for i, f in enumerate(frq)]
        print "P_done"

        (P11, P12, P13,
         P21, P22, P23,
         P31, P32)=[array(P_ele) for P_ele in zip(*P)]
        print "P_done 2"
        Ga=squeeze(2.0*absolute(P13)**2)
        Ba=imag(hilbert(Ga))
        P33=Ga+1.0j*Ba+2.0j*pi*f*Ct
        return (P11, P12, P13,
                P21, P22, P23,
                P31, P32, P33), Ga, -Ba

