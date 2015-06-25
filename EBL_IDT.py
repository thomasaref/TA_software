# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:43:01 2015

@author: thomasaref
"""

from Atom_IDT import IDT
from atom.api import Float, Int, Enum, Dict, Callable
from EBL_Item import EBL_Item
from Atom_Plotter import Plotter
from numpy import pi, cos, sin, mod

class EBL_IDT(EBL_Item, IDT):
    """handles everything related to drawing a IDT. Units are microns (um)"""
    trconnect_x=Float(9.0).tag(desc="connection length of transmon")
    trconnect_y=Float(2.5).tag(desc="connection length of transmon")
    trconnect_w=Float(0.5).tag(desc="connection length of transmon")
    trc_wbox=Float(14.0)
    trc_hbox=Float(12.5)
    g=Float(0.05).tag(desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz")
    o=Float(0.5).tag(desc="gap between electrode and end of finger. The vertical offset of the fingers. Setting this to zero produces a shorted reflector")
    #h=Float(25.5).tag(desc="height of finger. Equivalenbt to W")
    hbox=Float(20.0).tag(desc="height of electrode box")
    wbox=Float(0.0).tag(desc="width of electrode box. Setting to 0.0 (default) makes it autoscaling so it matches the width of the IDT")

    idt_tooth=Float(0.3).tag(desc="tooth size on CPW connection to aid contact")
    idt_numteeth=Int(5) #52 um, 12.5 um
    
    idt_type=Enum("basic", "stepped", "angle")
    qdt_type=Enum("IDT", "QDT")

    make_idt_dict=Dict().tag(private=True)
    
    conn_h=Float(65.0)
    #singleIDT=Callable()
    #doubleIDT=Callable()
    
    def plot(self):
        self.boss.plot.delete_all_plots() #=Plotter()
        self.makeIDT()
        for n,p in enumerate(self.polys.polylist):
            self.boss.plot.add_poly_plot(n=n, verts=p.get_verts(), cn=p.color, polyname=self.name)
        self.boss.plot.plot.request_redraw()  
    
    def _default_make_idt_dict(self):
        return dict(basic={"double": self.doubleIDT,
                           "single": self.singleIDT},
                    stepped={"double": self.doubleIDT,
                             "single": self.singleIDT},
                    angle={"double": self.doubleIDT,
                           "single": self.singleIDT})
                           
    def makeIDT(self):
        """Draws IDT depending on object parameters"""
        self.polys.polylist=[] #list of polygons that make up IDT pattern
        self.make_idt_dict[self.idt_type][self.df]()
        
    def singleIDT(self):
        """Add polygons representing qubit single fingered IDT to polylist (central fingers connect bottom to top)"""
        #write IDT
        #for a in range(-(self.Np-1), self.Np, 2):
        #    self.C(a*(self.a+self.g), self.o/2.0, self.a, self.W)
        #    self.C((a-1)*(self.a+self.g), -self.o/2.0, self.a, self.W)
        #self.C(self.Np*(self.a+self.g), -self.o/2.0, self.a, self.W)
        
        self.singleIDTfingers()
        self.singleIDTextrafingers()        
        ##write extra fingers
        #for a in range(0, self.ef):
        #    self.C(-a*(self.a+self.g)-(self.Np+1)*(self.a+self.g), -self.o/2.0, self.a, self.W)
        #    self.C(a*(self.a+self.g)+(self.Np+1)*(self.a+self.g), -self.o/2.0, self.a, self.W)

        #write connecting box at top and bottom
        if self.wbox==0.0:
            wr=self.Np*(2*self.a+2*self.g) +self.a+self.ef*(self.a+self.g)*2
        else:
            wr=self.wbox
        self.C(0, self.o/2.0+self.W/2.0+self.hbox/2.0, wr, self.hbox)
        self.C(0, -self.o/2.0-self.W/2.0-self.hbox/2.0, wr, self.hbox)

    def singleIDTfingers(self):
        for a in range(-(self.Np-1), self.Np, 2):
            self.C(a*(self.a+self.g), self.o/2.0, self.a, self.W)
            self.C((a-1)*(self.a+self.g), -self.o/2.0, self.a, self.W)
            if a in [-1,0] and self.qdt_type=="QDT":
                self.C(a*(self.a+self.g), -self.W/2.0-self.trconnect_y/2.0, self.a, self.o+self.trconnect_y)
                self.C(a*(self.a+self.g), -self.W/2.0-self.o/2.0-self.trc_hbox+self.trconnect_y/2.0-self.trconnect_w, self.a, self.trconnect_y)
        self.C(self.Np*(self.a+self.g), -self.o/2.0, self.a, self.W)

    def singleIDTextrafingers(self):
        """write extra fingers for single IDT"""
        for a in range(0, self.ef):
            self.C(-a*(self.a+self.g)-(self.Np+1)*(self.a+self.g), -self.o/2.0, self.a, self.W)
            self.C(a*(self.a+self.g)+(self.Np+1)*(self.a+self.g), -self.o/2.0, self.a, self.W)

    def doubleIDT(self):
        self.qubitsingleIDT()
    
    def qubitgate_and_gnd(self):
        self.P([(-self.trc_wbox/2.0, -self.o/2.0-self.W/2.0-self.trc_hbox),
                (self.trc_wbox/2.0, -self.o/2.0-self.W/2.0-self.trc_hbox),
                (self.trc_wbox/2.0, -self.conn_h),
                (-self.trc_wbox/2.0, -self.conn_h)])
        self.P([(-self.trc_wbox/2.0, self.o/2.0+self.W/2.0+self.hbox+10.0-0.25),
                (self.trc_wbox/2.0, self.o/2.0+self.W/2.0+self.hbox+10.0-0.25),
                (self.trc_wbox/2.0, 125.0),
                   (-self.trc_wbox/2.0, 125.0)])

    def squidtouch(self):
        #write top squid touch
        self.C(0, -self.o-self.W/2.0-self.trconnect_y-self.trconnect_w/2.0, self.trconnect_x, self.trconnect_w)

        #write bottom squid touch
        self.C(0, -self.o/2.0-self.trc_hbox+self.trconnect_y-self.trconnect_w/2.0, self.trconnect_x, self.trconnect_w)
        #self.C(0, -self.o/2.0-self.trc_hbox+self.W/2.0-self.trconnect_w/2.0, self.trc_wbox, self.trconnect_w)

    def qubitsingleIDT(self):
        """Add polygons representing qubit single fingered IDT to polylist (central fingers connect bottom to top)"""
        self.singleIDTfingers()
        self.singleIDTextrafingers()

        #write top box
        if self.wbox==0.0:
            wr=self.Np*(2*self.a+2*self.g) +self.a+self.ef*(self.a+self.g)*2
        else:
            wr=self.wbox
        self.C(0, self.o/2.0+self.W/2.0+self.hbox/2.0, wr, self.hbox)
        #self.C(0, -self.o/2.0-self.W/2.0-self.hbox/2.0, wr, self.hbox)
        
        #self.squid_touch()
        
        #write left part of transmon connect
        if mod(self.Np, 2)==0:
            wr=-(self.ef*(self.a+self.g)+(self.Np-1)*(self.a+self.g)-self.g)
            xr=-self.a/2.0-2.0*self.g-self.a
        else:
            wr=-(self.ef*(self.a+self.g)+self.Np*(self.a+self.g)-self.g)
            xr=-self.a/2.0-self.g
        self.R(xr, -self.o/2.0-self.W/2.0, wr, -self.trconnect_w)
        self.R(xr, -self.o/2.0-self.W/2.0, -(self.trc_wbox/2.0-self.a/2.0-self.g), -self.trconnect_w)
        self.R(-self.trc_wbox/2.0, -self.o/2.0-self.W/2.0, self.trconnect_w, -self.trc_hbox-self.trconnect_w)

        #write right part of transmon
        if mod(self.Np, 2)==0:
            wr=self.ef*(self.a+self.g)+(self.Np+1)*(self.a+self.g)-self.g
            xr=-self.a/2.0
        else:
            wr=self.ef*(self.a+self.g)+self.Np*(self.a+self.g)-self.g
            xr=self.a/2.0+self.g
        self.R(xr, -self.o/2.0-self.W/2.0, wr, -self.trconnect_w)
        self.R(xr, -self.o/2.0-self.W/2.0, self.trc_wbox/2.0-self.a/2.0-self.g, -self.trconnect_w)
        self.R(self.trc_wbox/2.0, -self.o/2.0-self.W/2.0, wr+self.trconnect_w, -self.trc_hbox-self.trconnect_w)

        self.qubitgate_and_gnd()
        #self.add_qubit_idt_teeth()

    def qubitdoubleIDT2(self):
        """Add polygons representing double finger IDT to polylist"""
        self.yt=self.yidt

        #write IDT
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+2.0*a*(self.w+self.gap)
            self.doubleplusrect()
            self.xt=self.xt-2*(self.w+self.gap)
            self.doubleminusrect()
        self.xt=self.xidt+2.0*self.Np*(self.w+self.gap)
        self.doubleminusrect()

        #Write extra fingers
        for a in range(0, self.ef):
            self.xt=self.xidt-2*a*(self.w+self.gap)-2.0*(self.Np)*(self.w+self.gap)-2.0*(self.gap+self.w)
            self.doubleminusrect()
            self.xt=self.xidt+2*a*(self.w+self.gap)+2.0*(self.Np)*(self.w+self.gap)+2.0*(self.gap+self.w)
            self.doubleminusrect()

        #write connecting box at top and bottom
        if self.wbox==0.0:
            #self.xr=self.xidt#-self.ef*(self.w+self.gap)-2.0*(self.Np-1)*(self.w+self.gap)-2.0*self.w-3.0*self.gap/2.0
            self.wr=4.0*self.ef*(self.w+self.gap)+4.0*self.Np*(self.w+self.gap)+2.0*self.w+self.gap
        else:
            self.xr=self.xidt-self.wbox/2.0
            self.wr=self.wbox
        self.xr=self.xidt
        self.yr=self.yidt+(self.h+self.offset+self.hbox)/2.0
        self.hr=self.hbox
        self.writecenterrect()
        self.xr=self.xidt
        self.yr=self.yidt-(self.h+self.offset+self.hbox)/2.0
        self.hr=-self.hbox

        self.drawdfqubitbottom()
        self.qubitgate_and_gnd()

    def drawdfqubitbottom(self):
        #assumes odd Np

        wboxt=4.0*self.ef*(self.w+self.gap)+4.0*self.Np*(self.w+self.gap)+2.0*self.w+self.gap
        #write left and right parts
        self.xr=self.xidt-self.w-3.0*self.gap/2.0
        self.wr=-(wboxt/2.0-self.w-3.0*self.gap/2.0)
        self.yr=self.yidt-self.offset/2.0-self.h/2.0
        self.hr=-self.trconnect_w
        self.writerect()
        self.xr=self.xidt+self.w+3.0*self.gap/2.0
        self.wr=wboxt/2.0-self.w-3.0*self.gap/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0
        self.hr=-self.trconnect_w
        self.writerect()

        wboxt=self.trc_wbox
        self.xr=self.xidt-self.w-3.0*self.gap/2.0
        self.wr=-(wboxt/2.0-self.w-3.0*self.gap/2.0)
        self.yr=self.yidt-self.offset/2.0-self.h/2.0
        self.hr=-self.trconnect_w
        self.writerect()
        self.xr=self.xidt+self.w+3.0*self.gap/2.0
        self.wr=wboxt/2.0-self.w-3.0*self.gap/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0
        self.hr=-self.trconnect_w
        self.writerect()

        self.xr=self.xidt-wboxt/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0#-self.trconnect
        self.hr=-(self.trc_hbox+self.trconnect_w)
        self.wr=self.trconnect_w
        self.writerect()
        self.xr=self.xidt+wboxt/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0#-self.trconnect
        self.hr=-(self.trc_hbox+self.trconnect_w)
        self.wr=-self.trconnect_w
        self.writerect()
        self.xr=self.xidt-wboxt/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox
        self.hr=-self.trconnect_w
        self.wr=wboxt
        self.writerect()

        #extend center fingers
        self.xr=self.xidt-(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0-self.h/2.0-(self.offset+self.trconnect_y)/2.0
        self.hr=self.offset+self.trconnect_y
        self.wr=self.w
        self.writecenterrect()
        self.xr=self.xidt+(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0-self.h/2.0-(self.offset+self.trconnect_y)/2.0
        self.writecenterrect()

        #extend bottom fingers
        self.xr=self.xidt-(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y/2.0-self.trconnect_w
        self.hr=self.trconnect_y
        self.wr=self.w
        self.writecenterrect()
        self.xr=self.xidt+(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y/2.0-self.trconnect_w
        self.hr=self.trconnect_y
        self.wr=self.w
        self.writecenterrect()

        self.hr=self.h
        #write top squid touch
        self.xr=self.xidt
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect_y-0.5*self.trconnect_w
        self.hr=self.trconnect_w
        self.wr=self.trconnect_x
        self.writecenterrect()

        #write bottom squid touch
        self.xr=self.xidt
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y+0.5*self.trconnect_w-self.trconnect_w
        self.hr=self.trconnect_w
        self.wr=self.trconnect_x
        self.writecenterrect()
        self.add_qubit_idt_teeth()

    def add_qubit_idt_teeth(self):
        
        sqt_x=self.xidt-self.trconnect_x/2.0
        sqt_y=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y

        self.idt_numteeth=int(self.trconnect_x/(2*self.idt_tooth))
        idt_conn=self.idt_tooth*(2*self.idt_numteeth-1)
        sqt_x=self.xidt-idt_conn/2.0
        sqt_y=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y
        sqt_y_top=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect_y-self.trconnect_w

        for i in range(self.idt_numteeth):
            self.rect(sqt_x+2*i*self.idt_tooth, sqt_y, self.idt_tooth, self.idt_tooth )                   
            self.rect(sqt_x+2*i*self.idt_tooth, sqt_y_top, self.idt_tooth, -self.idt_tooth )                   


if __name__=="__main__":
    a=EBL_IDT(name="EBL_Item_test")
    print type(a.boss)
    def runtemp():
        pass
    a.boss.run=runtemp
    a.boss.run_measurement()
    #a.df="single"
    print a.idt_type
    print a.qdt_type 
    a.Np=3
    a.makeIDT()
    a.show()
    


    def makeQubitBox(self):
        self.polylist=[]
        if self.wbox==0.0:
            #self.xr=self.xidt#-self.ef*(self.w+self.gap)-2.0*(self.Np-1)*(self.w+self.gap)-2.0*self.w-3.0*self.gap/2.0
            self.wr=4.0*self.ef*(self.w+self.gap)+4.0*self.Np*(self.w+self.gap)+2.0*self.w+self.gap
        else:
            self.xr=self.xidt-self.wbox/2.0
            self.wr=self.wbox
        self.xr=self.xidt
        self.hr=self.hbox+self.h+self.offset
        self.yr=self.yidt
        self.writecenterrect()

    def rotateIDT(self, theta=0.0):
        theta=theta/180.0*pi
        for n, p in enumerate(self.polylist):
            for m, v in enumerate(p.verts): #=[(s.xr,s.yr), (s.xr+s.wr,s.yr), (s.xr+s.wr, s.yr+s.hr), (s.xr, s.yr+s.hr)]
                x=v[0]
                y=v[1]
                xp=x*cos(theta)-y*sin(theta)
                yp=x*sin(theta)+y*cos(theta)
                p.verts[m]=(xp, yp)

    def makeBeam(self):
        self.polylist=[]
        self.wr=self.w
        self.hr=self.h
        self.beamerDoseTest()

    def beamerDoseTest(self):
        self.yt=self.yidt

        #write IDT
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+a*(self.w+self.gap)
            self.singleIDTpair()

        self.xr=self.xidt-(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0+self.hr/2.0+self.hbox/2.0
        self.hr=self.hbox
        self.writecenterrect()
        self.hr=self.h

    def makequbitIDT(self):
        """Draws IDT depending on object parameters"""
        self.polylist=[] #list of polygons that make up IDT pattern
        self.wr=self.w #set width of idt finger rectangle to w
        self.hr=self.h #set height of idt finger rectangle to h
        if self.df==1: #double fingered
            self.qubitdoubleIDT()
        else:
            self.qubitsingleIDT()

    def makequbitwingfing(self):
        """Draws IDT depending on object parameters"""
        self.polylist=[] #list of polygons that make up IDT pattern
        self.wr=self.w #set width of idt finger rectangle to w
        self.hr=self.h #set height of idt finger rectangle to h
        if self.df==1: #double fingered
            self.qubitdoublewingfing()
        else:
            self.qubitsinglewingfing()

    def singleIDT(self):
        """Add polygons representing qubit single fingered IDT to polylist (central fingers connect bottom to top)"""
        self.yt=self.yidt
        #write IDT
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+a*(self.w+self.gap)
            self.xr=self.xt
            self.yr=self.yt+self.offset/2.0
            self.writecenterrect()
            self.xr=self.xt-(self.w+self.gap)
            self.yr=self.yt-self.offset/2.0
            self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()

        #write extra fingers
        for a in range(0, self.ef):
            self.xr=self.xidt-a*(self.w+self.gap)-(self.Np+1)*(self.w+self.gap)#-(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()
            self.xr=self.xidt+a*(self.w+self.gap)+(self.Np+1)*(self.w+self.gap)#+(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()

        #write connecting box at top and bottom
        self.xr=self.xidt
        self.yr=self.yidt+self.offset/2.0+self.h/2.0+self.hbox/2.0
        self.hr=self.hbox
        if self.wbox==0.0:
            self.wr=self.Np*(2*self.w+2*self.gap) +self.w+self.ef*(self.w+self.gap)*2
        else:
            self.wr=self.wbox
        self.writecenterrect()
        self.xr=self.xidt
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.hbox/2.0
        self.writecenterrect()

    def qubitsingleIDT(self):
        """Add polygons representing qubit single fingered IDT to polylist (central fingers connect bottom to top)"""
        self.yt=self.yidt
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+a*(self.w+self.gap)
            self.xr=self.xt#-(self.w+self.gap)/2.0
            self.yr=self.yt+self.offset/2.0
            self.writecenterrect()
            if a in [-1,0]:
                self.xr=self.xt#-(self.w+self.gap)/2.0
                self.yr=self.yt+self.offset/2.0-self.h/2.0-(self.offset+self.trconnect_y)/2.0
                self.hr=self.offset+self.trconnect_y
                self.writecenterrect()
                self.xr=self.xt
                self.yr=self.yt-self.h/2.0-self.offset/2.0-self.trc_hbox+self.trconnect_y/2.0-self.trconnect_w
                self.hr=self.trconnect_y
                self.writecenterrect()
                self.hr=self.h
            self.xr=self.xt-(self.w+self.gap)
            self.yr=self.yt-self.offset/2.0
            self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()

        #write extra fingers
        for a in range(0, self.ef):
            self.xr=self.xidt-a*(self.w+self.gap)-(self.Np+1)*(self.w+self.gap)#-(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()
            self.xr=self.xidt+a*(self.w+self.gap)+(self.Np+1)*(self.w+self.gap)#+(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()
        #write top box
        self.xr=self.xidt
        self.yr=self.yidt+self.offset/2.0+self.h/2.0+self.hbox/2.0
        self.hr=self.hbox
        if self.wbox==0.0:
            self.wr=self.Np*(2*self.w+2*self.gap) +self.w+self.ef*(self.w+self.gap)*2
        else:
            self.wr=self.wbox
        self.writecenterrect()

        #write bottom box
        self.xr=self.xidt
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect_y/2.0-self.hbox
        self.hr=self.trconnect_w
        #self.writecenterrect()

        #write top squid touch
        self.xr=self.xidt
#        self.yr=self.yidt-3.0*self.trconnect-self.h/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect_y-0.5*self.trconnect_w
        self.hr=self.trconnect_w
        self.wr=self.trconnect_x
        self.writecenterrect()

        #write bottom squid touch
        self.xr=self.xidt
#        self.yr=self.yidt-3.0*self.trconnect-self.h/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y+0.5*self.trconnect_w-self.trconnect_w
        self.hr=self.trconnect_w
        self.wr=self.trconnect_x
        self.writecenterrect()

        self.xr=self.xidt
        self.yr=self.yidt-self.h/2.0-self.offset/2.0-self.trc_hbox-self.trconnect_w/2.0
        self.wr=self.trc_wbox
        self.hr=self.trconnect_w
        self.writecenterrect()

        #self.xr=self.xidt
        self.yr=self.yidt-self.offset/2.0-self.h/2.0#-self.trconnect_y #self.hbox
        self.hr=-self.trconnect_w
        #self.xr=self.xidt-self.ef*(self.w+self.gap)-(self.Np)*(self.w+self.gap)-self.w/2.0

        #write left part of transmon connect
        if mod(self.Np, 2)==0:
            #if self.wbox==0.0:
            self.wr=-(self.ef*(self.w+self.gap)+(self.Np-1)*(self.w+self.gap)-self.gap)
            #else:
            #    self.wr=-(self.wbox/2.0-self.gap-self.w/2.0-self.gap-self.w)
            self.xr=self.xidt-self.w/2.0-2.0*self.gap-self.w
        else:
            #if self.wbox==0.0:
            self.wr=-(self.ef*(self.w+self.gap)+self.Np*(self.w+self.gap)-self.gap)
            #else:
            #    self.wr=-(self.wbox/2.0-self.gap-self.w/2.0)
            self.xr=self.xidt-self.w/2.0-self.gap
        self.writerect()
        self.wr=-(self.trc_wbox/2.0-self.w/2.0-self.gap)
        self.writerect()
        self.xr=self.xidt-self.trc_wbox/2.0
        self.wr=-self.trconnect_w
        self.hr=-self.trc_hbox-self.trconnect_w
        self.writerect()

#        self.xr=self.xr+self.wr
#        self.hr=-(self.hbox-self.trconnect)
#        self.wr=self.trconnect
#        self.writerect()

        #write right part of transmon
        self.yr=self.yidt-self.offset/2.0-self.h/2.0#-self.trconnect_y #self.hbox
        self.hr=-self.trconnect_w
        if mod(self.Np, 2)==0:
            #if self.wbox==0.0:
            self.wr=self.ef*(self.w+self.gap)+(self.Np+1)*(self.w+self.gap)-self.gap
            #else:
            #    self.wr=self.wbox/2.0-self.gap-self.w/2.0+self.gap+self.w
            self.xr=self.xidt+self.w/2.0-self.w
        else:
            #if self.wbox==0.0:
            self.wr=self.ef*(self.w+self.gap)+self.Np*(self.w+self.gap)-self.gap
            #else:
            #    self.wr=self.wbox/2.0-self.gap-self.w/2.0
            self.xr=self.xidt+self.w/2.0+self.gap
        self.writerect()
        self.wr=self.trc_wbox/2.0-self.w/2.0-self.gap #only for odd number
        self.writerect()
        self.xr=self.xidt+self.trc_wbox/2.0
        self.wr=self.trconnect_w
        self.hr=-self.trc_hbox-self.trconnect_w
        self.writerect()
#        self.xr=self.xr+self.wr
#        self.hr=-(self.hbox-self.trconnect)
#        self.wr=-self.trconnect
#        self.writerect()


        #write connecting box at top and bottom
#        if self.wbox==0.0:
#            self.xr=self.xidt-self.ef*(self.w+self.gap)-(self.Np-1)*(self.w+self.gap)-(self.w+self.gap/2.0)
#            self.wr=2.0*(self.ef*(self.w+self.gap)+(self.Np-1)*(self.w+self.gap)+2*self.w+self.gap/2.0)
#        else:
#            self.xr=self.xidt-self.wbox/2.0
#            self.wr=self.wbox
#        self.yr=self.yidt+(self.h+self.offset)/2.0
#        self.hr=self.hbox
#        self.writerect()
#        self.yr=self.yidt-(self.h+self.offset)/2.0
#        # self.xt=self.xidt+a*(self.w+self.gap)
#        if mod(self.Np, 2)==0:
#            self.wr=2.0*(self.ef*(self.w+self.gap)/2.0+(self.Np)/2*(self.w+self.gap)-self.w/2.0-self.gap)
#        else:
#            self.wr=2.0*(self.ef*(self.w+self.gap)/2.0+(self.Np-1)/2*(self.w+self.gap)+self.w/2.0)#-self.gap/2.0)
#        self.hr=-self.hbox
#        #self.wr=self.wr/2.0
#        self.writerect()
#        self.xr=self.xr+self.wr+2*self.gap+self.w
#        if mod(self.Np, 2)==0:
#            self.wr=self.wr+self.w+self.gap
#        else:
#            self.wr=self.wr-self.w-self.gap
#        self.writerect()
        self.qubitgate_and_gnd()
        self.add_qubit_idt_teeth()

    def makequbitgate_and_gnd(self):
        self.polylist=[]
        self.qubitgate_and_gnd()

    def qubitgate_and_gnd(self):
        self.poly([(self.xidt-self.trc_wbox/2.0, self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox),
                   (self.xidt+self.trc_wbox/2.0, self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox),
                   (self.xidt+self.trc_wbox/2.0, self.yidt-65.0),
                   (self.xidt-self.trc_wbox/2.0, self.yidt-65.0)])
        self.poly([(self.xidt-self.trc_wbox/2.0, self.yidt+self.offset/2.0+self.h/2.0+self.hbox+10.0-0.25),
                   (self.xidt+self.trc_wbox/2.0, self.yidt+self.offset/2.0+self.h/2.0+self.hbox+10.0-0.25),
                   (self.xidt+self.trc_wbox/2.0, self.yidt+125.0),
                   (self.xidt-self.trc_wbox/2.0, self.yidt+125.0)])

    def qubitdoublewingfing(self):
        """Add polygons representing double finger IDT to polylist"""
        self.yt=self.yidt

        #write IDT
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+2.0*a*(self.w+self.gap)
            self.doubleplusrect()
            self.xt=self.xt-2*(self.w+self.gap)
            self.doubleminusrect()

        #Write extra fingers
        for a in range(0, self.ef):
            self.xt=self.xidt-2*a*(self.w+self.gap)-2.0*(self.Np)*(self.w+self.gap)-2.0*(self.gap+self.w)
            self.doubleminusrect()
            self.xt=self.xidt+2*a*(self.w+self.gap)+2.0*(self.Np)*(self.w+self.gap)#+2.0*(self.gap+self.w)
            self.doubleplusrect()
        self.xt=self.xidt+2.0*self.Np*(self.w+self.gap)+2*a*(self.w+self.gap)+2.0*(self.gap+self.w)
        self.doubleplusrect()

        #write connecting box at top and bottom
        if self.wbox==0.0:
            #self.xr=self.xidt#-self.ef*(self.w+self.gap)-2.0*(self.Np-1)*(self.w+self.gap)-2.0*self.w-3.0*self.gap/2.0
            self.wr=4.0*self.ef*(self.w+self.gap)+4.0*self.Np*(self.w+self.gap)+2.0*self.w+self.gap
        else:
            self.xr=self.xidt-self.wbox/2.0
            self.wr=self.wbox
        self.xr=self.xidt
        self.yr=self.yidt+(self.h+self.offset+self.hbox)/2.0
        self.hr=self.hbox
        self.writecenterrect()
        self.xr=self.xidt
        self.yr=self.yidt-(self.h+self.offset+self.hbox)/2.0
        self.hr=-self.hbox

        self.drawdfqubitbottom()

    def qubitdoubleIDT(self):
        """Add polygons representing double finger IDT to polylist"""
        self.yt=self.yidt

        #write IDT
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+2.0*a*(self.w+self.gap)
            self.doubleplusrect()
            self.xt=self.xt-2*(self.w+self.gap)
            self.doubleminusrect()
        self.xt=self.xidt+2.0*self.Np*(self.w+self.gap)
        self.doubleminusrect()

        #Write extra fingers
        for a in range(0, self.ef):
            self.xt=self.xidt-2*a*(self.w+self.gap)-2.0*(self.Np)*(self.w+self.gap)-2.0*(self.gap+self.w)
            self.doubleminusrect()
            self.xt=self.xidt+2*a*(self.w+self.gap)+2.0*(self.Np)*(self.w+self.gap)+2.0*(self.gap+self.w)
            self.doubleminusrect()

        #write connecting box at top and bottom
        if self.wbox==0.0:
            #self.xr=self.xidt#-self.ef*(self.w+self.gap)-2.0*(self.Np-1)*(self.w+self.gap)-2.0*self.w-3.0*self.gap/2.0
            self.wr=4.0*self.ef*(self.w+self.gap)+4.0*self.Np*(self.w+self.gap)+2.0*self.w+self.gap
        else:
            self.xr=self.xidt-self.wbox/2.0
            self.wr=self.wbox
        self.xr=self.xidt
        self.yr=self.yidt+(self.h+self.offset+self.hbox)/2.0
        self.hr=self.hbox
        self.writecenterrect()
        self.xr=self.xidt
        self.yr=self.yidt-(self.h+self.offset+self.hbox)/2.0
        self.hr=-self.hbox

        self.drawdfqubitbottom()
        self.qubitgate_and_gnd()

    def drawdfqubitbottom(self):
        #assumes odd Np

        wboxt=4.0*self.ef*(self.w+self.gap)+4.0*self.Np*(self.w+self.gap)+2.0*self.w+self.gap
        #write left and right parts
        self.xr=self.xidt-self.w-3.0*self.gap/2.0
        self.wr=-(wboxt/2.0-self.w-3.0*self.gap/2.0)
        self.yr=self.yidt-self.offset/2.0-self.h/2.0
        self.hr=-self.trconnect_w
        self.writerect()
        self.xr=self.xidt+self.w+3.0*self.gap/2.0
        self.wr=wboxt/2.0-self.w-3.0*self.gap/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0
        self.hr=-self.trconnect_w
        self.writerect()

        wboxt=self.trc_wbox
        self.xr=self.xidt-self.w-3.0*self.gap/2.0
        self.wr=-(wboxt/2.0-self.w-3.0*self.gap/2.0)
        self.yr=self.yidt-self.offset/2.0-self.h/2.0
        self.hr=-self.trconnect_w
        self.writerect()
        self.xr=self.xidt+self.w+3.0*self.gap/2.0
        self.wr=wboxt/2.0-self.w-3.0*self.gap/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0
        self.hr=-self.trconnect_w
        self.writerect()

        self.xr=self.xidt-wboxt/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0#-self.trconnect
        self.hr=-(self.trc_hbox+self.trconnect_w)
        self.wr=self.trconnect_w
        self.writerect()
        self.xr=self.xidt+wboxt/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0#-self.trconnect
        self.hr=-(self.trc_hbox+self.trconnect_w)
        self.wr=-self.trconnect_w
        self.writerect()
        self.xr=self.xidt-wboxt/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox
        self.hr=-self.trconnect_w
        self.wr=wboxt
        self.writerect()

        #extend center fingers
        self.xr=self.xidt-(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0-self.h/2.0-(self.offset+self.trconnect_y)/2.0
        self.hr=self.offset+self.trconnect_y
        self.wr=self.w
        self.writecenterrect()
        self.xr=self.xidt+(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0-self.h/2.0-(self.offset+self.trconnect_y)/2.0
        self.writecenterrect()

        #extend bottom fingers
        self.xr=self.xidt-(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y/2.0-self.trconnect_w
        self.hr=self.trconnect_y
        self.wr=self.w
        self.writecenterrect()
        self.xr=self.xidt+(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y/2.0-self.trconnect_w
        self.hr=self.trconnect_y
        self.wr=self.w
        self.writecenterrect()

        self.hr=self.h
        #write top squid touch
        self.xr=self.xidt
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect_y-0.5*self.trconnect_w
        self.hr=self.trconnect_w
        self.wr=self.trconnect_x
        self.writecenterrect()

################################
#        #write top squid touch
#        self.xr=self.xidt
##        self.yr=self.yidt-3.0*self.trconnect-self.h/2.0
#        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect_y-0.5*self.trconnect_w
#        self.hr=self.trconnect_w
#        self.wr=self.trconnect_x
#        self.writecenterrect()

        #write bottom squid touch
        self.xr=self.xidt
#        self.yr=self.yidt-3.0*self.trconnect-self.h/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y+0.5*self.trconnect_w-self.trconnect_w
        self.hr=self.trconnect_w
        self.wr=self.trconnect_x
        self.writecenterrect()
        self.add_qubit_idt_teeth()

    def add_qubit_idt_teeth(self):
        
        sqt_x=self.xidt-self.trconnect_x/2.0
        sqt_y=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y

        self.idt_numteeth=int(self.trconnect_x/(2*self.idt_tooth))
        idt_conn=self.idt_tooth*(2*self.idt_numteeth-1)
        sqt_x=self.xidt-idt_conn/2.0
        sqt_y=self.yidt-self.offset/2.0-self.h/2.0-self.trc_hbox+self.trconnect_y
        sqt_y_top=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect_y-self.trconnect_w

        
        #self.poly([(sqt_x, sqt_y),
        #           (sqt_x+idt_conn, sqt_y),
        #           (sqt_x+idt_conn, sqt_y-self.trconnect_w),
        #           (sqt_x,  sqt_y-self.trconnect_w)])
        for i in range(self.idt_numteeth):
            self.rect(sqt_x+2*i*self.idt_tooth, sqt_y, self.idt_tooth, self.idt_tooth )                   
            self.rect(sqt_x+2*i*self.idt_tooth, sqt_y_top, self.idt_tooth, -self.idt_tooth )                   

#            self.rect(self.idtR_x+2*i*self.idt_tooth, -self.h_idt/2.0, self.idt_tooth, self.idt_tooth ) 

#        self.xr=self.xidt
#        self.yr=self.yidt-self.h/2.0-self.offset/2.0-self.trc_hbox-self.trconnect_w/2.0
#        self.wr=self.trc_wbox
#        self.hr=self.trconnect_w
#        self.writecenterrect()
#
#        #self.xr=self.xidt
#        self.yr=self.yidt-self.offset/2.0-self.h/2.0#-self.trconnect_y #self.hbox
#        self.hr=-self.trconnect_w
#        #self.xr=self.xidt-self.ef*(self.w+self.gap)-(self.Np)*(self.w+self.gap)-self.w/2.0
#
#        #write left part of transmon connect
#        if mod(self.Np, 2)==0:
#            #if self.wbox==0.0:
#            self.wr=-(self.ef*(self.w+self.gap)+(self.Np-1)*(self.w+self.gap)-self.gap)
#            #else:
#            #    self.wr=-(self.wbox/2.0-self.gap-self.w/2.0-self.gap-self.w)
#            self.xr=self.xidt-self.w/2.0-2.0*self.gap-self.w
#        else:
#            #if self.wbox==0.0:
#            self.wr=-(self.ef*(self.w+self.gap)+self.Np*(self.w+self.gap)-self.gap)
#            #else:
#            #    self.wr=-(self.wbox/2.0-self.gap-self.w/2.0)
#            self.xr=self.xidt-self.w/2.0-self.gap
#        self.writerect()
#        self.wr=-(self.trc_wbox/2.0-self.w/2.0-self.gap)
#        self.writerect()
#        self.xr=self.xidt-self.trc_wbox/2.0
#        self.wr=-self.trconnect_w
#        self.hr=-self.trc_hbox-self.trconnect_w
#        self.writerect()
#
##        self.xr=self.xr+self.wr
##        self.hr=-(self.hbox-self.trconnect)
##        self.wr=self.trconnect
##        self.writerect()
#
#        #write right part of transmon
#        self.yr=self.yidt-self.offset/2.0-self.h/2.0#-self.trconnect_y #self.hbox
#        self.hr=-self.trconnect_w
#        if mod(self.Np, 2)==0:
#            #if self.wbox==0.0:
#            self.wr=self.ef*(self.w+self.gap)+(self.Np+1)*(self.w+self.gap)-self.gap
#            #else:
#            #    self.wr=self.wbox/2.0-self.gap-self.w/2.0+self.gap+self.w
#            self.xr=self.xidt+self.w/2.0-self.w
#        else:
#            #if self.wbox==0.0:
#            self.wr=self.ef*(self.w+self.gap)+self.Np*(self.w+self.gap)-self.gap
#            #else:
#            #    self.wr=self.wbox/2.0-self.gap-self.w/2.0
#            self.xr=self.xidt+self.w/2.0+self.gap
#        self.writerect()
#        self.wr=self.trc_wbox/2.0-self.w/2.0-self.gap #only for odd number
#        self.writerect()
#        self.xr=self.xidt+self.trc_wbox/2.0
#        self.wr=self.trconnect_w
#        self.hr=-self.trc_hbox-self.trconnect_w
#        self.writerect()

    def oldqubitdoubleIDT(self):
        """Add polygons representing qubit single fingered IDT to polylist (central fingers connect bottom to top)"""
        self.yt=self.yidt
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+2*a*(self.w+self.gap)
            self.yr=self.yt+self.offset/2.0
            self.xr=self.xt-(self.w+self.gap)/2.0
            self.writecenterrect()
            self.xr=self.xt+(self.w+self.gap)/2.0
            self.yr=self.yt+self.offset/2.0
            self.writecenterrect()
            if a in [-1,0]:
                self.xr=self.xt-(self.w+self.gap)/2.0
                self.yr=self.yt+self.offset/2.0-self.h/2.0-(self.offset+self.trconnect*2.0)/2.0
                self.hr=self.offset+2.0*self.trconnect
                self.writecenterrect()
                self.xr=self.xt+(self.w+self.gap)/2.0
                self.yr=self.yt+self.offset/2.0-self.h/2.0-(self.offset+self.trconnect*2.0)/2.0
                self.writecenterrect()
                self.hr=self.h
            self.xr=self.xt-2*(self.w+self.gap)-(self.w+self.gap)/2.0
            self.yr=self.yt-self.offset/2.0
            self.writecenterrect()
            self.xr=self.xt-2*(self.w+self.gap)+(self.w+self.gap)/2.0
            self.yr=self.yt-self.offset/2.0
            self.writecenterrect()
        self.xr=self.xt+2*(self.w+self.gap)-(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()
        self.xr=self.xt+2*(self.w+self.gap)+(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()

        #write extra fingers
        for a in range(0, self.ef):
            self.xr=self.xidt-a*(self.w+self.gap)-2*(self.Np+1)*(self.w+self.gap)+(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()
            self.xr=self.xidt+a*(self.w+self.gap)+2*(self.Np+1)*(self.w+self.gap)-(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()
        #write top box
        self.xr=self.xidt
        self.yr=self.yidt+self.offset/2.0+self.h/2.0+self.hbox/2.0
        self.hr=self.hbox
        if self.wbox==0.0:
            self.wr=self.Np*(2*self.w+2*self.gap) +self.w+self.ef*(self.w+self.gap)*2
        else:
            self.wr=self.wbox
        self.writecenterrect()

        #write bottom box
        self.xr=self.xidt
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect/2.0-self.hbox
        self.hr=self.trconnect
        self.writecenterrect()

        #write top squid touch
        self.xr=self.xidt
#        self.yr=self.yidt-3.0*self.trconnect-self.h/2.0
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-2.5*self.trconnect
        self.hr=self.trconnect
        self.wr=self.wr-4*self.trconnect
        self.writecenterrect()

        #self.xr=self.xidt
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect #self.hbox
        self.hr=self.trconnect
        #self.xr=self.xidt-self.ef*(self.w+self.gap)-(self.Np)*(self.w+self.gap)-self.w/2.0

        #write left part of transmon connect
        if mod(self.Np, 2)==0:
            if self.wbox==0.0:
                self.wr=-(self.ef*(self.w+self.gap)+2*(self.Np-1)*(self.w+self.gap)-self.gap)#+self.w+self.gap
            else:
                self.wr=-(self.wbox/2.0-self.gap-self.w/2.0-self.gap-self.w)
            self.xr=self.xidt-self.w/2.0-2.0*self.gap-self.w
        else:
            if self.wbox==0.0:
                self.wr=-(self.ef*(self.w+self.gap)+2*self.Np*(self.w+self.gap)-self.gap)
            else:
                self.wr=-(self.wbox/2.0-self.gap-self.w/2.0)
            self.xr=self.xidt-self.w/2.0-self.gap
        self.writerect()
        self.xr=self.xr+self.wr
        self.hr=-(self.hbox-self.trconnect)
        self.wr=self.trconnect
        self.writerect()
        #write right part of transmon
        self.yr=self.yidt-self.offset/2.0-self.h/2.0-self.trconnect #self.hbox
        self.hr=self.trconnect
        if mod(self.Np, 2)==0:
            if self.wbox==0.0:
                self.wr=self.ef*(self.w+self.gap)+(self.Np+1)*(self.w+self.gap)-self.gap
            else:
                self.wr=self.wbox/2.0-self.gap-self.w/2.0+self.gap+self.w
            self.xr=self.xidt+self.w/2.0-self.w
        else:
            if self.wbox==0.0:
                self.wr=self.ef*(self.w+self.gap)+self.Np*(self.w+self.gap)-self.gap
            else:
                self.wr=self.wbox/2.0-self.gap-self.w/2.0
            self.xr=self.xidt+self.w/2.0+self.gap
        self.writerect()
        self.xr=self.xr+self.wr
        self.hr=-(self.hbox-self.trconnect)
        self.wr=-self.trconnect
        self.writerect()

    def qubitsingleIDTpair(self):
        """Add polygons representing single finger IDT pair to polylist (called by singleIDT function)"""
        self.xr=self.xt-(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)/2.0
        self.yr=self.yt#+self.offset/2.0
        self.hr=self.h+self.offset
        self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)/2.0
        self.yr=self.yt-self.hr#+self.offset/2.0
        #self.hr=self.h+self.offset
        self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)/2.0
        self.yr=self.yt-self.hr-self.hbox
        self.hr=self.hbox
        self.wr=(self.ef*(self.w+self.gap)+(self.Np-1)*(self.w+self.gap)+self.w+self.gap/2.0)
        self.writecenterrect()
        self.hr=self.h
        self.wr=self.w

    def oldsingleIDT(self):
        """Add polygons representing single fingered IDT to polylist"""
        self.yt=self.yidt

        #write IDT
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+a*(self.w+self.gap)
            self.singleIDTpair()

        #write extra fingers
        for a in range(0, self.ef):
            self.xr=self.xidt-(a+1)*(self.w+self.gap)-(self.Np-1)*(self.w+self.gap)-(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()
            self.xr=self.xidt+(a+1)*(self.w+self.gap)+(self.Np-1)*(self.w+self.gap)+(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()

        #write connecting box at top and bottom
        if self.wbox==0.0:
            self.xr=self.xidt-self.ef*(self.w+self.gap)-(self.Np-1)*(self.w+self.gap)-(self.w+self.gap/2.0)
            self.wr=2.0*(self.ef*(self.w+self.gap)+(self.Np-1)*(self.w+self.gap)+self.w+self.gap/2.0)
        else:
            self.xr=self.xidt-self.wbox/2.0
            self.wr=self.wbox
        self.yr=self.yidt+(self.h+self.offset)/2.0
        self.hr=self.hbox
        self.writerect()
        self.yr=self.yidt-(self.h+self.offset)/2.0
        self.hr=-self.hbox
        self.writerect()


    def singleIDTpair(self):
        """Add polygons representing single finger IDT pair to polylist (called by singleIDT function)"""
        self.xr=self.xt-(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0
        self.writecenterrect()

    def doubleIDT(self):
        """Add polygons representing double finger IDT to polylist"""
        self.yt=self.yidt

        #write IDT
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+2.0*a*(self.w+self.gap)
            self.doubleplusrect()
            self.xt=self.xt-2*(self.w+self.gap)
            self.doubleminusrect()
        self.xt=self.xidt+2.0*self.Np*(self.w+self.gap)
        self.doubleminusrect()

        #Write extra fingers
        for a in range(0, self.ef):
            self.xt=self.xidt-2*a*(self.w+self.gap)-2.0*(self.Np)*(self.w+self.gap)-2.0*(self.gap+self.w)
            self.doubleminusrect()
            self.xt=self.xidt+2*a*(self.w+self.gap)+2.0*(self.Np)*(self.w+self.gap)+2.0*(self.gap+self.w)
            self.doubleminusrect()

        #write connecting box at top and bottom
        if self.wbox==0.0:
            #self.xr=self.xidt#-self.ef*(self.w+self.gap)-2.0*(self.Np-1)*(self.w+self.gap)-2.0*self.w-3.0*self.gap/2.0
            self.wr=4.0*self.ef*(self.w+self.gap)+4.0*self.Np*(self.w+self.gap)+2.0*self.w+self.gap
        else:
            self.xr=self.xidt-self.wbox/2.0
            self.wr=self.wbox
        self.xr=self.xidt
        self.yr=self.yidt+(self.h+self.offset+self.hbox)/2.0
        self.hr=self.hbox
        self.writecenterrect()
        self.xr=self.xidt
        self.yr=self.yidt-(self.h+self.offset+self.hbox)/2.0
        self.hr=-self.hbox
        self.writecenterrect()

    def plusrect(self):
        self.yr=self.yt+self.offset/2.0
        self.writecenterrect()

    def minusrect(self):
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()

    def doubleplusrect(self):
        self.xr=self.xt-(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0
        self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0
        self.writecenterrect()

    def doubleminusrect(self):
        self.xr=self.xt-(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()

    def olddoubleIDT(self):
        """Add polygons representing double finger IDT to polylist"""
        self.yt=self.yidt

        #write IDT
        for a in range(-(self.Np-1), self.Np, 2):
            self.xt=self.xidt+2.0*a*(self.w+self.gap)
            self.doubleIDTpair()

        #Write extra fingers
        for a in range(0, self.ef):
            self.xr=self.xidt-(a+1)*(self.w+self.gap)-2.0*(self.Np-1)*(self.w+self.gap)-3.0*(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()
            self.xr=self.xidt+(a+1)*(self.w+self.gap)+2.0*(self.Np-1)*(self.w+self.gap)+3.0*(self.gap+self.w)/2.0
            self.yr=self.yidt-self.offset/2.0
            self.writecenterrect()

        #write connecting box at top and bottom
        if self.wbox==0.0:
            self.xr=self.xidt-self.ef*(self.w+self.gap)-2.0*(self.Np-1)*(self.w+self.gap)-2.0*self.w-3.0*self.gap/2.0
            self.wr=2.0*self.ef*(self.w+self.gap)+4.0*(self.Np-1)*(self.w+self.gap)+4.0*self.w+3.0*self.gap
        else:
            self.xr=self.xidt-self.wbox/2.0
            self.wr=self.wbox
        self.yr=self.yidt+(self.h+self.offset)/2.0
        self.hr=self.hbox
        self.writerect()
        self.yr=self.yidt-(self.h+self.offset)/2.0
        self.hr=-self.hbox
        self.writerect()

    def doubleIDTpair(self):
        """Adds polygons represtning double finger IDT pair to polylist (called by doubleIDT function)"""
        self.xr=self.xt-3.0*(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()
        self.xr=self.xt-(self.w+self.gap)/2.0
        self.yr=self.yt-self.offset/2.0
        self.writecenterrect()
        self.xr=self.xt+(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0
        self.writecenterrect()
        self.xr=self.xt+3.0*(self.w+self.gap)/2.0
        self.yr=self.yt+self.offset/2.0
        self.writecenterrect()

    def writecenterrect(self):
        """Adds a centered rectangle to the polylist"""
        self.xr=self.xr-self.wr/2.0
        self.yr=self.yr-self.hr/2.0
        self.writerect()

