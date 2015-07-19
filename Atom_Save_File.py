# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:50:49 2015

@author: thomasaref
"""

from Atom_Filer import Filer
from atom.api import Bool, Dict, Unicode, observe, List, Event, Enum
import os
import shutil
import inspect
from numpy import ndarray
from LOG_functions import  log_info, log_warning, move_files_and_log, log_flush, move_log_file
from enaml import imports
from enaml.qt.qt_application import QtApplication
from Atom_Read_File import Read_HDF5, Read_NP, Read_TXT, Read_DXF

SETUP_GROUP_NAME="SetUp"
SAVE_GROUP_NAME="Measurements"

class Save_File(Filer):
    data_buffer=Dict()
    buffer_save=Bool(False)
    default_group_name=Unicode()
    group_names=List()
    save_event=Event()
    view=Enum("Save_File", "Auto")
    #files_exist=Bool(False)

    def _default_data_buffer(self):
        return {SAVE_GROUP_NAME:{}, SETUP_GROUP_NAME:{}}

    def _default_group_names(self):
        return self.data_buffer.keys()

    def _default_default_group_name(self):
        return sorted(self.data_buffer.keys())[0]
#    def _default_string_buffer(self):
#        return {SAVE_GROUP_NAME:{}, SETUP_GROUP_NAME:{}}

    #def _observe_buffer_save(self, change):
    #    print change

    @observe( "dir_path")
    def filedir_path_changed(self, change):
        """if the file path exists and the file location is changed, this function moves the entire directory to the new location"""
        if change['type']!='create':
            old_dir_path=change['oldvalue']
            if not os.path.exists(self.file_path):
                if os.path.exists(old_dir_path):
                    move_files_and_log(self.dir_path+self.divider, old_dir_path+self.divider, self.log_name)
                    log_info("Moved files to: {0}".format(self.dir_path))

    def makedir(self, old_log_path=None):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        if not os.path.exists(self.file_path):
            self.create_file()
            if old_log_path==None:
                pass#make_log_file(self.dir_path+self.divider+self.log_name+".log") #start log file if it doesn't exist
            else:
                move_log_file(self.dir_path+self.divider+self.log_name+".log", old_log_path+".log") #move backup log to folder and

    def save_code(self, obj):
        """saves the code containing the passed in object"""
        module_path, ext = os.path.splitext(inspect.getfile(obj))
        code_file_path = module_path + '.py'   # Should get the py file, not the pyc, if compiled.
        code_file_copy_path = self.dir_path+self.divider+os.path.split(module_path)[1]+".pyb"
        if not os.path.exists(code_file_copy_path):
            shutil.copyfile(code_file_path, code_file_copy_path)
            log_info("Saved code to: {0}".format(code_file_copy_path))

    def full_save(self, obj=None, old_log_path=None):
        """does a full save, making files and directories, flushing the buffers, and saving the code"""
        #if old_log_path==None:
        #    old_log_path=self.log_name
        self.makedir(old_log_path)
        self.flush_buffers()
        if obj!=None:
            self.save_code(obj)
        self.save_event()


    def flush_buffers(self):
        if self.buffer_save:
            self.buffer_save=False
            log_flush()
            for group_name, item in self.data_buffer.iteritems():
                for name, subitem in item.iteritems():
                    for key, arr in subitem.iteritems():
                        self.data_save(arr, name=name, group_name=group_name)
            #for group_name, item in self.string_buffer.iteritems():
            #    for name, subitem in item.iteritems():
            #        for key, newstr in subitem.iteritems():
            #            self.string_save(newstr, name=name, group_name=group_name)
            self.data_buffer=self._default_data_buffer()
            #self.string_buffer=self._default_string_buffer()
            self.buffer_save=True

    def data_save(self, data, name="Measurement", group_name=None, append=True):
        if group_name==None:
            group_name=self.default_group_name
        if self.buffer_save:
            if name not in self.data_buffer[group_name].keys():
                self.data_buffer[group_name][name]=dict()
                append=False
            if type(data) not in [list, ndarray]:
                data=[data]
            if append==False:
                namestr="{0}".format(len(self.data_buffer[group_name][name]))
                self.data_buffer[group_name][name][namestr]=data
            else:
                namestr="{0}".format(len(self.data_buffer[group_name][name])-1)
                self.data_buffer[group_name][name][namestr].extend(data)
        else:
            self.do_data_save(data, name, group_name, append)

    def show(self, read_file=None, coder=None):
        """stand alone for showing filer."""
        if read_file==None:
            if self.file_type=='HDF5':
                read_file=Read_HDF5(file_path=self.file_path)
            elif self.file_type=='dxf':
                read_file=Read_DXF(file_path=self.file_path)
            elif self.file_type=='text data':
                read_file=Read_NP(file_path=self.file_path)
            else:
                read_file=Read_TXT(file_path=self.file_path)
        with imports():
            from enaml_Filer import SaveMain
        app = QtApplication()
        view = SaveMain(save_file=self, read_file=read_file, coder=coder)
        view.show()
        app.start()

    def create_file(self):
        log_warning("create_file not overwritten")

    def do_data_save(self, data, name, groupname, append):
        log_warning("do_data_save not overwritten")

from HDF5_functions import create_hdf5, hdf5_data_save
class Save_HDF5(Save_File):
    def _default_file_type(self):
        return "HDF5"
    def create_file(self):
        create_hdf5(self.file_path, self.group_names)
        log_info("Created hdf5 file at: {0}".format(self.file_path))

    def do_data_save(self, data, name, group_name, append):
        hdf5_data_save(file_path=self.file_path, data=data, name=name, group_name=group_name, append=append)

from TXTNP_functions import create_txt,  save_txt_data, save_np_data, save_txt
class Save_TXT(Save_File):
    def _default_file_type(self):
        return "text"

    def create_file(self):
        create_txt(self.dir_path)
        log_info("Created txt file at: {0}".format(self.file_path))

    def do_data_save(self, data, name, group_name, append):
        save_txt_data(self.dir_path+self.divider, data, name)
        
    def direct_save(self, data, write_mode='a'):
        save_txt(file_path=self.file_path, data=data, write_mode=write_mode)
        log_info("Direct save of data to: {}".format(self.file_path))

class Save_NP(Save_TXT):
    def _default_file_type(self):
        return "text data"

    def do_data_save(self, data, name, group_name, append):
        save_np_data(self.dir_path+self.divider, data, name)

from DXF_functions import save_dxf

class Save_DXF(Save_File):
    def _default_file_type(self):
        return "dxf"

    #def _default_base_dir(self):
    #    return self.base_dir+self.divider+"OutputPatterns"

    def direct_save(self, data, write_mode='w'):
        save_dxf(file_path=self.file_path, data=data, write_mode=write_mode)
        log_info("Direct save of data to: {}".format(self.file_path))

if __name__=="__main__":

    a=Save_HDF5(buffer_save=True)
    print a.log_name
    log_info("prowdy")
    a.full_save()
    a.data_save(2, name="a")
    a.data_save([1,2,3], name="b")
    from numpy import array
    a.data_save(array([1,2,3]), name="b")
    a.data_save([4,5], name="b")
    a.data_save(["blah", "bob", True], name="c")
    a.data_save(unicode("bob"), name="c")

    #a.makedir()
    log_info("yo")
    a.quality="less interesting"
    log_info("bro")

    #b=Read_HDF5(file_path=a.file_path)
    #print b.read()
    print a.data_buffer
    a.flush_buffers()
    a.show() #show_saver(a, b)

    #a.move_log_file()
    #a.update_log("yowdy")

