# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:38:47 2015

@author: thomasaref
"""

from Atom_Base import Base
from atom.api import Str

class JDFViewer(Base):
    jdf_file=Str()
    
if __name__=="__main__":
    a=JDFViewer(name="blah")
    a.show()