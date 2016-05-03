import ctypes
from ctypes import c_int, c_long, c_float, c_double, c_ulong, POINTER, byref, create_string_buffer, pointer, Structure, c_void_p
from numpy import zeros, mean
BUFFER_SIZE = 20000000 

# open dll
_lib = ctypes.WinDLL('afDigitizerDll_32')

# define data types used by this dll
STRING = ctypes.c_char_p
AFBOOL = c_long
#afDigitizerInstance_t = c_long
#afDigitizerCaptureIQ_t = c_long

class afDigitizerBufferIQ_t(Structure):
    _fields_ = [
        ('iBuffer', POINTER(c_float)),
        ('qBuffer', POINTER(c_float)),
        ('samples', c_ulong),
        ('userData', c_void_p)]
    
class afDigitizer():
    """Represent a signal generator, redefines the dll function in python"""
    def do_func(self, sName, *args):
        error=getattr(_lib, "afDigitizerDll_"+sName)(self.session, *args)
        self.check_error(error)
        
    def get_func(self, sName, *args, **kwargs):
        dtype=kwargs.pop("dtype", c_long)
        dValue=dtype()
        self.do_func(sName, *(args+(byref(dValue),)))
        return dValue.value
        
    def create_object(self):
        ses=c_long()
        error=_lib.afDigitizerDll_CreateObject(byref(ses))
        self.session=ses.value
        self.check_error(error)

    def destroy_object(self):
        _lib.afDigitizerDll_DestroyObject(self.session)

    def boot_instrument(self, sLoResource, sRfResource, bLoIsPlugin=False):
        cLoResource = STRING(sLoResource)
        cRfResource = STRING(sRfResource)
        self.do_func("BootInstrument", cLoResource,
                               cRfResource, AFBOOL(bLoIsPlugin))
        return (cLoResource.value, cRfResource.value)

    def close_instrument(self, bCheckError=True):
        self.do_func("CloseInstrument")
            
    def lo_reference_set(self, lLORef):
        """Modes are [lormOCXO=0, lormInternal=1, lormExternalDaisy=2, lormExternalTerminated=3]"""
        self.do_func('LO_Reference_Set', lLORef)
        
    def lo_reference_get(self):
        """Modes are [lormOCXO=0, lormInternal=1, lormExternalDaisy=2, lormExternalTerminated=3]"""
        return self.get_func('LO_Reference_Get', dtype=c_long)

    def ref_is_locked(self):
        #Returns whether LO is locked to the external 10 Mhz reference when 
        #Reference is set to ExternalDaisy or ExternalTerminated.
        return self.get_func('LO_ReferenceLocked_Get')
 
    def rf_centre_frequency_set(self, dFreq):
        self.do_func('RF_CentreFrequency_Set', c_double(dFreq))

    def rf_centre_frequency_get(self):
        return self.get_func('RF_CentreFrequency_Get', dtype=c_double)

    def rf_rf_input_level_set(self, dValue):
        self.do_func('RF_RFInputLevel_Set', c_double(dValue))

    def rf_rf_input_level_get(self):
        return self.get_func('RF_RFInputLevel_Get', dtype=c_double)

    def modulation_generic_sampling_frequency_set(self, dValue):
        self.do_func('Modulation_GenericSamplingFrequency_Set', c_double(dValue))

    def modulation_generic_sampling_frequency_get(self):
        dValue=c_double()
        self.do_func('Modulation_GenericSamplingFrequency_Get', byref(dValue))
        return dValue.value

    def rf_remove_dc_offset_set(self, bOn=True):
        self.do_func('RF_RemoveDCOffset_Set', AFBOOL(bOn))

    def rf_remove_dc_offset_get(self):
        return bool(self.get_func('RF_RemoveDCOffset_Get'))

    def capture_iq_capt_mem(self, nSamples):
        nSamples = int(nSamples)
        typeBuffer = c_float*nSamples
        lValueI = typeBuffer()
        lValueQ = typeBuffer()
        self.do_func('Capture_IQ_CaptMem', c_ulong(nSamples), byref(lValueI), byref(lValueQ))
        return (list(lValueI), list(lValueQ))

    def trigger_source_set(self, iOption=0):
        """Options for the trigger source are found in the .ini file for the digitizer
        Sources are
        [PXI_TRIG_0=0, PXI_TRIG_1=1, PXI_TRIG_2=2, PXI_TRIG_3=3, PXI_TRIG_4=4, PXI_TRIG_5=5,
        PXI_TRIG_6=6, PXI_TRIG_7=7, PXI_STAR=8, PXI_LBL_0=9, PXI_LBL_1=10, PXI_LBL_2=11, 
        PXI_LBL_3=12, PXI_LBL_4=13, PXI_LBL_5=14, PXI_LBL_6=15, PXI_LBL_7=16, PXI_LBL_8=17,
        PXI_LBL_9=18, PXI_LBL_10=19, PXI_LBL_11=20, PXI_LBL_12=21, LVDS_MARKER_0=22, LVDS_MARKER_1=23, 
        LVDS_MARKER_2=24, LVDS_MARKER_3=25, LVDS_AUX_0=26, LVDS_AUX_1=27, LVDS_AUX_2=28, LVDS_AUX_3=29,
        LVDS_AUX_4=30, LVDS_SPARE_0=31, SW_TRIG=32, LVDS_MARKER_4=33, INT_TIMER=34, INT_TRIG=35, FRONT_SMB=36]"""
        self.do_func('Trigger_Source_Set', iOption)

    def trigger_source_get(self):
        """Options for the trigger source are found in the .ini file for the digitizer
        Sources are
        [PXI_TRIG_0=0, PXI_TRIG_1=1, PXI_TRIG_2=2, PXI_TRIG_3=3, PXI_TRIG_4=4, PXI_TRIG_5=5,
        PXI_TRIG_6=6, PXI_TRIG_7=7, PXI_STAR=8, PXI_LBL_0=9, PXI_LBL_1=10, PXI_LBL_2=11, 
        PXI_LBL_3=12, PXI_LBL_4=13, PXI_LBL_5=14, PXI_LBL_6=15, PXI_LBL_7=16, PXI_LBL_8=17,
        PXI_LBL_9=18, PXI_LBL_10=19, PXI_LBL_11=20, PXI_LBL_12=21, LVDS_MARKER_0=22, LVDS_MARKER_1=23, 
        LVDS_MARKER_2=24, LVDS_MARKER_3=25, LVDS_AUX_0=26, LVDS_AUX_1=27, LVDS_AUX_2=28, LVDS_AUX_3=29,
        LVDS_AUX_4=30, LVDS_SPARE_0=31, SW_TRIG=32, LVDS_MARKER_4=33, INT_TIMER=34, INT_TRIG=35, FRONT_SMB=36]"""
        return self.get_func('Trigger_Source_Get')

    def modulation_mode_set(self, iOption=0):
        """Modes are [mmUMTS=0, mmGSM=1, mmCDMA20001x=2, mmEmu2319=4, mmGeneric=5]"""
        self.do_func('Modulation_Mode_Set', iOption)

    def modulation_mode_get(self):
        """Modes are [mmUMTS=0, mmGSM=1, mmCDMA20001x=2, mmEmu2319=4, mmGeneric=5]"""
        return self.get_func('Modulation_Mode_Get', dtype=c_int)

    #Added 2014-02-22 by Philip    
    #Detects whether Whether a trigger event has occurred after arming the 
    #AF3070 trigger with the afRfDigitizerDll_Trigger_Arm method. Read-only
    def trigger_detected_get(self):
        return bool(self.get_func('Trigger_Detected_Get'))

    def trigger_polarity_set(self, iOption=0):
        """Modes are [Positive=0, Negative=1]"""
        self.do_func('Trigger_EdgeGatePolarity_Set', iOption)
        
    def trigger_polarity_get(self):
        """Modes are [Positive=0, Negative=1]"""
        return self.get_func('Trigger_EdgeGatePolarity_Get', dtype=c_int)
 
    def trigger_type_set(self, iOption=0):
        """Modes are [Edge=0, Gate=1]"""
        self.do_func('Trigger_TType_Set', iOption)
        
    def trigger_type_get(self):
        """Modes are [Positive=0, Negative=1]"""
        self.get_func('Trigger_TType_Get', dtype=c_int)
 
    def trigger_arm_set(self, inSamples=0):
        self.do_func('Trigger_Arm', inSamples)

    def data_capture_complete_get(self):
        return bool(self.get_func('Capture_IQ_CaptComplete_Get'))
 
    def error_message_get(self):
        msgBuffer=create_string_buffer(256)
        _lib.afDigitizerDll_ErrorMessage_Get(self.session, msgBuffer, 256)
        return msgBuffer.value

    def clear_errors(self):
        _lib.afDigitizerDll_ClearErrors(self.session)
        
    def check_error(self, error=0):
        """If error occurred, get error message and raise error"""
        if error>0:
            self.clear_errors()
        if error<0:
            raise Exception(str(error)+": "+self.error_message_get())
            
    def rf_level_correction_get(self):
        return self.get_func('RF_LevelCorrection_Get', dtype=c_double)
        
    def trigger_pre_edge_trigger_samples_get(self):
        return self.get_func('Trigger_PreEdgeTriggerSamples_Get', dtype=c_ulong)
        
    def trigger_pre_edge_trigger_samples_set(self, preEdgeTriggerSamples):
        self.do_func('Trigger_PreEdgeTriggerSamples_Set', c_ulong(preEdgeTriggerSamples))
        
    #def trigger_IQ_bandwidth_set(self, dBandWidth, iOption=0):
    #    self.do_func('Trigger_SetIntIQTriggerDigitalBandwidth', c_double(dBandWidth), c_int(iOption), byref(dValue))
    #    self.check_error(error)
    #    return dValue.value
 
    def check_ADCOverload(self):
        return bool(self.get_func('Capture_IQ_ADCOverload_Get'))
        
    def rf_userLOPosition_get(self):
        return self.get_func('RF_UserLOPosition_Get')
        
    def rf_userLOPosition_set(self, iLOPosition):
        self.do_func('RF_UserLOPosition_Set', iLOPosition)

    def capture_iq_reclaim_timeout_set(self, timeoutMillisecs=1000):
        self.do_func('Capture_IQ_ReclaimTimeout_Set', timeoutMillisecs)
    
    def capture_iq_reclaim_timeout_get(self):
        return self.get_func('Capture_IQ_ReclaimTimeout_Get') 
    
    def capture_iq_issue_buffer(self, buffer_ref, capture_ref, timeout=1):
        self.do_func('Capture_IQ_IssueBuffer',
                     byref(buffer_ref), 1000*timeout, byref(capture_ref))
                     
    def capture_iq_reclaim_buffer(self, capture_ref, buffer_ref_pointer):
        self.do_func('Capture_IQ_ReclaimBuffer', capture_ref, byref(buffer_ref_pointer))

    def capture_to_buffer(self, samples=1000, avgs=1, timeout=10, nTriggers=1):
        print self.check_ADCOverload()
        i_avgd = zeros(samples)
        q_avgd = zeros(samples)
        #samples=self.nSamples
        #avgs=self.nAverages_per_trigger
        #timeout=self.fTimeout
        tot_samps=int(samples*avgs)
        capture_ref=[c_long() for avgidx in range(nTriggers)]
        #buffer_ref=range(self.nTriggers)
        #buffer_ref_pointer=range(self.nTriggers)
        #i_buffer=range(self.nTriggers)
        #q_buffer=range(self.nTriggers)
        i_buffer = zeros(tot_samps, dtype=c_float)
        q_buffer = zeros(tot_samps, dtype=c_float)
        i_ctypes = i_buffer.ctypes.data_as(POINTER(c_float))
        q_ctypes = q_buffer.ctypes.data_as(POINTER(c_float))
        buffer_ref = afDigitizerBufferIQ_t(i_ctypes, q_ctypes, tot_samps)
        buffer_ref_pointer = pointer(buffer_ref)

        start_idx=nTriggers-1
        #self.log("acq started")
        for avgidx in range(1+start_idx):#self.nTriggers):
            #self.log(avgidx)
            self.capture_iq_issue_buffer(buffer_ref=buffer_ref, capture_ref=capture_ref[avgidx], 
                                               timeout = timeout)

        for avgidx in range(nTriggers):
            self.capture_iq_reclaim_buffer(capture_ref=capture_ref[avgidx],
                                                     buffer_ref_pointer=buffer_ref_pointer)
            if avgidx+start_idx < (nTriggers-1):
                self.capture_iq_issue_buffer(buffer_ref=buffer_ref, capture_ref=capture_ref[avgidx+start_idx+1], 
                                               timeout = timeout)
                                                     
            if buffer_ref_pointer:
                #self.log("BUFFER POINTER OK - Trigger {}".format(avgidx))
                total_samples = buffer_ref.samples
            else:
                #self.log("NO BUFFER!", 30)
                samples = 0
                
            i_avgd += mean(i_buffer[:total_samples].reshape(avgs, samples), axis=0)
            q_avgd += mean(q_buffer[:total_samples].reshape(avgs, samples), axis=0)
        #self.log("acq stopped")                
        i_avgd = i_avgd/nTriggers
        q_avgd = q_avgd/nTriggers
        cpx_avgd = i_avgd + 1j*q_avgd
        #self.log((avgs, samples))
        #self.log(i_buffer.reshape(avgs, samples).shape)
        #ibuf= np.mean(i_buffer.reshape(avgs, samples), axis=0)
        #qbuf= np.mean(q_buffer.reshape(avgs, samples), axis=0)
        #ibuf= i_buffer.reshape(avgs, samples)[:, 130]#, axis=0)
        #qbuf= q_buffer.reshape(avgs, samples)[:, 130]

        #cpx_buffer=i_buffer+1j*q_buffer
        #return cpx_buffer
        return cpx_avgd
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from numpy import log10, absolute, power
    # test driver
    d = afDigitizer()
    d.create_object()
    d.clear_errors()
    #Digitizer.boot_instrument('PXI8::15::INSTR', 'PXI8::14::INSTR')
    d.boot_instrument('3011D1', '3036D1')
    print d.modulation_mode_get()
    d.modulation_mode_set(5)
    print d.modulation_mode_get()
    d.lo_reference_set(0)
    d.rf_rf_input_level_set(-20)
    lc=d.rf_level_correction_get()
    dFreq = d.modulation_generic_sampling_frequency_get()
    print 'Current frequency: ' + str(dFreq)
    d.modulation_generic_sampling_frequency_set(250E6)
    dFreq = d.modulation_generic_sampling_frequency_get()
    print 'Current frequency: ' + str(dFreq)
    #[lI, lQ] = Digitizer.capture_iq_capt_mem(2048)
    cpx_avgd=d.capture_to_buffer()
    plt.plot(20*log10(absolute(cpx_avgd*power(10.0, lc/20.0))))
    plt.show()
#    print lI, lQ
    if 0:
        d.close_instrument()
        d.destroy_object()