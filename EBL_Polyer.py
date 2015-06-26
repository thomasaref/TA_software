# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:52:31 2015

@author: thomasaref
"""
from atom.api import Atom, Enum, Float, ContainerList
from enaml import imports
from enaml.qt.qt_application import QtApplication
from numpy import sin, cos

class EBL_PolyBase(Atom):
    color=Enum("green").tag(desc="color or datatype of item, could be used for dosing possibly")
    layer=Enum("Al").tag(desc='layer of item')

    #x_center=Float(0.0).tag(desc="x coordinate of center of pattern. this should almost always be 0.0, which is centered (default).", unit="um")
    #y_center=Float(0.0).tag(desc="y coordinate of center of pattern. this should almost always be 0.0, which is centered (default).", unit="um")

class EBLvert(Atom):
    x=Float()
    y=Float()

    def addxy(self, x=0.0, y=0.0):
        self.x+=x
        self.y+=y
        return self
        
    def rotate(self, cos_theta, sin_theta):
            xp=self.x*cos_theta-self.y*sin_theta
            yp=self.x*sin_theta+self.y*cos_theta
            self.x=xp
            self.y=yp 

class EBLPolygon(EBL_PolyBase):
    """Implements polygons for use in drawing EBL patterns and includes conversion of polygon to DXF or GDS format (text based)"""
    verts=ContainerList().tag(inside_type=EBLvert, desc='list of vertices of polygon', log=False)

    def _default_verts(self):
        return [EBLvert()]

    def rotate(self, cos_theta, sin_theta):
        for v in self.verts:
            v.rotate(cos_theta, sin_theta)
        
    def get_verts(self):
        return [(v.x,v.y) for v in self.verts]

    def offset_verts(self, x=0.0, y=0.0):
        for v in self.verts:
            v.addxy(x,y)
        #self.x_center+=x
        #self.y_center+=y
        
    def poly2dxf(self):
        """converts polygon to dxf format and returns list of commands (text based)"""
        tlist=['0\r\nLWPOLYLINE\r\n',  #place line
               '8\r\n{0}\r\n'.format(self.layer), #add to layer
               '62\r\n{0}\r\n'.format(self.color),
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
    return EBLPolygon(verts=[V(v) for v in verts], **kwargs)

def R(xr=0.0, yr=0.0, wr=1.0, hr=1.0, **kwargs):
    """creates rectangle EBLpolygon with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
    return P(verts=[(xr,yr), (xr+wr,yr), (xr+wr, yr+hr), (xr, yr+hr)], **kwargs)

class Polyer(EBL_PolyBase):
    polylist=ContainerList(EBLPolygon).tag(inside_type=EBLPolygon)

    def _default_polylist(self):
        return [EBLPolygon()]

    def offset_polygons(self, x=0.0, y=0.0):
        for p in self.polylist:
            p.offset_verts(x,y)
        #self.x_center+=x
        #self.y_center+=y

    def rotate(self, theta):
        for p in self.polylist:
            p.rotate(cos_theta=cos(theta), sin_theta=sin(theta))

    def CP(self,index=-1, x=0.0, y=0.0, **kwargs):
        """copies a polygon to an offset position and adds it"""
        poly=P(self.polylist[index].get_verts(), **kwargs)        
        poly.offset_verts(x,y)
        self.polylist.append(poly)
        
    def P(self, verts, **kwargs):
        """adds a polygon to the polylist with vertices given as a list of tuples"""
        self.polylist.append(P(verts, **kwargs))

    def R(self, xr, yr, wr, hr, **kwargs):
        """Adds a rectangle with bottom left corner coordinates to polylist"""
        self.polylist.append(R(xr, yr, wr, hr, **kwargs))

    def C(self, xr, yr, wr, hr, **kwargs):
        """Adds a centered rectangle to the polylist"""
        self.R(xr-wr/2.0, yr-hr/2.0, wr, hr, **kwargs)

    def show(self, inside_type=EBLPolygon, inner_type=EBLvert):
        """stand alone for showing polylist"""
        with imports():
            from EBL_enaml import EBMain
        app = QtApplication()
        view = EBMain(polyer=self, inside_type=inside_type, inner_type=inner_type)
        view.show()
        app.start()

if __name__=="__main__":
    a=Polyer()
    a.polylist=[R(), R(5), P([(0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1), (0,1)])]
    a.P([(0,0), (0,25), (0.1,25), (0.1, 0), (5, -5), (10, -5), (10, -10), (5, -10), (5, -5.1)])
    a.P([(-0.3, -5), (-0.30,25), (-0.2,25), (-0.2, -5), (5, -10), (10, -10), (10, -15), (5, -15), (5, -10.1)])
    print a.polylist[-1].get_verts()    
    a.CP(x=2.0, y=3.0)
    print a.polylist[-1].get_verts()    
    print a.polylist[-2].get_verts()    

    a.polylist[1].offset_verts(3,4)
    print a.polylist[1].get_verts()    

    #a.show()