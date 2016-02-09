# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:17:26 2015

@author: thomasaref
"""

from atom.api import Atom, Unicode, Typed, List, cached_property
from taref.tex.tex_backbone import (texwrap, include_figure, extract_block, make_table,
                                     mult_fig_start, mult_fig_end, add_mult_fig, include_image, compile_tex)

from collections import OrderedDict

from taref.core.agent import SubAgent as Operative
from enaml import imports
with imports():
    from tex_e import TEX_Window

def line_check(line):
    inline=line.strip()
    if inline.startswith("\pyb"):
        line_check.inblock=True
        line_check.key=line.split("\pyb")[1].split("{")[1].split("}")[0].strip()
        #return False
    elif inline.startswith("\pye"):
        line_check.inblock=False
        return True
    if line_check.inblock:
        tlist=line_check.dict.get(line_check.key, [])
        tlist.append(line)
        line_check.dict[line_check.key]=tlist
    return False #line_check.inblock
line_check.inblock=False
line_check.key=""
line_check.dict={}

from itertools import izip


class TEX(Operative):

    #read_file=Typed(Read_File)
    #write_file=Typed(Write_File)

    tex_list=List()
    input_code=Unicode()
    input_tex=Unicode()
    input_tex_list=List()
    output_tex=Unicode()
    source_tex=List()

    source_dict=Typed(OrderedDict, ())

    index_list=List()
    tlist=List()
    def make_input_tex(self):
        self.index_list=[]
        self.tlist=[]
        for line in self.input_code.split("\n"):
            line=line.strip()
            key=None
            if line.startswith("tx.ext("):
                try:
                    key=line.split("tx.ext('")[1].split("')")[0]
                except IndexError:
                    key=line.split('tx.ext("')[1].split('")')[0]
            self.tlist.append(line)
            self.index_list.append(None)
            if key is not None:
                source_list=zip(*[(key, "#"+item) for item in self.source_dict[key]])
                self.index_list.extend(source_list[0])
                self.tlist.extend(source_list[1])
        self.input_tex="\n".join(self.tlist)

    def _observe_input_tex(self, change):

        if change["type"]=="update":
            #self.make_input_tex()
            lineno=[n for n, (line1, line2) in enumerate(izip(change["oldvalue"].split("\n"), self.input_tex.split("\n"))) if line1 != line2][0]
            print lineno, self.index_list[lineno]
            key=self.index_list[lineno]
            if key is not None:
                #source_dict[key]=
                print [line for n, line in enumerate(self.tlist) if self.index_list[n]==key]

    def process_source_tex(self):
        for n, line in enumerate(self.source_tex):
            line=line.strip()
            if line.startswith("\pyb"):
                index=n+1
                key=line.split("\pyb")[1].split("{")[1].split("}")[0].strip()
            elif line.startswith("\pye"):
                self.source_dict[key]=["# "+item for item in self.source_tex[index:n]]


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
        self.tex_list.append(inline)

    def extract_block(self, name):
        return extract_block(name, self.source_tex)

    def ext(self, block_name):
        temp_list=self.extract_block(block_name)
        self.extend(temp_list)

    def extend(self, inlist):
        self.tex_list.extend(inlist)

    def make_table(self, table_values, table_format=None):
        make_table(self.tex_list, table_values, table_format)


    def mult_fig_start(self):
        mult_fig_start(self.tex_list)

    def mult_fig_end(self, caption):
        mult_fig_end(self.tex_list, caption)

    def add_mult_fig(self, graph_gen, fig_name, caption="", label="", **kwargs):
        return add_mult_fig(graph_gen, self.tex_list, self.dir_path, fig_name, caption, label, **kwargs)

    def include_image(self, fig_name, caption="", label=""):
        include_image(self.tex_list, self.dir_path, fig_name, caption, label)

    @cached_property
    def view_window(self):
        return TEX_Window(agent=self)

if __name__=="__main__":
    from taref.core.shower import shower
    tx=TEX()
    #tex_source="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A45_cooldown1/tikztry.tex"
    #print extract_block("sam", str_list)

    #print extract_block("bob", str_list)

    tx.source_tex="""\pyb {summary}
    \section{Summary}
    This is an attempt at reducing the coupling by changing the spacing of the fingers pairs on the qubit IDT, pushing them to a higher frequency. The coupling appears reduced by an order of magnitude and the qubit seems to be operating as a qubit. Unfortunately, the qubit frequency is below the IDT listening/talking frequency so it is never directly on resonance (this could be easily fixed by having less resistive junctions). Speedy was also experiencing quite a bit of trouble with blockages so the temperature was often in the 50-80 mK range.

\pye

\pyb {second entry}
this is the second entry
\pye""".split("\n")

    tx.input_code="""tx.ext("summary")

    tx.ext("second entry")"""
    tx.process_source_tex()
    tx.make_input_tex()
    print tx.source_dict
    if 1:
        qubit_values=[[r"Qubit"                                  ,  r"{}"                             ],
                      [r"Finger type"                            ,  r"double finger"                  ],
                      [r"Number of finger pairs, $N_{pq}$"      ,  r"9"                              ],
                      [r"Overlap length, $W$"                   ,  r"25 $\mu$m"                      ],
                      [r"finger width, $a_q$"                   ,  r"80 nm"                           ],
                      [r"DC Junction Resistances"               ,  r"8.93 k$\Omega$, 9.35k$\Omega$"  ],
                      [r"Metallization ratio"                   ,  r"50\%"                           ]]


        tx.add(r"\subsection{Qubit values}")
        tx.make_table(qubit_values, r"|p{5 cm}|p{3 cm}|")

    shower(tx)