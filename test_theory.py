# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:26:51 2015

@author: thomasaref
"""
from LOG_functions import log_debug
from scipy.constants import k,h,pi, epsilon_0 as eps0
from numpy import (squeeze, shape, linspace, log10, mean, amax, amin, absolute, reshape, transpose, 
                   real, imag, angle, cos, sqrt, array, exp, delete, sin)

from h5py import File

epsinf=46.0*eps0
Dvv=2.4/100.0
Np=55
W=7.0e-6
f0=4.48e9
print 3488.0/(0.096*8)

#0.8*1j 2 Dvv * Np * sin(X)/X

Gs=Dvv/epsinf
#2Ps=(1/4)*2*pi*f*W/Gs*|phi|**2 = Y0 phi|**2
#  Y0=sqrt(2pifW/2Gs)
#Pv=Vt**2 Ga/2 = Y0 |phi| **2

#Pv=2Ps
#1.247 * \epsinf Dvv/epsinf * sqrt(2pif*W/2Gs)
C=sqrt(2)*W*Np*46*eps0
print C

Ga0=3.11*2*pi*f0*epsinf*W*Dvv*Np**2
#Ga0=(sqrt(2)*1.247)**2  Y0 Dvv**2 Np**2
print 1/Ga0

def X(f):
    return pi*Np*(f-f0)/f0

def Ga(X):
     return Ga0*(sin(X)/X)**2

def Ba(X):
    return Ga0*(sin(2.0*X)-2.0*X)/(2*X**2)
    
def Y(f):
    return Ga(X(f))+1j*Ba(X(f))+1j*2.0*pi*f*C

def R(f):
    return (1.0/Y(f)-50.0)/(1.0/Y(f)+50.0)

import matplotlib.pyplot as plt
fzero=4.494e9
frq=linspace(4.0e9, 5.0e9, 1000)
plt.plot(frq, Ga(X(frq)), label="Ga")
plt.plot(frq, Ba(X(frq)), label="Ba")
plt.plot(frq, 2.0*pi*frq*C, label=("2*pi*f*C"))
#plt.plot(frq, Ba(X(frq))+2.0*pi*frq*C)
#plt.plot(frq,0*frq)
plt.plot(frq, absolute(R(frq))/100.0, label="|S33|/100")
plt.plot([fzero, fzero], [-0.01, 0.02], label="f=4.494 GHz")
plt.legend()
plt.xlabel("Frequency (GHz)")
plt.ylabel("1/Ohm")
plt.title("Theory")
plt.show()

def dB(x):
    return 20*log10(absolute(x))
    
with File("/Users/thomasaref/Dropbox/Current stuff/TA_enaml/testwritetrans.h5", "r") as f:
    freq=f["freq"][:]
    trans=f["magcom"][:]

plt.plot(freq, dB(trans))
plt.plot(frq, 10*log10(absolute(Ga(X(frq))/Ga0))-36.45)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Transmission (dB)")
plt.title("Setting center frequency using transmission")
plt.show()

freq=array([  4.40000000e+09,   4.40050000e+09,   4.40100000e+09,
         4.40150000e+09,   4.40200000e+09,   4.40250000e+09,
         4.40300000e+09,   4.40350000e+09,   4.40400000e+09,
         4.40450000e+09,   4.40500000e+09,   4.40550000e+09,
         4.40600000e+09,   4.40650000e+09,   4.40700000e+09,
         4.40750000e+09,   4.40800000e+09,   4.40850000e+09,
         4.40900000e+09,   4.40950000e+09,   4.41000000e+09,
         4.41050000e+09,   4.41100000e+09,   4.41150000e+09,
         4.41200000e+09,   4.41250000e+09,   4.41300000e+09,
         4.41350000e+09,   4.41400000e+09,   4.41450000e+09,
         4.41500000e+09,   4.41550000e+09,   4.41600000e+09,
         4.41650000e+09,   4.41700000e+09,   4.41750000e+09,
         4.41800000e+09,   4.41850000e+09,   4.41900000e+09,
         4.41950000e+09,   4.42000000e+09,   4.42050000e+09,
         4.42100000e+09,   4.42150000e+09,   4.42200000e+09,
         4.42250000e+09,   4.42300000e+09,   4.42350000e+09,
         4.42400000e+09,   4.42450000e+09,   4.42500000e+09,
         4.42550000e+09,   4.42600000e+09,   4.42650000e+09,
         4.42700000e+09,   4.42750000e+09,   4.42800000e+09,
         4.42850000e+09,   4.42900000e+09,   4.42950000e+09,
         4.43000000e+09,   4.43050000e+09,   4.43100000e+09,
         4.43150000e+09,   4.43200000e+09,   4.43250000e+09,
         4.43300000e+09,   4.43350000e+09,   4.43400000e+09,
         4.43450000e+09,   4.43500000e+09,   4.43550000e+09,
         4.43600000e+09,   4.43650000e+09,   4.43700000e+09,
         4.43750000e+09,   4.43800000e+09,   4.43850000e+09,
         4.43900000e+09,   4.43950000e+09,   4.44000000e+09,
         4.44050000e+09,   4.44100000e+09,   4.44150000e+09,
         4.44200000e+09,   4.44250000e+09,   4.44300000e+09,
         4.44350000e+09,   4.44400000e+09,   4.44450000e+09,
         4.44500000e+09,   4.44550000e+09,   4.44600000e+09,
         4.44650000e+09,   4.44700000e+09,   4.44750000e+09,
         4.44800000e+09,   4.44850000e+09,   4.44900000e+09,
         4.44950000e+09,   4.45000000e+09,   4.45050000e+09,
         4.45100000e+09,   4.45150000e+09,   4.45200000e+09,
         4.45250000e+09,   4.45300000e+09,   4.45350000e+09,
         4.45400000e+09,   4.45450000e+09,   4.45500000e+09,
         4.45550000e+09,   4.45600000e+09,   4.45650000e+09,
         4.45700000e+09,   4.45750000e+09,   4.45800000e+09,
         4.45850000e+09,   4.45900000e+09,   4.45950000e+09,
         4.46000000e+09,   4.46050000e+09,   4.46100000e+09,
         4.46150000e+09,   4.46200000e+09,   4.46250000e+09,
         4.46300000e+09,   4.46350000e+09,   4.46400000e+09,
         4.46450000e+09,   4.46500000e+09,   4.46550000e+09,
         4.46600000e+09,   4.46650000e+09,   4.46700000e+09,
         4.46750000e+09,   4.46800000e+09,   4.46850000e+09,
         4.46900000e+09,   4.46950000e+09,   4.47000000e+09,
         4.47050000e+09,   4.47100000e+09,   4.47150000e+09,
         4.47200000e+09,   4.47250000e+09,   4.47300000e+09,
         4.47350000e+09,   4.47400000e+09,   4.47450000e+09,
         4.47500000e+09,   4.47550000e+09,   4.47600000e+09,
         4.47650000e+09,   4.47700000e+09,   4.47750000e+09,
         4.47800000e+09,   4.47850000e+09,   4.47900000e+09,
         4.47950000e+09,   4.48000000e+09,   4.48050000e+09,
         4.48100000e+09,   4.48150000e+09,   4.48200000e+09,
         4.48250000e+09,   4.48300000e+09,   4.48350000e+09,
         4.48400000e+09,   4.48450000e+09,   4.48500000e+09,
         4.48550000e+09,   4.48600000e+09,   4.48650000e+09,
         4.48700000e+09,   4.48750000e+09,   4.48800000e+09,
         4.48850000e+09,   4.48900000e+09,   4.48950000e+09,
         4.49000000e+09,   4.49050000e+09,   4.49100000e+09,
         4.49150000e+09,   4.49200000e+09,   4.49250000e+09,
         4.49300000e+09,   4.49350000e+09,   4.49400000e+09,
         4.49450000e+09,   4.49500000e+09,   4.49550000e+09,
         4.49600000e+09,   4.49650000e+09,   4.49700000e+09,
         4.49750000e+09,   4.49800000e+09,   4.49850000e+09,
         4.49900000e+09,   4.49950000e+09,   4.50000000e+09,
         4.50050000e+09,   4.50100000e+09,   4.50150000e+09,
         4.50200000e+09,   4.50250000e+09,   4.50300000e+09,
         4.50350000e+09,   4.50400000e+09,   4.50450000e+09,
         4.50500000e+09,   4.50550000e+09,   4.50600000e+09,
         4.50650000e+09,   4.50700000e+09,   4.50750000e+09,
         4.50800000e+09,   4.50850000e+09,   4.50900000e+09,
         4.50950000e+09,   4.51000000e+09,   4.51050000e+09,
         4.51100000e+09,   4.51150000e+09,   4.51200000e+09,
         4.51250000e+09,   4.51300000e+09,   4.51350000e+09,
         4.51400000e+09,   4.51450000e+09,   4.51500000e+09,
         4.51550000e+09,   4.51600000e+09,   4.51650000e+09,
         4.51700000e+09,   4.51750000e+09,   4.51800000e+09,
         4.51850000e+09,   4.51900000e+09,   4.51950000e+09,
         4.52000000e+09,   4.52050000e+09,   4.52100000e+09,
         4.52150000e+09,   4.52200000e+09,   4.52250000e+09,
         4.52300000e+09,   4.52350000e+09,   4.52400000e+09,
         4.52450000e+09,   4.52500000e+09,   4.52550000e+09,
         4.52600000e+09,   4.52650000e+09,   4.52700000e+09,
         4.52750000e+09,   4.52800000e+09,   4.52850000e+09,
         4.52900000e+09,   4.52950000e+09,   4.53000000e+09,
         4.53050000e+09,   4.53100000e+09,   4.53150000e+09,
         4.53200000e+09,   4.53250000e+09,   4.53300000e+09,
         4.53350000e+09,   4.53400000e+09,   4.53450000e+09,
         4.53500000e+09,   4.53550000e+09,   4.53600000e+09,
         4.53650000e+09,   4.53700000e+09,   4.53750000e+09,
         4.53800000e+09,   4.53850000e+09,   4.53900000e+09,
         4.53950000e+09,   4.54000000e+09,   4.54050000e+09,
         4.54100000e+09,   4.54150000e+09,   4.54200000e+09,
         4.54250000e+09,   4.54300000e+09,   4.54350000e+09,
         4.54400000e+09,   4.54450000e+09,   4.54500000e+09,
         4.54550000e+09,   4.54600000e+09,   4.54650000e+09,
         4.54700000e+09,   4.54750000e+09,   4.54800000e+09,
         4.54850000e+09,   4.54900000e+09,   4.54950000e+09,
         4.55000000e+09,   4.55050000e+09,   4.55100000e+09,
         4.55150000e+09,   4.55200000e+09,   4.55250000e+09,
         4.55300000e+09,   4.55350000e+09,   4.55400000e+09,
         4.55450000e+09,   4.55500000e+09,   4.55550000e+09,
         4.55600000e+09,   4.55650000e+09,   4.55700000e+09,
         4.55750000e+09,   4.55800000e+09,   4.55850000e+09,
         4.55900000e+09,   4.55950000e+09,   4.56000000e+09,
         4.56050000e+09,   4.56100000e+09,   4.56150000e+09,
         4.56200000e+09,   4.56250000e+09,   4.56300000e+09,
         4.56350000e+09,   4.56400000e+09,   4.56450000e+09,
         4.56500000e+09,   4.56550000e+09,   4.56600000e+09,
         4.56650000e+09,   4.56700000e+09,   4.56750000e+09,
         4.56800000e+09,   4.56850000e+09,   4.56900000e+09,
         4.56950000e+09,   4.57000000e+09,   4.57050000e+09,
         4.57100000e+09,   4.57150000e+09,   4.57200000e+09,
         4.57250000e+09,   4.57300000e+09,   4.57350000e+09,
         4.57400000e+09,   4.57450000e+09,   4.57500000e+09,
         4.57550000e+09,   4.57600000e+09,   4.57650000e+09,
         4.57700000e+09,   4.57750000e+09,   4.57800000e+09,
         4.57850000e+09,   4.57900000e+09,   4.57950000e+09,
         4.58000000e+09,   4.58050000e+09,   4.58100000e+09,
         4.58150000e+09,   4.58200000e+09,   4.58250000e+09,
         4.58300000e+09,   4.58350000e+09,   4.58400000e+09,
         4.58450000e+09,   4.58500000e+09,   4.58550000e+09,
         4.58600000e+09,   4.58650000e+09,   4.58700000e+09,
         4.58750000e+09,   4.58800000e+09,   4.58850000e+09,
         4.58900000e+09,   4.58950000e+09,   4.59000000e+09,
         4.59050000e+09,   4.59100000e+09,   4.59150000e+09,
         4.59200000e+09,   4.59250000e+09,   4.59300000e+09,
         4.59350000e+09,   4.59400000e+09,   4.59450000e+09,
         4.59500000e+09,   4.59550000e+09,   4.59600000e+09,
         4.59650000e+09,   4.59700000e+09,   4.59750000e+09,
         4.59800000e+09,   4.59850000e+09,   4.59900000e+09,
         4.59950000e+09,   4.60000000e+09])
         
magcom=array([ 0.01309714 -7.25983009e-02j,  0.00214467 -7.35924393e-02j,
       -0.00884314 -7.29510635e-02j, -0.01957097 -7.06637353e-02j,
       -0.02984533 -6.67786971e-02j, -0.03937288 -6.14098050e-02j,
       -0.04794465 -5.46990223e-02j, -0.05543054 -4.67794538e-02j,
       -0.06158651 -3.78972553e-02j, -0.06634876 -2.81649828e-02j,
       -0.06960850 -1.79113690e-02j, -0.07125900 -7.28695095e-03j,
       -0.07132883 +3.46635748e-03j, -0.06979213 +1.40330289e-02j,
       -0.06660236 +2.42808480e-02j, -0.06201488 +3.38746496e-02j,
       -0.05591895 +4.26061749e-02j, -0.04866502 +5.03049716e-02j,
       -0.04039216 +5.67247309e-02j, -0.03119573 +6.17670491e-02j,
       -0.02153448 +6.54213279e-02j, -0.01147578 +6.74449578e-02j,
       -0.00123102 +6.80957660e-02j,  0.00883080 +6.71408698e-02j,
        0.01873062 +6.46533966e-02j,  0.02807371 +6.08489513e-02j,
        0.03656145 +5.55374660e-02j,  0.04429366 +4.90812287e-02j,
        0.05067166 +4.16350141e-02j,  0.05590013 +3.32946517e-02j,
        0.05985526 +2.44561471e-02j,  0.06220444 +1.52224591e-02j,
        0.06341150 +5.60834166e-03j,  0.06303599 -3.68027459e-03j,
        0.06125092 -1.30049223e-02j,  0.05823918 -2.17804238e-02j,
        0.05387422 -2.98309233e-02j,  0.04837506 -3.73578407e-02j,
        0.04209461 -4.36532684e-02j,  0.03463381 -4.89519909e-02j,
        0.02677810 -5.31037264e-02j,  0.01849409 -5.57449237e-02j,
        0.00988330 -5.73024862e-02j,  0.00162729 -5.75878546e-02j,
       -0.00673139 -5.64694069e-02j, -0.01489321 -5.47892191e-02j,
       -0.02239143 -5.14292493e-02j, -0.02973027 -4.72039916e-02j,
       -0.03600421 -4.18940261e-02j, -0.04125553 -3.54726575e-02j,
       -0.04566273 -2.87462045e-02j, -0.04838835 -2.15428937e-02j,
       -0.05050652 -1.40156411e-02j, -0.05127267 -6.74679317e-03j,
       -0.05100080 +7.21427903e-04j, -0.05004366 +7.81230256e-03j,
       -0.04782872 +1.44322421e-02j, -0.04496558 +2.11320613e-02j,
       -0.04143148 +2.69796941e-02j, -0.03675881 +3.25826295e-02j,
       -0.03134645 +3.76093350e-02j, -0.02509400 +4.12303247e-02j,
       -0.01813773 +4.40632217e-02j, -0.01150670 +4.52245921e-02j,
       -0.00486347 +4.54454981e-02j,  0.00135475 +4.49497625e-02j,
        0.00704859 +4.38807607e-02j,  0.01304038 +4.20387499e-02j,
        0.01844233 +3.99449468e-02j,  0.02370257 +3.64449807e-02j,
        0.02853675 +3.26519608e-02j,  0.03259113 +2.81562619e-02j,
        0.03601548 +2.30043810e-02j,  0.03885379 +1.74828134e-02j,
        0.04038731 +1.14398459e-02j,  0.04132546 +5.06718131e-03j,
        0.04059190 -6.49818801e-04j,  0.03913774 -6.29224861e-03j,
        0.03744442 -1.08876256e-02j,  0.03530572 -1.51667017e-02j,
        0.03319241 -1.96716115e-02j,  0.03061561 -2.39136778e-02j,
        0.02662949 -2.82180086e-02j,  0.02241191 -3.20064910e-02j,
        0.01697899 -3.43019813e-02j,  0.01180687 -3.61666232e-02j,
        0.00671332 -3.66578847e-02j,  0.00145747 -3.68665755e-02j,
       -0.00340414 -3.66957113e-02j, -0.00831518 -3.52274291e-02j,
       -0.01326862 -3.34996805e-02j, -0.01701491 -3.10068112e-02j,
       -0.02096076 -2.81094126e-02j, -0.02410381 -2.55043600e-02j,
       -0.02744336 -2.19564270e-02j, -0.03060599 -1.79635994e-02j,
       -0.03306713 -1.32106505e-02j, -0.03397644 -7.50855776e-03j,
       -0.03423032 -2.81439535e-03j, -0.03286706 +1.83051545e-03j,
       -0.03231183 +5.55065135e-03j, -0.03133084 +9.17173084e-03j,
       -0.03011259 +1.31637799e-02j, -0.02859299 +1.75739639e-02j,
       -0.02560112 +2.13437658e-02j, -0.02213598 +2.52335370e-02j,
       -0.01820417 +2.73762252e-02j, -0.01400993 +2.96309814e-02j,
       -0.00975309 +3.11667100e-02j, -0.00545525 +3.19191217e-02j,
       -0.00020924 +3.20695303e-02j,  0.00364406 +3.10829990e-02j,
        0.00786871 +2.93843709e-02j,  0.01057477 +2.80133300e-02j,
        0.01317135 +2.67208405e-02j,  0.01684180 +2.55282037e-02j,
        0.02056535 +2.43945345e-02j,  0.02485984 +2.08897926e-02j,
        0.02843510 +1.67229958e-02j,  0.02998894 +1.14806537e-02j,
        0.03050834 +6.31059986e-03j,  0.03021817 +2.93402839e-03j,
        0.02933108 -1.18193252e-03j,  0.02949874 -4.25069407e-03j,
        0.02827954 -7.97742791e-03j,  0.02707983 -1.16359964e-02j,
        0.02566787 -1.46845849e-02j,  0.02311782 -1.72385592e-02j,
        0.02221385 -2.08581742e-02j,  0.01956541 -2.35004500e-02j,
        0.01647067 -2.77296733e-02j,  0.01178519 -3.06563172e-02j,
        0.00602774 -3.17785963e-02j,  0.00032646 -3.18410918e-02j,
       -0.00335016 -2.95385625e-02j, -0.00705880 -2.82570925e-02j,
       -0.00893964 -2.71679983e-02j, -0.01203698 -2.61593368e-02j,
       -0.01582391 -2.54914723e-02j, -0.01884414 -2.36804206e-02j,
       -0.02287452 -2.03635432e-02j, -0.02527495 -1.79442950e-02j,
       -0.02748340 -1.41740562e-02j, -0.03014494 -1.04918890e-02j,
       -0.03175337 -6.62368257e-03j, -0.03279891 -4.48246283e-04j,
       -0.03249090 +4.18452360e-03j, -0.03007408 +9.21929441e-03j,
       -0.02797620 +1.26836076e-02j, -0.02606385 +1.47277592e-02j,
       -0.02411206 +1.78623442e-02j, -0.02348288 +2.09291931e-02j,
       -0.02052310 +2.43792068e-02j, -0.01714140 +2.85337139e-02j,
       -0.01268510 +3.06395479e-02j, -0.00766476 +3.18369791e-02j,
       -0.00370995 +3.29575092e-02j,  0.00046389 +3.25762480e-02j,
        0.00547216 +3.36766243e-02j,  0.01000990 +3.26873660e-02j,
        0.01564411 +3.06922160e-02j,  0.01997152 +2.77932007e-02j,
        0.02249692 +2.40280274e-02j,  0.02559732 +2.08923873e-02j,
        0.02727045 +1.86327454e-02j,  0.03029826 +1.49612864e-02j,
        0.03348878 +1.12797413e-02j,  0.03512907 +6.08600583e-03j,
        0.03596387 -1.42770905e-05j,  0.03520337 -4.66789212e-03j,
        0.03337096 -9.51860752e-03j,  0.03298876 -1.34525523e-02j,
        0.03116346 -1.74126681e-02j,  0.02910210 -2.29599793e-02j,
        0.02608110 -2.74583083e-02j,  0.02082264 -3.12273744e-02j,
        0.01608664 -3.40705216e-02j,  0.01121082 -3.50185893e-02j,
        0.00639830 -3.65908630e-02j,  0.00218121 -3.77828218e-02j,
       -0.00370164 -3.80271636e-02j, -0.00959242 -3.80563475e-02j,
       -0.01504087 -3.55561748e-02j, -0.02005914 -3.27209681e-02j,
       -0.02344745 -3.01039051e-02j, -0.02687327 -2.68437564e-02j,
       -0.03142038 -2.43360307e-02j, -0.03517528 -2.04033665e-02j,
       -0.03944245 -1.45810228e-02j, -0.04175877 -8.07994232e-03j,
       -0.04212389 -9.92606045e-04j, -0.04163247 +5.43063181e-03j,
       -0.03972014 +1.05642453e-02j, -0.03804587 +1.63733754e-02j,
       -0.03593243 +2.09626444e-02j, -0.03253259 +2.61700992e-02j,
       -0.02884313 +3.08164191e-02j, -0.02450656 +3.39521095e-02j,
       -0.01969593 +3.73502746e-02j, -0.01571023 +4.02457491e-02j,
       -0.01021006 +4.28415909e-02j, -0.00374700 +4.59954143e-02j,
        0.00391721 +4.69989590e-02j,  0.01254387 +4.60758321e-02j,
        0.01986432 +4.30298075e-02j,  0.02589351 +3.81783508e-02j,
        0.03049948 +3.39503549e-02j,  0.03382970 +2.93303709e-02j,
        0.03772348 +2.47198585e-02j,  0.04108457 +2.02146824e-02j,
        0.04368341 +1.43735381e-02j,  0.04634018 +8.46154150e-03j,
        0.04751442 +2.23340746e-03j,  0.04844208 -4.78541851e-03j,
        0.04868498 -1.19361226e-02j,  0.04709913 -1.99378338e-02j,
        0.04410319 -2.82441061e-02j,  0.03864067 -3.53513584e-02j,
        0.03175842 -4.10715155e-02j,  0.02482011 -4.43737321e-02j,
        0.01784660 -4.64944653e-02j,  0.01198561 -4.81556505e-02j,
        0.00601240 -4.95120697e-02j, -0.00070756 -5.07638641e-02j,
       -0.00788374 -5.14241047e-02j, -0.01562864 -5.05242795e-02j,
       -0.02351953 -4.85669486e-02j, -0.03104259 -4.51054163e-02j,
       -0.03818607 -4.03003544e-02j, -0.04469729 -3.41992900e-02j,
       -0.04975212 -2.67542154e-02j, -0.05356960 -1.84169803e-02j,
       -0.05526079 -9.79939755e-03j, -0.05570308 -1.59271120e-03j,
       -0.05496214 +6.23034453e-03j, -0.05368211 +1.33650396e-02j,
       -0.05195254 +2.08857674e-02j, -0.04937607 +2.82749161e-02j,
       -0.04548549 +3.59521285e-02j, -0.04002495 +4.32212800e-02j,
       -0.03321756 +4.93702963e-02j, -0.02531067 +5.44154532e-02j,
       -0.01687065 +5.79179786e-02j, -0.00779760 +6.01786189e-02j,
        0.00148529 +6.09500259e-02j,  0.01075652 +6.01812340e-02j,
        0.01983300 +5.79550304e-02j,  0.02817509 +5.44078313e-02j,
        0.03602432 +4.97131199e-02j,  0.04294222 +4.42236364e-02j,
        0.04930934 +3.76961157e-02j,  0.05480677 +3.03273462e-02j,
        0.05935302 +2.19819564e-02j,  0.06251834 +1.26894433e-02j,
        0.06413404 +3.06246523e-03j,  0.06412181 -6.89862343e-03j,
        0.06262177 -1.64163951e-02j,  0.05976276 -2.58794166e-02j,
        0.05553688 -3.47555541e-02j,  0.04988817 -4.30829674e-02j,
        0.04287266 -5.04292659e-02j,  0.03487583 -5.66204377e-02j,
        0.02585375 -6.14060611e-02j,  0.01631540 -6.48475513e-02j,
        0.00634564 -6.66839853e-02j, -0.00376875 -6.71189278e-02j,
       -0.01385590 -6.60569742e-02j, -0.02377573 -6.34606555e-02j,
       -0.03328759 -5.94645552e-02j, -0.04206292 -5.38930781e-02j,
       -0.05003675 -4.71142866e-02j, -0.05681917 -3.91325168e-02j,
       -0.06242606 -3.01172882e-02j, -0.06658573 -2.02667955e-02j,
       -0.06909256 -9.81574133e-03j, -0.06996160 +9.43798514e-04j,
       -0.06908880 +1.16864694e-02j, -0.06654167 +2.21544188e-02j,
       -0.06243955 +3.20764035e-02j, -0.05686067 +4.12012488e-02j,
       -0.05003608 +4.94089872e-02j, -0.04204834 +5.64971119e-02j,
       -0.03302223 +6.23736382e-02j, -0.02319994 +6.67935386e-02j,
       -0.01275950 +6.96555153e-02j, -0.00198948 +7.09036067e-02j,
        0.00886317 +7.05028102e-02j,  0.01958703 +6.84066713e-02j,
        0.02987533 +6.46577552e-02j,  0.03945434 +5.93247972e-02j,
        0.04808791 +5.25668375e-02j,  0.05552288 +4.45787124e-02j,
        0.06165364 +3.55260521e-02j,  0.06627816 +2.56676413e-02j,
        0.06930850 +1.52767962e-02j,  0.07074897 +4.55292780e-03j,
        0.07055791 -6.22201897e-03j,  0.06871156 -1.68521162e-02j,
        0.06526345 -2.70544328e-02j,  0.06034621 -3.65870707e-02j,
        0.05402511 -4.52440269e-02j,  0.04649856 -5.28565943e-02j,
        0.03789992 -5.92028387e-02j,  0.02844442 -6.42016381e-02j,
        0.01834171 -6.76636398e-02j,  0.00785183 -6.95335269e-02j,
       -0.00281029 -6.97859228e-02j, -0.01329574 -6.83709458e-02j,
       -0.02346769 -6.54016063e-02j, -0.03296352 -6.09345548e-02j,
       -0.04166581 -5.50641268e-02j, -0.04933497 -4.79894765e-02j,
       -0.05575019 -3.99225689e-02j, -0.06090994 -3.09838615e-02j,
       -0.06461985 -2.15343162e-02j, -0.06693868 -1.15829622e-02j,
       -0.06775489 -1.51536055e-03j, -0.06710797 +8.58255755e-03j,
       -0.06491681 +1.85333099e-02j, -0.06133897 +2.79594772e-02j,
       -0.05625004 +3.67939360e-02j, -0.04999415 +4.47022766e-02j,
       -0.04254580 +5.15060723e-02j, -0.03420674 +5.70873581e-02j,
       -0.02526263 +6.13011420e-02j, -0.01576243 +6.40745461e-02j,
       -0.00613410 +6.54872730e-02j,  0.00357676 +6.53650537e-02j,
        0.01310092 +6.39604256e-02j,  0.02224441 +6.12437688e-02j,
        0.03096785 +5.71415350e-02j,  0.03903737 +5.19644544e-02j,
        0.04618774 +4.55050580e-02j,  0.05239196 +3.80626358e-02j,
        0.05736000 +2.98285279e-02j,  0.06090262 +2.08162442e-02j,
        0.06319429 +1.15691228e-02j,  0.06383526 +2.12044735e-03j,
        0.06330083 -7.28952838e-03j,  0.06132898 -1.63101330e-02j,
        0.05812672 -2.50003785e-02j,  0.05386770 -3.31924520e-02j,
        0.04839729 -4.05212194e-02j,  0.04186695 -4.73139398e-02j,
        0.03452233 -5.28395995e-02j,  0.02622754 -5.73352911e-02j,
        0.01742724 -6.05118759e-02j,  0.00833745 -6.22109026e-02j,
       -0.00104805 -6.26084208e-02j, -0.01001559 -6.15655780e-02j,
       -0.01889021 -5.92112355e-02j, -0.02714245 -5.57817034e-02j,
       -0.03479766 -5.12621962e-02j, -0.04192692 -4.56324965e-02j,
       -0.04811668 -3.92293632e-02j, -0.05342492 -3.16701829e-02j,
       -0.05762753 -2.35060528e-02j, -0.06041434 -1.46904876e-02j,
       -0.06181289 -5.45009552e-03j, -0.06183335 +3.63303605e-03j,
       -0.06030758 +1.26842894e-02j, -0.05774951 +2.12466549e-02j,
       -0.05388926 +2.91643571e-02j, -0.04902471 +3.66222598e-02j,
       -0.04339375 +4.32207286e-02j, -0.03671086 +4.90394458e-02j,
       -0.02935820 +5.40430509e-02j, -0.02123306 +5.78477457e-02j,
       -0.01236970 +6.05548322e-02j, -0.00334989 +6.18746392e-02j,
        0.00599696 +6.15645088e-02j,  0.01514218 +5.99251315e-02j,
        0.02364581 +5.68131432e-02j,  0.03162466 +5.25097214e-02j,
        0.03867925 +4.73829247e-02j,  0.04495793 +4.12229449e-02j,
        0.05048862 +3.44847813e-02j,  0.05497843 +2.69703846e-02j,
        0.05848108 +1.86804738e-02j,  0.06080648 +1.00571690e-02j,
        0.06164647 +9.81721445e-04j,  0.06138119 -8.19556974e-03j,
        0.05947321 -1.71188321e-02j,  0.05629071 -2.58439258e-02j,
        0.05185487 -3.38496789e-02j,  0.04617979 -4.10149023e-02j,
        0.03966141 -4.73465137e-02j,  0.03232778 -5.23992404e-02j,
        0.02432178 -5.65888733e-02j,  0.01600887 -5.94454147e-02j,
        0.00726125 -6.12251833e-02j, -0.00173235 -6.18029833e-02j,
       -0.01068453 -6.09918535e-02j, -0.01963412 -5.88443503e-02j,
       -0.02802161 -5.54802269e-02j, -0.03592434 -5.08060120e-02j,
       -0.04307813 -4.50513773e-02j, -0.04928741 -3.82621437e-02j,
       -0.05445536 -3.05781178e-02j, -0.05837109 -2.22830139e-02j,
       -0.06098697 -1.34227378e-02j])#, dtype=complex64)





    
plt.plot(freq, dB(magcom))
plt.plot(frq, 10*log10(absolute(R(frq)))-23)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Reflection (dB)")
plt.title("S33 vs frequency")
plt.show()
EJmax=0.2*k
EC=0.04*k
f0=4.5e9
hf0=h*f0

S11_0 = 0.5094
S21_0 = 0.28# 0.26181; %0.270
S22_0 = 0.546 #0.55;
theta_L =0* 0.613349 #0.64; %-2.55068; %-0.59;

Gamma_ac = 500.0e6*2*pi# 38e6*2*pi;
Gamma_Phi = 0*2*pi
xi = 0*0.003 # Resub chg from 0.003
Gamma_tot = (1+xi)*Gamma_ac
Gamma_el = xi*Gamma_tot
Gamma_tot = Gamma_ac + Gamma_el
gamma_10 = Gamma_tot/2 + Gamma_Phi

# Omega_10 in regular frequency units
def flux_parabola(flux_over_flux0):
    EJ = EJmax*absolute(cos(pi*flux_over_flux0))
    E0 =  sqrt(8.0*EJ*EC)*0.5 - EC/4
    E1 =  sqrt(8.0*EJ*EC)*1.5 - (EC/12.0)*(6+6+3)
    return (E1-E0)/h;


# Per's definition: The detuning is positive for higher qubit frequency.
def detuning(flux_over_flux0):
    return 2.0*pi*(f0 - flux_parabola(flux_over_flux0))

# Qubit reflection, for an incoming N_in phonons per second *at the qubit*
# This is Per's expression, but adjusted for Anton's definition of detuning.
def  r_qubit(d_omega, P_in):
    N_in=P_in/hf0
    G = Gamma_tot
    g = gamma_10
    #S21 = S21_0
    #S22 = S22_0
    #tL = theta_L 
    P22=[]
    for N_idx, N in enumerate(N_in):
        P22.append(-(G/(2.0*g))*(1.0+1j*d_omega/g)/(1.0 + d_omega**2/g**2 + 2.0*N/g))
    return squeeze(array(P22))

def S11_IDT_no_IDT_ref(r_qubit):
    # Per's Eq. 12
    return S21_0**2/(exp(-2j*theta_L)/r_qubit - S22_0)

#zcs_S11_minus_detuned_tot_calc = C.S11_IDT_no_IDT_ref(zcs_S11_qubit_calc, C);
import matplotlib.pyplot as plt

print 1.0e-3*10**(-170.0/10.0)

x=linspace(0, 2, 201)
print shape(x)
#plt.plot(x, absolute(S11_IDT_no_IDT_ref(r_qubit(detuning(x), array([-1e-20]))) ))
#plt.show()
          

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0914/TA_A58_scb_refl_powsat_1.hdf5"

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0912/TA_A58_scb_trans_powfluxswp_higherbw.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0913/TA_A58_scb_refl_powfluxswp_higherbw_revV.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp_higherpower.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0911/TA_A58_scb_refl_powfluxswp_higherbw.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0915/TA_A58_scb_refl_powfluxswp_lowpow.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0916/TA_A58_scb_refl_powfluxswp_maxpow2.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0917/TA_A58_scb_refl_gateswp_n5dBm.hdf5"

powind=30
frqind=234
#from HDF5_functions import read_hdf5

#print read_hdf5(file_path)
print "start data read"
with File(file_path, 'r') as f:
    Magvec=f["Traces"]["Agilent VNA - S21"]#[:]
    data=f["Data"]["Data"]
    f0=f["Traces"]['Agilent VNA - S21_t0dt'][0][0]
    fstep=f["Traces"]['Agilent VNA - S21_t0dt'][0][1]
    print fstep
    print shape(Magvec)
    print shape(data)
    sm=shape(Magvec)[0]
    sy=shape(data)
    s=(sm, sy[0], sy[2]) 
    print s
    Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
    Magcom=reshape(Magcom, s, order="F")

    pwr=data[:, 0, 0]
    yoko= data[0, 1, :]
    freq=linspace(f0, f0+fstep*(sm-1), sm)
    print freq
    print yoko
    print pwr
print "end data read"




#plt.plot(dB(Magcom[:, :, 0]))
#Magcom=Magcom[:,:, powind]-mean(Magcom[:, :, powind ], axis=1, keepdims=True)

#diffS11=(amax(Magcom[4, powind, :]))
#diffS11=[]
#for n, a in enumerate(pwr):
#    MagcomdB=Magcom[:,:,n]-mean(Magcom[:,  82:83, n ], axis=1, keepdims=True)
#    MagcomdB=absolute(MagcomdB)
#    #diffS11.append(MagcomdB[942, 140]-MagcomdB[942, 85])
#    diffS11.append(mean(MagcomdB[866:1000, 124:155], axis=1)-mean(MagcomdB[866:1000, 73:96], axis=1))

#diffS11=amax(Magcom[frqind, :, 20:], axis=1)-amin(Magcom[frqind, :, 20:], axis=1)
#diffS11=absolute(Magcom[frqind, :, 57]-Magcom[frqind, :, 16])

if 1:
#    with File("testwritetrans.h5", "w") as ff:
#        ff.create_dataset("freq", data=freq)
#        ff.create_dataset("magcom", data=mean(Magcom[:, :, -1], axis=1))
#        
    plt.plot(freq, absolute(mean(Magcom[:, :, -1], axis=1)))
    #plt.plot(frq, absolute(R(frq)))
    plt.show()
    #Magcom=mean(Magcom[:, :, :], axis=0)
    #plt.plot(absolute(transpose(Magcom[:, 2]-Magcom[:,7])),
              #aspect="auto", origin="lower",
               # interpolation="none",
    #            )
    #plt.colorbar()                
    #plt.show()
    #Magy=[]
    #for n,p in enumerate(pwr):
    #    Magy.append(amax(absolute(Magcom[:, n, :]), axis=1)-amin(absolute(Magcom[:, n, :]), axis=1))
    Magy=amax(absolute(Magcom[:, :, :]), axis=2)-amin(absolute(Magcom[:, :, :]), axis=2)
    #plt.plot(Magy)
#    plt.plot(pwr-87, mean(Magy[:, :], axis=0))
    #plt.plot(dB(Magcom[236, powind, :]))#-mean(Magcom[:, :, powind], axis=1, keepdims=True)))
    #plt.show()
    plt.plot(freq, Magy[:, powind])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("max(|S11|)-min(|S11|)")
    plt.title("Cross section maxmin(S11) at -83 dBm")
    #plt.legend(pwr[(0, 5, 20, 30, 40, 45),])
    plt.show()
#MagcomdB=Magcom[890, :, :]    
#MagcomdB=mean(Magcom[985:995,:, :], axis=0)
#MagcomdB=mean(Magcom[120:125,:, :], axis=0)

#MagcomdB=mean(Magcom[944:946,:, :], axis=0)
#MagcomdB=mean(Magcom[419:421,:, :], axis=0)
#M#agcomdB=dB(MagcomdB)
#MagcomdB=absolute(Magcom[:, 50:, powind]-mean(Magcom[:, 50:, powind], axis=1, keepdims=True))
#MagcomdB=absolute(Magcom[220, :, :])#-mean(Magcom[:, powind, 0:1], axis=1, keepdims=True))

if 1:
    plt.plot(pwr-87, absolute(mean(Magcom[frqind, :, 310:330], axis=1)-mean(Magcom[frqind, :, 410:430], axis=1)))
    plt.ylabel("|\Delta S11|")
    plt.xlabel("Power (dBm)")
    plt.title("Power saturation at {} GHz".format(freq[frqind]/1.0e9))
    plt.show()
#print freq[985:995]
#print freq[122:123]



#if 0:
    #plt.plot(MagcomdB[:, powind])
    #plt.plot(MagcomdB[133, :])
    #plt.plot(pwr-20-87, mean(MagcomdB[130:136,:]+20, axis=0)-mean(MagcomdB[230:240,:]+20, axis=0))
    #plt.plot(pwr-87, mean(MagcomdB2[135:145,:], axis=0)-mean(MagcomdB2[230:240,:], axis=0))

if 1:
    plt.imshow( transpose(Magy), #MagcomdB[:, :], 
    #            #vmin=amin(Magy),
    #            #vmax=0.003, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[ amin(freq),amax(freq), 0,91,],            
                 )
    #plt.pcolormesh( enumerate(pwr), freq, Magy, #MagcomdB[:, :], 
                #vmin=amin(Magy),
                #vmax=0.003, #amax(Magvec), 
                #aspect="auto", origin="lower",
                #interpolation="none",
                #extent=[amin(yoko),amax(yoko), amin(freq),amax(freq)],            
    #             )
    plt.ylabel("Power (index)")
    plt.xlabel("Frequency (Hz)")
    plt.title("Max(|S11|)-Min|S11| along flux")
    plt.colorbar()
    plt.show()
    
if 1:
    print freq[frqind]
    plt.imshow( transpose(dB(Magcom[frqind, :, :])), 
    #            #vmin=amin(Magy),
    #            #vmax=0.003, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                #extent=[0,91, ],            
                 )
    #plt.pcolormesh( enumerate(pwr), freq, Magy, #MagcomdB[:, :], 
                #vmin=amin(Magy),
                #vmax=0.003, #amax(Magvec), 
                #aspect="auto", origin="lower",
                #interpolation="none",
                #extent=[amin(yoko),amax(yoko), amin(freq),amax(freq)],            
    #             )
    plt.xlabel("Power (index)")
    plt.ylabel("Flux (index)")
    plt.title("S11 in dB versus pwr and flux at {} GHz".format(freq[frqind]/1.0e9))
    plt.colorbar()
    plt.show()

vmax=0.002    
if 1:
    powind=40
    plt.imshow( absolute(Magcom[:, powind, :]-mean(Magcom[:, powind, 410:430], axis=1, keepdims=True)),
               #absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec),
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
           
    #             )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (bgsub)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()    

if 1:
    powind=30
    plt.imshow( absolute(Magcom[:, powind, :]-mean(Magcom[:, powind, 410:430], axis=1, keepdims=True)),
               #absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (bgsub)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()    


if 1:
    powind=20
    plt.imshow( absolute(Magcom[:, powind, :]-mean(Magcom[:, powind, 410:430], axis=1, keepdims=True)),
               #absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (bgsub)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()    

if 1:
    powind=18
    plt.imshow( absolute(Magcom[:, powind, :]-mean(Magcom[:, powind, 410:430], axis=1, keepdims=True)),
               #absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec),
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (bgsub)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()  

if 1:
    powind=16
    plt.imshow( absolute(Magcom[:, powind, :]-mean(Magcom[:, powind, 410:430], axis=1, keepdims=True)),
               #absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (bgsub)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()  

vmax=0.003    
if 1:
    powind=40
    plt.imshow(absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec),
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
           
    #             )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (diff from min)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()    

if 1:
    powind=30
    plt.imshow( absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (diff from min)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()    


if 1:
    powind=20
    plt.imshow( absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (diff from min)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()    

if 1:
    powind=18
    plt.imshow( absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec),
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (diff from min)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()  

if 1:
    powind=16
    plt.imshow( absolute(Magcom[:, powind, :])-amin(absolute(Magcom[:, powind, :]), axis=1, keepdims=True), 
                vmin=0, #amin(Magy),
                vmax=vmax, #amax(Magvec), 
                aspect="auto", origin="lower",
                interpolation="none",
                extent=[0,len(yoko), amin(freq),amax(freq) ],            
                 )
    plt.ylabel("Frequency (Hz)")
    plt.xlabel("Flux (index)")
    plt.title("|S11| at {} dBm (diff from min)".format(pwr[powind]-87) )
    plt.colorbar()
    plt.show()  


#Magcom=Magcom[frqind, :, :]#-mean(Magcom[frqind, :, :], axis=0, keepdims=True)
#plt.plot(transpose(absolute(Magcom[(0, 5, 10, 15, 25, 30), :])))
#plt.legend([0, 5, 10, 15, 25, 30])
#plt.show()

#MagcomdB=Magcom[:,:,powind]-mean(Magcom[:, 381:382, powind ], axis=1, keepdims=True)
#MagcomdB=absolute(MagcomdB)
#
##MagcomdB=dB(Magcom)
#plt.imshow(  MagcomdB[:, :], 
#            #vmin=amin(Magvec),
#            #vmax=0.001, #amax(Magvec), 
#            aspect="auto", origin="lower",
#            interpolation="none",
#            #extent=[amin(yoko),amax(yoko), amin(freq),amax(freq)],
#            
#             )
#plt.colorbar()
#plt.show()
        
#powind=3
#Magvec=Magdict[pwr[powind]]
#print pwr[powind]
##print shape(Magvec[509, :]), shape(yoko)