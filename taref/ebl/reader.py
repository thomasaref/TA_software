# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 18:43:29 2016

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons
from taref.ebl.polygon_backbone import read_dxf
from taref.core.backbone import private_property

file_path="/Users/thomasaref/Downloads/paddxfs/pads_W46.dxf"
read_func=read_dxf(file_path)

class reader(EBL_Polygons):
    polylist=private_property(read_func)
#
#    @private_property
#    def polylist(self):
#        pass
#    
#    @polylist.getter
#    def get_polylist(self):
        
if __name__=="__main__":
    a=reader()
    a.show()
        