# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 19:14:03 2016

@author: thomasaref
"""

#from sys import exc_info
#from os.path import basename
from atom.api import Atom, Unicode, Bool, List, Typed, Dict, cached_property#, Int
from taref.core.log import f_top
from enaml import imports
with imports():
    from taref.core.interactive_e import InteractiveWindow, CodeWindow
    from taref.core.log_e import LogWindow

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

    log_pane_visible=Bool(False)
    code_pane_visible=Bool(False)

    @cached_property
    def initial_position(self):
        return (0, 100)

    @cached_property
    def initial_size(self):
        return (500, 600)

    @cached_property
    def code_str(self):
        return "\n".join(self.file_reader.preamble)+"\n"+self.input_code+"\n"+"\n".join(self.file_reader.postamble)

    @cached_property
    def interactive_window(self):
        return InteractiveWindow(interact=self)

    @cached_property
    def code_window(self):
        return CodeWindow(interact=self)

    @cached_property
    def log_window(self):
        return LogWindow()

    def __init__(self, **kwargs):
        starter="."+kwargs.pop("starter", "")
        stopper="."+kwargs.pop("stopper", "")
        super(Interact, self).__init__(**kwargs)
        self.file_reader=File_Parser(starter=starter, stopper=stopper)

    def make_input_code(self):
        """process the topmost called code to allow access in the GUI and allow saving of a copy of the code"""
        if not self.file_read:
            Interact.file_read=True
            fb=f_top()
            self.locals_dict=fb.f_locals
            with open(fb.f_code.co_filename, "r") as f:
                file_text=f.read()
            self.input_code="\n".join([line for line in file_text.split("\n") if self.file_reader(line)])
            self.get_member("code_str").reset(self)

    def _observe_input_code(self, change):
        if change["type"]=="update":
            nn=change["value"].count("\n")-change.get('oldvalue', '').count('\n')
            if nn!=0 and self.exec_on_enter:
                self.exec_code()

    def exec_code(self):
        """simulates the python code producing the output texlist"""
        exec(self.input_code, {}, self.locals_dict)
        self.locals_dict.update(locals())
        self.get_member("code_str").reset(self)

