# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 20:42:21 2015

@author: thomasaref
"""

from enaml.qt.qt_application import QtApplication
from atom.api import Atom, Unicode, Bool, List, Typed
from enaml import imports

#from a_Backbone import get_attr

#from LOG_functions import log_info, log_warning, make_log_file, log_debug#, SAVE_GROUP_NAME, SETUP_GROUP_NAME, log_debug
#from atom.api import Atom, Bool, Typed, ContainerList, Callable, Dict, Float, Int, FloatRange, Range, Unicode, Str, List, Enum, Event, Instance
#from Atom_Read_File import Read_File
#from Atom_Save_File import Save_File, Save_HDF5
#from Plotter import Plotter

#def show_alone(agent):
#    app = QtApplication()
#    view=agent.view
#    view.show()
#    app.start()

class Chief(Atom):
    save_file=Unicode()
    name=Unicode()
    show_all=Bool(False)
    plots=List(default=["a", "b"])

chief=Chief()
 
#def get_attr(obj, name, default_value):
#    if hasattr(obj, name):
#        return getattr(obj, name)
#    return default_value
#    
#def get_name(agent, default_name="agent_", n=0):
#    if hasattr(a, "name"):
#        return a.name
#    return default_name.format(n)

def show(*agents):
    app = QtApplication()
    with imports():
        from e_Show import defaultView, showView
    loc_chief=None
    for n, a in enumerate(agents):
        if hasattr(a, "view"):
            view=a.view
        else:
            view=defaultView(agent=a)
        if hasattr(a, "name"):
            view.name=a.name
        else:
            view.name="agent_{0}".format(n)
        if hasattr(a, "chief"):
            loc_chief=a.chief
        view.title=view.name
        view.show()
        if loc_chief is not None:
            if not chief.show_all and n!=0:
                view.visible=False
    view=showView(title="ShowControl", name="show_control")#, chief=chief)
    if loc_chief is not None:
        view.chief=loc_chief
    view.show()
    app.start()

if __name__=="__main__":
    from atom.api import Atom, Unicode

    class test(Atom):
        """example test class with view defined"""
        a=Unicode("blah")
        name=Unicode("testy")

        @property
        def chief(self):
            return chief
            
        @property
        def view(self):
            with imports():
                from e_Show import Main
            return Main(test=self)

    class test2(Atom):
        """example test class without view defined"""
        a=Unicode("bob")

    a=test()
    #show(a)
    b=test2()
    c=test2()
    show(a,b, c)

#
#  0
#INSERT
#  5
#F8B0
#330
#1F
#100
#AcDbEntity
#  8
#Photomarks
#100
#AcDbBlockReference
#  2
#PL cross
# 10
#-7500.0
# 20
#4000.0
# 30
#0.0
# 41
#2.5
# 42
#2.5
# 43
#2.5
# 50
#180.0
#
#
#Group codes	Description
#100
#
#Subclass marker (AcDbBlockReference)
#
#66
#
#Variable attributes-follow flag (optional; default = 0); if the value of attributes-follow flag is 1, a series of attribute entities is expected to follow the insert, terminated by a seqend entity.
#
#2
#
#Block name
#
#10
#
#Insertion point (in OCS). DXF: X value; APP: 3D point
#
#20, 30
#
#DXF: Y and Z values of insertion point (in OCS)
#
#41
#
#X scale factor (optional; default = 1)
#
#
#42
#
#Y scale factor (optional; default = 1)
#
#
#43
#
#Z scale factor (optional; default = 1)
#
#
#50
#
#Rotation angle (optional; default = 0)
#
#70
#
#Column count (optional; default = 1)
#
#71
#
#Row count (optional; default = 1)
#
#44
#
#Column spacing (optional; default = 0)
#
#45
#
#Row spacing (optional; default = 0)
#
#210
#
#Extrusion direction. (optional; default = 0, 0, 1). 
#DXF: X value; APP: 3D vector
#
#220, 230
#
#DXF: Y and Z values of extrusion direction
#
#
#
#
#  0
#ENDSEC
#  0
#SECTION
#  2
#BLOCKS
#  0
#BLOCK
#  5
#20
#330
#1F
#100
#AcDbEntity
#  8
#0
#100
#AcDbBlockBegin
#  2
#*Model_Space
# 70
#     0
# 10
#0.0
# 20
#0.0
# 30
#0.0
#  3
#*Model_Space
#  1
#
#  0
#ENDBLK
#  5
#21
#330
#1F
#100
#AcDbEntity
#  8
#0
#100
#AcDbBlockEnd
#
#  0
#BLOCK
#  5
#F85F
#330
#F85E
#100
#AcDbEntity
#  8
#0
#100
#AcDbBlockBegin
#  2
#PL cross
# 70
#     0
# 10
#0.0
# 20
#0.0
# 30
#0.0
#  3
#PL cross
#  1
#
#  0
#LWPOLYLINE
#  5
#F860
#330
#F85E
#100
#AcDbEntity
#  8
#0
#100
#AcDbPolyline
# 90
#        5
# 70
#     1
# 43
#0.0
# 10
#-5.0
# 20
#4.999999999999886
# 10
#-5.0
# 20
#50.0
# 10
#5.0
# 20
#50.0
# 10
#5.0
# 20
#5.000000000000226
# 10
#0.0
# 20
#0.0000000000001137
#
#  0
#LWPOLYLINE
#  5
#F863
#330
#F85E
#100
#AcDbEntity
#  8
#0
#100
#AcDbPolyline
# 90
#        5
# 70
#     1
# 43
#0.0
# 10
#4.999999999999545
# 20
#5.0
# 10
#49.99999999999954
# 20
#5.0
# 10
#49.99999999999954
# 20
#-5.0
# 10
#5.0
# 20
#-5.0
# 10
#0.0
# 20
#0.0
#  0
#ENDBLK
#  5
#F864
#330
#F85E
#100
#AcDbEntity
#  8
#0
#100
#AcDbBlockEnd
#  0
#ENDSEC
#  0
#  
#
#
#
#Group codes	Description
#0
#
#Entity type (BLOCK)
#
#5
#
#Handle
#
#102
#
#Start of application defined group "{application_name". For example, "{ACAD_REACTORS" indicates the start of the AutoCAD persistent reactors group
#
#application-defined codes
#
#
#Codes and values within the 102 groups are application-defined.
#
#102
#
#End of group, "}"
#
#100
#
#Subclass marker (AcDbEntity)
#
#8
#
#Layer name
#
#100
#
#Subclass marker (AcDbBlockBegin)
#
#2
#
#Block name
#
#70
#
#Block-type flags (bit coded values, may be combined): 
#1 = This is an anonymous block generated by hatching, associative dimensioning, other internal operations, or an application
#2 = This block has attribute definitions
#4 = This block is an external reference (xref)
#8 = This block is an xref overlay 
#16 = This block is externally dependent
#32 = This is a resolved external reference, or dependent of an external reference (ignored on input)
#64 = This definition is a referenced external reference (ignored on input)
#
#10
#
#Base point. DXF: X value; APP: 3D point
#
#20, 30
#
#DXF: Y and Z values of base point
#
#3
#
#Block name
#
#1
#
#Xref path name (optional; present only if the block is an xref)  