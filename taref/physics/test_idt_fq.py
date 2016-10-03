# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 11:55:30 2016

@author: thomasaref
"""

#from taref.plotter.api import colormesh
from scipy.constants import pi, epsilon_0 as eps0
from scipy.signal import hilbert
from numpy import linspace, sin, amax, amin, argmin, argmax, cos, imag, sqrt, absolute, matrix, exp, eye, array, squeeze, float64, ones, log, meshgrid, argmin
import matplotlib.pyplot as plt
from taref.physics.surface_charge import alpha
from numpy.linalg import inv
from taref.physics.fitting import LorentzianFitter
f0=5.000000001e9

frq=linspace(3e9, 7e9, 400).astype(float64)
frq_q=linspace(1e9, 10e9, 500).astype(float64)
Np=9 #3 #9*3.9#*20 #1.2344
W=25.0e-6
ft="double"
vf=3488.0
Dvv=  0.048/2 #0.0007/2.0 #0.024/4.5 #
epsinf=46.0*eps0
Ct=sqrt(2)*W*Np*epsinf

f, fq = meshgrid(frq, frq_q, sparse=True)

wq=2*pi*fq
X=Np*pi*(f-f0)/f0
Ga0_mult={"single" : 2.872, "double" : 3.111}[ft]
Ga0=Ga0_mult*2.0*pi*f0*epsinf*W*Dvv*(Np**2)
print Np
print 0.55*2*Dvv*Np*f0/1e9
print Ga0/(2*Ct)/(2*pi)/1e9
print Ga0/(2*Ct)/(3*f0/Np)
print 2*pi*0.55*2*Dvv*Np**2
print 2*Dvv*Np**2
#alp_0=alpha(f0, f0, ft_mult=2)
#print alp_0
#alp_arr=alpha(frq, f0, ft_mult=2)

def _get_Y0(f, Dvv, epsinf, W):
    return pi*f*W*epsinf/Dvv

Y0_arr=_get_Y0(f=frq, W=W, epsinf=epsinf, Dvv=Dvv)

Ga=Ga0*(sin(X)/X)**2.0

Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
print Ba.shape
#h1=imag(hilbert(c1))

#plt.figure()
#plt.plot(frq/f0, Ga, linewidth=2.0)
#plt.plot(frq/f0, Ba)
#plt.xlim(0.0, 2.0)

w=2*pi*f
k=2*pi*f/vf

jkL=1.0j*k*Np*vf/f0

P33plusYL=Ga+1.0j*Ba+1.0j*w*Ct-1.0j*Ct/w*wq**2

S11=-Ga/P33plusYL*exp(-jkL)
s11=absolute(S11)**2

GL=6e-6
S13=1.0j*sqrt(2.0*Ga*GL)/P33plusYL*exp(-jkL/2.0)
s13=absolute(S13)**2

Cc=25e-15
ZL=50.0

Zatom=-1.0j/(w*Cc)+1/P33plusYL
#Zeff=ZL*Zatom/(Zatom+ZL)
Zeff=Zatom
S33=(Zeff-ZL)/(Zeff+ZL)
#S33=1+S33
t33=1-absolute(S33)**2
#t33=(t33.transpose()/amax(t33, axis=1)).transpose()
t33=t33/amax(t33, axis=0)

s33=absolute(S33)**2
#pl=
if 1:
    plt.pcolormesh(frq/1e9, frq_q/1e9, absolute(S33)**2, cmap="nipy_spectral")#.show()
    #plt.clim(0.7, 1.0)
    plt.colorbar()
    plt.xlabel("Frequency (GHz)")
    plt.ylabel("Qubit frequency (GHz)")

    plt.figure()
    fit=LorentzianFitter()
    fit.gamma=0.05
    fit.full_fit(x=frq_q/1e9, y=s33.transpose(), gamma=0.05)
    #            if self.calc_p_guess:
    #                self.fitter.make_p_guess(self.flux_axis[self.flat_flux_indices], y=self.MagAbsFilt_sq, indices=self.flat_indices, gamma=self.fitter.gamma)
    absfit=fit.reconstruct_fit(frq_q/1e9, fit.fit_params)
    plt.pcolormesh(frq/1e9, frq_q/1e9, absfit.transpose(), cmap="nipy_spectral") #, pl=pl)#.show()
    plt.xlabel("Frequency (GHz)")
    plt.ylabel("Qubit frequency (GHz)")

    #plt.clim(0.7, 1.0)
    plt.colorbar()

fit2=LorentzianFitter(fit_type="refl_lorentzian")
fit2.gamma=0.05
fit2.full_fit(x=frq_q/1e9, y=s11.transpose(), gamma=0.05)

plt.figure()

plt.pcolormesh(frq/1e9, frq_q/1e9, s11, cmap="nipy_spectral")#.show()
absfit2=fit2.reconstruct_fit(frq_q/1e9, fit2.fit_params)
plt.xlabel("Frequency (GHz)")
plt.ylabel("Qubit frequency (GHz)")

#plt.clim(0.0, 0.1)
plt.colorbar()

plt.figure()

plt.pcolormesh(frq/1e9, frq_q/1e9, absfit2.transpose(), cmap="nipy_spectral")#.show()
#plt.clim(0.0, 0.1)

#plt.clim(0.7, 1.0)
plt.colorbar()
plt.xlabel("Frequency (GHz)")
plt.ylabel("Qubit frequency (GHz)")

plt.figure()
plt.plot(frq, array([fp[1] for fp in fit.fit_params])*1e9, label="center S33")
plt.plot(frq, frq_q[argmin(absolute(S33)**2, axis=0)], label="min S33")
plt.plot(frq, frq+Ba[0,:]/(2*Ct)/(2*pi), label="theory")

plt.plot(frq, frq_q[argmax(absolute(S11)**2, axis=0)], label="min S11")
#plt.plot(frq, frq_q[argmax(absolute(S11)**2, axis=0)])
plt.plot(frq, array([fp[1] for fp in fit2.fit_params])*1e9, label="center S11")
plt.legend()
plt.xlabel("Frequency (Hz)")
plt.ylabel("Qubit frequency (Hz)")

plt.figure()
plt.plot(frq, absolute([fp[0] for fp in fit.fit_params]), label="width S33")
plt.plot(frq, Ga[0,:]/(2*Ct)/(2*pi)/1e9, label="theory")
plt.plot(frq, absolute([fp[0] for fp in fit2.fit_params]), label="width S11")
plt.legend()

plt.xlabel("Frequency (Hz)")
plt.ylabel("Coupling (Hz)")


plt.show()

if 0:
    plt.figure()
    plt.plot( frq, absolute(S33)[1000, :], label="S11")
    plt.plot( frq, absolute(S33)[800, :], label="S11")


    ss=1-absolute(S33)[:, 600]
    ss=ss/max(ss)
    ss2=1-absolute(S33)[:, 400]
    ss2=ss2/max(ss2)
    plt.figure()
    #min(absolute(S33)[:, 600]), label="S11")
    plt.plot( frq_q, ss, label="S33")
    plt.plot( frq_q, ss2, label="S33")

    plt.legend()
    plt.plot( frq_q, absolute(S11)[:, 550], label="S11")
    plt.plot( frq_q, absolute(S11)[:, 450], label="S11")

    plt.plot( frq_q, absolute(S33)[:, 550]/min(absolute(S33)[:, 550]), label="S11")
    plt.plot( frq_q, absolute(S33)[:, 450]/min(absolute(S33)[:, 450]), label="S11")
    #plt.show()
    plt.figure()
    plt.pcolormesh(frq, frq_q, absolute(S11)**2, cmap="spectral")
    ls=-Ba[0, :]/(2*Ct)/(2*pi)
    gamma=Ga[0, :]/(2*Ct)/(2*pi)
    fplus=sqrt(frq*(frq-2.0*ls+2.0*gamma))
    fminus=sqrt(frq*(frq-2.0*ls-2.0*gamma))
    FWHM=fplus-fminus

    centers=sqrt(frq*(frq-2.0*ls))
    #plt.plot(frq, centers)
    #plt.plot([frq[0], frq[-1]], [frq_q[1000], frq_q[1000]])
    #plt.plot([frq[0], frq[-1]], [frq_q[800], frq_q[800]])
    plt.ylim(2e9, 8e9)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Qubit Frequency (Hz)")
    #plt.plot(frq, fplus)
    #plt.plot(frq, fminus)

    plt.figure()
    plt.plot( frq, absolute(S11)[1000, :], label="S11")
    #plt.plot(frq/f0, Ga[0, :]/Ga0, linewidth=2.0)
    #plt.plot(frq/f0, Ba[0, :]/Ga0, linewidth=2.0)
    #plt.plot(frq/f0, absolute(centers-f0)/f0)
    ind1=argmin(absolute(centers[:470]-f0))
    ind2=argmin(absolute(centers[470:530]-f0))+470
    ind3=argmin(absolute(centers[530:]-f0))+530
    print ind1, (frq/f0)[ind1]
    print ind2, (frq/f0)[ind2]
    print ind3, (frq/f0)[ind3]

    def lor(x,p):
        return (p[0]**2/(p[0]**2+(x-p[1])**2))

    lor1=lor(frq, [gamma[ind1], frq[ind1]])
    lor2=lor(frq, [gamma[ind2], f0+ls[ind2]])
    lor3=lor(frq, [gamma[ind3], frq[ind3]])
    gX=Np*pi*(frq-f0)/f0
    #plt.plot(frq/f0, (sin(gX)/gX)**2.0)
    #plt.plot(frq/f0, (lor1+lor2+lor3)/3)
    plt.plot( frq, lor1, label="Lorentzian 1")
    plt.plot( frq, lor2, label="Lorentzian 2")
    plt.plot( frq, lor3, label="Lorentzian 3")
    plt.legend()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Response (a.u.)")

    plt.figure()
    plt.plot(frq, absolute(S11)[800, :], label="S11")
    ind1=argmin(absolute(centers[:450]-frq_q[800]))
    ind2=argmin(absolute(centers[450:]-frq_q[800]))+450
    #ind3=argmin(absolute(centers[700:]-f0))+700
    print ind1, (frq/f0)[ind1]
    print ind2, (frq/f0)[ind2]

    lor1=lor(frq, [gamma[ind1], frq[ind1]])
    lor2=lor(frq, [gamma[ind2], frq[ind2]])
    plt.plot(frq, lor1, label="Lorentzian 1")
    plt.plot(frq, lor2, label="Lorentzian 2")
    plt.legend()
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Response (a.u.)")
    plt.show()
    #Ga0=alp_0*Dvv*sqrt(Y0_arr)
    #Ga=alp_arr*Dvv*sqrt(Y0_arr)

    #def _get_rs(f, h=30.0e-9, vf=3488.0):
    #    lbda= vf/f
    #    rs=(-1.7/100-0.24*h/lbda)*1.0j
    #    #if absolute(rs)>=1.0:
    #    #    return 0.9999j
    #    return rs
    #
    #def _get_RAM_P_one_f(f, p, N_IDT, L_IDT, f0, alpha, rs, Y0, dloss1, dloss2,
    #                     W, Np,  ft,
    #                     vf, Dvv, epsinf):
    #    #k=2*pi*f/vf#-1.0j*(f/f0*dloss1+dloss2*(f/f0)**2) 0.19 f/1e9 + 0.88 (f/1e9)**2 dB/us*1e6/3488 *log(10.0)/20.0
    #    k=2*pi*f/vf-1.0j*(0.19*f/1e9 + 0.88*(f/1e9)**2)*1e6/3488*log(10.0)/20.0
    #    ts = sqrt(1.0-absolute(rs)**2)
    #    A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
    #                       [-rs,             exp(1.0j*k*p)]])#.astype(complex128)
    #    AN=A**int(N_IDT)
    #    AN11, AN12, AN21, AN22= AN[0,0], AN[0,1], AN[1,0], AN[1,1]
    #    P11=-AN21/AN22
    #    P21=AN11-AN12*AN21/AN22
    #    P12=1.0/AN22
    #    P22=AN12/AN22
    #    D = -1.0j*alpha*Dvv*sqrt(Y0) #/(2.0*Np)
    #    #D = -1.0j*sqrt(self.Ga0)/(2.0*Np)#*alpha*Dvv*sqrt(Y0)
    #
    #    B = matrix([(1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0), (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)])
    #    #B0 = (1.0-rs/ts+1.0/ts)*exp(-1.0j*k*p/2.0)
    #    #B1 = (1.0+rs/ts+1.0/ts)*exp(1.0j*k*p/2.0)
    #
    #    I = eye(2)
    #    if ft=="single":
    #        P32_base=(inv(I-A**2)*(I-A**(2*int(Np))))*matrix([[0],
    #                                                        [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-p)/2.0)]]) #geometric series
    #    else:
    #        P32_base=((I+A)*inv(I-A**4)*(I-A**(4*int(Np))))*matrix([[0],
    #                                                              [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-2.0*p)/2.0)]])
    #    P32=D*(B*P32_base)
    #        #P32=D*(B0*P32_base[0,0]+B1*P32_base[1,0])
    #        #P32=D*B*((I+A)*inv(I-A**4)*(I-A**(4*int(Np))))*matrix([[0],
    #        #                                                      [1.0/AN[1,1]*exp(1.0j*k*(L_IDT-2.0*p)/2.0)]]))[0] #geometric series
    #    P31=P32
    #    P13=P23=-P31/2.0
    #    return (P11, P12, P13,
    #            P21, P22, P23,
    #            P31, P32)
    #
    #def _get_RAM_P(frq, f0=5.000000001e9, alpha=1.247, rs=0.0j, Y0=None, dloss1=0.0, dloss2=0.0,
    #               W=25.0e-6, Np=9, ft="double",
    #               vf=3488.0, Dvv=0.024, epsinf=46.0*eps0):
    #    if Y0 is None:
    #        Y0=pi*f0*W*epsinf/Dvv
    #
    #    Ct_mult={ "single" : 1.0, "double" : sqrt(2)}[ft]
    #    Ct=Ct_mult*W*epsinf*Np
    #
    #    ft_mult={"double" : 2.0, "single" : 1.0}[ft]
    #    lbda0=vf/f0
    #    p=lbda0/(2*ft_mult)
    #    N_IDT=2*ft_mult*Np
    #    L_IDT=Np*lbda0
    #
    #    if isinstance(alpha, float):
    #        alpha=ones(len(frq))*alpha
    #    if isinstance(rs, complex):
    #        rs=ones(len(frq))*rs
    #    if isinstance(Y0, float):
    #        Y0=ones(len(frq))*Y0
    #    print "start P"
    #    P=[_get_RAM_P_one_f(f=f, Dvv=Dvv, epsinf=epsinf, W=W, vf=vf, rs=rs[i], Y0=Y0[i], p=p,
    #                        N_IDT=N_IDT, alpha=alpha[i], ft=ft, Np=Np, f0=f0, dloss1=dloss1, dloss2=dloss2, L_IDT=L_IDT) for i, f in enumerate(frq)]
    #    print "P_done"
    #
    #    (P11, P12, P13,
    #     P21, P22, P23,
    #     P31, P32)=[squeeze(P_ele) for P_ele in zip(*P)]
    #    print "P_done 2"
    #    Ga=2.0*absolute(P13)**2
    #    Ba=-imag(hilbert(Ga))
    #    P33=Ga+1.0j*Ba+2.0j*pi*f*Ct
    #    return (P11, P12, P13,
    #            P21, P22, P23,
    #            P31, P32, P33), Ga, Ba, Ct
    #



    plt.figure()
    plt.plot(frq/f0, l2, linewidth=2.0)
    plt.plot(frq/f0, h2)
    plt.xlim(0.0, 2.0)

    plt.figure()
    plt.plot(frq/f0, alp_arr)

    plt.figure()
    plt.plot(frq/f0, c1, label="sinc sq")
    #plt.plot(frq/f0, c2, label="giant atom")
    #plt.plot(frq/f0, c3, label="df giant atom")
    #plt.plot(frq/f0, c4, label="full expr")
    plt.plot(frq/f0, c5, label="RAM")
    #plt.xlim(0.0, 2.0)
    plt.legend()

    plt.figure()
    plt.plot(frq/f0, l1, label="sinc sq")
    #plt.plot(frq/f0, l2, label="giant atom")
    #plt.plot(frq/f0, h3, label="df giant atom")
    #plt.plot(frq/f0, h4, label="full expr")
    plt.plot(frq/f0, h5, label="RAM")
    #plt.xlim(0.0, 2.0)
    plt.legend()



    plt.show()
