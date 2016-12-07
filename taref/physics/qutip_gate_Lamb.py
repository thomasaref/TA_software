# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:36:14 2016

@author: thomasaref
"""

from qutip import destroy, basis, steadystate, mesolve, expect, Qobj, qeye
from taref.plotter.api import colormesh
#from matplotlib.pyplot import figure, plot, axhline, ylim, xlabel, ylabel, show, pcolormesh
from numpy import sqrt, linspace, cos, pi, arange, diag, absolute, kron, exp, conj, diff, zeros, sin
from scipy.constants import h, epsilon_0 as eps0
from time import time

Omega_sim_points = 10
sample_power_sim_dBm=-35.0 #linspace(-70.0, -20, 11)
spk_external_att = 0.0
Omega_el_squared_coeff = 1.2*3.9666e+21  # Omega^2 in angular frequency = omega_el_square_coeff * gate_power_at_fridgetop
#sample_power_sim_dBm = linspace(spk_sample_power_dBm(1), spk_sample_power_dBm(end), Omega_sim_points)
gate_fridge_att = -83.0
power_fridgetop_sim = 1e-3*10**(0.1*(sample_power_sim_dBm + spk_external_att + gate_fridge_att))
print power_fridgetop_sim
Omega_sim_vec = sqrt((power_fridgetop_sim)*Omega_el_squared_coeff)
#Omega_sim_vec=linspace(1.0, 400.0, 31)
print Omega_sim_vec
Omega=Omega_sim_vec

Npi=81
f0i=4.4601e9/1e6

Np=5
f0=4.40e9/1e6
W=25e-6
epsinf=46*eps0
Dvv=0.024

Ec = 0.302e9/1e6 # Charging energy.
Ejmax = 67.95e9/1e6 # Maximum Josephson energy.

gamma = 500e6*2*pi/(1e6*2*pi) # Relaxation rate of the transmon.
gamma_phi = 0*2*pi/(1e6*2*pi) # Dephasing rate of the transmon.
wd = 4.8066e9/1e6 # Drive frequency.

T = 21000* 0.03  # Temperature of the transmon bath in units of MHz (1K = 21 GHz).

N_gamma = 1/(exp(wd/T)-1)# % Thermal population of the transmon phonon bath around wd.

print N_gamma
N = 5  # number of basis states to consider

#Ejmax=30.0
#Ec=1.0
phi_arr=linspace(0.4, 0.5, 101)

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

#def lamb_shift()
#    Em=-Ej+sqrt(8.0*Ej*Ec)*(m+0.5) - (Ec/12.0)*(6.0*m**2+6.0*m+3.0)
#    if m==0:
#            return Em
#        Emm1=-Ej+sqrt(8.0*Ej*Ec)*(m-1+0.5) - (Ec/12.0)*(6.0*(m-1)**2+6.0*(m-1)+3.0)
#        fq=(Em-Emm1)/h
#        fls=self._get_Lamb_shift(f=fq, f0=f0, ft_mult=ft_mult, eta=eta, epsinf=epsinf, W=W, Dvv=Dvv, Np=Np, Ct_mult=Ct_mult)
#        return Em+h*fls


nvec=arange(N)
wdvec=nvec*wd
Ecvec=-Ec*(6.0*nvec**2+6.0*nvec+3.0)/12.0
Y0=pi*f0*W*epsinf/Dvv
mu=sqrt(2.0)*1.2472j*Dvv*Np
Ga0=2.0*Y0*absolute(mu)**2
Ct=sqrt(2)*W*epsinf*Np

def find_expect(phi=0.1, Omega_vec=3.0, wd=wd):

    wdvec=nvec*wd

    Ej = Ejmax*absolute(cos(pi*phi)) #; % Josephson energy as function of Phi.
    wq0=sqrt(8*Ej*Ec)
    X=Np*pi*(wq0-f0)/f0
    Ba=-1*gamma*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
    Ecp=Ec*(1-2*Ba/wq0)
    Ecvec=-Ecp*(6.0*nvec**2+6.0*nvec+3.0)/12.0

    wTvec = -Ej + sqrt(8.0*Ej*Ecp)*(nvec+0.5)+Ecvec


    #print diff(wTvec)
    if phi==0.4:
        print Ba/wq0
    if 0:
        zr=zeros(N)
        X=Np*pi*(diff(wTvec)-f0)/f0
        Ba=-0*gamma*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
        ls=-Ba#/(2*Ct)/(2*pi)#/1e6
        zr[1:]=ls
        #print Ga0/(2*Ct)/(2*pi)
        #print zr
        wTvec=wTvec+zr
    wTvec = wTvec-wdvec

    #print wTvec+diff(wTvec)


    transmon_levels = Qobj(diag(wTvec[range(N)]))

    H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
    final_state = steadystate(H, c_op_list)

    return expect( tm_l, final_state)

def expect_update(phi_arr, Omega, wd=wd):
    tstart=time()
    Xi=Npi*pi*(wd-f0i)/f0i
    Omega_r=Omega*(sin(Xi)/Xi)**2

    Omega_vec=- 0.5j*(Omega_r*adag - conj(Omega_r)*a)
    fexp=[find_expect(phi, Omega_vec, wd) for phi in phi_arr]
    print time()-tstart
    return fexp

fexpt=[expect_update(phi_arr, Omega, wdd) for wdd in linspace(4.2e9/1e6, 4.8e9/1e6, 91)] #Omega in Omega_sim_vec]

#fexpt=[[find_expect(phi, Omega) for phi in phi_arr] for Omega in Omega_sim_vec]
#print fexpt
colormesh( absolute(fexpt), cmap="RdBu_r").show() #phi_arr, sample_power_sim_dBm,
#plot(phi_arr, absolute(fexpt))
#show()
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