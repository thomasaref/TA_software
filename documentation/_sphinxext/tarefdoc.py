# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:43:45 2016

@author: thomasaref
"""
#from taref.core.log import log_debug
from atom.api import Property, Callable

def process_docstring(app, what, name, obj, options, lines):
    if what=="attribute":
        line=None
        metadata=getattr(obj, "metadata", None)
        if metadata is not None:
            line=metadata.get("desc", None)
        if isinstance(obj, Property):
            if line is None:
                line=obj.fget.__doc__
        if line is not None:
            lines[:]=[line]

def setup(app):
    app.connect('autodoc-process-docstring', process_docstring)


# what='function', 'method', 'attribute'
#name= u'taref.core.shower.shower',
#obj= <function shower at 0x108a29a28>,
#options={'members': <object object at 0x1002c76e0>},
#lines=[u'A powerful showing function for any Atom object(s) specified in agents.', u'Checks if an object has a view_window and otherwise uses a default window for the object.', u'', u'Checks kwargs for particular keywords:', u'    * ``start_it``: boolean representing whether to go through first time setup prior to starting app', u'    * ``app``: defaults to existing QtApplication instance and will default to a new instance if none exists', u'    chief_cls: if not included defaults to the first agent and defaults to Backbone if no agents are passed.', u'    show_log: shows the log_window of chief_cls if it has one, defaults to not showing', u'    show_ipy: shows the interactive_window of chief_cls if it has one, defaults to not showing', u'    show_code: shows the code_window of chief_cls if it has one, defaults to not showing', u'', u"shower also provides a chief_window (generally for controlling which agents are visible) which defaults to Backbone's chief_window", u'if chief_cls does not have one. attributes of chief_window can be modified with the remaining kwargs', ''])

# 'attribute',
# u'taref.core.log.StreamCatch.screen_height',
# <atom.scalars.Int object at 0x103031b90>,
# {'members': <object object at 0x1002c76e0>, 'undoc-members': True},
#[u'A value of type `int`.', u'', u'By default, ints are strictly typed.  Pass strict=False to the', u'constructor to enable int casting for longs and floats.', u'', u''])
