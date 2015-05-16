# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 20:17:59 2015

@author: thomasaref
"""

from numpy import ndarray, savetxt

def save_np_data(dir_path, data, name, append=True):
    savetxt(dir_path+name, data)
    
def create_txt(dir_path):
    pass
    #with open(dir_path+"Full_Log", 'w') as f:
    #    f.write("Full Log\n\n")
    
def save_txt_log(dir_path, new_string, log="Full Log"):      
    log=log.replace(" ", "_")
    with open(dir_path+log, 'a') as f:
       f.write(new_string)

def save_txt_data(dir_path, data, name, append=True):       
    if type(data)==dict:
        print data
    else:
        print dir_path+name
        name=name.replace(" ", "_")
        if type(data) not in [list, ndarray]:
            data=[data]
        with open(dir_path+name, 'a') as f:
            for d in data:
                f.write(str(d)+"\n")
                
def save_txt(file_path, data, write_mode='a'):       
    if type(data) not in [list, ndarray]:
        data=[data]
    with open(file_path, write_mode) as f:
        for d in data:
            f.write(str(d)+"\n")