# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 14:09:32 2016

@author: thomasaref
"""

from numpy import identity, pi, exp, kron, diag, transpose, conjugate, sqrt, zeros, cos, reshape, arange
from numpy.linalg import solve
from scipy import sparse
from scipy.constants import h

E_C=150.0
E_J_max=41000.0
Gamma_ac=38.0/(2*pi)
Gamma_Phi=0.0/(2*pi)
f0=5450.0
T=21000.0*0.0 # Temperature of the transmon bath in units of MHz (1K = 21 GHz).

Omega_vec=linpace(-500.0, 500.0, 1000)
phi_vec=linspace(-2.0, 2.0, 900)
Nt=5
###def Spike_simulation(Omega_vec, phi_vec, Nt, FixPointSteps, const):
###Omega_vec = Omega_vec/(2*pi*1e6);
# Eq. 5 from Anton's "TransmissionElectricToAcoustic.pdf":
#Omega_vec = 1e-6*2*sqrt(P_in*const.Gamma_el/(2*pi*const.hf0))

#Fel:
#Omega_vec = (1e-6/(2*pi))*2*sqrt(P_in*const.Gamma_el/(const.hf0));

#Omega_vec = 1e-6*2*sqrt(P_in/const.hf0)*sqrt(const.Gamma_el/(2*pi))

Omega_steps = len(Omega_vec)
phi_steps = len(phi_vec)

# Parameters

#Putting these in the form that the simulation code needs;
#E_C = const.EC/(1e6*const.h) # Charging energy.
#E_J_max = const.EJmax/(1e6*const.h) # Maximum Josephson energy.

gamma = Gamma_ac #const.Gamma_ac/(1e6*2*pi) # Relaxation rate of the transmon.
gamma_phi = Gamma_Phi#/(1e6*2*pi) # Dephasing rate of the transmon.
wd = f0#const.f0/1e6 # Drive frequency.


# ----------------------------------------
# From here on, it's purely Anton's code
# ----------------------------------------

N_gamma = 0.0 #1/(exp(wd/T)-1) # Thermal population of the transmon phonon bath around wd.

dim = Nt # Dimension of the total Hilbert space.

# Operators

It = sparse(identity(Nt)) # Unity matrix for the transmon.
Itot = It # Unity matrix for the total Hilbert space.

tm = sparse(diag(sqrt(range(1, Nt)),1)) # Lowering operator for the transmon.
tp = tm.transpose().conjugate() #ctranspose(tm) # Raising operator for the transmon.

tdiag = sparse(diag(range(Nt))) # Diagonal matrix for the transmon.

tdiag_l = kron(Itot,tdiag) # tdiag operator multiplying rho from the left.

tm_l = kron(Itot,tm) # tm operator multiplying rho from the left.

p = -1.0j*(tp - tm) # "P" operator.

# Dissipation terms

Lindblad_tm = gamma*(N_gamma+1)*(kron(tm.conjugate(),tm) -
                                    0.5*kron(Itot,tm.transpose().conjugate()*tm) -
                                    0.5*kron(tm.transpose()*tm.conjugate(),Itot))
# Relaxation.

Lindblad_tp = gamma*N_gamma*(kron(conj(tp),tp) -
                                    0.5*kron(Itot,ctranspose(tp)*tp) -...
                                    0.5*kron(transpose(tp)*conj(tp),Itot));
# Excitation (at T>0).

Lindblad_deph = 0.5*gamma_phi*(kron(conj(2*tdiag),2*tdiag) -...
                                    0.5*kron(Itot,ctranspose(2*tdiag)*2*tdiag) -...
                                    0.5*kron(transpose(2*tdiag)*conj(2*tdiag),Itot));
# Dephasing.
# Preparing storage matrices

CoherentOutput_temp = zeros(phi_steps,Omega_steps) # To store coherent output complex amplitude.
TotalOutputPower_temp = zeros(phi_steps,Omega_steps) # To store the total output power.
CoherentOutputPower_temp = zeros(phi_steps,Omega_steps) # To store coherent output power.
IncoherentOutputPower_temp = zeros(phi_steps,Omega_steps) # To store incoherent output power.

w01_vec = zeros(1,phi_steps) # To store transition energies.
w12_vec = zeros(1,phi_steps)
w23_vec = zeros(1,phi_steps)
w34_vec = zeros(1,phi_steps)
w45_vec = zeros(1,phi_steps)

# Looping over Omega

for k = range(Omega_steps):
    Omega = Omega_vec[k]
    # Looping over Phi
    for i = drange(1:phi_steps)

        phi = phi_vec(i);

        E_J = E_J_max*cos(pi*phi); # Josephson energy as function of Phi.

        wT_vec = -E_J + sqrt(8*E_J*E_C)*([0:Nt-1]+0.5)-E_C*(6*[0:Nt-1]**2+6*[0:Nt-1]+3)/12.0
        # Energy levels of the transmon.

        if k == Omega_steps

            w01_vec(i) = wT_vec(2)- wT_vec(1);
            w12_vec(i) = wT_vec(3)- wT_vec(2);
            w23_vec(i) = wT_vec(4)- wT_vec(3);
            w34_vec(i) = wT_vec(5)- wT_vec(4);
            w45_vec(i) = wT_vec(6)- wT_vec(5);

        end

        wT = wT_vec-[0:Nt-1]*wd;
        # Vector of the transmon level energies in the rotating frame of the drive.

        transmon_levels = sparse(diag(wT(1:Nt)));
        # Diagonal matrix with the transmon levels.

        # Fixpoint iteration

        a_ut = 0

        for j in range(FixPointSteps):

            Omega_true = Omega + 2*sqrt(gamma/2)*const.S22_0*exp(1i*2*const.theta_L)*a_ut;
            # Hamiltonian

            H = transmon_levels - 0.5j*(Omega_true*tp - conj(Omega_true)*tm);
            H_comm = -1.0j*(kron(Itot,H) - kron(transpose(H),Itot));

            # Liouvillian

            L = H_comm + Lindblad_tm + Lindblad_tp + Lindblad_deph

            # Calculating the steady state density matrix

            L2 = [reshape(eye(dim),1,dim^2);L]; #Add the condition trace(rho) = 1
	#arange(1,7).reshape(-1,2).transpose()
            rho_ss = L2\[1;zeros(dim^2,1)] # Steady state density matrix
            #linalg.solve(a,b)
            rho_ss_c = rho_ss #Column vector form

            a_ut = sqrt(gamma/2)*trace(reshape(tm_l*rho_ss_c,dim,dim));

        end

        CoherentOutput_temp(i,k) = a_ut;
 #       CoherentOutput_temp(i,k) = sqrt(gamma/2)*trace(reshape(tm_l*rho_ss_c,dim,dim));
        TotalOutputPower_temp(i,k) = abs((gamma/2)*trace(reshape(tdiag_l*rho_ss_c,dim,dim)));
        CoherentOutputPower_temp(i,k) = (abs(CoherentOutput_temp(i,k)))^2;
        IncoherentOutputPower_temp(i,k) = abs(TotalOutputPower_temp(i,k)-CoherentOutputPower_temp(i,k));

# Concatenate data from the different labs

#for cl in range(1,numlabs):
#    if labindex == cl:
#        labSend(CoherentOutput_temp,1,1)
#        labSend(TotalOutputPower_temp,1,2)
#        labSend(CoherentOutputPower_temp,1,3)
#        labSend(IncoherentOutputPower_temp,1,4)

#if labindex == 0
#    for c2 in range(1, numlabs):
#        CoherentOutput_temp = CoherentOutput_temp + labReceive[c2,0]
#        TotalOutputPower_temp = TotalOutputPower_temp + labReceive[c2,1]
#        CoherentOutputPower_temp = CoherentOutputPower_temp + labReceive[c2,2]
#        IncoherentOutputPower_temp = IncoherentOutputPower_temp + labReceive[c2,3]
#    CoherentOutput = CoherentOutput_temp
#    TotalOutputPower = TotalOutputPower_temp
#    CoherentOutputPower = CoherentOutputPower_temp
#    IncoherentOutputPower = IncoherentOutputPower_temp

    # Save the data

    #save filename... Chi gamma gamma_phi Omega_vec phi_vec wd_vec wp T Nt r

    #dlmwrite('reflection.txt', r,'\t')


# ---------------------------------------
# Martin's code again
# ----------------------------------------
# What comes out is the emission amplitude, with the
# unit of sqrt(megaphonons per second). Converting this to amplitude
# transmission coefficient
scale_factor = sqrt(1e6*const.hf0)#./repmat(sqrt(P_in), 1, phi_steps);

# Verified that this gives the same as the analytical expression:
coherent_S21 = (scale_factor.*CoherentOutput.');