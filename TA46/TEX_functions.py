# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 17:17:26 2015

@author: thomasaref
"""

from matplotlib.pyplot import savefig, close

    
def texwrap(dir_path, file_name, intex):
    tex=[]
    tex.append(r"\documentclass[12pt,a4paper]{article}")
    tex.append(r"\usepackage[top=1 in,  bottom=1 in, left=1 in, right=1 in]{geometry}")
    tex.append(r"\usepackage{amsfonts,amssymb,amsmath}")
    tex.append(r"\usepackage{graphicx}")
    tex.append(r"\usepackage{hyperref}")
    tex.append(r"\usepackage{color}")
    tex.append(r"%\usepackage{tikz}")
    tex.append(r"%\usepackage[siunitx]{circuitikz}")
    tex.append(r"%\usepackage{cite}")
    tex.append(r"\usepackage{caption}")
    tex.append(r"\usepackage{subcaption}")
    tex.append(r"\usepackage{rotating}")
    tex.append(r"\usepackage{paralist}")
    tex.append(r"\usepackage{cprotect}")
    tex.append(r"")
    tex.append(r"\definecolor{red}{rgb}{1, 0, 0}   %used for making comments in red color text")
    tex.append(r"\definecolor{green}{rgb}{0, 0.7, 0}")
    tex.append(r"\definecolor{blue}{rgb}{0, 0, 1}")
    tex.append(r"\newcommand{\mc}{\textcolor{red}}  %used for making comments in red color text remove before submit")
    tex.append(r"\newcommand{\mg}{\textcolor{green}}  %used for making comments in red color text remove before submit")
    tex.append(r"\newcommand{\mb}{\textcolor{blue}}  %used for making comments in red color text remove before submit")
    tex.append(r"\newcommand{\comment}[1]{}  %used for commenting out blocks of text remove before submit")
    tex.append(r"")
    tex.append(r"")
    
    tex.append(r"\begin{document}")
    tex.append(r"\author{Thomas Aref}")
    tex.append(r"%\inst{3} Department of Microtechnology and Nanoscience (MC2), Chalmers University of Technology, SE-412 96 G\"oteborg, Sweden")
    tex.append(r"\title{Sample TA210715A46 in Speedy 3-10-15 cooldown}")
    tex.append(r"\maketitle")
    tex.append(r"\noindent")
    
    tex.extend(intex)
    tex.append(r"\end{document}")
    
    with open(dir_path+file_name, "w") as f:
        f.write("\n".join(tex))

def include_image(tex, dir_path, fig_name, caption="", label=""):
    tex.append(r"\begin{figure}[ht!]")
    tex.append(r"\centering")
    tex.append("\\includegraphics[width=\\textwidth]{{{}}}".format(fig_name))
    tex.append("\\caption{{{}}}".format(caption))
    tex.append("\\label{{{}}}".format(label))
    tex.append(r"\end{figure}")
        
def include_figure(graph_gen, tex, dir_path, fig_name, caption="", label="", **kwargs):
    graph_gen(**kwargs)
    file_name=graph_gen.func_code.co_filename.split("Documents")[1]
    #if capt is None:
    caption="{0}  Analysis: \\verb;{1};".format(caption, file_name)
    #else:
    #caption="{0} \\\\ {1} \\\\ Analysis: \\verb;{2};".format(caption, capt, file_name)
    tex.append(r"\begin{figure}[ht!]")
    tex.append(r"\centering")
    tex.append("\\includegraphics[width=\\textwidth]{{{}}}".format(fig_name))
    tex.append("\\cprotect\\caption{{{}}}".format(caption))
    tex.append("\\label{{{}}}".format(label))
    tex.append(r"\end{figure}")
    savefig(dir_path+fig_name, bbox_inches='tight')
    close()

def mult_fig_start(tex):
    tex.append(r"\setcounter{subfigure}{0} % reset figure counter to 0.")
    tex.append(r"\begin{figure}[ht!]")
    tex.append(r"\centering")

def mult_fig_end(tex, caption):
    tex.append(r"\label{fig:setup}")
    tex.append("\\cprotect\\caption{{{}}}".format(caption))
    tex.append(r"\end{figure}")

def add_mult_fig(graph_gen, tex, dir_path, fig_name, caption="", label="", width=0.49, **kwargs):
    graph_gen(**kwargs)
    file_name=graph_gen.func_code.co_filename.split("Documents")[1]
    savefig(dir_path+fig_name, bbox_inches='tight')
    close()

    tex.append("\\begin{{subfigure}}[b]{{{}\\textwidth}}".format(width))
    tex.append("\\includegraphics[width=\\textwidth]{{{}}}".format(fig_name))
    tex.append("\\cprotect\\caption{{{}}}".format(caption))
    tex.append(r"\end{subfigure}")
    return "Analysis: \\verb;{0};".format(file_name)
    
def make_table(tex, table_values, table_format=None):
    if table_format is None:
        table_format="|"
        for a in table_values[0]:
            table_format+=r"p{3 cm}|"
    tex.append("\\begin{{tabular}}{{{}}}".format(table_format))
    tex.append(r"\hline")
    for a in table_values:
        table_line=""
        for b in a:
            table_line="{0} & {1}".format(table_line, b)
        table_line=table_line[2:]+r" \\"
        tex.append(table_line)    
        tex.append(r"\hline")
    tex.append(r"\end{tabular}")
    tex.append(r"")
    
class TEX(object):
    def __init__(self, dir_path, file_name):
        self.dir_path=dir_path
        self.file_name=file_name
        self.tex=[]

    def make_tex_file(self):
        texwrap(self.dir_path, self.file_name, self.tex)   
    
    def include_figure(self, graph_gen, fig_name, caption="", label="", **kwargs):
        include_figure(graph_gen, self.tex, self.dir_path, fig_name, caption, label, **kwargs) 

    def add(self, inline):
        self.tex.append(inline)
    
    def ext(self, inlist):
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