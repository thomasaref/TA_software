# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:36:14 2016

@author: thomasaref
"""

from qutip import destroy, basis, steadystate, mesolve, expect, Qobj, qeye, spectrum
from matplotlib.pyplot import figure, plot, axhline, ylim, xlabel, ylabel, show, pcolormesh, colorbar
from numpy import array, sqrt, linspace, cos, pi, arange, diag, absolute, kron, exp, conj, transpose, full, real, imag, shape
from numpy.linalg import eig
from scipy.constants import h
from time import time

wlist2 = linspace(0.1, 1000.0, 200)
Omega_sim_points = 10
sample_power_sim_dBm=linspace(-100.0, -70, 3)
spk_external_att = 0.0
Omega_el_squared_coeff = 1.2*3.9666e+21  # Omega^2 in angular frequency = omega_el_square_coeff * gate_power_at_fridgetop
#sample_power_sim_dBm = linspace(spk_sample_power_dBm(1), spk_sample_power_dBm(end), Omega_sim_points)
gate_fridge_att = -83.0
power_fridgetop_sim = 1e-3*10**(0.1*(sample_power_sim_dBm + spk_external_att + gate_fridge_att))
print power_fridgetop_sim
Omega_sim_vec = sqrt((power_fridgetop_sim)*Omega_el_squared_coeff)
#Omega_sim_vec=linspace(1.0, 400.0, 31)
print Omega_sim_vec
#Omega=Omega_sim_vec
Ec = 0.22e9/1e6 # Charging energy.
Ejmax = 22.2e9/1e6 # Maximum Josephson energy.
wp = 4.8066e9/1e6
gamma = 38.2059e6*2*pi/(1e6*2*pi) # Relaxation rate of the transmon.
gamma_phi = 0*2*pi/(1e6*2*pi) # Dephasing rate of the transmon.
wd = 4.80661e9/1e6 # Drive frequency.

T = 21000* 0.03  # Temperature of the transmon bath in units of MHz (1K = 21 GHz).

N_gamma = 1/(exp(wd/T)-1)# % Thermal population of the transmon phonon bath around wd.

print N_gamma
N = 5  # number of basis states to consider

phi_arr=linspace(0.25, 0.35, 101)

a = destroy(N)
adag=a.dag()

tdiag = Qobj(diag(range(0, N))) # Diagonal matrix for the transmon.

It= qeye(N)
tdiag_l = kron(It,tdiag) # tdiag operator multiplying rho from the left.

tm_l = kron(It, a) # tm operator multiplying rho from the left.

kappa = 0.1  # coupling to oscillator

c_op_list = []

n_th_a = 2  # temperature with average of 2 excitations

rate = gamma * (1 + N_gamma)

c_op_list.append(sqrt(rate) * a)  # decay operators

rate = gamma * N_gamma

c_op_list.append(sqrt(rate) * adag)  # excitation operators


# Excitation (at T>0).

#Lindblad_deph = 0.5*gamma_phi*(kron(conj(2*tdiag),2*tdiag) -...
#                                    0.5*kron(Itot,ctranspose(2*tdiag)*2*tdiag) -...
#                                    0.5*kron(transpose(2*tdiag)*conj(2*tdiag),Itot));

p = -1.0j*(adag - a) # "P" operator.

p_l = kron(It,p) # % "P" operator multiplying rho from the left.
p_r = kron(transpose(p),It) # "P" operator multiplying rho from the right.


nvec=arange(N)
wdvec=nvec*wd
Ecvec=-Ec*(6.0*nvec**2+6.0*nvec+3.0)/12.0
def find_expect(phi=0.1, Omega_vec=3.0):

    Ej = Ejmax*absolute(cos(pi*phi)) #; % Josephson energy as function of Phi.

    wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec

    wT = wTvec-wdvec
    transmon_levels = Qobj(diag(wT[range(N)]))
    H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
    #final_state = steadystate(H, c_op_list)

    #U,D = eig(full(L))

    #Uinv = inv(U)

    # Doing the chi integral (gives the susceptibility)

    #Dint = 1.0/(1.0j*(wp-wd)) #Qobj(1.0/(1.0j*(wp-wd)*diag(qeye(N**2))))# + diag(D))))

    #Lint = U*Dint*Uinv

    #Chi_temp(i,j) += (1.0/theta_steps)*1j*trace(reshape(tm_l*Lint*(p_l - p_r)*rho_ss_c,dim,dim))

    return spectrum(H, wlist2, c_op_list, tm_l, p)
    return expect( a, final_state) #tm_l

def expect_update(phi_arr, Omega):
    tstart=time()
    Omega_vec=- 0.5j*(Omega*adag - conj(Omega)*a)
    fexp=[find_expect(phi, Omega_vec) for phi in phi_arr]
    print time()-tstart
    return fexp
#Omega=Omega_sim_vec[20]
fexpt=array([expect_update(phi_arr, Omega) for Omega in Omega_sim_vec])

#fexpt=[[find_expect(phi, Omega) for phi in phi_arr] for Omega in Omega_sim_vec]
#print fexpt
for i in range(len(Omega_sim_vec)):
    figure()
    Z=fexpt[i, :, :]
    pcolormesh(Z) #(Z-50.0)/(Z+50.0))
    colorbar()
show()
if 0:
    print "yo"
    tlist = linspace(0, 50, 100)

    #In [15]: mcdata = mcsolve(H, psi0, tlist, c_op_list, [a.dag() * a], ntraj=100)
    medata = mesolve(H, psi0, tlist, c_op_list, [a.dag() * a])

    figure()

    plot(tlist, medata.expect[0], lw=2)
    axhline(y=fexpt, color='r', lw=1.5) # ss expt. value as horiz line (= 2)

    ylim([0, 10])
    xlabel('Time', fontsize=14)
    ylabel('Number of excitations', fontsize=14)
    #legend(('Monte-Carlo', 'Master Equation', 'Steady State'))

    #title('Decay of Fock state $\left|10\\rangle\\right.$' +
     #' in a thermal environment with $\langle n\\rangle=2$')
    show()