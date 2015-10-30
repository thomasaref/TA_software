# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 18:17:19 2014

@author: thomasaref
"""

"""This demo shows how to use Traits TreeEditors with PyTables to walk the
heirarchy of an HDF5 file.  This only picks out arrays and groups, but could
easily be extended to other structures, like tables.

In the demo, the path to the selected item is printed whenever the selection
changes.  In order to run, a path to an existing HDF5 database must be given
at the bottom of this file.
"""

from traits.api import HasTraits, Str, List, Instance, Array, File, Dict
from traitsui.api import TreeEditor, TreeNode, View, Item, Group#, FileEditor#, TabularEditor
from traitsui.ui_editors.array_view_editor import ArrayViewEditor
#import numpy as np

#from plot2D import myImagePlot
from numpy import squeeze, transpose, ndarray, shape
import h5py

# View for objects that aren't edited
no_view = View()


# HDF5 Nodes in the tree
class Hdf5ArrayNode(HasTraits):
    name   = Str( '<unknown>' )
    path = Str( '<unknown>' )
    parent_path = Str( '<unknown>' )
    contents=Array()
    subarray = List

class Hdf5GroupNode(HasTraits):
    name     = Str( '<unknown>' )
    path = Str( '<unknown>' )
    parent_path = Str( '<unknown>' )
    # Can't have recursive traits?  Really?
    #groups = List( Hdf5GroupNode )
    groups = List
    arrays = List( Hdf5ArrayNode )
    groups_and_arrays = List

class Hdf5FileNode(HasTraits):
    name   = Str( '<unknown>' )
    path   = Str( '/' )
    groups = List( Hdf5GroupNode )
    arrays = List( Hdf5ArrayNode )
    groups_and_arrays = List
    mydict=Dict

# Recurssively build tree, there is probably a better way of doing this.
def _get_sub_arrays(group, md=dict()):
    """Return a list of all arrays immediately below a group in an HDF5 file."""
    l = []
    for name,item in group.items():
        if _check_dataset(item):
            md[name]=item[:]
            a = Hdf5ArrayNode(
                    name = name,
                    path = item.name,
                    parent_path = item.parent.name,
                    contents=item[:]
                    )
            subarray=_get_subarray(a)
            if subarray!=[]:
                a.subarray=subarray
            l.append(a)
    return l, md

def _get_subarray(arr):
    l=[]
    for n, item in enumerate(arr.contents):
        if type(item)==ndarray:
            a = Hdf5ArrayNode(
                    name = str(n),
                    path = arr.path+str(n),
                    parent_path = arr.path,
                    contents=squeeze(item[:])
                    )
            subarray=_get_subarray(a)
            if subarray!=[]:
                a.subarray=subarray
            l.append(a)
    return l

def visit_all(mt, md=dict()):
    allkeys=mt.keys()
    for m in allkeys:
        md[m]=dict()
        try:
            mt[m].keys()
            visit_all(mt[m], md[m])
        except AttributeError:
            md[m]=mt[m][:]
    return md

def _get_sub_groups(group, md=dict()):
    """Return a list of all groups and arrays immediately below a group in an HDF5 file."""
    l = []
    for name, item in group.items():
        print name, item.name, item.parent.name
        if _check_group(item):
            md[name]=dict()
            g = Hdf5GroupNode(
                  name = name,
                  path=item.name,
                  parent_path = item.parent.name)

            subarrays, rd=_get_sub_arrays(item, md[name])

            if subarrays != []:
                g.arrays = subarrays
                md[name]= rd

            subgroups, rd = _get_sub_groups(item, md[name])
            if subgroups != []:
                g.groups = subgroups
                md[name]=rd

            g.groups_and_arrays = []
            g.groups_and_arrays.extend(subgroups)
            g.groups_and_arrays.extend(subarrays)

            l.append(g)

    return l, md

def _check_file(f):
    return type(f.id)==h5py.h5f.FileID
def _check_group(f):
    return type(f.id)==h5py.h5g.GroupID
def _check_dataset(f):
    return type(f.id)==h5py.h5d.DatasetID

def _hdf5_tree(filename):
    """Return a list of all groups and arrays below the root group of an HDF5 file."""

    h5file = h5py.File(filename, 'r')
    #print type(h5file.id) #[h5file.name].keys()

    groups, mydict = _get_sub_groups(h5file)
    arrays, otherdict = _get_sub_arrays(h5file)
    file_tree = Hdf5FileNode(
            name = filename,
            groups = groups,
            arrays = arrays,
            mydict=mydict
            )

    file_tree.groups_and_arrays = []
    file_tree.groups_and_arrays.extend(file_tree.groups)
    file_tree.groups_and_arrays.extend(file_tree.arrays)

    h5file.close()

    return file_tree

# Get a tree editor
def _hdf5_tree_editor(selected=''):
    """Return a TreeEditor specifically for HDF5 file trees."""
    return TreeEditor(
        nodes = [
            TreeNode(
                node_for  = [ Hdf5FileNode ],
                auto_open = True,
                children  = 'groups_and_arrays',
                label     = 'name',
                view      = no_view,
                ),
            TreeNode(
                node_for  = [ Hdf5GroupNode ],
                auto_open = False,
                children  = 'groups_and_arrays',
                label     = 'name',
                view      = no_view,
                ),
            TreeNode(
                node_for  = [ Hdf5ArrayNode ],
                auto_open = False,
                children  = 'subarray',
                label     = 'name',
                view      = no_view #View('name')#, editor=ArrayViewEditor(titles=['x'], format='%s'))),
                ),
            ],
        editable = False,
        selected = selected,
        )


if __name__ == '__main__':
    from traits.api import Any

    class ATree(HasTraits):
        h5_tree = Instance(Hdf5FileNode)
        node = Any
        data=Array


        traits_view =View(
            Group(
                Item('h5_tree',
                    editor = _hdf5_tree_editor(selected='node'),
                    resizable =True,

                    ),
                Item('data', editor=ArrayViewEditor(titles = [ 'data' ],
                                           format = '%s')),
                orientation = 'horizontal',

                ),
            title = 'HDF5 Tree Example',
            buttons = [ 'Undo', 'OK', 'Cancel' ],
            resizable = True,
            width = .5,
            height = .3
            )

        def _node_changed(self):
            print self.node.path

            #print self.node.contents
            if isinstance(self.node, Hdf5ArrayNode):
                print self.node.contents
                for item in self.node.contents:
                    print type(item)
                    print shape(item)
                    break
                self.data=self.node.contents
    print "Yo"
    class MainWindow(HasTraits):
        hdf_file=File('trash_test.hdf5')#'/Users/thomasaref/Dropbox/Current stuff/TA_meas_software/trash_test.hdf5')
        #sample3_digitizer_f_sweep_r_300mk_100nspulse.hdf5')
        traits_view =View(Group(
                     Item( 'hdf_file'),
                            #id     = 'file2',
                            #editor = FileEditor( entries = 10)),#,
                                          # filter  = [ 'All files (*.*)|*.*',
                                               #'HDF5 files (*.hdf5)|*.hdf5' ] )),
                orientation = 'vertical',

                ),
            title = 'HDF5 Tree Example',
            buttons = [ 'Undo', 'OK', 'Cancel' ],
            resizable = True,
            width = .5,
            height = .3,
		 #id='historytest'
            )
        #def _hdf_file_changed(self):
        #    self.Atree = ATree( h5_tree = _hdf5_tree(self.hdf_file))


    #a_tree = ATree( h5_tree = _hdf5_tree('/Users/thomasaref/Dropbox/Current stuff/TA_meas_software/sample3_digitizer_f_sweep_r_300mk_100nspulse.hdf5'), data=[0])
    mw=MainWindow()
    mw.configure_traits()
    a_tree = ATree( h5_tree = _hdf5_tree(mw.hdf_file), data=[0])
   # for a in a_tree.h5_tree.groups_and_arrays:
   #     if item.name=='Data':
   #         for subitem in item.groups_and_arrays:
   #             print subitem.name
    a_tree.configure_traits()
    f=a_tree.h5_tree.mydict
    #print f['Measurement']
    if "Data" in a_tree.h5_tree.mydict.keys():
        time=f["Traces"]["d - AvgTrace - t"][:]
        #Magvec=f["Traces"]["d - AvgTrace - Magvec"][:]
        Magvec=a_tree.node.contents
        frequency=f["Data"]["Data"][:]
        time=squeeze(time)
        Magvec=squeeze(Magvec)
        #print Magvec
        frequency=squeeze(frequency)

        x = time[:,0]*1.0e6
        y = frequency[0,:]/1.0e9
        z=transpose(Magvec*1000.0)

       # ip=myImagePlot(x,y,z)
       # ip.configure_traits()
