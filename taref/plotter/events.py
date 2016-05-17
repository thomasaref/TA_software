# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:53:43 2016

@author: thomasaref
"""

#from plotter_backbone import PlotUpdate
from numpy import argmin, absolute, amin, amax#, arange
from atom.api import Atom, Float, Int, Bool, observe#, cache_property
from taref.core.property import tag_property
from numpy import sqrt
from collections import OrderedDict

class MPLEventHandler(Atom):
    drawline=Bool()

    xstart=Float()
    xend=Float()

    @tag_property()
    def xdist(self):
        return self.xend-self.xstart

    ystart=Float()
    yend=Float()

    @tag_property()
    def ydist(self):
        return self.yend-self.ystart

    @tag_property()
    def total_dist(self):
        self.get_member("xdist").reset(self)
        self.get_member("ydist").reset(self)
        return sqrt(self.xdist**2+self.ydist**2)

    @observe("xend", "yend")
    def total_dist_calc(self, change):
        if change["type"]=="update":
            self.get_member("total_dist").reset(self)

class mpl_event(object):
    def __init__(self, pltr):
        self.pltr=pltr

class mpl_scroll(mpl_event):
    def __call__(self, event):
        xmin, xmax=self.pltr.axes.get_xlim()
        ymin, ymax=self.pltr.axes.get_ylim()

        x=(xmax+xmin)/2.0
        y=(ymax+ymin)/2.0
        xdist=(xmax-xmin)*(1.0-event.step/5.0)
        ydist=(ymax-ymin)*(1.0-event.step/5.0)

        self.pltr.set_xlim(x-xdist/2.0, x+xdist/2.0)
        self.pltr.set_ylim(y-ydist/2.0, y+ydist/2.0)
        self.pltr.draw()

class mpl_dblclick_move(mpl_event):
    def __call__(self, event):
        if event.inaxes is not None:
            if event.dblclick:
                x=event.xdata
                y=event.ydata
                xmin, xmax=self.pltr.axes.get_xlim()
                ymin, ymax=self.pltr.axes.get_ylim()
                xdist=(xmax-xmin)
                ydist=(ymax-ymin)
                self.pltr.set_xlim(x-xdist/2.0, x+xdist/2.0)#self.pltr.x_max-1.0*event.step*self.pltr.x_zoom_step)
                self.pltr.set_ylim(y-ydist/2.0, y+ydist/2.0)#self.pltr.y_min+event.step*self.pltr.y_zoom_step, self.pltr.y_max-1.0*event.step*self.pltr.y_zoom_step)
                self.pltr.draw()

class mpl_drag(mpl_event):
    def __call__(self, event):
        if event.inaxes is not None:
            xmin, xmax=self.pltr.axes.get_xlim()
            ymin, ymax=self.pltr.axes.get_ylim()
            if xmin!=self.pltr.x_min or xmax!=self.pltr.x_max:
                self.pltr.set_xlim(xmin, xmax)
            if ymin!=self.pltr.y_min or ymax!=self.pltr.y_max:
                self.pltr.set_ylim(ymin, ymax)
            if self.pltr.drawline==True:
                self.pltr.line_plot("dist", [self.pltr.xstart, event.xdata], [self.pltr.ystart, event.ydata], append=False,
                                    xlim=(xmin, xmax), ylim=(ymin, ymax))
                self.pltr.draw()

class mpl_cross_section(mpl_event):
    def __init__(self, plot_format):
        self.pltr=plot_format.plotter
        self.pfs=[pf for pf in self.pltr.plot_dict.values() if pf.plot_type=="colormap"]

    def __call__(self, event):
        if event.inaxes is not None:
            #xmin, xmax, ymin, ymax=None, None, None, None
            for n, pf in enumerate(self.pfs):
                xpos=argmin(absolute(event.xdata-pf.xdata))
                ypos=argmin(absolute(event.ydata-pf.ydata))
                pf.xcoord=event.xdata
                pf.ycoord=event.ydata
                pf.xind=xpos
                pf.yind=ypos
                if self.pltr.show_cross_section: #self.pf.plot_type=="colormap" and
                    h_data=pf.zdata[ypos, :]
                    v_data=pf.zdata[:, xpos]
                    if pf.h_line is None:
                        pf.h_line=self.pltr.horiz_axe.plot(pf.xdata, h_data)[0]
                        pf.v_line=self.pltr.vert_axe.plot(v_data, pf.ydata)[0]
                    else:
                        pf.h_line.set_ydata(h_data)
                        pf.v_line.set_xdata(v_data)
                        #self.pltr.vert_axe.set_xlim(min(v_data), max(v_data))
                    if self.pltr.auto_cs_ylim:
                        if n==0:
                            ymin=min(h_data)
                            ymax=max(h_data)
                        else:
                            ymin=min((min(h_data), ymin))
                            ymax=max((max(h_data), ymax))
                        self.pltr.cs_y_min=float(ymin)
                        self.pltr.cs_y_max=float(ymax)
                    if self.pltr.auto_cs_xlim:
                        if n==0:
                            xmin=min(v_data)
                            xmax=max(v_data)
                        else:
                            xmin=min((min(v_data), xmin))
                            xmax=max((max(v_data), xmax))
                        self.pltr.cs_x_min=float(xmin)
                        self.pltr.cs_x_max=float(xmax)

                        #self.pltr.cs_x_min=float(min((self.pltr.cs_x_min, min(v_data))))
                        #self.pltr.cs_x_max=float(max((self.pltr.cs_x_max, max(v_data))))

                        #self.pltr.horiz_axe.set_xlim(min(pf.xdata), max(pf.xdata))
                    #if self.pltr.auto_cs_ylim:
                        #self.pltr.horiz_axe.set_ylim(min(pf.ydata), max(pf.ydata))
                    if self.pltr.horiz_fig.canvas!=None:
                        self.pltr.horiz_fig.canvas.draw()
                    if self.pltr.vert_fig.canvas!=None:
                        self.pltr.vert_fig.canvas.draw()

            cc=self.pltr.plot_dict.get("cross_cursor", None)
            if cc is not None and self.pltr.show_cross_cursor:
                cc.move_cursor(event.xdata, event.ydata)
                self.pltr.draw()
            #xmin, xmax=self.pltr.axe.get_xlim()
            #ymin, ymax=self.pltr.axe.get_ylim()

            #self.pltr.line_plot("horiz", [xmin, xmax], [event.ydata, event.ydata], append=False,
                                #xlim=(xmin, xmax), ylim=(ymin, ymax))
            #self.pltr.draw()

class mpl_click_event(object):
    def __init__(self, pltr):
        self.pltr=pltr
        self.x=None
        self.y=None

    def __call__(self, event):
        if event.inaxes is not None:
            if event.dblclick:
                x=event.xdata
                y=event.ydata
                xdist=(self.pltr.x_max-self.pltr.x_min)
                ydist=(self.pltr.y_max-self.pltr.y_min)

                self.pltr.set_xlim(x-xdist/2.0, x+xdist/2.0)#self.pltr.x_max-1.0*event.step*self.pltr.x_zoom_step)
                self.pltr.set_ylim(y-ydist/2.0, y+ydist/2.0)#self.pltr.y_min+event.step*self.pltr.y_zoom_step, self.pltr.y_max-1.0*event.step*self.pltr.y_zoom_step)
                self.pltr.draw()
            else:
                if self.x is None:
                    self.x=event.xdata
                    self.y=event.ydata
                    self.pltr.xstart=self.x
                    self.pltr.ystart=self.y
                    self.pltr.drawline=True
                else:
                    self.pltr.xend=event.xdata
                    self.pltr.yend=event.ydata
                    self.pltr.xdist=event.xdata-self.x
                    self.pltr.ydist=event.ydata-self.y
                    self.x=None
                    self.y=None
                    self.pltr.drawline=False


