# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 14:51:44 2016

@author: thomasaref
"""

from atom.api import Atom, Float, cached_property
from collections import OrderedDict
#from enaml import imports
#from enaml.core.operators import op_subscribe
#def testy(*args, **kwargs):
#    print args[0], args[1], kwargs
#    print dir(args[0])
#    return op_subscribe(*args, **kwargs)    
#with imports(operators={"<<" : testy}, union=True):
#    from taref.test.test_atom_e import Main

from PyQt4 import QtGui
import sys

class Example(QtGui.QWidget):
    
    def __init__(self, obj):
        super(Example, self).__init__()
        
        self.initUI()
        self.obj=obj

    def onClicked(self):
        print "clicked"
        print dir(self.titleEdit)
        #self.obj.c=int(self.titleEdit.text())
        self.titleEdit.setText(str(self.obj.blah))
    def txchng(self):
        print "text changed"
        self.obj.c=int(self.titleEdit.text())
        
        
    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QtGui.QPushButton('Button', self)
        print dir(btn)
        btn.setText("yay")
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)       
        btn.clicked.connect(self.onClicked)
        #self.connect(btn, QtGui.QtCore.SIGNAL('clicked()'), self.onClicked)
        self.titleEdit = QtGui.QLineEdit()
        self.titleEdit.textChanged.connect(self.txchng)
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.titleEdit, 1, 0)
        
        grid.addWidget(btn, 1, 1)
        self.setLayout(grid) 
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Tooltips')    
        self.show()
        
def main():
    
    app = QtGui.QApplication(sys.argv)

    w = Example(obj=b)
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    sys.exit(app.exec_())


ind=100000
class Test(Atom):
    a=Float().tag(blue="good")

    @cached_property
    def b(self):
        return range(ind)
        
#print dir(Atom)

#print dir(object)
class Value(object):
    typer=None
    coercer=None
    
    def tag(self, **kwargs):
        self.metadata.update(kwargs)
        return self
        
    def __init__(self):
        self.metadata={}

class Property(Value):
    def __init__(self, fget=None, fset=None, fdel=None, cached=True):
        super(Property, self).__init__()
        self.fget=fget
        self.fset=fset
        self.fdel=fdel
        self.cached=cached
        self.do_reset=True
        
    def reset(self):
        self.do_reset=True

    def __get__(self, obj, typ):
        if self.do_reset:
            self.value=self.fget(obj)
            self.do_reset=not self.cached
        return self.value

class Int(Value):
    coercer=int
    def __init__(self, default=0):
        self.default=default
        self.metadata={}

    def __get__(self, obj, typ=None):
        return obj.__slots__.get(self, self.default)

    def __set__(self, obj, value):
        obj.notify(self, value)
        obj.__slots__[self]=self.coercer(value)


class myAtom(object):
    def __init__(self, **kwargs):
        self.__slots__={}
        for kw in kwargs:
            self.__slots__[self.get_member(kw)]=kwargs[kw]

    @classmethod
    def get_member(cls, name):
        return cls.__dict__[name]

    @classmethod
    def members(cls):
        return dict([(name, member) for name, member in cls.__dict__.items() if isinstance(member, Value)])

    def set_tag(self, name, **kwargs):
        self.get_member(name).metadata.update(kwargs)

    def get_tag(self, name, tag, none_value=None):
        return self.get_member(name).metadata.get(tag, none_value)

class test(myAtom):
    c=Int().tag(five=5, typer=int)

    #def __init__(self, **kwargs):
    #    super(test, self).__init__(**kwargs)

    def _observe_c(self, change):
        print change
        self.get_member("blah").reset()
        
    def notify(self, *args):
        print "parent", args
        #self.get_member("blah").reset()

    @Property
    def blah(self):
        return 4 #range(ind)

    @Property
    def d(self):
        return range(ind)
        
    @property
    def red(self):
        return range(ind)
        
    @property
    def view_window(self):
        return Main(test=self)

#    def __init__(self, a=2):
#        #self.a=a
#        self.get_member("c").parent=self#

        #super(test, self).__init__(a=a)



if __name__ == '__main__':
    from time import time
    a=Test()
    b=test(c=10)
    c=test()
    
    print b.__dict__
    print b.c, c.c
    c.c=20
    print b.c, c.c
    print dir(b)

    #tstart=time()
    #for n in range(1000):
    #    b.red
    #print tstart-time()

    

    
    
    tstart=time()
    for n in range(100000):
        a.b
    print tstart-time()

    tstart=time()
    for n in range(100000):
        b.d
    print tstart-time()

    #main()
if 0:
    print b.c
    print b.blah
    b.c=4
    print b.c
    print b.get_member("c")
    print b.get_member("c").metadata
    print b.members()
    b.set_tag("c", g=2)
    print b.get_tag("c", "g")
    print b.get_tag("c", "g2")
    print b.get_tag("c", "five")
    
    from taref.core.shower import shower
    from taref.core.api import get_main_params, get_all_tags
    print get_main_params(b)
    print get_all_tags(b, key="private", key_value=False, none_value=False)
    print b.members()
#shower(b)

#print dir(a)
#print dir(b)
#print a.__atom_members__
#print b.__dict__
#b.set_tag("a", blue="good")
#print b.get_tag("a", "blue")
#print b.get_tag("a", "red")
#print b.members()
#print b.get_member("a")
#print b.__dict__
#print b.members()
