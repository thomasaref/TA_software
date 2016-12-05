# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:08:37 2016

@author: thomasaref
"""

from numpy import pi, linspace, sqrt
from qutip import tensor, basis, destroy, qeye, mesolve
import matplotlib.pyplot as plt

wc = 1.0  * 2 * pi  # cavity frequency
wa = 1.0  * 2 * pi  # atom frequency
g  = 0.05 * 2 * pi  # coupling strength
kappa = 0.005          # cavity dissipation rate
gamma = 0.05           # atom dissipation rate
N = 15                 # number of cavity fock states
n_th_a = 0.0           # temperature in frequency units
use_rwa = True

tlist = linspace(0,25,100)

#Setup the operators, the Hamiltonian and initial state
psi0 = tensor(basis(N,1), basis(2,0))    # start with an excited atom
print basis(2,0)# operators
a  = tensor(destroy(N), qeye(2))
sm = tensor(qeye(N), destroy(2))

# Hamiltonian
if use_rwa:
    H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() * sm + a * sm.dag())
else:
    H = wc * a.dag() * a + wa * sm.dag() * sm + g * (a.dag() + a) * (sm + sm.dag())
#Create a list of collapse operators that describe the dissipation
c_op_list = []

rate = kappa * (1 + n_th_a)
if rate > 0.0:
    c_op_list.append(sqrt(rate) * a)

rate = kappa * n_th_a
if rate > 0.0:
    c_op_list.append(sqrt(rate) * a.dag())

rate = gamma
if rate > 0.0:
    c_op_list.append(sqrt(rate) * sm)
#Evolve the system
#Here we evolve the system with the Lindblad master equation solver, and we request that the expectation values of the operators a†a
# and σ+σ−
# are returned by the solver by passing the list [a.dag()*a, sm.dag()*sm] as the fifth argument to the solver.
output = mesolve(H, psi0, tlist, c_op_list, [a.dag() * a, sm.dag() * sm])
#Visualize the results
#Here we plot the excitation probabilities of the cavity and the atom (these expectation values were calculated by the mesolve above). We can clearly see how energy is being coherently transferred back and forth between the cavity and the atom.

#In [9]:
fig, ax = plt.subplots(figsize=(8,5))
ax.plot(tlist, output.expect[0], label="Cavity")
ax.plot(tlist, output.expect[1], label="Atom excited state")
ax.legend()
ax.set_xlabel('Time')
ax.set_ylabel('Occupation probability')
ax.set_title('Vacuum Rabi oscillations')
plt.show()