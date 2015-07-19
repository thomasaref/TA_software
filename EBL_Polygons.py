# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:52:31 2015

@author: thomasaref
"""
from atom.api import Atom, Enum, Float, List, Unicode
from numpy import sin, cos, pi
#from LOG_functions import log_debug

def gen_sP(verts):
    """generates a polygon from a list of vert tuples using a list comprehension. 
    Returns a tuple of verts divided by function defined unit factor"""
    return tuple([(v[0]/gen_sP.UNIT_FACTOR, v[1]/gen_sP.UNIT_FACTOR) for v in verts])
gen_sP.UNIT_FACTOR=1.0e-6  #microns

def sP(verts, vs=None):
    """converts verts to a polygon tuple, appends it to vs and returns vs. 
    returns a polygon list of length one if vs is none"""
    if vs is None:
        vs=[] #return [gen_sP(verts)]
    vs.append(gen_sP(verts))
    return vs
    
def sR(xr, yr, wr, hr, vs=None):
    """creates rectangle with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
    return sP(verts=[(xr,yr), (xr+wr,yr), (xr+wr, yr+hr), (xr, yr+hr)], vs=vs)

def sC(xr, yr, wr, hr, vs=None):
    """creates a centered rectangle with center coordinates=(xr,yr), width=wr, height=hr"""
    return sR(xr-wr/2.0, yr-hr/2.0, wr, hr, vs=vs)

def sT(xr, yr, wr, hr, ot="R", nt=10, vs=None):
    """makes a toothed rectangle at xr, yr dimensions wr, hr. Teeth are on side 
    given by ot (T, R, L, B) and nt is number of teeth"""
    vs=sR(xr, yr, wr, hr, vs)
    if ot in ("T", "B"):
        ts=wr/(2.0*nt)
    else:
        ts=hr/(2.0*nt)
    ct=ts*(2*nt-1)

    for tn in range(nt):
        if ot=="T":
            vs=sR(xr+wr/2.0-ct/2.0+2*tn*ts, yr+hr, ts, ts, vs )
        elif ot=="B":
            vs=sR(xr+wr/2.0-ct/2.0+2*tn*ts, yr, ts, -ts, vs )
        elif ot=="L":
            vs=sR(xr, yr+hr/2.0-ct/2.0+2*tn*ts, -ts, ts, vs )
        else:
            vs=sR(xr+wr, yr+hr/2.0-ct/2.0+2*tn*ts, ts, ts, vs )
    return vs

def sCT(xr, yr, wr, hr, ot="R", nt=10, vs=None):
    """returns a centered toothed rectangle"""    
    return sT(xr-wr/2.0, yr-hr/2.0, wr, hr, ot, nt=nt, vs=vs)

def sCross(xr, yr, wr, lw, vs=None):
    """returns a cross centered at xr, yr with width wr and linewidth lw"""
    return sP([(xr-wr/2.0, yr-lw/2.0),
                (xr-wr/2.0, yr+lw/2.0),
                (xr-lw/2.0, yr+lw/2.0),
                (xr-lw/2.0, yr+wr/2.0),
                (xr+lw/2.0, yr+wr/2.0),
                (xr+lw/2.0, yr+lw/2.0),
                (xr+wr/2.0, yr+lw/2.0),
                (xr+wr/2.0, yr-lw/2.0),
                (xr+lw/2.0, yr-lw/2.0),
                (xr+lw/2.0, yr-wr/2.0),
                (xr-lw/2.0, yr-wr/2.0),
                (xr-lw/2.0, yr-lw/2.0)], vs)

def offset(verts, x, y):
    """offsets verts by x and y"""
    x=x/gen_sP.UNIT_FACTOR
    y=y/gen_sP.UNIT_FACTOR
    return [tuple([(v[0]+x, v[1]+y) for v in p]) for p in verts]

def rotate(verts, theta):
    """rotates verts by theta. theta is in degrees"""
    theta=theta/180.0*pi
    cos_theta=cos(theta)
    sin_theta=sin(theta)
    return [tuple([(v[0]*cos_theta-v[1]*sin_theta, v[0]*sin_theta+v[1]*cos_theta) for v in p]) for p in verts]

def horiz_refl(verts):
    """horizontally reflects verts"""
    return [tuple([(-v[0], v[1]) for v in p]) for p in verts]

def vert_refl(verts):
    """vertically reflects verts"""
    return [tuple([(v[0], -v[1]) for v in p]) for p in verts]

def horizvert_refl(verts):
    """horizontally and vertically reflects verts. equivalent to horiz_refl(vert_refl(verts))"""
    return [tuple([(-v[0], -v[1]) for v in p]) for p in verts]

