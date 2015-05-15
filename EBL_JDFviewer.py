# -*- coding: utf-8 -*-
"""
Created on Thu May 14 18:38:47 2015

@author: thomasaref
"""

from Atom_Base import Base
from atom.api import Str, observe, Unicode
from Atom_Boss import Boss
from Atom_Read_File import Read_TXT
from LOG_functions import log_info, log_debug, make_log_file, log_warning

class Read_JDF(Read_TXT):
    """extends Read_TXT for jdf files"""
    def data_distributor(self, templist):
        self.data["jdf_view"]={"jdf_file": "".join(templist)}
                
class JDF_Boss(Boss):
    @observe('read_file.read_event')
    def obstest(self, change):
        print change

    def read_data_distribute(self):
        #log_warning("read_data_distribute not implemented!")
#        self.bases[0].jdf_file=str(self.read_file.data)
        #self.read_file.data={"blah":{"jdf_file":"yoyoyoy"}}
        for key, item in self.read_file.data.iteritems():
            target=filter(lambda x: x.name==key, a.boss.bases)
            if target!=[]:
                for subkey, subitem in item.iteritems():
                    if subkey in target[0].all_params:
                        setattr(target[0], subkey, subitem)
                    else:
                        log_warning("target base does not have target param!")
            else:
                log_warning("target base not found!")
        
    def _default_read_file(self):
        return Read_JDF(file_path="/Users/thomasaref/Dropbox/Current stuff/TA_software/idt.jdf")

jdfboss=JDF_Boss()
        
class JDF_Viewer(Base):
    name=Unicode("jdf_view").tag(private=True)
    jdf_file=Str().tag(discard=True, log=False)

    def read(self):
        self.boss.full_read()
        
    def _default_boss(self):
        jdfboss.BASE_DIR="/Users/thomasaref/Dropbox/Current stuff/TA_software"
        jdfboss.DIVIDER="/"
        jdfboss.LOG_NAME="record"
        jdfboss.FILE_NAME="meas"
        jdfboss.SETUP_GROUP_NAME="SetUp"
        jdfboss.SAVE_GROUP_NAME="Measurements"
        make_log_file(log_path=jdfboss.BASE_DIR+jdfboss.DIVIDER+jdfboss.LOG_NAME+".log")  #default log file
        return jdfboss
    
if __name__=="__main__":
    a=JDF_Viewer()
    a.read()
    print  a.jdf_file
    #a.show()