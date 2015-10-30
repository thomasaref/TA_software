# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:26:51 2015

@author: thomasaref
"""

from scipy.constants import k,h,pi
from numpy import (squeeze, shape, linspace, log10, mean, amax, amin, absolute, reshape, transpose,
                   real, imag, angle, cos, sqrt, array, exp, delete, float64, sin)
from LOG_functions import log_debug
EJmax=0.8*k
EC=0.04*k
f0=4.517e9
hf0=h*f0
print EJmax/h/1e9
print EC/h/1e9
S11_0 = 0.5094
S21_0 = 0.033828# 0.26181; %0.270
S22_0 = 0.546 #0.55;
theta_L =0* 0.613349 #0.64; %-2.55068; %-0.59;

Gamma_ac = 800.0e6*2*pi# 38e6*2*pi;
Gamma_Phi = 0*2*pi
xi = 0*0.003 # Resub chg from 0.003
Gamma_tot = (1+xi)*Gamma_ac
Gamma_el = xi*Gamma_tot
Gamma_tot = Gamma_ac + Gamma_el
gamma_10 = Gamma_tot/2 + Gamma_Phi

# Omega_10 in regular frequency units
def flux_parabola(flux_over_flux0):
    EJ = EJmax*absolute(cos(pi*flux_over_flux0))
    E0 =  -EJ + sqrt(8.0*EJ*EC)*0.5 - EC/4
    E1 =  -EJ + sqrt(8.0*EJ*EC)*1.5 - (EC/12.0)*(6+6+3)
    return (E1-E0)/h


# Per's definition: The detuning is positive for higher qubit frequency.
def detuning(flux_over_flux0):
    return 2.0*pi*(f0 - flux_parabola(flux_over_flux0))

print 0.45*0.05*5*f0
def lorz(frq):
    return 1.0/(1.0+1j*(frq-f0)/(0.45*0.05*5*f0))

def lorz2(frq):
    return 1.0/(1.0+1j*(frq-f0)/(0.45*0.05*5*frq))

Np=5 
def X(f):
    return pi*Np*(f-f0)/f0

def sinc(f):
     return absolute(sin(X(f))/X(f))   

def X2(f):
    return pi*55*(f-f0)/f0

def sinc2(f):
     return absolute(sin(X2(f))/X2(f))   

def lorz3(frq):
    return 1.0/(1.0+1j*(frq-f0)/(0.45*0.05*5*f0*sinc(frq)))
    
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
x=linspace(0.0001, 10.0e9, 1000)
#plt.plot(x, absolute(lorz(x)))
#plt.plot(x, absolute(lorz2(x)))
#plt.plot(x, absolute(lorz3(x)))

#plt.show()
print 1.0e-3*10**(-170.0/10.0)

xx=linspace(0, 5, 501)
print xx
b=[n for n,g in enumerate(flux_parabola(xx)-4.5e9) if abs(g)<40e6]
c= xx[b[1:]]-xx[b[:-1]]
d=array([g for g in c if g>0.01])
print d[1:]/d[:-1]

print shape(xx)

#plt.plot(xx, flux_parabola(xx))
#plt.plot(xx, detuning((xx+0.5)*0.5)/(2*pi))
#plt.show()
#plt.plot([0,5], [f0, f0])
#print [n for n,g in enumerate(flux_parabola(x)-4.5e9) if abs(g)<100e7]
xxfrq=(xx+0*1.35)*0.27*2

#plt.plot(xx, absolute(S11_IDT_no_IDT_ref(r_qubit(detuning(xxfrq), array([-1e-15]))) ))

refl=array([  1.94833119e-04,   2.64975621e-04,   2.79606844e-04,
         2.52141646e-04,   5.36696403e-04,   6.45913067e-04,
         6.64160005e-04,   7.06420804e-04,   7.64887896e-04,
         7.51023414e-04,   7.35045178e-04,   7.32211571e-04,
         7.33710884e-04,   7.13567599e-04,   7.00752542e-04,
         6.59192970e-04,   6.89634006e-04,   6.46120403e-04,
         7.14129477e-04,   6.95066119e-04,   6.81444304e-04,
         6.65642205e-04,   6.06941991e-04,   5.99592226e-04,
         5.60607819e-04,   6.36572659e-04,   6.05928304e-04,
         5.68012416e-04,   5.77232859e-04,   5.26203017e-04,
         5.39481640e-04,   5.14173764e-04,   5.04755182e-04,
         5.00184484e-04,   4.97297267e-04,   4.74345725e-04,
         4.76797461e-04,   4.63639648e-04,   4.66135476e-04,
         3.21296859e-04,   2.95166537e-04,   1.17796728e-04,
         8.51672812e-05,   1.44477075e-04,   9.54153948e-05,
         2.27648939e-04,   3.26353969e-04,   1.59296818e-04,
         1.75509864e-04,   1.07591564e-04,   1.55936825e-04,
         3.36020661e-04,   1.05760701e-04,   1.85207682e-04,
         1.61468372e-04,   1.99266899e-04,   2.33424507e-04,
         8.13340812e-05,   1.49774074e-04,   1.81383002e-04,
         2.80560576e-04,   3.53302341e-04,   1.73475739e-04,
         2.57434440e-04,   2.59447785e-04,   3.61844985e-04,
         5.00800612e-04,   2.01192684e-04,   2.67977215e-04,
         3.57483746e-04,   3.95151495e-04,   3.67432018e-04,
         1.93251442e-04,   3.51655675e-04,   4.22893558e-04,
         4.43519704e-04,   5.16220171e-04,   2.74070451e-04,
         3.38050275e-04,   4.22611338e-04,   5.15002292e-04,
         5.19750814e-04,   6.28205424e-04,   3.43753520e-04,
         3.34651966e-04,   4.85223369e-04,   4.95551154e-04,
         5.10228449e-04,   5.03511576e-04,   4.90384235e-04,
         5.57707390e-04,   5.79977233e-04,   5.92633733e-04,
         6.56378921e-04,   4.29599313e-04,   5.58244763e-04,
         5.47810458e-04,   6.41451858e-04,   7.00844976e-04,
         4.28447383e-04,   5.99205319e-04,   6.39105448e-04,
         7.49796280e-04,   6.46891072e-04,   5.92866563e-04,
         7.00166449e-04,   6.70337060e-04,   4.02106118e-04,
         6.61041762e-04,   7.04632723e-04,   7.40210176e-04,
         7.93093350e-04,   8.22698756e-04,   6.42746279e-04,
         7.29498919e-04,   8.36561201e-04,   5.92338271e-04,
         7.05515209e-04,   8.23355454e-04,   7.69203296e-04,
         7.40153715e-04,   8.00947368e-04,   6.06565562e-04,
         7.75598455e-04,   8.20108864e-04,   8.67356430e-04,
         8.76372447e-04,   6.50996808e-04,   8.64858448e-04,
         9.26422479e-04,   6.64734864e-04,   8.38111329e-04,
         8.18707573e-04,   8.45921226e-04,   8.27429642e-04,
         8.88234063e-04,   9.17023164e-04,   6.58778998e-04,
         8.44030350e-04,   9.64872888e-04,   9.24851454e-04,
         1.03545131e-03,   7.49457278e-04,   8.71597382e-04,
         9.90075758e-04,   8.02147086e-04,   8.24082992e-04,
         8.21977970e-04,   9.09955997e-04,   1.03566854e-03,
         7.99072499e-04,   9.14685719e-04,   9.35189368e-04,
         8.46317154e-04,   8.64399248e-04,   8.01733288e-04,
         5.28749719e-04,   5.74087258e-04,   6.45838270e-04,
         7.83480355e-04,   8.62002198e-04,   7.92587409e-04,
         8.01011687e-04,   6.65497733e-04,   7.26349477e-04,
         7.85305281e-04,   7.12317764e-04,   7.55961635e-04,
         5.95338177e-04,   7.48947030e-04,   7.39830022e-04,
         7.97955727e-04,   7.67879537e-04,   7.84902659e-04,
         8.72738718e-04,   8.24560644e-04,   8.28467833e-04,
         6.44864165e-04,   6.79738587e-04,   7.30256375e-04,
         7.83016963e-04,   8.06072669e-04,   7.34404777e-04,
         9.96400486e-04,   9.73222835e-04,   9.02428059e-04,
         9.33317759e-04,   8.54310871e-04,   7.60744675e-04,
         4.75848530e-04,   5.96894883e-04,   5.83723944e-04,
         6.47396431e-04,   6.01034903e-04,   6.56814256e-04,
         5.00843627e-04,   5.81172470e-04,   4.52437205e-04,
         5.27205702e-04,   5.55304810e-04,   6.52541115e-04,
         6.91151945e-04,   4.69982624e-04,   5.83081972e-04,
         5.09025820e-04,   5.84901718e-04,   3.23911256e-04,
         4.21468198e-04,   4.18075797e-04,   5.21783775e-04,
         5.57725143e-04,   4.24407277e-04,   4.52130073e-04,
         2.99626001e-04,   5.58223110e-04,   4.59378847e-04,
         4.89373808e-04,   4.69745020e-04,   2.90129276e-04,
         3.44979344e-04,   4.66434838e-04,   5.13119856e-04,
         3.28647962e-04,   4.41522541e-04,   4.43127356e-04,
         6.27255009e-04,   5.94377867e-04,   4.67952981e-04,
         2.18951187e-04,   2.59212829e-04,   3.69872316e-04,
         4.39642783e-04,   3.56498378e-04,   1.69187042e-04,
         1.98358204e-04,   2.60081695e-04,   3.83111270e-04,
         4.69233579e-04,   4.03458776e-04,   3.38532380e-04,
         3.50547198e-04,   4.73960128e-04,   2.74650025e-04,
         3.50359885e-04,   4.11111832e-04,   3.90605594e-04,
         4.71898646e-04,   5.51283534e-04,   5.04595693e-04,
         5.02915296e-04,   3.91515234e-04,   4.24063241e-04,
         5.03809249e-04,   5.30155608e-04,   5.13517705e-04,
         6.32303476e-04,   2.99463631e-04,   4.35107388e-04,
         4.46677965e-04,   5.33056038e-04,   7.49778526e-04,
         6.90834771e-04,   7.65762292e-04,   8.38294567e-04,
         7.92497827e-04,   7.55189802e-04,   5.05303498e-04,
         4.78966336e-04,   4.98926034e-04,   5.71643468e-04,
         6.24512846e-04,   5.11196500e-04,   4.27145656e-04,
         4.88893420e-04,   5.43382426e-04,   6.14654273e-04,
         6.14620105e-04,   3.67141241e-04,   6.13220152e-04,
         6.34913740e-04,   6.48446381e-04,   5.43483300e-04,
         6.05478941e-04,   7.45575177e-04,   7.11789413e-04,
         6.96817937e-04,   3.60944192e-04,   4.95519198e-04,
         5.94801095e-04,   5.35767293e-04,   6.36560319e-04,
         6.11144642e-04,   7.83255673e-04,   1.00351113e-03,
         9.12560034e-04,   6.13098033e-04,   6.93765760e-04,
         7.33241555e-04,   7.62450800e-04,   7.63065007e-04,
         7.71416933e-04,   4.82255477e-04,   7.30144675e-04,
         8.20630346e-04,   9.49360081e-04,   6.91354799e-04,
         7.95212458e-04,   8.51190300e-04,   8.41343019e-04,
         8.83663772e-04,   6.29954273e-04,   7.24317040e-04,
         8.62890214e-04,   8.96814920e-04,   9.48658155e-04,
         7.38003466e-04,   7.19890231e-04,   8.21487221e-04,
         8.35985760e-04,   7.75166962e-04,   6.99661381e-04,
         6.60624297e-04,   8.68227275e-04,   8.51078366e-04,
         7.97726796e-04,   8.25463852e-04,   8.00020993e-04,
         4.94860869e-04,   6.03424793e-04,   6.63961458e-04,
         6.46243687e-04,   7.12349429e-04,   7.19461823e-04,
         8.12116079e-04,   7.72363972e-04,   6.46587403e-04,
         6.93424081e-04,   5.94420300e-04,   6.82264159e-04,
         8.09713034e-04,   4.58359602e-04,   5.43222297e-04,
         6.55336422e-04,   7.27766368e-04,   8.45232164e-04,
         1.10241689e-03,   1.10212807e-03,   9.95020149e-04,
         5.11171238e-04,   9.01176129e-04,   6.44643733e-04,
         6.81231031e-04,   6.56027754e-04,   7.02650170e-04,
         7.41673866e-04,   6.14676799e-04,   6.97077834e-04,
         6.98645075e-04,   5.82736800e-04,   6.64136373e-04,
         5.50927361e-04,   8.95496167e-04,   9.06024070e-04,
         7.03316124e-04,   4.26323706e-04,   5.09393751e-04,
         5.34786959e-04,   6.17392245e-04,   5.42221882e-04,
         5.28873119e-04,   6.18532416e-04,   3.61719227e-04,
         5.16575121e-04,   6.24162785e-04,   5.11291320e-04,
         6.45733729e-04,   7.05693790e-04,   7.15849164e-04,
         5.71891665e-04,   5.82963519e-04,   7.06652994e-04,
         4.21234639e-04,   5.25982701e-04,   5.17546781e-04,
         4.94102249e-04,   4.42528370e-04,   1.80817413e-04,
         3.52996954e-04,   2.38088178e-04,   4.10837383e-04,
         4.67214966e-04,   5.97144826e-04,   2.19821173e-04,
         3.23869463e-04,   2.59622058e-04,   2.37220287e-04,
         2.57919426e-04,   1.44847363e-04,   5.98394727e-05,
         2.49930890e-04,   1.93068598e-04,   3.01663502e-04,
         2.42711845e-04,   2.21423878e-04,   1.85386889e-04,
         1.23045771e-04,   1.44278602e-04,   1.62890778e-04,
         2.54318991e-04,   2.20129994e-04,   2.94577221e-05,
         1.13039197e-04,   1.68196973e-04,   1.42674471e-04,
         1.76852744e-04,   1.50925815e-04,   1.32892106e-04,
         5.44706527e-05,   9.45448191e-05,   5.76487582e-05,
         1.97813191e-04,   5.09075180e-05,   2.18201050e-04,
         1.93456126e-05,   5.59131695e-05,   2.65827530e-05,
         3.13958066e-04,   2.09500067e-04,   4.48477134e-04,
         3.63132749e-05,   1.18717981e-04,   1.22690064e-04,
         1.33685680e-04,   1.35256414e-04,   1.40287637e-04,
         2.03282005e-04,   9.17279831e-05,   1.20235622e-04,
         1.87252081e-04,   1.57011469e-04,   2.21350914e-04,
         1.14017545e-04,   2.12239785e-04,   1.97756613e-04,
         2.20834670e-04,   1.61413482e-04,   2.48228578e-04,
         2.92985613e-04,   2.76565610e-04,   3.17110418e-04,
         1.57801551e-04,   2.66275601e-04,   2.66949297e-04,
         3.11077572e-04,   2.97576480e-04,   3.34340526e-04,
         1.37268536e-04,   2.54753773e-04,   2.78431951e-04,
         2.78158434e-04,   3.11481563e-04,   3.71623901e-04,
         2.17332563e-04,   3.25588015e-04,   4.40290751e-04,
         4.18589421e-04,   1.52323992e-04,   3.34984477e-04,
         4.80322691e-04,   4.78899834e-04,   5.45292336e-04,
         6.62936771e-04,   7.02432706e-04,   2.83192145e-04,
         4.53733723e-04,   5.47689269e-04,   5.78830310e-04,
         5.15143271e-04,   2.20448186e-04,   3.92406160e-04,
         5.58487664e-04,   5.43127593e-04,   5.33943239e-04,
         6.02466404e-04,   5.09120466e-04,   5.19344583e-04,
         2.76576204e-04,   4.50583961e-04,   1.49797066e-04,
         4.46230028e-04,   5.59046573e-04,   5.35067578e-04,
         3.56542092e-04,   4.23391466e-04,   5.44444891e-04,
         5.00041700e-04,   6.45613181e-04,   5.34115417e-04,
         4.69197577e-04,   2.99452251e-04,   3.55226890e-04])
plt.plot(xx, refl/amax(refl))
#plt.plot(xx, absolute(cos(pi*(xx+1.35)*0.27)))
plt.plot(xx, absolute(cos(pi*(xx-0.5)*0.54)))

plt.xlabel("Flux (V)")
plt.ylabel("S11 qubit")
plt.title("very rough S11 qubit fit try at -93 dBm and 4.517 GHz")
plt.show()

plt.plot(absolute(cos(pi*(xx+1.35)*0.27)), refl/amax(refl))
plt.show()
plt.plot(absolute(cos(pi*(xx-0.5)*0.54)), refl/amax(refl))

plt.show()
#plt.plot(xx, detuning((xx+0.5)*0.5)/(2*pi))

#plt.show()
          
from h5py import File
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0914/TA_A58_scb_refl_powsat_1.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0912/TA_A58_scb_trans_powfluxswp_higherbw.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0913/TA_A58_scb_refl_powfluxswp_higherbw_revV.hdf5"

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp_higherpower.hdf5"
file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0911/TA_A58_scb_refl_powfluxswp_higherbw.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0915/TA_A58_scb_refl_powfluxswp_lowpow.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0916/TA_A58_scb_refl_powfluxswp_maxpow2.hdf5"

powind=4
frqind=6708
#from HDF5_functions import read_hdf5
#print read_hdf5(file_path)
print "start data read"
with File(file_path, 'r') as f:
    Magvec=f["Traces"]["Agilent VNA - S21"]#[:]
    data=f["Data"]["Data"]
    fstart=f["Traces"]['Agilent VNA - S21_t0dt'][0][0]
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
    #Magcom=delete(Magcom, 73, axis=1)
    pwr=data[:, 0, 0].astype(float64)
    #pwr=delete(pwr, 73)
    yoko= data[0, 1, :].astype(float64)
    freq=linspace(fstart, fstart+fstep*(sm-1), sm)
    
    print Magcom.dtype, pwr.dtype, yoko.dtype, freq.dtype
print shape(Magcom)
print freq[frqind]
print yoko[powind]
print "end data read"
print pwr[410:430]

def dB(x):
    return 20*log10(absolute(x))

plt.pcolormesh(absolute(Magcom[:, :, powind]-mean(Magcom[:, :, powind], axis=1, keepdims=True)))
plt.show()
plt.plot( pwr, absolute(mean(Magcom[6700:6715, :, powind], axis=0)))

#plt.plot(absolute(cos(pi*(xx+1.35)*0.27)), absolute(mean(Magcom[930:950, :, powind], axis=0)))
plt.show()
plt.plot(absolute(cos(pi*(xx-0.5)*0.54)), absolute(mean(Magcom[930:950, :, powind], axis=0)))#-mean(Magcom[938:940, 410:430, powind], axis=1, keepdims=True), axis=0)))
plt.show()
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
#plt.plot(absolute(Magcom[:, 0, powind]))#-absolute(mean(Magcom[:, :, powind], axis=1, keepdims=True))))

print shape(pwr), pwr.dtype
print amax(pwr), amin(pwr)
print shape(xx), xx.dtype
print amax(xx), amin(pwr)


#plt.plot( detuning((pwr+0.5)*0.5)/(2*pi))
#plt.plot(pwr, absolute(Magcom[frqind, :, powind]-mean(Magcom[frqind, 410:430, powind], axis=0, keepdims=True)))

#print {"a":absolute(Magcom[frqind, :, powind]-mean(Magcom[frqind, 410:430, powind], axis=0, keepdims=True))}
#plt.plot(xx, absolute(S11_IDT_no_IDT_ref(r_qubit(detuning(xx), array([-1e-20]))) ))
#plt.show()

plt.pcolormesh(xx, freq,  absolute(Magcom[:, :, powind]-mean(Magcom[:, 410:430, powind], axis=1, keepdims=True)))
          # aspect="auto", origin="lower",
          # interpolation="none",
          #  extent=[ amin(pwr),amax(pwr), amin(freq),amax(freq)], 
          #      )
plt.xlabel("Flux (V)") 
plt.ylabel("Frequency (Hz)")
plt.title("|R-R(flx=4.2V)| vs freq & flux at -93 dBm")
plt.colorbar()
plt.show()

plt.pcolormesh(-detuning(xxfrq)/(2.0*pi), freq,  absolute(Magcom[:, :, powind]-mean(Magcom[:, 410:430, powind], axis=1, keepdims=True)))
          # aspect="auto", origin="lower",
          # interpolation="none",
          #  extent=[ amin(pwr),amax(pwr), amin(freq),amax(freq)], 
          #      )
plt.xlabel("Detuning (Hz)") 
plt.ylabel("Frequency (Hz)")
plt.title("|R-R(flx=4.2V)| vs freq & flux at -93 dBm")
plt.colorbar()
plt.show()

plt.plot(freq, absolute(Magcom[:, :, powind])-absolute(mean(Magcom[:, :, powind], axis=1, keepdims=True)))
plt.xlabel("Frequency (Hz)")
plt.ylabel("|S11|-|<S11>|")
plt.title("|S11| -|mean(S11 in flux)| plotted vs frequency")
plt.show()

plt.plot(pwr, transpose(absolute(Magcom[:, :, powind])-absolute(mean(Magcom[:, :, powind], axis=1, keepdims=True))))
plt.xlabel("Flux (V)")
plt.ylabel("|S11|-|<S11>|")
plt.title("|S11| -|mean(S11 in flux)| plotted vs flux (V)")
plt.show()
#plt.plot(xx, detuning((xx+0.5)*0.5))
#plt.plot(x, detuning((x+0.5)*0.5))
#print shape(pwr)
#print shape(-detuning(array(pwr)*0.8))
#plt.ylim(-0.0008, 0.0008)

plt.plot(-detuning(xxfrq)/(2.0*pi), transpose(absolute(Magcom[:, :, powind])-absolute(mean(Magcom[:, :, powind], axis=1, keepdims=True))))
plt.xlabel("Detuning (Hz)")
plt.ylabel("|S11|-|<S11>|")
plt.title("|S11| -|mean(S11 in flux)| plotted vs detuning")
plt.show()



if 1:
    #Magy=[]
    #for n,p in enumerate(pwr):
    #    Magy.append(amax(absolute(Magcom[:, n, :]), axis=1)-amin(absolute(Magcom[:, n, :]), axis=1))
    Magy=amax(absolute(Magcom[:, :, :]), axis=0)-amin(absolute(Magcom[:, :, :]), axis=0)
    #plt.plot(Magy)
#    plt.plot(pwr-87, mean(Magy[:, :], axis=0))
    #plt.plot(dB(Magcom[236, powind, :]))#-mean(Magcom[:, :, powind], axis=1, keepdims=True)))
    #plt.show()
    plt.plot(Magy[:, powind])
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