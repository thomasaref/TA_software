# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:46:23 2015

@author: thomasaref
"""

alt=True
def dxfstart():
    """starts dxf file"""
    tlist=[]
    tlist.append('0\r\n')
    tlist.append('SECTION\r\n')
    tlist.append('2\r\n')
    tlist.append('HEADER\r\n')  #starts header section of DXF
    if alt:
        tlist.append('9\r\n')
        tlist.append('$ACADVER\r\n') #specifies version to be AutoCAD2004
        tlist.append('1\r\n')
        tlist.append('AC1009\r\n')
    if 0:
        tlist.append('9\r\n')
        tlist.append('$INSBASE\r\n') #sets insertion base to (0,0,0)
        tlist.append('10\r\n')
        tlist.append('0.0\r\n')
        tlist.append('20\r\n')
        tlist.append('0.0\r\n')
        tlist.append('30\r\n')
        tlist.append('0.0\r\n')

    tlist.append('9\r\n')
    tlist.append('$EXTMIN\r\n') #x, y coordinates of lower left corner
    tlist.append('10\r\n')
    tlist.append('-50000.0\r\n')
    tlist.append('20\r\n')
    tlist.append('-50000.0\r\n')
    if alt:
        tlist.append('30\r\n')
        tlist.append('0.0\r\n')
    tlist.append('9\r\n')
    tlist.append('$EXTMAX\r\n') #x,y coordinates of upper right corner
    tlist.append('10\r\n')
    tlist.append('50000.0\r\n')
    tlist.append('20\r\n')
    tlist.append('50000.0\r\n')
    if alt:
        tlist.append('30\r\n')
        tlist.append('0.0\r\n')

        tlist.append('9\r\n')
        tlist.append('$LUNITS\r\n')
        tlist.append('70\r\n')
        tlist.append('2\r\n')
        tlist.append('9\r\n')
        tlist.append('$LUPREC\r\n')
        tlist.append('70\r\n')
        tlist.append('3\r\n')
    tlist.append('0\r\n')
    tlist.append('ENDSEC\r\n')
    if alt:
        tables(tlist)
        blocks(tlist)
    return tlist

def do_tup(item_list):
    return ["{0}\r\n{1}\r\n".format(item[0], item[1]) for item in item_list]

def tables(tlist):
    tlist.extend(do_tup(
    [(0, "SECTION"),
     (2, "TABLES"),
     (0, "TABLE"),
     (2, "LTYPE"),
    (70, 16),
    (0, "LTYPE"),
    (2, "CONTINUOUS"),
    (70, 0),
    (3, "Solid line"),
    (72, 65),
    (73, 0),
    (40, "0.00000000"),
    (0, "ENDTAB"),
    (0, "TABLE"),
    (2, "LAYER"),
    (70, 10),
    (0, "LAYER"),
    (2, "PADS"),
    (70, 0),
    (62, 6),
    (6, "CONTINUOUS"),
    (0, "ENDTAB"),
    (0, "ENDSEC")]))
    return tlist


def blocks(tlist):
    tlist.extend(do_tup([
    (0, "SECTION"),
    (2, "BLOCKS"),
    (0, "BLOCK"),
    (8, 0),
    (2, "$MODEL_SPACE"),
    (70, 0),
    (10, "0.00000000"),
    (20, "0.00000000"),
    (30, "0.00000000"),
    (3, "$MODEL_SPACE"),
    (1, ""),
    (0, "ENDBLK"),
    (8, 0),
    (0, "BLOCK"),
    (67, 1),
    (8, 0),
    (2, "$PAPER_SPACE"),
    (70, 0),
    (10, 0.00000000),
    (20, 0.00000000),
    (30, 0.00000000),
    (3, "$PAPER_SPACE"),
    (1, ""),
    (0, "ENDBLK"),
    (67, 1),
    (8, 0),
    (0, "ENDSEC")]))
    return tlist

def start_entities(tlist=[]):
    tlist.append('0\r\n')  #starts entities section
    tlist.append('SECTION\r\n')
    tlist.append('2\r\n')
    tlist.append('ENTITIES\r\n')
    return tlist

def dxfend(tlist=[]):
    """ends dxf file"""
    tlist.append('0\r\n')
    tlist.append('ENDSEC\r\n')
    tlist.append('0\r\n')
    tlist.append('EOF\r\n')
    return tlist


def poly2dxf(p, color, layer):
    """converts polygon to dxf format and returns list of commands (text based)"""
    if not alt:
        tlist=['0\r\nLWPOLYLINE\r\n',  #place line
                   '8\r\n{0}\r\n'.format(layer), #add to layer
                   '62\r\n{0}\r\n'.format(color),
                   '90\r\n{0}\r\n'.format(len(p)), #number of vertices
                   '70\r\n1\r\n'] #is closed
        for v in p:
                tlist.append('10\r\n{0}\r\n20\r\n{1}\r\n'.format(v[0],v[1])) #vertex coordinate X and Y
        return tlist
    else:
        tlist=[]
        tlist.extend(do_tup([
        (0, "POLYLINE"),
        (8, "PADS"),
        (66, 1),
        (10, 0.00000000),
        (20, 0.00000000),
        (30, 0.00000000),
        (70, 1)]))
        for v in p:
            tlist.extend(do_tup([
            (0, "VERTEX"),
            (8, "PADS"),
            (10, v[0]),
            (20, v[1]),
            (30, "0.00000000")]))
        tlist.extend(do_tup([
        (0, "SEQEND"),
        (8, "PADS")]))
        return tlist

#from numpy import flat
def EBL_Polygons2dxf(verts, color, layer):
    dlist=dxfstart()
    dlist=start_entities(dlist)
    mlist=[poly2dxf(p, color, layer) for p in verts]
    dlist.extend([item for sublist in mlist for item in sublist])
    dlist=dxfend(dlist)
    return dlist

def save_dxf(verts, color, layer, file_path, write_mode="w"):
    dlist=EBL_Polygons2dxf(verts, color, layer)
    dxfstr=''.join(dlist)
    with open(file_path, write_mode) as g:
        g.write(dxfstr)

class AC_List(object):
    tlist=[]
    def append(self, value):
        self.tlist.append(value)

    def ac(self, num_start, ac_command, num_end=None):
        self.tlist.append("{0}\r\n".format(num_start))
        self.tlist.append("{0}\r\n".format(ac_command))
        if num_end is not None:
            self.tlist.append("{0}\r\n".format(num_end))

def insert_block(acl=AC_List()):
    acl.ac(0, 'INSERT',)
    acl.ac(5, "F8B0")  #330  #1F
    acl.ac(100, "AcDbEntity")  #Subclass marker
    acl.ac(8, 'Photomarks')
    acl.ac(100, "AcDcBlockReference") #Subclass marker
    acl.ac(2, 'PL cross') #Block name
    acl.ac(10, -7500.0) #x
    acl.ac(20, 4000.0)  #y
    acl.ac(30, 0.0)     #z
    #acl.ac(50, 0.0)     #rotation

#
#def dlist2dxf(self):
#    """writes dlist to dxf file"""
#    if '.dxf' in self.filer.main_file:
#        dlist2dxf(dlist=self.dlist, fileout=self.filer.file_path)
#    else:
#        print('Fail: can only write dxf to .dxf file')

#    def dlist2dstr(self):z

#    def writetxtfile(self):
#        """writes dstr to text file. mostly for debugging"""
#        if '.gds' in self.fileout:
#            print('Fail: cannot write txt to .gds file')
#        else:
#            with open(self.fullfileout, 'w') as g:
#                g.write(self.dstr)
#
#    def readtxtfile(self):
#        """reads text file and places in filestr. mostly for debugging"""
#        with open(self.fullfilein, 'r') as f:
#            self.filestr = f.read()

class testverts(object):
    unit_factor=1.0
    verts=[]

    def sP(self, verts, inlist=None):
        if inlist is None:
            inlist=[]
        inlist.append(self._gen_sP(verts)) #tuple([(v[0]/self.unit_factor, v[1]/self.unit_factor) for v in verts])
        return inlist

    def _gen_sP(self, verts):
        return tuple([(v[0]/self.unit_factor, v[1]/self.unit_factor) for v in verts])

    def _gen_sR(self, xr, yr, wr, hr):
        """creates rectangle EBLpolygon with (x,y) coordinates=(xr,yr), width=wr, height=hr"""
        return self._gen_sP(verts=[(xr,yr), (xr+wr,yr), (xr+wr, yr+hr), (xr, yr+hr)])

def start_blocks(acl=AC_List()):
    acl.ac(0, "SECTION")
    acl.ac(2, "TABLES")
    acl.ac(0, "TABLE")
    acl.ac(2, "LAYER")
    #acl.ac(0, LAYER)
    acl.ac(100, "AcDbSymbolTableRecord")
    acl.ac(100, "AcDbLayerTableRecord")
    acl.ac(2, "Photomarks") #layer name
    acl.ac(70, 0) #flags
    acl.ac(62, 1) #color number, if negative, layer is off
    acl.ac(6, "Continuous") #linetype name

#370
#    -3
#390
#F
#1001
#AcAecLayerStandard
#1000

#1000
    acl.ac(0, "ENDTAB")

    acl.ac(0, "TABLE")
    acl.ac(2, "BLOCK_RECORD")

    acl.ac(0, "BLOCK_RECORD")
    acl.ac(100, "AcDbSymbolTableRecord")
    acl.ac(100, "AcDbBlockTableRecord")
    acl.ac(2, "PL cross")
    acl.ac(0, "ENDTAB")

    acl.ac(0, "ENDSEC")

    acl.ac(0, "SECTION")
    acl.ac(2, "BLOCKS")
    #acl.ac(0, "BLOCK")
    #acl.ac(5, 20) #330 #1F
    #acl.ac(100, "AcDbEntity")
    #acl.ac(8, 0)
    #acl.ac(100, "AcDbBlockBegin")
    #acl.ac(2, "*Model_Space")
    #acl.ac(70, 0)
    #acl.ac(10, 0.0)
# 20
#0.0
# 30
#0.0
#  3
#*Model_Space
#  1
#
#  0
#ENDBLK
#  5
#21
#330
#1F
#100
#AcDbEntity
#  8
#0
#100
#AcDbBlockEnd
#
    acl.ac(0, "BLOCK")
    acl.ac(5, "F8B0")
    #330
    #F85E
    acl.ac(100, "AcDbEntity")
    acl.ac(8, 0) #layer name
    acl.ac(100, "AcDbBlockBegin")
    acl.ac(2, "PL cross")  #black name"
    acl.ac(70, 0) #block type flags
    acl.ac(10, 0.0) #x
    acl.ac(20, 0.0) #y
    acl.ac(30, 0.0) #z
    acl.ac(3, "PL cross") #block name again
    acl.ac(1, "") #xref name (present only if block is an xref)
#
    tp=testverts()

    verts=tp.sP([(0.0, 0.0), (1.0,1.0), (0.0,1.0)])

    mlist=[poly2dxf(p, 0, 0) for p in verts]
    acl.tlist.extend([item for sublist in mlist for item in sublist])

#    tp=testverts()
#    p=[]
#    p.extend(tp.sP([(0, 0), (1,0), (0,1)]))
#    acl.ac(0, "LWPOLYLINE") ##regular polygon
###    acl.ac(5, "F860")
#    acl.ac(8, 0) #layer \r\n{0}\r\n'.format(layer), #add to layer
#    #acl.ac(62, 0) #\r\n{0}\r\n'.format(color),
#    acl.ac(90, "{0}".format(len(p))) #number of vertices=4
#    acl.ac(70, 1) #is closed
#    for v in p:
#        acl.tlist.append('10\r\n{0}\r\n20\r\n{1}\r\n'.format(v[0],v[1])) #vertex coordinate X and Y

#330
#F85E
#100
#AcDbEntity
#  8
#0
#100
#AcDbPolyline
# 90
#        5
# 70
#     1
# 43
#0.0
    acl.ac(0, "ENDBLK")
#  5
#F864
#330
#F85E
    acl.ac(100, "AcDbEntity")
    acl.ac(8, 0)
    acl.ac(100, "AcDbBlockEnd")
    acl.ac(0, "ENDSEC")
    return acl

def testblock():
    tlist=dxfstart()
    tacl=start_blocks()
    tlist.extend(tacl.tlist)
    tlist=start_entities(tlist)
    tp=testverts()

    verts=tp.sP([(0.0, 0.0), (0.5,0.0), (0.0,1.0)])

    mlist=[poly2dxf(p, 0, "al") for p in verts]
    tlist.extend([item for sublist in mlist for item in sublist])

    #cacl=AC_List()
    #cacl.ac(0, "LWPOLYLINE") ##regular polygon
##    acl.ac(5, "F860")
    #cacl.ac(8, 0) #layer \r\n{0}\r\n'.format(layer), #add to layer
    #acl.ac(62, 0) #\r\n{0}\r\n'.format(color),
    #cacl.ac(90, "{0}".format(len(p))) #number of vertices=4
    #cacl.ac(70, 1) #is closed
    #for v in p:
    #    cacl.tlist.append('10\r\n{0}\r\n20\r\n{1}\r\n'.format(v[0],v[1])) #vertex coordinate X and Y

    bacl=AC_List()
    bacl.ac(0, 'INSERT',)
    bacl.ac(5, "F8B0")  #330  #1F
    bacl.ac(100, "AcDbEntity")  #Subclass marker
    bacl.ac(8, 0)
    bacl.ac(100, "AcDcBlockReference") #Subclass marker
    bacl.ac(2, 'PL cross') #Block name
    bacl.ac(10, 0.0) #x
    bacl.ac(20, 0.0)  #y
    bacl.ac(30, 0.0)     #z
    #b#acl.ac(50, 0.0)     #rotation
    tlist.extend(bacl.tlist)
    tlist=dxfend(tlist)

    for i,t in enumerate(tlist):
        print 2*i, t, 2*i
    dxfstr=''.join(tlist)
    with open("/Users/thomasaref/Documents/TA_software/dxfblocktest.dxf", "w") as g:
        g.write(dxfstr)

from taref.core.universal import read_text
def read_dxf(file_path):
    """reads dxf file in and places polygons in polylist"""
    str_list=read_text(file_path)
    data=zip(str_list[0::2], str_list[1::2])#str_list[0:2:-1]#, str_list[1:2:-1])
    in_polyline=False
    in_vertex=False
    layer_names=[]
    verts=[]
    for n, line in enumerate(data):
        if line==("0", "SECTION"):
            print n*2
        if line==("0", "POLYLINE"):
            in_polyline=True
            xcoords=[]
            ycoords=[]
        if in_vertex:
            if line[0]=="8":
                layer_names.append(line[1])
                layer_name=line[1]
            elif line[0]=="10":
                xcoords.append(float(line[1]))
            elif line[0]=="20":
                ycoords.append(float(line[1]))
            elif line[0]=="0":
                in_vertex=False
        if in_polyline and line==("0", "VERTEX"):
            in_vertex=True
        if line==("0", "SEQEND"):
            in_polyline=False
            verts.append((layer_name, zip(xcoords, ycoords)))
    print layer_name
    print [item[1] for item in verts if item[0]=="PADS"]

if __name__=="__main__":
    #testblock()
    file_path="/Users/thomasaref/Downloads/paddxfs/pads_W46.dxf"
    read_dxf(file_path)

#    if '.dxf' in self.filein:
#        self.polylist=readdxflayer(self.filein, inlayer=layername)


#from atom.api import Atom, List, Unicode#, Property
#
#class EBLPolygon(Atom):
#    """Implements polygons for use in drawing EBL patterns and includes conversion of polygon to DXF or GDS format (text based)"""
#
#    verts=List().tag(desc='list of vertices')
#    cn=Unicode('green').tag(desc="color or datatype of polygon, could be used for dosing possibly")
#    layer=Unicode('Al').tag(desc='layer of polygon')
#    #codes=Property()
#
#    #def _get_codes(self):
#    #    """used for drawing polygons by matplotlib functions"""
#    #    codes=[2 for x in self.verts]
#    #    codes[0]=1
#    #    return codes
#from EBLPolygon import EBLPolygon



#def readdxflayer(filein, inlayer='Al'):
#    """Reads layer inlayer of dxf file filein to polylist and returns it"""
#    inEntities=inObject=polyline=0
#    xcoord=[]
#    ycoord=[]
#    polylist=[]
#    layer=''
#    nameline=''
#    with open(filein, 'r') as f:
#        TotalList=list(f)
#        for a, line in enumerate(TotalList):
#            if 'ENTITIES' in line:
#                inEntities=1
#            if inEntities:
#                if line.strip()=='0':
#                    if TotalList[a+1].strip()=='LWPOLYLINE' or TotalList[a+1].strip()=='ENDSEC':
#                        if inObject:
#                            if nameline=='LWPOLYLINE':
#                                polyline=polyline+1
#                                if layer==inlayer:
#                                    if xcoord!=[] and ycoord!=[]:
#                                        poly1=EBLPolygon(verts=zip(xcoord, ycoord), cn='red', layer=layer)
#                                        polylist.append(poly1)
#                                        #verts=verts+zip(xcoord,ycoord)
#                                        #codes=codes+[Path.MOVETO] + (len(xcoord) - 1) * [Path.LINETO]#+[Path.CLOSEPOLY]
#                                    xcoord=[]
#                                    ycoord=[]
#                        nameline=TotalList[a+1].strip()
#                        inObject=1
#                if inObject:
#                    if nameline=='LWPOLYLINE':
#                        sline=line.strip()
#                        if sline=='8':
#                            layer=TotalList[a+1].strip()
#                        if sline=='10':
#                            xcoord.append(float(TotalList[a+1].strip()))
#                        if sline=='20':
#                            ycoord.append(float(TotalList[a+1].strip()))
#                if nameline=='ENDSEC':
#                    break
#    return polylist
#
#if __name__=="__main__":
#    a=EBLPolygon(verts=[(0,0), (1,1), (2, 0)])
#    print a.codes
#    print a.verts
#    b=EBLRectangle()
#    print b.codes
#    print b.verts