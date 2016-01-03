# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 10:46:56 2015

@author: thomasaref
"""

from taref.ebl.wafer_coords import FullWafer
from atom.api import Typed, Unicode, Atom, List, Coerced, observe
from taref.core.log import log_debug
from taref.core.shower import show
from taref.core.backbone import set_attr, get_tag, sqze
from enaml import imports
from re import compile as compiler
    
P_FINDER=compiler("P\((\d+)\)")
def find_P_nums(key):
    """utility function for extracting all P numbers from key"""
    return [int(p) for p in P_FINDER.findall(key)]

A_FINDER=compiler("A\((\d+)\)")
def find_A_nums(key):
    """utility function for extracting all A numbers from key"""
    return [int(a) for a in A_FINDER.findall(key)]

SEPARATOR=";"
def format_comment(comment, sep=SEPARATOR, fmt_str=" {0} {1}"):
    """utility function for including or not including a comment"""
    if comment!="":
        return fmt_str.format(sep, comment)
    return comment

def parse_comment(line, sep=SEPARATOR):
    """utility function that strips a text line of its comment and 
    returns both the line and comment without padding spaces."""
    tempstr, sep, comment=line.partition(sep)
    tempstr=tempstr.strip()
    comment=comment.strip()
    return tempstr, comment

def xy_string_split(tempstr):
    """utility function that processes a string list of tuples into a list"""
    return tempstr.split("(")[1].split(")")[0].split(",")+tempstr.split("(")[2].split(")")[0].split(",")

def tuple_split(tempstr):
    """utility function that processes a text tuple into a numeric list"""
    return tempstr.split("(")[1].split(")")[0].split(",")

class JDF_Assign(Atom):
    """describes a jdf assign statement. defaults to a single pattern P(1) at position 1,1"""
    assign_type=List(default=['P(1)']).tag(desc="list of assigns")
    pos_assign=List(default=[(1,1),]).tag(desc="list of tuples of position")
    shot_assign=Unicode().tag(desc="shot mod table name")
    comment=Unicode().tag(desc="comment on assign")
    short_name=Unicode().tag(desc="short name used for display in html table")
    
    def dup_assign(self):
        """duplicates assign as separate object using string parsing functionality"""
        dup_str, dup_comment=parse_comment(self.jdf_output)
        return JDF_Assign(tempstr=dup_str, comment=dup_comment)
        
    @property
    def A_nums(self):
        """all A numbers in assign_type"""
        return find_A_nums(self.assign_str)

    @property
    def P_nums(self):
        """all P numbers in assign_type"""
        return find_P_nums(self.assign_str)

    def _default_pos_assign(self):
        return [(1,1)]
        
    def _default_short_name(self):
        return self.comment.split(" ")[0]
        
    def xy_offset(self, x_start, x_step, y_start, y_step):
        return [(x_start+(p[0]-1)*x_step, y_start+(p[1]-1)*y_step) for p in self.pos_assign]

    @property
    def assign_str(self):
        """utility combination of assign_type list as string"""
        return "+".join(self.assign_type)

    @property
    def jdf_output(self):
        """produces output string for jdf"""
        pos_asgn=""
        for pos in self.pos_assign:
            pos_asgn+="({x},{y}),".format(x=pos[0], y=pos[1])
        pos_asgn=pos_asgn[:-1]
        shot_asgn=format_comment(self.shot_assign, sep=",", fmt_str="{0} {1}")
        asgn_comment=format_comment(self.comment)
        return "\tASSIGN {asgn_type} -> ({pos_asgn}{shot_asgn}) {asgn_comment}".format(
                  asgn_type=self.assign_str, pos_asgn=pos_asgn, shot_asgn=shot_asgn, asgn_comment=asgn_comment)

    def __init__(self, **kwargs):
        """Processes kwargs to allow string definition to be passes as well"""
        tempstr=kwargs.pop("tempstr", "ASSIGN P(1) -> ((1,1))")
        kwargs["comment"]=kwargs.get("comment", "")
        assign_type=kwargs.get("assign_type", tempstr.split("ASSIGN")[1].split("->")[0].strip().split("+"))
        kwargs["assign_type"]=[unicode(at) for at in assign_type]
        kwargs["pos_assign"]=kwargs.get("pos_assign", [])
        kwargs["shot_assign"]=kwargs.get("shot_assign", "")
        if kwargs["pos_assign"]==[]:
            for item in tempstr.split("->")[1].partition("(")[2].rpartition(")")[0].split(")"):
                if "(" in item:
                    xcor, ycor=item.split("(")[1].split(",")
                    kwargs["pos_assign"].append((int(xcor), int(ycor)))
                elif "," in item:
                    kwargs["shot_assign"]=unicode(item.split(",")[1].strip())
        super(JDF_Assign, self).__init__(**kwargs)
        
class JDF_Array(Atom):
    """describes a jdf array. defaults to an array centered at 0,0 with one item.
    array_num=0 corresponds to the main array"""
    array_num=Coerced(int)
    x_start=Coerced(int)
    x_num=Coerced(int, (1,))
    x_step=Coerced(int)
    y_start=Coerced(int)
    y_num=Coerced(int, (1,)) 
    y_step=Coerced(int) 
    assigns=List()
    comment=Unicode()

    def xy_offset(self, index=0):
        return self.assigns[index].xy_offset(self.x_start, self.x_step, self.y_start, self.y_step)
        
    def _default_assigns(self):
        return []
        
    @property
    def jdf_output(self):
        array_comment=format_comment(self.comment)
        tl=["{arr_num}: ARRAY ({x_start}, {x_num}, {x_step})/({y_start}, {y_num}, {y_step}){arr_com}".format(
               arr_num=self.array_num, x_start=self.x_start, x_num=self.x_num, x_step=self.x_step, 
               y_start=self.y_start, y_num=self.y_num, y_step=self.y_step, arr_com=array_comment)]
        tl.extend([asg.jdf_output for asg in self.assigns])
        tl.append("AEND\n")
        return tl

    def add_assign(self, tempstr, comment):
        self.assigns.append(JDF_Assign(tempstr=tempstr, comment=comment))#
    
    def __init__(self, **kwargs):
        """Processes kwargs to allow string definition to be passes as well"""
        tempstr=kwargs.pop("tempstr", "")
        if tempstr=="":
            super(JDF_Array, self).__init__(**kwargs)
        else:
            comment=kwargs.get("comment", "")
            if ":" in tempstr:
                array_num=kwargs.get("array_num", tempstr.split(":")[0])
            else:
                array_num=0
            x_start, x_num, x_step, y_start, y_num, y_step=xy_string_split(tempstr)
            super(JDF_Array, self).__init__(array_num=array_num, x_start=x_start,
                 x_num=x_num, x_step=x_step, y_start=y_start, y_num=y_num, y_step=y_step, comment=comment)
        
class JDF_Main_Array(JDF_Array):
    """adds the marker locations for the main jdf array"""
    M1x=Coerced(int, (1500,))
    M1y=Coerced(int, (1500,))
    
    @property
    def jdf_output(self):
        array_comment=format_comment(self.comment)
        tl=["ARRAY ({x_start}, {x_num}, {x_step})/({y_start}, {y_num}, {y_step}){arr_com}".format(
                x_start=self.x_start, x_num=self.x_num, x_step=self.x_step, 
               y_start=self.y_start, y_num=self.y_num, y_step=self.y_step, arr_com=array_comment)]
        tl.append("\tCHMPOS M1=({M1x}, {M1y})".format(M1x=self.M1x, M1y=self.M1y))
        tl.extend([asg.jdf_output for asg in self.assigns])
        tl.append("AEND\n")
        return tl

class JDF_Pattern(Atom):
    """describes a jdf pattern. has a number, location and name of file"""
    num=Coerced(int) 
    x=Coerced(float) 
    y=Coerced(float) 
    name=Unicode()
    comment=Unicode()
    
    @property
    def xy_offset(self):
        return (self.x, self.y)

    @property
    def jdf_output(self):
        comment=format_comment(self.comment)
        return "P({pnum}) '{pname}.v30' ({px},{py}){com}".format(
             pnum=self.num, pname=self.name, px=self.x, py=self.y, com=comment)

    def __init__(self, **kwargs):
        """Processes kwargs to allow string definition to be passed as well"""
        tempstr=kwargs.pop("tempstr", "P(1)''.v30 (0,0)")

        kwargs["comment"]=kwargs.get("comment", "")
        kwargs["name"]=kwargs.get("name", tempstr.split("'")[1].split(".")[0])
        kwargs["num"]=kwargs.get("num", tempstr.split("(")[1].split(")")[0])
        kwargs["x"]=kwargs.get("x", tempstr.split("(")[2].split(")")[0].split(",")[0])
        kwargs["y"]=kwargs.get("y", tempstr.split("(")[2].split(")")[0].split(",")[1])
        super(JDF_Pattern, self).__init__(**kwargs)
        
class JDF_Top(Atom):
    """Top class that controls distribution of patterns into JDF"""
    wafer_coords=Typed(FullWafer)

    @property
    def xy_offsets(self):
        """recursive traces down locations of all patterns"""
        overall_dict={}
        for pd in [self.p_off_recur(m_arr, p_off={}) for m_arr in self.main_arrays]:
            for key in pd:
                overall_dict[key]=overall_dict.get(key, [])+pd[key]
        return overall_dict

    def p_off_recur(self, p_arr, x_off_in=0, y_off_in=0, p_off={}):
        """recursive search function for pattern locations"""
        for a in p_arr.assigns:
            for pa in a.pos_assign:
                x_off=x_off_in+p_arr.x_start+(pa[0]-1)*p_arr.x_step
                y_off=y_off_in+p_arr.y_start-(pa[1]-1)*p_arr.y_step
                for p in [pattern for pattern in self.patterns if pattern.num in a.P_nums]:
                    if p.name not in p_off:
                        p_off[p.name]=[]
                    p_off[p.name].append((x_off+p.x, y_off+p.y))
                for arr in [array for array in self.sub_arrays if array.array_num in a.A_nums]:
                    self.p_off_recur(arr, x_off, y_off, p_off)
        return p_off

    def assign_condition(self, item, n=0):
        return [assign.short_name for assign in self.main_arrays[n].assigns if item in assign.pos_assign]
        
    @observe("wafer_coords.distribute_event")
    def observe_distrib_event(self, change):
        #self.distribute_coords()
        #self.wafer_coords.html_text2=self.wafer_coords.html_table_string(self.assign_condition)
        print self.xy_offsets
        
    @property
    def view_window(self):
        with imports():
            from taref.ebl.jdf_e import JDF_View
        return JDF_View(jdf=self)

    def _default_wafer_coords(self):
        return FullWafer()
            
    def set_valcom(self, name, value, comment=""):
        """utility function for setting a comment while setting value"""        
        set_attr(self, name, value, comment=comment)

    def append_valcom(self, inlist, name, fmt_str="{0}{1}", sep=";"):
            comment=format_comment(get_tag(self, name, "comment", ""))
            value=getattr(self, name)
            inlist.append(fmt_str.format(value, comment))

    @property
    def arrays(self):
        return sqze(self.main_arrays, self.sub_arrays)
        
    def distribute_coords(self, num=None):
        """distribute coords using wafer_coords object"""
        self.comments=["distributed main array for quarter wafer {}".format(self.wafer_coords.wafer_type)]
        self.Px, self.Py, self.Qx, self.Qy=self.wafer_coords.GLM
        
        assigns=[assign.dup_assign() for assign in self.main_arrays[0].assigns]
        self.main_arrays=self._default_main_arrays()
        for arr in self.main_arrays:
            arr.assigns=[assign.dup_assign() for assign in assigns]
            
        if num is None:
            num=len(self.patterns)
        for m, qw in enumerate(self.wafer_coords.quarter_wafers):
            for n, c in enumerate(qw.distribute_coords(num)):
                self.main_arrays[m].assigns[n].pos_assign=c[:]
            self.main_arrays[m].x_start=qw.x_offset
            self.main_arrays[m].x_num=qw.N_chips
            self.main_arrays[m].x_step=qw.step_size
    
            self.main_arrays[m].y_start=qw.y_offset
            self.main_arrays[m].y_num=qw.N_chips
            self.main_arrays[m].y_step=qw.step_size

        self.output_jdf=self.jdf_produce()
        self.input_jdf=self.output_jdf

    input_jdf=Unicode()
    output_jdf=Unicode()
    comments=List() 

    Px=Coerced(int, (-40000,)).tag(desc="X coordinate of global P mark")
    Py=Coerced(int, (4000,)).tag(desc="Y coordinate of global P mark")
    Qx=Coerced(int, (-4000,))
    Qy=Coerced(int, (40000,))

    mgn_name=Unicode("IDT")
    wafer_diameter=Coerced(int, (4,))
    write_diameter=Coerced(float, (-4.2,))

    stdcur=Coerced(int, (2,)).tag(desc="Current to use in nA")
    shot=Coerced(int, (8,)).tag(desc="Shot size in nm. should divide 4 um evenly")
    resist=Coerced(int, (165,)).tag(desc="dose")
    resist_comment=Unicode()
    main_arrays=List().tag(desc="main arrays in JDF")
    sub_arrays=List().tag(desc="arrays in JDF")#.tag(width='max', inside_type=jdf_array)
    patterns=List().tag(desc="patterns in JDF")#.tag(width='max', inside_type=jdf_pattern)
    jdis=List().tag(desc="jdis in JDF")

    def _default_main_arrays(self):
        if self.wafer_coords.wafer_type=="Full":
            return [JDF_Main_Array(), JDF_Main_Array(), JDF_Main_Array(), JDF_Main_Array()]
        return [JDF_Main_Array()]

    def _observe_input_jdf(self, change):
        self.jdf_parse(self.input_jdf)
        self.output_jdf=self.jdf_produce()
    
    def clear_JDF(self):
        self.comments=[]
        self.main_arrays=[]
        self.sub_arrays=[]
        self.patterns=[]
        self.jdis=[]

    def add_pattern(self, tempstr, comment):
        self.patterns.append(JDF_Pattern(tempstr=tempstr, comment=comment))

    def add_array(self, tempstr, comment):
        if ":" in tempstr:
            array=JDF_Array(tempstr=tempstr, comment=comment)
            self.sub_arrays.append(array)
        else:
            array=JDF_Main_Array(tempstr=tempstr, comment=comment)
            self.main_arrays.append(array)
        return array
            
        
    def jdf_parse(self, jdf_data):
        """reads a jdf text and puts the data into objects"""
        jdf_list=jdf_data.split("\n")
        inside_path=False
        inside_layer=False
        self.clear_JDF()
        for n, line in enumerate(jdf_list):
            tempstr, comment=parse_comment(line)
            if tempstr=="" and comment!="":
                self.comments.append(comment)
            if tempstr.startswith('GLMPOS'):
                self.Px, self.Py, self.Qx, self.Qy=xy_string_split(tempstr) 
            elif tempstr.startswith('JOB'):
                mgn_name, self.wafer_diameter, self.write_diameter=tempstr.split(",") 
                self.mgn_name=mgn_name.split("'")[1].strip()
            elif tempstr.startswith("PATH"):
                inside_path=True
            elif "LAYER" in tempstr:
                inside_layer=True
            if inside_path:
                if 'ARRAY' in tempstr:
                    array=self.add_array(tempstr, comment)
                elif 'ASSIGN' in tempstr:
                    array.add_assign(tempstr, comment)
                elif 'CHMPOS' in tempstr:
                    M1x, M1y=tuple_split(tempstr)
                    if len(self.main_arrays)>0:
                        self.main_arrays[-1].M1x=M1x
                        self.main_arrays[-1].M1y=M1y
                elif "PEND" in tempstr:
                    inside_path=False
            elif inside_layer:
                if 'END' in tempstr:
                    inside_layer=False
                elif 'STDCUR' in tempstr:
                    self.set_valcom("stdcur", tempstr.split("STDCUR")[1], comment)
                elif 'SHOT' in tempstr:
                    self.set_valcom("shot", tempstr.split(',')[1], comment)
                elif 'RESIST' in tempstr:
                    self.set_valcom("resist", tempstr.split('RESIST')[1], comment)
                elif 'P(' in tempstr:
                    self.add_pattern(tempstr, comment)
                elif tempstr.startswith('@'):
                    jdi_str=tempstr.split("'")[1].split(".jdi")[0]
                    self.jdis.append(jdi_str)
                        
    def jdf_produce(self):
        """produces a jdf from the data stored in the object"""
        jl=[]
        jl.append("JOB/W '{name}', {waf_diam}, {write_diam}\n".format(name=self.mgn_name,
                  waf_diam=self.wafer_diameter, write_diam=self.write_diameter))
        if len(self.comments)>0:
            jl.append(";{comment}\n".format(comment=self.comments[0]))
        jl.append("GLMPOS P=({Px}, {Py}), Q=({Qx},{Qy})".format(Px=self.Px, Py=self.Py, Qx=self.Qx, Qy=self.Qy))
        jl.append("PATH")

        for n, item in enumerate(self.arrays):
            jl.extend(item.jdf_output)
        jl.append("PEND\n\nLAYER 1")

        for n, item in enumerate(self.patterns):
            jl.append(item.jdf_output)

        self.append_valcom(jl, "stdcur", "\nSTDCUR {0}{1}")
        self.append_valcom(jl, "shot", "SHOT A, {0}{1}")
        self.append_valcom(jl, "resist", "RESIST {0}{1}\n")
        
        for item in self.jdis:
            jl.append("@ '{jdi_name}.jdi'".format(jdi_name=item))
        jl.append("\nEND 1\n")
        
        if len(self.comments)>1:
            for item in self.comments[1:]:
                jl.append(";{}".format(item))
                
        return "\n".join(jl)

def jdf_parse(jdf_data):
    """returns a JDF_Top object with the data given in jdf_data"""
    jdf=JDF_Top()
    jdf.jdf_parse(jdf_data)
    return jdf
    
def jdf_qw_swap(jdf_data, qw="A", num=None):
    jdf=jdf_parse(jdf_data)
    jdf.quarter_wafer=qw
    jdf.distribute_coords(num=num)
    return jdf.jdf_produce()
    
def gen_jdf_quarter_wafer(patterns, qw="A"):
    """guesses at jdf from list of patterns. patterns is a dictionary with an optional shot_mod and an optional position list?"""
    jdf=JDF_Top(quarter_wafer=qw)
    jdf.arrays.append(JDF_Main_Array())                                                        
    for n,p in enumerate(patterns):
        jdf.patterns.append(JDF_Pattern(num=n+1, name=p))
        jdf.jdis.append(p)
        jdf.arrays.append(JDF_Array(array_num=n+1,
                                    assigns=[JDF_Assign(assign_type=['P({0})'.format(n+1)],
                                                        shot_assign=patterns[p].get("shot_mod", ""),
                                                        #pos_assign=patterns[p].get("pos", [(1,1)])
                                                        assign_comment=p)]))
        jdf.arrays[0].assigns.append(JDF_Assign(assign_type=['A({0})'.format(n+1)],
                                             assign_comment=p))
    jdf.distribute_coords()
    return jdf
    



if __name__=="__main__":
    a=JDF_Top()
    jdf_data="""JOB/W 'IDT',4,-4.2

