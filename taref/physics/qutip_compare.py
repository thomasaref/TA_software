# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 14:17:42 2017

@author: thomasaref
"""

from qutip import mat2vec, tensor, destroy, qeye, Qobj, spre, spost, liouvillian, steadystate
from numpy import  squeeze, array, ones, linspace, dot,  real, zeros, diag, arange, sqrt, conj, exp, prod, kron,  transpose, identity
from numpy.linalg import pinv, solve, eig, inv
N=2
Ec=0.02
Ej=1.0
wd=4.8
Omega=3.0

#print qeye(N)
#print help(qeye)
a=destroy(N) #equivalent to tm
adag=a.dag()
#print a

#print a.dag() #equivalent to tp

print Qobj(diag(range(0, 2*N, 2))) #dephasing operator, tdiag
#print help(diag)

print spre(a) #tm_l = kron(Itot,tm);

p = -1.0j*(adag - a) # "P" operator.

print p

print spre(p) #p_l = kron(Itot,p) % "P" operator multiplying rho from the left.


print spost(p)  #p_r = kron(transpose(p),Itot) % "P" operator multiplying rho from the right.
N_gamma=0.0
gamma=0.01
rate = gamma 

c_op_list=[sqrt(rate) * a,]  # decay operators

nvec=arange(N)
wdvec=nvec*wd
Ecvec=-Ec*(6.0*nvec**2+6.0*nvec+3.0)/12.0

wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec

    #wdvec=nvec*sqrt(8.0*Ej*Ec)
    #wdvec=nvec*wd

wT = wTvec-wdvec
transmon_levels = Qobj(diag(wT[range(N)]))
print transmon_levels
#Omega_vec=- 0.5j*(Omega*adag - conj(Omega)*a)
theta=0.0
Omega_vec= 0.5*Omega*(a*exp(-1j*theta)+adag*exp(1j*theta))
print Omega_vec
H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
print H
#Ht = H.data.T
#from qutip.cy.spmath import zcsr_kron

#from qutip.fastsparse import fast_csr_matrix, fast_identity
#spI=fast_identity(N)
#data = -1j * zcsr_kron(spI, H.data)
#data += 1j * zcsr_kron(Ht, spI)
#print data.toarray()
L=liouvillian(H, c_op_list) #ends at same thing as L = H_comm + Lindblad_tm ;
#print L
#print dir(L)

rho_ss = steadystate(L) #same as rho_ss_c but that's in column vector form
print rho_ss

wlist = linspace(-500.0, 500.0, 201)

use_pinv=True

tr_mat = tensor([qeye(n) for n in L.dims[0][0]])
N = prod(L.dims[0][0])

A = L.full()
D, U= L.eigenstates()
print D.shape, D
print diag(D)
b = spre(p).full()-spost(p).full()
a = spre(a).full()

tr_vec = transpose(mat2vec(tr_mat.full()))

rho_ss = steadystate(L)
rho = transpose(mat2vec(rho_ss.full()))

I = identity(N * N)
P = kron(transpose(rho), tr_vec)
Q = I - P

wp=4.9
w=-(wp-wd)

MMR = pinv(-1.0j * w * I + A) #eig(MMR)[0] is equiv to Dint
#MMR = pinv(-1.0j * w * I) # + A)
MMR = dot(Q, solve(-1.0j * w * I + A, Q))
#MMR = pinv(-1.0j * w * I + D)
#print diag(1.0/(1j*(wp-wd)*ones(N**2)+D)) #Dint = diag(1./(1i*(wp-wd)*diag(eye(dim^2)) + diag(D)))

print 1.0/(1j*(wp-wd)*ones(N**2)+D) #Dint = diag(1./(1i*(wp-wd)*diag(eye(dim^2)) + diag(D)))
U2=squeeze([u.full() for u in U]).transpose()
#print pinv(U)
Dint=eig(MMR)[0]
print "MMR", eig(MMR)[1]
print "Umult", U2*Dint*inv(U2)

s = dot(tr_vec,
        dot(a, dot(MMR, dot(b, transpose(rho)))))
print "s", 1j*s[0][0] #matches Chi_temp result

if 0:
    spectrum = zeros(len(wlist))
    
    for idx, w in enumerate(wlist):
        if use_pinv:
            MMR = pinv(-1.0j * w * I + A)
        else:
            MMR = dot(Q, solve(-1.0j * w * I + A, Q))
    
        s = dot(tr_vec,
                   dot(a, dot(MMR, dot(b, transpose(rho)))))
        spectrum[idx] = -2 * real(s[0, 0])
