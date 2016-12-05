# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 09:54:01 2016

@author: thomasaref
"""

from numpy import diag, arange, ones, array, linspace
from qutip import Qobj
import matplotlib.pyplot as plt

def hamiltonian(Ec, Ej, N, ng):
    """
    Return the charge qubit hamiltonian as a Qobj instance.
    """
    m = diag(4 * Ec * (arange(-N,N+1)-ng)**2) + 0.5 * Ej * (diag(-ones(2*N), 1) +
                                                            diag(-ones(2*N), -1))
    return Qobj(m)

def plot_energies(ng_vec, energies, ymax=(20, 3)):
    """
    Plot energy levels as a function of bias parameter ng_vec.
    """
    fig, axes = plt.subplots(1,2, figsize=(16,6))

    for n in range(len(energies[0,:])):
        axes[0].plot(ng_vec, energies[:,n])
    axes[0].set_ylim(-2, ymax[0])
    axes[0].set_xlabel(r'$n_g$', fontsize=18)
    axes[0].set_ylabel(r'$E_n$', fontsize=18)

    for n in range(len(energies[0,:])):
        axes[1].plot(ng_vec, (energies[:,n]-energies[:,0])/(energies[:,1]-energies[:,0]))
    axes[1].set_ylim(-0.1, ymax[1])
    axes[1].set_xlabel(r'$n_g$', fontsize=18)
    axes[1].set_ylabel(r'$(E_n-E_0)/(E_1-E_0)$', fontsize=18)
    return fig, axes

def visualize_dynamics(result, ylabel):
    """
    Plot the evolution of the expectation values stored in result.
    """
    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(result.times, result.expect[0])

    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xlabel(r'$t$', fontsize=16)

N = 10
Ec = 1.0
Ej = 50.0

print "hi"
ng_vec = linspace(-4, 4, 200)

energies = array([hamiltonian(Ec, Ej, N, ng).eigenenergies() for ng in ng_vec])

plot_energies(ng_vec, energies)

plt.show()