; For exposure on YZ-cut LiNbO3, Cop+ZEP., q-wafer D
GLMPOS P=(4000,-40000),Q=(40000,-4000)   ;D wafer
PATH
ARRAY (7500,8,5000)/(-7500,8,5000)  ; D wafer
        CHMPOS M1=(1500, 1500)

	ASSIGN A(1)+A(2)+A(15)  ->  ((1,1), (7,2), (6,4)) ;D32080 with two IDTs and Squid connect
	ASSIGN A(1)+A(3)+A(15)  ->  ((2,1), (8,2), (7,4)) ;S32080 with two IDTs and Squid connect
	ASSIGN A(1)+A(4)+A(15)  ->  ((3,1), (1,3), (1,5), (2,7)) ;S32050 with two IDTs and Squid connect
	ASSIGN A(1)+A(5)+A(15)  ->  ((4,1), (2,3), (2,5), (3,7))  ;D32050 with two IDTs and Squid connect
	ASSIGN A(1)+A(6)+A(15)  ->  ((5,1), (3,3), (3,5), (4,7)) ;D9050 with two IDTs and Squid connect
	ASSIGN A(1)+A(7)+A(15)  ->  ((6,1), (4,3), (4,5), (1,8))  ;S9050 with two IDTs and Squid connect
	ASSIGN A(1)+A(8)+A(15)  ->  ((7,1), (5,3), (5,5))  ;S9080 with two IDTs and Squid connect
	ASSIGN A(1)+A(9)+A(15)  ->  ((8,1), (6,3), (6,5), (2,8))  ;D9080 with two IDTs and Squid connect
	ASSIGN A(12)+A(10)+A(15) -> ((1,2),  (7,3), (1,6)) ;D5080 with two FDTs and Squid connect
        ASSIGN A(12)+A(11)+A(15) ->  ((2,2), (1,4), (2,6))   ;D5096 with two FDTs and Squid connect
        ASSIGN A(13)+A(15)       ->  ((3,2), (2,4), (3,6))   ;IDT by itself
        ASSIGN A(14)+A(15)       ->  ((4,2), (3,4), (4,6))         ;FDT by itself
	ASSIGN A(1)+A(15)        -> ((5,2), (4,4), (5,6))     ;Two IDTs alone with squid connect
	ASSIGN A(12)+A(15)       -> ((6,2), (5,4), (1,7))          ;two FDTs alone with squid connect


