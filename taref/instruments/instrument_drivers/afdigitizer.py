# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:11:10 2016

@author: Morran or Lumi
"""

from ctypes import  c_long, pointer, c_float, c_double, c_ulong, POINTER, byref, WinDLL, Structure, c_void_p, create_string_buffer
from numpy import zeros, array, log10, absolute, mean, fft, empty
import matplotlib.pyplot as plt
from pxi_backbone import PXI_Backbone

#Code for generating COM module
#from comtypes.client import CreateObject
#s=CreateObject("afComSigGen.afCoSigGen")
from comtypes.gen import AFCOMDIGITIZERLib

class afDigitizerBufferIQ_t(Structure):
    _fields_ = [
        ('iBuffer', POINTER(c_float)),
        ('qBuffer', POINTER(c_float)),
        ('samples', c_ulong),
        ('userData', c_void_p)]

class afDigitizer(PXI_Backbone):
    def __init__(self, lib_name, func_prefix=None):
        super(afDigitizer, self).__init__(lib_name=='afDigitizerDll_32.dll', com_lib=AFCOMDIGITIZERLib)

    def start_dig(self, lo_address='3011D1', dig_address='3036D1', plugin=False, mod_mode=5):
        if mod_mode is None:
            mod_mode="mmGeneric"
        self.do_func("BootInstrument", self.session, lo_address, dig_address, plugin)
        print self.get_func('Modulation_Mode_Get', self.session)#dtype=c_int
        self.do_func("Modulation_Mode_Set", self.session, 5) #set mod mode to generic
        print self.get_func('Modulation_Mode_Get', self.session)
        print self.get_func('IsActive_Get', self.session)

        self.rf_centre_frequency_set(self.center_frequency)
        self.rf_rf_input_level_set(self.ref_amplitude)

        self.trigger_source_set(self.trigger_source_)
        self.trigger_edge_gate_polarity_set(self.trigger_edge_)
        self.trigger_pre_edge_trigger_samples_set(self.pretrigger_samples)

    def set_sampling_frequency(self, sample_rate):
        self.do_func('Modulation_GenericSamplingFrequency_Get', self.session, c_double(sample_rate))
        self.sample_rate=sample_rate

    def get_sampling_frequency(self):
        self.frequency=self.get_func('Modulation_GenericSamplingFrequency_Get', self.session, dtype=c_double)
        return self.frequency

    def get_trace(self, points=1000, timeout=1000):
        self.do_func("Capture_IQ_ReclaimTimeout_Set", timeout)

        self.i_buffer = empty(points, dtype=c_float)
        self.q_buffer = empty(points, dtype=c_float)
        #self.all_cpx = np.empty(self.averages, dtype=complex)
        self.i_ctypes = self.i_buffer.ctypes.data_as(POINTER(c_float))
        self.q_ctypes = self.q_buffer.ctypes.data_as(POINTER(c_float))
        self.buffer_ref = afDigitizerBufferIQ_t(self.i_ctypes, self.q_ctypes, points)
        self.buffer_ref_pointer = pointer(self.buffer_ref)
        self.capture_ref = c_long()

        self.do_func('Capture_IQ_IssueBuffer', self.session, self.buffer_ref, self.timeout, byref(self.capture_ref))
        self.do_func('Capture_IQ_ReclaimBuffer', self.session, self.capture_ref, byref(self.buffer_ref_pointer))
        if self.buffer_ref_pointer:
            print "BUFFER POINTER OK"
            total_samples = self.buffer_ref.samples
            print(total_samples)
        else:
            print "NO BUFFER"
            total_samples = 0

        self.samples = total_samples
        return self.i_buffer[:total_samples], self.q_buffer[:total_samples]
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
        self.do_func('CloseInstrument', self.session)
        self.do_func("DestroyObject", self.session)

    #i_buffer = zeros(num_samples, dtype=c_float)
    #q_buffer = zeros(num_samples, dtype=c_float)
    #i_ctypes = i_buffer.ctypes.data_as(POINTER(c_float))
    #q_ctypes = q_buffer.ctypes.data_as(POINTER(c_float))

    def captmem(self, num_samples):
        typeBuffer=c_float*num_samples
        i_buffer=typeBuffer()
        q_buffer=typeBuffer()
        self.do_func("Capture_IQ_CaptMem", self.session, num_samples, byref(i_buffer), byref(q_buffer))
        return array(i_buffer), array(q_buffer)

    def get_level_correction(self):
        self.level_correction=self.get_func('RF_LevelCorrection_Get', self.session, dtype=c_double)
        return self.level_correction

    def calc_mean_power(self, I, Q):
        return 10*log10(mean(I**2+Q**2))+self.level_correction

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
    try:
        d=afDigitizer()
        d.start_dig()
        I, Q=d.captmem(2000)
        d.get_level_correction()
        print d.calc_mean_power(I, Q)
        I, Q=d.get_trace(1000)
        print d.calc_mean_power(I, Q)
        plt.plot(20*log10(absolute(fft.fftshift(fft.fft(I+1j*Q)))))
        plt.show()
    finally:
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
