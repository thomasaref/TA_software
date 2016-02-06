# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:17:26 2015

@author: thomasaref
"""

from atom.api import Atom, Unicode, Typed, List   
from taref.core.tex_backbone import (texwrap, include_figure, extract_block, make_table,
                                     mult_fig_start, mult_fig_end, add_mult_fig, include_image, compile_tex)

class TEX(Atom):
    
    read_file=Typed(Read_File)
    write_file=Typed(Write_File)
    
    tex=List()
    tex_input=Unicode()    
    tex_output=Unicode()
    
#    """wrapper object which combines tex functions"""
#    def __init__(self, dir_path, file_name, tex_source=None):
#        self.dir_path=dir_path
#        self.file_name=file_name
#        self.tex=[]
#        if tex_source is None:
#            self.str_list=None
#        else:
#            self.str_list=read_tex(tex_source)
    def compile_tex(self):
        compile_tex(self.dir_path, self.file_name)

    def make_tex_file(self):
        texwrap(self.dir_path, self.file_name, self.tex)   
    
    def include_figure(self, graph_gen, fig_name, caption="", label="", **kwargs):
        include_figure(graph_gen, self.tex, self.dir_path, fig_name, caption, label, **kwargs) 

    def add(self, inline):
        self.tex.append(inline)

    def extract_block(self, name):
        return extract_block(name, self.str_list)
        
    def ext(self, block_name):
        temp_list=self.extract_block(block_name)
        self.extend(temp_list)
        
    def extend(self, inlist):
        self.tex.extend(inlist)
        
    def make_table(self, table_values, table_format=None):
        make_table(self.tex, table_values, table_format)
        

    def mult_fig_start(self):
        mult_fig_start(self.tex)

    def mult_fig_end(self, caption):
        mult_fig_end(self.tex, caption)

    def add_mult_fig(self, graph_gen, fig_name, caption="", label="", **kwargs):
        return add_mult_fig(graph_gen, self.tex, self.dir_path, fig_name, caption, label, **kwargs)
        
    def include_image(self, fig_name, caption="", label=""):
        include_image(self.tex, self.dir_path, fig_name, caption, label)        