AEND

1: ARRAY (-200, 2, 500)/(0, 1, 0)
	ASSIGN P(1) -> ((1,1), IDT2)
	ASSIGN P(1) -> ((2,1), IDT2)
AEND

2: ARRAY (0,1,0)/(0,1,0)
	ASSIGN P(2) -> ((1,1), D32080)
AEND

3: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(3) -> ((1,1), S32080)
AEND

4: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(4) -> ((1,1), S32050)
AEND

5: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(5) -> ((1,1), D32050)
AEND

6: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(6) -> ((1,1), D9050)
AEND

7: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(7) -> ((1,1), S9050)
AEND

8: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(8) -> ((1,1), S9080)
AEND

9: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(9) -> ((1,1), D9080)
AEND

10: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(10) -> ((1,1), D5080)
AEND

11: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(11) -> ((1,1), SCB2)
AEND

12: ARRAY (-200, 2, 500)/(0, 1, 0)
	ASSIGN P(12) -> ((1,1), FDT2)
	ASSIGN P(12) -> ((2,1), FDT2)
AEND

13: ARRAY (-200, 2, 500)/(0, 1, 0)
	ASSIGN P(1) -> ((1,1), IDT2)
AEND

14: ARRAY (-200, 2, 500)/(0, 1, 0)
	ASSIGN P(12) -> ((1,1), FDT2)
