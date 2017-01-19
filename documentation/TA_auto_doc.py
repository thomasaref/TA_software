# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 13:18:39 2017

@author: thomasaref
"""

from os import listdir, makedirs
from os.path import exists

base_path=r"/Users/thomasaref/TA_software/documentation/"

parts=["core", "analysis",  #"filer",  "plotter", "tex",# "physics", "instruments", "ebl"
]


#file_names=[f for f in listdir(r"/Users/thomasaref/TA_software/taref") if not f.startswith("_") and not f.startswith(".")]
#print file_names

#for file in os.listdir("/mydir"):
#    if file.endswith(".txt"):
#        print(file)

#pn=parts[1]
for pn in parts:
    dir_path=base_path+pn+"_doc"
    
    if not exists(dir_path):
        makedirs(dir_path)
        print "Made directory at: {0}".format(dir_path)
    
    file_names=[f[:-3] for f in listdir(r"/Users/thomasaref/TA_software/taref/{}".format(pn)) if f.endswith("py") and not f.startswith("_")]
    
    for fn in file_names:
        strlist=["*******************",
                 fn, 
                 "*******************",
                 "",
                 ".. automodule:: taref.{pn}.{fn}".format(pn=pn, fn=fn),
                 "    :members:",
                 "    :undoc-members:",
                 ]
        with open(dir_path+"/"+"{fn}.rst".format(fn=fn), "w") as f:
            f.write("\n".join(strlist))
    
    strlist=[pn,
             "======================================",
             "",
             "Contents:",
             "",
             ".. toctree::",
             "    :maxdepth: 2",
             ""]
    strlist.extend(["    {}.rst".format(fn) for fn in file_names])         
    
    with open(dir_path+"/"+"{pn}.rst".format(pn=pn), "w") as f:
        f.write("\n".join(strlist))

strlist=["taref",
         "======================================",
         "",
         "Contents:",
         "",
         ".. toctree::",
         "    :maxdepth: 2",
         ""]

strlist.extend(["    {0}_doc/{0}.rst".format(pn) for pn in parts])         


with open(base_path+"taref.rst", "w") as f:
    f.write("\n".join(strlist))
    
#taref
#======================================
#
#Contents:
#
#.. toctree::
#    :maxdepth: 2
#
#    core_doc/core.rst
#    physics_doc/physics.rst
#    analysis_doc/analysis.rst

