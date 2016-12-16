# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:36:14 2016

@author: thomasaref
"""

from qutip import destroy, basis, steadystate, mesolve, expect, Qobj, qeye, spectrum, correlation_ss, correlation_2op_1t
from matplotlib.pyplot import figure, plot, axhline, ylim, xlabel, ylabel, show, pcolormesh, colorbar
from numpy import matrix, sin, interp, array, sqrt, linspace, cos, pi, arange, diag, absolute, kron, exp, conj, transpose, full, real, imag, shape
from numpy.linalg import eig, inv
from scipy.constants import h
from scipy.ndimage.interpolation import rotate
from time import time

wlist2 = linspace(-500.0, 500.0, 201)
Omega_sim_points = 10
sample_power_sim_dBm=-80.0 #linspace(-100.0, -70, 3)
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

phi_arr=linspace(0.2, 0.35, 51)
Ej_arr=linspace(10078, 17960, 51)
w0_arr=linspace(4211, 5622, 301)

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
print p_r

nvec=arange(N)
wdvec=nvec*wd
Ecvec=-Ec*(6.0*nvec**2+6.0*nvec+3.0)/12.0
def find_expect(phi=0.1, Omega_vec=3.0, wd=wd):

    Ej = (phi**2)/(8*Ec) #Ejmax*absolute(cos(pi*phi)) #; % Josephson energy as function of Phi.

    wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec

    #wdvec=nvec*sqrt(8.0*Ej*Ec)
    #wdvec=nvec*wd

    wT = wTvec-wdvec
    transmon_levels = Qobj(diag(wT[range(N)]))
    H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
    #final_state = steadystate(H, c_op_list)
    #print H.shape
    #print dir(H)
    #U,D = eig(H.full())
    #print D
    #Uinv = Qobj(inv(D))
    #U=Qobj(D)
    # Doing the chi integral (gives the susceptibility)

    #Dint = 1.0/(1.0j*(wp-wd)) #Qobj(1.0/(1.0j*(wp-wd)*diag(qeye(N**2))))# + diag(D))))

    #Hint = H.expm() #U*H*Uinv

    #Chi_temp(i,j) += (1.0/theta_steps)*1j*trace(reshape(tm_l*Lint*(p_l - p_r)*rho_ss_c,dim,dim))
    #exp1=correlation_2op_1t(H, None, wlist2, c_op_list, a, p, solver="es")
    #exp2=correlation_2op_1t(H, None, wlist2, c_op_list, p, a, solver="es", reverse=True)
    #exp1=correlation_2op_1t(H, None, wlist2, c_op_list, a, p_l-p_r, solver="es")

    #exp1=correlation_ss(H, wlist2, c_op_list, a, p)
    #exp2=correlation_ss(H, wlist2, c_op_list, p, a, reverse=True)
    exp1=spectrum(H, wlist2, c_op_list, a, p, solver="pi", use_pinv=True)
    exp2=spectrum(H, wlist2, c_op_list, p, a, solver="pi", use_pinv=False)
    return exp1-exp2
    return expect( a, final_state) #tm_l

def expect_update(phi_arr, Omega, wd):
    tstart=time()
    Omega_vec=- 0.5j*(Omega*adag - conj(Omega)*a)
    fexp=[find_expect(phi, Omega_vec, wd) for phi in phi_arr]
    print time()-tstart
    return fexp
Omega=Omega_sim_vec#[1]
fexpt=array(expect_update(w0_arr, Omega, wd))# for wd in wp+wlist2])
# for Omega in Omega_sim_vec])

#fexpt=[[find_expect(phi, Omega) for phi in phi_arr] for Omega in Omega_sim_vec]
#print fexpt
#for i in range(len(Omega_sim_vec)):

Ej = Ejmax*absolute(cos(pi*phi_arr)) #; % Josephson energy as function of Phi.
wTvec = sqrt(8.0*Ej*Ec)#*(nvec+0.5)
print Ej
#raise Exception
if 1:
    figure()
    #Z=fexpt[i, :, :]
    pcolormesh(wlist2, w0_arr, absolute(fexpt), cmap="RdBu_r") #(Z-50.0)/(Z+50.0))
    colorbar()
    figure()
    pcolormesh(wlist2, w0_arr, fexpt, cmap="RdBu_r")
    colorbar()

    figure()
    #Z=fexpt[i, :, :]
    pcolormesh(absolute(fexpt), cmap="RdBu_r") #(Z-50.0)/(Z+50.0))
    colorbar()
    figure()
    pcolormesh(fexpt, cmap="RdBu_r")
    colorbar()

    frot=rotate(fexpt, -45-90-3, reshape=False)
    figure()
    pcolormesh(wlist2[::-1], w0_arr, frot, cmap="RdBu_r")
    colorbar()
    #figure()
    #pcolormesh(imag(fexpt))
    #colorbar()

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