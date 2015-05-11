# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:13:08 2015

@author: thomasaref
"""

from h5py import Group, File, special_dtype
from numpy import ndarray

def read_hdf5(file_path):
    with File(file_path, 'r') as f:
        data=reread(f)#print key, item.keys(), isinstance(item, Group)
    return data

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

def create_hdf5(file_path, group_names):
        ##Valid modes
        ##r	Readonly, file must exist
        ##r+	Read/write, file must exist
        ##w	Create file, truncate if exists
        ##w-	Create file, fail if exists
        ##a	Read/write if exists, create otherwise (default)

        with File(file_path, 'w') as f:
            #logging=f.create_group("Logging")
            #dt = special_dtype(vlen=unicode)
            #full_log = logging.create_dataset("Full Log", (0,), dtype=dt, maxshape=(None,))#chunks=True)
            #full_log.attrs["index"]=0
            for gn in group_names:
                f.create_group(gn)

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
    create_hdf5(file_path, ["Measurement", "SETUP"])
    hdf5_data_save(file_path, [4.0,5,6], name="yo")
    hdf5_data_save(file_path, [1.03,2,3.0], name="yo")
    hdf5_data_save(file_path, 7, name="yo")
    hdf5_data_save(file_path, "blah", name="bo", group_name="Measurement", append=True)
    hdf5_data_save(file_path, ["bobbby", "thomasaass"], name="obo", group_name="Measurement", append=True)

    print read_hdf5(file_path)