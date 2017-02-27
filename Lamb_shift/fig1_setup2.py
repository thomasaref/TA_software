# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 09:31:29 2017

@author: thomasaref
"""

from taref.plotter.api import line
from TA88_fundamental import TA88_Lyzer
#from fig1_setup import IDT

from numpy import linspace, pi, cos, sin, flipud
from matplotlib.image import imread
from scipy.ndimage import rotate
#f=plt.figure(figsize=(4.5, 4.5)) #, tight_layout=True)
#f.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
#axes=f.add_subplot(111)
#axes.get_xaxis().set_visible(False)
#axes.get_yaxis().set_visible(False)
import_image=True
show_axes=False
color="black"
linewidth=1.0
fontsize=8
sp=20
x=20
y=28
#f.text(0, 0.9, "a)", fontsize=fontsize)

pl="fig1"
a=TA88_Lyzer()
a.save_folder.main_dir="fig1_setup"

def capacitor(x=0, y=0, w=5, h=22, g=2, label="$C_C$", lx=5, ly=7,
               color=color, fontsize=fontsize, linewidth=linewidth, **kwargs):
    pl=line([x, x, x-w, x+w], [y+h+g, y+g, y+g, y+g], color=color, linewidth=linewidth, **kwargs)
    line([x, x, x-w, x+w], [y-h-g, y-g, y-g, y-g], color=color, linewidth=linewidth, pl=pl)
    pl.axes.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")
    return pl

def box(x=0, y=0, w=5, h=10, g=14, label="$G_a$",
        color=color, fontsize=fontsize, linewidth=linewidth, lx=0.0, ly=0.0, **kwargs):
    pl=line([x, x, x-w, x+w], [y+h+g, y+g, y+g, y+g], color=color, linewidth=linewidth, **kwargs)
    line([x-w, x-w], [y-g, y+g], color=color, linewidth=linewidth, **kwargs)
    line([x, x, x-w, x+w], [y-h-g, y-g, y-g, y-g], color=color, linewidth=linewidth, **kwargs)
    line([x+w, x+w], [y-g, y+g], color=color, linewidth=linewidth, **kwargs)
    if label is not None:
        pl.axes.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")
    return pl


def hbox(x=0, y=0, w=5, h=10, g=6, label="$Z_C$", color=color,
         fontsize=fontsize, linewidth=linewidth, lx=0.0, ly=0.0, **kwargs):
    pl=line([x+h+g, x+g, x+g, x+g], [y, y, y-w, y+w], color=color, linewidth=linewidth, **kwargs)
    line([x-g, x+g], [y-w, y-w], color=color, linewidth=linewidth, **kwargs)
    line([x-h-g, x-g, x-g, x-g], [y, y, y-w, y+w], color=color, linewidth=linewidth, **kwargs)
    line([x-g, x+g], [y+w, y+w], color=color, linewidth=linewidth, **kwargs)
    pl.axes.text(x+lx, y+ly, label, fontsize=fontsize, color=color, ha="center", va="center")
    return pl

def IDT(x=0, y=0, sp=20, **kwargs):
    box(x, y, **kwargs)
    box(x+sp, y, label="$iB_a$", **kwargs)
    capacitor(x+2*sp, y, label="$C_t$", **kwargs)
    #plt.plot([x, x+2*sp], [y+3.5, y+3.5], color=color, linewidth=linewidth)
    #plt.plot([x, x+2*sp], [y-3.5, y-3.5], color=color, linewidth=linewidth)

def IDT_r(x=0, y=0, sp=10, **kwargs):
    box(x+2*sp, y, **kwargs)
    box(x+sp, y, label="$iB_a$", **kwargs)
    capacitor(x, y, **kwargs)
    #plt.plot([x, x+2*sp], [y+3.5, y+3.5], color=color, linewidth=linewidth)
    #plt.plot([x+0, x+2*sp], [y-3.5, y-3.5], color=color, linewidth=linewidth)

def JJ(x=0, y=0, jjx=2.0, jjy=2.0, color=color, linewidth=linewidth, **kwargs):
    line([x-jjx, x+jjx], [y-jjy, y+jjy], color=color, linewidth=linewidth, **kwargs)
    line([x-jjx, x+jjx], [y+jjy, y-jjy], color=color, linewidth=linewidth, **kwargs)

def SQUID(x=0, y=0, w=8, g=14, h=10, jjx=2, jjy=2, color=color, linewidth=linewidth,
          label="$L_J$", lx=6, ly=20, **kwargs):
    box(x=x, y=y, w=w, g=g, h=h, color=color, linewidth=linewidth, label=label, lx=lx, ly=ly, **kwargs)
    JJ(x-w, y, jjx=jjx, jjy=jjy, color=color, linewidth=linewidth, **kwargs)
    JJ(x+w, y, jjx=jjx, jjy=jjy, color=color, linewidth=linewidth, **kwargs)

def circle(x=0, y=0, r=1, Nsteps=101, color=color, linewidth=linewidth, **kwargs):
    theta=linspace(0, 2*pi, Nsteps)
    x_arr=x+r*cos(theta)
    y_arr=y+r*sin(theta)
    line(x_arr, y_arr, color=color, linewidth=linewidth, **kwargs)

def arc_arrow(x=0, y=0, angle=13*pi/8.0, sangle=0.0, r=1, Nsteps=101, xa=0.01, ya=0.007, color=color, linewidth=linewidth, **kwargs):
    theta=linspace(sangle, angle, Nsteps)
    x_arr=x+r*cos(theta)
    y_arr=y+r*sin(theta)
    line(x_arr, y_arr, color=color, linewidth=linewidth, **kwargs)
    pl.axes.arrow(x_arr[-1], y_arr[-1], xa, ya, shape='full', lw=linewidth,
                  length_includes_head=False, edgecolor="black", facecolor="black",
                  head_width=10)

def wave(x=0, y=0, Nsteps=101, w=8, f=2, A=3, color=color, linewidth=linewidth, **kwargs):
    theta=linspace(0, 2*pi*f, Nsteps)
    x_arr=linspace(x, x+w, Nsteps)
    y_arr=y+A*sin(theta)
    line(x_arr, y_arr, color=color, linewidth=linewidth, **kwargs)

if __name__=="__main__":
    pl=capacitor(x=50, y=45+23, h=14, g=2,
             ncols=2, nrows=2, nplot=2,
             auto_ylim=False, y_min=0, y_max=100,
             auto_xlim=False, x_min=0, x_max=100, pl=pl, fig_width=3.5, fig_height=3.5)

    IDT(20, 20+8, pl=pl)
    SQUID(80, 20+8, pl=pl)
    hbox(x=50-16, y=9+45+30, pl=pl)
    line([x, x+3*sp], [y+16+8, y+16+8], color=color, linewidth=linewidth, pl=pl)
    line([x, x+3*sp], [y-16-8, y-16-8], color=color, linewidth=linewidth, pl=pl)
    circle(80,28, r=2, pl=pl)
    circle(80,28, r=0.2, pl=pl)
    pl.axes.text(80, 20, "$\Phi_B$", fontsize=fontsize, color=color, ha="center", va="center")
    wave(5,28, color="green", pl=pl)
    wave(5,83, color="blue", pl=pl)

    #plt.figure(figsize=(6.4, 4.4))
    #f.savefig("testy_circuit_draw", dpi=150, bbox_inches='tight', transparent=True)

    pl.axes.get_xaxis().set_visible(False)
    pl.axes.get_yaxis().set_visible(False)
    pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.1, hspace = 0.1)

    #pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
    pl.nplot=1
    if import_image:
        img=imread(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/Lamb_shift_source/Good_sample_images/Alignment_Johan-000001.png")
        #img=imread(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/Lamb_shift_source/Good_sample_images/TA210715A46-000000.png")
        img=rotate(img, -2.9, reshape=False)
        img=img[50:-50, 400:1400, :]
        print img.shape
        pl.axes.imshow(flipud(img), origin='lower')
        #line([280,753], [440,440], pl=pl, auto_ylim=False, y_min=0, y_max=1000,
        #             auto_xlim=False, x_min=0, x_max=1600)
        #line([50,50+236.5], [100,100], pl=pl, auto_ylim=False, y_min=-250, y_max=1350,
        #             auto_xlim=False, x_min=0, x_max=1600)

        #line([50,50+236.5], [100,100], pl=pl, auto_ylim=False, y_min=150, y_max=1550,
        #             auto_xlim=False, x_min=-200, x_max=1200)
    if 0:
        line([195, 432], [487, 487], pl=pl)
    line([80, 80+2*118.5], [250, 250], pl=pl, linewidth=10,
         auto_ylim=False, y_min=150, y_max=1550,
                 auto_xlim=False, x_min=-200, x_max=1200, color="black")
    #left circuit
    circle(-95,578, r=80, pl=pl)
    arc_arrow(-95, 578, r=50, pl=pl)

    circle(-95,300, r=80, pl=pl)
    circle(-95,820, r=80, pl=pl)
    arc_arrow(-95, 820, r=50, pl=pl)
    box(-95-78, y=820, w=10, g=10, h=0, label=None, pl=pl)

    line([-175, -15], [1000, 1000], pl=pl, color=color, linewidth=linewidth)
    line([-175, -95], [1000, 1150], pl=pl, color=color, linewidth=linewidth)
    line([-15, -95], [1000, 1150], pl=pl, color=color, linewidth=linewidth)
    wave(-130,300, w=80, A=50, f=1, color="green", pl=pl)

    line([-95, -95], [1150, 1400], pl=pl, color=color, linewidth=linewidth)
    line([-95, -95], [900, 1000], pl=pl, color=color, linewidth=linewidth)
    line([-95, -95], [578+80, 820-80], pl=pl, color=color, linewidth=linewidth)
    line([-95, -95], [300+80, 578-80], pl=pl, color=color, linewidth=linewidth)
    line([-95+80, -95+80+50], [578, 578], pl=pl, color=color, linewidth=linewidth)

    #right circuit
    hshift=1190.0
    circle(-95+hshift,578, r=80, pl=pl)
    arc_arrow(-95+hshift, 578, r=50, sangle=-pi, angle=-pi-13*pi/8.0, xa=-0.01, ya=0.007, pl=pl)
    arc_arrow(-95+hshift, 820, r=50, sangle=-pi, angle=-pi-13*pi/8.0, xa=-0.01, ya=0.007, pl=pl)
    box(-95+hshift+78, y=820, w=10, g=10, h=0, label=None, pl=pl)
    circle(-95+hshift,300, r=80, pl=pl)
    circle(-95+hshift,820, r=80, pl=pl)
    line([-175+hshift, -15+hshift], [1000, 1000], pl=pl, color=color, linewidth=linewidth)
    line([-175+hshift, -95+hshift], [1000, 1150], pl=pl, color=color, linewidth=linewidth)
    line([-15+hshift, -95+hshift], [1000, 1150], pl=pl, color=color, linewidth=linewidth)
    wave(-130+hshift,300, w=80, A=50, f=1, color="red", pl=pl)

    line([-95+hshift, -95+hshift], [1150, 1520], pl=pl, color=color, linewidth=linewidth)
    line([-95+hshift, -95+hshift], [900, 1000], pl=pl, color=color, linewidth=linewidth)
    line([-95+hshift, -95+hshift], [578+80, 820-80], pl=pl, color=color, linewidth=linewidth)
    line([-95+hshift, -95+hshift], [300+80, 578-80], pl=pl, color=color, linewidth=linewidth)
    line([-95-80+hshift, -95-80-50+hshift], [578, 578], pl=pl, color=color, linewidth=linewidth)

    #top circuit
    circle(200,1250, r=80, pl=pl)
    circle(432,1250, r=80, pl=pl)
    arc_arrow(432, 1250, r=50, pl=pl)
    circle(650,1250, r=80, pl=pl)
    arc_arrow(650, 1250, r=50, pl=pl)
    box(650, y=1250+78, w=10, g=10, h=0, label=None, pl=pl)

    line([850-80, 850+80], [1300, 1300], pl=pl, color=color, linewidth=linewidth)
    line([850-80, 850], [1300, 1450], pl=pl, color=color, linewidth=linewidth)
    line([850+80, 850], [1300, 1450], pl=pl, color=color, linewidth=linewidth)
    wave(160,1250, w=80, A=50, f=1, color="blue", pl=pl)

    line([850, 850], [1450, 1520], pl=pl, color=color, linewidth=linewidth)
    line([280, 432-80], [1250, 1250], pl=pl, color=color, linewidth=linewidth)
    line([432+80, 650-80], [1250, 1250], pl=pl, color=color, linewidth=linewidth)
    line([650+80, 850], [1250, 1250], pl=pl, color=color, linewidth=linewidth)
    line([432, 432], [1250-80, 1250-80-130], pl=pl, color=color, linewidth=linewidth)
    line([850, 850], [1250, 1300], pl=pl, color=color, linewidth=linewidth)


    pl.axes.axis("off")


    pl.axes.get_xaxis().set_visible(False)
    pl.axes.get_yaxis().set_visible(False)
    #pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
    pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.1, hspace = 0.1)

    pl.axes.text(75, 230, "$200\,\mathrm{\mu m}$", color="white")

    pl.axes.text(20, 650, "LiNbO$_3$", color="white")

    #pl.axes.text(500, 1000, "Al")

    pl.axes.text(20, 1000, "Au")


    pl.figure.text(0.03, 0.95, "a)")
    pl.figure.text(0.53, 0.95, "b)")
    pl.figure.text(0.03, 0.45, "c)", color="white")
    pl.figure.text(0.53, 0.45, "d)")

    pl.nplot=3
    if import_image:
        img=imread(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/Lamb_shift_source/Good_sample_images/left_21.tif")
        print img.shape
        pl.axes.imshow(flipud(img), origin='lower')
    line([20.5,57.7], [39,39], pl=pl, auto_ylim=False, y_min=0, y_max=1000,
                 auto_xlim=False, x_min=0, x_max=1000)
    pl.axes.get_xaxis().set_visible(False)
    pl.axes.get_yaxis().set_visible(False)
    #pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.0, hspace = 0.0)
    pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.1, hspace = 0.1)

    #line([100+20.5,100+57.7], [139,139], pl=pl, auto_ylim=False, y_min=100, y_max=665,
    #             auto_xlim=False, x_min=100, x_max=665)
    line([150,150+151], [145,145], pl=pl, auto_ylim=False, y_min=100, y_max=665,
                 auto_xlim=False, x_min=100, x_max=665, color="black", linewidth=10)
    pl.axes.text(180, 140, "$1\,\mu m$", color="white")
    pl.axes.text(600, 620, "Al", color="white")

    pl.nplot=4

    if import_image:
        img=imread(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/Lamb_shift_source/Good_sample_images/qdt_31.tif")

        #img=rotate(img, -2.9, reshape=False)
        #img=img[50:-50, :, :]
        pl.axes.imshow(flipud(img), origin='lower')
    line([20.5, 95.5], [39,39], pl=pl, auto_ylim=False, y_min=0, y_max=1000,
                 auto_xlim=False, x_min=0, x_max=1000)

    pl.axes.get_xaxis().set_visible(False)
    pl.axes.get_yaxis().set_visible(False)

    pl.figure.subplots_adjust(left = 0.0, right = 1.0, bottom = 0.0, top = 1.0, wspace = 0.1, hspace = 0.1)

    pl.axes.text(220, 620, "$2\,\mu m$", color="white")

    line([230,230+75], [630, 630], pl=pl, auto_ylim=False, y_min=80, y_max=770,
                 auto_xlim=False, x_min=180, x_max=870, linewidth=10, color="black")
    #pl.axes.text(20, 100, "$100\,\mathrm{\mu m}$")

    #    plt.xlim(0, 100
    #    plt.ylim(0, 100)
    pl.figure.tight_layout()
    a.save_plots([pl,])
    pl.show()

