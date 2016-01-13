# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 16:36:03 2015

@author: thomasaref
"""

from taref.ebl.pads import PADS
from taref.ebl.wafer_labels import Wafer_Labels, Digit
from taref.ebl.cross import Cross, Symmetric_Cross, Symmetric_Inverse_Cross
from taref.ebl.rectangle import Rectangle#, Dashed_Line_Horiz
from taref.ebl.wafer_aligner import Wafer_Aligner, Wafer_Width_Checker

if __name__=="__main__":
    jdf_text="""
PATH
ARRAY (-42500, 8, 5000)/(42500, 8, 5000); A part
   CHMPOS M1=(1500, 1500)
   ASSIGN A(1)+P(11)+P(26) -> ((1,7)); GLM cross left, small cross top left
   ASSIGN A(1)+P(11)+P(25)+P(13) -> ((1,8)); GLM cross left and bottom, small cross bottom left
   ASSIGN P(10) -> ((1,5), (1,6), (2,4), (3,3), (4,2), (5,1), (6,1)); GLM cross centered off chips
   ASSIGN A(1)+P(13) -> ((2,8), (3,8), (4,8), (6,8), (7,8)); GLM cross on bottom
   ASSIGN A(1)+P(6) -> ((5,8)); horizontal alignment cross on bottom
   ASSIGN A(1)+P(23)+P(22) -> ((8,8)) ; small GLM on bottom and on right
   ASSIGN A(1)+P(12) -> ((8,2), (8,3), (8,4), (8,6), (8,7)); GLM cross on right
   ASSIGN A(1)+P(9) -> ((8,5)); vertical alignment cross on right
   ASSIGN A(1)+P(12)+P(14)+P(28) -> ((8,1)); GLM cross on right and on top, small cross top right
   ASSIGN A(1)+P(14)+P(26) -> ((7,1)); GLM cross on top, small cross top left

   ASSIGN A(1) -> (                  (5,2),(6,2),(7,2))
   ASSIGN A(1) -> (            (4,3),(5,3),(6,3),(7,3))
   ASSIGN A(1) -> (      (3,4),(4,4),(5,4),(6,4),(7,4))
   ASSIGN A(1) -> ((2,5),(3,5),(4,5),(5,5),(6,5),(7,5))
   ASSIGN A(1) -> ((2,6),(3,6),(4,6),(5,6),(6,6),(7,6))
   ASSIGN A(1) -> ((2,7),(3,7),(4,7),(5,7),(6,7),(7,7))
AEND

