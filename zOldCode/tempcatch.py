# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:19:19 2015

@author: thomasaref
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/Users/thomasaref/.spyder2/.temp.py
"""

from numpy import concatenate, array, linspace, meshgrid, exp, transpose, atleast_2d, split
#            #zdata=concatenate(zdata, array([[1,2,3]]))
#            xs = linspace(0, 10, 6)
#            ys = linspace(0, 5, 6)
#            x, y = meshgrid(xs,ys)
#            z = exp(-(x**2+y**2)/100)
#
#            #zz= plotr.splitMultiD(zdata)
#            #print zz
#            #zz.append(array([[1.0],[2.0],[3.0]]))
#            #print zz
#            #z=plotr.gatherMultiD(zz)
#            z=concatenate((zdata, transpose(atleast_2d([1,2,3]))), axis=1)
# 
def line_up(arrin):
    arr=array(arrin)
    if arr.ndim<2:
        return transpose(atleast_2d(arr))
    else:
        return arr
           
def concat2(*args):
    print args
    return concatenate(args)       
def concat(*args):
    print args
    print transpose(atleast_2d(args))
    #args2=(line_up(o) for o in args)
    #return concat2(*args2)
    return transpose(concatenate(atleast_2d(*args)))

    #print *args


        
def splitMultiD(arr, axis=1):
    if arr.ndim<2:
        return atleast_2d(arr)
    else:
        return transpose(split(arr, arr.shape[axis], axis=axis))

mylist=[[1,2,3], [4,5,6], [7,8,9]]
myarr=concat(*mylist)   
print myarr
print splitMultiD(myarr, 1)
#print concat(myarr, [10,11,12])
def gatherMultiD(self, arrs, axis=1):
         print arrs[0].ndim
#             print "yo"
         return concatenate(arrs, axis)
#from operator import attrgetter
#
##print dir(slice(None))
#
#class a:
#    def __init__(self, b):
#        self.b=b
#    
#c=[a(2), a(3), a(4)]
#d=[a(1), a(3), a(5)]
#
#attr=(o.b for o in c)
#attr2=(o.b for o in d)
#print 2 in attr
#print 2 in attr2
##print list(set(attr).intersection(attr2))[0]
##print attr.next()
#print d in c
##print 1 in attr
#print 3 in attr
#print 4 in attr
#print 2 in attr



#f = attrgetter('b')
#print f(c)
# myapp.py
#import logging
#import mylib

#def main():
#    logging.basicConfig(filename='myapp.log', level=logging.INFO)
#    logging.info('Started')
#    mylib.do_something()
#    logging.info('Finished')

#if __name__ == '__main__':
#    main()
# mylib.py
#import logging

def do_something():
    logging.info('Doing something')

#logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

#from atom.api import Atom, Range, FloatRange, Dict
#from collections import OrderedDict

#print vars(Atom)
#for x in range(1,11):
#    print '{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x)
#class Experiment(Atom):
#    md=Dict()
#    coef = FloatRange(-1.0, 1.0, 0.0)
#
#    gain = Range(0, 100, 10)
#
#class LastUpdatedOrderedDict(OrderedDict):
#    'Store items in the order the keys were last added'
#
#    def __setitem__(self, key, value):
#        if key in self:
#            del self[key]
#        OrderedDict.__setitem__(self, key, value)
#
#zerogp = 200e-6 #200 uV, gap of aluminum at zero temperature
#Tc=1.3
#Delta=1.76*k*Tc
##print Delta*1e6
##T=0.3
##print pi*Delta/(2*e)*tanh(Delta/(2*k*T))
#Ic=100e-9
#Rn=pi*Delta/(2.0*e)/Ic
#print Rn
#EjoverEc=65
#
#f0=4.8e9
#
#Ej= sqrt(EjoverEc*(h*f0)**2/8.0) 
#Ec=Ej/EjoverEc
#Ctr = e**2/(2.0*Ec)
#Ltr = (hbar/(2.0*e ))**2/Ej
##Ej=hbar Ic/(2.0*e)
#Ic=Ej/hbar*(2.0*e)# Ic/(2.0*e)
#
#N=7
#W=25.0e-6
#epsinf=46*eps0
##                Dvv=2.4e-2,
##                v=3488.0),
#Ctr=N*W*epsinf*sqrt(2)
#Ec = e**2/(2.0*Ctr)
#Ej=Ec*EjoverEc
#
#f0=sqrt((8.0/EjoverEc)*Ej**2)/h#= EjoverEc*(h*f0)**2/8.0 
#print Ej, Ec, Ctr, Ltr, Ic
#Rn=pi*Delta/(2.0*e)/Ic
#print Rn, Ej/Ec, f0/1.0e9

#if __name__ == '__main__':
#    exp = Experiment()
#    md=OrderedDict()
#    md['a']=2
#    md['b']=3
#    md[1]=1
#    md[2]=2
#    print md.items()
#    print dir(type(exp).coef)
#    print exp.get_member('coef').validate_mode[1][0]
#    exp.coef = 0.5
#    print(exp.coef)

#    print(exp.gain)
#    exp.gain = 99
#    print(exp.gain)