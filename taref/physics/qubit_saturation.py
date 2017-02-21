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
from taref.core.api import SProperty, private_property, Array
from atom.api import Float, Int, Callable

class Sat_Qubit(Qubit):
    #sample_power_dBm=Float(-30.0)
    atten=Float(83.0)
    phi_arr=Array()
    pwr_arr=Array()

    def _default_phi_arr(self):
        return linspace(0.2, 0.3, 101)

    def _default_pwr_arr(self):
        return linspace(-50.0, 0, 31)

    gamma=Float(38.0e6)
    gamma_el=Float(0.750e6)
    gamma_phi=Float(0.0)

    T=Float(0.03)
    N_dim=Int(5)

    fd=Float(4.5e9)

    N_gamma=SProperty()
    @N_gamma.getter
    def _get_N_gamma(self, fd, T):
        return 1.0/(exp(h*fd/(k*T))-1.0)

    @private_property
    def a_op(self):
        return destroy(self.N_dim)

    @private_property
    def a_dag(self):
        return self.a_op.dag()

    c_ops=SProperty().tag(sub=True)
    @c_ops.getter
    def _get_c_ops(self, gamma, N_gamma, a_op, a_dag):
        rate1 = gamma * (1 + N_gamma)
        rate2=gamma*N_gamma
        return [sqrt(rate1)*a_op, sqrt(rate2) * a_dag]

    @private_property
    def nvec(self):
        return arange(self.N_dim)

    @private_property
    def fdvec(self):
        return self.nvec*self.fd

    @private_property
    def Ecvec(self):
        return -self.Ec*(6.0*self.nvec**2+6.0*self.nvec+3.0)/12.0

    @private_property
    def pwr_lin(self):
        pwr_fridge=self.pwr_arr-self.atten
        return 0.001*10**(pwr_fridge/10.0)
        
    @private_property
    def Omega_arr(self):
        pwr_fridge=self.pwr_arr-self.atten
        return sqrt(0.001*10**(pwr_fridge/10.0)/(h*a.fd))*sqrt(2*self.gamma_el)

    @private_property
    def value_grid(self):
        value_grid=array(meshgrid(self.phi_arr, self.Omega_arr))
        return zip(value_grid[0, :, :].flatten(), value_grid[1, :, :].flatten())

    funcer=Callable()
#    @private_property
#    def funcer(self):
#        def find_expect2(vg): #phi=0.1, Omega_vec=3.0):
#            phi, Omega=vg#.shape
#            Omega_vec=-0.5j*(Omega*a.a_dag - conj(Omega)*a.a_op)
#
#            Ej = a.Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.
#
#            wTvec = (-Ej + sqrt(8.0*Ej*a.Ec)*(a.nvec+0.5)+a.Ecvec)/h #\omega_m
#
#            wT = wTvec-a.fdvec #rotating frame of gate drive \omega_m-m*\omega_\gate
#            transmon_levels = Qobj(diag(wT[range(a.N_dim)]))
#            H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
#            final_state = steadystate(H, a.c_ops) #solve master equation
#
#            return expect( a.a_op, final_state) #expectation value of relaxation operator
#            #Omega=\alpha\sqrt{2\Gamma_10} where |\alpha|^2=phonon flux=number of phonons per second
#            #Omega=2\alpha\sqrt{\gamma} where |\alpha|^2=phonon flux=number of phonons per second
#
#        return find_expect
    
#Omega=2 a sqrt(gamma_el)  a^2=number of photons/s=
#a=sqrt(pwr/hf)
#t=sqrt(gamma/2/(pwr/hf)<>

#t=log(sqrt(gamma/2)<>-log(pwr/hf)

    @private_property
    def fexpt(self):
        #vg=self.value_grid
        fexpt=parallel_map(self.funcer, self.value_grid,  progress_bar=True)
        return reshape(fexpt, (len(self.pwr_arr), len(self.phi_arr)))

if __name__=="__main__":
    a=Sat_Qubit()
    #print a.Ec/h
    #raise Exception

    a.Ec = 0.22e9*h # Charging energy.
    a.Ejmax = 22.2e9*h # Maximum Josephson energy.

    a.gamma = 38.2059e6 # Acoustic relaxation rate of the transmon.
    a.gamma_el=0.750e6 #electric relaxation rate
    a.gamma_phi = 0.0e6 # Dephasing rate of the transmon.
    a.fd = 4.8066e9#/1e6 # Drive frequency.

    def find_expect(vg, self=a): #phi=0.1, Omega_vec=3.0):
            phi, Omega=vg#.shape
            Omega_vec=-0.5j*(Omega*self.a_dag - conj(Omega)*self.a_op)

            Ej = self.Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.

            wTvec = (-Ej + sqrt(8.0*Ej*self.Ec)*(self.nvec+0.5)+self.Ecvec)/h #\omega_m

            wT = wTvec-a.fdvec #rotating frame of gate drive \omega_m-m*\omega_\gate
            transmon_levels = Qobj(diag(wT[range(self.N_dim)]))
            H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
            final_state = steadystate(H, self.c_ops) #solve master equation

            return expect( self.a_op, final_state) #expectation value of relaxation operator
            #Omega=\alpha\sqrt{2\Gamma_10} where |\alpha|^2=phonon flux=number of phonons per second
            #Omega=2\alpha\sqrt{\gamma} where |\alpha|^2=phonon flux=number of phonons per second
        #return find_expec
    a.funcer=find_expect
    colormesh(a.phi_arr, a.pwr_arr, absolute(a.fexpt), cmap="RdBu_r")
    colormesh(absolute(a.fexpt), cmap="RdBu_r")
    pd=20*log10(absolute(a.fexpt)[:, 77]*sqrt(a.gamma/2.0*h*a.fd/a.pwr_lin))
    line(a.pwr_arr, pd) #20*log10(absolute(a.fexpt)[:, 77]*sqrt(a.gamma/2.0*h*a.fd/a.pwr_lin)))
    line(a.pwr_arr, 10**(pd/10.0)).show()

# Excitation (at T>0).

#Lindblad_deph = 0.5*gamma_phi*(kron(conj(2*tdiag),2*tdiag) -...
#                                    0.5*kron(Itot,ctranspose(2*tdiag)*2*tdiag) -...
#                                    0.5*kron(transpose(2*tdiag)*conj(2*tdiag),Itot));
