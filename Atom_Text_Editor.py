# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:38:47 2015

@author: thomasaref

A simple text editor driver allowing one to load, edit and save text files
"""

from Atom_Base import Base
from atom.api import Str, observe, Unicode, Typed, ContainerList, Int
from Atom_Read_File import Read_TXT
from Atom_Save_File import Save_TXT
#from LOG_functions import log_info, log_debug, make_log_file, log_warning

class Text_Editor(Base):
    main_file=Unicode("idt.jdf").tag(private=True)
    dir_path=Unicode("/Users/thomasaref/Dropbox/Current stuff/TA_software").tag(private=True)
    data=Str().tag(discard=True, log=False)
    read_file=Typed(Read_TXT)
    save_file=Typed(Save_TXT)

    #def _default_name(self):
    #    return "base{0}".format(len(self.boss.bases))

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

def xy_string_split(tempstr):
    return tempstr.split("(")[1].split(")")[0].split(",")+tempstr.split("(")[2].split(")")[0].split(",")

def tuple_split(tempstr):
    return tempstr.split("(")[1].split(")")[0].split(",")

class JDF_Editor(Text_Editor):
    jdf_list=ContainerList()
    Px=Int()
    Py=Int()
    Qx=Int()
    Qy=Int()

    def jdf_parse(self):
        self.jdf_list=self.data.split("\n")
        inside_path=False
        inside_layer=False
        patterns=[]
        array_num=0
        assign_array=[]
        for n, line in enumerate(self.jdf_list):
            #if  n==4:
            templist=line.split(";")
            tempstr=templist[0].strip() #remove comments
            if ';' in line:
                comment=templist[1].strip()
            if tempstr.startswith('GLMPOS'):
                self.Px, self.Py, self.Qx, self.Qy=xy_string_split(tempstr) #get P and Q mark positions
                #Px, Py, Qx, Qy
            elif 'JOB' in tempstr:
                mgn_name, wafer_diameter, write_diameter=tempstr.split(",") #magazine name and wafer size
                mgn_name=mgn_name.split("'")[1].strip()
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
                elif 'ASSIGN' in tempstr:
                    assign_type=tempstr.split("ASSIGN")[1].split("->")[0].strip().split("+")
                    
                    assign_num=[s.split(')') for s in tempstr.split("->")[1].split("(")]

                    pos_assign=tempstr.split("->")[1].partition("(")[2].rpartition(")")[0].split(")")
                    for item in pos_assign:
                        if "(" in item:
                            print item.split("(")[1].split(",")
                        elif "," in item:
                            print item.split(",")[1].strip()
                    
                    print array_num, assign_type, pos_assign
                    if array_num==0:
                        assign_array.append(("+".join(assign_type), comment))
                elif 'CHMPOS' in tempstr:
                    M1x, M1y=tuple_split(tempstr)
                elif "PEND" in tempstr:
                    inside_path=False
            elif inside_layer:
                if 'END' in tempstr:
                    inside_layer=False
                elif 'STDCUR' in tempstr:
                    stdcur=tempstr.split("STDCUR")[1]
                    print stdcur
                elif 'SHOT' in tempstr:
                    shot=tempstr.split(',')[1]
                    print shot
                elif 'RESIST' in tempstr:
                    resist=tempstr.split('RESIST')[1]
                    print resist
                elif 'P(' in tempstr:
                    pattern_name=tempstr.split("'")[1].split(".")[0]
                    patterns.append(pattern_name)
                    pattern_num=tempstr.split("(")[1].split(")")[0]
                    pattern_x=tempstr.split("(")[2].split(")")[0].split(",")[0]
                    pattern_y=tempstr.split("(")[2].split(")")[0].split(",")[0]
                    #print pattern_num, pattern_x, pattern_y, pattern_name

        #print patterns
        print assign_array


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

print Awafer
print
print BadCoords

GoodCoords = [x for x in Awafer if x not in BadCoords]

print
print GoodCoords

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

print numBadCoords, numGoodCoords

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
    print "ASSIGN {arrays} -> ({nums}{dose}) ;{comment}".format(arrays=item[0], comment=item[1], nums=tempstr[:-2], dose="")

if __name__=="__main__":
    a=JDF_Editor()#dir_path="/Volumes/aref/jbx9300/job/TA150515B/IDTs", main_file="idt.jdf")
    b=Text_Editor()
    a.read_file.read()
    print a.data
    a.jdf_parse()
    print a.Px
    #print a.jdf_list
    #a.show()
    #print a.jdf_save_file.file_path
#/Volumes/aref/jbx9300/job/TA150515B/IDTs