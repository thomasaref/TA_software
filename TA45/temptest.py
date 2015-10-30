# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 18:22:36 2015

@author: thomasaref
"""

from numpy import loadtxt, shape, interp, linspace, savetxt


data=loadtxt("/Users/thomasaref/Downloads/bat54xv2.340", skiprows=8)

print shape(data)

from matplotlib.pyplot import plot, show
N=linspace(1,200, 200)
x=linspace(2,300, 200)
y=interp(x, data[::-1,2], data[::-1,1])
plot(data[:,2], data[:,1], )

x=x[::-1]
y=y[::-1]
plot(x, y, 'o' )
show()

print x
print y
savetxt("temptestout.txt", zip(N,y,x), delimiter="\t", fmt=["%d", "%.6f", "%.6f"])