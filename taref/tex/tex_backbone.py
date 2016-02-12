# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 05:20:56 2016

@author: thomasaref

functions for creating latex documents
"""

from matplotlib.pyplot import savefig, close
from subprocess import call
from taref.core.universal import write_text

from contextlib import contextmanager
from os import chdir, getcwd

@contextmanager
def cd(newdir):
    """a context manager that changes directory to newdir during it's context and switches back to the starting directory when done"""
    prevdir = getcwd()
    chdir(newdir)
    try:
        yield
    finally:
        chdir(prevdir)

def compile_tex(dir_path, file_name, cmd="/usr/texbin/pdflatex"):
    """uses subprocess call to compile and show pdf using pdflatex.
    Might need to check path of pdflatex command with which command in terminal"""
    with cd(dir_path):
        call([cmd, file_name+".tex"])
        call(["open", file_name+".pdf"])

def extract_block(name, str_list):
    """reads a block in a latex document marked with the commands \pyb and \pye"""
    extract_list=[]
    inblock=False
    for line in str_list:
        if line.startswith("\pyb".strip()):
            if line.split("{")[1].split("}")[0].strip()==name:
                inblock=True
        if inblock:
            extract_list.append(line)
            if line.startswith("\pye"):
                return extract_list[1:-1]
    return extract_list[1:]


def texwrap(dir_path, file_name, intex):
    """wraps the tex list with the necessary beginning and end and write it to file"""
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

    write_text(dir_path+file_name, tex)

def include_image(tex, dir_path, fig_name, caption="", label=""):
    """inserts th image specified by dir_path and fig_name into the list tex"""
    tex.append(r"\begin{figure}[ht!]")
    tex.append(r"\centering")
    tex.append("\\includegraphics[width=\\textwidth]{{{}}}".format(fig_name))
    tex.append("\\caption{{{}}}".format(caption))
    tex.append("\\label{{{}}}".format(label))
    tex.append(r"\end{figure}")

def include_figure(graph_gen, tex, dir_path, fig_name, caption="", label="", **kwargs):
    """uses the passed function graph_gen and kwargs to generate a figure and save it to the given file path"""
    graph_gen(**kwargs)
    file_name=graph_gen.func_code.co_filename.split("Documents")[1]
    caption="{0}  Analysis: \\verb;{1};".format(caption, file_name)
    tex.append(r"\begin{figure}[ht!]")
    tex.append(r"\centering")
    tex.append("\\includegraphics[width=\\textwidth]{{{}}}".format(fig_name))
    tex.append("\\cprotect\\caption{{{}}}".format(caption))
    tex.append("\\label{{{}}}".format(label))
    tex.append(r"\end{figure}")
    savefig(dir_path+fig_name, bbox_inches='tight')
    close()

def mult_fig_start(tex):
    """starts a multi figure with many subfigures"""
    tex.extend([r"\setcounter{subfigure}{0} % reset figure counter to 0.",
               r"\begin{figure}[ht!]",
               r"\centering"])

def mult_fig_end(tex, caption):
    """ends a multi figure with many subfigues"""
    tex.extend([r"\label{fig:setup}",
               "\\cprotect\\caption{{{}}}".format(caption),
               r"\end{figure}"])

def add_mult_fig(graph_gen, tex, dir_path, fig_name, caption="", label="", width=0.49, **kwargs):
    """adds a graph to a multi figure using the function graph_gen and given kwargs"""
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
    """makes a latex table from table values"""
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
