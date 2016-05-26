# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 14:11:10 2016

@author: Morran or Lumi
"""

from ctypes import  c_long, pointer, c_float, c_double, c_ulong, POINTER, byref, WinDLL, Structure, c_void_p, create_string_buffer
from numpy import zeros, array, log10, absolute, mean, fft, empty, power
import matplotlib.pyplot as plt
import pxi_backbone
reload(pxi_backbone)

from pxi_backbone import PXI_Backbone, pp
from time import time
if 0:  #Code for generating COM module
    from comtypes.client import CreateObject
    s=CreateObject("afComDigitizer.afCoDigitizer")
from comtypes.gen import AFCOMDIGITIZERLib

class afDigitizerBufferIQ_t(Structure):
    _fields_ = [
        ('iBuffer', POINTER(c_float)),
        ('qBuffer', POINTER(c_float)),
        ('samples', c_ulong),
        ('userData', c_void_p)]

class afDigitizer(PXI_Backbone):
    BUFFER_SIZE=67108608 #buffer size for 3035C with 32 bit data type

    def log(self, msg):
        if self.parent is not None:
            self.parent.log(msg)
        else:
            print msg
            
    def __init__(self, num_samples=1000, avgs_per_trig=1, num_trigs=1, timeout=10000, start_idx=None, parent=None):
        """initialization calls PXI_Backbone __init__ with appropriate arguments"""
        super(afDigitizer, self).__init__(lib_name='afDigitizerDll_32.dll', com_lib=AFCOMDIGITIZERLib)
        self._num_samples=num_samples
        self._avgs_per_trig=avgs_per_trig
        self.num_trigs=num_trigs
        self.timeout=timeout
        self._start_idx=start_idx
        self.parent=parent
    
    @property
    def total_samples(self):
        return self.num_samples*self.avgs_per_trig
        
    @property
    def sampling_time(self):
        return self.num_samples/self.sample_rate        

    @property
    def start_idx(self):
        if self._start_idx is None:
            return self.num_trigs-1
        return self._start_idx
        
    @start_idx.setter
    def start_idx(self, value):
        if value>self.num_trigs-1 or value<0:
            raise Exception("start idx out of bounds")
        self._start_idx=value

    @property
    def num_trigs(self):
        return self._num_trigs
    
    @num_trigs.setter    
    def num_trigs(self, value):
        self._num_trigs=int(value)

    @property
    def timeout(self):
        return self._timeout
    
    @timeout.setter    
    def timeout(self, value):
        self._timeout=int(value)
          
    @property        
    def num_samples(self):
        return self._num_samples

    @num_samples.setter
    def num_samples(self, value):
        if value*self.avgs_per_trig> self.BUFFER_SIZE:
            raise Exception('The total number of samples exceeds the buffer size')
        self._num_samples=int(value)
        self.prep_captmem()
        self.prep_buffer()

    @property        
    def avgs_per_trig(self):
        return self._avgs_per_trig

    @avgs_per_trig.setter
    def avgs_per_trig(self, value):
        if value*self.num_samples> self.BUFFER_SIZE:
            raise Exception('The total number of samples exceeds the buffer size')
        self._avgs_per_trig=int(value)
        self.prep_captmem()
        self.prep_buffer()


    is_active=pp('IsActive', prefix=bool, set_suffix=None)
    reference_locked=pp('LO_ReferenceLocked', prefix=bool, set_suffix=None)
    LO_position=pp("RF_LOPosition", prefix="lop") #Below, Above
    ADC_overload=pp("Capture_IQ_ADCOverload", prefix=bool, set_suffix=None)

    sample_rate=pp('Modulation_GenericSamplingFrequency', dtype=c_double)
    modulation_mode=pp('Modulation_Mode', prefix='mm') #Generic
    LO_reference=pp('LO_Reference', prefix='lorm') #OXCO
    input_level=pp('RF_RFInputLevel', dtype=c_double)
    frequency=pp('RF_CentreFrequency', dtype=c_double)

    trigger_source=pp('Trigger_Source', prefix='ts')
    edge_gate_polarity=pp('Trigger_EdgeGatePolarity')
    pre_edge_trigger_samples=pp('Trigger_PreEdgeTriggerSamples', coercer=int)
    sw_trigger_mode=pp('Trigger_SwTriggerMode', prefix='swt') #Immediate, Armed
    reclaim_timeout=pp('Capture_IQ_ReclaimTimeout', coercer=int)
    pipelining_enable=pp("Capture_PipeliningEnable", prefix=bool)
    dc_offset_remove=pp("RF_RemoveDCOffset", prefix=bool)

    int_trig_source=pp("Trigger_IntTriggerSource", prefix="its")
    int_trig_abs_threshold=pp("Trigger_IntTriggerAbsThreshold", dtype=c_double)

    timer_advance=pp("Timer_Advance", dtype=c_ulong)
    timer_period=pp("Timer_Period", dtype=c_double)

    def get_abs_sample_time(self, ind=0):
        return self.get_func("Capture_IQ_GetAbsSampleTime", ind, dtype=c_double)

    def get_sample_captured(self, ind=0):
        return self.get_func("Capture_IQ_GetSampleCaptured", ind, prefix=bool)

    trigger_detected=pp("Capture_IQ_TriggerDetected", set_suffix=None, coercer=bool)

    def start_dig(self, lo_address='3011D1', dig_address='3036D1', plugin=False, modulation_mode="Generic", lo_reference="OCXO"):
        """boots the digitizer, doing some minor setting for basic operation"""
        self.address=dig_address
        self.lo_address=lo_address
        self.do_func("ClearErrors")
        self.do_func("BootInstrument", lo_address, dig_address, plugin)
        self.modulation_mode=modulation_mode
        self.LO_reference=lo_reference
        self.sw_trigger_mode="Armed"

    level_correction=pp('RF_LevelCorrection', dtype=c_double, set_suffix=None)

    @property
    def lc(self):
        """cached level correction. set lc to None to reset"""
        if getattr(self, '_lc', None) is None:
            self._lc=self.level_correction
        return self._lc

    @lc.setter
    def lc(self, value):
        self._lc=value

    def prep_buffer(self):
        self.i_buffer = empty(self.total_samples, dtype=c_float)
        self.q_buffer = empty(self.total_samples, dtype=c_float)
        i_ctypes = self.i_buffer.ctypes.data_as(POINTER(c_float))
        q_ctypes = self.q_buffer.ctypes.data_as(POINTER(c_float))
        self.buffer_ref = afDigitizerBufferIQ_t(i_ctypes, q_ctypes, self.total_samples)
        self.buffer_ref_pointer = pointer(self.buffer_ref)
        #self.capture_ref = c_long()
        self.capture_ref=[c_long() for avgidx in range(int(self.num_trigs))]
        
    def buffer_capture(self):     
        start_idx=self.start_idx
        total_samples=self.total_samples
        avgs=self.avgs_per_trig
        samples=self.num_samples
        num_trigs=int(self.num_trigs)
        i_avgd = zeros(samples)
        q_avgd = zeros(samples)
        for avgidx in range(1+start_idx):
            self.do_func('Capture_IQ_IssueBuffer', byref(self.buffer_ref), self.timeout, byref(self.capture_ref[avgidx]))
        for avgidx in range(num_trigs):
            self.do_func('Capture_IQ_ReclaimBuffer', self.capture_ref[avgidx], byref(self.buffer_ref_pointer))
            if not self.buffer_ref_pointer:
                raise Exception("No buffer ref pointer!")
            if avgidx+start_idx < (num_trigs-1):
                self.do_func('Capture_IQ_IssueBuffer', byref(self.buffer_ref), self.timeout, byref(self.capture_ref[avgidx+start_idx+1]))
            i_avgd += mean(self.i_buffer[:total_samples].reshape(avgs, samples), axis=0)
            q_avgd += mean(self.q_buffer[:total_samples].reshape(avgs, samples), axis=0)
        i_avgd = i_avgd/self.num_trigs
        q_avgd = q_avgd/self.num_trigs
        self.cpx_avgd=i_avgd + 1j*q_avgd
        return self.cpx_avgd

    def get_trace(self, points=1000, timeout=10000):
        """uses issue buffer, reclaim buffer time data collection"""
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

    def stop_dig(self):
        """closes the instrument and destroys the object"""
        self.do_func('CloseInstrument')
        self.do_func("DestroyObject")

    def trigger_arm(self, num_samples):
        """arms the trigger to capture 2*n samples"""
        self.do_func('Capture_IQ_TriggerArm', 2*num_samples)

    def captmem(self, total_samples):
        """performs captmem using internal num_samples, i_buffer, q_buffer. cal prep_captmem2 before calling this"""
        self.do_func("Capture_IQ_CaptMem", total_samples, byref(self.i_buf), byref(self.q_buf))

    def prep_captmem(self):
        """does internal prep of buffers"""
        typeBuffer=c_float*self.total_samples
        self.i_buf=typeBuffer()
        self.q_buf=typeBuffer()


    def captmem_from_offset(self, offset):
        """does captmem from offset with internal buffers"""
        self.do_func("Capture_IQ_GetCaptMemFromOffset", offset, self.total_samples, byref(self.i_buf), byref(self.q_buf))

    def full_captmem(self):
        """combines trigger arm with capture"""
        total_samples=self.total_samples
        self.trigger_arm(total_samples)
        samples=self.num_samples
        i_avgd = zeros(samples)
        q_avgd = zeros(samples)
        avgs=self.avgs_per_trig
        num_trigs=int(self.num_trigs)
        for avgidx in range(0, num_trigs):
            for i in range(10000):
                #print "no trig!"
                if self.trigger_detected:
                    break
            self.captmem(total_samples)
            if avgidx<num_trigs-1:
                self.trigger_arm(total_samples)
            i_avgd += mean(array(self.i_buf).reshape(avgs, samples), axis=0)
            q_avgd += mean(array(self.q_buf).reshape(avgs, samples), axis=0)
        i_avgd = i_avgd/self.num_trigs
        q_avgd = q_avgd/self.num_trigs
        self.cpx_avgd=i_avgd + 1j*q_avgd
        return self.cpx_avgd

    def calc_mean_power(self):
        """calculates mean power of level corrected stored data"""
        return 20*log10(mean(absolute(self.cpx_lc)))

    @property
    def cpx_lc(self):
        """returns the level corrected complex data using the cached level correction"""
        return self.cpx_avgd*power(10.0, self.lc/20.0)

    @property
    def fftd(self):
        """performs FFT on level corrected data for display"""
        fftd=20*log10(absolute(fft.fftshift(fft.fft(self.cpx_lc))))
        return fftd-fftd.max()+self.calc_mean_power()
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
    if 1:
        #d.get_func("Capture_IQ_GetAbsSampleTime", 1000, dtype=c_double)
        #d.get_func("Capture_IQ_GetSampleCaptured", 3000, prefix=bool)
        d=afDigitizer()
        d.start_dig()
        d.input_level=0.0
        d.sample_rate=250.0e6
        #print d.get_func("Trigger_Source_Get", prefix="ts")
        #print d.get_func('RF_CentreFrequency_Get', dtype=c_double)
        print d.get_func('Modulation_Mode_Get')
        print d.get_func('IsActive_Get')
        d.sw_trigger_mode='Armed'
    if 0:
        from afsiggen import afSigGen
        a=afSigGen()
        a.start()
        a.level=-30
        a.output=True
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
