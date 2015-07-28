# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:52:31 2015

@author: thomasaref
"""
from atom.api import Atom, Enum, Float, List, Unicode, Typed, Dict, Bool, observe
from numpy import sin, cos, pi
from a_Agent import sAgent
from Atom_Save_File import Save_DXF
from a_BeamerGen import BeamerGen

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

def sCross(xr, yr, wr, hr, lw, vs=None):
    """returns a cross centered at xr, yr with width wr, height hr and linewidth lw"""
    return sP([(xr-wr/2.0, yr-lw/2.0),
                (xr-wr/2.0, yr+lw/2.0),
                (xr-lw/2.0, yr+lw/2.0),
                (xr-lw/2.0, yr+hr/2.0),
                (xr+lw/2.0, yr+hr/2.0),
                (xr+lw/2.0, yr+lw/2.0),
                (xr+wr/2.0, yr+lw/2.0),
                (xr+wr/2.0, yr-lw/2.0),
                (xr+lw/2.0, yr-lw/2.0),
                (xr+lw/2.0, yr-hr/2.0),
                (xr-lw/2.0, yr-hr/2.0),
                (xr-lw/2.0, yr-lw/2.0)], vs)

def offset(verts, x, y):
    """offsets verts by x and y"""
    if x==0.0 and y==0.0:
        return verts
    x=x/gen_sP.UNIT_FACTOR
    y=y/gen_sP.UNIT_FACTOR
    return [tuple([(v[0]+x, v[1]+y) for v in p]) for p in verts]

def rotate(verts, theta):
    """rotates verts by theta. theta is in degrees"""
    if theta==0.0:
        return verts
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
    """Generates an individual digit list of vertices"""
    for func in digit_dict[str(dig_key)]:
        vs=func(xr, yr, wr, hr, vs)
    return vs


def sTransform(verts, x_off=0.0, y_off=0.0, theta=0.0, orient="TL", vs=None):
    """Transforms verts by given arguments and extends vs with them"""
    if vs is None:
        vs=[]
    if orient=="BR":
        verts=horizvert_refl(verts)
    elif orient=="BL":
        verts=vert_refl(verts)
    elif orient=="TR":
        verts=horiz_refl(verts)
    verts=rotate(verts, theta)
    verts=offset(verts, x_off, y_off)
    vs.extend(verts)
    return vs

def sPoly(obj, x_off=0.0, y_off=0.0, theta=0.0, orient="TL", vs=None):
    """attachs a EBL_Polygons obj verts to a list of verts after transforming them"""
    if vs is None:
        vs=[]
    obj.verts=[]
    obj.make_polylist()
    return sTransform(obj.verts[:], x_off, y_off, theta, orient, vs)

from Plotter import Plotter
from enaml import imports
from a_Show import show
from collections import OrderedDict

class Polygon_Chief(Atom):
    angle_x=Float(0.3e-6).tag(desc="shift in x direction when doing angle evaporation", unit="um")
    angle_y=Float(0.0e-6).tag(desc="shift in y direction when doing angle evaporation", unit="um")
    view_type=Enum("pattern", "angle")
    add_type=Enum("overwrite", "add")

    save_file=Unicode()
    name=Unicode()
    plot=Typed(Plotter, ())
    agents=List()
    pattern_dict=Dict() #for plotting
    patterns=Typed(OrderedDict, ()) #for generating jdf

    def show(self):
        show(*self.agents)

    def do_plot(self):
        for p in self.agents:
            p.verts=[]
            p.make_polylist()
            self.pattern_dict[p.name]=dict(verts=p.verts[:], color=p.color, layer=p.layer, plot_sep=p.plot_sep)
            p.make_name_sug()
            p.save_file.main_file=p.name_sug+".dxf"

        for key in self.pattern_dict:
            if self.pattern_dict[key]["plot_sep"]:
                self.plot.set_data(key, self.pattern_dict[key]["verts"], self.pattern_dict[key]["color"])

        xmin=min(b.xmin for b in self.agents)
        xmax=max(b.xmax for b in self.agents)
        ymin=min(b.ymin for b in self.agents)
        ymax=max(b.ymax for b in self.agents)
        self.plot.set_xlim(xmin, xmax)
        self.plot.set_ylim(ymin, ymax)
        self.plot.draw()

    @property
    def show_all(self):
        return True

    @property
    def view_window(self):
        with imports():
            from e_Show import EBLView
        return EBLView(chief=self)

pc=Polygon_Chief()

class EBL_Polygons(sAgent):
    color=Enum("green", "blue", "red", "purple", "brown", "black").tag(desc="color or datatype of item, could be used for dosing possibly")
    layer=Enum("Al", "Al_35nA", "Au").tag(desc='layer of item')
    save_file=Typed(Save_DXF, ()).tag(no_spacer=True)
    name_sug=Unicode().tag(no_spacer=True)
    shot_mod_table=Unicode()
    bmr=Typed(BeamerGen).tag(private=True)
    plot_sep=Bool(True)
    verts=List(default=[]).tag(private=True)

    def add_to_jdf(self):
        self.chief.patterns[self.name_sug]={"shot_mod":self.shot_mod_table}

    def make_name_sug(self):
        name_sug=""
        self.name_sug=name_sug

    def full_EBL_save(self, dir_path="""/Users/thomasaref/Dropbox/Current stuff/TA_software/discard/"""):
        self.verts=[]
        self.make_polylist()
        self.make_name_sug()
        file_path=dir_path+self.name_sug+".dxf"
        self.save_file.direct_save(self.verts[:], self.color, self.layer, file_path=file_path, write_mode='w')
        self.bmr=BeamerGen(file_name=self.name_sug, mod_table_name = self.shot_mod_table, bias=-0.009, base_path=dir_path,
                           extentLLy=-150, extentURy=150)
        self.bmr.gen_flow()
        self.add_to_jdf()

    @observe('save_file.save_event')
    def obs_save_event(self, change):
        self.save_file.direct_save(self.verts[:], self.color, self.layer, write_mode='w')

    @property
    def base_name(self):
        return "EBL_Polygons"

    @property
    def initial_position(self):
        return (0,300)

    @property
    def chief(self):
        return pc

    def __init__(self, **kwargs):
        """extends __init__ auto make polylist"""
        super(EBL_Polygons, self).__init__(**kwargs)
        self.make_polylist()

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

    def make_polylist(self):
        """function that makes polgyons in list. overwritten in children classes"""
        pass

    def P(self, verts):
        """adds a polygon to the polylist with vertices given as a list of tuples"""
        sP(verts, self.verts) #extend necesary

    def Poly(self, obj, x_off=0.0, y_off=0.0, theta=0.0, orient="TL"):
        """adds polygons to verts using an EBL_Polygons object as the source"""
        sPoly(obj, x_off, y_off, theta, orient, vs=self.verts)

    def R(self, xr, yr, wr, hr):
        """creates a rectangle EBLpolygon with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
        sR(xr, yr, wr, hr, self.verts)

    def C(self, xr, yr, wr, hr):
        """Adds a centered rectangle to the polylist"""
        sC(xr, yr, wr, hr, self.verts)

    def T(self, xr, yr, wr, hr, ot="R", nt=10):
        """adds a toothed rectangle to the polylist"""
        sT(xr, yr, wr, hr, ot=ot, nt=nt, vs=self.verts)

    def CT(self, xr, yr, wr, hr, ot="R", nt=10):
        """adds a centered toothed rectangle to the polylist"""
        sCT(xr, yr, wr, hr, ot=ot, nt=nt, vs=self.verts)

    def Cross(self, xr, yr, wr, lw):
        """adds a cross to the polylist"""
        sCross(xr, yr, wr, lw, self.verts)

    def Dig(self, dig_key, xr, yr, wr, hr):
        """adds a digit to the polylist"""
        sDig(dig_key, xr, yr, wr, hr, self.verts)

if __name__=="__main__":
    a=EBL_Polygons()
    print sP([(0,0), (1,0), (0,1)])
    a.show()

#    print a.sP([(0,0), (1,0), (0,1)])
#    print a.sR(0,0,1,1)
#    print a.sC(0,0,1,1)
#    print a.P([(0,0), (1,0), (0,1)])
#    print a.R(0,0,1,1)
#    print a.C(0,0,1,1)
#    print a.verts
#    a.offset(5,9)
#    print a.verts

