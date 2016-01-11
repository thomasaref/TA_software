# -*- coding: utf-8 -*-
"""
Created on Wed May 14 18:03:31 2014

@author: thomasaref
"""

from scipy.constants import e, h, hbar, k as kB, epsilon_0 as eps0, pi
Z0=50.0
f0=5.0e9
w0=2.0*pi*f0
W=10.0e-6
Np=30

material="LiNbYZ"
if material=="STquartz":
    epsinf=5.6*eps0
    Dvv=0.06e-2
    v=3159.0
elif material=='GaAs':
    epsinf=1.2e-10
    Dvv=0.035e-2
    v=2900.0
elif material=='LiNbYZ':
    epsinf=46*eps0
    Dvv=2.4e-2
    v=3488.0
elif material=='LiNb128':
    epsinf=56*eps0
    Dvv=2.7e-2
    v=3979.0
elif material=='LiNbYZX':
    epsinf=46*eps0
    Dvv=0.8e-2
    v=3770.0
elif material=="MDCQuartz":
    Dvv=0.2/2.0/100.0
    epsinf=5.0e-11
    v=3642.0
elif material=="LiTaZY":
    Dvv=0.93/2.0/100.0
    epsinf=4.4e-10
    v=3329.0
elif material=="LiTaMDC":
    Dvv=1.54/2.0/100.0
    epsinf=4.4e-10
    v=3370.0
else:
    print "Material not listed"
lbda0=v/f0
Cs=epsinf
K2=2.0*Dvv #2.26*Dvv
y0=2.0*pi*Cs*v/K2
mu=0.8j*K2
print e, h, hbar, kB, eps0, pi

from numpy import zeros, linspace, round, mod, array, argmin, delete, sqrt
from numpy.linalg import eig
from matplotlib.pyplot import plot, show, close, ylim, legend, ylabel, xlabel
#from scipy.special import mathieu_a

def EkdivEc(ng=0.5, Ec=1.0/4.0, Ej=2.0, N=50):
    #calculates transmon energy level with N states (more states is better approximation)
    #effectively solves the mathieu equation but for fractional inputs (which doesn't work in scipy.special.mathieu_a
    d1=[]
    d2=[]
    d3=[]
    for a in ng:
        NL=2*N+1
        A=zeros((NL, NL))
        for b in range(0,NL):
            A[b, b]=4.0*Ec*(b-N-a)**2
            if b!=NL-1:
                A[b, b+1]= -Ej/2.0
            if b!=0:
                A[b, b-1]= -Ej/2.0
        w,v=eig(A)
        d1.append(min(w))#/h*1e-9)
        w=delete(w, w.argmin())
        d2.append(min(w))#/h*1e-9)
        w=delete(w, w.argmin())
        d3.append(min(w))#/h*1e-9)
    return array(d1), array(d2), array(d3)

N=30
ng=[0.0]#linspace(-0.6001, 1.6, 101) #[0.5] 
f0=8.0e9
Ej=f0*h/h*1e-9
EjoverEc=linspace(0.1, 40, 101) #array([1*4.0])
Ej0=Ej#*sqrt(EjoverEc/8)
#Np=30
#Cs=5.0e-10
#Cj=Np*W*Cs
#Ec=e**2/(2*Cj)
#Ec=Ej/EjoverEc
#d1, d2, d3= EkdivEc(ng=ng, Ec=Ec, Ej=Ej, N=50)
        
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

E01a, Ctr, data, d1, d2, d3=sweepEc()
Ec=Ej/EjoverEc#/h*1e-9
Ec0=Ej0/EjoverEc#/h*1e-9
anharm=-1/(sqrt(8.0*Ej0/Ec0)-1.0)
E01a=sqrt(8*Ej0*Ec0)-Ec0

plot(Ej0/Ec0/4.0, anharm*E01a, label='transmon approx')#*E01a/h*1e-9, label="anharm transmon approx")
plot(EjoverEc/4.0, data, label="anharm python ng=0")

ng=[0.5]#linspace(-0.6001, 1.6, 101) #[0.5] 
E01a, Ctr, data, d1, d2, d3=sweepEc()
plot(EjoverEc/4.0, data, label="anharm python ng=0.5 E=%.3f" % data[-1])
#print Ctr
#plot(ng, d1, 'o', label="eigenvalue solution python")
#plot(ng, d2, 'o')
#plot(ng, d3, 'o')

results = []
with open('/Users/thomasaref/Dropbox/Current stuff/mmataoutputanharm.txt') as inputfile:
    for line in inputfile:
        results.append([float(i) for i in line.strip().split('\t')])
results=array(results)
results=results.transpose()
#with open('path/to/file') as infile:
#    answer = [[int(i) for i in line.strip().split(',')] for line in infile]            
plot(results[0], results[1], label='Bloch Bands ala mathieu nb ng=0.5')
plot(results[0], results[2], label='Bloch Bands ala mathieu nb ng=0')
#plot(results[0], 4.0*Ec*results[3])
#print results[1]
plot(EjoverEc, data, label="anharm many charge states")

Np=2
#W=20.0e-6
f0=4.0e9
W=Ctr/(1.414*Np*epsinf)
coupling1=0.5*f0*Np*2.0*Dvv    
plot(EjoverEc/4.0, zeros(101,)+coupling1*1e-9, label="Np={0}, coupling={1}".format(Np, coupling1*1e-9))
plot(EjoverEc/4.0, W*1e6/10, label="IDT W (um)")#, d2, ng, d3)
Nidt=sqrt(1.0/50.0/(3.11*2.0*pi*f0*epsinf*W*Dvv))
plot(EjoverEc/4.0, Nidt/10.0, label="N IDT/10")#, d2, ng, d3)

#W=10.0e-6
#Np=Ctr/(1.414*W*epsinf)
#coupling1=0.5*f0*Np*2.0*Dvv    
#plot(EjoverEc, coupling1*1e-9, label="coupling (W=10 um)")
#plot(EjoverEc, Np, label="Number of finger pairs (W=10 um)")#, d2, ng, d3)
#W=5.0e-6
#Np=Ctr/(1.414*W*epsinf)
#coupling1=0.5*f0*Np*2.0*Dvv    
#plot(EjoverEc/4.0, coupling1*1e-9, label="coupling (W=5 um)")
#plot(EjoverEc, Np, label="Number of finger pairs (W=5 um)")#, d2, ng, d3)
plot(EjoverEc/4, zeros(101,), label="y=0")
ylim(-2,10)
ylabel("Frequency (GHz) or length of fingers (um) or probe IDT number of fingers/10")#"relative anharm") #Energy level (Eq)")#"Frequency (GHz) or length of fingers (um)")
xlabel("Ej over EQ")
legend()
show()
#q=-Ej/(2*Ec)
#s=-2*ng
#for a in ng:
#    lbda=mathieu_a(2*abs(a), q)
#    print a, lbda#+4*Ec*a**2
