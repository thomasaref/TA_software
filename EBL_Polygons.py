# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:52:31 2015

@author: thomasaref
"""
from atom.api import Atom, Enum, Float, List
from numpy import sin, cos, pi
#from LOG_functions import log_debug



def offset(verts, x, y, uf=1.0):
    x=x/uf
    y=y/uf
    return [tuple([(v[0]+x, v[1]+y) for v in p]) for p in verts]

def rotate(verts, theta):
    theta=theta/180.0*pi
    cos_theta=cos(theta)
    sin_theta=sin(theta)
    return [tuple([(v[0]*cos_theta-v[1]*sin_theta, v[0]*sin_theta+v[1]*cos_theta) for v in p]) for p in verts]

def horiz_refl(verts):
    return [tuple([(-v[0], v[1]) for v in p]) for p in verts]

def vert_refl(verts):
    return [tuple([(v[0], -v[1]) for v in p]) for p in verts]

def horizvert_refl(verts):
    return [tuple([(-v[0], -v[1]) for v in p]) for p in verts]

def minx(verts):
    if verts==[]:
        return -1.0
    return min([min([v[0] for v in p]) for p in verts])

def miny(verts):
    if verts==[]:
        return -1.0
    return min([min([v[1] for v in p]) for p in verts])

def maxx(verts):
    if verts==[]:
        return 1.0
    return max([max([v[0] for v in p]) for p in verts])

def maxy(verts):
    if verts==[]:
        return 1.0
    return max([max([v[1] for v in p]) for p in verts])

def poly2dxf(p, color, layer):
    """converts polygon to dxf format and returns list of commands (text based)"""
    tlist=['0\r\nLWPOLYLINE\r\n',  #place line
               '8\r\n{0}\r\n'.format(layer), #add to layer
               '62\r\n{0}\r\n'.format(color),
               '90\r\n{0}\r\n'.format(len(p)), #number of vertices=4
               '70\r\n1\r\n'] #is closed
    for v in p:
            tlist.append('10\r\n{0}\r\n20\r\n{1}\r\n'.format(v[0],v[1])) #vertex coordinate X and Y
    return tlist

def polylist2dxf(verts, color, layer):
    return [poly2dxf(p, color, layer) for p in verts] #flatten?

class EBL_Polygons(Atom):
    color=Enum("green").tag(desc="color or datatype of item, could be used for dosing possibly")
    layer=Enum("Al").tag(desc='layer of item')
    unit_factor=Float(1.0e-6)
    verts=List().tag(private=True)
    children=List().tag(private=True)
    x_ref=Float(0.0).tag(desc="x coordinate of reference point of pattern.", unit="um")
    y_ref=Float(0.0).tag(desc="y coordinate of reference point of pattern", unit="um")
    theta=Float(0.0).tag(desc="angle to rotate in degrees")
    orient=Enum("TL", "TR", "BL", "BR")

    @property
    def xmin(self):
        if self.verts==[]:
            self.pros(self)
        return minx(self.verts)

    @property
    def xmax(self):
        if self.verts==[]:
            self.pros(self)
        return maxx(self.verts)

    @property
    def ymin(self):
        if self.verts==[]:
            self.pros(self)
        return miny(self.verts)

    @property
    def ymax(self):
        if self.verts==[]:
            self.pros(self)
        return maxy(self.verts)

    def extend(self, verts):
        if self.orient=="TL":
            self.verts.extend(verts)
        elif self.orient=="BL":
            self.verts.extend(vert_refl(verts))
        elif self.orient=="TR":
            self.verts.extend(horiz_refl(verts))
        else:
            self.verts.extend(horizvert_refl(verts))


    def pros(self, EP):
        EP.make_polylist()
        EP.rotate(EP.theta)
        EP.offset(EP.x_ref, EP.y_ref)
        self.extend(EP.verts)

    def pro_vs(self, EP):
        EP.make_polylist()
        EP.rotate(EP.theta)
        EP.offset(EP.x_ref, EP.y_ref)
        self.extend(EP.verts)
        EP.verts=[]

    def P(self, verts):
        """adds a polygon to the polylist with vertices given as a list of tuples"""
        #self.verts.append(self._gen_sP(verts))
        self.extend(self.sP(verts))

    def R(self, xr, yr, wr, hr):
        """creates rectangle EBLpolygon with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
        #self.verts.append(self._gen_sR(xr, yr, wr, hr))
        self.extend(self.sR(xr, yr, wr, hr))

    def C(self, xr, yr, wr, hr):
        """Adds a centered rectangle to the polylist"""
        #self.verts.append(self._gen_sC(xr, yr, wr, hr))
        self.extend(self.sC(xr, yr, wr, hr))

    def T(self, xr, yr, wr, hr, ot="R", nt=10):
        self.extend(self.sT(xr, yr, wr, hr, ot=ot, nt=nt))

    def sT(self, xr, yr, wr, hr, ot="R", nt=10, vs=None):
        vs=self.sR(xr, yr, wr, hr, vs)
        if ot in ("T", "B"):
            ts=wr/(2.0*nt)
        else:
            ts=hr/(2.0*nt)
        ct=ts*(2*nt-1)

        for tn in range(nt):
            if ot=="T":
                vs=self.sR(xr+wr/2.0-ct/2.0+2*tn*ts, yr+hr, ts, ts, vs )
            elif ot=="B":
                vs=self.sR(xr+wr/2.0-ct/2.0+2*tn*ts, yr, ts, -ts, vs )
            elif ot=="B":
                vs=self.sR(xr, yr+hr/2.0-ct/2.0+2*tn*ts, -ts, ts, vs )
            else:
                vs=self.sR(xr+wr, yr+hr/2.0-ct/2.0+2*tn*ts, ts, ts, vs )
        return vs

    def CT(self, xr, yr, wr, hr, ot="R", nt=10):
        self.extend(self.sCT(xr, yr, wr, hr, ot=ot, nt=nt))

    def sCT(self, xr, yr, wr, hr, ot="R", nt=10, vs=None):
        return self.sT(xr-wr/2.0, yr-hr/2.0, wr, hr, ot, nt=nt, vs=vs)

    def sP(self, verts, inlist=None):
        if inlist is None:
            inlist=[]
        inlist.append(self._gen_sP(verts)) #tuple([(v[0]/self.unit_factor, v[1]/self.unit_factor) for v in verts])
        return inlist

    def sR(self, xr, yr, wr, hr, inlist=None):
        """creates rectangle EBLpolygon with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
        if inlist is None:
            inlist=[]
        inlist.append(self._gen_sR(xr, yr, wr, hr))
        return inlist

    def sC(self, xr, yr, wr, hr, inlist=None):
        """Adds a centered rectangle to the polylist"""
        if inlist is None:
            inlist=[]
        inlist.append(self._gen_sC(xr, yr, wr, hr))
        return inlist

    def _gen_sP(self, verts):
        return tuple([(v[0]/self.unit_factor, v[1]/self.unit_factor) for v in verts])

    def _gen_sR(self, xr, yr, wr, hr):
        """creates rectangle EBLpolygon with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
        return self._gen_sP(verts=[(xr,yr), (xr+wr,yr), (xr+wr, yr+hr), (xr, yr+hr)])

    def _gen_sC(self, xr, yr, wr, hr):
        """Adds a centered rectangle to the polylist"""
        return self._gen_sR(xr-wr/2.0, yr-hr/2.0, wr, hr)

    def offset(self, x, y):
        self.verts=offset(self.verts, x, y, self.unit_factor)

    def horiz_refl(self):
        self.verts=horiz_refl(self.verts)

    def vert_refl(self):
        self.verts=vert_refl(self.verts)

    def rotate(self, theta):
        self.verts=rotate(self.verts, theta)

    def clear_verts(self):
        self.verts=[((0,0),)]

if __name__=="__main__":
    a=EBL_Polygons(unit_factor=2.0)
    print a.sP([(0,0), (1,0), (0,1)])
    print a.sR(0,0,1,1)
    print a.sC(0,0,1,1)
    print a.P([(0,0), (1,0), (0,1)])
    print a.R(0,0,1,1)
    print a.C(0,0,1,1)
    print a.verts
    a.offset(5,9)
    print a.verts

