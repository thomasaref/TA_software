# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:52:31 2015

@author: thomasaref
"""
from taref.core.log import log_debug

from atom.api import Enum, List, Unicode, Typed, Bool, observe
from taref.core.agent import Operative
from taref.core.api import private_property, reset_properties, reset_property
from taref.filer.save_file import Save_DXF
from taref.ebl.beamer_gen import BeamerGen
from taref.ebl.polygon_backbone import (minx, maxx, miny, maxy, sP, sPoly,
                                        sR, sC, sT, sCT, sCross, sDig, sWaferDig)
from taref.ebl.jdf import JDF_Top
from taref.plotter.plotter import Plotter
from taref.ebl.DXF_functions import save_dxf
from taref.core.shower import shower


class EBL_Polygons(Operative):
    base_name="EBL_Polygons"
    initial_position=(0,300)

    color=Enum("green", "blue", "red", "purple", "brown", "black").tag(desc="color or datatype of item, could be used for dosing possibly")
    layer=Enum("Al", "Al_35nA", "Au").tag(desc='layer of item')
    save_file=Typed(Save_DXF, ()).tag(no_spacer=True)
    name_sug=Unicode().tag(no_spacer=True)
    shot_mod_table=Unicode()
    bmr=Typed(BeamerGen).tag(private=True)
    plot_sep=Bool(True)
    verts=List(default=[]).tag(private=True)

    jdf=JDF_Top()

    plot=Plotter(name="EBL Plot", xlabel="x (um)", ylabel="y (um)", title="EBL Plot")

    def show(self):
        if self.jdf.input_jdf=="":
            self.jdf.gen_jdf([agent for agent in self.agent_dict.values() if isinstance(agent, EBL_Polygons)])
        self.plot_JDF()

        shower(self, self.plot)

    @property
    def cls_run_funcs(self):
        return [self.plot_JDF, self.save_JDF_DXF]

#    @classmethod
#    def activated(cls):
#        print "hello"
#        if cls.jdf.input_jdf=="":
#            cls.jdf.gen_jdf([agent for agent in cls.agent_dict.values() if isinstance(agent, EBL_Polygons)])
#        cls.plot_JDF()

    @classmethod
    def plot_JDF(cls):
        xmin=minx([])
        xmax=maxx([])
        ymin=miny([])
        ymax=maxy([])
        cls.jdf.get_member("xy_offsets").reset(cls.jdf)
        xy_off=cls.jdf.xy_offsets
        log_debug(2)
        for p in cls.jdf.patterns:
            a=cls.agent_dict[p.name]
            reset_properties(a) #fix updating of properties
            reset_property(a, "polylist")
            log_debug(a)
            verts=[]
            for chip in xy_off.get(p.name, []):
                sPoly(a, x_off=chip[0]*1.0e-6, y_off=chip[1]*1.0e-6, vs=verts)
            log_debug(a)
            pf=cls.plot.plot_dict.get(a.name+"_plot", None)
            if pf is None:
                cls.plot.polygon(verts, color=a.color, plot_name=a.name+"_plot")
            else:
                pf.alter_xy(verts, color=a.color)
            log_debug(a)
            xmin=min([minx(verts), xmin])
            xmax=max([maxx(verts), xmax])
            ymin=min([miny(verts), ymin])
            ymax=max([maxy(verts), ymax])
        log_debug(1)
        cls.plot.set_xlim(xmin, xmax)
        cls.plot.set_ylim(ymin, ymax)
        cls.plot.draw()

    @classmethod
    def save_JDF_DXF(cls):
        cls.jdf.get_member("xy_offsets").reset(cls.jdf)
        xy_off=cls.jdf.xy_offsets
        verts=[]
        for p in cls.jdf.patterns:
            a=cls.agent_dict[p.name] #[agent for agent in self.agents if agent.name==p.name][0]
            for chip in xy_off.get(p.name, []):
                sPoly(a, x_off=chip[0]*1.0e-6, y_off=chip[1]*1.0e-6, vs=verts)
        save_dxf(verts, color="green", layer="PADS", file_path="marialasertest.dxf", write_mode="w")

    def add_to_jdf(self):
        self.chief.patterns[self.name_sug]={"shot_mod":self.shot_mod_table}

    def make_name_sug(self):
        name_sug=""
        self.name_sug=name_sug

    def full_EBL_save(self, dir_path="""/Users/thomasaref/Dropbox/Current stuff/TA_software/discard/S2015_06_22_180739/"""):
        self.make_name_sug()
        file_path=dir_path+self.name_sug+".dxf"
        self.save_file.direct_save(self.polylist[:], self.color, self.layer, file_path=file_path, write_mode='w')
        self.bmr=BeamerGen(file_name=self.name_sug, mod_table_name = self.shot_mod_table, bias=-0.009, base_path=dir_path,
                           extentLLy=-150, extentURy=150)
        self.bmr.gen_flow()
        self.add_to_jdf()

    @observe('save_file.save_event')
    def obs_save_event(self, change):
        self.save_file.direct_save(self.verts[:], self.color, self.layer, write_mode='w')

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

    @private_property
    def polylist(self):
        """example polylist. to be overwritten in child classes
        In general, self.verts should be cleared first i.e. self.verts=[] but this case is
        interesting for testing out functions"""
        #self.verts=[]
        return self.verts

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
    a.Dig("8", 0, 0, 10.0e-6, 1.0e-6)
    a.Dig("B", 30.0e-6, 0, 10.0e-6, 1.0e-6)

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

