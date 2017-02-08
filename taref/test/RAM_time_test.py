# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 18:15:03 2017

@author: thomasaref
"""

from numpy import matrix, exp, sqrt, pi

rs=1j*0.02
ts=sqrt(1+rs**2)

v=3488.0
f=4.4e9

lbda=v/f

k=2*pi/lbda

p=lbda/2.0

jkp=1j*k*p

A=matrix([[1.0/ts*exp(-jkp), rs/ts],
          [-rs/ts, 1.0/ts*exp(jkp)]])

Np=3
N=4*Np-3

print A
AN=A**N
print AN
(AN11, AN12,
 AN21, AN22)=(AN[0,0], AN[0,1], AN[1,0], AN[1,1])

print AN11, AN12,AN21, AN22

P11=-AN21/AN22
P21=AN11-AN12*AN21/AN22
P12=1.0/AN22
P22=AN12/AN22
B=matrix([(1-rs/ts+1/ts)*exp(-jkp/2), (1+rs/ts+1/ts)*exp(jkp/2)])
print A**0

L=p*N


strt=matrix([0,1.0/AN22*exp(-1j*k*(L-2*p)/2.0)])

#[(4*n-4, 4*n-3)for n in range(1, Np+1)]

Asum=sum([A**(4*n-4)+A**(4*n-3) for n in range(1, Np+1)])

P32=B*(A**0+A**1+A**4+A**5+A**8+A**9)*strt
P23=-P32/2.0
P13=-P31/2.0
P13=P23