# -*- coding: utf-8 -*-
"""
Created on Sun Apr 27 11:22:03 2014

@author: thomasaref
"""
#import h5py
from atom.api import Atom, Bool, List, Dict, Unicode, Property, Enum, observe, Int
from h5py import Group, File, special_dtype
from time import strftime, localtime
from os import makedirs
import os
import shutil
import inspect
from Atom_Filer import Filer, QualityFiler

#class Filer(Atom):
#    base_dir=Unicode("/Users/thomasaref/Dropbox/Current stuff/TA_enaml")
#    main_dir=Unicode("")
#    main_file=Unicode("meas.hdf5")
#    divider=Unicode("/")
#
#    file_path=Unicode()
#    dir_path=Unicode()
#
#    #def _get_file_path(self):
#    #    return self.dir_path+self.divider+self.main_file
#
#    #def _get_dir_path(self):
#    #    return self.base_dir+self.divider+self.main_dir
#
#    def _default_main_dir(self):
#        return strftime("S%Y-%m-%d_%H%M%S", localtime())
#
#    def _default_file_path(self):
#        return self.dir_path+self.divider+self.main_file
#
#    @observe( "dir_path", "main_file", 'divider')
#    def file_path_changed(self, change):
#        self.file_path=self.dir_path+self.divider+self.main_file
#        
#    def _default_dir_path(self):
#        return self.base_dir+self.divider+self.main_dir
#        
#    @observe( "base_dir", "main_dir", 'divider')
#    def dir_path_changed(self, change):
#        #print self.dir_path
#        self.dir_path=self.base_dir+self.divider+self.main_dir
#        #print self.dir_path
#        
##        if change['type']!='create':
##            print change
##            if os.path.exists(self.file_path):
##                shutil.move(self.save_dir_path, self.file_path)
#
#class QualityFiler(Filer):
#    quality=Enum("discard", "less interesting", "interesting")
#
#    @observe( "base_dir", "main_dir", 'divider', 'quality')
#    def dir_path_changed(self, change):
#        self.dir_path=self.base_dir+self.divider+self.quality+self.divider+self.main_dir
#
#    def _default_dir_path(self):
#        return self.base_dir+self.divider+self.quality+self.divider+self.main_dir
#        
#if __name__=="__main__":
#    filer=QualityFiler()
##    print filer.file_path
##    print filer.dir_path
##    filer.makedir()
##    filer.save_code(filer)

from numpy import loadtxt
class Read_HDF5(Filer):
    data=Dict()

    def open_and_read(self):
        with File(self.file_path, 'r') as f:
            self.data=self.reread(f)#print key, item.keys(), isinstance(item, Group)
            print "Read data from file: {0}".format(self.file_path)
        return self.data

    def reread(self, g, md=dict()):
        """recursively reads all data into a dictionary"""
        for key, item in g.iteritems():
            md[key]=dict()

            if isinstance(item, Group):
                md[key]=self.reread(item, md[key])
            else:
                md[key]['data']=item[:]
            if item.attrs.keys()!=[]:
                md[key]['attrs']=dict()
                for akey, aitem in item.attrs.iteritems():
                    md[key]['attrs'][akey]=aitem                
        return md
        

    def read_txt(self):
        self.data={"data":loadtxt(self.file_path)}
        return self.data

#f = open('workfile', 'w')
# 'r' when the file will only be read, 
#'w' for only writing (an existing file with the same name will be erased),
# 'a' opens the file for appending; any data written to the file is automatically added to the end. 
#'r+' opens the file for both reading and writing. The mode argument is optional; 'r' will be assumed if it’s omitted.
    
if __name__=="__main__":
    reader=Read_HDF5(main_dir= 'two tone, flux vs control freq, egate n111dbm, IDT n127dbm  2013-10-12_104752', main_file='meas.h5') #'discard/Saved 2015-02-11_130527',)
    a=reader.open_and_read()
    print a['GeneralStepper (110329744)']['attrs'].keys()
    #a=reader.data
#def printname(name):
#    print name
#f.visit(printname)
#f.visititems()
#for line in f:
#        print line,

# f.write('This is a test\n')

