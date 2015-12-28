# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:36:03 2015

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons, letter_A

class Test_Polygons(EBL_Polygons):
    def make_polylist(self):
        self.Dig("A", 0.0, 0.0, 10.0e-6, 2.0e-6)
#
#(xr+wr/2.0-lw/2.0, yr-wr),
#
#y=bx+a
#yr-wr=bxr-bwr/2.0+blw/2.0+a
#yr+wr-lw=bxr+a
#
#-2wr+lw=-bwr/2.0+blw/2.0
#
#b=(-2wr+lw)/(-wr/2.0+lw/2.0)
#b=-4wr/(-wr+lw)
#
#yr+wr-lw-(-2wr+lw)xr/(-wr/2+lw/2)=a
#yr+lw/2.0=(-2wr+lw)/(-wr/2+lw/2)x+yr+wr-lw-(-2wr+lw)/(-wr/2+lw/2)
#+lw/2.0=(-2wr+lw)/(-wr/2+lw/2)x+wr-lw-(-2wr+lw)/(-wr/2+lw/2)
#(-2wr+lw)/(-wr/2+lw/2)x=-wr+lw+lw/2.0+(-2wr+lw)/(-wr/2.0+lw/2.0)
#x=(-wr+lw+lw/2.0)(-wr2.0+lw/2.0)/(-2wr+lw)+xr
#
#[(xr+(-wr+lw+lw/2.0)(-wr/2.0-lw/2.0)/(-2wr+lw), yr+lw/2.0),
# (xr+(-wr+lw-lw/2.0)(-wr/2.0-lw/2.0)/(-2wr+lw), yr+lw/2.0),
# )
# (xr, yr+wr-lw),
#                (xr-wr/2.0+lw/2.0, yr-wr)],        
#xr+(lw+wr)/2.0-lw/2.0
if __name__=="__main__":
    print letter_A(0.0, 0.0, 10.0e-6, 1.0e-6)
    a=Test_Polygons()
    b=Test_Polygons()
    #a.chief.jdf.distribute_coords()
    print a.chief.jdf.arrays[0].assigns[0].pos_assign
    print a.chief.jdf.jdf_produce()
    print a.chief.jdf.output_jdf
    
    #a.make_polylist()
    #print a.verts
    a.show()