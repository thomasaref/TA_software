# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:08:41 2016

@author: thomasaref
"""

from taref.saw.qdt import QDT
from taref.saw.idt import IDT
from taref.core.atom_extension import get_tag

qdt=QDT(material='LiNbYZ',
        ft="double",
        a=80.0e-9,
        Np=9,
        Rn=(3570.0+4000.0)/2.0,
        W=25.0e-6,
        eta=0.5)

idt=IDT(material='LiNbYZ',
        ft="double",
        Np=36,
        W=25.0e-6,
        eta=0.5,
        a=96.0e-9)

if __name__=="__main__":
    print get_tag(qdt, "a", "unit")
    print qdt.latex_table()
    qdt.show()
