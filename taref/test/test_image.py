# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 08:55:44 2016

@author: thomasaref
"""

import matplotlib.pyplot as plt


f=plt.figure(figsize=(4.5, 4.5)) #, tight_layout=True)
f.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
axes=f.add_subplot(111)
axes.get_xaxis().set_visible(False)
axes.get_yaxis().set_visible(False)
color="black"
linewidth=3.0
fontsize=18
#plt.plot([1,2,3], [1,2,3])

#plt.plot([10, 10, 9, 11], [10, 9, 9, 9])
f.text(0, 0.9, "a)", fontsize=fontsize)

def capacitor(x=0, y=0, w=3, h=3, g=0.5, label="$C_C$", color=color, fontsize=fontsize, linewidth=linewidth, lx=2, ly=1.1):
    plt.plot([x, x, x-w, x+w], [y+h+g, y+g, y+g, y+g], color=color, linewidth=linewidth)
    plt.plot([x, x, x-w, x+w], [y-h-g, y-g, y-g, y-g], color=color, linewidth=linewidth)
    plt.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")

def box(x=0, y=0, w=3, h=1, g=2.5, label="$G_a$", color=color, fontsize=fontsize, linewidth=linewidth, lx=0.0, ly=0.0):
    plt.plot([x, x, x-w, x+w], [y+h+g, y+g, y+g, y+g], color=color, linewidth=linewidth)
    plt.plot([x-w, x-w], [y-g, y+g], color=color, linewidth=linewidth)
    plt.plot([x, x, x-w, x+w], [y-h-g, y-g, y-g, y-g], color=color, linewidth=linewidth)
    plt.plot([x+w, x+w], [y-g, y+g], color=color, linewidth=linewidth)
    plt.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")

def hbox(x=0, y=0, w=1, h=3, g=2.5, label="$Z_C$", color=color, fontsize=fontsize, linewidth=linewidth, lx=0.0, ly=0.0):
    plt.plot([x+h+g, x+g, x+g, x+g], [y, y, y-w, y+w], color=color, linewidth=linewidth)
    plt.plot([x-g, x+g], [y-w, y-w], color=color, linewidth=linewidth)
    plt.plot([x-h-g, x-g, x-g, x-g], [y, y, y-w, y+w], color=color, linewidth=linewidth)
    plt.plot([x-g, x+g], [y+w, y+w], color=color, linewidth=linewidth)
    plt.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")

def IDT(x=0, y=0, sp=10):
    box(x, y)
    box(x+sp, y, label="$iB_a$")
    capacitor(x+2*sp, y, label="$C_t$")
    plt.plot([x, x+2*sp], [y+3.5, y+3.5], color=color, linewidth=linewidth)
    plt.plot([x, x+2*sp], [y-3.5, y-3.5], color=color, linewidth=linewidth)

def IDT_r(x=0, y=0, sp=10):
    box(x+2*sp, y)
    box(x+sp, y, label="$iB_a$")
    capacitor(x, y)
    plt.plot([x, x+2*sp], [y+3.5, y+3.5], color=color, linewidth=linewidth)
    plt.plot([x+0, x+2*sp], [y-3.5, y-3.5], color=color, linewidth=linewidth)

IDT(0)
capacitor(x=10, y=7)
hbox(y=7)
#IDT_r(0)
#plt.figure(figsize=(6.4, 4.4))
#f.savefig("testy_circuit_draw", dpi=150, bbox_inches='tight', transparent=True)

plt.show()