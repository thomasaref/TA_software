# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:46:23 2015

@author: thomasaref
"""

def makedxfdlist(self):
    """converts polylist to text commands dlist in dxf format"""
    self.dlist=dxfstart()
    for p in self.polylist:
        self.dlist.extend(p.poly2dxf())
    self.dlist.extend(dxfend())

    
def dlist2dxf(self):
    """writes dlist to dxf file"""
    if '.dxf' in self.filer.main_file:
        dlist2dxf(dlist=self.dlist, fileout=self.filer.file_path)
    else:
        print('Fail: can only write dxf to .dxf file')

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
    
def Save(self):
     print "saving to file"
     self.makedxfdlist()
     self.dlist2dxf()
     self.bmr=BeamerGen()
     self.bmr.name=self.name
     self.bmr.mod_table_name = self.shot_mod_table
     self.bmr.bias=-0.009
     self.bmr.base_path=self.filer.dir_path+self.filer.divider
     self.bmr.extentLLy=-150
     self.bmr.extentURy=150
     self.bmr.gen_flow()
     self.jdf.add_pattern(self.name, self.shot_mod_table)
     
from atom.api import Atom, List, Unicode#, Property

class EBLPolygon(Atom):
    """Implements polygons for use in drawing EBL patterns and includes conversion of polygon to DXF or GDS format (text based)"""

    verts=List().tag(desc='list of vertices')
    cn=Unicode('green').tag(desc="color or datatype of polygon, could be used for dosing possibly")
    layer=Unicode('Al').tag(desc='layer of polygon')    
    #codes=Property()
    
    #def _get_codes(self):
    #    """used for drawing polygons by matplotlib functions"""
    #    codes=[2 for x in self.verts]
    #    codes[0]=1 
    #    return codes
        

if __name__=="__main__":
    a=EBLPolygon(verts=[(0,0), (1,1), (2, 0)])
    print a.codes
    print a.verts
    b=EBLRectangle() 
    print b.codes
    print b.verts     