class Save_HDF5(QualityFiler):
    cmd_num=Int()
    log_list=List() #are these replaced by log_buffer?
    log_str=Unicode()#are these replaced by log_buffer?
    print_log=Bool(True)
    
    cmd_buffer=List(default=[]) #remove?
    log_buffer=Dict(default={"Full Log":""})
    point_buffer=Dict(default={"Measurement":{}, "Set Up":{}})
    string_buffer=Dict(default={"Measurement":{}, "Set Up":{}})
    buffer_save=Bool(False)
    comment=Unicode()

    @observe( "dir_path")
    def filedir_path_changed(self, change):
        if change['type']!='create':
            old_dir_path=change['oldvalue']
            if not os.path.exists(self.file_path):
                if os.path.exists(old_dir_path):
                    shutil.move(old_dir_path, self.dir_path)
                    self.update_log("Moved files to: {0}".format(self.dir_path))

    def update_log(self, logstr):
        if logstr[0:4]=="RAN:":
            self.cmd_num+=1
        newstr="[{cmd_num}] {logstr}".format(cmd_num=self.cmd_num, logstr=logstr)
        if self.print_log:
            print newstr
        self.log_list.insert(0, newstr)
        self.log_str="\n".join(self.log_list)
        self.write_to_log(newstr)
            
    def makedir(self):
        if not os.path.exists(self.dir_path):
            makedirs(self.dir_path)
        if not os.path.exists(self.file_path):
            ##Valid modes
            ##r	Readonly, file must exist
            ##r+	Read/write, file must exist
            ##w	Create file, truncate if exists
            ##w-	Create file, fail if exists
            ##a	Read/write if exists, create otherwise (default)

            with File(self.file_path, 'w') as f:
                logging=f.create_group("Logging")
                dt = special_dtype(vlen=unicode)
                full_log = logging.create_dataset("Full Log", (0,), dtype=dt, maxshape=(None,))#chunks=True)
                full_log.attrs["index"]=0
                f.create_group("Measurement")
                f.create_group("Set Up")
            self.update_log("Created file at: {0}".format(self.file_path))                
            
    def save_code(self, obj):
        module_path, ext = os.path.splitext(inspect.getfile(obj))
        code_file_path = module_path + '.py'   # Should get the py file, not the pyc, if compiled.
        code_file_copy_path = self.dir_path+self.divider+os.path.split(module_path)[1]+".py"
        if not os.path.exists(code_file_copy_path):
            shutil.copyfile(code_file_path, code_file_copy_path)
            self.update_log("Saved code to: {0}".format(code_file_copy_path))
        
    def full_save(self, obj):
        self.makedir()
        self.flush_buffers()
        self.save_code(obj)
        
