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
from qutip import qeye, destroy, tensor, spre, spost, operator_to_vector, vector_to_operator, to_super, num
import qutip
#print dir(qutip)
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
qtdiag=num(Nt)
qtdiagdag=qtdiag.dag()
#print tdiag
#print num(Nt)

tdiag_l = kron(Itot,tdiag) # tdiag operator multiplying rho from the left.
print tdiag_l

tm_l = kron(Itot,tm) # tm operator multiplying rho from the left.

#print tm_l
tensor(qeye(Nt), destroy(Nt)).data
qIt=qeye(Nt)
p = -1.0j*(tp - tm) # "P" operator.
print tensor(qIt, num(Nt)).data==tdiag_l

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
lb_tm=gamma*(N_gamma+1)*(tensor(a.conj(), a)-0.5*tensor(qIt, adag*a)-0.5*tensor(adag*a, qIt))
print lb_tm.data==Lindblad_tm

print num(Nt)
#print tensor(a.conj(), a).data==kron(tm.conjugate(),tm)
#print kron(tm.conjugate(),tm)
#print tensor(a, adag).data
#print tensor(adag, a).data==kron(tm.conjugate(),tm)

#print 0.5*kron(Itot,dot(tm.transpose().conjugate(), tm))==0.5*tensor(qIt, adag*a).data
#print 0.5*kron(dot(tm.transpose(), tm.conjugate()),Itot)==0.5*tensor(adag*a, qIt).data
#print Lindblad_tm==lb_tm.data
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
lb_tp=gamma*N_gamma*(tensor(adag.conj(), adag)-0.5*tensor(qIt,a*adag)-0.5*tensor(a*adag, qIt))
#print lb_tp
print Lindblad_tp==lb_tp.data
# Excitation (at T>0).

#Lindblad_deph = 0.5*gamma_phi*(kron(conj(2*tdiag),2*tdiag) -...
#                                    0.5*kron(Itot,ctranspose(2*tdiag)*2*tdiag) -...
#                                    0.5*kron(transpose(2*tdiag)*conj(2*tdiag),Itot));

Lindblad_deph = 0.5*gamma_phi*(kron(2*tdiag.conjugate(),2*tdiag) -
                                    0.5*kron(Itot,dot(2*tdiag.conjugate().transpose(), 2*tdiag)) -
                                    0.5*kron(dot(2*tdiag.transpose(), 2*tdiag.conjugate()),Itot))
lp_deph= 0.5*gamma_phi*(tensor(2*qtdiag.conj(), 2*qtdiag)-0.5*tensor(qIt, 2*qtdiagdag*2*qtdiag)
    -0.5*tensor(2*qtdiagdag*2*qtdiag, qIt))

print Lindblad_deph==lp_deph.data

# Preparing storage matrices

CoherentOutput_temp = zeros((phi_steps,Omega_steps)) # To store coherent output complex amplitude.
TotalOutputPower_temp = zeros((phi_steps,Omega_steps)) # To store the total output power.
CoherentOutputPower_temp = zeros((phi_steps,Omega_steps)) # To store coherent output power.
IncoherentOutputPower_temp = zeros((phi_steps,Omega_steps)) # To store incoherent output power.

w01_vec = zeros(phi_steps) # To store transition energies.
w12_vec = zeros(phi_steps)
w23_vec = zeros(phi_steps)
w34_vec = zeros(phi_steps)
w45_vec = zeros(phi_steps)

# Looping over Omega
Nt_vec=arange(Nt)

for k in range(Omega_steps):

    Omega = Omega_vec[k]

    # Looping over Phi

    for i in range(phi_steps):

        phi = phi_vec[i]

        E_J = E_J_max*cos(pi*phi) # Josephson energy as function of Phi.
        wT_vec = -E_J + sqrt(8.0*E_J*E_C)*(Nt_vec+0.5)-E_C*(6*Nt_vec**2+6*Nt_vec+3)/12.0
        # Energy levels of the transmon.

        if k == Omega_steps-1:

            w01_vec[i] = wT_vec[2]- wT_vec[1]
            w12_vec[i] = wT_vec[3]- wT_vec[2]
            w23_vec[i] = wT_vec[4]- wT_vec(3);
            w34_vec[i] = wT_vec(5)- wT_vec(4);
            w45_vec[i] = wT_vec(6)- wT_vec(5);

        wT = wT_vec-Nt_vec*wd
        # Vector of the transmon level energies in the rotating frame of
        # the drive.

        transmon_levels = diag(wT(1:Nt)));
        % Diagonal matrix with the transmon levels.

        %% Fixpoint iteration

        a_ut = 0;

        for j = 1:FixPointSteps

            Omega_true = Omega + 2*sqrt(gamma/2)*const.S22_0*exp(1i*2*const.theta_L)*a_ut;
            %% Hamiltonian

            H = transmon_levels - 0.5*1i*(Omega_true*tp - conj(Omega_true)*tm);
            H_comm = -1i*(kron(Itot,H) - kron(transpose(H),Itot));

            %% Liouvillian

            L = H_comm + Lindblad_tm + Lindblad_tp + Lindblad_deph;

            %% Calculating the steady state density matrix

            L2 = [reshape(eye(dim),1,dim^2);L]; %Add the condition trace(rho) = 1

            rho_ss = L2\[1;zeros(dim^2,1)]; % Steady state density matrix

            rho_ss_c = rho_ss; %Column vector form

            a_ut = sqrt(gamma/2)*trace(reshape(tm_l*rho_ss_c,dim,dim));

        end

        CoherentOutput_temp(i,k) = a_ut;
 %       CoherentOutput_temp(i,k) = sqrt(gamma/2)*trace(reshape(tm_l*rho_ss_c,dim,dim));
        TotalOutputPower_temp(i,k) = abs((gamma/2)*trace(reshape(tdiag_l*rho_ss_c,dim,dim)));
        CoherentOutputPower_temp(i,k) = (abs(CoherentOutput_temp(i,k)))^2;
        IncoherentOutputPower_temp(i,k) = abs(TotalOutputPower_temp(i,k)-CoherentOutputPower_temp(i,k));

    end

end