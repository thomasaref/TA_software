# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 15:52:51 2017

@author: thomasaref
"""


from qutip import destroy, spectrum, Qobj
from numpy import linspace, sqrt, arange, diag, conj
from time import time

from numpy import prod, transpose, identity, kron, zeros, dot, real
from numpy.linalg import pinv, solve
from qutip import issuper, liouvillian, qeye, tensor, spre, mat2vec, steadystate

def _spectrum_pi(H, wlist, c_ops, a_op, b_op, use_pinv=False):
    """
    Internal function for calculating the spectrum of the correlation function
    :math:`\left<A(\\tau)B(0)\\right>`.
    """

    #print issuper(H)

    L = H if issuper(H) else liouvillian(H, c_ops)

    tr_mat = tensor([qeye(n) for n in L.dims[0][0]])
    N = prod(L.dims[0][0])

    A = L.full()
    b = spre(b_op).full()
    a = spre(a_op).full()

    tr_vec = transpose(mat2vec(tr_mat.full()))

    rho_ss = steadystate(L)
    rho = transpose(mat2vec(rho_ss.full()))

    I = identity(N * N)
    P = kron(transpose(rho), tr_vec)
    Q = I - P

    spectrum = zeros(len(wlist))

    for idx, w in enumerate(wlist):
        if use_pinv:
            MMR = pinv(-1.0j * w * I + A)
        else:
            MMR = dot(Q, solve(-1.0j * w * I + A, Q))

        s = dot(tr_vec,
                   dot(a, dot(MMR, dot(b, transpose(rho)))))
        spectrum[idx] = -2 * real(s[0, 0])

    return spectrum

N=5

wlist2 = linspace(-500.0, 500.0, 201)
w0_arr=linspace(4211, 5622, 301)

a = destroy(N)
adag=a.dag()

gamma=38.0
wd = 4806.6
Ec = 220.0 # Charging energy.
Ejmax = 22000.0
rate = gamma

c_op_list=[sqrt(rate) * a]  # decay operators


p = -1.0j*(adag - a) # "P" operator.

#p_l = kron(It,p) # % "P" operator multiplying rho from the left.
#p_r = kron(transpose(p),It) # "P" operator multiplying rho from the right.
#print p_r

nvec=arange(N)
wdvec=nvec*wd
Ecvec=-Ec*(6.0*nvec**2+6.0*nvec+3.0)/12.0

print "yo"
def find_expect(phi=0.2, Omega=3.0, wd=wd, use_other=True):

    Ej = (phi**2)/(8*Ec) #Ejmax*absolute(cos(pi*phi)) #; % Josephson energy as function of Phi.

    wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec

    wT = wTvec-wdvec
    transmon_levels = Qobj(diag(wT[range(N)]))
    Omega_vec=- 0.5j*(Omega*adag - conj(Omega)*a)
    H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
    if use_other:
        exp1=spectrum(H, wlist2, c_op_list, a, p, solver="pi", use_pinv=False)
    else:
        exp1=_spectrum_pi(H, wlist2, c_op_list, a, p, use_pinv=False)
    return exp1


for n in range(5):
    tstart=time()
    find_expect(use_other=False)
    print time()-tstart

for n in range(5):
    tstart=time()
    find_expect()
    print time()-tstart


