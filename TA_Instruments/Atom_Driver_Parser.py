# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 12:52:52 2015

@author: thomasaref
"""

from Atom_Text_Editor import Text_Editor
from Atom_Base import Base
from atom.api import Unicode

def get(td, key):
    if key in td.keys():
        return td[key]
    return None
    
class Driver_Parser(Base):
    instr_name=Unicode()
    
    def produce_driver(self):
        pass
    
    def parse_driver(self, data):
        in_visa=False
        td={}
        data_list=data.split("\n")
        for n, line in enumerate(data_list):
            if line!="" and not line.startswith("#"):
                if "[Model and options]" in line or "[VISA settings]" in line:
                    in_visa=True
                if in_visa:
                   if line.startswith("[") and "[General settings]" not in line and "[Model and options]" not in line and "[VISA settings]" not in line:
                       td={}
                       td["bracket"]=line.split("[")[1].split("]")[0].strip()
                   elif line.startswith("name"):
                       td["name"]=line.partition(":")[2].strip()
                   elif line.startswith("datatype"):
                       td["datatype"]=line.partition(":")[2].strip()
                   elif line.startswith("unit"):
                       td["unit"]=line.partition(":")[2].strip()
                   elif line.startswith("enabled"):
                       td["enabled"]=line.partition(":")[2].strip()
                   elif line.startswith("def_value"):
                       td["def_value"]=line.partition(":")[2].strip()
                   elif line.startswith("low_lim"):
                       td["low_lim"]=line.partition(":")[2].strip()
                   elif line.startswith("high_lim"):
                       td["high_lim"]=line.partition(":")[2].strip()
                   elif line.startswith("combo_def_"):
                       if "combo_def" not in td.keys():
                           td["combo_def"]=[]
                       td["combo_def"].append(line.partition(":")[2].strip())
                   elif line.startswith("cmd_def_"):
                       if "cmd_def" not in td.keys():
                           td["cmd_def"]=[]
                       td["cmd_def"].append(line.partition(":")[2].strip())
                   elif line.startswith("group"):
                       td["group"]=line.partition(":")[2].strip()
                   elif line.startswith("state_quant"):
                       td["state_quant"]=line.partition(":")[2].strip()
                   elif line.startswith("state_value"):
                       if "state_value" not in td.keys():
                           td["state_value"]=[]
                       td["state_value"].append(line.partition(":")[2].strip())
                   elif line.startswith("permission"):
                       td["permission"]=line.partition(":")[2].strip()
                   elif line.startswith("set_cmd"):
                       td["set_cmd"]=line.partition(":")[2].strip()
                   elif line.startswith("group"):
                       td["sweep_cmd"]=line.partition(":")[2].strip()
                   elif line.startswith("group"):
                       td["get_cmd"]=line.partition(":")[2].strip()
    
                elif line.startswith("name"):
                    self.instr_name=line.partition(":")[2].strip()
                else:
                    print line
        print td
        self.create_var(td)
    def create_var(self, td):
        if td!={}:
            tempstr=""
            if td["datatype"]=='COMBO':
                mapping = dict(zip(td["combo_def"], td["cmd_def"]))
                tempstr+="Enum{combo_def}.tag(mapping={mapping}, ".format(combo_def=tuple(td["combo_def"]), mapping=mapping)
            if "set_cmd" in td.keys():
                print td["set_cmd"]
                tempstr+="set_cmd={set_cmd}, ".format(set_cmd=repr(td["set_cmd"]))
            if "get_cmd" in td.keys():
                tempstr+="get_cmd={get_cmd}, ".format(get_cmd=td["get_cmd"])

            tempstr=tempstr[:-2]+")\n"
            if "def_value" in td.keys():
                tempstr+="\ndef _default_name(self):\n\treturn '{def_value}'\n\n".format(def_value=td["def_value"])
            print tempstr
if __name__=="__main__":
    a=Text_Editor(name="ini_viewer", dir_path="/Users/thomasaref/Documents/Thomas/Research/SampleFiles", main_file="Keithley_2000_Multimeter.ini")
    a.read_file.read()
    b=Driver_Parser()
    b.parse_driver( a.data)    
    a.show()