# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 17:18:17 2015

@author: thomasaref
"""

from numpy import sin, cos, pi

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
def letter_A(xr, yr, wr, lw, vs=None):
    """Draws the capital letter A of width wr, height 2*wr and linewidth lw"""
    vs=sP([(xr-wr/2.0-lw/2.0, yr-wr), (xr-lw, yr+wr), (xr+lw, yr+wr),
                (xr+wr/2.0+lw/2.0, yr-wr), (xr+wr/2.0-lw/2.0, yr-wr), (xr, yr+wr-lw),
                (xr-wr/2.0+lw/2.0, yr-wr)], vs)
    return sP([(xr+(-wr+lw-lw/2.0)*(-wr/2.0-lw/2.0)/(-2*wr+lw), yr-lw/2.0),
                (xr+(-wr+lw+lw/2.0)*(-wr/2.0-lw/2.0)/(-2*wr+lw), yr+lw/2.0),
    #(xr+(-wr+lw-lw/2.0)*(wr-lw)/(4.0*wr), yr-lw/2.0),
                #(xr-lw-(lw+wr/2.0)/2.0+lw/2.0, yr),
               #(xr+(-wr+lw+lw/2.0)*(wr-lw)/(4.0*wr), yr+lw/2.0), #return sP([(xr-wr/2.0+lw/2.0, yr-lw/2.0), (xr-wr/2.0+lw/2.0, yr+lw/2.0),
               (xr+wr/2.0-lw/2.0, yr+lw/2.0),(xr+wr/2.0-lw/2.0, yr-lw/2.0),], vs) 
    
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

def sWaferDig(wafer_type, x_dig, y_dig, xr, yr, wr, hr, vs=None):
    vs=sDig(wafer_type, xr-wr-2*hr, yr, wr, hr, vs)
    vs=sDig(x_dig, xr, yr, wr, hr, vs)
    return sDig(y_dig, xr+wr+2*hr, yr, wr, hr, vs)   

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
