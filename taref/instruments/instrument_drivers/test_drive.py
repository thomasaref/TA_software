# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:36:04 2016

@author: thomasaref
"""
from af302xC_packager import af302xCPackager
from afsiggen import afSigGen
from afdigitizer import afDigitizer
from NI6652 import NI6652
import matplotlib.pyplot as plt
from time import time, sleep
from numpy import log10, absolute
from ctypes import c_ulong

def gen_waveform(sel=True):
    temp=[str(0) for n in range(300)]
    if sel:
        temp.extend([str(1) for n in range(300)])
    else:
        temp[10]='1'
    temp=','.join(temp)
    return temp, temp

aiq=af302xCPackager()
aiq.package_waveform(gen_waveform(False))

#try:
if 1:
    a=afSigGen()
    d=afDigitizer()
    d.start_dig()
    d.input_level=0.0
    d.sample_rate=250.0e6
    d.sw_trigger_mode='Armed'
    d.pipelining_enable=True
    d.trigger_source="PXI_STAR"

    a=afSigGen()
    a.start()
    a.level=-20
    a.output=True
    a.arb_add_file(aiq.aiq_file_path)
    a.scenario_set("PXI_STAR_TO_ARBTRIG")
    print a.scenario_list_get()
    a.arb_external_trigger_enable=True
    a.modulation_source="ARB"
    #print a.scenario_list_get()
    #a.arb_play_file(aiq.aiq_file_path)

    print d.level_correction
    tm=NI6652()
    tm.connect_SW_trigger("PXI_Star1")
    tm.connect_SW_trigger("PXI_Star5")
    tm.connect_SW_trigger("PXI_Star9")
    #cpx=d.get_trace()
    #print d.calc_mean_power()
    #plt.plot(d.fftd())
    #plt.show()
    #cpx=d.captmem(2000)
    #print d.calc_mean_power()
    #plt.plot(20*log10(absolute(d.cpx_lc)+1e-10))
    #plt.plot(d.fftd())
    #d.prep_captmem(d.BUFFER_SIZE)
    def test2(o=100, r=1000, w=20, m=d.BUFFER_SIZE):
        d.prep_captmem2(w)
        i_avgd=zeros(w)
        q_avgd=zeros(w)
        for i in range(o,m,r):
            d.trigger_arm(w)
            m.send_software_trigger()
            d.captmem()
            i_avgd+=array(d.i_buffer)
            q_avgd+=array(d.q_buffer)
        return (i_avgd+1j*q_avgd)#/(n+1)
            
    def test(o=100, r=1000, w=20, m=d.BUFFER_SIZE):
        a.arb_stop_playing()
        a.arb_play_file(aiq.aiq_file_path)
        d.trigger_arm(m)
        tm.send_software_trigger()
        i_buffer, q_buffer=d.prep_captmem(w)
        i_avgd=zeros(w)
        q_avgd=zeros(w)
        for i in range(100):
            print "no trig!"
            if d.trigger_detected:
                break
        for n, i in enumerate(range(o,m,r)):
            d.captmem_from_offset(i, w, i_buffer, q_buffer)
            i_avgd+=array(i_buffer)
            q_avgd+=array(q_buffer)
        return (i_avgd+1j*q_avgd)/(n+1)
        #d.prep_captmem(m)
        #return d.captmem_from_offset(o, w)

    from numpy import mean, array, zeros
    
    def testwrap(o=100, r=1000, w=20, m=d.BUFFER_SIZE, run_both=True):
        tstart=time()
        d1=test(o,r,w,m)
        #d1=mean(array(test(o,r,w,m)), axis=0)
        #d1=mean([arr[0]+1j*arr[1] for arr in d1])
        print time()-tstart
        if run_both:
            tstart=time()
            d2=test2(o,r,w,m)
            #cpx_avgd=zeros(w)
            #q_avgd=zeros(w)
            #d.prep_captmem(m/10)
            #for i in range(10):
            #    cpx=test2(o,r,w,m)

            #    cpx_avgd += mean(array(cpx).reshape(10, m/10), axis=0)
                #q_avgd += mean(array(lQ).reshape(10, m/10), axis=0)

            #d2=cpx_avgd #i_avgd+1j*q_avgd
            print time()-tstart
            return d1, d2
        return d1
        
    #plt.show()
    def test_run(m=1000, n=10000000):
        d.trigger_arm(n)
        for i in range(100):
            print d.get_sample_captured(m)
        d.captmem(m)
        
    def stop():
        d.stop_dig()
        a.stop()
        tm.stop()
    #plt.plot(20*log10(absolute(d.fftd())))
    #plt.show()
#except Exception as e: #finally:
#    d.stop_dig()
#    a.stop()
#    raise e
if 0:
    d.trigger_arm(int(6.7e7))
    d.get_func("Capture_IQ_CapturedSampleCount_Get", dtype=c_ulong)
    tarr=[d.get_abs_sample_time(n) for n in range(len(d.cpx_lc))]
    [tarr[n+1]-tarr[n] for n in range(len(tarr)-1)]
    a.arb_add_file(aiq.aiq_file_path)
    a.arb_play_file(aiq.aiq_file_path)
    a.arb_stop_playing()
    a.modulation_source="CW"
    