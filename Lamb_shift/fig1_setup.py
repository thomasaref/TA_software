# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 08:55:44 2016

@author: thomasaref
"""

import matplotlib.pyplot as plt
from numpy import linspace, pi, cos, sin

f=plt.figure(figsize=(4.5, 4.5)) #, tight_layout=True)
f.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
axes=f.add_subplot(111)
axes.get_xaxis().set_visible(False)
axes.get_yaxis().set_visible(False)
color="black"
linewidth=3.0
fontsize=16
sp=20
x=20
y=20
#plt.plot([1,2,3], [1,2,3])

#plt.plot([10, 10, 9, 11], [10, 9, 9, 9])
f.text(0, 0.9, "a)", fontsize=fontsize)

def capacitor(x=0, y=0, w=5, h=14, g=2, label="$C_C$", color=color, fontsize=fontsize, linewidth=linewidth, lx=5, ly=5):
    plt.plot([x, x, x-w, x+w], [y+h+g, y+g, y+g, y+g], color=color, linewidth=linewidth)
    plt.plot([x, x, x-w, x+w], [y-h-g, y-g, y-g, y-g], color=color, linewidth=linewidth)
    plt.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")

def box(x=0, y=0, w=5, h=10, g=6, label="$G_a$", color=color, fontsize=fontsize, linewidth=linewidth, lx=0.0, ly=0.0):
    plt.plot([x, x, x-w, x+w], [y+h+g, y+g, y+g, y+g], color=color, linewidth=linewidth)
    plt.plot([x-w, x-w], [y-g, y+g], color=color, linewidth=linewidth)
    plt.plot([x, x, x-w, x+w], [y-h-g, y-g, y-g, y-g], color=color, linewidth=linewidth)
    plt.plot([x+w, x+w], [y-g, y+g], color=color, linewidth=linewidth)
    plt.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")

def hbox(x=0, y=0, w=5, h=10, g=6, label="$Z_C$", color=color, fontsize=fontsize, linewidth=linewidth, lx=0.0, ly=0.0):
    plt.plot([x+h+g, x+g, x+g, x+g], [y, y, y-w, y+w], color=color, linewidth=linewidth)
    plt.plot([x-g, x+g], [y-w, y-w], color=color, linewidth=linewidth)
    plt.plot([x-h-g, x-g, x-g, x-g], [y, y, y-w, y+w], color=color, linewidth=linewidth)
    plt.plot([x-g, x+g], [y+w, y+w], color=color, linewidth=linewidth)
    plt.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")

def IDT(x=0, y=0, sp=20):
    box(x, y)
    box(x+sp, y, label="$iB_a$")
    capacitor(x+2*sp, y, label="$C_t$")
    #plt.plot([x, x+2*sp], [y+3.5, y+3.5], color=color, linewidth=linewidth)
    #plt.plot([x, x+2*sp], [y-3.5, y-3.5], color=color, linewidth=linewidth)

def IDT_r(x=0, y=0, sp=10):
    box(x+2*sp, y)
    box(x+sp, y, label="$iB_a$")
    capacitor(x, y)
    plt.plot([x, x+2*sp], [y+3.5, y+3.5], color=color, linewidth=linewidth)
    plt.plot([x+0, x+2*sp], [y-3.5, y-3.5], color=color, linewidth=linewidth)

def JJ(x=0, y=0, jjx=2.0, jjy=2.0, color=color, linewidth=linewidth):
    plt.plot([x-jjx, x+jjx], [y-jjy, y+jjy], color=color, linewidth=linewidth)
    plt.plot([x-jjx, x+jjx], [y+jjy, y-jjy], color=color, linewidth=linewidth)

def SQUID(x=0, y=0, w=8, g=8, h=8, jjx=2, jjy=2, color=color, linewidth=linewidth, label="$L_J$", lx=5, ly=12):
    box(x=x, y=y, w=w, g=g, h=h, color=color, linewidth=linewidth, label=label, lx=lx, ly=ly)
    JJ(x-w, y, jjx=jjx, jjy=jjy, color=color, linewidth=linewidth)
    JJ(x+w, y, jjx=jjx, jjy=jjy, color=color, linewidth=linewidth)

def circle(x=0, y=0, r=1, Nsteps=101, color=color, linewidth=linewidth):
    theta=linspace(0, 2*pi, Nsteps)
    #r_arr=linspace(0, r, Nsteps)
    x_arr=x+r*cos(theta)
    y_arr=y+r*sin(theta)
    plt.plot(x_arr, y_arr, color=color, linewidth=linewidth)

def wave(x=0, y=0, Nsteps=101, w=8, f=2, A=3, color=color, linewidth=linewidth):
    theta=linspace(0, 2*pi*f, Nsteps)
    x_arr=linspace(x, x+w, Nsteps)
    y_arr=y+A*sin(theta)
    plt.plot(x_arr, y_arr, color=color, linewidth=linewidth)

IDT(20, 20)
SQUID(80, 20)
capacitor(x=50, y=45, h=7)
hbox(x=50-16, y=9+45)
plt.plot([x, x+3*sp], [y+16, y+16], color=color, linewidth=linewidth)
plt.plot([x, x+3*sp], [y-16, y-16], color=color, linewidth=linewidth)
circle(80,20, r=2)
circle(80,20, r=0.2)
plt.text(80, 20-5, "$\Phi_B$", fontsize=fontsize, color=color, ha="center", va="center")
wave(5,20, color="green")
#IDT_r(0)
#plt.figure(figsize=(6.4, 4.4))
#f.savefig("testy_circuit_draw", dpi=150, bbox_inches='tight', transparent=True)
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.show()