# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:53:43 2016

@author: thomasaref
"""

class mpl_drag_event(object):
    def __init__(self, pltr):
        self.pltr=pltr

    def __call__(self, event):

        xmin, xmax=self.pltr.axe.get_xlim()
        ymin, ymax=self.pltr.axe.get_ylim()
        if xmin!=self.pltr.x_min or xmax!=self.pltr.x_max:
            self.pltr.set_xlim(xmin, xmax)
        if ymin!=self.pltr.y_min or ymax!=self.pltr.y_max:
            self.pltr.set_ylim(ymin, ymax)
        if self.pltr.drawline==True:
            self.pltr.line_plot("dist", [self.pltr.xstart, event.xdata], [self.pltr.ystart, event.ydata], append=False,
                                xlim=(xmin, xmax), ylim=(ymin, ymax))
            self.pltr.draw()

class mpl_click_event(object):
    def __init__(self, pltr, x=None, y=None):
        self.pltr=pltr
        self.h_axe=self.pltr.horiz_axe
        self.v_axe=self.pltr.vert_axe
        self.data=self.pltr.alldata
        self.x=x
        self.y=y
        self.h_line=None
        self.v_line=None


    def __call__(self, event):
        if event.inaxes is not None:
            xpos=argmin(absolute(event.xdata-self.x))
            ypos=argmin(absolute(event.ydata-self.y))
            self.pltr.xcoord=event.xdata
            self.pltr.ycoord=event.ydata
            self.pltr.xind=xpos
            self.pltr.yind=ypos
            if self.h_line is None:
                self.min=amin(self.data)
                self.max=amax(self.data)
                self.h_line=self.h_axe.plot(self.data[ypos, :])[0]
                self.v_line=self.v_axe.plot(self.data[:, xpos], arange(201))[0]
            else:
                h_data=self.data[ypos, :]
                self.h_line.set_ydata(h_data)
                self.h_axe.set_ylim(min(h_data), max(h_data))
                v_data=self.data[:, xpos]
                self.v_line.set_xdata(v_data)
                self.v_axe.set_xlim(min(v_data), max(v_data))
            if self.pltr.horiz_fig.canvas!=None:
                self.pltr.horiz_fig.canvas.draw()
            if self.pltr.vert_fig.canvas!=None:
                self.pltr.vert_fig.canvas.draw()

            #xmin, xmax=self.pltr.axe.get_xlim()
            #ymin, ymax=self.pltr.axe.get_ylim()

            #self.pltr.line_plot("horiz", [xmin, xmax], [event.ydata, event.ydata], append=False,
                                #xlim=(xmin, xmax), ylim=(ymin, ymax))
            #self.pltr.draw()

        #xpos=argmin(absolute(event.xdata-self.x))
        #ypos=argmin(absolute(event.ydata-self.y))
        #log_debug(xpos, ypos)

        #['__doc__', '__init__', '__module__', '__str__', '_update_enter_leave', 'button', 'canvas', 'dblclick', 'guiEvent', 'inaxes', 'key', 'lastevent', 'name', 'step', 'x', 'xdata', 'y', 'ydata']
#        if event.dblclick:
#            x=event.xdata
#            y=event.ydata
#            xdist=(self.pltr.x_max-self.pltr.x_min)
#            ydist=(self.pltr.y_max-self.pltr.y_min)
#
#            self.pltr.set_xlim(x-xdist/2.0, x+xdist/2.0)#self.pltr.x_max-1.0*event.step*self.pltr.x_zoom_step)
#            self.pltr.set_ylim(y-ydist/2.0, y+ydist/2.0)#self.pltr.y_min+event.step*self.pltr.y_zoom_step, self.pltr.y_max-1.0*event.step*self.pltr.y_zoom_step)
#            self.pltr.draw()
#        else:
#            if self.x is None:
#                self.x=event.xdata
#                self.y=event.ydata
#                self.pltr.xstart=self.x
#                self.pltr.ystart=self.y
#                self.pltr.drawline=True
#            else:
#                self.pltr.xdist=event.xdata-self.x
#                self.pltr.ydist=event.ydata-self.y
#                self.x=None
#                self.y=None
#                self.pltr.drawline=False

class mpl_scroll_event(object):
    def __init__(self, pltr):
        self.pltr=pltr

    def __call__(self, event):
        x=(self.pltr.x_max+self.pltr.x_min)/2.0 #event.xdata
        y=(self.pltr.y_max+self.pltr.y_min)/2.0
        xdist=(self.pltr.x_max-self.pltr.x_min)*(1.0-event.step/5.0)
        ydist=(self.pltr.y_max-self.pltr.y_min)*(1.0-event.step/5.0)

        self.pltr.set_xlim(x-xdist/2.0, x+xdist/2.0)#self.pltr.x_max-1.0*event.step*self.pltr.x_zoom_step)
        self.pltr.set_ylim(y-ydist/2.0, y+ydist/2.0)#self.pltr.y_min+event.step*self.pltr.y_zoom_step, self.pltr.y_max-1.0*event.step*self.pltr.y_zoom_step)
        self.pltr.draw()
