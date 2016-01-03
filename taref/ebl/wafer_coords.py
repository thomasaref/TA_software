# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 12:51:22 2015

@author: thomasaref
"""
from atom.api import Enum, Int, Unicode, List, Float, Event, Atom, observe, cached_property
from enaml import imports
#from taref.core.log import log_debug
from taref.core.backbone import sqze

QUARTER_WAFER_SIGNS={"A" : (-1, 1), "B" : (1, 1), "C" : (-1, -1), "D" : (1, -1)}

def numCoords(Coords, lengthAA):
    """utility function that returns length of coords modulo? length of assign array"""
    return int(len(Coords)//lengthAA)
        
class SubWaferCoord(Atom):
    wafer_type=Enum("Full")
    diameter=Float(4).tag(unit="in", desc="wafer diameter in inches")
    chip_size=Int(5000).tag(desc="size of chip in microns", unit=" um")
    gap_size=Int(5000).tag(desc="gap from center of wafer", unit=" um")
    
    bad_coord_type=Enum("quarter wafer", "full wafer", "none")

    html_text2=Unicode().tag(log=False)

    distribute_event=Event()

    Px=Int(4000)
    Py=Int(40000)
    Qx=Int(40000)
    Qy=Int(4000)

    @cached_property    
    def x_offset(self):
        return 0
    
    @cached_property    
    def y_offset(self):
        return 0

    @cached_property    
    def N_chips(self):
        return 1

    @cached_property    
    def step_size(self):
        return 0

    @property
    def GLM(self):
        return [self.Px, self.Py, self.Qx, self.Qy]

    @property
    def view_window(self):
        with imports():
            from taref.ebl.wafer_coords_e import WaferCoordsView
        view=WaferCoordsView(wc=self)
        return view

class WaferCoords(SubWaferCoord):
    wafer_type=Enum("A", "B", "C", "D")
    
    @observe("wafer_type", "diameter", "chip_size", "gap_size", "bad_coord_type")
    def do_update(self, change):
        if change['type'] == 'update':
            self.get_member('x_mult').reset(self)
            self.get_member('y_mult').reset(self)
            self.get_member('radius').reset(self)
            self.get_member('x_offset').reset(self)
            self.get_member('y_offset').reset(self)
            self.get_member('N_chips').reset(self)
            self.get_member('step_size').reset(self)
            self.get_member('array').reset(self)
            self.get_member('wafer').reset(self)
            self.get_member('bad_coords').reset(self)
            self.get_member('good_coords').reset(self)
            self.get_member('html_text').reset(self)
        
    @property
    def GLM(self):
        return {"A" : [-self.Py,  self.Px, -self.Px,  self.Py],
                "B" : [ self.Px,  self.Py,  self.Py,  self.Px],
                "C" : [-self.Py, -self.Px, -self.Px, -self.Py],
                "D" : [ self.Px, -self.Py,  self.Py, -self.Px]}[self.wafer_type]        
    
    @property
    def xy_locations(self):
        return [(self.wafer_type, item[0], item[1],
                 self.x_offset+(item[0]-1)*self.chip_size,
                 self.y_offset-(item[1]-1)*self.chip_size) for item in self.wafer]

    @cached_property
    def x_mult(self):
        return QUARTER_WAFER_SIGNS[self.wafer_type][0]    

    @cached_property
    def y_mult(self):
        return QUARTER_WAFER_SIGNS[self.wafer_type][1]    

    @cached_property
    def radius(self):
        return int(self.diameter*25400/2)

    @cached_property
    def N_chips(self):
        return (self.radius-self.gap_size)/self.chip_size-1

    @cached_property
    def x_offset(self):  
        return self.x_mult*(self.gap_size+self.chip_size/2)-(self.N_chips-1)*(1-self.x_mult)/2*self.chip_size

    @cached_property    
    def y_offset(self):
        return self.y_mult*(self.gap_size+self.chip_size/2)+(self.N_chips-1)*(1+self.y_mult)/2*self.chip_size

    @cached_property    
    def step_size(self):
        return self.chip_size

    @cached_property
    def array(self):
        return [self.x_offset, self.N_chips, self.chip_size, self.y_offset, self.N_chips, self.chip_size]

    @cached_property
    def wafer(self):
        return [(x+1, y+1) for x in range(self.N_chips) for y in range(self.N_chips)
              if ((x+self.x_mult)*self.chip_size+self.x_offset)**2+((self.y_mult-y)*self.chip_size+self.y_offset)**2<=self.radius**2]

    @cached_property
    def bad_coords(self):
        if self.bad_coord_type=="quarter wafer":
            return [ item for item in self.wafer
                 if (item[0]+1, item[1]) not in self.wafer or (item[0]-1, item[1]) not in self.wafer
                 or (item[0], item[1]+1) not in self.wafer or (item[0], item[1]-1) not in self.wafer]
        elif self.bad_coord_type=="full wafer":
            return [ item for item in self.wafer
                     if (item[0]+self.x_mult, item[1]) not in self.wafer
                     or (item[0], item[1]-self.y_mult) not in self.wafer]
        return []
        
    @cached_property
    def good_coords(self):
        return [x for x in self.wafer if x not in self.bad_coords]

    def html_table_string(self, condition):
        tt=['\n<table border="1">']
        for y in range(self.N_chips): 
            tt.append('<tr>')
            for x in range(self.N_chips):
                tt.append('<td>')
                item=(x+1, y+1)
                tt.extend(condition(item))
                tt.append('</td>')
            tt.append('</tr>')
        tt.append("</table>")
        return "\n".join(tt)

    def badgood_condition(self, item):
        if item in self.wafer:
            if item in self.bad_coords:
                return ['<p style="color:red"> {0} </p>'.format(item)]
            if item in self.good_coords:
                return ['<p style="color:green"> {0} </p>'.format(item)]
        return []

    @cached_property
    def html_text(self):
        return self.html_table_string(self.badgood_condition)
   
    def distr_one_coord(self, i, num_skip, num_good_coords, num_bad_coords):
        """Distributes a single coordinate. used by distribute_coords"""
        templist=[self.bad_coords[n*num_skip+i] for n in range(num_bad_coords)]
        templist.extend([self.good_coords[m*num_skip+i] for m in range(num_good_coords)])
        leftover=len(self.bad_coords)-num_bad_coords*num_skip
        if num_bad_coords*num_skip+i<len(self.bad_coords):
            templist.append(self.bad_coords[(num_bad_coords)*num_skip+i])
        elif num_good_coords*num_skip-leftover+i<len(self.good_coords):
            templist.append(self.good_coords[num_good_coords*num_skip-leftover+i])
        if num_good_coords*num_skip-leftover+num_skip+i<len(self.good_coords):
            templist.append(self.good_coords[(num_good_coords+1)*num_skip-leftover+i])
        return templist
    
    def distribute_coords(self, num_patterns):
        """distributes num_patterns amongst good and bad coordinates as evenly as possible"""
        num_good_coords=numCoords(self.good_coords, num_patterns)
        num_bad_coords=numCoords(self.bad_coords, num_patterns)
        return [self.distr_one_coord(i, num_patterns, num_good_coords, num_bad_coords) for i in range(num_patterns)]
    
class FullWafer(SubWaferCoord):
    wafer_type=Enum("Full", "A", "B", "C", "D")
    quarter_wafers=List()

    @property
    def xy_locations(self):
        t_list=[]
        for qw in self.quarter_wafers:
            t_list.extend(qw.xy_locations)
        return t_list    
        
    @observe("wafer_type", "diameter", "chip_size", "gap_size", "bad_coord_type")
    def do_update(self, change):
        if change['type'] == 'update':
            if change["name"]=="wafer_type":
                if self.wafer_type!="Full":
                    self.quarter_wafers=[WaferCoords(wafer_type=self.wafer_type,
                                                 diameter=self.diameter, chip_size=self.chip_size,
                                                 gap_size=self.gap_size, bad_coord_type=self.bad_coord_type)]
                else:
                    self.quarter_wafers=self._default_quarter_wafers()
            else:
                for item in self.quarter_wafers:
                    item.diameter=self.diameter
                    item.chip_size=self.chip_size
                    item.gap_size=self.gap_size
                    item.bad_coord_type=self.bad_coord_type
            self.get_member('N_chips').reset(self)
            self.get_member('html_text').reset(self)
         
    def _default_quarter_wafers(self):
        return [WaferCoords(wafer_type="A", diameter=self.diameter, chip_size=self.chip_size,
                gap_size=self.gap_size, bad_coord_type=self.bad_coord_type),
                WaferCoords(wafer_type="B", diameter=self.diameter, chip_size=self.chip_size,
                gap_size=self.gap_size, bad_coord_type=self.bad_coord_type),
                WaferCoords(wafer_type="C", diameter=self.diameter, chip_size=self.chip_size,
                gap_size=self.gap_size, bad_coord_type=self.bad_coord_type),
                WaferCoords(wafer_type="D", diameter=self.diameter, chip_size=self.chip_size,
                gap_size=self.gap_size, bad_coord_type=self.bad_coord_type)]


    @cached_property    
    def N_chips(self):
        if self.wafer_type=="Full":
            return 1
        return self.quarter_wafers[0].N_chips
        
    def html_table_string(self, condition):
        if self.wafer_type=="Full":
            tt=['<table border="1">']
            tT=[]
            tB=[]
            for y in range(self.quarter_wafers[0].N_chips):
                tT.append('<tr>')
                tB.append('<tr>')
                tt_list=[[], [], [],[]]
                for x in range(self.quarter_wafers[0].N_chips):
                    item=(x+1, y+1)
                    for n, tp in enumerate(tt_list):
                        tp.extend(sqze([['<td>'], condition(item, n), ['</td>']]))
                tT.extend(tt_list[0])
                if self.quarter_wafers[0].gap_size>0:
                    tT.append("<td></td>")
                if self.quarter_wafers[1].gap_size>0:
                    tT.append("<td></td>")
                tT.extend(tt_list[1])
                tT.append('</tr>')
    
                tB.extend(tt_list[2])
                if self.quarter_wafers[2].gap_size>0:
                    tB.append("<td></td>")
                if self.quarter_wafers[3].gap_size>0:
                    tB.append("<td></td>")
                tB.extend(tt_list[3])
                tB.append('</tr>')
            tt.extend(tT)
            if self.quarter_wafers[0].gap_size>0:
                tt.append("<tr></tr>")
            if self.quarter_wafers[2].gap_size>0:
                tt.append("<tr></tr>")
            tt.extend(tB)
            tt.append("</table>")
            return "\n".join(tt)
        return self.quarter_wafers[0].html_table_string(condition)

    def badgood_condition(self, item, n=0):
        return self.quarter_wafers[n].badgood_condition(item)

    @cached_property
    def html_text(self):
        return self.html_table_string(self.badgood_condition)

    def distribute_coords(self, num_patterns):
        if self.wafer_type!="Full":
            return self.quarter_wafers[0].distribute_coords(num_patterns)
        return sqze(qw.distribute_coords(num_patterns) for qw in self.quarter_wafers)

if __name__=="__main__":
    from taref.core.shower import show

    if 0:
        #a=SubWaferCoord()
        a=WaferCoords()
        print a.xy_locations
        #print a.wafer
        #print a.distribute_coords(5)        
        show(a)#a.show()
         
    a=FullWafer()
    print a.xy_locations
    print a.distribute_coords(5)        
    
    #a.html=a.html_txt()
    show(a)
        
