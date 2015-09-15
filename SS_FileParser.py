# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:48:06 2015

@author: thomasaref
"""

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp.hdf5"

from HDF5_functions import read_hdf5
#
#g=read_hdf5(file_path)
#print g
#print
#print g["Traces"].keys()
#
#print g["Traces"].attrs
from atom.api import Atom, Unicode, List, Dict, Typed, Bool, Float, Coerced
from numpy import shape, array, ndarray

from h5py import File

class DataParser(Atom):
    #f=Typed(File)

    user=Unicode()
    project=Unicode()
    log_name=Unicode()  
    comment=Unicode()
    
    step_parallel=Bool(True)
    log_parallel=Bool(True)

    wait_between=Float()
    version=Unicode()
    creation_time=Float()
    time_per_point=Float()
    
    channels=Dict()
    data=Dict()
    instrument_config=Dict()
    instruments=Dict()
    log_list=List()
    
    time_stamp=Coerced(ndarray, coercer=array)

    def read_ssfile(self, f):
        self.project=f["Tags"].attrs["Project"][0]
        self.user=f["Tags"].attrs["User"][0]
        self.log_name=f.attrs["log_name"]
        self.comment=f.attrs["comment"]
        
        self.step_parallel=bool(f.attrs["step_parallel"])
        self.log_parallel=bool(f.attrs["log_parallel"])
        self.wait_between=f.attrs["wait_between"]
        self.version=f.attrs["version"]
        self.creation_time=f.attrs["creation_time"]
        self.time_per_point=f.attrs["time_per_point"]
        
        key="Traces"
        for akey, aitem in f[key].attrs.iteritems():
            print akey, aitem
        print f[key].keys()
        #print shape(f[key]["Time stamp"])
        #print f["Traces"]["Agilent VNA - S21"+"_N"][:]
        #print f["Traces"]["Agilent VNA - S21"+"_t0dt"][:]

    def print_self(self):
        for mem in self.members():
            print "{name}: {attr}".format(name=mem, attr=getattr(self, mem))                       
    
    def trace_extract(self, f, trace_name="Agilent VNA - S21"):
        print shape(f["Traces"][trace_name])  
        print f["Traces"][trace_name+"_N"][:]
        print f["Traces"][trace_name+"_t0dt"][:]
        print shape(f["Traces"]["Time stamp"])
        f0=f["Traces"][trace_name+"_t0dt"][0][0]
        fstep=f["Traces"][trace_name+"_t0dt"][0][1]
        if self.time_stamp==[]:
            self.time_stamp=f["Traces"]["Time stamp"][:]
          
dp=DataParser()

with File(file_path, "r") as f:
    dp.read_ssfile(f) 
    dp.trace_extract(f)
