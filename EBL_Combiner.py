# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:18:34 2015

@author: thomasaref
"""

from EBL_Item import EBL_Item
from atom.api import Enum
from LOG_functions import log_debug

class EBL_Combiner(EBL_Item):
    
    subitems=Enum("None").tag(desc="names of drawing functions to call")

    def make_polylist(self):
        for item in self.get_member("subitems").items:
            subitem=self.get_map("subitems", item)
            #log_debug(item)
            #log_debug(subitem)
            subitem.predraw()            
            self.polys.extend(subitem.polys)
            
    def _default_main_params(self):
        return ["plot", "view_type", "offset_verts", "rotate", "horiz_refl", "vert_refl", "clear_polylist"]#, "subitems"]