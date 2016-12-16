# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 11:15:56 2016

@author: thomasaref
"""

#Main program for calculating the susceptibility in the two-tone
# spectroscopy measurement on the transmon qubit. The calculations assume
#WEAK phonon probe.

# We calculate the reflection coefficient (proportional to the
# susceptibility) for a transmon in an open transmission line.

# Everything in units of MHz unless otherwise stated.
# We are in the rotating frame of the drive.

# We scan the qubit frequencies (by changing the flux) and the drive
# frequency. The probe is constant at 4.8 GHz. We can use different drive
# powers, but the drive power is constant during a scan.

#function reflection = Twotone_simulation(gate_freq_vec, phi_vec, Omega, Nt, theta_steps, const)

from numpy import shape, trace, reshape, diag, absolute, cos, meshgrid, array, arange, pi, exp, prod, transpose, identity, kron, zeros, dot, real, linspace, sqrt
from numpy.linalg import pinv, solve, eig, inv
from qutip import spectrum, expect, Qobj, parallel_map, issuper, liouvillian, qeye, tensor, spre, mat2vec, steadystate, destroy
from matplotlib.pyplot import pcolormesh, show

sample_power_sim_dBm=linspace(-100.0, -50, 31)
spk_external_att = 0.0
Omega_el_squared_coeff = 1.2*3.9666e+21  # Omega^2 in angular frequency = omega_el_square_coeff * gate_power_at_fridgetop
gate_fridge_att = -83.0
power_fridgetop_sim = 1e-3*10**(0.1*(sample_power_sim_dBm + spk_external_att + gate_fridge_att))
#print power_fridgetop_sim
Omega_sim_vec = sqrt((power_fridgetop_sim)*Omega_el_squared_coeff)
#Omega_sim_vec=linspace(1.0, 400.0, 31)
#Omega = (1e-6/(2*pi))*2*sqrt(P_in*const.Gamma_el/(const.hf0))
#print Omega_sim_vec
Omega = 20#Omega/(2*pi*1e6)
#Omega=Omega_sim_vec
Ec = 0.22e9/1e6 # Charging energy.
Ejmax = 22.2e9/1e6 # Maximum Josephson energy.

gamma = 38.2059e6*2*pi/(1e6*2*pi) # Relaxation rate of the transmon.
gamma_phi = 0*2*pi/(1e6*2*pi) # Dephasing rate of the transmon.

wd = 4.8066e9/1e6 # Drive frequency.

wd_vec = linspace(4.3e9, 5.3e9, 91)/1e6

wp =  4.8066e9/1e6 # Probe frequency.

T = 21000.0*0.03#Temperature of the transmon bath in units of MHz (1K = 21 GHz).
N_gamma = 1.0/(exp(wp/T)-1.0)#Thermal population of the transmon phonon bath around wp.

theta_start = 0
theta_steps = 4
theta_end = (1.0-1.0/theta_steps)*2.0*pi;
theta_vec = linspace(theta_start, theta_end, theta_steps)# Vector of drive phases.

N = 5 # Number of levels included in the transmon. INCREASE Nt for high drive powers!


#It = sparse(eye(Nt)); % Unity matrix for the transmon.
#Itot = It; % Unity matrix for the total Hilbert space.
#
#tm = sparse(diag(sqrt(1:Nt-1),1)); % Lowering operator for the transmon.
#tp = ctranspose(tm); % Raising operator for the transmon.
#
#tdiag = sparse(diag(0:2:2*(Nt-1))); % Operator for dephasing.
#
#tm_l = kron(Itot,tm); % tm operator multiplying rho from the left.
#
#p = -1i*(tp - tm); % "P" operator.
#
#p_l = kron(Itot,p); % "P" operator multiplying rho from the left.
#p_r = kron(transpose(p),Itot); % "P" operator multiplying rho from the right.

#
#w01_vec = zeros(1,phi_steps); % To store transition energies.
#w12_vec = zeros(1,phi_steps);
#w23_vec = zeros(1,phi_steps);
#w34_vec = zeros(1,phi_steps);

# Looping over Phi and wd

phi_arr=linspace(0.23, 0.33, 101)

a = destroy(N)
#print a
adag=a.dag()
#print adag

c_op_list = []

rate = gamma * (1 + N_gamma)

c_op_list.append(sqrt(rate) * a)  # decay operators

rate = gamma * N_gamma

c_op_list.append(sqrt(rate) * adag)  # excitation operators

p = -1.0j*(adag - a) # "P" operator.

#p_l = kron(It,p) # % "P" operator multiplying rho from the left.
#p_r = kron(transpose(p),It) # "P" operator multiplying rho from the right.
#print p_r

nvec=arange(N)
#wdvec=nvec*wd
Ecvec=-Ec*(6.0*nvec**2+6.0*nvec+3.0)/12.0

def make_H(phi, Omega, wdvec, theta=0.0):
    Omega_op=0.5*Omega*(a*exp(-1.0j*theta)+adag*exp(1.0j*theta))
    Ej = Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.

    wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec

    wT = wTvec-wdvec
    transmon_levels = Qobj(diag(wT[range(N)]))
    H=transmon_levels +Omega_op
    return H

def find_expect(vg):
    phi, Omega=vg
    H=make_H(phi, Omega, wdvec, 0.0)
    #Omega_op=- 0.5j*(Omega*adag - conj(Omega)*a)

    #Ej = Ejmax*absolute(cos(pi*phi)) #Josephson energy as function of Phi.

    #wTvec = -Ej + sqrt(8.0*Ej*Ec)*(nvec+0.5)+Ecvec

    #wT = wTvec-wdvec
    #transmon_levels = Qobj(diag(wT[range(N)]))
    #H=transmon_levels +Omega_op
    final_state = steadystate(H, c_op_list)

    return expect( a, final_state)

if 0:
    value_grid=array(meshgrid(phi_arr, Omega_sim_vec))
    vg=zip(value_grid[0, :, :].flatten(), value_grid[1, :, :].flatten())
    fexpt=parallel_map(find_expect, vg,  progress_bar=True)
    fexpt=reshape(fexpt, (31, 101))
    pcolormesh(phi_arr, sample_power_sim_dBm, absolute(fexpt), cmap="RdBu_r")
    show()

#w01_vec(i) = wT_vec(2)- wT_vec(1); % Transition energies.
#w12_vec(i) = wT_vec(3)- wT_vec(2);
#w23_vec(i) = wT_vec(4)- wT_vec(3);
#w34_vec(i) = wT_vec(5)- wT_vec(4);
H=make_H(0.2, 190, 4000.0)
print H
L = liouvillian(H, c_op_list)
print L
tr_mat = tensor([qeye(n) for n in L.dims[0][0]])
print tr_mat
tr_vec = transpose(mat2vec(tr_mat.full()))
print tr_vec
N = prod(L.dims[0][0])
print N
A=L.full()


a_sup=spre(a).full()
b_sup=spre(p).full()

D,U=eig(A)
print "D", D
I = identity(N * N)
w=3.0
MMR1 = pinv(-1.0j * w * I + A)
print A*MMR1*inv(A)
print U*MMR1*inv(U)
#raise Exception

#A.expm()


#MMR1 = pinv(1.0j * w * I + diag(D))

#print "MMR", MMR1
#MMR = diag(1.0/(1.0j*w*diag(I)+diag(D)))
#print "MMR2", MMR

#print U

#Uinv=inv(U)
#print "Uinv", Uinv

#Lint=U*MMR*Uinv
#print "Lint", diag(Lint)
#Lop=Qobj(U)#.expm()
#print diag(Lop*MMR*Lop.dag())
#print Lop

rho_ss = steadystate(L)
rho = transpose(mat2vec(rho_ss.full()))

print p.shape

print transpose(rho)
print spectrum(H, [3.0], c_op_list, a, p, solver="pi", use_pinv=True)
#print "p", dot(p, transpose(rho))
s = dot(tr_vec, dot(a_sup, dot(MMR1, dot(b_sup, transpose(rho)))))
print s
print -2 * real(s[0, 0])
#spectrum[idx] = -2 * real(s[0, 0])

#        Chi_temp[i,j] += (1/theta_steps)
sol=a*p*rho_ss
print D.shape
print U.shape
#print MMR.shape
#print Lint.shape
print sol.shape
print rho_ss.shape
print rho.shape
print a.shape
print p.shape
#print 1j*trace(reshape(a*Lint*p*rho_ss,N,N))

#raise Exception
#    A = L.full()
#    b = spre(p).full()
#    a = spre(a).full()
I = identity(N * N)

tr_mat = tensor(qeye(N))
tr_vec = transpose(mat2vec(tr_mat.full()))


def two_tone(vg, listening=False, use_pinv=True):
    phi, wd=vg
    H=make_H(phi, Omega, wd*nvec, 0.0)

    if listening:
        final_state = steadystate(H, c_op_list)
        return expect( a, final_state)
    L = liouvillian(H, c_op_list)
    #tr_mat = tensor([qeye(n) for n in L.dims[0][0]])
    #N = prod(L.dims[0][0])

    A = L.full()

    #tr_vec = transpose(mat2vec(tr_mat.full()))

    rho_ss = steadystate(L)
    rho = transpose(mat2vec(rho_ss.full()))

    #P = kron(transpose(rho), tr_vec)
    #Q = I - P
    w=wp-wd
    if 1:
       D,U=eig(A)
       Uinv=inv(U)
    #spectrum = zeros(len(wlist))

    #for idx, w in enumerate(wlist):
    if 1:
        if use_pinv:
            MMR = pinv(-1.0j * w * I + A)
            #MMR = A*MMR*inv(A)
        elif use_pinv==1:
            MMR = dot(Q, solve(-1.0j * w * I + A, Q))
        else:
            MMR = diag(1.0/(1.0j*w*diag(I)+diag(D)))
            Lint=U*MMR*Uinv
            #Chi_temp[i,j] += (1/theta_steps)*1j*trace(reshape(tm_l*Lint*(p_l - p_r)*rho_ss_c,dim,dim))

        #rho_tr=transpose(rho)
        #p1=dot(b_sup, rho_tr)
        #p2=dot(rho_tr, b_sup)

        #s = dot(tr_vec,
        #           dot(a_sup, dot(MMR, p1-p2)))

        s1 = dot(tr_vec,
                   dot(a_sup, dot(MMR, dot(b_sup, transpose(rho)))))
        s2 = dot(tr_vec,
                   dot(b_sup, dot(MMR, dot(a_sup, transpose(rho)))))
        s=s1-s2
        #spectrum[idx] =
        return -2 * real(s[0, 0])


    return spectrum

if 1:
    value_grid=array(meshgrid(phi_arr, wd_vec))
    #print "tw", two_tone((0.2, 4000.0))
    vg=zip(value_grid[0, :, :].flatten(), value_grid[1, :, :].flatten())
    fexpt=parallel_map(two_tone, vg,  progress_bar=True)
    print shape(fexpt) #.shape
    fexpt=reshape(fexpt, (len(wd_vec), len(phi_arr)))
    #pcolormesh( absolute(fexpt), cmap="RdBu_r")
    pcolormesh( fexpt, cmap="RdBu_r")
    colorbar()
    show()


def _spectrum_pi(H, wlist, c_ops, a_op, b_op, use_pinv=False):
    """
    Internal function for calculating the spectrum of the correlation function
    :math:`\left<A(\\tau)B(0)\\right>`.
    """

    print issuper(H)

    L = H if issuper(H) else liouvillian(H, c_ops)

    tr_mat = tensor([qeye(n) for n in L.dims[0][0]])
    N = prod(L.dims[0][0])

    A = L.full()
    b = spre(b_op).full()
    a = spre(a_op).full()

    tr_vec = transpose(mat2vec(tr_mat.full()))

    rho_ss = steadystate(L)
    rho = transpose(mat2vec(rho_ss.full()))

    I = identity(N * N)
    P = kron(transpose(rho), tr_vec)
    Q = I - P

    spectrum = zeros(len(wlist))

    for idx, w in enumerate(wlist):
        if use_pinv:
            MMR = pinv(-1.0j * w * I + A)
        else:
            MMR = dot(Q, solve(-1.0j * w * I + A, Q))

        s = dot(tr_vec,
                   dot(a, dot(MMR, dot(b, transpose(rho)))))
        spectrum[idx] = -2 * real(s[0, 0])

    return spectrum





#for cl = 2:numlabs
#
#if labindex == cl
#
#labSend(Chi_temp,1,1);
#
#end
#end
#
#if labindex == 1
#
#for c2 = 2:numlabs
#
#Chi_temp = Chi_temp + labReceive(c2,1);
#
#end
#
#Chi = Chi_temp;
#r = (gamma/2)*Chi; % The reflection coefficient.
#
#end
#
#
#
#%% Save the data
#
#if labindex == 1
#
#%save filename... Chi gamma gamma_phi Omega_vec phi_vec wd_vec wp T Nt r
#
#%dlmwrite('reflection.txt', r,'\t')
#
#end
#reflection = r;
