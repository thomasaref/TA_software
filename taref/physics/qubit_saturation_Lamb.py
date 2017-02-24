# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:36:14 2016

@author: thomasaref
"""

from qutip import destroy, basis, steadystate, mesolve, expect, Qobj, qeye, parallel_map, parfor
from numpy import log10, sqrt, linspace, cos, pi, arange, diag, absolute, kron, exp, conj, meshgrid, shape, array, reshape
from scipy.constants import h, k
from time import time
from taref.plotter.api import line, colormesh
from taref.physics.qubit import Qubit
from taref.core.api import SProperty, private_property, Array
from atom.api import Float, Int, Callable

from qutip.fastsparse import fast_csr_matrix#, fast_identity
from numpy import integer, int32, sin, diff

def Lamb_destroy(self, phi, fd, N, offset=0):
    if not isinstance(N, (int, integer)):  # raise error if N not integer
        raise ValueError("Hilbert space dimension must be integer value")

    if 0:
        Ej = self.Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.
    
        fvec = (-Ej + sqrt(8.0*Ej*self.Ec)*(self.nvec+0.5)+self.Ecvec)/h #\omega_m
        X=self.Np*pi*(diff(fvec)-self.f0)/self.f0
    if 1:
        #nvec=arange(N-1)
        X=self.Np*pi*(fd-self.f0)/self.f0
    gamma=0.1*fd/5e9+(sin(X)/(self.Np*sin(X/self.Np)))**2    
    data = gamma*sqrt(arange(offset+1, N+offset, dtype=complex))
    ind = arange(1,N, dtype=int32)
    ptr = arange(N+1, dtype=int32)
    ptr[-1] = N-1
    return Qobj(fast_csr_matrix((data,ind,ptr),shape=(N,N)), isherm=False)

class Sat_Qubit(Qubit):
    atten=Float(83.0)
    phi_arr=Array()
    pwr_arr=Array()
    frq_arr=Array()

    Np=Int(9)
    f0=Float(4.50001e9)
    def _default_phi_arr(self):
        return linspace(0.1, 0.5, 500)

    def _default_pwr_arr(self):
        return linspace(-50.0, 0, 31)

    def _default_frq_arr(self):
        return linspace(2.0e9, 8.0e9, 501)

    gamma=Float(38.0e6)
    gamma_el=Float(0.750e6)
    gamma_phi=Float(0.0)

    T=Float(0.03)
    N_dim=Int(8)

    fd=Float(4.5e9)
    
    Zc=Float(50.0)
    Cc=Float(0.0)
    Ct=Float(100.0e-15)

    Gamma_C=SProperty()
    @Gamma_C.getter
    def _get_Gamma_C(self, fd, Cc,Ct, Zc):
        return 2*pi*(Zc*Cc**2*fd**2)/(4*(Cc+Ct))

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

    @private_property
    def tdiag(self):
        return Qobj(diag(range(0, 2*self.N_dim, 2))) #dephasing operator, tdiag        

    c_ops=SProperty().tag(sub=True)
    @c_ops.getter
    def _get_c_ops(self, gamma, N_gamma, a_op, a_dag, tdiag, gamma_phi):
        rate1 = gamma * (1 + N_gamma)
        rate2=gamma*N_gamma
        return [sqrt(rate1)*a_op, sqrt(rate2) * a_dag, gamma_phi*tdiag]

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
        value_grid=array(meshgrid(self.phi_arr, self.frq_arr))
        #value_grid=array(meshgrid(self.phi_arr, self.Omega_arr))
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
    

    @private_property
    def fexpt(self):
        fexpt=parallel_map(self.funcer, self.value_grid,  progress_bar=True)
        return reshape(fexpt, (len(self.frq_arr), len(self.phi_arr)))

if __name__=="__main__":
    a=Sat_Qubit()
    a.N_dim=8
    #print a.Ec/h
    #raise Exception
    a.atten=83+20
    a.Ec = 0.22e9*h # Charging energy.
    a.Ejmax = 22.2e9*h # Maximum Josephson energy.

    a.gamma = 538.2059e6 # Acoustic relaxation rate of the transmon.
    a.gamma_el=a.gamma #0.750e6 #electric relaxation rate
    a.gamma_phi = 0.01e6 # Dephasing rate of the transmon.
    a.fd = 4.8066e9#/1e6 # Drive frequency.

    def find_expect(vg, self=a): #phi=0.1, Omega_vec=3.0):
            phi, Omega=vg#.shape
            Omega_vec=-0.5j*(Omega*self.a_dag - conj(Omega)*self.a_op)

            Ej = self.Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.

            wTvec = (-Ej + sqrt(8.0*Ej*self.Ec)*(self.nvec+0.5)+self.Ecvec)/h #\omega_m

            #rate1 = gamma * (1 + N_gamma)
            #rate2=gamma*N_gamma
            #c_ops=[sqrt(rate1)*a_op, sqrt(rate2) * a_dag]

            wT = wTvec-a.fdvec #rotating frame of gate drive \omega_m-m*\omega_\gate
            transmon_levels = Qobj(diag(wT[range(self.N_dim)]))
            H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
            
            a_op=Lamb_destroy(a, phi, a.N_dim)
            a_dag=a_op.dag()
            rate1 = a.gamma * (1 + a.N_gamma)
            rate2=a.gamma*a.N_gamma
            c_ops=[sqrt(rate1)*a_op, sqrt(rate2) * a_dag]
            
            final_state = steadystate(H, c_ops) #solve master equation

            return expect( self.a_op, final_state) #expectation value of relaxation operator
            #Omega=\alpha\sqrt{2\Gamma_10} where |\alpha|^2=phonon flux=number of phonons per second
            #Omega=2\alpha\sqrt{\gamma} where |\alpha|^2=phonon flux=number of phonons per second

    Omega=a.Omega_arr[5]
    def find_expect2(vg, self=a): #phi=0.1, Omega_vec=3.0):
            phi, fd=vg#.shape

            Ej = self.Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.

            wTvec = (-Ej + sqrt(8.0*Ej*self.Ec)*(self.nvec+0.5)+self.Ecvec)/h #\omega_m

            #rate1 = gamma * (1 + N_gamma)
            #rate2=gamma*N_gamma
            #c_ops=[sqrt(rate1)*a_op, sqrt(rate2) * a_dag]
            #X=self.Np*pi*(diff(wTvec)-self.f0)/self.f0
            
            #Delta=a.gamma*(sin(2*X)-2*X)/(2*X**2)
            #delt_arr=[0.0]
            #delt_arr.extend(Delta[:])
            
            X=self.Np*pi*(fd-self.f0)/self.f0
            Delta=a.gamma*(sin(2*X)-2*X)/(2*X**2)
            wT = wTvec+(-Delta-fd)*a.nvec #rotating frame of gate drive \omega_m-m*\omega_\gate
            
            #wT = wTvec+array(delt_arr)-fd*a.nvec #rotating frame of gate drive \omega_m-m*\omega_\gate
            transmon_levels = Qobj(diag(wT[range(self.N_dim)]))

            a_op=Lamb_destroy(self=a, phi=phi, fd=fd, N=a.N_dim)
            a_dag=a_op.dag()

            rate1 = a.gamma * (1 + a.N_gamma)
            rate2=a.gamma*a.N_gamma
            c_ops=[sqrt(rate1)*a_op, sqrt(rate2) * a_dag]

            Omega_vec=-0.5j*(Omega*a_dag - conj(Omega)*a_op)
            H=transmon_levels +Omega_vec #- 0.5j*(Omega_true*adag - conj(Omega_true)*a)
            
            final_state = steadystate(H, c_ops) #solve master equation

            
            #final_state = steadystate(H, self.c_ops) #solve master equation

            #return expect( self.a_op, final_state) #expectation value of relaxation operator
            return expect( a_op, final_state) #expectation value of relaxation operator
                        
            #Omega=\alpha\sqrt{2\Gamma_10} where |\alpha|^2=phonon flux=number of phonons per second
            #Omega=2\alpha\sqrt{\gamma} where |\alpha|^2=phonon flux=number of phonons per second

    a.funcer=find_expect2

    if 1:
        #colormesh(a.phi_arr, a.pwr_arr, absolute(a.fexpt), cmap="RdBu_r")
        pl=colormesh(a.phi_arr, a.frq_arr, absolute(a.fexpt), cmap="RdBu_r")

        pl=colormesh(a.phi_arr, a.frq_arr, 10*log10(absolute(a.fexpt)), cmap="RdBu_r")

        pl=colormesh(a.phi_arr, a.frq_arr, 10*log10(absolute(a.fexpt))-10*log10(absolute(a.fexpt[-1,:])), cmap="RdBu_r")
        pl=colormesh(a.phi_arr, a.frq_arr, (10*log10(absolute(a.fexpt)).transpose()-10*log10(absolute(a.fexpt[:,-1]))).transpose(), cmap="RdBu_r")

        #pd=10*log10(absolute(a.fexpt)[:, 77]*sqrt(a.gamma/2.0*h*a.fd/a.pwr_lin))
        #line(a.pwr_arr, pd) #20*log10(absolute(a.fexpt)[:, 77]*sqrt(a.gamma/2.0*h*a.fd/a.pwr_lin)))
        #pl=line(a.pwr_arr, 10**(pd/10.0), color="green")#.show()
        #pl=line(a.pwr_arr, ((absolute(a.fexpt)[:, 77])*1.08*sqrt(a.gamma/2.0*h*a.fd/a.pwr_lin)),
        #        color="red",
        #        pl=pl)

        g=a.gamma/2.0
        N=a.pwr_lin/(h*a.fd)#*abs(const.S21_0/(1+const.S22_0*exp(2i*const.theta_L)))^2
        Ej = a.Ejmax*absolute(cos(pi*a.phi_arr)) #Josephson energy as function of Phi.
        wTvec = (sqrt(8.0*Ej*a.Ec)-a.Ec)/h #\omega_m
        line(a.phi_arr, wTvec, pl=pl).show()


    print Lamb_destroy(a, 0.3, 8)        
    dw = wTvec-a.fd#rotating frame of gate drive \omega_m-m*\omega_\gate
    dw=0.0
    print a.fd
    print wTvec
    print dw
    print N[0]
    print a.a_op*2
    
    #Omega=2 a sqrt(gamma_el)  a^2=number of photons/s=
    #a=sqrt(pwr/hf)
    #t=sqrt(gamma/2/(pwr/hf)<>
    
    #t=log(sqrt(gamma/2)<>-log(pwr/hf)

    #2*(Omega/gamma)**2
    #Omega =sqrt(N)sqrt(2gamma)
    #Omega**2/gamma^2=N2/gamma
    def r_qubit(N):
        return -sqrt(a.gamma_el*g/2.0)/g*(1+1j*dw/g)/(1.0+dw**2/g**2+2*N/g*(a.gamma_el/(2.0*g)))

        #return -(a.gamma_el/(2.0*g))*(1+1j*dw/g)/(1.0 + dw**2/g**2 + 2*N/g*a.gamma_el/g)            

    #def t_qubit(N):
        #-sqrt(a.gamma_el*a.gamma/2.0)*(1j*dw+g)/(dw**2+g**2+Omega**2/2)
    #    return -sqrt(a.gamma_el*a.gamma/2.0)/g*(1+1j*dw)/(1.0+dw**2/g**2+2*N/g)

    #    return -(a.gamma_el/(2.0*g))*(1+1j*dw/g)/(1.0 + dw**2/g**2 + 2*N/g)            

    #P21(d_omega_idx, N_idx) = -sqrt(2*x*(1-x))*0.5*G*(g+1i*dw)./(dw^2 + g^2 + 4*x*g*N);
    #Omega = 2*sqrt(N_in(N_idx)*const.Gamma_el/(2*pi));
    #t(d_omega_idx, N_idx) = sqrt(0.5*const.Gamma_ac*const.Gamma_el)*(1i*d_omega(d_omega_idx) - const.Gamma_tot/2)./(d_omega(d_omega_idx).^2 + const.Gamma_tot^2/4 + Omega^2/2);
    
    #P21(d_omega_idx, O_idx) = -(g+1i*dw)./(dw^2 + g^2 + (g/G)*Omega(O_idx).^2);
    
    #pl="blah"
    line(a.pwr_arr, absolute(r_qubit(N)), pl=pl).show()

#    for n in N:   
#        line(absolute(r_qubit(n)), pl=pl)#.show()
#    def r_maxmin():
#        return [max(absolute(r_qubit(n))) for n in N]
#    line(a.pwr_arr, r_maxmin()).show()
    #line(a.pwr_arr, absolute([max(r_qubit(n) for n in N]))
# Excitation (at T>0).

#Lindblad_deph = 0.5*gamma_phi*(kron(conj(2*tdiag),2*tdiag) -...
#                                    0.5*kron(Itot,ctranspose(2*tdiag)*2*tdiag) -...
#                                    0.5*kron(transpose(2*tdiag)*conj(2*tdiag),Itot));
