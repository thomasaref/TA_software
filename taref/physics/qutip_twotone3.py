# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 14:13:38 2016

@author: thomasaref
"""

from numpy import conj, array, meshgrid, trace, reshape, linspace, exp, pi, transpose, diag, eye, kron, sqrt, arange, identity, absolute, cos, dot, real
from numpy.linalg import pinv, inv, eig
from qutip import to_super, destroy, tensor, liouvillian, spre, spost, mat2vec, Qobj, steadystate, qeye, parallel_map
from matplotlib.pyplot import pcolormesh, colorbar, show

wd_vec = linspace(4.3e9, 5.3e9, 91)/1e6
phi_arr=linspace(0.23, 0.33, 51)

Omega = 50

Ec = 0.22e9/1e6 # Charging energy.
Ejmax = 22.2e9/1e6 # Maximum Josephson energy.

gamma = 38e6*2*pi/(1e6*2*pi) # Relaxation rate of the transmon.
gamma_phi = 0*2*pi/(1e6*2*pi) # Dephasing rate of the transmon.

wp =  4.8066e9/1e6 # Probe frequency.

T = 21000.0*0.03#Temperature of the transmon bath in units of MHz (1K = 21 GHz).
N_gamma = 1.0/(exp(wp/T)-1.0)#Thermal population of the transmon phonon bath around wp.

theta_start = 0
theta_steps = 4
theta_end = (1.0-1.0/theta_steps)*2.0*pi
theta_vec = linspace(theta_start, theta_end, theta_steps)# Vector of drive phases.

N = 5 # Number of l

a=destroy(N)
adag=a.dag()

It= qeye(N)

#tdiag = sparse(diag(0:2:2*(Nt-1))); % Operator for dephasing.
#tdiag = Qobj(diag(range(0, N))) # Diagonal matrix for the transmon.
#tdiag_l = kron(It,tdiag) # tdiag operator multiplying rho from the left.

#tm_l = kron(It, a) # tm operator multiplying rho from the left.

c_op_list = []

rate = gamma * (1 + N_gamma)

c_op_list.append(sqrt(rate) * a)  # decay operators

Lindblad_tm = rate*(kron(a.conj(),a) -
              0.5*kron(It,adag*a) -
              0.5*kron(a.trans()*a.conj(),It))

print Lindblad_tm.shape

rate = gamma * N_gamma

c_op_list.append(sqrt(rate) * adag)  # excitation operators

Lindblad_tp = gamma*N_gamma*(kron(adag.conj(), adag) -
                             0.5*kron(It,a*adag) -
                             0.5*kron(adag.trans()*adag.conj(),It))

# Excitation (at T>0).
#Lindblad_deph = 0.5*gamma_phi*(kron(conj(tdiag),tdiag) -...
#                                    0.5*kron(Itot,ctranspose(tdiag)*tdiag) -...
#                                    0.5*kron(transpose(tdiag)*conj(tdiag),Itot));
# Dephasing.

p = -1.0j*(adag - a) # "P" operator.

#p_l = kron(It,p) # % "P" operator multiplying rho from the left.
#p_r = kron(transpose(p),It) # "P" operator multiplying rho from the right.

p_l=spre(p).full()
p_r=spost(p).full()
p_l_m_p_r=p_l-p_r
tm_l=spre(a).full()

nvec=arange(N)
Ecvec=-Ec*(6.0*nvec**2+6.0*nvec+3.0)/12.0

Omega_op=[0.5*Omega*(a*exp(-1.0j*theta)+adag*exp(1.0j*theta)) for theta in [0.0]]

tr_mat = tensor(qeye(N))
#N = np.prod(L.dims[0][0])
tr_vec = transpose(mat2vec(tr_mat.full()))

p_sup = spre(p).full()
a_sup = spre(a).full()

I=identity(N*N)
Idiag=diag(I)

# Excitation (at T>0).

#Lindblad_deph = 0.5*gamma_phi*(kron(conj(tdiag),tdiag) -...
#                                    0.5*kron(Itot,ctranspose(tdiag)*tdiag) -...
#                                    0.5*kron(transpose(tdiag)*conj(tdiag),Itot));
print "yo"

print eye(N).shape

eye(5).shape(25)
print reshape(eye(N),0,N**2)
raise Exception

def two_tone(vg):
    phi, wd=vg
    Ej = Ejmax*absolute(cos(pi*phi))#(phi**2)/(8*Ec) # #; % Josephson energy as function of Phi.

    wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec
    wdvec=nvec*wd
    wT = wTvec-wdvec

    transmon_levels = Qobj(diag(wT[range(N)]))

    for Om in Omega_op:
        H = transmon_levels + Om

        H_comm = -1j*(kron(It,H) - kron(transpose(H),It));

        L = H_comm + Lindblad_tm + Lindblad_tp #+ Lindblad_deph;

        print L

        #L2 = [reshape(eye(N),1,N**2); L]; %Add the condition trace(rho) = 1

        #rho_ss = L2\[1;zeros(dim^2,1)]; % Steady state density matrix

        #rho_ss_c = rho_ss; %Column vector form
        L = liouvillian(H, c_op_list)

        #D, V=L.eigenstates()
        #print "D", D.shape
        #print "V", V.shape
        #print L.diag()
        #print L.diag().shape
        #raise Exception
        A = L.full()

        rho_ss = steadystate(L)
        rho = transpose(mat2vec(rho_ss.full()))
        if 1:
            w=wp-wd
            MMR = pinv(-1.0j * w * I + A)
            Lexp=L.expm()
            MMR=Lexp*MMR*Lexp.dag()
            #    MMR = np.dot(Q, np.linalg.solve(-1.0j * w * I + A, Q))

            #print p_l.shape
            #print p_l
            #print transpose(rho).shape

            #print dot(p_l.full(), transpose(rho))
            s = dot(tr_vec,
                       dot(tm_l, dot(MMR, dot(p_l_m_p_r, transpose(rho)))))
            return -2 * real(s[0, 0])
        D,U = eig(L.full())

        Uinv = inv(U)

        Dint = diag(1.0/(1.0j*(wp-wd)*Idiag + diag(D)))

        Lint = U*Dint*Uinv


        #H_comm = -1.0j*(kron(It,H) - kron(transpose(H),It))


        #print H
        #print H.shape, H.full().shape
        #print H_comm, H_comm.shape
        #L = H_comm + Lindblad_tm + Lindblad_tp + Lindblad_deph
        #p_l=spre(p)
        #p_r=spost(p)
        #tm_l=spre(a)
        #print L.shape, A.shape,
        #print dir(L)
        #print L.eigenenergies().shape
        #print L.eigenstates()#.shape
        #L2 = [reshape(eye(dim),1,dim^2);L]; %Add the condition trace(rho) = 1
        #rho_ss = L2\[1;zeros(dim^2,1)]; % Steady state density matrix
        #rho_ss_c = rho_ss; %Column vector form

        #print "tm_l", tm_l.full().shape
        #print "Lint", Lint.shape
        #print "pl", p_l.full().shape
        #print "pr", p_r.full().shape
        #print "rho", to_super(rho_ss) #rho_ss.full().shape #rho.shape
        #print (tm_l.full()*Lint*(p_l.full() - p_r.full())*rho).shape
        #raise Exception
        return 1j*trace(tm_l*Lint*(p_l_m_p_r)*rho_ss)

value_grid=array(meshgrid(phi_arr, wd_vec))
vg=zip(value_grid[0, :, :].flatten(), value_grid[1, :, :].flatten())
print "1"
two_tone((0.23, 4000.0))
print "2"

fexpt=parallel_map(two_tone, vg,  progress_bar=True)
fexpt=reshape(fexpt, (len(wd_vec), len(phi_arr)))
pcolormesh(fexpt, cmap="RdBu_r")
colorbar()
show()
#arange(1,7).reshape(-1,2).transpose()
#        return (1.0/theta_steps)*1j*trace(reshape(tm_l*Lint*(p_l - p_r)*rho_ss_c,N,N))

#            Chi_temp(i,j) = Chi_temp(i,j) + (1/theta_steps)*1i*trace(reshape(tm_l*Lint*(p_l - p_r)*rho_ss_c,dim,dim));



#    r = (gamma/2)*Chi; % The reflection coefficient.
