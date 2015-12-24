# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 12:51:22 2015

@author: thomasaref
"""

from atom.api import Enum, Int, ContainerList, Unicode
from taref.core.agent import Agent
from enaml import imports

 #3print '\033[1;32mGreen like Grass\033[1;m'
 #4print '\033[1;33mYellow like Yolk\033[1;m'
 #5print '\033[1;34mBlue like Blood\033[1;m'
 
QUARTER_WAFER_SIGNS={"A" : (-1, 1), "B" : (1, 1), "C" : (-1, -1), "D" : (1, -1)}

class WaferCoords(Agent):
    diameter=Int(4).tag(unit=" in", desc="wafer diameter in inches")
    radius=Int().tag(unit=" um", desc="wafer radius in microns")
    chip_size=Int(5000).tag(desc="size of chip in microns", unit=" um")
    gap_size=Int(5000).tag(desc="gap from center of wafer", unit=" um")

    wafer_type=Enum("A", "B", "C", "D")

    x_offset=Int()
    x_mult=Int()    
    y_offset=Int()
    y_mult=Int()
    N_chips=Int()
    html_text=Unicode()
    wafer=ContainerList(default=[0])
    bad_coords=ContainerList(default=[0])
    good_coords=ContainerList(default=[0])
    array=Unicode()

    def _update_array(self, x_offset, y_offset, N_chips, chip_size):        
        return unicode([(x_offset, N_chips, chip_size), (y_offset, N_chips, chip_size)])
    
    def _update_x_mult(self, wafer_type):
        return QUARTER_WAFER_SIGNS[wafer_type][0]    

    def _update_y_mult(self, wafer_type):
        return QUARTER_WAFER_SIGNS[wafer_type][1]    

    def _update_radius(self, diameter):
        return diameter*25400/2

    def _update_x_offset(self, x_mult, gap_size, chip_size):  
        return x_mult*(gap_size+chip_size/2)-7*(1-x_mult)/2*chip_size
    
    def _update_y_offset(self, y_mult, gap_size, chip_size):  
        return y_mult*(gap_size+chip_size/2)+7*(1+y_mult)/2*chip_size

    def _update_N_chips(self, radius, chip_size, gap_size):
        return (radius-gap_size)/chip_size-1

    def _update_wafer(self, x_offset, y_offset, x_mult, y_mult, chip_size, radius, N_chips):
        return [(x+1, y+1) for x in range(N_chips) for y in range(N_chips)
              if ((x+x_mult)*chip_size+x_offset)**2+((y_mult-y)*chip_size+y_offset)**2<=radius**2]

    def _update_bad_coords(self, wafer):
        return [ item for item in wafer
                 if (item[0]+1, item[1]) not in wafer or (item[0]-1, item[1]) not in wafer
                 or (item[0], item[1]+1) not in wafer or (item[0], item[1]-1) not in wafer]

    def _update_good_coords(self, wafer, bad_coords):
        return [x for x in wafer if x not in bad_coords]
    
    def _update_html_text(self, wafer, good_coords, bad_coords, N_chips):
        tt=['<table border="1">']
        for y in range(N_chips):
            tt.append('<tr>')
            for x in range(N_chips):
                tt.append('<td>')
                item=(x+1, y+1)
                if item in wafer:
                    if item in bad_coords:
                        tt.append('<p style="color:red"> {0} </p>'.format(item))
                    if item in good_coords:
                        tt.append('<p style="color:green"> {0} </p>'.format(item))
                tt.append('</td>')
            tt.append('</tr>')
        tt.append("</table>")
        return "\n".join(tt)

                 
    @property
    def view_window(self):
        with imports():
            from taref.ebl.wafer_coords_e import Main
        return Main(wc=self)

a=WaferCoords()
a.wafer_type="B"
a.diameter=4
a.chip_size=5000
a.gap_size=5000

a.show()
        
def gen_spots(chipsize=5000, gapsize=5000, waferD=4, qw="D"):
    mydict={}
    mx, my=QUARTER_WAFER_SIGNS[qw]    
    xo=mx*(gapsize+chipsize/2)-7*(1-mx)/2*chipsize
    yo=my*(gapsize+chipsize/2)+7*(1+my)/2*chipsize
    R=waferD*25400/2
    N=(R-gapsize)/chipsize-1
    mydict["Array"]=[(xo, N, chipsize), (yo, N, chipsize)]
    xo+=mx*chipsize    
    yo+=my*chipsize
    #mydict["Wafer"]
    wafer=[(x+1, y+1) for x in range(N) for y in range(N)
    if (x*chipsize+xo)**2+(-y*chipsize+yo)**2<=R**2]
   
    BadCoords = [ item for item in wafer
    if (item[0]+1, item[1]) not in wafer 
    or (item[0]-1, item[1]) not in wafer
    or (item[0], item[1]+1) not in wafer
    or (item[0], item[1]-1) not in wafer]

    print 
    def func(item):
        if item in wafer:
            return item
        return (0, 0)
    print [func((x+1, y+1)) for x in range(N) for y in range(N)]

gen_spots()
GLM_dict=dict(A=[(-40000, 4000), (-4000, 40000)],
              B=[(4000, 40000), (40000, 4000)],
              C=[(-40000, -4000), (-4000, -40000)],
              D=[(4000, -40000), (40000, -4000)])

def get_GLM(qw):
    """returns Px, Py, Qx, Qy" for a given quarter wafer"""
    glm=GLM_dict[qw]
    return glm[0][0], glm[0][1], glm[1][0], glm[1][1] 