ARRAY (7500, 8, 5000)/(42500, 8, 5000); B part
    CHMPOS M1=(1500, 1500)
    ASSIGN A(1)+P(11) -> ( (1,2), (1,3), (1,4), (1,6), (1,7)); GLM cross left
    ASSIGN A(1)+P(13) -> ( (2,8), (3,8), (5,8), (6,8), (7,8); GLM cross bottom
    ASSIGN A(1)+P(14)+P(28) -> ((2,1)); GLM cross on top, small cross top right
    ASSIGN A(1)+P(14)+P(11)+P(26) -> ((1,1)); GLM cross on top and on left, small cross top left
    ASSIGN A(1)+P(12)+P(28) -> ((8,7)); GLM cross on right, small cross top right
    ASSIGN A(1)+P(13)+P(12)+P(27) -> ((8,8)); GLM cross on top and on left, small cross top left
    ASSIGN A(1)+P(21)+P(23) -> ((1,8)); small cross left and bottom
    ASSIGN A(1)+P(6) -> ((4,8)); horizontal alignment cross on bottom
    ASSIGN A(1)+P(8) -> ((1,5)); vertical alignment cross on left


    ASSIGN P(10) -> ((3,1), (4,1), (5,2), (6,3), (7,4), (8,5), (8,6)); GLM cross centered off chips

	ASSIGN A(1) -> ((2,2),(3,2),(4,2))
	ASSIGN A(1) -> ((2,3),(3,3),(4,3),(5,3))
	ASSIGN A(1) -> ((2,4),(3,4),(4,4),(5,4),(6,4))
	ASSIGN A(1) -> ((2,5),(3,5),(4,5),(5,5),(6,5),(7,5))
	ASSIGN A(1) -> ((2,6),(3,6),(4,6),(5,6),(6,6),(7,6))
 	ASSIGN A(1) -> ((2,7),(3,7),(4,7),(5,7),(6,7),(7,7))
AEND

ARRAY (-42500, 8, 5000)/(-7500, 8, 5000); C part
    CHMPOS M1=(1500, 1500)
    ASSIGN A(1)+P(11)+P(26)+P(14) -> ((1,1)); GLM cross left and top, small cross top left
    ASSIGN A(1)+P(11)+P(25) -> ((1,2)); GLM cross left and bottom, small cross bottom left
    ASSIGN P(10) -> ((1,3), (1,4), (2,5), (3,6), (4,7), (5,8), (6,8)); GLM cross centered off chips
    ASSIGN A(1)+P(14) -> ((2,1), (3,1), (4,1), (6,1), (7,1)); GLM cross on top
    ASSIGN A(1)+P(7) -> ((5,1)); horizontal alignment cross on top
    ASSIGN A(1)+P(24)+P(22) -> ((8,1)) ; small GLM on top and on right
    ASSIGN A(1)+P(12) -> ((8,2), (8,3), (8,5), (8,6), (8,7)); GLM cross on right
    ASSIGN A(1)+P(9) -> ((8,4)); vertical alignment cross on right
    ASSIGN A(1)+P(12)+P(13)+P(27) -> ((8,8)); GLM cross on right and on bottom, small cross bottom right
    ASSIGN A(1)+P(13)+P(25) -> ((7,8)); GLM cross on bottom, small cross bottom left

    ASSIGN A(1) -> ((2,2), (3,2),(4,2), (5,2), (6,2), (7,2))
    ASSIGN A(1) -> ((2,3), (3,3),(4,3), (5,3), (6,3), (7,3))
    ASSIGN A(1) -> ((2,4), (3,4),(4,4), (5,4), (6,4), (7,4))
    ASSIGN A(1) -> (       (3,5),(4,5), (5,5), (6,5), (7,5))
    ASSIGN A(1) -> (             (4,6), (5,6), (6,6), (7,6))
    ASSIGN A(1) -> (                    (5,7), (6,7), (7,7))
AEND

ARRAY (7500, 8, 5000)/(-7500, 8, 5000); D part
    CHMPOS M1=(1500, 1500)
    ASSIGN A(1)+P(11) -> ((1,2), (1,3), (1,5), (1,6), (1,7)); GLM cross left
    ASSIGN A(1)+P(14) -> ((2,1), (3,1), (5,1), (6,1), (7,1)); GLM cross on top
    ASSIGN A(1)+P(13)+P(27) -> ((2,8)); GLM cross on bottom, small cross bottom right
    ASSIGN A(1)+P(11)+P(13)+P(25) -> ((1,8)); GLM cross on bottom and on left, small cross bottom left
    ASSIGN A(1)+P(12)+P(28)+P(14) -> ((8,1)); GLM cross on top and on right, small cross top right
    ASSIGN A(1)+P(12)+P(27) -> ((8,2)); GLM cross on top and on right, small cross top left
    ASSIGN A(1)+P(21)+P(24) -> ((1,1)); small cross left and top
    ASSIGN A(1)+P(7) -> ((4,1)); horizontal alignment cross on top
    ASSIGN A(1)+P(8) -> ((1,4)); vertical alignment cross on left
    ASSIGN P(10) -> ((3,8), (4,8), (5,7), (6,6), (7,5), (8,4), (8,3)); GLM cross centered off chips

    ASSIGN A(1) -> ((2,2), (3,2), (4,2), (5,2), (6,2), (7,2))
    ASSIGN A(1) -> ((2,3), (3,3), (4,3), (5,3), (6,3), (7,3))
    ASSIGN A(1) -> ((2,4), (3,4), (4,4), (5,4), (6,4), (7,4))
    ASSIGN A(1) -> ((2,5), (3,5), (4,5), (5,5), (6,5))
    ASSIGN A(1) -> ((2,6), (3,6), (4,6), (5,6))
    ASSIGN A(1) -> ((2,7), (3,7), (4,7),
AEND

1: ARRAY (0, 1, 0)/(0, 1, 0); PADS plus chip marks
	ASSIGN A(2)+A(3)+P(4)+P(5) -> ((1,1))
AEND

2: ARRAY (0, 1, 0)/(0, 1, 0); PADS
	ASSIGN P(1) -> ((1,1))
AEND

3: ARRAY (-1500, 2, 3000)/(1500, 2, 3000); chip marks for one chip
    ASSIGN P(3) -> ((1,1), (1,2), (2,1), (2,2))

4: ARRAY(-2000, 2, 4000)/(25000, 2, 50000)
	ASSIGN P(36) -> ((1,1), (1,2), (2,1), (2,2)); vert short lines

5: ARRAY(-25000, 2, 50000)/(2000, 2, 4000)
	ASSIGN P(37) -> ((1,1), (1,2), (2,1), (2,2)); horiz short lines

ARRAY (0, 1, 0)/(0, 1, 0); Labels, lift off assist
	ASSIGN P(2) -> ((1,1)); wafer labels
	ASSIGN P(30)+P(31)+P(32)+P(33) -> ((1,1)); big letters
	ASSIGN P(34)+P(35) -> ((1,1)); long dicing lines
	ASSIGN A(4)+A(5) -> ((1,1)); long dicing lines
     ASSIGN P(40)+P(41)+P(42)+P(43) -> ((1,1)) ; Wafer aligner


AEND
PEND

LAYER 1
P(1) 'PADS.v30' (0.0,0.0)
P(2) 'WAFER_LABELS.v30' (-1500.0, 2000.0)

P(3) 'MARKER_CROSS.v30' (0.0, 0.0)
P(4) 'PHOTO_CROSS.v30' (-1400.0, -1730.0)
P(5) 'INV_PHOTO_CROSS.v30' (-1600.0, -1730.0)

P(6) 'ALIGN_HORIZ.v30' (0.0, -3500.0); bottom
P(7) 'ALIGN_HORIZ.v30' (0.0, 3500.0); top
P(8) 'ALIGN_VERT.v30' (-3500.0, 0.0); left
P(9) 'ALIGN_VERT.v30' (3500.0, 0.0); right

P(10) 'GLM_CROSS.v30' (0.0, 0.0) ;centered GLM
P(11) 'GLM_CROSS.v30' (-3500.0, 0.0) ;left GLM
P(12) 'GLM_CROSS.v30' (3500.0, 0.0) ;right GLM
P(13) 'GLM_CROSS.v30' (0.0, -3500.0, 0.0) ;bottom GLM
P(14) 'GLM_CROSS.v30' (0.0, 3500.0) ;top GLM

P(20) 'SMALL_GLM_CROSS.v30' (0.0, 0.0) ;centered GLM
P(21) 'SMALL_GLM_CROSS.v30' (-3500.0, 0.0) ;left GLM
P(22) 'SMALL_GLM_CROSS.v30' (3500.0, 0.0) ;right GLM
P(23) 'SMALL_GLM_CROSS.v30' (0.0, -3500.0, 0.0) ;bottom GLM
P(24) 'SMALL_GLM_CROSS.v30' (0.0, 3500.0) ;top GLM

P(25) 'SMALL_GLM_CROSS.v30' (-3500.0, -3500.0) ;bottom_left GLM
P(26) 'SMALL_GLM_CROSS.v30' (-3500.0, 3500.0) ;top_left GLM
P(27) 'SMALL_GLM_CROSS.v30' (3500.0, -3500.0) ;bottom_right GLM
P(28) 'SMALL_GLM_CROSS.v30' (3500.0, 3500.0) ;top_right GLM



P(30) 'BIG_A.v30' (-3000.0, 3000.0)
P(31) 'BIG_B.v30' (3000.0, 3000.0)
P(32) 'BIG_C.v30' (-3000.0, -3000.0)
P(33) 'BIG_D.v30' (3000.0, -3000.0)
P(34) 'HORIZ_LONG_LINE.v30' (0.0, 0.0)
P(35) 'VERT_LONG_LINE.v30' (0.0, 0.0)

P(36) 'VERT_SHORT_LINE.v30' (0.0, 0.0)
P(37) 'HORIZ_SHORT_LINE.v30' (0.0, 0.0)

P(40) 'HORIZ_W_ALIGN' (0.0, -48130.0)
P(41) 'VERT_W_ALIGN' (-48130.0, 0.0)
P(42) 'HORIZ_W_ALIGN' (0.0, 48130.0)
P(43) 'VERT_W_ALIGN' (48130.0, 0.0)


"""
    pads=PADS()
    wafer_labels=Wafer_Labels()
    liftoff_assist=Rectangle()

    marker_cross=Symmetric_Cross(name="MARKER_CROSS", height=400.0e-6,
                                 linewidth=4.0e-6, color="purple")

    glm_cross=Symmetric_Cross(name="GLM_CROSS", height=1000.0e-6,
                              linewidth=20.0e-6, color="red")

    small_glm_cross=Symmetric_Cross(name="SMALL_GLM_CROSS", height=250.0e-6,
                              linewidth=25.0e-6, color="red")

    align_cross_horiz=Cross(name="ALIGN_HORIZ", height=450.0e-6,
                            width=4000.0e-6, linewidth=50.0e-6, color="red")
    align_cross_vert=Cross(name="ALIGN_VERT", height=4000.0e-6, width=450.0e-6,
                           linewidth=20.0e-6, color="red")

    big_A=Digit(name="BIG_A", digit="A", digit_height=2500.0e-6, lettering_width=350.0e-6)
    big_B=Digit(name="BIG_B", digit="B", digit_height=2500.0e-6, lettering_width=350.0e-6)
    big_C=Digit(name="BIG_C", digit="C", digit_height=2500.0e-6, lettering_width=350.0e-6)
    big_D=Digit(name="BIG_D", digit="D", digit_height=2500.0e-6, lettering_width=350.0e-6)

    photo_cross=Symmetric_Cross(name="PHOTO_CROSS", height=100.0e-6, linewidth=10.0e-6)
    inv_photo_cross=Symmetric_Inverse_Cross(name="INV_PHOTO_CROSS", height=120.0e-6, linewidth=12.0e-6)
    #dashed_line_horiz=Dashed_Line_Horiz(name="DASHED_LINE_HORIZ")
    horiz_long_line=Rectangle(name="HORIZ_LONG_LINE", height=1.0e-3, width=85.0e-3)
    vert_long_line=Rectangle(name="VERT_LONG_LINE", height=85.0e-3, width=1.0e-3)
    horiz_short_line=Rectangle(name="HORIZ_SHORT_LINE", height=0.5e-3, width=40.0e-3)
    vert_short_line=Rectangle(name="VERT_SHORT_LINE", height=40.0e-3, width=0.5e-3)

    wafer_align=Wafer_Aligner(name="HORIZ_W_ALIGN")
    wafer_align=Wafer_Aligner(name="VERT_W_ALIGN", angle=90.0)

    pads.chief.jdf.input_jdf=jdf_text
    pads.show()