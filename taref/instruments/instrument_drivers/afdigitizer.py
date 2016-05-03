# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:11:10 2016

@author: Morran or Lumi
"""

from ctypes import  c_long, pointer, c_float, c_double, c_ulong, POINTER, byref, WinDLL, Structure, c_void_p, create_string_buffer
from numpy import zeros, array, log10, absolute, mean, fft, empty, power
import matplotlib.pyplot as plt
from pxi_backbone import PXI_Backbone, pp
from time import time

#Code for generating COM module
#from comtypes.client import CreateObject
#s=CreateObject("afComDigitizer.afCoDigitizer")
from comtypes.gen import AFCOMDIGITIZERLib

class afDigitizerBufferIQ_t(Structure):
    _fields_ = [
        ('iBuffer', POINTER(c_float)),
        ('qBuffer', POINTER(c_float)),
        ('samples', c_ulong),
        ('userData', c_void_p)]
        
class afDigitizer(PXI_Backbone):
    def __init__(self):
        super(afDigitizer, self).__init__(lib_name='afDigitizerDll_32.dll', com_lib=AFCOMDIGITIZERLib)

    @property
    def is_active(self):
        return self.get_func('IsActive_Get', prefix=bool)

    sample_rate=pp('Modulation_GenericSamplingFrequency', dtype=c_double)
    modulation_mode=pp('Modulation_Mode', prefix='mm') #Generic
    LO_reference=pp('LO_Reference', prefix='lorm') #OXCO
    input_level=pp('RF_RFInputLevel', dtype=c_double) 
    frequency=pp('RF_CentreFrequency', dtype=c_double)
    
    trigger_source=pp('Trigger_Source', prefix='ts')
    edge_gate_polarity=pp('Trigger_EdgeGatePolarity')
    pre_edge_trigger_samples=pp('Trigger_PreEdgeTriggerSamples')
    sw_trigger_mode=pp('Trigger_SwTriggerMode', prefix='swt') #Immediate, Armed
    reclaim_timeout=pp('Capture_IQ_ReclaimTimeout')
    
    def start_dig(self, lo_address='3011D1', dig_address='3036D1', plugin=False, mod_mode="Generic"):
        self.do_func("ClearErrors")
        self.do_func("BootInstrument", lo_address, dig_address, plugin)
        self.modulation_mode=mod_mode
        d.LO_reference='OCXO'

    @property
    def lc(self):
        if getattr(self, '_lc', None) is None:
            self._lc=self.level_correction
        return self._lc
            
    def get_trace(self, points=1000, timeout=10000):
            
        self.reclaim_timeout=timeout
        #self.set_func("Capture_IQ_ReclaimTimeout_Set", timeout)
        i_avgd = zeros(points)
        q_avgd = zeros(points)
        #samples=self.nSamples
        avgs=1 #self.nAverages_per_trigger
        #timeout=self.fTimeout
        #tot_samps=int(self.nTotalSamples)
      
        i_buffer = empty(points, dtype=c_float)
        q_buffer = empty(points, dtype=c_float)
        #self.all_cpx = np.empty(self.averages, dtype=complex)
        i_ctypes = i_buffer.ctypes.data_as(POINTER(c_float))
        q_ctypes = q_buffer.ctypes.data_as(POINTER(c_float))
        buffer_ref = afDigitizerBufferIQ_t(i_ctypes, q_ctypes, points)
        buffer_ref_pointer = pointer(buffer_ref)
        capture_ref = c_long()
        tstart=time()
        self.do_func('Capture_IQ_IssueBuffer', byref(buffer_ref), timeout, byref(capture_ref))
        self.do_func('Capture_IQ_ReclaimBuffer', capture_ref, byref(buffer_ref_pointer))
        print tstart-time()
        if buffer_ref_pointer:
            print "BUFFER POINTER OK"
            total_samples = buffer_ref.samples
            print(total_samples)
        else:
            raise Exception("NO BUFFER")
            total_samples = 0

        #self.samples = total_samples
        i_avgd += mean(i_buffer[:total_samples].reshape(avgs, points), axis=0)
        q_avgd += mean(q_buffer[:total_samples].reshape(avgs, points), axis=0)
        #self.log("acq stopped")                
        i_avgd = i_avgd/1 #self.nTriggers
        q_avgd = q_avgd/1 #self.nTriggers
        self.cpx_avgd = i_avgd + 1j*q_avgd

        return self.cpx_avgd #self.i_buffer[:total_samples], self.q_buffer[:total_samples]
        #I = mean(self.i_buffer[:total_samples])
        #Q = mean(self.q_buffer[:total_samples])
        #self.Mag_vec = np.sqrt(I**2 + Q**2)
        #self.Phase = np.angle(I+1j*Q, deg=True)
        #self.Mag_rms = np.sqrt(np.mean(self.q_buffer[:total_samples]**2 + self.i_buffer[:total_samples]**2))
        #self.all_cpx[:total_samples] = self.i_buffer[:total_samples] + 1j*self.q_buffer[:total_samples]
        #self.Mag_abs = np.mean(np.abs(self.all_cpx))
        #self.I = I
        #self.Q = Q
        #self.point_ready = True
        #print("Data received!")

    def stop_dig(self):
        self.do_func('CloseInstrument')
        self.do_func("DestroyObject")

    def trigger_arm(self, num_samples):
        self.do_func('Capture_IQ_TriggerArm', 2*num_samples)
 
    def captmem(self, num_samples):
        typeBuffer=c_float*num_samples
        i_buffer=typeBuffer()
        q_buffer=typeBuffer()
        tstart=time()
        self.do_func("Capture_IQ_CaptMem", num_samples, byref(i_buffer), byref(q_buffer))
        print time()-tstart
        self.cpx_avgd=array(i_buffer)+1j*array(q_buffer)
        return self.cpx_avgd
    
    def full_run(self, num):
        self.trigger_arm(num)
        self.captmem(num)

    @property
    def level_correction(self):
        return self.get_func('RF_LevelCorrection_Get', dtype=c_double)
 
    def calc_mean_power(self):
        return 20*log10(mean(absolute(self.cpx_lc)))

    @property
    def cpx_lc(self):
        return self.cpx_avgd*power(10.0, self.lc/20.0)
        
    def fftd(self):
        fftd=20*log10(absolute(fft.fftshift(fft.fft(self.cpx_lc))))
        return fftd-fftd.max()+d.calc_mean_power()
#    def capt_test(num):
#        try:
#            pDetected=c_long()
#            print _lib.afDigitizerDll_Capture_IQ_TriggerArm(ses, 1*num)
#            while pDetected.value==0:
#                print _lib.afDigitizerDll_Capture_IQ_TriggerDetected_Get(ses, byref(pDetected))
#                print pDetected.value
#            pCaptured=c_long()
#            while pCaptured.value==0:
#                print _lib.afDigitizerDll_Capture_IQ_GetSampleCaptured(ses, num, byref(pCaptured))
#                print pCaptured.value
#            i_buffer = zeros(num, dtype=c_float)
#            q_buffer = zeros(num, dtype=c_float)
#            i_ctypes = i_buffer.ctypes.data_as(POINTER(c_float))
#            q_ctypes = q_buffer.ctypes.data_as(POINTER(c_float))
#            print _lib.afDigitizerDll_Capture_IQ_CaptMem(ses, num, i_ctypes, q_ctypes)
#            #print _lib.afDigitizerDll_Capture_IQ_GetCaptMemFromOffset(ses, 10, num, i_ctypes, q_ctypes)
#            return i_buffer, q_buffer
#        except KeyboardInterrupt:
#            print 'keyboard interaupt'

if __name__=="__main__":
    d=afDigitizer()
    d.start_dig()
    d.input_level=0.0
    d.sample_rate=250.0e6
    #print d.get_func("Trigger_Source_Get", prefix="ts")
    #print d.get_func('RF_CentreFrequency_Get', dtype=c_double)
    print d.get_func('Modulation_Mode_Get')
    print d.get_func('IsActive_Get')
    d.sw_trigger_mode='Armed'
    from afsiggen import afSigGen
    a=afSigGen()
    a.start()
    a.level_set(-30)
    a.rf_state_set(True)
    print d.level_correction
    cpx=d.get_trace()
    print d.calc_mean_power()
    if 0:
        d.start_dig()
        I, Q=d.captmem(2000)
        d.get_level_correction()
        print d.calc_mean_power(I, Q)
        I, Q=d.get_trace(1000)
        print d.calc_mean_power(I, Q)
        plt.plot(20*log10(absolute(fft.fftshift(fft.fft(I+1j*Q)))))
        plt.show()
        d.stop_dig()
        #print get_func("Capture_IQ_GetAbsSampleTime", ses, 0)

        #print get_func("Trigger_Source_Get", ses)


        #print get_func("Capture_PipeliningEnable_Get", ses)

        #do_func('Capture_PipeliningEnable_Set', ses, 1)

        #do_func('Trigger_SwTriggerMode_Set', ses, 1) #set software trigger mode to armed
        #print get_func('Trigger_SwTriggerMode_Get', ses)

        #print get_func('Capture_IQ_TriggerCount_Get', ses)


        #pSampleNumber=c_ulong()
        #_lib.afDigitizerDll_Capture_IQ_GetTriggerSampleNumber(ses, 0, byref(pSampleNumber))
