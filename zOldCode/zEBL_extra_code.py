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
