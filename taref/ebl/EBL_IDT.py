# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:43:01 2015

@author: thomasaref
"""

from taref.saw.idt import IDT
from atom.api import Float, Bool, Enum, Int
from taref.ebl.polygons import EBL_Polygons
from numpy import  mod
from taref.core.backbone import private_property

class EBL_IDT(EBL_Polygons, IDT):
    """handles everything related to drawing a IDT. Units are microns (um)"""
    trconnect_x=Float(9.0e-6).tag(desc="connection length of transmon", unit="um")
    trconnect_y=Float(2.0e-6).tag(desc="connection length of transmon", unit="um")
    trconnect_w=Float(0.5e-6).tag(desc="connection length of transmon", unit="um")
    trc_wbox=Float(14.0e-6).tag(desc="width of transmon box", unit="um")
    trc_hbox=Float(12.5e-6).tag(desc="height of transmon box", unit="um")
    o=Float(0.5e-6).tag(unit="um",
                    desc="gap between electrode and end of finger. The vertical offset of the fingers. Setting this to zero produces a shorted reflector")
    hbox=Float(0.5e-6).tag(desc="height of electrode box", unit="um")
    wbox=Float(0.0e-6).tag(unit="um", desc="width of electrode box. Setting to 0.0 (default) makes it autoscaling so it matches the width of the IDT")

    idt_tooth=Float(0.3e-6).tag(unit="um", desc="tooth size on CPW connection to aid contact")

    idt_type=Enum("basic", "stepped").tag(desc="basic is a regular IDT, stepped uses stepped fingers for harmonic suppression")
    qdt_type=Enum("IDT", "QDT")

    conn_h=Float(150.0e-6).tag(unit="um")
    add_gate=Bool(True)
    add_gnd=Bool(True)
    add_teeth=Bool(True)
    step_num=Int(3)
    gate_distance=Float(10.0e-6).tag(desc="distance to gate", unit="um")

    def _default_color(self):
        return "blue"

    def _default_main_params(self):
        return self.all_main_params
        mp=["idt_type", "qdt_type", "ft",
            "add_gate", "add_gnd", "add_teeth", "angle_x", "angle_y", "step_num",
            "Np", "a", "g", "W", "o","f0", "eta", "ef", "wbox", "hbox", "material",
            "trconnect_x", "trconnect_y", "trconnect_w", "trc_wbox", "trc_hbox",
            "conn_h",  "idt_tooth", "v", "Dvv", "epsinf", "Ct", "p", "x_ref", "y_ref"]
        return mp

    def make_name_sug(self):
        name_sug=""
        name_sug+=dict(basic="", stepped="stp")[self.idt_type]
        name_sug+=self.qdt_type
        name_sug+=dict(single="s", double="d")[self.ft]
        if self.idt_type=="stepped":
            name_sug+="{0}s{1}a{2}e{3}".format(self.Np, self.step_num, int(self.a*1e9), int(self.eta*100))
        else:
            name_sug+="{0}e{1}a{2}h{3}".format(self.Np, self.ef, int(self.a*1e9), int(self.hbox))
        self.name_sug=name_sug
        shot_mod=""
        shot_mod+=dict(basic="", stepped="T")[self.idt_type]
        shot_mod+=dict(IDT="I", QDT="Q")[self.qdt_type]
        shot_mod+=dict(single="S", double="D")[self.ft]
        shot_mod+="{0}".format(len(self.chief.patterns)) #int(self.a*1e9)) #self.Np, self.ef,
        self.shot_mod_table=shot_mod

    @property
    def m(self):
        return {"basic": 0, "stepped": 1}[self.idt_type]

    @property
    def xo(self):
        return self.a*(1.0-1.0/self.step_num)*self.m

    @private_property
    def polylist(self):
        """draws single or double fingered IDT.
        If it is for a qubit, it adjusts the bottom box to contain SQUID connections
        (central fingers connect bottom to top)"""
        self.verts=[]
        self._IDTfingers()
        self._IDTextrafingers()
        self._IDTtopbottombox()
        if self.qdt_type=="QDT":
            self._squid_touch()
            self._left_transmon_connect()
            self._right_transmon_connect()
            if self.add_teeth:
                self._add_qubit_idt_teeth()
            if self.add_gate:
                self._qubitgate()
            if self.add_gnd:
                self._qubitgnd()
        return self.verts

    def _subfingrect(self, xt, yt, wt, ht, m):
        """writes part of finger for stepped IDTs"""
        if self.ft=="double":
            self.C(xt-(self.a+self.g)/2.0, yt, wt, ht)
            self.C(xt+(self.a+self.g)/2.0, yt, wt, ht)
        else:
            self.C(xt, yt, wt, ht)
        if m>1:
            self._subfingrect(xt+self.a/self.step_num, yt+ht, wt, ht, m-1)
        return

    def _fingrect(self, xt, yt, wt, ht, m=0):
        """writes IDT finger width a and length W and two for a double finger"""
        if m!=0:
            if m<0:
                self._fingrect(xt, yt-self.W/2.0, wt, self.o)
            else:
                self._fingrect(xt+self.a*(1.0-1.0/self.step_num), yt+self.W/2.0, wt, self.o)
            self._subfingrect(xt, -self.W/2.0*(1.0-1.0/self.step_num), wt, self.W/self.step_num, self.step_num)
        else:
            if self.ft=="double":
                self.C(xt-(self.a+self.g)/2.0, yt, wt, ht)
                self.C(xt+(self.a+self.g)/2.0, yt, wt, ht)
            else:
                self.C(xt, yt, wt, ht)

    def _IDTfingers(self):
        """writes IDT fingers for single finger IDT with extensions for connections if it is qubit type IDT"""
        for n in range(-(self.Np-1), self.Np, 2):
            self._fingrect(self.mult*n*(self.a+self.g), self.o/2.0, self.a, self.W+self.o, self.m)
            self._fingrect(self.mult*(n-1)*(self.a+self.g), -self.o/2.0, self.a, self.W+self.o, -self.m)
            if n in [-1,0] and self.qdt_type=="QDT":
                self._fingrect(self.mult*n*(self.a+self.g), -self.W/2.0-(self.o+self.trconnect_y+self.trconnect_w)/2.0, self.a, -(self.o+self.trconnect_y+self.trconnect_w))
                self._fingrect(self.mult*n*(self.a+self.g), -self.W/2.0-self.o-self.trc_hbox+self.trconnect_y/2.0, self.a, self.trconnect_y)
        self._fingrect(self.mult*self.Np*(self.a+self.g), -self.o/2.0, self.a, self.W+self.o, -self.m)

    def _IDTextrafingers(self):
        """write extra fingers for a single IDT"""
        for n in range(0, self.ef):
            self._fingrect(-self.mult*n*(self.a+self.g)-self.mult*(self.Np+1)*(self.a+self.g), -self.o/2.0, self.a, self.W, -self.m)
            self._fingrect(self.mult*n*(self.a+self.g)+self.mult*(self.Np+1)*(self.a+self.g), -self.o/2.0, self.a, self.W, -self.m)

    def _IDTtopbottombox(self):
        """writes connecting box at top and also bottom for regular IDT"""
        if self.wbox==0.0:
            wr=self.mult*2*self.Np*(self.a+self.g) +self.mult*self.a+self.mult*2*self.ef*(self.a+self.g)+(self.mult-1)*self.g
        else:
            wr=self.wbox
        self.C(self.xo, self.o+self.W/2.0+self.hbox/2.0, wr, self.hbox)
        if self.qdt_type=="QDT":
            self.R(-self.trc_wbox/2.0, -self.o-self.W/2.0-self.trc_hbox-self.trconnect_w, self.trc_wbox, self.trconnect_w)
        else:
            self.C(0, -self.o-self.W/2.0-self.hbox/2.0, wr, self.hbox)

    def _qubitgnd(self):
        """writes qubit ground"""
        self.P([(-self.trc_wbox/2.0, -self.o-self.W/2.0-self.trc_hbox-self.trconnect_w),
                (self.trc_wbox/2.0, -self.o-self.W/2.0-self.trc_hbox-self.trconnect_w),
                (self.trc_wbox/2.0, -self.conn_h),
                (-self.trc_wbox/2.0, -self.conn_h)])

    def _qubitgate(self):
        """writes gate for a qubit IDT"""
        self.P([(-self.trc_wbox/2.0, self.o+self.W/2.0+self.hbox+self.gate_distance),#-0.25e-6),
                (self.trc_wbox/2.0, self.o+self.W/2.0+self.hbox+self.gate_distance), #-0.25e-6),
                (self.trc_wbox/2.0, self.conn_h),
                   (-self.trc_wbox/2.0, self.conn_h)])

    def _squid_touch(self):
        """writes squid connections"""
        self.R(-self.trconnect_x/2.0, -self.o-self.W/2.0-self.trconnect_y-self.trconnect_w, self.trconnect_x, -self.trconnect_w)
        self.R(-self.trconnect_x/2.0, -self.o-self.W/2.0-self.trc_hbox+self.trconnect_y, self.trconnect_x, self.trconnect_w)

    def _left_transmon_connect(self):
        """write left part of transmon connect"""
        if mod(self.Np, 2)==0: #needs fixing for evens
            wr=-(self.mult*self.ef*(self.a+self.g)+self.mult*(self.Np-1)*(self.a+self.g)-self.g)
            xr=-self.mult*self.a/2.0-2.0*self.g-self.a
        else:
            wr=-(self.mult*self.ef*(self.a+self.g)+self.mult*self.Np*(self.a+self.g)-self.g)
            xr=-self.mult*self.a/2.0-self.g-(self.mult-1)*self.g/2.0
        self.R(xr, -self.o-self.W/2.0, wr, -self.trconnect_w)
        self.R(xr, -self.o-self.W/2.0, -(self.trc_wbox/2.0-self.a/2.0-self.g), -self.trconnect_w)
        self.R(-self.trc_wbox/2.0, -self.o-self.W/2.0, -self.trconnect_w, -self.trc_hbox-self.trconnect_w)

    def _right_transmon_connect(self):
        """write right part of transmon connect"""
        if mod(self.Np, 2)==0:
            wr=self.ef*(self.a+self.g)+(self.Np+1)*(self.a+self.g)-self.g
            xr=-self.a/2.0
        else:
            wr=self.mult*self.ef*(self.a+self.g)+self.mult*self.Np*(self.a+self.g)-self.g
            xr=self.mult*self.a/2.0+self.g+(self.mult-1)*self.g/2.0
        self.R(xr, -self.o-self.W/2.0, wr, -self.trconnect_w)
        self.R(xr, -self.o-self.W/2.0, self.trc_wbox/2.0-self.a/2.0-self.g, -self.trconnect_w)
        self.R(self.trc_wbox/2.0, -self.o-self.W/2.0, self.trconnect_w, -self.trc_hbox-self.trconnect_w)

    def _add_qubit_idt_teeth(self):
        """adds teeth to qubit squid connection"""
        idt_numteeth=int(self.trconnect_x/(2*self.idt_tooth))
        idt_conn=self.idt_tooth*(2*idt_numteeth-1)
        sqt_x=-idt_conn/2.0
        sqt_y=-self.o-self.W/2.0-self.trc_hbox+self.trconnect_y+self.trconnect_w
        sqt_y_top=-self.o-self.W/2.0-self.trconnect_y-2*self.trconnect_w

        for i in range(idt_numteeth):
            self.R(sqt_x+2*i*self.idt_tooth, sqt_y, self.idt_tooth, self.idt_tooth )
            self.R(sqt_x+2*i*self.idt_tooth, sqt_y_top, self.idt_tooth, -self.idt_tooth )


if __name__=="__main__":
    a=EBL_IDT(name="EBL_Item_test")

    #a.ft="single"
    a.qdt_type="QDT"
    a.add_gate=False
    a.add_gnd=False
    a.add_teeth=False
    a.idt_type="stepped"
    a.Np=3
    #a.makeIDT()
    #print a.polys.get_verts()
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

    def makequbitwingfing(self):
        """Draws IDT depending on object parameters"""
        self.polylist=[] #list of polygons that make up IDT pattern
        self.wr=self.w #set width of idt finger rectangle to w
        self.hr=self.h #set height of idt finger rectangle to h
        if self.df==1: #double fingered
            self.qubitdoublewingfing()
        else:
            self.qubitsinglewingfing()

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