Array_dict=dict(A=[(-42500,8,5000), (42500,8,5000)],
                B=[(7500,8,5000), (42500,8,5000)],
                C=[(-42500,8,5000), (-7500,8,5000)],
                D=[(7500,8,5000), (-7500,8,5000)])

def get_Array(qw):
    """returns Px, Py, Qx, Qy" for a given quarter wafer"""
    ar=Array_dict[qw]
    return ar[0][0], ar[0][1], ar[0][2], ar[1][0], ar[1][1], ar[1][2]  

def give_GoodCoords(WAFER, BadCoords):
    return [x for x in WAFER if x not in BadCoords]

def get_WaferCoords(qwaf):
    A_WAFER=[                                         (7,1), (8,1),
                                       (5,2), (6,2), (7,2), (8,2),
                                (4,3), (5,3), (6,3), (7,3), (8,3),
                         (3,4), (4,4), (5,4), (6,4), (7,4), (8,4),
                  (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5),
                  (2,6), (3,6), (4,6), (5,6), (6,6), (7,6), (8,6),
           (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7),
           (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)]
    
    A_BadCoords=[(7,1), (8,1),
               (5,2), (8,2),
               (4,3), (8,3),
               (3,4), (8,4),
               (2,5), (8,5),
               (2,6), (8,6),
               (1,7), (8,7),
               (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)]
    
    B_WAFER=[(1, 1), (2, 1),
             (1, 2), (2, 2), (3, 2), (4, 2),
             (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
             (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
             (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),
             (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
             (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7),
             (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
    
    B_BadCoords=[(1, 1), (2, 1),
             (1, 2), (4, 2),
             (1, 3), (5, 3),
             (1, 4), (6, 4),
             (1, 5), (7, 5),
             (1, 6), (7, 6),
             (1, 7), (8, 7),
             (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
        
    C_WAFER=[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
             (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
                     (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
                     (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
                             (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
                                     (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
                                             (5, 7), (6, 7), (7, 7), (8, 7),
                                                             (7, 8), (8, 8)]
    
    C_BadCoords=[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
                                                                 (1, 2), (8, 2),
                                                                 (2, 3), (8, 3),
                                                                 (2, 4), (8, 4),
                                                                 (3, 5), (8, 5),
                                                                 (4, 6), (8, 6),
                                                                 (5, 7), (8, 7),
                                                                 (7, 8), (8, 8)]
    
    D_WAFER=[(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1),
             (1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2),
             (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3),
             (1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4),
             (1,5), (2,5), (3,5), (4,5), (5,5), (6,5),
             (1,6), (2,6), (3,6), (4,6), (5,6),
             (1,7), (2,7), (3,7), (4,7),
             (1,8), (2,8)]
    
    D_BadCoords=[(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1),
                 (1,2), (8,2),
                 (1,3), (7,3),
                 (1,4), (7,4),
                 (1,5), (6,5),
                 (1,6), (5,6),
                 (1,7), (4,7),
                 (1,8), (2,8)]
    if qwaf=='A':
        WAFER=A_WAFER
        BadCoords=A_BadCoords
    elif qwaf=='B':
        WAFER=B_WAFER
        BadCoords=B_BadCoords
    elif qwaf=='C':
        WAFER=C_WAFER
        BadCoords=C_BadCoords
    elif qwaf=='D':
        WAFER=D_WAFER
        BadCoords=D_BadCoords
    else:
        print "Bad quarter wafer!"
    GoodCoords=give_GoodCoords(WAFER, BadCoords)
    return WAFER, BadCoords, GoodCoords
    
    #D_GoodCoords=give_GoodCoords(D_WAFER, D_BadCoords)

def numCoords2(Coords, AssignArray):
    return int(len(Coords)//len(AssignArray))

def numCoords(Coords, lengthAA):
    return int(len(Coords)//lengthAA)

#AssignArray=[('A(1)+A(2)+A(15)', 'D32080 with two IDTs and Squid connect'),
#        ('A(1)+A(3)+A(15)', 'S32080 with two IDTs and Squid connect'),
#        ('A(1)+A(4)+A(15)', 'S32050 with two IDTs and Squid connect'),
#        ('A(1)+A(5)+A(15)',  'D32050 with two IDTs and Squid connect'),
#        ('A(1)+A(6)+A(15)',  'D9050 with two IDTs and Squid connect'),
#        ('A(1)+A(7)+A(15)', 'S9050 with two IDTs and Squid connect'),
#        ('A(1)+A(8)+A(15)', 'S9080 with two IDTs and Squid connect'),
#        ('A(1)+A(9)+A(15)', 'D9080 with two IDTs and Squid connect'),
#        ('A(12)+A(10)+A(15)', 'D5080 with two FDTs and Squid connect'),
#        ('A(12)+A(11)+A(15)', 'D5096 with two FDTs and Squid connect'),
#        ('A(13)+A(15)', 'IDT by itself'),
#        ('A(14)+A(15)', 'FDT by itself'),
#        ('A(1)+A(15)',  'Two IDTs alone with squid connect'),
#        ('A(12)+A(15)', 'two FDTs alone with squid connect')]


#print numBadCoords, numGoodCoords

def distr_one_coord(i, BadCoords, GoodCoords, numBadCoords, numGoodCoords, numSkip):
    templist=[BadCoords[n*numSkip+i] for n in range(numBadCoords)]
    templist.extend([GoodCoords[m*numSkip+i] for m in range(numGoodCoords)])
    leftover=len(BadCoords)-numBadCoords*numSkip
    if numBadCoords*numSkip+i<len(BadCoords):
        templist.append(BadCoords[(numBadCoords)*numSkip+i])
    elif numGoodCoords*numSkip-leftover+i<len(GoodCoords):
        templist.append(GoodCoords[numGoodCoords*numSkip-leftover+i])
    if numGoodCoords*numSkip-leftover+numSkip+i<len(GoodCoords):
        templist.append(GoodCoords[(numGoodCoords+1)*numSkip-leftover+i])
    return templist
    
def distribute_coords(lengthAA, qwaf='A'):#BadCoords, WAFER):
    WAFER, BadCoords, GoodCoords=get_WaferCoords(qwaf=qwaf)
    numGoodCoords=numCoords(GoodCoords, lengthAA)
    numBadCoords=numCoords(BadCoords, lengthAA)
    numSkip=lengthAA
    return [distr_one_coord(i, BadCoords, GoodCoords, numBadCoords, numGoodCoords, numSkip) for i in range(lengthAA)]

def distr_coords2(AssignArray, qwaf='A'):#BadCoords, WAFER):
    WAFER, BadCoords, GoodCoords=get_WaferCoords(qwaf=qwaf)
    numGoodCoords=numCoords(GoodCoords, AssignArray)
    numBadCoords=numCoords(BadCoords, AssignArray)
    numSkip=len(AssignArray)    
    for i, item in enumerate(AssignArray):
        tempstr=""
        for n in range(numBadCoords):
            tempstr+=str(BadCoords[n*numSkip+i])+", "
        for m in range(numGoodCoords):
            tempstr+=str(GoodCoords[m*numSkip+i])+", "
        leftover=len(BadCoords)-numBadCoords*numSkip
        if numBadCoords*numSkip+i<len(BadCoords):
            tempstr+=str(BadCoords[(n+1)*numSkip+i])+", "
        #offset+=1
        elif numGoodCoords*numSkip-leftover+i<len(GoodCoords):
            tempstr+=str(GoodCoords[numGoodCoords*numSkip-leftover+i])+", "
        if numGoodCoords*numSkip-leftover+numSkip+i<len(GoodCoords):
            tempstr+=str(GoodCoords[(numGoodCoords+1)*numSkip-leftover+i])+", "
    tempstr=tempstr[:-2]
    
    #if (m+1)*numSkip+i<len(GoodCoords):
    #    tempstr+=str(GoodCoords[(m+1)*numSkip+i])+", "
#    print "ASSIGN {arrays} -> ({nums}{dose}) ;{comment}".format(arrays=item[0], comment=item[1], nums=tempstr[:-2], dose="")
