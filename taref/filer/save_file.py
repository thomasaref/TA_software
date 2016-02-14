# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:50:49 2015

@author: thomasaref
"""

from taref.core.log import  log_info, make_log_file, remove_log_file, log_debug
from taref.filer.filer import Filer
from atom.api import cached_property, Unicode, List, Event, Enum, Typed, Int, Bool
from os.path import exists as os_path_exists#, splitext as os_path_splitext, split as os_path_split
from os import makedirs as os_makedirs
from shutil import move#, copyfile
#from inspect import getfile
from numpy import ndarray, size
#from taref.core.read_file import Read_HDF5, Read_NP, Read_TXT, Read_DXF
#from collections import OrderedDict
from taref.core.atom_extension import tag_Callable

from taref.filer.HDF5_functions import rewrite_hdf5, group, dataset#, File
from taref.core.universal import write_text
#from taref.core.TXTNP_functions import  save_txt_data, save_np_data, save_txt

from enaml import imports
with imports():
    from taref.filer.read_file_e import ReadFileExt, ReadFileMain

class Save_File(Filer):
    buffer_size=Int(100).tag(desc="size of buffer as number of elements in a list/array")
    save_event=Event()
    file_created=Bool(False)
    write_mode=Enum("w", "a")
    flush_buffer=Bool(True)
    fixed_mode=Bool(False)
    comment=Unicode()

    def _default_show_details(self):
        return False

    def _default_show_simple(self):
        return False

    @tag_Callable(button_label="Save")
    def file_action(self):
        self.save()

    @cached_property
    def data_str(self):
        return unicode(self.data_buffer)

    def log_save(self):
        log_info("save not implemented! file not saved: {0}".format(self.file_path))

    def log_create(self):
        log_info("save not implemented! file not created at {0}".format(self.file_path))

#    def browse_clicked(self):
#        super(Save_File, self).browse_clicked()
#        self.save()

    def save(self, data=None, *args, **kwargs):
        self.save_event()
        write_mode=kwargs.pop("write_mode", None)
        if write_mode is not None:
            self.write_mode=write_mode
        flush_buffer=kwargs.pop("flush_buffer", None)
        if flush_buffer is not None:
            self.flush_buffer=flush_buffer
        if data is None:
            self.flush_buffer=True
        else:
            self.buffer_save(data, *args, **kwargs)
            self.get_member("data_str").reset(self)
        if self.flush_buffer:
            self.makedir()
            if not self.file_created:
                self.log_create()
                self.file_created=True
            self.save_to_file()
            self.data_buffer=self._default_data_buffer()
            self.flush_buffer=False
        if not self.fixed_mode:
            self.write_mode="a"
        self.log_save()

    @cached_property
    def view(self):
        return ReadFileExt

    @cached_property
    def view_window(self):
        """stand alone for showing save file."""
        return ReadFileMain(agent=self)

    def close(self):
        """flushes the butter using save"""
        self.save()

    def _observe_dir_path(self, change):
        """if the file path exists and the file location is changed, this function moves the
        entire directory to the new location and sets up the log file for appended logging"""
        if change['type']!='create':
            old_dir_path=change['oldvalue']
            if old_dir_path is None:
                old_dir_path=""
            if not os_path_exists(self.file_path):
                if os_path_exists(old_dir_path):
                    remove_log_file()
                    move(old_dir_path, self.dir_path)
                    make_log_file(self.log_path)
                    log_info("Moved files to: {0}".format(self.dir_path))

    def makedir(self):
        """creates the directory and data file and log file"""
        if not os_path_exists(self.folder.dir_path):
            os_makedirs(self.folder.dir_path)
            log_info("Made directory at: {0}".format(self.folder.dir_path))
        #if not os_path_exists(self.file_path):
            #if hasattr(self, "save_file"):
            #    self.save_file=self._default_save_file() #self.create_file()
            #make_log_file(self.log_path, mode="w")

#    def save_code(self, obj):
#        """saves the code containing the passed in object"""
#        if obj is not None:
#            module_path, ext = os_path_splitext(getfile(obj))
#            code_file_path = module_path + '.py'   # Should get the py file, not the pyc, if compiled.
#            code_file_copy_path = self.dir_path+self.divider+os_path_split(module_path)[1]+".pyb"
#            if not os_path_exists(code_file_copy_path):
#                copyfile(code_file_path, code_file_copy_path)
#                log_info("Saved code to: {0}".format(code_file_copy_path))

#    def full_save(self, obj=None):
#        """does a full save, making files and directories, flushing the buffers, and saving the code"""
#        self.makedir()
#        self.save()
#        self.flush_buffers()
#        #self.save_code(obj)

    #def flush_buffers(self):
    #    pass

    #    self.do_data_save()
    #    self.data_buffer=self._default_data_buffer()

    #def do_data_save(self):
    #    log_warning("do_data_save not overwritten")

class Save_HDF5(Save_File):
    data_buffer=Typed(group)

    def log_create(self):
        log_info("Created hdf5 file at: {0}".format(self.file_path))

    def log_save(self):
        log_info("Data saved to hdf5 file at: {0}".format(self.file_path))

    def _default_data_buffer(self):
        return group(attrs=dict(comment=self.comment))

    def _default_file_suffix(self):
        return "hdf5"

    def save(self, data=None,  name="Measurement", group_name="Data", append=True, write_mode=None):
        super(Save_HDF5, self).save(data,  name=name, group_name=group_name, append=append, write_mode=write_mode)

    def save_to_file(self):
        rewrite_hdf5(self.save_file, self.data_buffer)


    def buffer_save(self, data, name="Measurement", group_name="Data", append=True):
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
            self.flush_buffer=True #() #self.do_data_save(data, name, group_name, append)

    @cached_property
    def view_window(self):
        with imports():
            from taref.filer.filer_e import SaveMain
        return SaveMain(save_file=self, read_file=Read_HDF5(file_path=self.file_path))

class Save_TXT(Save_File):
    data_buffer=List()

    def _default_data_buffer(self):
        return []

    def default_file_suffix(self):
        return ".txt"

    def log_create(self):
        log_info("Created text file at: {0}".format(self.file_path))

    def log_save(self):
        log_debug("Data saved to text file at: {0}".format(self.file_path))

    def buffer_save(self, text_list):
        self.data_buffer.extend(text_list)
        if len(self.data_buffer)>=self.buffer_size:
            self.flush_buffer=True

    def save_to_file(self):
        write_text(self.file_path, self.data_buffer, mode=self.write_mode)

    def save(self, data=None, write_mode=None, flush_buffer=None):
        if not isinstance(data, list) and data is not None:
            data=[unicode(data)]
        super(Save_TXT, self).save(data, write_mode=write_mode, flush_buffer=flush_buffer)

    #@cached_property
    #def view_window(self):
    #    with imports():
    #        from taref.core.filer_e import SaveMain
    #    return SaveMain(save_file=self, read_file=Read_TXT(file_path=self.file_path))

class Save_NP(Save_TXT):
    def _default_file_suffix(self):
        return ".txt"

    def do_data_save(self, data, name, group_name, append):
        save_np_data(self.dir_path+self.divider, data, name)

from taref.ebl.DXF_functions import save_dxf

class Save_DXF(Save_File):
    def _default_file_suffix(self):
        return ".dxf"

    #def _default_base_dir(self):
    #    return self.base_dir+self.divider+"OutputPatterns"

    def direct_save(self, verts, color, layer, file_path=None, write_mode='w'):
        if file_path is None:
            file_path=self.file_path
        save_dxf(verts, color, layer, file_path, write_mode)
        log_info("Direct save of data to: {}".format(file_path))


if __name__=="__main__":
    from taref.core.shower import shower

    a=Save_TXT()
    shower(a)

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

