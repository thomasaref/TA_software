# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 17:43:38 2016

@author: thomasaref
"""
from qutip import tensor, destroy, create, qeye, shape, expect, ket2dm, fock_dm, mesolve, basis, steadystate, num, Qobj#, charge, tunneling
import matplotlib.pyplot as plt
from numpy import zeros, pi, linspace, sqrt, arange, ones, delete, array
from time import time
import scipy.sparse as sp

Na=3
fa=1
alpha=0.1
hqtemp = zeros((Na,Na))
hqtemp[1,1]= fa
if Na > 2:
    for idx in range(2,Na):
        hqtemp[idx,idx] = hqtemp[idx-1,idx-1]+(fa-(idx-1)*alpha)
print hqtemp
#eqn C1 in Koch transmon paper
b=destroy(3)
bdag=b.dag()
bdagb=b*bdag

def transmon(EjoverEc, Ec=1.0):
    H=Ec*(-EjoverEc+sqrt(8.0*EjoverEc)*(bdagb+0.5)-1.0/12.0*(b+bdag)**4.0)
    return H.eigenenergies()


def scb_charge(Nmax, ng=0.0, Nmin=None):
    if Nmin is None:
        Nmin = -Nmax
    diag = (arange(Nmin, Nmax+1, dtype=float)-ng)**2
    C = sp.diags(diag, 0, format='csr', dtype=complex)
    return Qobj(C, isherm=True)

def scb_tunneling(N, m=1):
    N=2*N+1
    diags = [ones(N-m,dtype=int),ones(N-m,dtype=int)]
    T = sp.diags(diags,[m,-m],format='csr', dtype=complex)
    return Qobj(T, isherm=True)

Ec=150.0e6#*h
EjoverEc=linspace(0.1, 40, 101) #array([1*4.0])
Ej_vec=EjoverEc*Ec
#print -Ej/2*scb_tunneling(2*5+1)
tr_energies=array([transmon(Ejd, Ec=Ec) for Ejd in EjoverEc])
plt.plot(Ej_vec, tr_energies[:,0])#-Ej_vec)
plt.plot(Ej_vec, tr_energies[:,1])
plt.plot(Ej_vec, tr_energies[:,2])
def calc_energies(ng, Ej, Ec=Ec, N=50):
    H=4.0*Ec*scb_charge(N, ng)-Ej/2*scb_tunneling(N)
    ev=H.eigenenergies()
    d1=min(ev)
    ev=delete(ev, ev.argmin())
    d2=min(ev)
    ev=delete(ev, ev.argmin())
    d3=min(ev)
    return (d1, d2, d3)

ng_vec=linspace(-2, 2, 100)
#print ng_vec
#Ej_vec=linspace(0.1,40, 20)
#energies=[calc_energies(ng) for ng in ng_vec]
energies=[calc_energies(0.5, Ej) for Ej in Ej_vec]

print energies[0][2]-energies[0][1], energies[0][1]-energies[0][0], energies[0][2]-energies[0][1]-(energies[0][1]-energies[0][0])
print sqrt(8*Ej*Ec)-Ec
print energies[0][2], energies[0][1], energies[0][0]
print -Ej+sqrt(8*Ej*Ec)*2.5, -Ej+sqrt(8*Ej*Ec)*1.5, -Ej+sqrt(8*Ej*Ec)*0.5


energies=array(energies)


plt.plot(Ej_vec, energies)
plt.plot(Ej_vec, -Ej_vec+sqrt(8*Ej_vec*Ec)*0.5- Ec/4.0, ".")
plt.plot(Ej_vec, -Ej_vec+sqrt(8*Ej_vec*Ec)*1.5- (Ec/12.0)*(6.0+6.0+3.0), ".")
plt.plot(Ej_vec, -Ej_vec+sqrt(8*Ej_vec*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0), ".")
plt.show()
#print energies.shape
plt.figure()
plt.plot(EjoverEc, (energies[:,2]-energies[:,1]-(energies[:,1]-energies[:,0]))/(energies[:,1]-energies[:,0]))

def anharm(Ej=Ej, Ec=Ec):
    E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
    E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
    E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
    return -1/(sqrt(8*Ej/Ec)-1)*(E1-E0)
    return (E2-E1)-(E1-E0)#)/(E1-E0)

plt.plot(EjoverEc, -1.0/(sqrt(8*EjoverEc)-1.0))

#, -Ej_vec+sqrt(8*Ej_vec*Ec)*1.5, -Ej_vec+sqrt(8*Ej_vec*Ec)*0.5])

plt.show()

if 0:
    N=5
    print charge(5)
    print tunneling(5)
    print Qobj(sp.eye(N, N, 1, dtype=complex, format='csr'), isherm=False)

    print Qobj(sp.spdiags(1, 1, N, N, format='csr'), isherm=False)

    #E_J = E_J_max*cos(pi*phi) # Josephson energy as function of Phi.
    #wT_vec = -E_J + sqrt(8.0*E_J*E_C)*(Nt_vec+0.5)-E_C*(6*Nt_vec**2+6*Nt_vec+3)/12.0

    #N_gamma=1.0/(exp(hbar*w0/(k*T))-1.0)
    #print N_gamma
    #print 1/(exp(f0/1.0e6/21000.0/T)-1)
    #gamma=50.0e6

    print num(9, -4)

    N=3
    n=num(2*N+1, -N)
    print n
    print destroy(2*N+1, -N)

    def steady(N = 20):  # number of basis states to consider
        n=num(N)
        a = destroy(N)
        H = a.dag() * a
        print H.eigenstates()
        #psi0 = basis(N, 10)  # initial state
        kappa = 0.1  # coupling to oscillator
        c_op_list = []
        n_th_a = 2  # temperature with average of 2 excitations
        rate = kappa * (1 + n_th_a)
        c_op_list.append(sqrt(rate) * a)  # decay operators
        rate = kappa * n_th_a
        c_op_list.append(sqrt(rate) * a.dag())  # excitation operators
        final_state = steadystate(H, c_op_list)
        fexpt = expect(a.dag() * a, final_state)

        #tlist = linspace(0, 100, 100)

        #mcdata = mcsolve(H, psi0, tlist, c_op_list, [a.dag() * a], ntraj=100)

        #medata = mesolve(H, psi0, tlist, c_op_list, [a.dag() * a])
        #plot(tlist, mcdata.expect[0],
        #plt.plot(tlist, medata.expect[0], lw=2)
        plt.axhline(y=fexpt, color='r', lw=1.5) # ss expt. value as horiz line (= 2)
        plt.ylim([0, 10])
        plt.show()
    #steady()
    def osc_relax():
        w = 1.0               # oscillator frequency
        kappa = 0.1           # relaxation rate
        a = destroy(10)       # oscillator annihilation operator
        rho0 = fock_dm(10, 5) # initial state, fock state with 5 photons
        H = w * a.dag() * a   # Hamiltonian

        # A list of collapse operators
        c_ops = [sqrt(kappa) * a]
        tlist = linspace(0, 50, 100)

        # request that the solver return the expectation value of the photon number state operator a.dag() * a
        result = mesolve(H, rho0, tlist, c_ops, [a.dag() * a])
        print result
        fig, axes = plt.subplots(1,1)
        axes.plot(tlist, result.expect[0])
        axes.set_xlabel(r'$t$', fontsize=20)
        axes.set_ylabel(r"Photon number", fontsize=16);

    def compute(N, wc, wa, glist, use_rwa):

        # Pre-compute operators for the hamiltonian
        a  = tensor(destroy(N), qeye(2))
        sm = tensor(qeye(N), destroy(2))
        nc = a.dag() * a
        na = sm.dag() * sm

        idx = 0
        na_expt = zeros(shape(glist))
        nc_expt = zeros(shape(glist))
        for g in glist:

            # recalculate the hamiltonian for each value of g
            if use_rwa:
                H = wc * nc + wa * na + g * (a.dag() * sm + a * sm.dag())
            else:
                H = wc * nc + wa * na + g * (a.dag() + a) * (sm + sm.dag())

            # find the groundstate of the composite system
            evals, ekets = H.eigenstates()
            psi_gnd = ekets[0]
            na_expt[idx] = expect(na, psi_gnd)
            nc_expt[idx] = expect(nc, psi_gnd)

            idx += 1

        return nc_expt, na_expt, ket2dm(psi_gnd)

    #
    # set up the calculation
    #
    wc = 1.0 * 2 * pi   # cavity frequency
    wa = 1.0 * 2 * pi   # atom frequency
    N = 20              # number of cavity fock states
    use_rwa = False     # Set to True to see that non-RWA is necessary in this regime

    glist = linspace(0, 2.5, 50) * 2 * pi # coupling strength vector

    start_time = time()
    print "start calculation"
    #osc_relax()
    #nc, na, rhoss_final = compute(N, wc, wa, glist, use_rwa)
    print('time elapsed = ' + str(time() - start_time))
    #plt.show()

    # plot the cavity and atom occupation numbers as a function of
    #
    fig, ax = plt.subplots()

    ax.plot(glist/(2*pi), nc)
    ax.plot(glist/(2*pi), na)
    ax.legend(("Cavity", "Atom excited state"))
    ax.set_xlabel('g - coupling strength')
    ax.set_ylabel('Occupation probability')
    ax.set_title('# photons in the groundstate');
    plt.show()