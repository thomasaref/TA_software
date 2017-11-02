# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 20:02:28 2017

@author: thomasaref
"""

from json import load
from urllib2 import urlopen


j=urlopen("http://ergast.com/api/f1/1957/results.json")
a = load(j)

print "givenName\t\tfamilyName\t\tdateOfBirth\tnationality"

for n in range(5):
    b=a["MRData"]["RaceTable"]["Races"][0]["Results"][n]["Driver"]
    print "{0}\t\t{1}\t\t{2}\t\t{3}".format(b["givenName"], b["familyName"], b["dateOfBirth"], b["nationality"])
    