#    def open_file(self):
#        self.f=File(self.file_path, 'w')
#
#    def close_file(self):
#        self.flush_buffers()
#        self.f.flush()
#        self.f.close()        

        
    def write_to_log(self, new_string, log="Full Log"):
        if self.buffer_save:
            self.log_buffer[log]=self.log_buffer[log]+new_string+"\n"
        else:
            with File(self.file_path) as f:
                dset=f["Logging"][log]
                n=dset.attrs["index"]
                for item in new_string.split("\n"):
                    #if item !="":
                        if n>=len(dset):
                            a=len(dset)+1
                            dset.resize(a,axis=0)
                        dset[n]=item
                        n=n+1
                dset.attrs["index"]=n

    def flush_buffers(self):
        if self.buffer_save:
            self.buffer_save=False
            for key, item in self.log_buffer.items():
                self.write_to_log(item, log=key)
            for group_name, item in self.point_buffer.iteritems():
                for name, subitem in item.iteritems():
                    for key, arr in subitem.iteritems():
                        self.dataset_save(arr, name=name, group_name=group_name)
            for group_name, item in self.string_buffer.iteritems():
                for name, subitem in item.iteritems():
                    for key, newstr in subitem.iteritems():
                        self.string_save(newstr, name=name, group_name=group_name)                    
            self.log_buffer={"Full Log":""}
            self.point_buffer={"Measurement":{}, "Set Up":{}}
            self.buffer_save=True

    def dataset_save(self, arr, name="Measurement", group_name="Measurement"):
        if self.buffer_save:
            if name not in self.point_buffer[group_name].keys():
                self.point_buffer[group_name][name]=dict()
            namestr="{0}".format(len(self.point_buffer[group_name][name]))
            self.point_buffer[group_name][name][namestr]=arr
        else:
            with File(self.file_path, 'a') as f:
                measurement=f[group_name]
                if name not in measurement.keys():
                    measurement.create_group(name)
                namestr="{0}".format(len(measurement[name]))
                measurement[name].create_dataset(namestr, data=arr)

    def string_save(self, new_string, name="Measurement", group_name="Measurement", append=True):
        if self.buffer_save:
            self.string_buffer[group_name]
            if name not in self.string_buffer[group_name].keys():
                self.string_buffer[group_name][name]=dict()
                append=False
            if append==False:
                namestr="{0}".format(len(self.string_buffer[group_name][name]))
                self.string_buffer[group_name][name][namestr]=""
            namestr="{0}".format(len(self.string_buffer[group_name][name])-1)
            self.string_buffer[group_name][name][namestr]+=new_string+"\n"
        else:
            with File(self.file_path, 'a') as f:
                measurement=f[group_name]
                if name not in measurement.keys():
                    measurement.create_group(name)
                    append=False
                if append==False:
                    namestr="{0}".format(len(measurement[name]))
                    dt = special_dtype(vlen=unicode)
                    measurement[name].create_dataset(namestr, (0,), dtype=dt, maxshape=(None,))#chunks=True)
                    measurement[name][namestr].attrs["index"]=0
                namestr="{0}".format(len(measurement[name])-1)
                dset=measurement[name][namestr]
                n=dset.attrs["index"]
                for item in new_string.split("\n"):
                        if n>=len(dset):
                            a=len(dset)+1
                            dset.resize(a,axis=0)
                        dset[n]=item
                        n=n+1
                dset.attrs["index"]=n

    def point_save(self, value, name="Measurement", group_name="Measurement", append=True):
        if self.buffer_save:
            if name not in self.point_buffer[group_name].keys():
                self.point_buffer[group_name][name]=dict()
                append=False
            if append==False:
                namestr="{0}".format(len(self.point_buffer[group_name][name]))
                self.point_buffer[group_name][name][namestr]=[]
            namestr="{0}".format(len(self.point_buffer[group_name][name])-1)
            self.point_buffer[group_name][name][namestr].append(value)
        else:
            with File(self.file_path, 'a') as f:
                #print f.keys()
                measurement=f[group_name]
                if name not in measurement.keys():
                    measurement.create_group(name)
                    append=False
                if append==False:
                    namestr="{0}".format(len(measurement[name]))
                    measurement[name].create_dataset(namestr, (0,), dtype=float, maxshape=(None,))#chunks=True)
                    measurement[name][namestr].attrs["index"]=0
                namestr="{0}".format(len(measurement[name])-1)
                dset=measurement[name][namestr]
                n=dset.attrs["index"]
                if n>=len(dset):
                    a=len(dset)+1
                    dset.resize(a,axis=0)
                dset[n]=float(value)
                n=n+1
                dset.attrs["index"]=n



        #"""Main capture thread controlling acquisition of data"""
       # with h5py.File('mytestfile.hdf5', 'w') as f:
            #Valid modes
            #r	Readonly, file must exist
            #r+	Read/write, file must exist
            #w	Create file, truncate if exists
            #w-	Create file, fail if exists
            #a	Read/write if exists, create otherwise (default)
        #    logging=f.create_group("Logging")
        #    dt = h5py.special_dtype(vlen=unicode)
        #    full_log = logging.create_dataset("Full Log", (1000,), dtype=dt, maxshape=(None,))#chunks=True)
        #    full_log.attrs["length"]=0
            #short_log = f.create_dataset("Short Log", (1000,), dtype=dt, maxshape=(None,))#chunks=True)

            #meas=f.create_group("Measurements")
            #arr = arange(100)
            #data=meas.create_dataset("blah", data=arr)
            #data.attrs["my"]=string_("wassup")

if __name__=="__main__2":
    hdf5=Save_HDF5()
    hdf5.write_to_log("yo")
    hdf5.dataset_save([1,2,3], name="arr")
    hdf5.point_save(1,name="point")
    hdf5.string_save("blah")