AEND

15: ARRAY (-500, 2, 1000)/(-1500, 1, 0)
	ASSIGN P(13) -> ((1,1), QBRI)
	ASSIGN P(14) -> ((2,1), QBR3)
AEND
PEND

LAYER 1
   P(1) 'cIDT9bd36ef0w96wb0.v30' (0,0)
   P(2) 'cQDT9bd3ef20w80wb0.v30' (0,0)
   P(3) 'cQDT9bs3ef20w80wb0.v30' (0,0)
   P(4) 'cQDT9bs3ef20w50wb0.v30' (0,0)
   P(5) 'cQDT9bd3ef20w50wb0.v30' (0,0)
   P(6) 'cQDT9bd9ef0w50wb0.v30' (0,0)
   P(7) 'cQDT9bs9ef0w50wb0.v30' (0,0)
   P(8) 'cQDT9bs9ef0w80wb0.v30' (0,0)
   P(9) 'cQDT9bd9ef0w80wb0.v30' (0,0)
   P(10) 'cQDT9bd5ef0w80wb0.v30' (0,0)
   P(11) 'cQDT9bd5ef0w96wb0.v30' (0,0)
   P(12) 'cIDT9bd55ef0w96wb0.v30' (0,0)

   P(13) 'cQbri.v30' (0,0)
   P(14) 'cQbr3.v30' (0,0)
   ;SPPRM 3.996,,,1,1 ;use if SHOT is 6 nm (doesn't divide 4 um which is default)
   STDCUR 2
   SHOT A,8
   RESIST 165 ; new dose from dose test TA020315A_dt with modified bias from TA060315B

@ 'idt_s.jdi'
@ 'cQDT9bd3ef20w80wb0.jdi'
@ 'cQDT9bs3ef20w80wb0.jdi'
@ 'cQDT9bs3ef20w50wb0.jdi'
@ 'cQDT9bd3ef20w50wb0.jdi'
@ 'cQDT9bd9ef0w50wb0.jdi'
@ 'cQDT9bs9ef0w50wb0.jdi'
@ 'cQDT9bs9ef0w80wb0.jdi'
@ 'cQDT9bd9ef0w80wb0.jdi'
@ 'cQDT9bd5ef0w80wb0.jdi'
@ 'scb_s.jdi'
@ 'fdt_s.jdi'
@ 'cQbri.jdi'
@ 'cQbr3.jdi'

END 1"""

    jdf_data="""PATH
ARRAY (-42500, 8, 5000)/(42500, 8, 5000)
	CHMPOS M1=(1500, 1500)
	ASSIGN A(1) -> ((1,1),(1,8),(8,8))  ; D32080 with two IDTs and Squid connect
AEND

1: ARRAY (-200, 2, 500)/(0, 1, 0)
	ASSIGN P(1) -> ((1,1), IDT2) 
	ASSIGN P(1) -> ((2,1), IDT2) 
AEND

2: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(2) -> ((1,1), D32080) 
AEND

3: ARRAY (0, 1, 0)/(0, 1, 0)
	ASSIGN P(3) -> ((1,1), S32080) 
AEND

PEND

LAYER 1
P(1) 'cIDT9bd36ef0w96wb0.v30' (0.0,0.0)
P(2) 'cQDT9bd3ef20w80wb0.v30' (0.0,0.0)
P(3) 'cQDT9bs3ef20w80wb0.v30' (0,0)
"""
    a.input_jdf=jdf_data
    #print a.arrays[0].assigns[0].pos_assign
    show(a, a.wafer_coords)
    #print a.arrays[0].assigns[0].pos_assign
    
    #a=Text_Editor(name="Text_Editor", dir_path="/Volumes/aref/jbx9300/job/TA150515B/IDTs", main_file="idt.jdf")
    
    #class Pattern(Atom):
    #    name=Unicode()
    #    shot_mod=Unicode()
        
    #b=gen_jdf_quarter_wafer(dict(IDT={"shot_mod":"IDT1"}, QDT={}), "B")    
    #print b.jdf_produce()
    #b=JDF_Top(text=jdf_data)#_base()
    #b.do_plot()
    #b.jdf_parse(jdf_data)
    #print b.Px, b.Py, b.Qx, b.Qy
    #print b.arrays[0].assigns
    #print b.patterns[0].name

    #b.arrays.extend((jdf_array(), jdf_array(x_start=5), jdf_array(x_start=5), jdf_array(x_start=5)))
    #a.read_file.read()
    #print a.data
    #b.jdf_parse(a.data)
    #c=Base()
    #a.jdf.arrays.append(4.5)
    #a.jdf.arrays.append(4)

    #print a.Px
    #print [a.get_tag(aa, 'label', aa) for aa in a.all_params]
    #print a.jdf_list
    #print b.get_member('arrays').item.validate_mode[1]
    #show(b)
#    b.show()
    #print a.data
    #print b.jdf_produce()
    #print a.jdf_save_file.file_path
#/Volumes/aref/jbx9300/job/TA150515B/IDTs