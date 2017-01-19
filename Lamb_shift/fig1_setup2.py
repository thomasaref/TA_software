# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 09:31:29 2017

@author: thomasaref
"""

from taref.plotter.api import line

#from fig1_setup import IDT

from numpy import linspace, pi, cos, sin, flipud
from matplotlib.image import imread
from scipy.ndimage import rotate
#f=plt.figure(figsize=(4.5, 4.5)) #, tight_layout=True)
#f.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
#axes=f.add_subplot(111)
#axes.get_xaxis().set_visible(False)
#axes.get_yaxis().set_visible(False)
color="black"
linewidth=1.0
fontsize=8
sp=20
x=20
y=20
#f.text(0, 0.9, "a)", fontsize=fontsize)

pl="fig1"

def capacitor(x=0, y=0, w=5, h=14, g=2, label="$C_C$", lx=15, ly=10, 
               color=color, fontsize=fontsize, linewidth=linewidth, **kwargs):
    pl=line([x, x, x-w, x+w], [y+h+g, y+g, y+g, y+g], color=color, linewidth=linewidth, **kwargs)
    line([x, x, x-w, x+w], [y-h-g, y-g, y-g, y-g], color=color, linewidth=linewidth, pl=pl)
    pl.axes.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")
    return pl

pl=capacitor(x=50, y=45, h=7,
             ncols=2, nrows=2, nplot=2, 
             auto_ylim=False, y_min=0, y_max=100,
             auto_xlim=False, x_min=0, x_max=100)
pl.axes.get_xaxis().set_visible(False)
pl.axes.get_yaxis().set_visible(False)
pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
pl.nplot=1
img=imread(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/Lamb_shift_source/Good_sample_images/Alignment_Johan-000001.png")
#img=imread(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/Lamb_shift_source/Good_sample_images/TA210715A46-000000.png")
img=rotate(img, -2.9, reshape=False)
img=img[50:-50, :, :]
print img.shape
pl.axes.imshow(flipud(img), origin='lower')
pl.axes.get_xaxis().set_visible(False)
pl.axes.get_yaxis().set_visible(False)
pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
line([280,753], [440,440], pl=pl, auto_ylim=False, y_min=0, y_max=1000,
             auto_xlim=False, x_min=0, x_max=1600)
line([50,50+236.5], [100,100], pl=pl, auto_ylim=False, y_min=-250, y_max=1350,
             auto_xlim=False, x_min=0, x_max=1600)
pl.axes.text(20, 100, "$100\,\mathrm{\mu m}$")

pl.axes.text(20, 1000, "LiNbO$_3$")

pl.axes.text(500, 1000, "Al")

pl.axes.text(800, 1000, "Au")


pl.figure.text(0.0, 0.95, "a)")
pl.figure.text(0.53, 0.95, "b)")
pl.figure.text(0.0, 0.45, "c)")
pl.figure.text(0.53, 0.45, "d)")

pl.nplot=3

img=imread(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/Lamb_shift_source/Good_sample_images/left_21.tif")
pl.axes.imshow(flipud(img), origin='lower')
pl.axes.get_xaxis().set_visible(False)
pl.axes.get_yaxis().set_visible(False)
pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
line([20.5,57.7], [39,39], pl=pl, auto_ylim=False, y_min=0, y_max=1000,
             auto_xlim=False, x_min=0, x_max=1000)
#line([100+20.5,100+57.7], [139,139], pl=pl, auto_ylim=False, y_min=100, y_max=665,
#             auto_xlim=False, x_min=100, x_max=665)
line([150,150+151], [139,139], pl=pl, auto_ylim=False, y_min=100, y_max=665,
             auto_xlim=False, x_min=100, x_max=665, color="white")
pl.axes.text(150, 150, "$1\,\mu m$", color="white")
pl.axes.text(600, 600, "Al", color="white")

pl.nplot=4

img=imread(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/Lamb_shift_source/Good_sample_images/qdt_31.tif")

#img=rotate(img, -2.9, reshape=False)
#img=img[50:-50, :, :]
pl.axes.imshow(flipud(img), origin='lower')
pl.axes.get_xaxis().set_visible(False)
pl.axes.get_yaxis().set_visible(False)
pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
line([20.5, 96], [39,39], pl=pl, auto_ylim=False, y_min=0, y_max=1000,
             auto_xlim=False, x_min=0, x_max=1000)

#line([50,50+236.5], [100,100], pl=pl, auto_ylim=False, y_min=-250, y_max=1350,
#             auto_xlim=False, x_min=0, x_max=1600)
#pl.axes.text(20, 100, "$100\,\mathrm{\mu m}$")

#    plt.xlim(0, 100
#    plt.ylim(0, 100)


def box(x=0, y=0, w=5, h=10, g=6, label="$G_a$", 
        color=color, fontsize=fontsize, linewidth=linewidth, lx=0.0, ly=0.0, **kwargs):
    pl=line([x, x, x-w, x+w], [y+h+g, y+g, y+g, y+g], color=color, linewidth=linewidth, **kwargs)
    line([x-w, x-w], [y-g, y+g], color=color, linewidth=linewidth, **kwargs)
    line([x, x, x-w, x+w], [y-h-g, y-g, y-g, y-g], color=color, linewidth=linewidth, **kwargs)
    line([x+w, x+w], [y-g, y+g], color=color, linewidth=linewidth, **kwargs)
    pl.axes.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")

pl.show()

def hbox(x=0, y=0, w=5, h=10, g=6, label="$Z_C$", color=color, 
         fontsize=fontsize, linewidth=linewidth, lx=0.0, ly=0.0, **kwargs):
    pl=line([x+h+g, x+g, x+g, x+g], [y, y, y-w, y+w], color=color, linewidth=linewidth, **kwargs)
    line([x-g, x+g], [y-w, y-w], color=color, linewidth=linewidth, **kwargs)
    line([x-h-g, x-g, x-g, x-g], [y, y, y-w, y+w], color=color, linewidth=linewidth, **kwargs)
    line([x-g, x+g], [y+w, y+w], color=color, linewidth=linewidth, **kwargs)
    pl.axes.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center", **kwargs)

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

if __name__=="__main__":
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