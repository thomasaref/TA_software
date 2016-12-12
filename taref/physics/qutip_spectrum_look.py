# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:46:11 2016

@author: thomasaref
"""


from numpy import prod, transpose, identity, kron, zeros, dot, real
from numpy.linalg import pinv, solve
from qutip import issuper, liouvillian, qeye, tensor, spre, mat2vec, steadystate


def _spectrum_pi(H, wlist, c_ops, a_op, b_op, use_pinv=False):
    """
    Internal function for calculating the spectrum of the correlation function
    :math:`\left<A(\\tau)B(0)\\right>`.
    """

    print issuper(H)

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

def _spectrum_es(H, wlist, c_ops, a_op, b_op):
    """
    Internal function for calculating the spectrum of the correlation function
    :math:`\left<A(\\tau)B(0)\\right>`.
    """
    if debug:
        print(inspect.stack()[0][3])

    # construct the Liouvillian
    L = liouvillian(H, c_ops)

    # find the steady state density matrix and a_op and b_op expecation values
    rho0 = steadystate(L)

    a_op_ss = expect(a_op, rho0)
    b_op_ss = expect(b_op, rho0)

    # eseries solution for (b * rho0)(t)
    es = ode2es(L, b_op * rho0)

    # correlation
    corr_es = expect(a_op, es)

    # covariance
    cov_es = corr_es - np.real(np.conjugate(a_op_ss) * b_op_ss)

    # spectrum
    spectrum = esspec(cov_es, wlist)

    return spectrum