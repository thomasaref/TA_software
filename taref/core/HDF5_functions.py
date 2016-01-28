# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:13:08 2015

@author: thomasaref

collection of functions for working with hdf5 files. string save is not working currently.
"""

from h5py import Group, File, special_dtype
from numpy import ndarray
from collections import OrderedDict

class dataset(object):
    """a class that represents a HDF5 dataset"""
    def __init__(self,  data=[], append=True, attrs=None, datatype=None, maxshape=(None,)):
        if attrs is None:
            attrs={}
        attrs["append"]=append
        self.attrs=attrs
        self.maxshape=maxshape
        if datatype in [str, unicode, bool]:
            self.datatype = special_dtype(vlen=unicode)
            self.data=[str(d) for d in data]
        else:
            if datatype is None:
                self.datatype=type(data[0])
            else:
                self.datatype=datatype
            self.data=data

    def __repr__(self):
        return "dataset( data={data}, datatype={datatype})".format(data=self.data, datatype=self.datatype)

    def __getitem__(self, key):
        return self.data[key]

class group(OrderedDict):
    """a class that represents a hdf5 group"""
    def __init__(self, attrs=None, *args, **kwargs):
        super(group, self).__init__(*args, **kwargs)
        if attrs is None:
            attrs={}
        self.attrs=attrs

    def __repr__(self):
        dict_str=super(group, self).__repr__()
        dict_str+="[attrs={attrs}]".format(attrs=self.attrs)
        return dict_str

def reread(g, md=dict()):
    """recursively reads all data into a dictionary"""
    for key, item in g.iteritems():
        md[key]=dict()

        if isinstance(item, Group):
            md[key]=reread(item, md[key])
        else:
            md[key]['data']=item[:]
        if item.attrs.keys()!=[]:
            md[key]['attrs']=dict()
            for akey, aitem in item.attrs.iteritems():
                md[key]['attrs'][akey]=aitem
    return md

def read_hdf5_dict(file_path):
    with File(file_path, 'r') as f:
        data=reread(f)#print key, item.keys(), isinstance(item, Group)
    return data

def reread_group(g, store_data=True, md=group()):
    """recursively reads all data into groups and datasets. If store_data is False only keeps first 5 data entries
    (i.e. so structure of a large hdf5 file can be seen but data can be extracted selectively directly from file."""
    if isinstance(g, File):
        if g.attrs.keys()!=[]:
            for akey, aitem in g.attrs.iteritems():
                md.attrs[akey]=aitem
    for key, item in g.iteritems():
        if isinstance(item, Group):
            myg=group()
            myg=reread_group(item, store_data=store_data, md=myg)
        else:
            if store_data:
                myg=dataset( data=item[:])
            else:
                myg=dataset( data=item[0:4])
        if item.attrs.keys()!=[]:
            for akey, aitem in item.attrs.iteritems():
                myg.attrs[akey]=aitem
        md[key]=myg
    return md

def read_hdf5(file_path, store_data=False):
    with File(file_path, 'r') as f:
        data=reread_group(f, store_data=store_data)#print key, item.keys(), isinstance(item, Group)
    return data

def write_hdf5_file_path(file_path, data_dict, write_mode="a"):
    with File(file_path, write_mode) as f:
        rewrite_hdf5(f, data_dict)

def rewrite_hdf5(g, data_dict):
    """recursively writes all data in a dictionary. assumes data is grouped using group and dataset defined above"""
    for ddkey, dditem in data_dict.iteritems():
        if ddkey not in g.keys():
            g.create_group(ddkey)
            for attr in dditem.attrs:
                g[ddkey].attrs[attr]=dditem.attrs[attr]
            append=False
        else:
            append=dditem.attrs.get("append", False)
            g[ddkey].attrs["append"]=append
        if isinstance(dditem, dataset): #dataset
            if not append:
                namestr="{0}".format(len(g[ddkey]))
                g[ddkey].create_dataset(namestr, data=dditem.data, dtype=dditem.datatype, maxshape=dditem.maxshape)#chunks=True)
                #g[ddkey][namestr].attrs["index"]=len(dditem.data)-1
            else:
                namestr="{0}".format(len(g[ddkey])-1)
                dset=g[ddkey][namestr]
                #n=dset.attrs["index"]
                #if n>=len(dset)-1:
                n=len(dset)
                a=n+len(dditem.data)
                dset.resize(a,axis=0)
                dset[n:]=dditem.data
                #n+=len(dditem.data)
                #dset.attrs["index"]=n
        elif isinstance(dditem, group):
            rewrite_hdf5(g[ddkey], dditem)
#            else:
#                rewrite(g, item, key)
#    else:
#        if append==False:
#            if type(data[0]) in [str, unicode, bool]:
#                        datatype = special_dtype(vlen=unicode)
#                        data=map(str, data)
#                    else:
#                        datatype=type(data[0])
#                    namestr="{0}".format(len(measurement[name]))
#                    measurement[name].create_dataset(namestr, data=data, dtype=datatype, maxshape=(None,))#chunks=True)
#                    measurement[name][namestr].attrs["index"]=len(data)-1
#                else:
#
    #else:
        #pass #print g, dd
#        datatype=type(dd[0])
#        namestr="{0}".format(len(g))
#        g.create_dataset(namestr, data=dd, dtype=datatype, maxshape=(None,))#chunks=True)
#        g[namestr].attrs["index"]=len(dd)-1


#def create_hdf5(file_path):#, group_names):
        ##Valid modes
        ##r	Readonly, file must exist
        ##r+	Read/write, file must exist
        ##w	Create file, truncate if exists
        ##w-	Create file, fail if exists
        ##a	Read/write if exists, create otherwise (default)

#        with File(file_path, 'w') as f:
#            pass
            #logging=f.create_group("Logging")
            #dt = special_dtype(vlen=unicode)
            #full_log = logging.create_dataset("Full Log", (0,), dtype=dt, maxshape=(None,))#chunks=True)
            #full_log.attrs["index"]=0
            #for gn in group_names:
            #    f.create_group(gn)

#def save_hdf5_log(file_path, new_string, log="Full Log"):
#    """saves a log string to an HDF5 file"""
#    with File(file_path) as f:
#        dset=f["Logging"][log]
#        n=dset.attrs["index"]
#        for item in new_string.split("\n"):
#                if n>=len(dset):
#                    a=len(dset)+1
#                    dset.resize(a,axis=0)
#                dset[n]=item
#                n=n+1
#        dset.attrs["index"]=n
def hdf5_dict_save(file_path, data_dict, append=True, write_mode="a"):
    with File(file_path, write_mode) as f:
        for gn in data_dict.keys():
            if gn not in f.keys():
                f.create_group(gn)
            measurement=f[gn]
            for name, data_item in data_dict[gn]:
                if name not in measurement.keys():
                    measurement.create_group(name)
                    append=False
                data=data_item[name]
                if append==False:
                    if type(data[0]) in [str, unicode, bool]:
                        datatype = special_dtype(vlen=unicode)
                        data=map(str, data)
                    else:
                        datatype=type(data[0])
                    namestr="{0}".format(len(measurement[name]))
                    measurement[name].create_dataset(namestr, data=data, dtype=datatype, maxshape=(None,))#chunks=True)
                    measurement[name][namestr].attrs["index"]=len(data)-1
                else:
                    namestr="{0}".format(len(measurement[name])-1)
                    dset=measurement[name][namestr]
                    n=dset.attrs["index"]
                    if n>=len(dset)-1:
                        a=len(dset)+len(data)
                        dset.resize(a,axis=0)
                    dset[n+1:]=data
                    n=n+len(data)
                    dset.attrs["index"]=n

def hdf5_data_save(file_path, data, name, group_name, append=True):
    if type(data) not in [list, ndarray]:
        data=[data]#    self.data_buffer[group_name][name][namestr]=[data]
    with File(file_path, 'a') as f:
        measurement=f[group_name]
        if name not in measurement.keys():
            measurement.create_group(name)
            append=False
        if append==False:
            if type(data[0]) in [str, unicode, bool]:
                datatype = special_dtype(vlen=unicode)
                data=map(str, data)
            else:
                datatype=type(data[0])
            namestr="{0}".format(len(measurement[name]))
            measurement[name].create_dataset(namestr, data=data, dtype=datatype, maxshape=(None,))#chunks=True)
            measurement[name][namestr].attrs["index"]=len(data)-1
        else:
            namestr="{0}".format(len(measurement[name])-1)
            dset=measurement[name][namestr]
            n=dset.attrs["index"]
            if n>=len(dset)-1:
                a=len(dset)+len(data)
                dset.resize(a,axis=0)
            dset[n+1:]=data
            n=n+len(data)
            dset.attrs["index"]=n

#not used######################
#
#def hdf5_dataset_save(file_path, arr, name, group_name="Measurement"):
#    with File(file_path, 'a') as f:
#        measurement=f[group_name]
#        if name not in measurement.keys():
#            measurement.create_group(name)
#        namestr="{0}".format(len(measurement[name]))
#        measurement[name].create_dataset(namestr, data=arr)
#
#def do_string_save(filepath, new_string, name, group_name="Measurement", append=True):
#    with File(file_path, 'a') as f:
#        measurement=f[group_name]
#        if name not in measurement.keys():
#            measurement.create_group(name)
#            append=False
#        if append==False:
#            namestr="{0}".format(len(measurement[name]))
#            dt = special_dtype(vlen=unicode)
#            measurement[name].create_dataset(namestr, (0,), dtype=dt, maxshape=(None,))#chunks=True)
#            measurement[name][namestr].attrs["index"]=0
#        namestr="{0}".format(len(measurement[name])-1)
#        dset=measurement[name][namestr]
#        n=dset.attrs["index"]
#        for item in new_string.split("\n"):
#                if n>=len(dset):
#                    a=len(dset)+1
#                    dset.resize(a,axis=0)
#                dset[n]=item
#                n=n+1
#        dset.attrs["index"]=n
#
#
#def open_hdf5(file_path):
#    """opens an HDF5 file. not used"""
#    return File(file_path, 'w')
#
#def close_hdf5(f):
#    """flushes and closes an hdf5 file"""
#    f.flush()
#    f.close()

if __name__=="__main__":
    file_path='testhdf5.hdf5'
    #create_hdf5(file_path, ["Measurement", "SETUP"])
    #hdf5_data_save(file_path, [4.0,5,6], name="yo")
    #hdf5_data_save(file_path, [1.03,2,3.0], name="yo")
    #hdf5_data_save(file_path, 7, name="yo")
    #hdf5_data_save(file_path, "blah", name="bo", group_name="Measurement", append=True)
    #hdf5_data_save(file_path, ["bobbby", "thomasaass"], name="obo", group_name="Measurement", append=True)

    a=group()
    a["fudge"]=dataset( data=[7,8,9], attrs={"yo":"mama"})
    a["tacos"]=group( blue=dataset(data=[1.2, 1.5, 1.6], attrs={"yay":"man"}), attrs={"dog":"cat"})
    #print isinstance(a["fudge"], dataset)
    write_hdf5(file_path, a, "w")
    a=group()
    a["fudge"]=dataset(data=[4,5,6], append=False)
    a["tacos"]=group(blue=dataset(data=[1,2,3], append=False))
    write_hdf5(file_path, a)
    #hdf5_dict_save(file_path, data={"Meas": dict(a=[1, 2,3])})
    print read_hdf5(file_path)
    #b=read_hdf5(file_path)
    #print b.name, b.attrs, b#[c.name for c in b.children], b["tacos"]["blue"]["other"].attrs #.children[0].children[0].datatype#, b.children[1].name, b.children[2].name