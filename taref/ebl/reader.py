# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 18:43:29 2016

@author: thomasaref
"""

from taref.ebl.polygons import EBL_Polygons
from taref.ebl.polygon_backbone import read_dxf
from taref.core.backbone import private_property


def FromDXF(file_path, **kwargs):
    read_func=read_dxf(file_path)

    class reader(EBL_Polygons):
        polylist=private_property(read_func)

    return reader(**kwargs)

if __name__=="__main__":
    file_path="/Users/thomasaref/Downloads/paddxfs/pads_W35.dxf"
    a=FromDXF(file_path, name='pads_W35')
    file_path="/Users/thomasaref/Downloads/paddxfs/pads_W46.dxf"
    b=FromDXF(file_path, name='pads_W46')

    jdf_text="""JOB/W 'R6PADS',4,-4.2

; For exposure on YZ-cut LiNbO3, piece D.
; Changing Np of transmon and gate distance

GLMPOS P=(10000,-46000),Q=(46000,-10000)

PATH MINI
ARRAY (7500,8,5000)/(-7500,8,5000)
	CHMPOS M1=(1500,1500)
	ASSIGN P(1) -> ((1,1-6),(1,8),(3,1-6),(5,1-6),(7,1-4),P35)
	ASSIGN P(2) -> ((1,7),(2,*),(3,7),(4,1-7),(6,1-5),(8,1-2),P46)
	;SKIP ((3,8),(4,8),(5,7-8),(6,6-8), (7,5-8), (8,3-8))
AEND
PEND

LAYER 1
	P(1) 'pads_W35.v30' (0,0)
	P(2) 'pads_W46.v30' (0,0)

   STDCUR 70
   SHOT A,100
   RESIST 30 ;Taken from TA 19 may 2015

@ 'pads_W35.jdi'
@ 'pads_W46.jdi'

END 1"""

    a.jdf.input_jdf=jdf_text
    a.show()
