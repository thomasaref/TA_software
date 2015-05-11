# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 14:42:28 2015

@author: thomasaref
"""
from pyaudio import PyAudio
from numpy import sin, pi, amax, amin, linspace, interp, zeros, log10
from Atom_HDF5 import Read_HDF5
from Atom_Plotter import Plotter


#f=Read_HDF5(read_file='/Users/thomasaref/Dropbox/Current stuff/TA_enaml/Two tone, egate n91dbm idt n127dbm 2013-10-13_213934/meas.h5')
#f=Read_HDF5(read_file='/Users/thomasaref/Dropbox/Current stuff/TA_enaml/Two tone, egate n167 dBm, Idt n127dBm 2013-10-30_083942/meas.h5')
#f=Read_HDF5(read_file='/Users/thomasaref/Dropbox/Current stuff/TA_enaml/two tone, flux vs control freq, egate n111dbm, IDT n127dbm  2013-10-12_104752/meas.h5')
#f=Read_HDF5(read_file="/Users/thomasaref/Dropbox/Current stuff/TA_enaml/
#f=Read_HDF5(main_dir="Listening, PXI source, n60 to 0 dBm, Yok n0p6 to n0p2 2013-11-14_132730")
#f=Read_HDF5(main_dir='Pulse 25ns improved gate V sweep Yoko 0p696V 2013-11-06_102036')
f=Read_HDF5(main_dir='Time domain, gate 5mV with flux sweep -10dbm 2013-11-04_093303')
f.open_and_read()
print f.data['Mag'].keys()

#mag_vec=f.data['Mag_vec']['Mag_vec']
##anr= f.data['Mag_vec']['Anritsu frequency']
#anr=f.data['Mag_vec']['RF power']
#yok= f.data['Mag_vec']['Yoko voltage']
#phase=f.data['Phase']['Phase']

mag_vec=f.data['Mag']['I']
anr=f.data['Mag']['time']
yok= f.data['Mag']['Yoko voltage']

#i=166
#td=mag_vec[i, :]

i=21 #95
#td=mag_vec[i, :]
#print yok[i]
td=mag_vec[94:133, i]

x=linspace(0, len(td)-1, len(td))
#y=-(0.375/150.0)*(x-150)
#y=0.0131-(0.01334-0.0131)/150.0* (x-150)
#td=-(td-y)
td=(td-amin(td))/(amax(td)-amin(td))
#for i, a in enumerate(td):
#    if a<0.1:
#        td[i]=0
#print td

#td=(td)*127+128#-mean(td)
#td=td[[ 16, 27, 36]]
#See http://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 128000 #32000 #number of frames per second/frameset.
#See http://www.phy.mtu.edu/~suits/notefreqs.html
FREQUENCY = 587.33#/20.0 #D5 #1000#261.63 #Hz, waves per second, 261.63=C4-note.
LENGTH =10 #seconds to play sound

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''
sd=linspace(0, NUMBEROFFRAMES-1, NUMBEROFFRAMES)
x=linspace(0, NUMBEROFFRAMES-1, len(td))
tdi=interp(sd, x, td)
aamin=amin(mag_vec)
aamax=amax(mag_vec)

#freq=yok[[  16,  27, 36]]*7320.0+4387.33+80+27-100 #FREQUENCY #anr/4.8e9*FREQUENCY
#D5 587.33
#B5	 987.77
#E6	 1318.51
#print freq
#b=zeros(sd.shape)
#for qq, ww in enumerate(td):
#    b+=ww*sin(pi*sd/(BITRATE/freq[qq]))

freq=FREQUENCY
b=tdi*sin(pi*sd/(BITRATE/freq))
b=(b-amin(b))/(amax(b)-amin(b))
c=(b*254+1).astype(int)

plot=Plotter()

#td=mag_vec[:, 80]
plot.add_plot("cross_sec", yname="Macvec", ydata=td, xname="time", xdata=anr[94:133]/1.0e-9)
#td=mag_vec[:, 85]
#plot.add_plot("cross_sec1", yname="Macvec1", ydata=td)
#td=mag_vec[[ 16,  27, 36], 95]
#plot.add_plot("cross_sec2", yname="Macvec2", ydata=c)

#plot.add_plot("cross_sec2", yname="Macvec2", ydata=mag_vec[:, 95])
#td=mag_vec[:, 95]
#plot.add_plot("cross_sec3", yname="Macvec3", ydata=td)
#td=mag_vec[:, 100]
#plot.add_plot("cross_sec4", yname="Macvec4", ydata=td)
#td=mag_vec[:, 105]
#plot.add_plot("cross_sec5", yname="Macvec5", ydata=td)
#td=mag_vec[:, 110]
#plot.add_plot("cross_sec6", yname="Macvec6", ydata=td)

#plot.add_img_plot(mag_vec, yok, linspace(0, len(anr)-1, len(anr)))
#zplot.add_img_plot(zname="blah", zdata=mag_vec)#z, ydata=linspace(0, len(anr)-1, len(anr)), xdata=linspace(0, len(yok)-1, len(yok)))

#plot.add_plot("cross_sec", yname="Macvec1", ydata=c)
#    plot.add_plot("cross_se2", yname="Macvec2", ydata=mag_vec[:, 75])
plot.show()
for x in xrange(NUMBEROFFRAMES):
    WAVEDATA = WAVEDATA+chr(c[x])

#fill remainder of frameset with silence
for x in xrange(RESTFRAMES):
    WAVEDATA = WAVEDATA+chr(128)

p = PyAudio()
FORMAT=p.get_format_from_width(1)
stream = p.open(format = p.get_format_from_width(1),
                channels = 1,
                rate = BITRATE,
                output = True)
stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()

if 0:
    import wave
    wf = wave.open('short_pulse.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(BITRATE)
    wf.writeframes(WAVEDATA)
    wf.close()