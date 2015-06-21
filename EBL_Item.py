# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 22:26:23 2015

@author: thomasaref
"""
from LOG_functions import log_warning#, log_debug
#log_debug(1)
from Atom_Base import Base#, NoShowBase
from EBL_Boss import ebl_boss
from atom.api import Atom, Enum, Float, ContainerList, Int, observe, Property#, Str#, Typed, List, Unicode, Int, Atom, Range, Bool, observe
from enaml import imports
from enaml.qt.qt_application import QtApplication

class EBL_Base(Base):
    def _default_boss(self):
        ebl_boss.make_boss()
        return ebl_boss

class NoShow_EBL_Base(EBL_Base):
    def _default_show_base(self):
        return False

class EBL_PolyBase(Atom):
    color=Enum("green").tag(desc="color or datatype of item, could be used for dosing possibly")
    layer=Enum("Al").tag(desc='layer of item')

    x_center=Float(0.0).tag(desc="x coordinate of center of pattern. this should almost always be 0.0, which is centered (default).", unit="um")
    y_center=Float(0.0).tag(desc="y coordinate of center of pattern. this should almost always be 0.0, which is centered (default).", unit="um")

class NoShow_EBL_PolyBase(EBL_PolyBase):
    def _default_show_base(self):
        return False

class EBLvert(Atom):
    #def _default_base_name(self):
    #    return "EBLvert"

    x=Float()#.tag(log=False)
    y=Float()#.tag(log=False)

def getxy(vert):
    return (vert.x, vert.y)

class EBLPolygon(EBL_PolyBase):
    """Implements polygons for use in drawing EBL patterns and includes conversion of polygon to DXF or GDS format (text based)"""
    verts=ContainerList().tag(inside_type=EBLvert, desc='list of vertices of polygon', log=False)

    #def _default_base_name(self):
    #    return "EBLPolygon"

    def get_verts(self):
        return map(getxy, self.verts)

    def poly2dxf(self):
        """converts polygon to dxf format and returns list of commands (text based)"""
        tlist=['0\r\nLWPOLYLINE\r\n',  #place line
               '8\r\n{0}\r\n'.format(self.layer), #add to layer
               '62\r\n{0}\r\n'.format(self.cn),
               '90\r\n{0}\r\n'.format(len(self.verts)), #number of vertices=4
               '70\r\n1\r\n'] #is closed
        for v in self.verts:
            tlist.append('10\r\n{0}\r\n20\r\n{1}\r\n'.format(v.x,v.y)) #vertex coordinate X and Y
        return tlist

def V(vtuple):
    """creates vertice from tuple"""
    return EBLvert(x=vtuple[0], y=vtuple[1])

def P(verts, **kwargs):
    """creates EBLPolygon from tuple of vertices and keyword arguments"""
    return EBLPolygon(verts=map(V,verts), **kwargs)

def R(xr=0.0, yr=0.0, wr=1.0, hr=1.0, **kwargs):
    """creates rectangle EBLpolygon with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
    return P(verts=[(xr,yr), (xr+wr,yr), (xr+wr, yr+hr), (xr, yr+hr)], **kwargs)

class PolyList(EBL_PolyBase):
    polylist=ContainerList(EBLPolygon).tag(inside_type=EBLPolygon)
    #view=Enum("EBL").tag(private=True)

    #def plot(self):
    #    for n,p in enumerate(self.polylist):
    #        self.boss.plot.add_poly_plot(n=n, verts=p.get_verts(), cn=p.color, polyname=self.name)
    #    self.boss.plot.plot.request_redraw()

    def P(self, verts):
        """adds a polygon to the polylist with vertices given as a list of tuples"""
        self.polylist.append(P(verts, layer=self.layer, color=self.color))

    def R(self, xr, yr, wr, hr):
        """Adds a rectangle with bottom left corner coordinates to polylist"""
        self.polylist.append(R(xr, yr, wr, hr, layer=self.layer, color=self.color))

    def C(self, xr, yr, wr, hr):
        """Adds a centered rectangle to the polylist"""
        self.R(xr-wr/2.0, yr-hr/2.0, wr, hr)

    def show(self, inside_type=EBLPolygon):
        """stand alone for showing polylist"""
        with imports():
            from EBL_enaml import EBLMain
        app = QtApplication()
        view = EBLMain(polylist=self.polylist, inside_type=inside_type)
        view.show()
        app.start()

