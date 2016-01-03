# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:52:31 2015

@author: thomasaref
"""
from atom.api import Enum, List, Unicode, Typed, Bool, observe
from taref.core.agent import SubAgent
from taref.core.save_file import Save_DXF
from taref.ebl.beamer_gen import BeamerGen
from taref.ebl.polygon_chief import polygon_chief
from taref.core.log import log_warning
from taref.ebl.polygon_backbone import (minx, maxx, miny, maxy, sP, sPoly,
                                        sR, sC, sT, sCT, sCross, sDig, sWaferDig)

class EBL_Polygons(SubAgent):
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
        return polygon_chief

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
        log_warning("make_polylist not overwritten!")

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

    def Cross(self, xr, yr, wr, hr, lw):
        """adds a cross to the polylist"""
        sCross(xr, yr, wr, hr, lw, self.verts)

    def Dig(self, dig_key, xr, yr, wr, hr):
        """adds a digit to the polylist"""
        sDig(dig_key, xr, yr, wr, hr, self.verts)

    def WaferDig(self, wafer_type, x_dig, y_dig, xr, yr, wr, hr):
        sWaferDig(wafer_type, x_dig, y_dig, xr, yr, wr, hr, self.verts)


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

