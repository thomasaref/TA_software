# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:36:14 2016

@author: thomasaref
"""

from qutip import destroy, basis, steadystate, mesolve, expect, Qobj, qeye, parallel_map, parfor
#from matplotlib.pyplot import figure, plot, axhline, ylim, xlabel, ylabel, show, pcolormesh
from numpy import log10, sqrt, linspace, cos, pi, arange, diag, absolute, kron, exp, conj, meshgrid, shape, array, reshape
from scipy.constants import h, k
from time import time
from taref.plotter.api import line, colormesh
from taref.physics.qubit import Qubit
from taref.core.api import SProperty, private_property
from atom.api import Float, Int

class Sat_Qubit(Qubit):
    sample_power_dBm=Float(-30.0)
    
    gamma=Float(38.0e6)
    gamma_phi=Float(0.0)
    
    T=Float(0.03)
    N_dim=Int(5)    
    
    fd=Float(4.5e9)
    N_gamma=SProperty()
    @N_gamma.getter
    def _get_N_gamma(self, fd, T):
        return 1.0/(exp(h*fd/(k*T))-1.0)
        
    #value_grid=array(meshgrid(phi_arr, Omega_sim_vec))
    
    @private_property
    def a_op(self):
        return destroy(self.N_dim)
        
    @private_property
    def adag(self):
        return self.a_op.dag()
        
    c_ops=SProperty().tag(sub=True)
    @c_ops.getter
    def _get_c_ops(self, gamma, N_gamma, a, adag):
        rate1 = gamma * (1 + N_gamma)
        rate2=gamma*N_gamma
        return [sqrt(rate1)*a, sqrt(rate2) * adag]

    @private_property
    def nvec(self):
        return arange(self.N_dim)

    @private_property
    def fdvec(self):
        return self.nvec*self.fd

    @private_property
    def Ecvec(self):
        return -self.Ec*(6.0*self.nvec**2+6.0*self.nvec+3.0)/12.0

    def find_expect(vg): #phi=0.1, Omega_vec=3.0):
        phi, Omega=vg#.shape
        Omega_vec=- 0.5j*(Omega*adag - conj(Omega)*a)
    
        Ej = Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.
    
        wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec #\omega_m
    
        wT = wTvec-wdvec #rotating frame of gate drive \omega_m-m*\omega_\gate
        transmon_levels = Qobj(diag(wT[range(N)]))
        H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
        final_state = steadystate(H, c_op_list) #solve master equation
    
        return expect( a, final_state) #expectation value of relaxation operator
        #Omega=\alpha\sqrt{2\Gamma_10} where |\alpha|^2=phonon flux=number of phonons per second
        #Omega=2\alpha\sqrt{\gamma} where |\alpha|^2=phonon flux=number of phonons per second
        

Omega_sim_points = 10
sample_power_sim_dBm=linspace(-100.0, -50, 31)
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

gamma = 38.2059e6*2*pi/(1e6*2*pi) # Relaxation rate of the transmon.
gamma_phi = 0*2*pi/(1e6*2*pi) # Dephasing rate of the transmon.
wd = 4.8066e9/1e6 # Drive frequency.

T = 21000* 0.03  # Temperature of the transmon bath in units of MHz (1K = 21 GHz).

N_gamma = 1.0/(exp(wd/T)-1.0)# % Thermal population of the transmon phonon bath around wd.

print N_gamma
N = 5  # number of basis states to consider

#Ejmax=30.0
#Ec=1.0
phi_arr=linspace(0.2, 0.3, 101)

value_grid=array(meshgrid(phi_arr, Omega_sim_vec))

a = destroy(N)
print a
adag=a.dag()
print adag
#tdiag = Qobj(diag(range(0, N))) # Diagonal matrix for the transmon.
#print tdiag
#It= qeye(N)
#tdiag_l = kron(It,tdiag) # tdiag operator multiplying rho from the left.

#tm_l = kron(It, a) # tm operator multiplying rho from the left.

#kappa = 0.1  # coupling to oscillator

c_op_list = []

#n_th_a = 2  # temperature with average of 2 excitations

rate = gamma * (1 + N_gamma)

c_op_list.append(sqrt(rate) * a)  # decay operators

rate = gamma * N_gamma

c_op_list.append(sqrt(rate) * adag)  # excitation operators


# Excitation (at T>0).

#Lindblad_deph = 0.5*gamma_phi*(kron(conj(2*tdiag),2*tdiag) -...
#                                    0.5*kron(Itot,ctranspose(2*tdiag)*2*tdiag) -...
#                                    0.5*kron(transpose(2*tdiag)*conj(2*tdiag),Itot));
nvec=arange(N)
wdvec=nvec*wd
Ecvec=-Ec*(6.0*nvec**2+6.0*nvec+3.0)/12.0
def find_expect(vg): #phi=0.1, Omega_vec=3.0):
    phi, Omega=vg#.shape
    Omega_vec=- 0.5j*(Omega*adag - conj(Omega)*a)

    Ej = Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.

    wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec #\omega_m

    wT = wTvec-wdvec #rotating frame of gate drive \omega_m-m*\omega_\gate
    transmon_levels = Qobj(diag(wT[range(N)]))
    H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
    final_state = steadystate(H, c_op_list) #solve master equation

    return expect( a, final_state) #expectation value of relaxation operator
    #Omega=\alpha\sqrt{2\Gamma_10} where |\alpha|^2=phonon flux=number of phonons per second
    #Omega=2\alpha\sqrt{\gamma} where |\alpha|^2=phonon flux=number of phonons per second

def expect_update(Omega):
    tstart=time()
    Omega_vec=- 0.5j*(Omega*adag - conj(Omega)*a)
    fexp=parallel_map(find_expect, phi_arr, task_kwargs=dict(Omega_vec=Omega_vec))# for phi in phi_arr]
    print time()-tstart
    return fexp

vg=zip(value_grid[0, :, :].flatten(), value_grid[1, :, :].flatten())
fexpt=parallel_map(find_expect, vg,  progress_bar=True)
fexpt=reshape(fexpt, (31, 101))
#fexpt=[expect_update(Omega) for Omega in Omega_sim_vec]

#fexpt=[[find_expect(phi, Omega) for phi in phi_arr] for Omega in Omega_sim_vec]
#print fexpt
colormesh(phi_arr, sample_power_sim_dBm, absolute(fexpt), cmap="RdBu_r")
#figure()
colormesh(absolute(fexpt), cmap="RdBu_r")
#figure()
line(sample_power_sim_dBm, 20*log10(absolute(fexpt)[:, 77])-sample_power_sim_dBm)
#figure()
line(sample_power_sim_dBm, 10**((20*log10(absolute(fexpt)[:, 77])-sample_power_sim_dBm)/10.0)).show()

#plot(phi_arr, absolute(fexpt))
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