# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 18:59:00 2015

@author: thomasaref
"""

#    @property
#    def Al_test_strip(self):
#        """creates Al test strip, not used?"""
#        self.P([(-self.gndplane_testgap/2.0, -self.yheight),
#                   (self.gndplane_testgap/2.0, -self.yheight),
#                   (self.gndplane_big_gap/2.0+self.gndplane_width, -self.w/2.0-self.gap),
#                   (-self.gndplane_big_gap/2.0-self.gndplane_width, -self.w/2.0-self.gap)])
#        self.P([(-self.gndplane_big_gap/2.0-self.gndplane_width, -self.w/2.0-self.gap),
#                  (-self.gndplane_big_gap/2.0-self.gndplane_width, -self.gndplane_gap/2.0),
#                  (-self.gndplane_big_gap/2.0, -self.gndplane_gap/2.0),
#                  (-self.gndplane_big_gap/2.0, -self.w/2.0-self.gap)])
#        self.P([(self.gndplane_big_gap/2.0+self.gndplane_width, -self.w/2.0-self.gap),
#                  (self.gndplane_big_gap/2.0+self.gndplane_width, -self.gndplane_gap/2.0),
#                  (self.gndplane_big_gap/2.0, -self.gndplane_gap/2.0),
#                  (self.gndplane_big_gap/2.0, -self.w/2.0-self.gap)])

#    def make_idt_conn(self):
#        """connects CPW to IDT"""
#        self.R(-self.width/2.0, -self.height/2.0, -self.Al_sec, -self.w)
#        self.P([(-self.width/2.0, -self.height/2.0), (-self.width/2.0, self.height/2.0), (-3.0*self.width/2.0, -self.height/2.0)])

#from Plotter import Plotter
#from enaml import imports
#from a_Chief import show
#from collections import OrderedDict

#class Polygon_Chief(Atom):
#    angle_x=Float(0.3e-6).tag(desc="shift in x direction when doing angle evaporation", unit="um")
#    angle_y=Float(0.0e-6).tag(desc="shift in y direction when doing angle evaporation", unit="um")
#    view_type=Enum("pattern", "angle")
#    add_type=Enum("overwrite", "add")
#
#    save_file=Unicode()
#    name=Unicode()
#    plot=Typed(Plotter, ())
#    agents=List()
#    pattern_dict=Dict() #for plotting
#    patterns=Typed(OrderedDict, ()) #for generating jdf
#
#    def show(self):
#        show(*self.agents)
#
#    def do_plot(self):
#        for p in self.agents:
#            p.verts=[]
#            p.make_polylist()
#            self.pattern_dict[p.name]=dict(verts=p.verts[:], color=p.color, layer=p.layer, plot_sep=p.plot_sep)
#            p.make_name_sug()
#            p.save_file.main_file=p.name_sug+".dxf"
#
#        for key in self.pattern_dict:
#            if self.pattern_dict[key]["plot_sep"]:
#                self.plot.set_data(key, self.pattern_dict[key]["verts"], self.pattern_dict[key]["color"])
#
#        xmin=min(b.xmin for b in self.agents)
#        xmax=max(b.xmax for b in self.agents)
#        ymin=min(b.ymin for b in self.agents)
#        ymax=max(b.ymax for b in self.agents)
#        self.plot.set_xlim(xmin, xmax)
#        self.plot.set_ylim(ymin, ymax)
#        self.plot.draw()
#
#    @property
#    def show_all(self):
#        return True
#
#    @property
#    def view_window(self):
#        with imports():
#            from e_Show import EBLView
#        return EBLView(chief=self)

#pc=Polygon_Chief()

                #asgn_type="+".join(item.assign_type)
                #pos_asgn=""
                #for pos in item.pos_assign:
                #    pos_asgn+="({x},{y}),".format(x=pos[0], y=pos[1])
                #pos_asgn=pos_asgn[:-1]
                #if item.shot_assign=="":
                #    shot_asgn=""
                #else:
                #    shot_asgn=", {sa}".format(sa=item.shot_assign)
                #if item.assign_comment=="":
                #    asgn_comment=""
                #else:
                #    asgn_comment=";{ac}".format(ac=item.assign_comment)
                #jl.append("\tASSIGN {asgn_type} -> ({pos_asgn}{shot_asgn}) {asgn_comment}".format(
                #          asgn_type=asgn_type, pos_asgn=pos_asgn, shot_asgn=shot_asgn, asgn_comment=asgn_comment))

#            if item.array_num==0:
#                jl.append("ARRAY ({x_start}, {x_num}, {x_step})/({y_start}, {y_num}, {y_step})".format(
#                       x_start=self.arrays[0].x_start, x_num=self.arrays[0].x_num, x_step=self.arrays[0].x_step,
#                       y_start=self.arrays[0].y_start, y_num=self.arrays[0].y_num, y_step=self.arrays[0].y_step))
#                jl.append("\tCHMPOS M1=({M1x}, {M1y})".format(M1x=self.arrays[0].M1x, M1y=self.arrays[0].M1y))
#            else:
#                jl.append("{arr_num}: ARRAY ({x_start}, {x_num}, {x_step})/({y_start}, {y_num}, {y_step})".format(
#                       arr_num=item.array_num, x_start=item.x_start, x_num=item.x_num, x_step=item.x_step,
#                       y_start=item.y_start, y_num=item.y_num, y_step=item.y_step))
#            for asg_item in item.assigns:
#                jl.append(asg_item.jdf_output)
#            jl.append("AEND\n")
#                    if ":" in tempstr:
#                        array_num=tempstr.split(":")[0] #for subarrays
#                        x_start, x_num, x_step, y_start, y_num, y_step=xy_string_split(tempstr)
#                        self.arrays.append(JDF_Array(array_num=array_num, x_start=x_start, x_num=x_num, x_step=x_step,
#                                         y_start=y_start, y_num=y_num, y_step=y_step, comment=comment))
#                    else:
#                        x_start, x_num, x_step, y_start, y_num, y_step=xy_string_split(tempstr)
#                        self.arrays.append(JDF_Main_Array(x_start=x_start, x_num=x_num, x_step=x_step,
#                                                         y_start=y_start, y_num=y_num, y_step=y_step, comment=comment))


    #def _update_array(self, x_offset, y_offset, N_chips, chip_size):   
    #    log_debug("array")
    #    return [x_offset, N_chips, chip_size, y_offset, N_chips, chip_size]

    #def _update_x_mult(self, wafer_type):
     #   log_debug("x_mult")
     #   return QUARTER_WAFER_SIGNS[wafer_type][0]    

    #def _update_y_mult(self, wafer_type):
    #    log_debug("y_mult")
    #    return QUARTER_WAFER_SIGNS[wafer_type][1]    

    #def _update_radius(self, diameter):
    #    log_debug("radius")
    #    return int(diameter*25400/2)
        
    #def _update_x_offset(self, gap_size, chip_size, N_chips):  
    #    log_debug("x_offset")
    #    return self.x_mult*(gap_size+chip_size/2)-(N_chips-1)*(1-self.x_mult)/2*chip_size
    
    #def _update_y_offset(self, gap_size, chip_size, N_chips):  
    #    log_debug("y_offset")
    #    return self.y_mult*(gap_size+chip_size/2)+(N_chips-1)*(1+self.y_mult)/2*chip_size

    #def _update_N_chips(self, chip_size, gap_size):
    #    log_debug("N_chips")
    #    return (self.radius-gap_size)/chip_size-1

#    def _update_wafer(self, x_offset, y_offset, chip_size, N_chips):
#        log_debug("wafer")
#        return [(x+1, y+1) for x in range(N_chips) for y in range(N_chips)
#              if ((x+self.x_mult)*chip_size+x_offset)**2+((self.y_mult-y)*chip_size+y_offset)**2<=self.radius**2]
#
#    def _update_bad_coords(self, wafer, bad_coord_type):
#        log_debug("bad_coords")
#        if bad_coord_type=="quarter wafer":
#            return [ item for item in wafer
#                 if (item[0]+1, item[1]) not in wafer or (item[0]-1, item[1]) not in wafer
#                 or (item[0], item[1]+1) not in wafer or (item[0], item[1]-1) not in wafer]
#        return [ item for item in wafer
#                 if (item[0]+self.x_mult, item[1]) not in wafer
#                 or (item[0], item[1]-self.y_mult) not in wafer]
#
#    def _update_good_coords(self, wafer, bad_coords):
#        log_debug("good_coords")
#        return [x for x in wafer if x not in bad_coords]
#    
    def _update_html_text(self, wafer, good_coords, bad_coords, N_chips):

    #wafer=List().tag(update=["_update_bad_coords", "_update_good_coords"])
    #bad_coords=List()
    #good_coords=List()

    #radius=Int().tag(unit=" um", desc="wafer radius in microns")

#    @property
#    def view_window(self):
#        with imports():
#            from taref.ebl.wafer_coords_e import FullWaferView
#        view=FullWaferView(fw=self)
#        #view.visible=False
#        return view
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

#gen_spots()
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
    
def distribute_coords(lengthAA, qwaf='A'):
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
