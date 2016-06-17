# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:15:35 2016

@author: thomasaref
"""

from numpy import pi, exp, sqrt, matrix, linspace, sin, cos, arccos, absolute, array, dot, diag, complex64, complex128, eye
from numpy.linalg import eig, inv
from taref.physics.fundamentals import eps0

Dvv=2.4e-2 #0.07/100.0/2.0
epsinf=46*eps0 #120.0e-12
vf=3488.0 #2864.0
Gs=Dvv/epsinf
#y0=3.1e-3
#y0a=2*pi*epsinf*vf/(2*Dvv)
f0=5.0e9 #4.8586e9#4.8556e9
w0=2.0*pi*f0
lbda0=vf/f0
p=lbda0/2.0
W=25.0e-6
Np=9
Y0=1/50.0

def RAMtest():
    N=9
    rs=0.1j
    k=2*pi/1.0
    p=2.0
    ts = sqrt(1-absolute(rs)**2)

    A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
                      [-rs,             exp(1.0j*k*p)  ]])#.astype(complex128)
    #ei,vec=eig(A)
    #AN = dot(dot(vec,diag(ei)**(N)), inv(vec))
    #print AN
    AN=A**(N)
    print AN
    rho_fs=1.694
    D = -1j*rho_fs*sqrt(k*vf*W*Gs/2.0)
    B = matrix([(1.0-rs/ts+1.0/ts)*exp(-1j*k*p/2.0), (1.0+rs/ts+1.0/ts)*exp(1j*k*p/2.0)])

    P32=D*B*inv(eye(2)-A**2)*(eye(2)-AN)*matrix([[0],
                                                   [1.0/AN[1,1]]])[0] #geometric series

    P23=-P32/2.0

    cnbn=A*(cnm1, bnm1)
    In=D*B*(cnm1, bnm1)

    #w=2.0*pi*f
    #k=w/vf#-1.0j*loss
    p11=p22=rs*exp(-1.0j*k*p) #Morgan 8.1
    p12=ts*exp(-1.0j*k*p) #Morgan 8.1

    g=1.0/p*arccos(cos(k*p)/ts+0.0j) #adding 0.0j so arccos does not return nan

    sinNgp=sin(N*g*p)
    sinNm1gp=sin((N-1)*g*p)
    singp=sin(g*p)
    P11=p11*sinNgp/(sinNgp-p12*sinNm1gp)
    P12=P21=p12*singp/(sinNgp-p12*sinNm1gp)
    P22=p22*sinNgp/(sinNgp-p12*sinNm1gp)

    print P11, -AN[1,1]/AN[0,1]/2.0
    print P21, AN[0,0]+P11*AN[1,0]
    #print P12, 1.0/AN[1,1]
    #print P22, AN[0,1]/AN[1,1]



RAMtest()
def RAM(q=0.5, f=f0, rs=0.0, loss=0.0):
    ts = sqrt(1-absolute(rs)**2)
    w=2.0*pi*f
    k=w/vf#-1.0j*loss
    p11=p22=rs*exp(-1.0j*k*p) #Morgan 8.1
    p12=ts*exp(-1.0j*k*p) #Morgan 8.1

    g=1.0/p*arccos(cos(k*p)/ts+0.0j) #adding 0.0j so arccos does not return nan

    sinNgp=sin(N*g*p)
    sinNm1gp=sin((N-1)*g*p)
    singp=sin(g*p)
    P11=p11*sinNgp/(sinNgp-p12*sinNm1gp)
    P12=P21=p12*singp/(sinNgp-p12*sinNm1gp)
    P22=p22*sinNgp/(sinNgp-p12*sinNm1gp)

    In=-1.0j*rhob(k)*sqrt(w*W*Gs/2.0)*((cnm1+bn)*exp(-0.5j*k*p)+(cn*bnm1)*exp(0.5j*k*p))

    cnm1=0


    P32=P31
    P13=-P31/2.0
    P23=-P32/2.0
    Ga=absolute(P13)**2+absolute(P23)**2
    Ba=hilbert
    C=sqrt(2)*W*epsinf*Np

    P33=Ga+1.0j*Ba+1.0j*w*C


    A = 1.0/ts*matrix([[exp(-1.0j*k*p),       rs      ],
                      [-rs,             exp(1j*k*p)  ]])
    AN=A**(2*N)

    ei,vec=eig(A)
    AN = dot(dot(vec,diag(ei)**(2*N)), inv(vec))
    print AN
    print A**N

    #p11 = r*exp(-1j*k*p)
    #p12 = t*exp(-1j*k*p)
    P11 = zeros(len(k),complex)
    P12 = zeros(len(k),complex)
    P13 = zeros(len(k),complex)
    P21 = zeros(len(k),complex)
    P22 = zeros(len(k),complex)
    P23 = zeros(len(k),complex)
    for i,K in enumerate(k):
        #RAM = array([[p12[i]-p11[i]**2/p12[i],p11[i]/p12[i]],[-p11[i]/p12[i], 1/p12[i]]])
        A = 1.0/t*array([[exp(-1j*K*p),r],[-r,exp(1j*K*p)]])
        ei,vec=linalg.eig(A)
        AN = dot(dot(vec,diag(ei)**(2*N)),linalg.inv(vec))
        P11[i]=- AN[1,0]/AN[1,1]
        P21[i]=AN[0,0]+P11[i]*AN[0,1]
        P12[i]=1.0/AN[1,1]
        P22[i]=AN[0,1]/AN[1,1]
        cb0=array([[1],[P11[i]]])
        D = -1j*rho_fs*sqrt(K*v*W*Gamma/2.0)
        B = array([(1.0-r/t+1.0/t)*exp(-1j*K*p/2.0), (1.0+r/t+1.0/t)*exp(1j*K*p/2.0)])
        Atot=dot(linalg.inv(eye(2)-dot(A,A)),eye(2)-AN)
        """
        Here we have I_{n+1} = D * [B1 B2] * [c_n;b_n] = D*B*A**n*[c_0;b_0]
        Summing over even n gives inv(I-A**2)*(I-A**(2*N))
        I_0 is slightly different: letting c_-1=b_-1=0, I_0 becomes D*[exp(-1j...),exp(1j...)]*[c_0;b_0]
        """
        I=D*dot(B,dot(Atot,cb0))
        P13[i]=-I[0]/2.0
        cb0=array([[0],[1.0/AN[1,1]]])
        I=D*dot(B,dot(Atot,cb0))
        P23[i]=-I[0]/2.0
    return P11,P12,P13,P21,P22,P23
def calcT(a=0.5, f=f0, rs=0.0, ts=1.0):
    #lbda=vf/f
    w=2.0*pi*f
    k=w/vf-1.0j*3.0e3

    p11=p22=rs*exp(-1.0j*k*p) #Morgan 8.1
    p12=p21=ts*exp(-1.0j*k*p) #Morgan 8.1

    p13=p23=a*1.0j*1.694*Dvv*sqrt(w*W*epsinf/(2.0*Dvv))*exp(-1.0j*k*p/2.0) #renormalized P-matrix (compared to Datta's) so reciprocity is satisfied. Datta's Y0=sqrt(w*W*epsinf/(2.0*Dvv))
    p31=p32=-2.0*p13
    p33=p31*p13/exp(-1.0j*k*p) #-2.0*m0p*sqrt(w*W*epsinf/(2.0*Dvv)) #Phase factor has to be like this to match Datta's assumption that electrical admittance of single finger is real

    T=matrix([[p21-p22*p11/p12,    p22/p12,    p23-p22*p13/p12, 0.0], #Though it may not look like it, this is equivalent to the T-matrix one can derive from end of Datta's chapter 4
              [   -p11/p12,        1/p12,        -p13/p12,      0.0], #This is also eqn D.22 in Morgan
              [      0,              0,              1.0,       0.0],
              [  p31-p32*p11/p12,  p32/p12,   p33-p32*p13/p12,  1.0]])
    return T

frq=linspace(f0-0.00001e9, f0+0.3e9,1000)

y0=[]
y1=[]

y2=[]
y3=[]

for f in frq:
    #T matrix calculation. Modified from end of chapter 4 in Datta with some things from Morgan
    lbda=vf/f
    w=2.0*pi*f

    rs=-0.75j*Dvv+1.07j*30.0e-9/lbda #From Datta this works better if it is 20*log10(S33) instead of 10*log10(S33)
    #rs=-0.75j*Dvv-0.62j*30.0e-9/lbda #From Datta Plugging through some formulas in Datta. I got rs=-0.75jDvv+1.07jh\lbda for aluminum electrodes on GaAs.
                                     #Morgan has parameters for quartz and lithium niobate but not GaAs. Should check literature for values
    ts=sqrt(1.0-abs(rs)**2.0)


    Tp=calcT(a=0.5, f=f, rs=rs, ts=ts) #a is assumed +1/2 for positive fingers
    Tn=calcT(a=-0.5, f=f, rs=rs, ts=ts) #a is assumed -1/2 for negative fingers
    T2=Tp*Tn #single finger configuration
    T=T2**Np #raise to number of pairs power

    T11=T[0,0]
    T12=T[0,1]
    T13=T[0,2]
    T21=T[1,0]
    T22=T[1,1]
    T23=T[1,2]
    T31=T[3,0]
    T32=T[3,1]
    T33=T[3,2]
    Ga=T33-T23*T32/T22 #this is actually Ga+jBa. Matches sinc^2 function model when rs=0.0

    Ct=epsinf*Np*W #total capacitance of single fingered IDT
    P33=Ga+1.0j*w*Ct #Total admittance
    S33=(Y0-P33)/(Y0+P33) #Electrical reflectivity is the usual thing

    y0.append(abs(S33))
    #y0.append(angle(S33, deg=1))

    X=Np*pi*(w-w0)/w0  #Analytical sinc^2 calculation for comparison. Models should reduce to this when rs is set to 0.0 and they appear to
    Ga0=2.87*w0*epsinf*W*Np**2.0*Dvv #Morgan 1.12
    Ga1=Ga0*(sin(X)/X)**2.0 #Morgan 1.12
    Ba1=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
    P33a=Ga1+1.0j*Ba1+1.0j*w*Ct
    S33a=(Y0-P33a)/(Y0+P33a)

    P21=T11-T21*T12/T22 #inverse of Morgan D.22
    P22=T12/T22
    P23=T13-T12*T23/T22
    P11=-T21/T22
    P12=1/T22
    P13=-T23/T22
    P31=T31-T21*T32/T22
    P32=T32/T22
    P33=T33-T23*T32/T22

    S11=P11-P13*P31/(Y0+P33) #From Rukhlenko 2000 eqn 1.8
    S12=P12-P13*P32/(Y0+P33)
    S13=2.0*sqrt(Y0)*P13/(Y0+P33)
    S21=P21-P23*P31/(Y0+P33)
    S22=P22-P23*P32/(Y0+P33)
    S23=2*sqrt(Y0)*P23/(Y0+P33)
    S31=-P31*sqrt(Y0)/(Y0+P33)
    S32=-P32*sqrt(Y0)/(Y0+P33)

    y1.append(abs(S11))
    #y1.append(angle(S13, deg=1))

    #Coupling of Modes (COM) calcuation as described in Morgan chapter 8. Eqn numbers refer to Morgan's eqn numbers
    #h=30.0e-9 #film thickness
    #rs=-0.03j  #-0.718j*Dvv-0.001j*h/lbda0
    #ts=sqrt(1.0-abs(rs)**2.0)

    ke=w/vf-1.0j*3.0e3 #you can include loss between electrodes by making adding imaginary component #ve=w/Re(ke)
    N=Np #number of finger pairs

    kc=kg=pi/p #eqn 8.23
    d=ke-kg #eqn 8.23
    c12=rs/p #eqn 8.41 assuming rs1=rs2=rs
    s=sqrt(d**2.0-abs(c12)**2.0+0.0j) #eqn 8.35
    rhoke=1.694*epsinf #this is given by eqn 5.59 which is an awful formula. I use numerical evaluation of eqn 5.59 given on page 13 middle paragraph

    a1=0.5*1.0j*rhoke*sqrt(2.0*w*W*Gs)/(2.0*p) #eqn 8.42 I had to insert a factor of 0.5 (similar to T matrix approach) which I don't quite understand.
                                               #This factor of 0.5 is probably due to the array factor of one pair of fingers

    Ct=N*W*epsinf #L*Cl total capacitance of single finger IDT.
    L=N*2.0*p #length of single finger IDT
    D=s*cos(s*L)+1.0j*d*sin(s*L) #near eqn 8.40
    K1=(conj(a1)*c12-1.0j*d*a1)/s**2.0 #eqn 8.38
    K2=(a1*conj(c12)+1.0j*d*conj(a1))/s**2.0 #eqn 8.38

    P11=-conj(c12)*sin(s*L)/D #eqn 8.40a
    P12=P21=s*exp(-1.0j*kc*L)/D #eqn 8.40b
    P22=c12*sin(s*L)*exp(-2.0j*kc*L)/D #eqn 8.40c
    P31=(2.0*conj(a1)*sin(s*L)-2*s*K2*(cos(s*L)-1))/D #eqn 8.40d
    P13=P31/(-2.0) #eqn 8.40d
    P32=exp(-1.0j*kc*L)*(-2*a1*sin(s*L)-2*s*K1*(cos(s*L)-1))/D #eqn 8.40e
    P23=P32/(-2.0) #eqn 8.40e
    P33=-K1*P31-K2*P32*exp(1.0j*kc*L)+2*(conj(a1)*K1-a1*K2)*L+1.0j*w*Ct #eqn 8.40f

    Ya=-K1*P31-K2*P32*exp(1.0j*kc*L)+2*(conj(a1)*K1-a1*K2)*L #Ga+jBa

    S33b=(Y0-P33)/(Y0+P33) #standard electrical reflection

    S11=P11-P13*P31/(Y0+P33) #From Rukhlenko 2000 eqn 1.8
    S12=P12-P13*P32/(Y0+P33)
    S13=2.0*sqrt(Y0)*P13/(Y0+P33)
    S21=P21-P23*P31/(Y0+P33)
    S22=P22-P23*P32/(Y0+P33)
    S23=2*sqrt(Y0)*P23/(Y0+P33)
    S31=-P31*sqrt(Y0)/(Y0+P33)
    S32=-P32*sqrt(Y0)/(Y0+P33)

    y3.append(abs(S13))
    #y3.append(angle(S13, deg=1))
