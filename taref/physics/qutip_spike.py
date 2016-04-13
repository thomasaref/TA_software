# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 15:15:05 2016

@author: thomasaref
"""

from scipy.constants import pi, h, hbar, k
from numpy import exp
from numpy import identity, pi, exp, kron, diag, transpose, conjugate, sqrt, zeros, cos, reshape, arange, dot
from numpy.linalg import solve
#from scipy import sparse
from qutip import qeye, destroy, tensor
f0=4.5e9
w0=2*pi*f0
T=0.02
#print k*T/h/1e9
N_gamma=1.0/(exp(hbar*w0/(k*T))-1.0)
#print N_gamma
#print 1/(exp(f0/1.0e6/21000.0/T)-1)
gamma=50.0e6
gamma_phi=100.0e3
Nt=3
#It = sparse(identity(Nt))
It= qeye(Nt)
a=destroy(Nt)
adag=a.dag()

It = identity(Nt) # Unity matrix for the transmon.
Itot = It # Unity matrix for the total Hilbert space.

tm = diag(sqrt(range(1, Nt)),1) # Lowering operator for the transmon.
tp = tm.transpose().conjugate() #ctranspose(tm) # Raising operator for the transmon.

tdiag = diag(range(Nt)) # Diagonal matrix for the transmon.

#print tdiag

tdiag_l = kron(Itot,tdiag) # tdiag operator multiplying rho from the left.
#print tdiag_l

tm_l = kron(Itot,tm) # tm operator multiplying rho from the left.

#print tm_l
tensor(qeye(Nt), destroy(Nt)).data
qIt=qeye(Nt)
p = -1.0j*(tp - tm) # "P" operator.

#print p
#print -1.0j*(adag-a)


#Lindblad_tm = gamma*(N_gamma+1)*(kron(conj(tm),tm) -...
#                                    0.5*kron(Itot,ctranspose(tm)*tm) -...
#                                    0.5*kron(transpose(tm)*conj(tm),Itot));

Lindblad_tm = gamma*(N_gamma+1)*(kron(tm.conjugate(),tm) -
                                    0.5*kron(Itot,dot(tm.transpose().conjugate(), tm)) -
                                    0.5*kron(dot(tm.transpose(), tm.conjugate()),Itot))
#print kron(tm.conjugate(),tm)
#print tensor(a.conj(), a)
#print kron(tm.conjugate(),tm)==tensor(a.conj(), a).data

#print 0.5*kron(Itot,tm.transpose().conjugate()*tm)==0.5*tensor(qIt, adag*a).data
#print 0.5*kron(tm.transpose()*tm.conjugate(),Itot)==0.5*tensor(a.trans()*a.conj(), qIt).data
#print dot(tm.transpose(), tm.conjugate())
#print a#.trans()*a.conj()
print Lindblad_tm
lb_tm=gamma*(N_gamma+1)*(tensor(a.conj(), a)-0.5*tensor(qIt, adag*a)-0.5*tensor(a.trans()*a.conj(), qIt))
print lb_tm
print Lindblad_tm==lb_tm.data
#print tm
#print tm.transpose()==a.trans().data
#print tm
# Relaxation.

#Lindblad_tp = gamma*N_gamma*(kron(conj(tp),tp) -...
#                                    0.5*kron(Itot,ctranspose(tp)*tp) -...
#                                    0.5*kron(transpose(tp)*conj(tp),Itot));
Lindblad_tp = gamma*N_gamma*(kron(tp.conjugate(),tp) -
                                    0.5*kron(Itot,dot(tp.transpose().conjugate(), tp)) -
                                    0.5*kron(dot(tp.transpose(),tp.conjugate()),Itot))

#print Lindblad_tp
#print kron(tp.conjugate(),tp)==tensor(adag.conj(), adag).data
#print 0.5*kron(Itot,dot(tp.transpose().conjugate(), tp))==0.5*tensor(qIt,a*adag).data
#print 0.5*kron(dot(tp.transpose(),tp.conjugate()),Itot)==0.5*tensor(adag.trans()*adag.conj(), qIt).data
lb_tp=gamma*N_gamma*(tensor(adag.conj(), adag)-0.5*tensor(qIt,a*adag)-0.5*tensor(adag.trans()*adag.conj(), qIt))
#print lb_tp
#print Lindblad_tp==lb_tp.data
# Excitation (at T>0).

#Lindblad_deph = 0.5*gamma_phi*(kron(conj(2*tdiag),2*tdiag) -...
#                                    0.5*kron(Itot,ctranspose(2*tdiag)*2*tdiag) -...
#                                    0.5*kron(transpose(2*tdiag)*conj(2*tdiag),Itot));

Lindblad_deph = 0.5*gamma_phi*(kron(2*tdiag.conjugate(),2*tdiag) -
                                    0.5*kron(Itot,dot(2*tdiag.conjugate().transpose(), 2*tdiag)) -
                                    0.5*kron(dot(2*tdiag.transpose(), 2*tdiag.conjugate()),Itot))
lp_deph= 0.5*gamma_phi*(tensor(2*qtdiag.conj(), 2*qtdiag)-0.5*tensor(qIt, 2*qtdiag.dag()*2*qtdiag)
    -0.5*tensor(2*tdiag.trans()*2*tdiag*conj, qIt))