from scipy.constants import epsilon_0 as eps0
from numpy import sqrt

class IDT(EBL_Base):
    df=Enum("single", "double").tag(desc="'double' for double fingered, 'single' for single fingered. defaults to double fingered")
    Np=Int(36).tag(desc="number of finger pairs. this should be at least 1 and defaults to 36.")
    ef=Int(0).tag(desc="number of extra fingers to compensate for edge effect. Defaults to 0")
    a=Float(0.096).tag(unit="um", desc="width of fingers (um). same as gap generally. Adjusting relative to gap is equivalent to adjusting the bias in Beamer")
    gap=Float(0.096).tag(unit="um", desc="gap between fingers (um). about 0.096 for double fingers at 4.5 GHz")
    offset=Float(0.5).tag(unit="um", desc="gap between electrode and end of finger. The vertical offset of the fingers. Setting this to zero produces a shorted reflector")
    W=Float(25.5).tag(unit="um", desc="height of finger")
    hbox=Float(20.0).tag(desc="height of electrode box")
    wbox=Float(30.0).tag(desc="width of electrode box. Setting to 0.0 (default) makes it autoscaling so it matches the width of the IDT")

    epsinf=Float()
    Dvv=Float()
    v=Float()
    material = Enum('LiNbYZ', 'GaAs', 'LiNb128', 'LiNbYZX', 'STquartz')

    def _observe_material(self, change):
        if self.material=="STquartz":
            self.epsinf=5.6*eps0
            self.Dvv=0.06e-2
            self.v=3159.0
        elif self.material=='GaAs':
            self.epsinf=1.2e-10
            self.Dvv=0.035e-2
            self.v=2900.0
        elif self.material=='LiNbYZ':
            self.epsinf=46*eps0
            self.Dvv=2.4e-2
            self.v=3488.0
        elif self.material=='LiNb128':
            self.epsinf=56*eps0
            self.Dvv=2.7e-2
            self.v=3979.0
        elif self.material=='LiNbYZX':
            self.epsinf=46*eps0
            self.Dvv=0.8e-2
            self.v=3770.0
        else:
            log_warning("Material not listed")

    f0=Float().tag(label="f0",
                unit="GHz",
                desc="Center frequency",
                reference="")

    @observe('w', 'v', 'gap', 'df')
    def _get_f0(self, change):
        v,a, g=self.v, self.a*1e-6, self.gap*1e-6
        p=g+a
        if self.df:
            lbda0=4*p
        else:
            lbda0=2*p
        self.f0=v/lbda0/1.0e9


    Ct=Property().tag(label="Ct",
                   unit="F",
                   desc="Total capacitance of IDT",
                   reference="Morgan page 16/145")
    #@observe('epsinf', 'h', 'Np', 'df')
    def _get_Ct(self):
        W, epsinf, Np=self.h*1e-6, self.epsinf, self.Np
        if self.df=="double":
            return sqrt(2.0)*W*epsinf*Np
        return W*epsinf*Np

    def _default_material(self):
        return 'LiNbYZ' #'GaAs'

class EBLIDT(IDT):
    """handles everything related to drawing a IDT. Units are microns (um)"""
    trconnect_x=Float(9.0).tag(desc="connection length of transmon")
    trconnect_y=Float(2.5).tag(desc="connection length of transmon")
    trconnect_w=Float(0.5).tag(desc="connection length of transmon")
    trc_wbox=Float(14.0)
    trc_hbox=Float(12.5)

    idt_tooth=Float(0.3).tag(desc="tooth size on CPW connection to aid contact")
    idt_numteeth=Int(5) #52 um, 12.5 um

a=EBL_Item(name="EBL_item_test")
#a.polylist=[R(), R(5)]#, P([(0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1)])]
a.P([(0,0), (0,25), (0.1,25), (0.1, 0), (5, -5), (10, -5), (10, -10), (5, -10), (5, -5.1)])
a.P([(-0.3, -5), (-0.30,25), (-0.2,25), (-0.2, -5), (5, -10), (10, -10), (10, -15), (5, -15), (5, -10.1)])
b=IDT()
a.show()
