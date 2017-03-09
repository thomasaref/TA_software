# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:36:14 2016

@author: thomasaref
"""

from qutip import destroy, basis, steadystate, mesolve, expect, Qobj, qeye, parallel_map, parfor
from numpy import arccos, sin, append, log10, sqrt, linspace, cos, pi, arange, diag, absolute, exp, conj, meshgrid, array, reshape, shape
from scipy.constants import h, k
from taref.plotter.api import line, colormesh
from taref.physics.qubit import Qubit
from taref.core.api import SProperty, private_property, Array
from atom.api import Float, Int, Callable, Bool
from scipy.constants import e
print e
#from qutip.fastsparse import fast_csr_matrix#, fast_identity
#from numpy import integer, int32, sin, diff


class Sat_Qubit(Qubit):
    atten=Float(83.0)
    phi_arr=Array()
    pwr_arr=Array()
    frq_arr=Array()
    
    do_ls=Bool(True)
    harm_osc=Bool(False)

    Np=Int(9)
    f0=Float(5.30001e9)
    def _default_phi_arr(self):
        return linspace(0.2, 0.4, 150)*pi

    def _default_pwr_arr(self):
        return linspace(-50.0, 0, 31)

    def _default_frq_arr(self):
        return linspace(3.5e9, 7.5e9, 51)

    gamma=Float(38.0e6)
    gamma_el=Float(0.750e6)
    gamma_phi=Float(0.0)

    T=Float(0.03)
    N_dim=Int(8)

    fd=Float(4.5e9)

    Zc=Float(50.0)
    
    Ic=Float(112.0e-9)

    def _get_fTvec(self, phi, gamma, Delta, fd, Psaw):
        C=self.Ct*(1.0+2.0*Delta/fd)+self.Cc
        Ec=e**2/(2*C)
        Ecvec=-Ec*(6.0*self.nvec**2+6.0*self.nvec+3.0)/12.0

        
        Isq=0.0*4.0*gamma*2.0*(self.Cc+self.Ct)*Psaw*1#+0.0j
        if Isq<self.Ic**2:
            Ej = self.Ejmax*absolute(cos(phi))*sqrt(1.0-Isq/self.Ic**2) #Josephson energy as function of Phi.
        else:
            Ej=0.0#print sqrt(Isq)
        if self.harm_osc:
            return sqrt(8.0*Ej*Ec)*(self.nvec+0.5)/h          
        return (-Ej + sqrt(8.0*Ej*Ec)*(self.nvec+0.5)+Ecvec)/h #\omega_m
        #return 0.0*(-Ej + 1.0*sqrt(8.0*Ej*self.Ec)*(self.nvec+0.5)+self.Ecvec)/h #\omega_m
        
    def _get_X(self, f, f0, Np):
        return Np*pi*(f-f0)/f0

    def _get_GammaDelta(self, gamma, fd, f0, Np):
        if not self.do_ls:
            return gamma, 0.0
        X=self._get_X(f=fd, f0=f0, Np=Np)
        Delta=gamma*(sin(2*X)-2*X)/(2*X**2)
        Gamma=gamma*(sin(X)/X)**2
        return Gamma, Delta

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
        return sqrt(self.pwr_lin/h*2.0)
        #pwr_fridge=self.pwr_arr-self.atten
        #return sqrt(0.001*10**(pwr_fridge/10.0)/(h*a.fd))*sqrt(2*self.gamma_el)

    @private_property
    def value_grid(self):
        value_grid=array(meshgrid(self.phi_arr, self.frq_arr))
        #value_grid=array(meshgrid(self.phi_arr, self.Omega_arr))
        return zip(value_grid[0, :, :].flatten(), value_grid[1, :, :].flatten())

    funcer=Callable()
    funcer2=Callable()

    @private_property
    def value_grid2(self):
        value_grid=array(meshgrid(self.phi_arr, self.pwr_arr))
        return zip(value_grid[0, :, :].flatten(), value_grid[1, :, :].flatten())

    power_plot=Bool(True)
    acoustic_plot=Bool(True)

    @private_property
    def fexpt(self):
        self.power_plot=False
        fexpt=parallel_map(self.funcer, self.value_grid,  progress_bar=True)
        return reshape(fexpt, (len(self.frq_arr), len(self.phi_arr)))

    @private_property
    def fexpt2(self):
        self.power_plot=True
        fexpt=parallel_map(self.funcer, self.value_grid2,  progress_bar=True)
        #print shape(self.value_grid2)
        #print self.pwr_arr.shape
        #print self.phi_arr.shape
        #print shape(fexpt)
        return reshape(fexpt, (len(self.pwr_arr), len(self.phi_arr)))

    def find_expect(self, vg, pwr, fd):
        if self.power_plot:
            phi, pwr=vg
        else:
            phi, fd=vg
        pwr_fridge=pwr-self.atten
        lin_pwr=0.001*10**(pwr_fridge/10.0)
        Omega=sqrt(lin_pwr/h*2.0)

        gamma, Delta=self._get_GammaDelta(fd=fd, f0=self.f0, Np=self.Np, gamma=self.gamma)
        g_el=self._get_Gamma_C(fd=fd)
        wTvec=self._get_fTvec(phi=phi, gamma=gamma, Delta=Delta, fd=fd, Psaw=lin_pwr)

        if self.acoustic_plot:
            Om=Omega*sqrt(gamma/fd)
        else:
            Om=Omega*sqrt(g_el/fd)
        wT = wTvec-fd*self.nvec #rotating frame of gate drive \omega_m-m*\omega_\gate
        transmon_levels = Qobj(diag(wT[range(self.N_dim)]))
        rate1 = (gamma+g_el)*(1.0 + self.N_gamma)
        rate2 = (gamma+g_el)*self.N_gamma
        c_ops=[sqrt(rate1)*self.a_op, sqrt(rate2)*self.a_dag]#, sqrt(rate3)*self.a_op, sqrt(rate4)*self.a_dag]
        Omega_vec=-0.5j*(Om*self.a_dag - conj(Om)*self.a_op)
        H=transmon_levels +Omega_vec
        final_state = steadystate(H, c_ops) #solve master equation
        fexpt=expect(self.a_op, final_state) #expectation value of relaxation operator
        #return fexpt
        if self.acoustic_plot:
            return 1.0*gamma/Om*fexpt
        else:
            return 1.0*sqrt(g_el*gamma)/Om*fexpt

if __name__=="__main__":
    a=Sat_Qubit()
    a.N_dim=8*2
    #a.do_ls=True #False
    #a.harm_osc=True
    a.atten=83+20
    a.Ec = 0.22e9/2*h # Charging energy.
    a.Ejmax = 2*22.2e9*h # Maximum Josephson energy.

    a.gamma = 1038.2059e6 # Acoustic relaxation rate of the transmon.
    a.gamma_el=a.gamma #0.750e6 #electric relaxation rate
    a.gamma_phi = 0.00e6 # Dephasing rate of the transmon.
    a.fd = 4.5066e9#/1e6 # Drive frequency.
    a.Ct=150e-15
    a.Cc=2e-15
    a.Zc=50.0
    a.acoustic_plot=True #False
    pwr=-100.0
    #Omega=a.Omega_arr[0]
    fd=4.5e9 #a.frq_arr[15]

    def find_expect(vg, self=a, fd=fd, pwr=pwr):
        return self.find_expect(vg=vg, fd=fd, pwr=pwr)
    a.funcer=find_expect


    if 1:
        pl=colormesh(a.phi_arr, a.pwr_arr, absolute(a.fexpt2), cmap="RdBu_r")
        lp=line(a.pwr_arr, absolute(a.fexpt2[:, 127/4]))
        lp=line(a.pwr_arr, absolute(a.fexpt2[:, 127/4+1]), pl=lp)
        lp=line(a.pwr_arr, absolute(a.fexpt2[:, 127/4-1]), pl=lp)

        pl=colormesh(a.phi_arr, a.pwr_arr, 1-absolute(a.fexpt2), cmap="RdBu_r")

        pl=colormesh(a.phi_arr, a.pwr_arr, 10*log10(absolute(a.fexpt2)), cmap="RdBu_r")
        #pl.show()
    a.phi_arr=linspace(-1.0, 1.0, 50)*pi


    if 1:

        pl1=colormesh(a.phi_arr, a.frq_arr, absolute(a.fexpt), cmap="RdBu_r")
        pl1=colormesh(a.phi_arr, a.frq_arr, 1-absolute(a.fexpt), cmap="RdBu_r")


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
        Ej = a.Ejmax*absolute(cos(a.phi_arr)) #Josephson energy as function of Phi.
        wTvec = (sqrt(8.0*Ej*a.Ec)-a.Ec)/h #\omega_m

        line(a.phi_arr, wTvec, pl=pl)#.show()
        line(a.phi_arr, wTvec, pl=pl1)#.show()

        g, d=a._get_GammaDelta(fd=a.frq_arr, f0=a.f0, Np=a.Np, gamma=a.gamma)
        w0=a.frq_arr+d
        Ej=((h*w0+a.Ec)**2)/(8.0*a.Ec)
        phi=arccos(Ej/a.Ejmax)#/pi #Josephson energy as function of Phi.
        phi_extend=append(phi, -phi)
        phi_extend=append(phi_extend, -phi+pi)
        phi_extend=append(phi_extend, phi-pi)
        freq=append(a.frq_arr, a.frq_arr)
        freq=append(freq, freq)

        line(phi_extend, freq, pl=pl1, color="cyan")
        line(phi_extend, freq, pl=pl, color="cyan").show()
        #line(a.phi_arr, wTvec-d, pl=pl).show()

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

#def Lamb_destroy(self, phi, fd, N, offset=0):#, ftype="drive"):
#    if not isinstance(N, (int, integer)):  # raise error if N not integer
#        raise ValueError("Hilbert space dimension must be integer value")
#
#    #Ej = self.Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.
#    #if ftype=="Anton":
#    #    fvec = (-Ej + sqrt(8.0*Ej*self.Ec)*(self.nvec+0.5)+self.Ecvec)/h #\omega_m
#    #    X=self.Np*pi*(diff(fvec)-self.f0)/self.f0
#    #elif ftype=="SHO":
#    #    fvec=sqrt(8.0*Ej*self.Ec)/h
#    #    X=self.Np*pi*(fvec-self.f0)/self.f0
#    #else:
#    X=self.Np*pi*(fd-self.f0)/self.f0
#    gamma=(sin(X)/X)**2
#
#    #gamma=0.0*fd/5e9+(sin(X)/(self.Np*sin(X/self.Np)))**2
#    data = sqrt(gamma)*sqrt(arange(offset+1, N+offset, dtype=complex))
#    ind = arange(1,N, dtype=int32)
#    ptr = arange(N+1, dtype=int32)
#    ptr[-1] = N-1
#    return Qobj(fast_csr_matrix((data,ind,ptr),shape=(N,N)), isherm=False)
