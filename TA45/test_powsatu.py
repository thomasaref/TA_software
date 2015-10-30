# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 14:26:51 2015

@author: thomasaref
"""

from scipy.constants import k,h,pi, e, hbar, epsilon_0 as eps0
from numpy import sin, squeeze, shape, linspace, log10, mean, amax, amin, absolute, reshape, transpose, real, imag, angle, cos, sqrt, array, exp, delete

print 3488.0/(8*96.0e-9)/1.0e9
print 3488.0/(8*80.0e-9)/1.0e9

Np=9
C=1.414*46*eps0*25.0e-6*Np

print C, 1.414*46*eps0*25.0e-6*36
Tc=1.3
Delta=3.528/2.0*k*Tc
print Delta/e*1e6
Rn=9.0e3

Ic=pi *Delta/(2.0*e)/Rn
print Ic

Ejmax=hbar*Ic/(2.0*e)
Ec=e**2/(2.0*C)
print Ejmax/k, Ec/k, Ejmax/Ec

EJmax=0.82*k
print EJmax/h/1e9, Ec/h/1e9
print (sqrt(8.0*EJmax*Ec)+Ec/4-(Ec/12.0)*(6+6+3))/h/1e9
EC=0.007*k
print (sqrt(8.0*EJmax*EC)+EC/4-(EC/12.0)*(6+6+3))/h/1e9

f0=4.453e9
hf0=h*f0
print "coupling {}".format(0.45*Np*0.046*f0/1.0e9)
S11_0 = 0.5094
S21_0 = 0.28# 0.26181; %0.270
S22_0 = 0.546 #0.55;
theta_L =0*0.613349 #0.64; %-2.55068; %-0.59;

Gamma_ac = 0.0001e6*2*pi# 38e6*2*pi;
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

x=linspace(-10, 10, 401)
plt.plot(x, flux_parabola(x*0.195))
plt.show()
phi=linspace(-pi, pi, 101)
f=linspace(4e9, 6e9, 101)
#plt.plot(phi, (1-cos(Np*phi))/(1-cos(phi))/81.0)
fo0=5.45e9
plt.plot(f, 0.45*Np*0.046*fo0/1.0e9*(sin(Np*pi*(f-fo0)/fo0/2.0)/(Np*pi*(f-fo0)/fo0/2.0))**2)
plt.plot(f, 0.45*Np*0.046*fo0/1.0e9*(sin(Np*pi*(f-fo0)/fo0)/(Np*pi*(f-fo0)/fo0))**2)

plt.plot([f0, f0], [0, 0.45*Np*0.046*fo0/1.0e9])
plt.show()
print shape(x)
#plt.plot(x, absolute(S11_IDT_no_IDT_ref(r_qubit(detuning(x), array([-1e-10]))) ))
#plt.show()
          
from h5py import File
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0914/TA_A58_scb_refl_powsat_1.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0912/TA_A58_scb_trans_powfluxswp_higherbw.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0913/TA_A58_scb_refl_powfluxswp_higherbw_revV.hdf5"

#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp_higherpower.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0911/TA_A58_scb_refl_powfluxswp_higherbw.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/TA_A58_scb_refl_power_fluxswp.hdf5"
#file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A58_cooldown1/Data_0915/TA_A58_scb_refl_powfluxswp_lowpow.hdf5"

file_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/Data_1005/TA_A46_refl_fluxmap_andpower.hdf5"

#from HDF5_functions import read_hdf5
from numpy import float64
#print read_hdf5(file_path)
print "start data read"
with File(file_path, 'r') as f:
    print f["Traces"].keys()
    Magvec=f["Traces"]["Rohde&Schwarz Network Analyzer - S12"]#[:]
    data=f["Data"]["Data"]
    fstart=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][0]
    fstep=f["Traces"]['Rohde&Schwarz Network Analyzer - S12_t0dt'][0][1]
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
    pwr=data[:, 0, 0]
    #pwr=delete(pwr, 73)
    yoko= data[0, 1, :]
    yoko=yoko.astype(float64)
    #print yoko
    freq=linspace(fstart, fstart+fstep*(sm-1), sm)

print shape(Magcom)
print "end data read"

def dB(x):
    return 20*log10(absolute(x))

powind=0
frqind=234
print pwr[powind]

if 0:
    plt.pcolormesh( dB(Magcom[:, 0, :]))
    plt.show()
    
    plt.pcolormesh(yoko, freq, dB(Magcom[:, 0, :]))
    plt.xlabel("Flux (V)")
    plt.ylabel("Frequency (Hz)")
    plt.title("Reflection fluxmap at -117 dBm")
    plt.colorbar()
    plt.show()
Magcom=Magcom[:,powind, :]-mean(Magcom[:, powind, 184:188 ], axis=1, keepdims=True)

print freq[106]

#plt.plot(flux_parabola((yoko-2.5)*0.195), absolute(Magcom[106, :]))
#plt.show()
#plt.plot(amax(absolute(Magcom), axis=0))
#plt.plot(absolute(Magcom[105, :]))
plt.plot(yoko, absolute(Magcom[106, :])/amax(absolute(Magcom[106, :])))
#plt.plot(yoko, absolute(Magcom[106, :]))

#plt.plot(yoko, absolute(cos(pi*(yoko-2.5)*0.195))) #flux_parabola(yoko)/amax(flux_parabola(yoko)))
#plt.plot(yoko, flux_parabola((yoko-2.5)*0.195)/f0)
#plt.plot(yoko, detuning((yoko-2.5)*0.195)/f0)
#R=r_qubit(detuning((yoko)*0.195), array([0.0]))

def couple(f):
    return 0.45*Np*0.046*fo0/1.0e9*(sin(Np*pi*(f-fo0)/fo0/2.0)/(Np*pi*(f-fo0)/fo0/2.0))**2
def couple2(f):    
    return 0.45*Np*0.046*fo0/1.0e9*(sin(Np*pi*(f-fo0)/fo0)/(Np*pi*(f-fo0)/fo0))**2

#det=detuning(yoko*0.195)
#f=flux_parabola(yoko*0.195)
#RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*couple(f)))
#plt.plot(yoko, absolute(RR)/amax(absolute(RR)), label="50 MHz")
#
#RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*couple2(f)))
#plt.plot(yoko, absolute(RR)/amax(absolute(RR)), label="50 MHz")

RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*50.0e6))
plt.plot(yoko, absolute(RR)/amax(absolute(RR)), label="50 MHz")
#RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*100.0e6))
#plt.plot(yoko, absolute(RR)/amax(absolute(RR)))
#RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*50.0e6))
#plt.plot(yoko, absolute(RR)/amax(absolute(RR)))
RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*200.0e6))
plt.plot(yoko, absolute(RR)/amax(absolute(RR)), label="200 MHz")
#RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*300.0e6))
#plt.plot(yoko, absolute(RR)/amax(absolute(RR)))
RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*500.0e6))
plt.plot(yoko, absolute(RR)/amax(absolute(RR)), label="300 MHz")
RR=1/(1-1j*detuning(yoko*0.195)/(2.0*pi*800.0e6))
plt.plot(yoko, absolute(RR)/amax(absolute(RR)), label="800 MHz")
plt.legend()

#plt.plot(yoko, absolute(R)/amax(absolute(R)))

plt.show()
print yoko[186]
plt.pcolormesh(yoko, freq, absolute(Magcom))
plt.xlabel("Flux (V)")
plt.ylabel("Frequency (Hz)")
plt.title("Reflection fluxmap at -117 dBm")
plt.colorbar()
plt.show()

plt.plot(absolute(Magcom[:, 250]))
plt.show()

plt.pcolormesh(absolute(Magcom))
plt.show()

print freq[106]
plt.plot(amax(absolute(Magcom), axis=0))
#plt.plot(absolute(Magcom[105, :]))
plt.plot(absolute(Magcom[106, :]))

plt.show()
plt.plot(transpose(absolute(Magcom[:, :])))
plt.show()

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