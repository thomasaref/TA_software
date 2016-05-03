# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:36:04 2016

@author: thomasaref
"""
from af302xC_packager import af302xCPackager
from afsiggen import afSigGen
from afdigitizer import afDigitizer
import matplotlib.pyplot as plt
from time import time
from numpy import log10, absolute

class afWaveform(af302xCPackager):
    def gen_waveform(self):
        temp=[str(0) for n in range(300)]
        #a.extend([str(1) for n in range(300)])
        temp[10]='1'
        temp=','.join(temp)
        return temp, temp
wf=afWaveform()
wf.package_waveform()

try:
    a=afSigGen()
    d=afDigitizer()
    d.start_dig()
    d.input_level=0.0
    d.sample_rate=250.0e6
    d.sw_trigger_mode='Armed'

    a=afSigGen()
    a.start()
    a.level=-20
    a.output=True
    print d.level_correction
    cpx=d.get_trace()
    print d.calc_mean_power()
    cpx=d.captmem(2000)
    print d.calc_mean_power()
    plt.plot(20*log10(absolute(d.fftd)))
    plt.show()
finally:
    d.stop_dig()
    a.stop()


