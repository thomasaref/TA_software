# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:50:49 2015

@author: thomasaref
"""

from LOG_functions import  log_info, log_warning, make_log_file, remove_log_file
log_info(1)
from Atom_Filer import Filer
from atom.api import Bool, Dict, Unicode, observe, List, Event, Enum, Typed, Int
log_info(2)
from os.path import exists as os_path_exists, splitext as os_path_splitext, split as os_path_split
from os import makedirs as os_makedirs
from shutil import move, copyfile
from inspect import getfile
log_info(3)
from numpy import ndarray, size
from enaml import imports
from enaml.qt.qt_application import QtApplication
from Atom_Read_File import Read_HDF5, Read_NP, Read_TXT, Read_DXF
from collections import OrderedDict
from HDF5_functions import group, dataset
      

class Save_File(Filer):
    data_buffer=Typed(OrderedDict)
    buffer_save=Bool(False)
    buffer_size=Int(100).tag(desc="size of buffer as number of elements in a list/array")
    #default_group_name=Unicode()
    save_event=Event()
    save_file=Typed()

    def _default_data_buffer(self):
        return OrderedDict()

    #@property
    #def buffer_flush(self):
    #    """returns if buffer should be flushed"""
    #    return size(self.data_buffer[group_name][name][namestr])>self.buffer_size or size(self.data_buffer[group_name][name].keys())>self.buffer_size

#    def close(self):
#        self.save_file.flush()
#        self.save_file.close()
        
    @property
    def view(self):
        return "Save_File"

    def _observe_dir_path(self, change):
        """if the file path exists and the file location is changed, this function moves the
        entire directory to the new location and sets up the log file for appended logging"""
        if change['type']!='create':
            old_dir_path=change['oldvalue']
            if not os_path_exists(self.file_path):
                if os_path_exists(old_dir_path):
                    remove_log_file()
                    move(old_dir_path, self.dir_path)
                    make_log_file(self.log_path)
                    log_info("Moved files to: {0}".format(self.dir_path))

    def makedir(self):
        """creates the directory and data file and log file"""
        if not os_path_exists(self.dir_path):
            os_makedirs(self.dir_path)
            log_info("Made directory at: {0}".format(self.dir_path))
        if not os_path_exists(self.file_path):
            self.create_file()
            make_log_file(self.log_path, overwrite=True)

    def save_code(self, obj):
        """saves the code containing the passed in object"""
        if obj is not None:
            module_path, ext = os_path_splitext(getfile(obj))
            code_file_path = module_path + '.py'   # Should get the py file, not the pyc, if compiled.
            code_file_copy_path = self.dir_path+self.divider+os_path_split(module_path)[1]+".pyb"
            if not os_path_exists(code_file_copy_path):
                copyfile(code_file_path, code_file_copy_path)
                log_info("Saved code to: {0}".format(code_file_copy_path))

    def full_save(self, obj=None):
        """does a full save, making files and directories, flushing the buffers, and saving the code"""
        self.makedir()
        self.flush_buffers()
        self.save_code(obj)
        self.save_event()

    def flush_buffers(self):
        self.do_data_save()
        self.data_buffer=self._default_data_buffer()
        
#        write_hdf5(self)
##        if self.buffer_save:
 #           self.buffer_save=False
 #           for group_name, item in self.data_buffer.iteritems():
 #               for name, subitem in item.iteritems():
 ##                   for key, arr in subitem.iteritems():
  #                      self.data_save(arr, name=name, group_name=group_name)
  #          self.data_buffer=OrderedDict()
  #          self.buffer_save=True

    def data_save(self):
        pass
#    def data_save(self, data, name="Measurement", group_name="Data", append=True):
#        """grows data_buffer using name and group_name and flushes when length exceeds buffer_size"""
#        if group_name not in self.data_buffer.keys():
#            self.data_buffer[group_name]=group()
#        if name not in self.data_buffer[group_name].keys():
#            self.data_buffer[group_name][name]=group(attrs=dict(append=append))
#            append=False
#        if type(data) not in [list, ndarray]:
#            data=[data]
#        if append==False:
#            namestr="{0}".format(len(self.data_buffer[group_name][name]))
#            self.data_buffer[group_name][name][namestr]=dataset(data=data, append=append)
#        else:
#            namestr="{0}".format(len(self.data_buffer[group_name][name])-1)
#            self.data_buffer[group_name][name][namestr].extend(data)
#        if size(self.data_buffer[group_name][name][namestr])>self.buffer_size or size(self.data_buffer[group_name][name].keys())>self.buffer_size:
#            self.flush_buffers() #self.do_data_save(data, name, group_name, append)

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

    def do_data_save(self):
        log_warning("do_data_save not overwritten")

from HDF5_functions import create_hdf5, hdf5_data_save, write_hdf5
class Save_HDF5(Save_File):
    data_buffer=Typed(group)
    
    def _default_data_buffer(self):
        return group(attrs=dict(comment=self.comment))

    def _default_file_type(self):
        return "HDF5"

    def create_file(self):
        create_hdf5(self.file_path)
        log_info("Created hdf5 file at: {0}".format(self.file_path))

    def do_data_save(self):
        write_hdf5(file_path=self.file_path, data=self.data_buffer)
        #hdf5_data_save(file_path=self.file_path, data=data, name=name, group_name=group_name, append=append)
    
    def data_save(self, data, name="Measurement", group_name="Data", append=True):
        """grows data_buffer using name and group_name and flushes when length exceeds buffer_size"""
        if group_name not in self.data_buffer.keys():
            self.data_buffer[group_name]=group()
        if name not in self.data_buffer[group_name].keys():
            self.data_buffer[group_name][name]=group() #attrs=dict(append=append))
            append=False
        if type(data) not in [list, ndarray]:
            data=[data]
        if append==False:
            namestr="{0}".format(len(self.data_buffer[group_name][name]))
            self.data_buffer[group_name][name][namestr]=dataset(data=data, append=append)
        else:
            namestr="{0}".format(len(self.data_buffer[group_name][name])-1)
            self.data_buffer[group_name][name][namestr].extend(data)
        if size(self.data_buffer[group_name][name][namestr])>self.buffer_size or size(self.data_buffer[group_name][name].keys())>self.buffer_size:
            self.flush_buffers() #self.do_data_save(data, name, group_name, append)

from TXTNP_functions import create_txt,  save_txt_data, save_np_data, save_txt
class Save_TXT(Save_File):
    def _default_file_type(self):
        return "text"

    def create_file(self):
        create_txt(self.dir_path)
        log_info("Created txt file at: {0}".format(self.file_path))

    def data_save(self, data, name="Measurement"):
        name=name.replace(" ", "_")
        if type(data) not in [list, ndarray]:
            data=[data]
        if name not in self.data_buffer.keys():
            self.data_buffer[name]=data
        else:
            self.data_buffer[name].extend(data)
        if size(self.data_buffer[name])>self.buffer_size:
            self.flush_buffers()

    def do_data_save(self):
        save_txt_data(self.dir_path+self.divider, self.data)
        
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

    def direct_save(self, verts, color, layer, file_path=None, write_mode='w'):
        if file_path is None:
            file_path=self.file_path
        save_dxf(verts, color, layer, file_path, write_mode)
        log_info("Direct save of data to: {}".format(file_path))

if __name__=="__main__2":

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

