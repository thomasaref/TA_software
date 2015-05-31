# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:38:47 2015

@author: thomasaref

A simple text editor driver allowing one to load, edit and save text files
"""

from Atom_Base import Base
from atom.api import Str, observe, Unicode, Typed, ContainerList, Int, Float, Bool, List, Atom, Coerced, Instance
from Atom_Read_File import Read_TXT
from Atom_Save_File import Save_TXT
#from LOG_functions import log_info, log_debug, make_log_file, log_warning

class Text_Editor(Base):
    main_file=Unicode("idt.jdf").tag(private=True)
    dir_path=Unicode("/Users/thomasaref/Dropbox/Current stuff/TA_software").tag(private=True)
    data=Str().tag(discard=True, log=False, width="max", label="")
    read_file=Typed(Read_TXT).tag(width="max")
    save_file=Typed(Save_TXT).tag(width='max')

    @observe('read_file.read_event')
    def obs_read_event(self, change):
        self.data="".join(self.read_file.data["data"])

    @observe('save_file.save_event')
    def obs_save_event(self, change):
        self.save_file.direct_save(self.data, write_mode='w')

    def _default_read_file(self):
        return Read_TXT(main_file=self.main_file, dir_path=self.dir_path)

    def _default_save_file(self):
        return Save_TXT(main_file=self.read_file.main_file, dir_path=self.read_file.dir_path)

    def data_list(self):
        return self.data.split("\n")

def xy_string_split(tempstr):
    return tempstr.split("(")[1].split(")")[0].split(",")+tempstr.split("(")[2].split(")")[0].split(",")

def tuple_split(tempstr):
    return tempstr.split("(")[1].split(")")[0].split(",")

class NoShowBase(Base):
    def _default_show_base(self):
        return False

class jdf_array(NoShowBase):
    """describes a jdf array. defaults to an array centered at 0,0 with one item. array_num=0 corresponds to the main array"""
    array_num=Int()
    x_start=Int()
    x_num=Int(1)
    x_step=Int()
    y_start=Int()
    y_num=Int(1)
    y_step=Int()
    M1x=Int()
    M1y=Int()

    def _default_main_params(self):
        return ['array_num', 'x_start', 'x_num', 'x_step', 'y_start', 'y_num', 'y_step', 'M1x', 'M1y']

class jdf_pos(NoShowBase):
    x=Int()
    y=Int()

class jdf_assign(NoShowBase):
    assign_type=ContainerList().tag(inside_type=unicode)
    pos_assign=ContainerList().tag(inside_type=jdf_pos)#inside_labels=["x", "y"])
    shot_assign=Unicode() #ContainerList(default=[0])
    assign_comment=Unicode()

    def add_pos(self, pos_x, pos_y):
        tempassign=jdf_pos(name="pos_assign{0}".format(len(self.pos_assign)), show_base=False)
        tempassign.x=pos_x
        tempassign.y=pos_y
        self.pos_assign.append(tempassign)

class jdf_pattern(NoShowBase):
    pattern_num=Int(1)
    pattern_x=Int()
    pattern_y=Int()
    pattern_name=Unicode()

    def _default_main_params(self):
        return ['pattern_num', 'pattern_name', 'pattern_x', 'pattern_y']

class jdf_base(Base):
    comment=Unicode()
    Px=Int()
    Py=Int()
    Qx=Int()
    Qy=Int()

    GLMPOS_comment=Unicode()

    mgn_name=Unicode()
    wafer_diameter=Float()
    write_diameter=Float()

    stdcur=Int(2)
    shot=Int(8)
    resist=Int(165)
    arrays=ContainerList().tag(width='max', inside_type=jdf_array)
    assigns=ContainerList().tag(width='max', inside_type=jdf_assign)
    patterns=ContainerList().tag(width='max', inside_type=jdf_pattern)

    def add_array(self, x_start, x_num, x_step, y_start, y_num, y_step, M1x=0, M1y=0, array_num=0):
        temparray=jdf_array(name="jdf_array{0}".format(len(self.arrays)), show_base=False)
        temparray.x_start=x_start
        temparray.x_num=x_num
        temparray.x_step=x_step
        temparray.y_start=y_start
        temparray.y_num=y_num
        temparray.y_step=y_step
        temparray.M1x=M1x
        temparray.M1y=M1y
        temparray.array_num=array_num
        self.arrays.append(temparray)

    def add_assign(self, assign_type, pos_assign, shot_assign, assign_comment):
        tempassign=jdf_assign(name="jdf_assign{0}".format(len(self.assigns)), show_base=False)
        tempassign.assign_type=assign_type
        for item in pos_assign:
            tempassign.add_pos(item[0], item[1])
        tempassign.shot_assign=shot_assign
        tempassign.assign_comment=assign_comment
        self.assigns.append(tempassign)

    def add_pattern(self, pattern_num, pattern_name, pattern_x, pattern_y):
        temppattern=jdf_pattern(name="jdf_pattern{0}".format(len(self.patterns)), show_base=False)
        temppattern.pattern_name=pattern_name
        temppattern.pattern_x=pattern_x
        temppattern.pattern_y=pattern_y
        temppattern.pattern_num=pattern_num
        self.patterns.append(temppattern)

    def jdf_parse(self, jdf_data):
        jdf_list=jdf_data.split("\n")
        inside_path=False
        inside_layer=False
        patterns=[]
        array_num=0
        assign_array=[]
        for n, line in enumerate(jdf_list):
            comment=""
            templist=line.split(";")
            tempstr=templist[0].strip() #remove comments
            if ';' in line:
                comment=templist[1].strip()
            if tempstr.startswith('GLMPOS'):
                self.Px, self.Py, self.Qx, self.Qy=xy_string_split(tempstr) #get P and Q mark positions
            elif 'JOB' in tempstr:
                mgn_name, self.wafer_diameter, self.write_diameter=tempstr.split(",") #magazine name and wafer size
                self.mgn_name=mgn_name.split("'")[1].strip()
            elif 'PATH' in tempstr:
                inside_path=True
            elif "LAYER" in tempstr:
                inside_layer=True
            if inside_path:
                if 'ARRAY' in tempstr:
                    if ":" in tempstr:
                        array_num=tempstr.split(":")[0] #for subarrays
                        x_start, x_num, x_step, y_start, y_num, y_step=xy_string_split(tempstr)
                    else:
                        x_start, x_num, x_step, y_start, y_num, y_step=xy_string_split(tempstr) #for main array
                    self.add_array(x_start=x_start, x_num=x_num, x_step=x_step, y_start=y_start, y_num=y_num, y_step=y_step)
                elif 'ASSIGN' in tempstr:
                    assign_type=tempstr.split("ASSIGN")[1].split("->")[0].strip().split("+")
                    assign_type=[unicode(at) for at in assign_type]
                    pos_assign=[]
                    shot_assign=""
                    for item in tempstr.split("->")[1].partition("(")[2].rpartition(")")[0].split(")"):
                        if "(" in item:
                            xcor, ycor=item.split("(")[1].split(",")
                            pos_assign.append((xcor,ycor))
                        elif "," in item:
                            shot_assign=unicode(item.split(",")[1].strip())
                    #pos_assign=[int(pa) for pa in pos_assign]
                    self.add_assign(assign_type=assign_type, pos_assign=pos_assign,
                                    shot_assign=shot_assign, assign_comment=comment)
                    #print array_num, assign_type, pos_assign
                    if array_num==0:
                        assign_array.append(("+".join(assign_type), comment))
                elif 'CHMPOS' in tempstr:
                    M1x, M1y=tuple_split(tempstr)
                    self.arrays[-1].M1x=M1x
                    self.arrays[-1].M1y=M1y
                elif "PEND" in tempstr:
                    inside_path=False
            elif inside_layer:
                if 'END' in tempstr:
                    inside_layer=False
                elif 'STDCUR' in tempstr:
                    stdcur=tempstr.split("STDCUR")[1]
                    self.stdcur=stdcur
                elif 'SHOT' in tempstr:
                    shot=tempstr.split(',')[1]
                    self.shot=shot
                elif 'RESIST' in tempstr:
                    resist=tempstr.split('RESIST')[1]
                    self.resist=resist
                elif 'P(' in tempstr:
                    pattern_name=tempstr.split("'")[1].split(".")[0]
                    patterns.append(pattern_name)
                    pattern_num=tempstr.split("(")[1].split(")")[0]
                    pattern_x=tempstr.split("(")[2].split(")")[0].split(",")[0]
                    pattern_y=tempstr.split("(")[2].split(")")[0].split(",")[0]
                    self.add_pattern(pattern_num=pattern_num, pattern_name=pattern_name, pattern_x=pattern_x, pattern_y=pattern_y)
                elif tempstr.startswith('@'):
                    pass
    def jdf_produce(self):
        jl=[] #jdf_data.split("\n")
        jl.append("JOB/W '{name}', {waf_diam}, {write_diam}\n\n".format(name=self.mgn_name,
                  waf_diam=self.wafer_diameter, write_diam=self.write_diameter))
        jl.append(";{comment}\n\n".format(comment=self.comment))
        jl.append("GLMPOS P=({Px}, {Py}), Q=({Qx},{Qx})\n\n".format(Px=self.Px, Py=self.Py, Qx=self.Qx, Qy=self.Qy))
        jl.append("PATH\n")
        jl.append("ARRAY ({x_start}, {x_num}, {x_step})/({y_start}, {y_num}, {y_step})\n".format(
               x_start=self.arrays[0].x_start, x_num=self.arrays[0].x_num, x_step=self.arrays[0].x_step,
               y_start=self.arrays[0].y_start, y_num=self.arrays[0].y_num, y_step=self.arrays[0].y_step))
        jl.append("\tCHMPOS M1=({M1x}, {M1y})\n)".format(M1x=self.arrays[0].M1x, M1y=self.arrays[0].M1y))

        for item in self.assigns:
            asgn_type="+".join(item.assign_type)
            pos_asgn=""
            for pos in item.pos_assign:
                pos_asgn+="({x},{y}),".format(x=pos.x, y=pos.y)
            if item.shot_assign=="":
                shot_asgn=""
            else:
                shot_asgn=", {sa}".format(sa=item.shot_assign)
            if item.assign_comment=="":
                asgn_comment=""
            else:
                asgn_comment=";{ac}".format(ac=item.assign_comment)
            jl.append("ASSIGN {asgn_type} -> ({pos_asgn}{shot_asgn}) {asgn_comment}".format(
                      asgn_type=asgn_type, pos_asgn=pos_asgn, shot_asgn=shot_asgn, asgn_comment=asgn_comment))
        jl.append("AEND\n\n")

        for n, item in enumerate(self.arrays[1:]):
            jl.append("{arr_num}: ARRAY ({x_start}, {x_num}, {x_step})/({y_start}, {y_num}, {y_step})\n".format(
                   arr_num=item.array_num, x_start=item.x_start, x_num=item.x_num, x_step=item.x_step,
                   y_start=item.y_start, y_num=item.y_num, y_step=item.y_step))
        jl.append("AEND\nPEND\n\nLAYER 1\n")

        for n, item in enumerate(self.patterns):
            jl.append("P({pnum}) '{pname}.v30' ({px},{py})\n".format(
                      pnum=item.pattern_num, pname=item.pattern_name, px=item.pattern_x, py=item.pattern_y))
        jl.append("STDCUR {0}".format(self.stdcur))
        jl.append("SHOT A,{0}".format(self.shot))
        jl.append("RESIST {}".format(self.resist))
        jl.append("END 1")

        return "\n".join(jl)

#        for n, line in enumerate(jl):#:df_list):
#            templist=line.split(";")
#            tempstr=templist[0].strip() #remove comments
#            if ';' in line:
#                comment=templist[1].strip()
#            if tempstr.startswith('GLMPOS'):
#                self.Px, self.Py, self.Qx, self.Qy=xy_string_split(tempstr) #get P and Q mark positions
#            elif 'JOB' in tempstr:
#                mgn_name, self.wafer_diameter, self.write_diameter=tempstr.split(",") #magazine name and wafer size
#                self.mgn_name=mgn_name.split("'")[1].strip()
#            elif 'PATH' in tempstr:
#                inside_path=True
#            elif "LAYER" in tempstr:
#                inside_layer=True
#            if inside_path:
#                if 'ARRAY' in tempstr:
#                    if ":" in tempstr:
#                        array_num=tempstr.split(":")[0] #for subarrays
#                        x_start, x_num, x_step, y_start, y_num, y_step=xy_string_split(tempstr)
#                    else:
#                        x_start, x_num, x_step, y_start, y_num, y_step=xy_string_split(tempstr) #for main array
#                    self.add_array(x_start=x_start, x_num=x_num, x_step=x_step, y_start=y_start, y_num=y_num, y_step=y_step)
#                elif 'ASSIGN' in tempstr:
#                    assign_type=tempstr.split("ASSIGN")[1].split("->")[0].strip().split("+")
#                    assign_type=[unicode(at) for at in assign_type]
#                    pos_assign=[]
#                    shot_assign=""
#                    for item in tempstr.split("->")[1].partition("(")[2].rpartition(")")[0].split(")"):
#                        if "(" in item:
#                            xcor, ycor=item.split("(")[1].split(",")
#                            pos_assign.append((xcor,ycor))
#                        elif "," in item:
#                            shot_assign=unicode(item.split(",")[1].strip())
#                    #pos_assign=[int(pa) for pa in pos_assign]
#                    self.add_assign(assign_type=assign_type, pos_assign=pos_assign, shot_assign=shot_assign)
#                    #print array_num, assign_type, pos_assign
#                    if array_num==0:
#                        assign_array.append(("+".join(assign_type), comment))
#                elif 'CHMPOS' in tempstr:
#                    M1x, M1y=tuple_split(tempstr)
#                    self.arrays[-1].M1x=M1x
#                    self.arrays[-1].M1y=M1y
#                elif "PEND" in tempstr:
#                    inside_path=False
#            elif inside_layer:
#                if 'END' in tempstr:
#                    inside_layer=False
#                elif 'STDCUR' in tempstr:
#                    stdcur=tempstr.split("STDCUR")[1]
#                    self.stdcur=stdcur
#                elif 'SHOT' in tempstr:
#                    shot=tempstr.split(',')[1]
#                    self.shot=shot
#                elif 'RESIST' in tempstr:
#                    resist=tempstr.split('RESIST')[1]
#                    self.resist=resist
#                elif 'P(' in tempstr:
#                    pattern_name=tempstr.split("'")[1].split(".")[0]
#                    patterns.append(pattern_name)
#                    pattern_num=tempstr.split("(")[1].split(")")[0]
#                    pattern_x=tempstr.split("(")[2].split(")")[0].split(",")[0]
#                    pattern_y=tempstr.split("(")[2].split(")")[0].split(",")[0]
#                    self.add_pattern(pattern_num=pattern_num, pattern_name=pattern_name, pattern_x=pattern_x, pattern_y=pattern_y)

Awafer=[                                         (7,1), (8,1),
                                   (5,2), (6,2), (7,2), (8,2),
                            (4,3), (5,3), (6,3), (7,3), (8,3),
                     (3,4), (4,4), (5,4), (6,4), (7,4), (8,4),
              (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5),
              (2,6), (3,6), (4,6), (5,6), (6,6), (7,6), (8,6),
       (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7),
       (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)]

BadCoords=[(7,1), (8,1),
           (5,2), (8,2),
           (4,3), (8,3),
           (3,4), (8,4),
           (2,5), (8,5),
           (2,6), (8,6),
           (1,7), (8,7),
           (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)]

#print Awafer
#print
#print BadCoords

GoodCoords = [x for x in Awafer if x not in BadCoords]

#print
#print GoodCoords

AssignArray=[('A(1)+A(2)+A(15)', 'D32080 with two IDTs and Squid connect'),
        ('A(1)+A(3)+A(15)', 'S32080 with two IDTs and Squid connect'),
        ('A(1)+A(4)+A(15)', 'S32050 with two IDTs and Squid connect'),
        ('A(1)+A(5)+A(15)',  'D32050 with two IDTs and Squid connect'),
        ('A(1)+A(6)+A(15)',  'D9050 with two IDTs and Squid connect'),
        ('A(1)+A(7)+A(15)', 'S9050 with two IDTs and Squid connect'),
        ('A(1)+A(8)+A(15)', 'S9080 with two IDTs and Squid connect'),
        ('A(1)+A(9)+A(15)', 'D9080 with two IDTs and Squid connect'),
        ('A(12)+A(10)+A(15)', 'D5080 with two FDTs and Squid connect'),
        ('A(12)+A(11)+A(15)', 'D5096 with two FDTs and Squid connect'),
        ('A(13)+A(15)', 'IDT by itself'),
        ('A(14)+A(15)', 'FDT by itself'),
        ('A(1)+A(15)',  'Two IDTs alone with squid connect'),
        ('A(12)+A(15)', 'two FDTs alone with squid connect')]

numCoords=int(len(Awafer)//len(AssignArray))
numBadCoords=int(len(BadCoords)//len(AssignArray))
numGoodCoords=int(len(GoodCoords)//len(AssignArray))
numSkip=len(AssignArray)

#print numBadCoords, numGoodCoords

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

    #if (m+1)*numSkip+i<len(GoodCoords):
    #    tempstr+=str(GoodCoords[(m+1)*numSkip+i])+", "
#    print "ASSIGN {arrays} -> ({nums}{dose}) ;{comment}".format(arrays=item[0], comment=item[1], nums=tempstr[:-2], dose="")

if __name__=="__main__":
    a=Text_Editor(name="Text_Editor")#dir_path="/Volumes/aref/jbx9300/job/TA150515B/IDTs", main_file="idt.jdf")
    b=jdf_base(name="JDF")#_base()
    #b.arrays.extend((jdf_array(), jdf_array(x_start=5)))
    a.read_file.read()
    #print a.data
    b.jdf_parse(a.data)
    #c=Base()
    #a.jdf.arrays.append(4.5)
    #a.jdf.arrays.append(4)

    #print a.Px
    #print [a.get_tag(aa, 'label', aa) for aa in a.all_params]
    #print a.jdf_list
    #print b.get_member('arrays').item.validate_mode[1]

    b.show()
    print a.data
    print b.jdf_produce()
    #print a.jdf_save_file.file_path
#/Volumes/aref/jbx9300/job/TA150515B/IDTs