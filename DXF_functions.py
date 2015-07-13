# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:46:23 2015

@author: thomasaref
"""

def dxfstart():  
    """starts dxf file"""
    tlist=[]
    tlist.append('0\r\n')
    tlist.append('SECTION\r\n')
    tlist.append('2\r\n')
    
    tlist.append('HEADER\r\n')  #starts header section of DXF
    tlist.append('9\r\n')
    #tlist.append('$ACADVER\r\n') #specifies version to be AutoCAD2004
    #tlist.append('1\r\n')
    #tlist.append('AC1018\r\n')
    #tlist.append('9\r\n')

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
    tlist.append('-1000.0\r\n')
    tlist.append('20\r\n')
    tlist.append('-1000.0\r\n')
    tlist.append('9\r\n')
    tlist.append('$EXTMAX\r\n') #x,y coordinates of upper right corner 
    tlist.append('10\r\n')
    tlist.append('1000.0\r\n')
    tlist.append('20\r\n')
    tlist.append('1000.0\r\n')
    tlist.append('0\r\n')
    tlist.append('ENDSEC\r\n')

    tlist.append('0\r\n')  #starts entities section
    tlist.append('SECTION\r\n')
    tlist.append('2\r\n')
    tlist.append('ENTITIES\r\n')
    return tlist
    
def dxfend():  
    """ends dxf file"""
    tlist=[]
    tlist.append('0\r\n')
    tlist.append('ENDSEC\r\n')
    tlist.append('0\r\n')
    tlist.append('EOF\r\n')
    return tlist
        

def poly2dxf(p, color, layer):
    """converts polygon to dxf format and returns list of commands (text based)"""
    tlist=['0\r\nLWPOLYLINE\r\n',  #place line
               '8\r\n{0}\r\n'.format(layer), #add to layer
               '62\r\n{0}\r\n'.format(color),
               '90\r\n{0}\r\n'.format(len(p)), #number of vertices=4
               '70\r\n1\r\n'] #is closed
    for v in p:
            tlist.append('10\r\n{0}\r\n20\r\n{1}\r\n'.format(v[0],v[1])) #vertex coordinate X and Y
    return tlist

#from numpy import flat    
def EBL_Polygons2dxf(verts, color, layer):
    dlist=dxfstart()
    mlist=[poly2dxf(p, color, layer) for p in verts]
    dlist.extend([item for sublist in mlist for item in sublist])

    dlist.extend(dxfend())
    return dlist

def save_dxf(file_path, data, write_mode="w"):
    dlist=EBL_Polygons2dxf(data.verts, data.color, data.layer)
    dxfstr=''.join(dlist)
    with open(file_path, write_mode) as g:
        g.write(dxfstr)    
    
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
            
def readdxf(self, layername='Al'):
    """reads dxf file in and places polygons in polylist"""
    if '.dxf' in self.filein:
        self.polylist=readdxflayer(self.filein, inlayer=layername)
    
     
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