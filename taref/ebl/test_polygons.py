# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:36:03 2015

@author: thomasaref
"""

from taref.ebl.pads import PADS
from taref.ebl.wafer_labels import Wafer_Labels
from taref.ebl.cross import Cross, Symmetric_Cross
from taref.ebl.rectangle import Rectangle

if __name__=="__main__":
    jdf_text="""
PATH
ARRAY (-42500, 8, 5000)/(42500, 8, 5000)
	CHMPOS M1=(1500, 1500)
	ASSIGN A(1) -> ((1,7),(2,8),(3,8),(4,7),(5,5),(6,3),(6,8),(7,5),(8,2),(8,7)) 
	ASSIGN A(1) -> ((1,8),(3,4),(4,3),(4,8),(5,6),(6,4),(7,1),(7,6),(8,3),(8,8)) 
	ASSIGN A(1) -> ((2,5),(3,5),(4,4),(5,2),(5,7),(6,5),(7,2),(7,7),(8,4)) 
	ASSIGN A(1) -> ((2,6),(3,6),(4,5),(5,3),(5,8),(6,6),(7,3),(7,8),(8,5)) 
	ASSIGN A(1) -> ((2,7),(3,7),(4,6),(5,4),(6,2),(6,7),(7,4),(8,1),(8,6)) 
AEND

ARRAY (7500, 8, 5000)/(42500, 8, 5000)
	CHMPOS M1=(1500, 1500)
	ASSIGN A(1) -> ((1,1),(1,6),(2,3),(2,8),(3,6),(4,4),(5,3),(5,8),(6,8),(8,7)) 
	ASSIGN A(1) -> ((1,2),(1,7),(2,4),(3,2),(3,7),(4,5),(5,4),(6,4),(7,5),(8,8)) 
	ASSIGN A(1) -> ((1,3),(1,8),(2,5),(3,3),(3,8),(4,6),(5,5),(6,5),(7,6)) 
	ASSIGN A(1) -> ((1,4),(2,1),(2,6),(3,4),(4,2),(4,7),(5,6),(6,6),(7,7)) 
	ASSIGN A(1) -> ((1,5),(2,2),(2,7),(3,5),(4,3),(4,8),(5,7),(6,7),(7,8)) 
AEND

ARRAY (-42500, 8, 5000)/(-7500, 8, 5000)
	CHMPOS M1=(1500, 1500)
	ASSIGN A(1) -> ((1,1),(2,4),(3,5),(4,5),(5,4),(6,2),(6,7),(7,5),(8,2),(8,7)) 
	ASSIGN A(1) -> ((1,2),(3,1),(4,1),(4,6),(5,5),(6,3),(7,1),(7,6),(8,3),(8,8)) 
	ASSIGN A(1) -> ((2,1),(3,2),(4,2),(5,1),(5,6),(6,4),(7,2),(7,7),(8,4)) 
	ASSIGN A(1) -> ((2,2),(3,3),(4,3),(5,2),(5,7),(6,5),(7,3),(7,8),(8,5)) 
	ASSIGN A(1) -> ((2,3),(3,4),(4,4),(5,3),(6,1),(6,6),(7,4),(8,1),(8,6)) 
AEND

ARRAY (7500, 8, 5000)/(-7500, 8, 5000)
	CHMPOS M1=(1500, 1500)
	ASSIGN A(1) -> ((1,1),(1,6),(2,3),(2,8),(3,5),(4,3),(5,1),(5,6),(6,5),(8,1)) 
	ASSIGN A(1) -> ((1,2),(1,7),(2,4),(3,1),(3,6),(4,4),(5,2),(6,1),(7,1),(8,2)) 
	ASSIGN A(1) -> ((1,3),(1,8),(2,5),(3,2),(3,7),(4,5),(5,3),(6,2),(7,2)) 
	ASSIGN A(1) -> ((1,4),(2,1),(2,6),(3,3),(4,1),(4,6),(5,4),(6,3),(7,3)) 
	ASSIGN A(1) -> ((1,5),(2,2),(2,7),(3,4),(4,2),(4,7),(5,5),(6,4),(7,4)) 
AEND

1: ARRAY (0, 1, 0)/(0, 1, 0); PADS plus chip marks
	ASSIGN P(1)+A(2) -> ((1,1)) 
AEND

2: ARRAY (-1500, 2, 3000)/(1500, 2, 3000); chip marks
    ASSIGN P(3) -> ((1,1), (1,2), (2,1), (2,2))
    
ARRAY (0, 1, 0)/(0, 1, 0); Labels, GLM marks, lift off assist
	ASSIGN P(2) -> ((1,1)) 
	ASSIGN P(4)+P(5) -> ((1,1)) 

AEND
PEND

LAYER 1
P(1) 'PADS.v30' (0.0,0.0)
P(2) 'WAFER_LABELS.v30' (-1500.0, 2000.0)
P(3) 'MARKER_CROSS.v30' (0.0, 0.0)
P(4) 'GLM_CROSS.v30' (-10000.0, 4000.0)
P(5) 'GLM_CROSS.v30' (0.0, -5000.0)
P(6) 'ALIGN_HORIZ.v30' (-25000.0, 4000.0)

"""
    pads=PADS()
    wafer_labels=Wafer_Labels()
    liftoff_assist=Rectangle()

    marker_cross=Symmetric_Cross(name="MARKER_CROSS", height=400.0e-6, 
                                 linewidth=4.0e-6, color="purple")
    glm_cross=Symmetric_Cross(name="GLM_CROSS", height=1000.0e-6,
                              linewidth=20.0e-6, color="red")

    align_cross_horiz=Cross(name="ALIGN_HORIZ", height=450.0e-6, 
                            width=4000.0e-6, linewidth=50.0e-6, color="red")
    align_cross_vert=Cross(name="ALIGN_VERT", height=4000.0e-6, width=450.0e-6,
                           linewidth=20.0e-6, color="red")
    
    pads.chief.jdf.input_jdf=jdf_text
    pads.show()