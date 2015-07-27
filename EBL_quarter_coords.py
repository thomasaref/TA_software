# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 12:51:22 2015

@author: thomasaref
"""

GLM_dict=dict(A=[(-40000, 4000), (-4000, 40000)],
              B=[(4000, 40000), (40000, 4000)],
              C=[(-40000, -4000), (-4000, -40000)],
              D=[(4000, -40000), (40000, -4000)])

def get_GLM(qw):
    """returns Px, Py, Qx, Qy" for a given quarter wafer"""
    glm=GLM_dict[qw]
    return glm[0][0], glm[0][1], glm[1][0], glm[1][1] 

Array_dict=dict(A=[(-42500,8,5000), (42500,8,5000)],
                B=[(7500,8,5000), (42500,8,5000)],
                C=[(-42500,8,5000), (-7500,8,5000)],
                D=[(7500,8,5000), (-7500,8,5000)])

def get_Array(qw):
    """returns Px, Py, Qx, Qy" for a given quarter wafer"""
    ar=Array_dict[qw]
    return ar[0][0], ar[0][1], ar[0][2], ar[1][0], ar[1][1], ar[1][2]  

def give_GoodCoords(WAFER, BadCoords):
    return [x for x in WAFER if x not in BadCoords]

def get_WaferCoords(qwaf):
    A_WAFER=[                                         (7,1), (8,1),
                                       (5,2), (6,2), (7,2), (8,2),
                                (4,3), (5,3), (6,3), (7,3), (8,3),
                         (3,4), (4,4), (5,4), (6,4), (7,4), (8,4),
                  (2,5), (3,5), (4,5), (5,5), (6,5), (7,5), (8,5),
                  (2,6), (3,6), (4,6), (5,6), (6,6), (7,6), (8,6),
           (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (8,7),
           (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)]
    
    A_BadCoords=[(7,1), (8,1),
               (5,2), (8,2),
               (4,3), (8,3),
               (3,4), (8,4),
               (2,5), (8,5),
               (2,6), (8,6),
               (1,7), (8,7),
               (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8)]
    
    B_WAFER=[(1, 1), (2, 1),
             (1, 2), (2, 2), (3, 2), (4, 2),
             (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
             (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
             (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),
             (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),
             (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7),
             (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
    
    B_BadCoords=[(1, 1), (2, 1),
             (1, 2), (4, 2),
             (1, 3), (5, 3),
             (1, 4), (6, 4),
             (1, 5), (7, 5),
             (1, 6), (7, 6),
             (1, 7), (8, 7),
             (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
        
    C_WAFER=[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
             (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
                     (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3),
                     (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4),
                             (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5),
                                     (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),
                                             (5, 7), (6, 7), (7, 7), (8, 7),
                                                             (7, 8), (8, 8)]
    
    C_BadCoords=[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
                                                                 (1, 2), (8, 2),
                                                                 (2, 3), (8, 3),
                                                                 (2, 4), (8, 4),
                                                                 (3, 5), (8, 5),
                                                                 (4, 6), (8, 6),
                                                                 (5, 7), (8, 7),
                                                                 (7, 8), (8, 8)]
    
    D_WAFER=[(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1),
             (1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2),
             (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3),
             (1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4),
             (1,5), (2,5), (3,5), (4,5), (5,5), (6,5),
             (1,6), (2,6), (3,6), (4,6), (5,6),
             (1,7), (2,7), (3,7), (4,7),
             (1,8), (2,8)]
    
    D_BadCoords=[(1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1),
                 (1,2), (8,2),
                 (1,3), (7,3),
                 (1,4), (7,4),
                 (1,5), (6,5),
                 (1,6), (5,6),
                 (1,7), (4,7),
                 (1,8), (2,8)]
    if qwaf=='A':
        WAFER=A_WAFER
        BadCoords=A_BadCoords
    elif qwaf=='B':
        WAFER=B_WAFER
        BadCoords=B_BadCoords
    elif qwaf=='C':
        WAFER=C_WAFER
        BadCoords=C_BadCoords
    elif qwaf=='D':
        WAFER=D_WAFER
        BadCoords=D_BadCoords
    else:
        print "Bad quarter wafer!"
    GoodCoords=give_GoodCoords(WAFER, BadCoords)
    return WAFER, BadCoords, GoodCoords
    
    #D_GoodCoords=give_GoodCoords(D_WAFER, D_BadCoords)

def numCoords2(Coords, AssignArray):
    return int(len(Coords)//len(AssignArray))

def numCoords(Coords, lengthAA):
    return int(len(Coords)//lengthAA)

#AssignArray=[('A(1)+A(2)+A(15)', 'D32080 with two IDTs and Squid connect'),
#        ('A(1)+A(3)+A(15)', 'S32080 with two IDTs and Squid connect'),
#        ('A(1)+A(4)+A(15)', 'S32050 with two IDTs and Squid connect'),
#        ('A(1)+A(5)+A(15)',  'D32050 with two IDTs and Squid connect'),
#        ('A(1)+A(6)+A(15)',  'D9050 with two IDTs and Squid connect'),
#        ('A(1)+A(7)+A(15)', 'S9050 with two IDTs and Squid connect'),
#        ('A(1)+A(8)+A(15)', 'S9080 with two IDTs and Squid connect'),
#        ('A(1)+A(9)+A(15)', 'D9080 with two IDTs and Squid connect'),
#        ('A(12)+A(10)+A(15)', 'D5080 with two FDTs and Squid connect'),
#        ('A(12)+A(11)+A(15)', 'D5096 with two FDTs and Squid connect'),
#        ('A(13)+A(15)', 'IDT by itself'),
#        ('A(14)+A(15)', 'FDT by itself'),
#        ('A(1)+A(15)',  'Two IDTs alone with squid connect'),
#        ('A(12)+A(15)', 'two FDTs alone with squid connect')]


#print numBadCoords, numGoodCoords

def distr_one_coord(i, BadCoords, GoodCoords, numBadCoords, numGoodCoords, numSkip):
    templist=[BadCoords[n*numSkip+i] for n in range(numBadCoords)]
    templist.extend([GoodCoords[m*numSkip+i] for m in range(numGoodCoords)])
    leftover=len(BadCoords)-numBadCoords*numSkip
    if numBadCoords*numSkip+i<len(BadCoords):
        templist.append(BadCoords[(numBadCoords)*numSkip+i])
    elif numGoodCoords*numSkip-leftover+i<len(GoodCoords):
        templist.append(GoodCoords[numGoodCoords*numSkip-leftover+i])
    if numGoodCoords*numSkip-leftover+numSkip+i<len(GoodCoords):
        templist.append(GoodCoords[(numGoodCoords+1)*numSkip-leftover+i])
    return templist
    
def distribute_coords(lengthAA, qwaf='A'):#BadCoords, WAFER):
    WAFER, BadCoords, GoodCoords=get_WaferCoords(qwaf=qwaf)
    numGoodCoords=numCoords(GoodCoords, lengthAA)
    numBadCoords=numCoords(BadCoords, lengthAA)
    numSkip=lengthAA
    return [distr_one_coord(i, BadCoords, GoodCoords, numBadCoords, numGoodCoords, numSkip) for i in range(lengthAA)]

def distr_coords2(AssignArray, qwaf='A'):#BadCoords, WAFER):
    WAFER, BadCoords, GoodCoords=get_WaferCoords(qwaf=qwaf)
    numGoodCoords=numCoords(GoodCoords, AssignArray)
    numBadCoords=numCoords(BadCoords, AssignArray)
    numSkip=len(AssignArray)    
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
    tempstr=tempstr[:-2]
    
    #if (m+1)*numSkip+i<len(GoodCoords):
    #    tempstr+=str(GoodCoords[(m+1)*numSkip+i])+", "
#    print "ASSIGN {arrays} -> ({nums}{dose}) ;{comment}".format(arrays=item[0], comment=item[1], nums=tempstr[:-2], dose="")
