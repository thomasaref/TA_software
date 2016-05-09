# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 19:14:03 2016

@author: thomasaref
"""

from sys import exc_info
from os.path import basename
from atom.api import Atom, Unicode, Bool, List, Typed, Dict, cached_property, Int
from enaml import imports
with imports():
    from taref.core.ipython_e import InteractiveWindow

import sys

def f_top_finder(fb):
    """A recursive top frame finder"""
    if fb.f_back is None:
        return fb
    return f_top_finder(fb.f_back)

def f_top_limited(fb, n=100):
    """A limited recursion top frame finder"""
    for m in range(n):
        if fb.f_back is None:
            return fb
        fb=fb.f_back
    return fb

def f_top(n=100):
    """returns the top frame after n steps. n defaults to 100"""
    try:
        raise Exception
    except:
        fb=exc_info()[2].tb_frame.f_back
    return f_top_limited(fb, n)

def msg(*args, **kwargs):
    """log msg that accepts multiple args with file info"""
    n=kwargs.pop("n", 1)
    fb=f_top(n)
    return "{0} {1} {2}: {3}".format(fb.f_lineno, basename(fb.f_code.co_filename),
              fb.f_code.co_name, ", ".join([str(arg) for arg in args]))



class File_Parser(Atom):
    """a callable object for extracting the strings in a list between starter and stopper. For use when parsing text files"""
    starter=Unicode(".")
    stopper=Unicode(".")
    inblock=Bool(False)
    local_name=Unicode()
    preamble=List()
    postamble=List()

    def __call__(self, line):
        """meant for use inside a list comprehension. will return True or False depending on if line is in
        between starter and stopper. If starter is ".", all code will end up in the preamble.
        If local_name does not match for stopper, stopping will be skipped
        local name is extracted as the first thing before starter.
        preamble is the list of lines before starter is reached, (indicated by local_name not being set)
        postamble is the list of lines after stopper."""
        line=line.strip()
        if self.starter in line and self.starter!="." and not line.startswith("#") and self.local_name=="":
            self.inblock=True
            self.local_name=line.split(self.starter)[0]
        elif self.stopper in line and self.stopper!="." and not line.startswith("#"):
            if line.split(self.stopper)[0]==self.local_name:
                self.inblock=False
                return True
        if not self.inblock:
            if self.local_name=="":
                self.preamble.append(line)
            else:
                self.postamble.append(line)
        return self.inblock

class Interact(Atom):
    input_code=Unicode()
    file_reader=Typed(File_Parser)
    locals_dict=Dict()
    file_read=False
    exec_on_enter=Bool(False)

    log_height=Int(100)
    log_width=Int(300)
    log_str=Unicode()

    @cached_property
    def initial_position(self):
        return (0, self.log_height)

    @cached_property
    def initial_size(self):
        return (self.log_width, self.log_height)

    def write(self, in_str):
        self.log_str+=in_str

    def redirect_stdout(self, visible):
        if visible:
            sys.stdout=self
            sys.stderr=self
        else:
            sys.stdout=sys.__stdout__ #old_stdout
            sys.stderr=sys.__stderr__

    @cached_property
    def interact_window(self):
        return InteractiveWindow(interact=self)

    def __init__(self, **kwargs):
        starter="."+kwargs.pop("starter", "")
        stopper="."+kwargs.pop("stopper", "")
        super(Interact, self).__init__(**kwargs)
        self.file_reader=File_Parser(starter=starter, stopper=stopper)

    def make_input_code(self):
        """process the topmost called code to allow access in the GUI and allow saving of a copy of the code"""
        if not self.file_read:
            print "reading code"
            Interact.file_read=True
            fb=f_top()
            self.locals_dict=fb.f_locals
            with open(fb.f_code.co_filename, "r") as f:
                file_text=f.read()
            self.input_code="\n".join([line for line in file_text.split("\n") if self.file_reader(line)])

    def _observe_input_code(self, change):
        if change["type"]=="update":
            nn=change["value"].count("\n")-change.get('oldvalue', '').count('\n')
            if nn!=0 and self.exec_on_enter:
                self.exec_code()


    def exec_code(self):
        """simulates the python code producing the output texlist"""
        self.log_str=""
        exec(self.input_code, {}, self.locals_dict)
        self.locals_dict.update(locals())

