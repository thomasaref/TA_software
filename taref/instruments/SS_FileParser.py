# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:48:06 2015

@author: thomasaref
"""

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp.hdf5"
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1008/TA46_refll_fluxpowswp_4p2GHz4pGHz.hdf5"

#from SHOW_functions import show
#from enaml import imports
#from enaml.qt.qt_application import QtApplication

#from HDF5_functions import read_hdf5
#
#g=read_hdf5(file_path)
#print g
#print
#print g["Traces"].keys()
#
#print g["Traces"].attrs
from atom.api import Atom, Unicode, List, Dict, Typed, Bool, Float, Coerced
from numpy import shape, array, ndarray, linspace, reshape, dtype
from taref.core.universal import Array
from h5py import File
from taref.core.atom_extension import private_property

def empty_array():
    return []

class DataParser(Atom):
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

    channels=Typed(ndarray)
    data=Dict()
    shaper=List()
    instrument_config=Dict()
    instruments=Typed(ndarray)
    log_list=Typed(ndarray).tag(desc="names of traces")
    step_config=Dict()
    step_list=Typed(ndarray)
    trace_list=List()

    def _observe_user(self, change):
        print change

    time_stamp=Coerced(ndarray, coercer=array, factory=empty_array)

    #specific variables
    f0=Coerced(float)
    fstep=Coerced(float)
    numsteps=Coerced(int)
    frequency=Coerced(ndarray, coercer=array, factory=empty_array)

    magcom=Coerced(ndarray, coercer=array, factory=empty_array)


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

        self.step_list=f["Step list"][:]

        for akey in f["Step config"]:
            self.step_config[akey]=dict(relation_parameters=f["Step config"][akey]["Relation parameters"][:],
                                        step_items=f["Step config"][akey]["Step items"][:])

        self.log_list=f["Log list"][:]
        self.instruments=f["Instruments"][:]
        self.channels=f["Channels"][:]

        for akey in f["Instrument config"]:
            self.instrument_config[akey]=dict()
            for bkey, bitem in f["Instrument config"][akey].attrs.iteritems():
                self.instrument_config[akey][bkey]=bitem

        for akey in f["Data"]:
            self.data[akey]=f["Data"][akey][:]
        for akey, aitem in f["Data"].attrs.iteritems():
            self.data[akey]=aitem

        self.shaper=list(shape(f["Data"]["Data"]))
        print f["Traces"].keys()
        #key="Channels"
        #for akey, aitem in f[key].attrs.iteritems():
        #    print akey, aitem
        #for akey in f[key]:
        #    print akey, f[key][akey].keys()
        #print f[key]['Agilent VNA - Output power'].keys()
        #print f["Channels"][:] #.keys()
        #print f["Traces"].keys()
        for key in f["Traces"].keys():
            if key=="Time stamp":
                #if len(self.time_stamp)==0:
                self.time_stamp=f["Traces"]["Time stamp"][:]

#            else:
#                if key[-2:]!="_N" and key[-5:]!="_t0dt":
#                    self.trace_list.append(key)

        #self.trace_extract(f, trace_name=self.trace_list[0])
        #print f[key]["Channel names"].attrs.keys()
        #print key, f[key][:]
        #print shape(f[key]["Time stamp"])
        #print f["Traces"]["Agilent VNA - S21"+"_N"][:]
        #print f["Traces"]["Agilent VNA - S21"+"_t0dt"][:]

    def print_self(self):
        for mem in self.members():
            #print mem,
            attr=getattr(self, mem)
            #if isinstance(attr, list):
            #    attr=array(attr)
            print "{name}: {attr}".format(name=mem, attr=attr)

    def trace_extract(self, f, trace_name="Agilent VNA - S21"):
        print shape(f["Traces"][trace_name])
        print shape(f["Traces"]["Time stamp"])
        #sm=shape(Magvec)[0]
        #sy=shape(data)
        #print s
        #self.step_config["Traces"]=f["Log list"][:]
        self.numsteps=f["Traces"][trace_name+"_N"][0]
        self.f0=f["Traces"][trace_name+"_t0dt"][0][0]
        self.fstep=f["Traces"][trace_name+"_t0dt"][0][1]
        if len(self.frequency)==0:
            self.frequency=linspace(self.f0, self.f0+self.fstep*(self.numsteps-1), self.numsteps)
        s=(self.numsteps, self.shaper[0], self.shaper[2])
        Magvec=f["Traces"][trace_name]
        Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
        self.magcom=reshape(Magcom, s, order="F")

    @private_property
    def view_window(self):
        from enaml import imports
        with imports():
            from SS_FileParser_enaml import Main
        return Main(ss=self)

#    def show(self):
#        app=QtApplication()
#        with imports():
#            from SS_FileParser_enaml import Main
#        view=Main(ss=self)
#        view.show()
#        app.start()


dp=DataParser()

with File(file_path, "r") as f:
    dp.read_ssfile(f)
    #dp.trace_extract(f)
    #dp.print_self()
    #print dp.magcom.dtype
from taref.core.shower import shower
shower(dp)
#dp.show()