def minx(verts):
    """returns minimum x coordinate in list of verts and -1.0 if list is empty"""
    if verts==[]:
        return -1.0
    return min([min([v[0] for v in p]) for p in verts])

def miny(verts):
    """returns minimum y coordinate in list of verts and -1.0 if list is empty"""
    if verts==[]:
        return -1.0
    return min([min([v[1] for v in p]) for p in verts])

def maxx(verts):
    """returns maximum x coordinate in list of verts and 1.0 if list is empty"""
    if verts==[]:
        return 1.0
    return max([max([v[0] for v in p]) for p in verts])

def maxy(verts):
    """returns maximum y coordinate in list of verts and 1.0 if list is empty"""
    if verts==[]:
        return 1.0
    return max([max([v[1] for v in p]) for p in verts])
        
def sHD(xr, yr, wr, lw, vs=None):
    """draws a horizontal diamond at xr, yr of width wr, linewidth lw"""
    return sP([(xr, yr), (xr+lw/2.0, yr+lw/2), (xr+wr-lw/2.0, yr+lw/2.0),
                 (xr+wr, yr), (xr+wr-lw/2.0, yr-lw/2.0), (xr+lw/2.0, yr-lw/2)], vs)

def sVD(xr, yr, wr, lw, vs=None):
    """draws a vertical diamond at xr, yr of width wr, linewidth lw"""
    return sP([(xr, yr), (xr-lw/2.0, yr+lw/2.0), (xr-lw/2.0, yr+wr-lw/2.0),
                 (xr, yr+wr), (xr+lw/2.0, yr+wr-lw/2.0), (xr+lw/2.0, yr+lw/2.0)], vs)
    
def M(xr, yr, wr, lw, vs=None):
    """draws middle of digit"""    
    return sHD(xr-wr/2.0, yr, wr, lw, vs)
    
def T(xr, yr, wr, hr, vs=None):
    """draws top of digit"""    
    return sHD(xr-wr/2.0, yr+wr, wr, hr, vs)

def B(xr, yr, wr, hr, vs=None):
    """draws bottom of digit"""    
    return sHD(xr-wr/2.0, yr-wr, wr, hr, vs)

def TL(xr, yr, wr, hr, vs=None):
    """draws top left of digit"""    
    return sVD(xr-wr/2.0, yr, wr, hr, vs)
        
def TR(xr, yr, wr, hr, vs=None):
    """draws top right of digit"""    
    return sVD(xr+wr/2.0, yr, wr, hr, vs)

def BR(xr, yr, wr, hr, vs=None):
    """draws bottom right of digit"""    
    return sVD(xr+wr/2.0, yr-wr, wr, hr, vs)

def BL(xr, yr, wr, hr, vs=None):
    """draws bottom left of digit"""    
    return sVD(xr-wr/2.0, yr-wr, wr, hr, vs)
    
def sqL(xr, yr, wr, lw, vs=None):
    """draws square left for letters B and D"""
    return sR(xr-wr/2.0-lw/2.0, yr-wr-lw/2.0, lw, 2*wr+lw, vs)

digit_dict={    "0":[T, TL, BL, B, BR, TR],
                "1":[TR, BR],
                "2":[T, TR, M, BL, B],
                "3":[T, TR, M, BR, B],
                "4":[TL, TR, M, BR],
                "5":[T, TL, M, BR, B],
                "6":[T, TL, M, BR, B, BL],
                "7":[T, TR, BR],
                "8":[T, TL, TR, M, BL, BR, B], 
                "9":[T, TL, TR, M, BR, B],
                "A":[T, TL, TR, M, BL, BR],
                "B":[T, sqL, TR, M, BR, B],
                "C":[T, TL, BL, B],
                "D":[T, sqL, B, BR, TR]}

def sDig(dig_key, xr, yr, wr, hr, vs=None):
    for func in digit_dict[str(dig_key)]:
        vs=func(xr, yr, wr, hr, vs)
    return vs

    
def sPoly(obj, vs=None):
    if vs is None:
        vs=[]
    obj.make_polylist()
    if obj.orient=="BR":
        obj.horizvert_refl()
    elif obj.orient=="BL":
        obj.vert_refl()
    elif obj.orient=="TR":
        obj.horiz_refl()
    obj.rotate(obj.theta)
    obj.offset(obj.x_ref, obj.y_ref)
    vs.extend(obj.verts)
    return vs

#digit_dict.update(dict(zip([str(key) for key in digit_dict.keys()], digit_dict.values())))
class Polygon_Chief(Atom):
    save_file=Unicode()
    name=Unicode()
    plots=List(default=["a", "b"])
    #log_str=Unicode("blarg")
    
    @property
    def show_all(self):
        return True
pc=Polygon_Chief()

class EBL_Polygons(Atom):
    color=Enum("green", "blue", "red", "purple", "brown", "black").tag(desc="color or datatype of item, could be used for dosing possibly")
    layer=Enum("Al", "Al_35nA", "Au").tag(desc='layer of item')
    #unit_factor=Float(1.0e-6)
    verts=List(default=[]).tag(private=True)
    children=List().tag(private=True)
    x_ref=Float(0.0).tag(desc="x coordinate of reference point of pattern.", unit="um")
    y_ref=Float(0.0).tag(desc="y coordinate of reference point of pattern", unit="um")
    theta=Float(0.0).tag(desc="angle to rotate in degrees")
    orient=Enum("TL", "TR", "BL", "BR")

    #@property
    #def chief(self):
    #    return pc
    
    @property
    def xmin(self):
        return minx(self.verts)

    @property
    def xmax(self):
        return maxx(self.verts)

    @property
    def ymin(self):
        return miny(self.verts)

    @property
    def ymax(self):
        return maxy(self.verts)
        
    def extend(self, vert_obj):
        """accepts either a list of vertices or an EBL_Polygons object and adds its vertices to self.verts"""
        if hasattr(vert_obj, "verts"):
            vert_obj.make_verts()
            self.verts.extend(vert_obj.verts)
        else:
            self.verts.extend(vert_obj)

    def make_polylist(self):
        pass
        #self.P([(0,0)])
    
#    def make_verts(self):
#        self.make_polylist()
#        if self.orient=="BR":
#            self.horizvert_refl()
#        elif self.orient=="BL":
#            self.vert_refl()
#        elif self.orient=="TR":
#            self.horiz_refl()
#        self.rotate(self.theta)
#        self.offset(self.x_ref, self.y_ref)
#        for c in self.children:
#            c.make_verts()



#    def pros(self, EP):
#        EP.make_polylist()
#        EP.rotate(EP.theta)
#        EP.offset(EP.x_ref, EP.y_ref)
#        self.extend(EP.verts)
#
#    def pro_vs(self, EP):
#        EP.make_polylist()
#        EP.rotate(EP.theta)
#        EP.offset(EP.x_ref, EP.y_ref)
#        self.extend(EP.verts)
#        EP.verts=[]

#    def make_polylist(self):
#        self.verts.extend(sP([(0,0), (1,1), (1,0)]))
        
    def P(self, verts):
        """adds a polygon to the polylist with vertices given as a list of tuples"""
        sP(verts, self.verts) #extend necesary

    def Poly(self, obj):
        sPoly(obj, self.verts)

    def R(self, xr, yr, wr, hr):
        """creates rectangle EBLpolygon with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
        sR(xr, yr, wr, hr, self.verts)

    def C(self, xr, yr, wr, hr):
        """Adds a centered rectangle to the polylist"""
        sC(xr, yr, wr, hr, self.verts)

    def T(self, xr, yr, wr, hr, ot="R", nt=10):
        sT(xr, yr, wr, hr, ot=ot, nt=nt, vs=self.verts)

    def CT(self, xr, yr, wr, hr, ot="R", nt=10):
        sCT(xr, yr, wr, hr, ot=ot, nt=nt, vs=self.verts)

    def Cross(self, xr, yr, wr, lw):
        sCross(xr, yr, wr, lw, self.verts)
        
    def Dig(self, dig_key, xr, yr, wr, hr):
        sDig(dig_key, xr, yr, wr, hr, self.verts)

    def offset(self, x, y):
        if x!=0.0 and y!=0.0:
            self.verts=offset(self.verts, x, y)

    def horiz_refl(self):
        self.verts=horiz_refl(self.verts)

    def vert_refl(self):
        self.verts=vert_refl(self.verts)

    def rotate(self, theta):
        if theta!=0.0:
            self.verts=rotate(self.verts, theta)

    def clear_verts(self):
        self.verts=[((0,0),)]
    


                    

if __name__=="__main__":
    a=EBL_Polygons()
    print sP([(0,0), (1,0), (0,1)])
    a.P([(0,0), (1,0), (0,1)])
    
    a.P([(0,0), (1.5,2), (2,2)])
    print a.verts
    from a_Show import show
    show(a)

#    print a.sP([(0,0), (1,0), (0,1)])
#    print a.sR(0,0,1,1)
#    print a.sC(0,0,1,1)
#    print a.P([(0,0), (1,0), (0,1)])
#    print a.R(0,0,1,1)
#    print a.C(0,0,1,1)
#    print a.verts
#    a.offset(5,9)
#    print a.verts

