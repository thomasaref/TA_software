from ctypes import c_char_p, WinDLL, c_long, byref, Structure, c_float, POINTER, c_ulong,\
    c_void_p, create_string_buffer, c_int, c_double, pointer, c_ushort
from numpy import linspace, zeros, mean, absolute, angle, log10
import time
STRING = c_char_p
_lib = WinDLL('afDigitizerDll_32')
AFBOOL = c_long
afDigitizerInstance_t = c_long
afDigitizerCaptureIQ_t = c_long

TrueFalse={True : -1, False : 0}

class afDigitizerBufferIQ_t(Structure): #Mirrors a struct in C
    _fields_ = [('iBuffer', POINTER(c_float)),
                ('qBuffer', POINTER(c_float)),
                ('samples', c_ulong),
                ('userData', c_void_p),]

def getDllFunc(name, argtypes=[afDigitizerInstance_t], restype=c_long):
    """Create a dll function with given input and output types"""
    obj = getattr(_lib, name)
    obj.restype = restype
    obj.argypes = argtypes
    return obj

#constants:
#lo_resource_name="PXI3::10::INSTR"
#dig_resource_name="PXI4::15::INSTR"
#class afDigitizer:
#session = afDigitizerInstance_t()

def get_error(session, errorcode):
    if errorcode:
        print "CODE: ", errorcode
        errorDescriptionBufferSize = 512
        errorDescription = create_string_buffer(errorDescriptionBufferSize)
        ErrorMessage_Get = getDllFunc('afDigitizerDll_ErrorMessage_Get',
                                argtypes = [afDigitizerInstance_t, c_char_p, c_long])
        ErrorMessage_Get(session, errorDescription, errorDescriptionBufferSize)
        if errorcode <0:
            raise Exception(errorDescription.value)
        else:
            print "Warning: %s"%errorDescription.value

def callDllFunc(instr, *args, **kwargs):
    if 'Dllname' in kwargs.keys():
        #assumes kwargs contains Dllname and argtypes
        if 'valtype' in kwargs.keys():
            tempvalue=kwargs['valtype']()
            args=args+(byref(tempvalue),)
       # self.update_cmd("afDig call: {0}".format(kwargs['Dllname']))
        if 'argtypes' not in kwargs.keys():
            kwargs['argtypes']=[afDigitizerInstance_t]
        obj=getDllFunc(name=kwargs['Dllname'], argtypes=kwargs['argtypes'])
        if args==():
            args=(instr.session,)
        error=obj(*args)
        get_error(instr.session, error)
        if 'valtype' in kwargs.keys():
            return tempvalue.value
    else:
        #assumes set/get function with order self, Dllname, valtype
        Dllname=args[0]
        valtype=args[1]
        if Dllname[-3:]=='Set':
           # self.update_cmd("afDig SET: {0}".format(Dllname))
            obj=getDllFunc(name=Dllname, argtypes=[afDigitizerInstance_t, valtype])
            value=args[2]
            error=obj(instr.session, valtype(value))
            get_error(instr.session, error)
        elif Dllname[-3:]=='Get':
            #self.update_cmd("afDig GET: {0}".format(Dllname))
            obj = getDllFunc(name=Dllname, argtypes=[afDigitizerInstance_t, POINTER(valtype)])
            dValue = valtype()
            error = obj(instr.session, byref(dValue))
            get_error(instr.session, error)
            return dValue.value
        else:
            print "Bad Dllname! Doesn't end in Set or Get!"


def EepromCacheEnable_Set(instr, EepromCacheEnable):
    callDllFunc(instr, 'afDigitizerDll_EepromCacheEnable_Set', AFBOOL, EepromCacheEnable)
def EepromCacheEnable_Get(self):
    return callDllFunc(self, 'afDigitizerDll_EepromCacheEnable_Get', AFBOOL)

#def EepromCachePathLength_Get(self):
#    callDllFunc(self, 'afDigitizerDll_EepromCachePathLength_Get', c_long)

#def EepromCachePath_Get(self):
#    callDllFunc(self, 'afDigitizerDll_EepromCachePath_Get', c_long)
#def EepromCachePath_Set(self):
#    callDllFunc(self, 'afDigitizerDll_EepromCachePath_Set', c_char_p)

def CreateObject(instr):
    callDllFunc(instr, byref(instr.session),
        Dllname='afDigitizerDll_CreateObject',
        argtypes=[POINTER(afDigitizerInstance_t)])

def DestroyObject(instr):
    callDllFunc(instr, Dllname='afDigitizerDll_DestroyObject')

def BootInstrument(instr, LoResource, RfResource, LoIsPlugin=False):
    callDllFunc(instr, instr.session, str(LoResource), str(RfResource), LoIsPlugin,
        Dllname='afDigitizerDll_BootInstrument',
        argtypes=[afDigitizerInstance_t, c_char_p, c_char_p, AFBOOL])

def CloseInstrument(instr):
    callDllFunc(instr, Dllname='afDigitizerDll_CloseInstrument')

def ClearErrors(instr):
    callDllFunc(instr, Dllname='afDigitizerDll_ClearErrors')

def GetVersion(instr):
    blah=callDllFunc(instr, Dllname='afDigitizerDll_GetVersion',
                    argtypes=[POINTER(c_long)], valtype=c_long)
    print blah
    return blah
    #self.update_log('Get Version')


def Capture_IQ_ADCOverload_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_IQ_ADCOverload_Get', AFBOOL)

def Capture_IQ_CaptComplete_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_IQ_CaptComplete_Get', AFBOOL)

def Capture_IQ_CapturedSampleCount_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_IQ_CapturedSampleCount_Get', c_ulong)

#def Capture_IQ_EventHandler_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IQ_EventHandler_Set', afDigitizerCaptureIQEventHandler_t)
#def Capture_IQ_EventHandler_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IQ_EventHandler_Get', afDigitizerCaptureIQEventHandler_t)

def Capture_IQ_ListAddrCount_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_IQ_ListAddrCount_Get', c_ulong)

def Capture_IQ_ReclaimTimeout_Set(instr, Capture_IQ_ReclaimTimeout):
    callDllFunc(instr, 'afDigitizerDll_Capture_IQ_ReclaimTimeout_Set', c_long, Capture_IQ_ReclaimTimeout)
def Capture_IQ_ReclaimTimeout_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_IQ_ReclaimTimeout_Get', c_long)

afDigitizerDll_iqrIQResolution_t = {'16Bit' : 0, 'Auto' : 1}
def Capture_IQ_Resolution_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_IQ_Resolution_Get', c_int)
def Capture_IQ_Resolution_Set(instr, Capture_IQ_Resolution):
    callDllFunc(instr, 'afDigitizerDll_Capture_IQ_Resolution_Set', c_int, Capture_IQ_Resolution)

def Capture_IQ_TriggerCount_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_IQ_TriggerCount_Get', c_ulong)

def Capture_IQ_TriggerDetected_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_IQ_TriggerDetected_Get', AFBOOL)

def Capture_IQ_Abort(instr):
    callDllFunc(instr, Dllname='afDigitizerDll_Capture_IQ_Abort')
    #self.update_log('Capture IQ Abort')

def Capture_IQ_Cancel(instr, capture_ref):
    callDllFunc(instr, instr.session, capture_ref,
        Dllname='afDigitizerDll_Capture_IQ_Cancel',
        argtypes=[afDigitizerInstance_t, afDigitizerCaptureIQ_t])

def Capture_IQ_CaptMem(instr, numberOfIQSamples, iBuffer, qBuffer):
    callDllFunc(instr, instr.session, numberOfIQSamples, iBuffer, qBuffer,
        Dllname='afDigitizerDll_Capture_IQ_CaptMem',
        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(c_float), POINTER(c_float)])

def Capture_IQ_CaptMemWithKey(instr, numberOfIQSamples, iBuffer, qBuffer, tag, key):
    callDllFunc(instr, instr.session, numberOfIQSamples, iBuffer, qBuffer, tag, key,
        Dllname='afDigitizerDll_Capture_IQ_CaptMemWithKey',
        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(c_float), POINTER(c_float), POINTER(c_double), POINTER(c_double)])

def Capture_IQ_GetAbsSampleTime(instr, sampleNumber):
    return callDllFunc(instr, instr.session, sampleNumber,
        Dllname='afDigitizerDll_Capture_IQ_GetAbsSampleTime',
        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(c_double)], valtype=c_double)

def Capture_IQ_GetCaptMemFromOffset(instr, offset, numberOfIQSamples, iBuffer, qBuffer):
    callDllFunc(instr, instr.session, offset, numberOfIQSamples, iBuffer, qBuffer,
        Dllname='afDigitizerDll_Capture_IQ_GetCaptMemFromOffset',
        argtypes=[afDigitizerInstance_t, c_ulong, c_ulong, POINTER(c_float), POINTER(c_float)])

def Capture_IQ_GetCaptMemFromOffsetWithKey(instr, offset, numberOfIQSamples, iBuffer, qBuffer, tag, key):
    callDllFunc(instr, instr.session, offset, numberOfIQSamples, iBuffer, qBuffer, tag, key,
        Dllname='afDigitizerDll_Capture_IQ_GetCaptMemFromOffsetWithKey',
        argtypes=[afDigitizerInstance_t, c_ulong, c_ulong, POINTER(c_float), POINTER(c_float), POINTER(c_double), POINTER(c_double)])

#def Capture_IQ_GetListAddrInfo(self, listEvent, byref(*pListAddr), byref(*pStartSample), byref(*pNumSamples), byref(*pInvalidSamples)):
#    callDllFunc(self, self.instr.sesson, listEvent, byref(*pListAddr), byref(*pStartSample), byref(*pNumSamples), byref(*pInvalidSamples),
#        Dllname='afDigitizerDll_Capture_IQ_GetListAddrInfo',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(), POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)])
#    self.update_log('Capture_IQ_GetListAddrInfo')

#def Capture_IQ_GetOutstandingBuffers(self, pCount, pCompleted):
#    callDllFunc(self, self.instr.sesson, pCount, pCompleted,
#         Dllname='afDigitizerDll_Capture_IQ_GetOutstandingBuffers',
#         argtypes=[afDigitizerInstance_t, POINTER(c_ulong), POINTER(c_ulong)])
#    self.update_log('Capture_IQ_GetOutstandingBuffers')
##
#def Capture_IQ_GetTriggerSampleNumber(self, triggerNumber, byref(*pSampleNumber)):
#    callDllFunc(self, self.instr.sesson, triggerNumber, byref(*pSampleNumber),
#        Dllname='afDigitizerDll_Capture_IQ_GetTriggerSampleNumber',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(c_ulong)])

def Capture_IQ_IssueBuffer(instr, buffer_ref, timeoutMillisecs, capture_ref):
    callDllFunc(instr, instr.session, byref(buffer_ref), timeoutMillisecs, byref(capture_ref),
        Dllname='afDigitizerDll_Capture_IQ_IssueBuffer',
        argtypes=[afDigitizerInstance_t, POINTER(afDigitizerBufferIQ_t), c_long, POINTER(afDigitizerCaptureIQ_t)])

def Capture_IQ_ReclaimBuffer(instr, capture_ref, buffer_ref_pointer):
    callDllFunc(instr, instr.session, capture_ref, byref(buffer_ref_pointer),
        Dllname='afDigitizerDll_Capture_IQ_ReclaimBuffer',
        argtypes=[afDigitizerInstance_t, afDigitizerCaptureIQ_t, POINTER(POINTER(afDigitizerBufferIQ_t))])

#def Capture_IQ_ReclaimBufferWithKey(self, capture, byref(**pBuffer), byref(tag), byref(key)):
#    callDllFunc(self, self.instr.sesson, capture, byref(**pBuffer), byref(tag), byref(key),
#        Dllname='afDigitizerDll_Capture_IQ_ReclaimBufferWithKey',
#        argtypes=[afDigitizerInstance_t, , POINTER(), POINTER(c_double), POINTER(c_double)])
#    self.update_log('Capture_IQ_ReclaimBufferWithKey')
#
#def Capture_IQ_GetBufferKey(self, capture, byref(tag), byref(key)):
#    callDllFunc(self, self.instr.sesson, capture, byref(tag), byref(key),
#        Dllname='afDigitizerDll_Capture_IQ_GetBufferKey',
#        argtypes=[afDigitizerInstance_t, , POINTER(c_double), POINTER(c_double)])
#    self.update_log('Capture_IQ_GetBufferKey')

def Capture_IQ_TriggerArm(instr, samples):
    callDllFunc(instr, instr.session, samples,
        Dllname='afDigitizerDll_Capture_IQ_TriggerArm',
        argtypes=[afDigitizerInstance_t, c_ulong])

#def Capture_IQ_GetSampleCaptured(self, sampleNumber, byref(*pSampleCaptured)):
#    callDllFunc(self, self.instr.sesson, sampleNumber, byref(*pSampleCaptured),
#        Dllname='afDigitizerDll_Capture_IQ_GetSampleCaptured',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(AFBOOL)])
#    self.update_log('Capture_IQ_GetSampleCaptured')

#def Capture_IQ_Power_IsAvailable_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IQ_Power_IsAvailable_Get', AFBOOL)
#
#def Capture_IQ_Power_NumOfSteps_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IQ_Power_NumOfSteps_Set', c_long)
#
#def Capture_IQ_Power_NumOfSteps_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IQ_Power_NumOfSteps_Get', c_long)
#
#def Capture_IQ_Power_NumMeasurementsAvail_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IQ_Power_NumMeasurementsAvail_Get', c_long)
#
#def Capture_IQ_Power_SetParameters(self, stepLength, measOffset, measLength):
#    callDllFunc(self, self.instr.sesson, stepLength, measOffset, measLength,
#        Dllname='afDigitizerDll_Capture_IQ_Power_SetParameters',
#        argtypes=[afDigitizerInstance_t, c_long, c_long, c_long])
#    self.update_log('Capture_IQ_Power_SetParameters')
#
#def Capture_IQ_Power_GetParameters(self, byref(pStepLength), byref(pMeasOffset), byref(pMeasLength)):
#    callDllFunc(self, self.instr.sesson, byref(pStepLength), byref(pMeasOffset), byref(pMeasLength),
#        Dllname='afDigitizerDll_Capture_IQ_Power_GetParameters',
#        argtypes=[afDigitizerInstance_t, POINTER(c_long), POINTER(c_long), POINTER(c_long)])
#    self.update_log('Capture_IQ_Power_GetParameters')
#
#def Capture_IQ_Power_GetAllMeasurements(self, numMeasurements, byref(powers)):
#    callDllFunc(self, self.instr.sesson, numMeasurements, byref(powers),
#        Dllname='afDigitizerDll_Capture_IQ_Power_GetAllMeasurements',
#        argtypes=[afDigitizerInstance_t, c_long, POINTER(c_double)])
#    self.update_log('Capture_IQ_Power_GetAllMeasurements')
#
#def Capture_IQ_Power_GetSingleMeasurement(self, step, byref(pPower)):
#    callDllFunc(self, self.instr.sesson, step, byref(pPower),
#        Dllname='afDigitizerDll_Capture_IQ_Power_GetSingleMeasurement',
#        argtypes=[afDigitizerInstance_t, c_long, POINTER(c_double)])
#    self.update_log('Capture_IQ_Power_GetSingleMeasurement')


afDigitizerDll_sdtSampleDataType_t = {'IFData' : 0, 'IQData' : 1}
def Capture_SampleDataType_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_SampleDataType_Get', c_int)
def Capture_SampleDataType_Set(instr, Capture_SampleDataType):
    callDllFunc(instr, 'afDigitizerDll_Capture_SampleDataType_Set', c_int, Capture_SampleDataType)

def Capture_PipeliningEnable_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_PipeliningEnable_Get', AFBOOL)
def Capture_PipeliningEnable_Set(instr, Capture_PipeliningEnable):
    callDllFunc(instr, 'afDigitizerDll_Capture_PipeliningEnable_Set', AFBOOL, Capture_PipeliningEnable)

afDigitizerDll_ctmCaptureTimeoutMode_t = {'Auto' : 0, 'User' : 1}
def Capture_TimeoutMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_TimeoutMode_Get', c_int)
def Capture_TimeoutMode_Set(instr, Capture_TimeoutMode):
    callDllFunc(instr, 'afDigitizerDll_Capture_TimeoutMode_Set', c_int, Capture_TimeoutMode)

def Capture_UserTimeout_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Capture_UserTimeout_Get', c_ulong)
def Capture_UserTimeout_Set(instr, Capture_UserTimeout):
    callDllFunc(instr, 'afDigitizerDll_Capture_UserTimeout_Set', c_ulong, Capture_UserTimeout)

afDigitizerDll_lormReferenceMode_t = {'OCXO' : 0, 'Internal' : 1, 'ExternalDaisy' : 2, 'ExternalTerminated' : 3}
def LO_Reference_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LO_Reference_Get', c_int)
def LO_Reference_Set(instr, LO_Reference):
    callDllFunc(instr, 'afDigitizerDll_LO_Reference_Set', c_int, LO_Reference)

def LO_ReferenceLocked_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LO_ReferenceLocked_Get', AFBOOL)

afDigitizerDll_lolbLoopBandwidth_t = {'Normal' : 0, 'Narrow' : 1, 'Unspecified' : 2}
def LO_LoopBandwidth_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LO_LoopBandwidth_Get', c_int)
def LO_LoopBandwidth_Set(instr, LO_LoopBandwidth):
    callDllFunc(instr, 'afDigitizerDll_LO_LoopBandwidth_Set', c_int, LO_LoopBandwidth)

def LO_Resource_Temperature_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LO_Resource_Temperature_Get', c_double)

afDigitizerDll_lotmTriggerMode_t = {'None' : 0, 'Advance' : 1, 'Toggle' : 2, 'Hop' : 3}
def LO_Trigger_Mode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LO_Trigger_Mode_Get', c_int)
def LO_Trigger_Mode_Set(instr, LO_Trigger_Mode):
    callDllFunc(instr, 'afDigitizerDll_LO_Trigger_Mode_Set', c_int, LO_Trigger_Mode)

def LO_Options_CheckFitted(instr, OptionNumber):
    callDllFunc(instr, instr.sesson, OptionNumber,
        Dllname='afDigitizerDll_LO_Options_CheckFitted',
        argtypes=[afDigitizerInstance_t, c_long, POINTER(AFBOOL)], valtype=AFBOOL)

afDigitizerDll_mmModulationMode_t = {'UMTS' : 0, 'GSM' : 1, 'CDMA20001x' : 2, 'Emu2319' : 4, 'Generic' : 5}
def Modulation_Mode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_Mode_Get', c_int)
def Modulation_Mode_Set(instr, Modulation_Mode):
    callDllFunc(instr, 'afDigitizerDll_Modulation_Mode_Set', c_int, Modulation_Mode)

def Modulation_DecimatedSamplingFrequency_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_DecimatedSamplingFrequency_Get', c_double)

def Modulation_UndecimatedSamplingFrequency_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_UndecimatedSamplingFrequency_Get', c_double)

def Modulation_GenericDecimationRatio_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_GenericDecimationRatio_Get', c_ulong)
def Modulation_GenericDecimationRatio_Set(instr, Modulation_GenericDecimationRatio):
    callDllFunc(instr, 'afDigitizerDll_Modulation_GenericDecimationRatio_Set', c_ulong, Modulation_GenericDecimationRatio)

def Modulation_GenericDecimationRatioMin_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_GenericDecimationRatioMin_Get', c_ulong)

def Modulation_GenericDecimationRatioMax_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_GenericDecimationRatioMax_Get', c_ulong)

def Modulation_GenericSamplingFrequency_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_GenericSamplingFrequency_Get', c_double)
def Modulation_GenericSamplingFrequency_Set(instr, Modulation_GenericSamplingFrequency):
    callDllFunc(instr, 'afDigitizerDll_Modulation_GenericSamplingFrequency_Set', c_double, Modulation_GenericSamplingFrequency)

def Modulation_GenericSamplingFrequencyMax_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_GenericSamplingFrequencyMax_Get', c_double)

def Modulation_GenericSamplingFrequencyMin_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_GenericSamplingFrequencyMin_Get', c_double)

def Modulation_GenericSamplingFreqNumerator_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_GenericSamplingFreqNumerator_Get', c_ulong)

def Modulation_GenericSamplingFreqDenominator_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Modulation_GenericSamplingFreqDenominator_Get', c_ulong)

def Modulation_SetGenericSamplingFreqRatio(instr, numerator, denominator):
    callDllFunc(instr, instr.sesson, numerator, denominator,
        Dllname='afDigitizerDll_Modulation_SetGenericSamplingFreqRatio',
        argtypes=[afDigitizerInstance_t, c_long, c_long])

afDigitizerDll_afmAutoFlatnessMode_t = {'Disable' : 0, 'Enable' : 1}
def RF_AutoFlatnessMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_AutoFlatnessMode_Get', c_int)
def RF_AutoFlatnessMode_Set(instr, RF_AutoFlatnessMode):
    callDllFunc(instr, 'afDigitizerDll_RF_AutoFlatnessMode_Set', c_int, RF_AutoFlatnessMode)

afDigitizerDll_atoAutoTemperatureOptimization_t = {'Disable' : 0, 'Enable' : 1}
def RF_AutoTemperatureOptimization_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_AutoTemperatureOptimization_Get', c_int)
def RF_AutoTemperatureOptimization_Set(instr, RF_AutoTemperatureOptimization):
    callDllFunc(instr, 'afDigitizerDll_RF_AutoTemperatureOptimization_Set', c_int, RF_AutoTemperatureOptimization)

def RF_CentreFrequency_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_CentreFrequency_Get', c_double)
def RF_CentreFrequency_Set(instr, RF_CentreFrequency):
    callDllFunc(instr, 'afDigitizerDll_RF_CentreFrequency_Set', c_double, RF_CentreFrequency)

afDigitizerDll_lopLOPosition_t = {'LO Below' : 0, 'LO Above' : 1}
def RF_SetCentreFrequencyAndLOPosition(instr, CenterFrequency, LOPosition):
    callDllFunc(instr, instr.sesson, CenterFrequency, LOPosition,
        Dllname='afDigitizerDll_RF_SetCentreFrequencyAndLOPosition',
        argtypes=[afDigitizerInstance_t, c_double, c_int])

def RF_CentreFrequencyLOAboveMax_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_CentreFrequencyLOAboveMax_Get', c_double)

def RF_CentreFrequencyLOBelowMin_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_CentreFrequencyLOBelowMin_Get', c_double)

def RF_CentreFrequencyMax_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_CentreFrequencyMax_Get', c_double)

def RF_CentreFrequencyMin_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_CentreFrequencyMin_Get', c_double)

def RF_CurrentChannel_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_CurrentChannel_Get', c_ushort)
def RF_CurrentChannel_Set(instr, RF_CurrentChannel):
    callDllFunc(instr, 'afDigitizerDll_RF_CurrentChannel_Set', c_ushort, RF_CurrentChannel)

def RF_DividedLOFrequency_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_DividedLOFrequency_Get', c_double)

afDigitizerDll_erExternalReference_t = {'Lock To 10MHz' : 0, 'Free Run' : 2}
def RF_ExternalReference_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_ExternalReference_Get', c_int)
def RF_ExternalReference_Set(instr, RF_ExternalReference):
    callDllFunc(instr, 'afDigitizerDll_RF_ExternalReference_Set', c_int, RF_ExternalReference)

afDigitizerDll_femFrontEndMode_t = {'Auto' : 0, 'AutoIF' : 1, 'Manual' : 2}
def RF_FrontEndMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_FrontEndMode_Get', c_int)
def RF_FrontEndMode_Set(instr, RF_FrontEndMode):
    callDllFunc(instr, 'afDigitizerDll_RF_FrontEndMode_Set', c_int, RF_FrontEndMode)

afDigitizerDll_isInputSource_t = {'IFInput' : 0, 'RFInput' : 1}
def RF_InputSource_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_InputSource_Get', c_int)
def RF_InputSource_Set(instr, RF_InputSource):
    callDllFunc(instr, 'afDigitizerDll_RF_InputSource_Set', c_int, RF_InputSource)

def RF_LevelCorrection_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_LevelCorrection_Get', c_double)

def RF_LOFrequency_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_LOFrequency_Get', c_double)

def RF_LOOffset_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_LOOffset_Get', c_double)

afDigitizerDll_lopLOPosition_t = {'LO Below' : 0, 'LO Above' : 1}
def RF_LOPosition_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_LOPosition_Get', c_int)
def RF_LOPosition_Set(instr, RF_LOPosition):
    callDllFunc(instr, 'afDigitizerDll_RF_LOPosition_Set', c_int, RF_LOPosition)
def RF_UserLOPosition_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_UserLOPosition_Get', c_int)
def RF_UserLOPosition_Set(instr, RF_UserLOPosition):
    callDllFunc(instr, 'afDigitizerDll_RF_UserLOPosition_Set', c_int, RF_UserLOPosition)
def RF_ActualLOPosition_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_ActualLOPosition_Get', c_int)

afDigitizerDll_lopmLOPositionMode_t = {'LO Manual' : 0, 'LO SemiAuto' : 1, 'LO Auto' : 2}
def RF_LOPositionMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_LOPositionMode_Get', c_int)
def RF_LOPositionMode_Set(instr, RF_LOPositionMode):
    callDllFunc(instr, 'afDigitizerDll_RF_LOPositionMode_Set', c_int, RF_LOPositionMode)

def RF_PreAmpEnable_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_PreAmpEnable_Get', AFBOOL)
def RF_PreAmpEnable_Set(instr, RF_PreAmpEnable):
    callDllFunc(instr, 'afDigitizerDll_RF_PreAmpEnable_Set', AFBOOL, RF_PreAmpEnable)

def RF_AutoPreAmpSelection_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_AutoPreAmpSelection_Get', AFBOOL)
def RF_AutoPreAmpSelection_Set(instr, RF_AutoPreAmpSelection):
    callDllFunc(instr, 'afDigitizerDll_RF_AutoPreAmpSelection_Set', AFBOOL, RF_AutoPreAmpSelection)

def RF_RemoveDCOffset_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_RemoveDCOffset_Get', AFBOOL)
def RF_RemoveDCOffset_Set(instr, RF_RemoveDCOffset):
    callDllFunc(instr, 'afDigitizerDll_RF_RemoveDCOffset_Set', AFBOOL, RF_RemoveDCOffset)

afDigitizerDll_rfrmReferenceMode_t = {'Internal' : 2, 'External Daisy' : 0, 'External PCI Backplane' : 1}
def RF_Reference_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_Reference_Get', c_int)
def RF_Reference_Set(instr, RF_Reference):
    callDllFunc(instr, 'afDigitizerDll_RF_Reference_Set', c_int, RF_Reference)

def RF_ReferenceLocked_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_ReferenceLocked_Get', AFBOOL)

def RF_RFAttenuation_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_RFAttenuation_Get', c_ulong)
def RF_RFAttenuation_Set(instr, RF_RFAttenuation):
    callDllFunc(instr, 'afDigitizerDll_RF_RFAttenuation_Set', c_ulong, RF_RFAttenuation)

def RF_RFAttenuationMax_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_RFAttenuationMax_Get', c_ulong)

def RF_RFAttenuationMin_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_RFAttenuationMin_Get', c_ulong)

def RF_RFAttenuationStep_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_RFAttenuationStep_Get', c_ulong)

def RF_RFInputLevel_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_RFInputLevel_Get', c_double)
def RF_RFInputLevel_Set(instr, RF_RFInputLevel):
    callDllFunc(instr, 'afDigitizerDll_RF_RFInputLevel_Set', c_double, RF_RFInputLevel)

def RF_RFInputLevelMax_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_RFInputLevelMax_Get', c_double)
def RF_RFInputLevelMin_Get(instr):
    callDllFunc(instr, 'afDigitizerDll_RF_RFInputLevelMin_Get', c_double)

def RF_SampleFrequency_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_SampleFrequency_Get', c_double)

def RF_DitherEnable_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_DitherEnable_Get', AFBOOL)
def RF_DitherEnable_Set(instr, RF_DitherEnable):
    callDllFunc(instr, 'afDigitizerDll_RF_DitherEnable_Set', AFBOOL, RF_DitherEnable)

def RF_DitherAvailable_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_DitherAvailable_Get', AFBOOL)

def RF_Resource_Temperature_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_Resource_Temperature_Get', c_double)

def RF_Routing_ScenarioListSize_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_RF_Routing_ScenarioListSize_Get', c_ulong)

def RF_OptimizeTemperatureCorrection(instr):
    callDllFunc(instr, Dllname='afDigitizerDll_RF_OptimizeTemperatureCorrection')

def RF_GetBandwidth (instr, centreFreq, span, flatness):
    return callDllFunc(instr, instr.sesson, centreFreq, span, flatness,
        Dllname='afDigitizerDll_RF_GetBandwidth ',
        argtypes=[afDigitizerInstance_t, c_double, c_double, c_int, POINTER(c_double)], valtype=c_double)

afDigitizerDll_lopLOPosition_t = {'LO Below' : 0, 'LO Above' : 1}
def RF_GetRecommendedLOPosition(instr, digitizerFreq, signalFreq):
    return callDllFunc(instr, instr.sesson, digitizerFreq, signalFreq,
        Dllname='afDigitizerDll_RF_GetRecommendedLOPosition',
        argtypes=[afDigitizerInstance_t, c_double, c_double, POINTER(c_int)], valtype=c_int)

#def RF_GetHighSensitivitySettings(self, rfFreq, peakLevel, byref(*pRFAttenuationHS), byref(*pIFAttenuationHS), byref(*pPreAmplifierHS)):
#    callDllFunc(self, self.instr.sesson, rfFreq, peakLevel, byref(*pRFAttenuationHS), byref(*pIFAttenuationHS), byref(*pPreAmplifierHS),
#        Dllname='afDigitizerDll_RF_GetHighSensitivitySettings',
#        argtypes=[afDigitizerInstance_t, c_double, c_double, POINTER(c_ulong), POINTER(c_ulong), POINTER(AFBOOL)])
#    self.update_log('RF_GetHighSensitivitySettings')

def Trigger_Count_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_Count_Get', c_ulong)

def Trigger_Detected_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_Detected_Get', AFBOOL)

afDigitizerDll_egpPolarity_t = {'Positive' : 0, 'Negative' : 1}
def Trigger_EdgeGatePolarity_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_EdgeGatePolarity_Get', c_int)
def Trigger_EdgeGatePolarity_Set(instr, Trigger_EdgeGatePolarity):
    callDllFunc(instr, 'afDigitizerDll_Trigger_EdgeGatePolarity_Set', c_int, Trigger_EdgeGatePolarity)

def Trigger_HoldOff_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_HoldOff_Get', c_ulong)
def Trigger_HoldOff_Set(instr, Trigger_HoldOff):
    callDllFunc(instr, 'afDigitizerDll_Trigger_HoldOff_Set', c_ulong, Trigger_HoldOff)

def Trigger_OffsetDelay_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_OffsetDelay_Get', c_long)
def Trigger_OffsetDelay_Set(instr, Trigger_OffsetDelay):
    callDllFunc(instr, 'afDigitizerDll_Trigger_OffsetDelay_Set', c_long, Trigger_OffsetDelay)

def Trigger_PostGateTriggerSamples_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_PostGateTriggerSamples_Get', c_ulong)
def Trigger_PostGateTriggerSamples_Set(instr, Trigger_PostGateTriggerSamples):
    callDllFunc(instr, 'afDigitizerDll_Trigger_PostGateTriggerSamples_Set', c_ulong, Trigger_PostGateTriggerSamples)

def Trigger_PreEdgeTriggerSamples_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_PreEdgeTriggerSamples_Get', c_ulong)
def Trigger_PreEdgeTriggerSamples_Set(instr, Trigger_PreEdgeTriggerSamples):
    callDllFunc(instr, 'afDigitizerDll_Trigger_PreEdgeTriggerSamples_Set', c_ulong, Trigger_PreEdgeTriggerSamples)

afDigitizerDll_tsTrigSource_t = {'PXI_TRIG_0' : 0, 'PXI_TRIG_1' : 1, 'PXI_TRIG_2' : 2, 'PXI_TRIG_3' : 3,
    'PXI_TRIG_4' : 4, 'PXI_TRIG_5' : 5, 'PXI_TRIG_6' : 6, 'PXI_TRIG_7' : 7, 'PXI_STAR' : 8, 'PXI_LBL_0' : 9,
    'PXI_LBL_1' : 10, 'PXI_LBL_2' : 11, 'PXI_LBL_3' : 12, 'PXI_LBL_4' : 13, 'PXI_LBL_5' : 14, 'PXI_LBL_6' : 15,
    'PXI_LBL_7' : 16, 'PXI_LBL_8' : 17, 'PXI_LBL_9' : 18, 'PXI_LBL_10' : 19, 'PXI_LBL_11' : 20, 'PXI_LBL_12' : 21,
    'LVDS_MARKER_0' : 22, 'LVDS_MARKER_1' : 23, 'LVDS_MARKER_2' : 24, 'LVDS_MARKER_3' : 25, 'LVDS_AUX_0' : 26,
    'LVDS_AUX_1' : 27, 'LVDS_AUX_2' : 28, 'LVDS_AUX_3' : 29, 'LVDS_AUX_4' : 30, 'LVDS_SPARE_0' : 31,
    'SW_TRIG' : 32, 'INT_TIMER' : 34, 'INT_TRIG' : 35, 'FRONT_SMB' : 36}
def Trigger_Source_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_Source_Get', c_long)
def Trigger_Source_Set(instr, Trigger_Source):
    callDllFunc(instr, 'afDigitizerDll_Trigger_Source_Set', c_long, Trigger_Source)

afDigitizerDll_swtSwTrigMode_t = {'Immediate' : 0, 'Armed' : 1}
def Trigger_SwTriggerMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_SwTriggerMode_Get', c_int)
def Trigger_SwTriggerMode_Set(instr, Trigger_SwTriggerMode):
    callDllFunc(instr, 'afDigitizerDll_Trigger_SwTriggerMode_Set', c_int, Trigger_SwTriggerMode)

afDigitizerDll_ttTrigType_t = {'Edge' : 0, 'Gate' : 1}
def Trigger_TType_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_Trigger_TType_Get', c_int)
def Trigger_TType_Set(instr, Trigger_TType):
    callDllFunc(instr, 'afDigitizerDll_Trigger_TType_Set', c_int, Trigger_TType)

def Trigger_Arm(instr, numberOfSamples):
    callDllFunc(instr, instr.sesson, numberOfSamples,
        Dllname='afDigitizerDll_Trigger_Arm',
        argtypes=[afDigitizerInstance_t, c_ulong])

afDigitizerDll_lmLVDSMode_t = {
    'Input' : 0,
    'Tristate' : 1,
    'Output' : 3,
    }

def LVDS_AuxiliaryMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LVDS_AuxiliaryMode_Get', c_int)
def LVDS_AuxiliaryMode_Set(instr, LVDS_AuxiliaryMode):
    callDllFunc(instr, 'afDigitizerDll_LVDS_AuxiliaryMode_Set', c_int, LVDS_AuxiliaryMode)

def LVDS_ClockEnable_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LVDS_ClockEnable_Get', AFBOOL)
def LVDS_ClockEnable_Set(instr, LVDS_ClockEnable):
    callDllFunc(instr, 'afDigitizerDll_LVDS_ClockEnable_Set', AFBOOL, LVDS_ClockEnable)

def LVDS_DataMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LVDS_DataMode_Get', c_int)
def LVDS_DataMode_Set(instr, LVDS_DataMode):
    callDllFunc(instr, 'afDigitizerDll_LVDS_DataMode_Set', c_int, LVDS_DataMode)

def LVDS_DataDelay_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LVDS_DataDelay_Get', c_double)

def LVDS_MarkerMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LVDS_MarkerMode_Get', c_int)
def LVDS_MarkerMode_Set(instr, LVDS_MarkerMode):
    callDllFunc(instr, 'afDigitizerDll_LVDS_MarkerMode_Set', c_int, LVDS_MarkerMode)

def LVDS_SamplingRateModeAvailable_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LVDS_SamplingRateModeAvailable_Get', AFBOOL)

afDigitizerDll_lsrmLvdsSamplingRateMode_t = {
    'LockedToCapture' : 0,
    'AutoAdjust' : 1,
    }
def LVDS_SamplingRateMode_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LVDS_SamplingRateMode_Get', c_int)
def LVDS_SamplingRateMode_Set(instr, LVDS_SamplingRateMode):
    callDllFunc(instr, 'afDigitizerDll_LVDS_SamplingRateMode_Set', c_int, LVDS_SamplingRateMode)

def LVDS_SamplingRate_Get(instr):
    return callDllFunc(instr, 'afDigitizerDll_LVDS_SamplingRate_Get', c_double)

afDigitizerDll_lcrLvdsClockRate_t = {
    '62_5MHz' : 1,
    '125MHz' : 0,
    '180MHz' : 2,
    }
def LVDS_ClockRate_Get(instr):
    callDllFunc(instr, 'afDigitizerDll_LVDS_ClockRate_Get', c_int)
def LVDS_ClockRate_Set(instr, LVDS_ClockRate):
    callDllFunc(instr, 'afDigitizerDll_LVDS_ClockRate_Set', c_int, LVDS_ClockRate)
######################
	#if err:
	#	afDigitizerDll_Capture_IQ_Cancel(Digitizer,0);  //cancel all pending buffers before quitting.

def capture_iq_capt_mem(instrument, nSamples):
        # define buffer type
        typeBuffer = c_float*nSamples
        iBuffer = typeBuffer()
        qBuffer = typeBuffer()

        Capture_IQ_CaptMem(instrument, nSamples, iBuffer, qBuffer)
        data={'I':list(iBuffer), 'Q':list(qBuffer)}
        return data

def buffer_read(instr, avgs_per_trig, trig_to_avg, num_samples, trig_timeout, Trigger_PreEdgeTriggerSamples, Modulation_GenericSamplingFrequency, BUFFER_SIZE):
    #i_data = empty(self.num_samples) #Dataset('I', data=np.empty(self.samples), unit='V')
    #q_data = empty(self.num_samples) #Dataset('Q', data=np.empty(self.samples), unit='V')
    #avgs_per_trig.update_log_set()
    #num_samples.update_log_set()
    total_samples=  avgs_per_trig*num_samples
    if total_samples > BUFFER_SIZE:
            raise(Exception('The total number of samples exceeds the buffer size'))
    i_buffer = zeros(BUFFER_SIZE, dtype=c_float)
    q_buffer = zeros(BUFFER_SIZE, dtype=c_float)
    #all_cpx = zeros(self.BUFFER_SIZE, dtype=complex)

    i_ctypes = i_buffer.ctypes.data_as(POINTER(c_float))
    q_ctypes = q_buffer.ctypes.data_as(POINTER(c_float))
    buffer_ref = afDigitizerBufferIQ_t(i_ctypes, q_ctypes, int(total_samples))
    buffer_ref_pointer = pointer(buffer_ref)
    capture_ref = afDigitizerCaptureIQ_t()

    i_avgd = zeros(num_samples)
    q_avgd = zeros(num_samples)
    #Trigger_PreEdgeTriggerSamples.receive()
    #pretrig_samples=self.instr.Trigger_PreEdgeTriggerSamples.value
    #Modulation_GenericSamplingFrequency.receive()
    #trig_to_avg.update_log_set()
    #trig_timeout.update_log_set()
    for avgidx in range(trig_to_avg):
        Capture_IQ_IssueBuffer(instr, buffer_ref, trig_timeout, capture_ref)
        Capture_IQ_ReclaimBuffer(instr, capture_ref, buffer_ref_pointer)
        #if err:
        #    afDigitizerDll_Capture_IQ_Cancel(Digitizer,0) #cancel all pending buffers before quitting.

        if buffer_ref_pointer:
            print "BUFFER POINTER OK - Trigger {}".format(avgidx)
            print "Received {0} points".format(buffer_ref.samples)
            total_samples=buffer_ref.samples
        else:
            raise(Exception("NO BUFFER"))
            total_samples = 0

        i_avgd = i_avgd + mean(i_buffer[:total_samples].reshape(avgs_per_trig, num_samples), axis=0)
        q_avgd = q_avgd + mean(q_buffer[:total_samples].reshape(avgs_per_trig, num_samples), axis=0)

    i_avgd = i_avgd/trig_to_avg
    q_avgd = q_avgd/trig_to_avg
    cpx_avgd = i_avgd + 1j*q_avgd
    results=dict()
    results["time"]=1.0e6*linspace(-Trigger_PreEdgeTriggerSamples, num_samples-Trigger_PreEdgeTriggerSamples, num_samples)/Modulation_GenericSamplingFrequency
    #self.value["IQ"].value=cpx_avgd
    results["I"]=i_avgd
    #results["Q"]=q_avgd
    #results["Mag_vec"]=absolute(cpx_avgd)
    #results["Mag_rms"]=absolute(cpx_avgd)
    #results["Phase"]=angle(cpx_avgd, deg=True)

    instr.receive('RF_LevelCorrection')
    #power=10*log10(i_avgd**2 + q_avgd**2) + self.instr.RF_LevelCorrection.value
    results["Q"]=10*log10(i_avgd**2 + q_avgd**2) + instr.RF_LevelCorrection
    #self.instr.meanP.value=mean(power)
    return results #self.group.dict_write(**results)
    #for key in self.value:
    #    self.value[key]=results[key]

#def booting():
#    	afDigitizerDll_lolbLoopBandwidth_t loopBandwidth = afDigitizerDll_lolbNarrow;#
#	afDigitizerDll_erExternalReference_t RFref = afDigitizerDll_erLockTo10MHz;#
#	afDigitizerDll_mmModulationMode_t ModMode = afDigitizerDll_mmGeneric;
#	afDigitizerDll_femFrontEndMode_t  FrontEnd = afDigitizerDll_femAuto;
#	afDigitizerDll_rfrmReferenceMode_t RFrefDaisy = afDigitizerDll_rfrmExternalDaisy;

	#err = afDigitizerDll_BootInstrument(Digitizer,LOstr,RFstr,LOext);
	#err = afDigitizerDll_RF_ExternalReference_Set(Digitizer,RFref);
	#err = afDigitizerDll_RF_Reference_Set(Digitizer,RFrefDaisy);
	#err = afDigitizerDll_Modulation_Mode_Set(Digitizer,ModMode);
	#break;
	#err = afDigitizerDll_Modulation_SetGenericSamplingFreqRatio(Digitizer,1,1);
	#err = afDigitizerDll_LO_LoopBandwidth_Set(Digitizer,loopBandwidth);
	#err = afDigitizerDll_RF_FrontEndMode_Set(Digitizer,FrontEnd);




##Free-running data capture pipeline
#CaptureIQPipelining(self, numIQ)
#    self.captiq_pipeline_enable.send(True)
#    captIQ_capt_mem(self, total_samples, ibuffer, qbuffer)
#
##Triggered data capture pipelining
#CaptureIQPipeliningtrig(self, numIQ)
#       self.captiq_pipeling_enable.send(True)
#       captIQ_trigger_arm(self, total_samples)
#       afDigitizerDll_Trigger_Detected_Get(m_Digitizer, triggered);
#       while
#       afDigitizerDll_Trigger_Detected_Get(m_Digitizer, triggered);
#       captIQ_capt_mem(self, total_samples, ibuffer, qbuffer)
#

#def direct_read(self):
#    #gets frequency checks if it matches specsampfreq
#    total_samples=  self.avgs_per_trig*self.num_samples
#    Capture_IQ_TriggerArm(self, total_samples)
#
#    self.capt_compl.receive()
#    while self.capt_compl.value==False:
#        time.sleep(1)
#        self.capt_compl.receive()
#    Capture_IQ_CaptMem(self, total_samples, ibuffer, qbuffer)
#
#    Im = mean(Idata)
#    Qm = mean(Qdata)
#    Iavg= ((m-1)/m)*Iavg+(1/m)*Im
#    Qavg = ((m-1)/m)*Qavg+(1/m)*Qm
#    Ispec[n] = Iavg
#    Qspec[n] = Qavg
#    MagSpec[n] = sqrt(Iavg^2+Qavg^2)
#    PhaseSpec[n] = atan2(Qavg,Iavg)*180/pi

#def fromhelp():
    #CreateObject
    #EepromCacheEnable #speeds up subsequent boots
    #BootInstrument
   # eternal 10Mhz: set LO.reference_set to extrernal daisy chain
   #     lock 3030 to 10 MHx using RF.externalReference_set
   # interal 10MHz:
   #     Lo.Options.CheckFitted
  #      if option fitted, set 3011 to OCXO:
  #      else set 3010 to internal
  #      lock 3030 to 10MHz
    #check ref is locked

    #set RF.inputsource_set
    #set RF.frontendmode
    #set centrefrequency to middle range
    #so LO position
    #SetInputCentreFrequency
    #SetRFinputlevelFrontendtoauto
    #setRFinputlevel
    #setsampleratemodulationmode
    #setamplerategeneric samplpingfrequency
    #trigger.source_set
    #allocatememoryforIQdata
    #DataI
    #DataQ
    #CaptMem
    #get level correction
    #CloseInstrument
    #DestroyObject

    #numberofiqsamples 16 and 32000000

#def sampleAndAverage(self):
#        """Sample the signal, calc I+j*Q theta and store it in the driver object"""
#
#        self.instr.sw_trig_mode.send('Armed')
#        total_samples = self.num_samples*self.avgs_per_trig
#        self.instr.level_correction.receive()
#        # If the stop sample is set to high, set it to nSamples
#        #if self.bCutTrace:
#        #    if self.nStopSample > self.nSamples:
#        #        self.nStopSample = self.nSamples
#        #else: #If we don't want to cut the trace, set start value to 1 and stop value to the last
#        #    self.nStartSample = 1
#        #    self.nStopSample = self.nSamples
#
#        Capture_IQ_TriggerArm(self, total_samples)
#        self.checkADCOverload()
#
#        # Define two vectors that will be used to collect the raw data
#        vI = zeros(self.nStopSample-self.nStartSample+1)
#        vQ = zeros(self.nStopSample-self.nStartSample+1)
#
#        # For each trigger, we collect the data
#        from numpy import array
#        vectorI = array([])
#        vectorQ = array([])
#
#        for i in range(0, self.trig_to_avg):
#            self.capt_compl.receive()
#            while self.capt_compl.value==False:
#                #Sleep some time in between checks
#                time.sleep(1)
#                self.checkADCOverload()
#                self.capt_compl.receive()
#                Capture_IQ_CaptMem(self, total_samples, ibuffer, qbuffer)
#                #Re-arm the trigger to prepare the digitizer for the next iteration
#                if i < (self.nTriggers-2):
#                    captIQ_trigger_arm(self, total_samples)
#                    self.checkADCOverload()
#
#            # The raw data is stored as a long array, continously appending the newly aquired data
#            if self.bRaw or self.bCollectHistogram:
#                    vectorI = np.append(vectorI, np.array(lI)*np.power(10,dLevelCorrection/20))
#                    vectorQ = np.append(vectorQ, np.array(lQ)*np.power(10,dLevelCorrection/20))
#
#            # Check if we want to take absolute value before averaging
#            # Fold the data
#            if self.bAbsoluteValue:
#                vI = vI + np.mean(np.abs(np.array(lI).reshape(nAvgPerTrigger, self.nSamples+nPreTriggers))[:,range(self.nStartSample-1, self.nStopSample)], axis=0)
#                vQ = vQ + np.mean(np.abs(np.array(lQ).reshape(nAvgPerTrigger, self.nSamples+nPreTriggers))[:,range(self.nStartSample-1, self.nStopSample)], axis=0)
#            else:
#                # If not, we just add the aquired vectorI and vectorQ to the vI and vQ arrays
#                # Fold the data
#               vI = vI + np.mean(np.array(lI).reshape(nAvgPerTrigger, self.nSamples+nPreTriggers)[:,range(self.nStartSample-1, self.nStopSample)], axis=0)
#               vQ = vQ + np.mean(np.array(lQ).reshape(nAvgPerTrigger, self.nSamples+nPreTriggers)[:,range(self.nStartSample-1, self.nStopSample)], axis=0)
#        # Average the sum of vI and vQ using the number of triggers and do level correction
#        vI = vI/self.nTriggers*np.power(10,dLevelCorrection/20)
#        vQ = vQ/self.nTriggers*np.power(10,dLevelCorrection/20)
#
#
#        # Create the time trace
#        self.cTrace = vI+1j*vQ
#
#        # Return the non averaged vectors if wanted
#        if self.bRaw:
#            self.cRaw = vectorI + 1j*vectorQ
#
#        # If we want to collect IQ histogram
#  #      if self.bCollectHistogram:
#
# #         vHistogram = self.CollectHistogram(self.nBins,vectorI, vectorQ)
#
##          f = h5py.File('C:\Users\Juliana\Desktop\Paraamp\Histograms\SampRate\Histogram_' + str(int(self.getValue('Sampling rate'))) + 'Hz_' + time.strftime("%y_%m_%d_%H_%M_%S")+'.hdf5','w')
##          f.create_dataset('Histogram',data=vHistogram[0])
##          f.create_dataset('Iedges',data=vHistogram[1])
##          f.create_dataset('Qedges',data=vHistogram[2])
##          f.close()
#        # Remove the big vectors (if any)
#        if self.bRaw or self.bCollectHistogram:
#            vectorI = None
#            vectorQ = None
#
#        # Finally, we store the avgeraged signal
#        self.cAvgSignal = np.average(vI)+1j*np.average(vQ)
#

#############################Unprocessed afDigitezerDll functions
#def ErrorCode_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ErrorCode_Get', c_long)

#afDigitizerDll_mtModuleType_t = {
#    'mtAFDIGITIZER' : -1,
#    'mtAF3010' : &H3010,
#    'mtAF3030' : &H3030,
#    'mtAF3070' : &H3070,
#    'mtPlugin' : &H0,
#    }
#
#def ErrorSource_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ErrorSource_Get', c_int)


#def EventOnError_Enable_Get(self):
#    callDllFunc(self, 'afDigitizerDll_EventOnError_Enable_Get', AFBOOL)
#
#def EventOnError_Enable_Set(self):
#    callDllFunc(self, 'afDigitizerDll_EventOnError_Enable_Set', AFBOOL)
#
#def EventOnWarning_Enable_Get(self):
#    callDllFunc(self, 'afDigitizerDll_EventOnWarning_Enable_Get', AFBOOL)
#
#def EventOnWarning_Enable_Set(self):
#    callDllFunc(self, 'afDigitizerDll_EventOnWarning_Enable_Set', AFBOOL)
#
#def EventOnError_Handler_Set(self):
#    callDllFunc(self, 'afDigitizerDll_EventOnError_Handler_Set', )
#
#def EventOnWarning_Handler_Set(self):
#    callDllFunc(self, 'afDigitizerDll_EventOnWarning_Handler_Set', )
#
#def IsActive_Get(self):
#    callDllFunc(self, 'afDigitizerDll_IsActive_Get', AFBOOL)
#
#def LoRfSpeedSyncEnable_Set(self):
#    callDllFunc(self, 'afDigitizerDll_LoRfSpeedSyncEnable_Set', AFBOOL)
#
#def LoRfSpeedSyncEnable_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LoRfSpeedSyncEnable_Get', AFBOOL)

#def *afDigitizerErrorWarningEventHandler_t)(self, eventSrc, status, msg):
#    callDllFunc(self, handlerId, eventSrc, status, msg,
#        Dllname='*afDigitizerErrorWarningEventHandler_t)',
#        argtypes=[, c_int, c_long, c_char_p])
#    self.update_log('*afDigitizerErrorWarningEventHandler_t)')
#
#def *afDigitizerCaptureIQEventHandler_t)(self, iqEvent, byref(*buffer), capture):
#    callDllFunc(self, self.instr.sesson, iqEvent, byref(*buffer), capture,
#        Dllname='*afDigitizerCaptureIQEventHandler_t)',
#        argtypes=[afDigitizerInstance_t, c_int, POINTER(), ])
#    self.update_log('*afDigitizerCaptureIQEventHandler_t)')
#
#def Calibrate_LoNull_CurrentFreqCalRequired_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Calibrate_LoNull_CurrentFreqCalRequired_Get', AFBOOL)
#
#def Calibrate_LoNull_FreqBandCalRequired_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Calibrate_LoNull_FreqBandCalRequired_Get', AFBOOL)
#
#def Calibrate_LoNull_CurrentFreqCal(self):
#    callDllFunc(self, self.instr.sesson,
#        Dllname='afDigitizerDll_Calibrate_LoNull_CurrentFreqCal',
#        argtypes=[afDigitizerInstance_t])
#    self.update_log('Calibrate_LoNull_CurrentFreqCal')
#
#def Calibrate_LoNull_FreqBandCal(self):
#    callDllFunc(self, self.instr.sesson,
#        Dllname='afDigitizerDll_Calibrate_LoNull_FreqBandCal',
#        argtypes=[afDigitizerInstance_t])
#    self.update_log('Calibrate_LoNull_FreqBandCal')

#
#def Capture_IF_ADCOverload_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IF_ADCOverload_Get', AFBOOL)
#
#def Capture_IF_CaptComplete_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IF_CaptComplete_Get', AFBOOL)
#
#def Capture_IF_CapturedSampleCount_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IF_CapturedSampleCount_Get', c_ulong)
#
#def Capture_IF_ListAddrCount_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IF_ListAddrCount_Get', c_ulong)
#
#def Capture_IF_TriggerCount_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IF_TriggerCount_Get', c_ulong)
#
#def Capture_IF_TriggerDetected_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Capture_IF_TriggerDetected_Get', AFBOOL)
#
#def Capture_IF_Abort(self):
#    callDllFunc(self, self.instr.sesson,
#        Dllname='afDigitizerDll_Capture_IF_Abort',
#        argtypes=[afDigitizerInstance_t])
#    self.update_log('Capture_IF_Abort')
#
#def Capture_IF_CaptMem(self, numberOfIFSamples, byref(ifBuffer)):
#    callDllFunc(self, self.instr.sesson, numberOfIFSamples, byref(ifBuffer),
#        Dllname='afDigitizerDll_Capture_IF_CaptMem',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER()])
#    self.update_log('Capture_IF_CaptMem')
#
#def Capture_IF_GetAbsSampleTime(self, sampleNumber, byref(*psampleTime)):
#    callDllFunc(self, self.instr.sesson, sampleNumber, byref(*psampleTime),
#        Dllname='afDigitizerDll_Capture_IF_GetAbsSampleTime',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(c_double)])
#    self.update_log('Capture_IF_GetAbsSampleTime')
#
#def Capture_IF_GetCaptMemFromOffset(self, offset, numberOfIFSamples, byref(ifBuffer)):
#    callDllFunc(self, self.instr.sesson, offset, numberOfIFSamples, byref(ifBuffer),
#        Dllname='afDigitizerDll_Capture_IF_GetCaptMemFromOffset',
#        argtypes=[afDigitizerInstance_t, c_ulong, c_ulong, POINTER()])
#    self.update_log('Capture_IF_GetCaptMemFromOffset')
#
#def Capture_IF_GetListAddrInfo(self, listEvent, byref(*pListAddr), byref(*pStartSample), byref(*pNumSamples), byref(*pInvalidSamples)):
#    callDllFunc(self, self.instr.sesson, listEvent, byref(*pListAddr), byref(*pStartSample), byref(*pNumSamples), byref(*pInvalidSamples),
#        Dllname='afDigitizerDll_Capture_IF_GetListAddrInfo',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(), POINTER(c_ulong), POINTER(c_ulong), POINTER(c_ulong)])
#    self.update_log('Capture_IF_GetListAddrInfo')
#
#def Capture_IF_GetTriggerSampleNumber(self, triggerNumber, byref(*pSampleNumber)):
#    callDllFunc(self, self.instr.sesson, triggerNumber, byref(*pSampleNumber),
#        Dllname='afDigitizerDll_Capture_IF_GetTriggerSampleNumber',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(c_ulong)])
#    self.update_log('Capture_IF_GetTriggerSampleNumber')
#
#def Capture_IF_TriggerArm(self, samples):
#    callDllFunc(self, self.instr.sesson, samples,
#        Dllname='afDigitizerDll_Capture_IF_TriggerArm',
#        argtypes=[afDigitizerInstance_t, c_ulong])
#    self.update_log('Capture_IF_TriggerArm')
#
#def Capture_IF_GetSampleCaptured(self, sampleNumber, byref(*pSampleCaptured)):
#    callDllFunc(self, self.instr.sesson, sampleNumber, byref(*pSampleCaptured),
#        Dllname='afDigitizerDll_Capture_IF_GetSampleCaptured',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(AFBOOL)])
#    self.update_log('Capture_IF_GetSampleCaptured')
#
#def ListMode_Available_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Available_Get', AFBOOL)
#
#def ListMode_ReTrigAvailable_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_ReTrigAvailable_Get', AFBOOL)
#
#afDigitizerDll_liAddressSource_t = {
#    'liasManual' : 0,
#    'liasExternal' : 1,
#    'liasCounter' : 2,
#    'liasExtSerial' : 3,
#    }
#
#def ListMode_AddressSource_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_AddressSource_Get', c_int)
#
#afDigitizerDll_liAddressSource_t = {
#    'liasManual' : 0,
#    'liasExternal' : 1,
#    'liasCounter' : 2,
#    'liasExtSerial' : 3,
#    }
#
#def ListMode_AddressSource_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_AddressSource_Set', c_int)
#
#afDigitizerDll_rmRepeatMode_t = {
#    'rmSingle' : 0,
#    'rmNTimes' : 1,
#    'rmContinuous' : 2,
#    }
#
#def ListMode_RepeatMode_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_RepeatMode_Set', c_int)
#
#afDigitizerDll_rmRepeatMode_t = {
#    'rmSingle' : 0,
#    'rmNTimes' : 1,
#    'rmContinuous' : 2,
#    }
#
#def ListMode_RepeatMode_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_RepeatMode_Get', c_int)
#
#def ListMode_RepeatCount_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_RepeatCount_Set', c_ushort)
#
#def ListMode_RepeatCount_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_RepeatCount_Get', c_ushort)
#
#def ListMode_Counter_StartAddress_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Counter_StartAddress_Get', c_ushort)
#
#def ListMode_Counter_StartAddress_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Counter_StartAddress_Set', c_ushort)
#
#def ListMode_Counter_StopAddress_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Counter_StopAddress_Get', c_ushort)
#
#def ListMode_Counter_StopAddress_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Counter_StopAddress_Set', c_ushort)
#
#afDigitizerDll_liCounterStrobe_t = {
#    'licsExternal' : 0,
#    'licsTimer' : 1,
#    }
#
#def ListMode_Counter_StrobeSource_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Counter_StrobeSource_Get', c_int)
#
#afDigitizerDll_liCounterStrobe_t = {
#    'licsExternal' : 0,
#    'licsTimer' : 1,
#    }
#
#def ListMode_Counter_StrobeSource_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Counter_StrobeSource_Set', c_int)
#
#def ListMode_Strobe_NegativeEdge_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Strobe_NegativeEdge_Get', AFBOOL)
#
#def ListMode_Strobe_NegativeEdge_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Strobe_NegativeEdge_Set', AFBOOL)
#
#def ListMode_Channel_DwellInSamples_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Channel_DwellInSamples_Get', c_ulong)
#
#def ListMode_Channel_DwellInSamples_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Channel_DwellInSamples_Set', c_ulong)
#
#def ListMode_Channel_WaitForReTrig_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Channel_WaitForReTrig_Get', AFBOOL)
#
#def ListMode_Channel_WaitForReTrig_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Channel_WaitForReTrig_Set', AFBOOL)
#
#def ListMode_Channel_DiscardSamples_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Channel_DiscardSamples_Get', AFBOOL)
#
#def ListMode_Channel_DiscardSamples_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Channel_DiscardSamples_Set', AFBOOL)
#
#def ListMode_Channel_DiscardSamplesUntilReTrig_Get(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Channel_DiscardSamplesUntilReTrig_Get', AFBOOL)
#
#def ListMode_Channel_DiscardSamplesUntilReTrig_Set(self):
#    callDllFunc(self, 'afDigitizerDll_ListMode_Channel_DiscardSamplesUntilReTrig_Set', AFBOOL)

#
#def LO_Options_AvailableCount_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Options_AvailableCount_Get', c_ulong)
#
#def LO_Resource_FPGACount_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_FPGACount_Get', c_ushort)
#
#def LO_Resource_FPGAConfiguration_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_FPGAConfiguration_Get', c_ushort)
#
#def LO_Resource_FPGAConfiguration_Set(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_FPGAConfiguration_Set', c_ushort)
#
#def LO_Resource_IsActive_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_IsActive_Get', AFBOOL)
#
#def LO_Resource_IsPlugin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_IsPlugin_Get', AFBOOL)
#
#def LO_Resource_PluginName_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_PluginName_Get', c_long)
#
#def LO_Resource_PluginName_Set(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_PluginName_Set', c_char_p)
#
#def LO_Resource_ModelCode_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_ModelCode_Get', c_long)
#
#def LO_Resource_ResourceString_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_ResourceString_Get', c_long)
#
#def LO_Resource_SerialNumber_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_SerialNumber_Get', c_long)
#
#def LO_Resource_SessionID_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Resource_SessionID_Get', c_long)
#
#afDigitizerDll_tsaTriggerSourceAddressed_t = {
#    'tsaNONE' : 0,
#    'tsaTRIG' : 1,
#    'tsaLBR' : 2,
#    'tsaSER' : 3,
#    }
#
#def LO_Trigger_AddressedSource_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Trigger_AddressedSource_Get', c_int)
#
#afDigitizerDll_tsaTriggerSourceAddressed_t = {
#    'tsaNONE' : 0,
#    'tsaTRIG' : 1,
#    'tsaLBR' : 2,
#    'tsaSER' : 3,
#    }
#
#def LO_Trigger_AddressedSource_Set(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Trigger_AddressedSource_Set', c_int)
#
#afDigitizerDll_tssTriggerSourceSingle_t = {
#    'tssLBL0' : 0,
#    'tssLBR0' : 1,
#    'tssPTB0' : 2,
#    'tssPXI_STAR' : 3,
#    'tssPTB1' : 4,
#    'tssPTB2' : 5,
#    'tssPTB3' : 6,
#    'tssPTB4' : 7,
#    'tssPTB5' : 8,
#    'tssPTB6' : 9,
#    'tssPTB7' : 10,
#    'tssLBR1' : 11,
#    'tssLBR2' : 12,
#    'tssLBR3' : 13,
#    'tssLBR4' : 14,
#    'tssLBR5' : 15,
#    'tssLBR6' : 16,
#    'tssLBR7' : 17,
#    'tssLBR8' : 18,
#    'tssLBR9' : 19,
#    'tssLBR10' : 20,
#    'tssLBR11' : 21,
#    'tssLBR12' : 22,
#    }
#
#def LO_Trigger_SingleSource_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Trigger_SingleSource_Get', c_int)
#
#def LO_Trigger_SingleSource_Set(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Trigger_SingleSource_Set', c_int)
#
#def LO_Trigger_SingleStartChannel_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Trigger_SingleStartChannel_Get', c_ushort)
#
#def LO_Trigger_SingleStartChannel_Set(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Trigger_SingleStartChannel_Set', c_ushort)
#
#def LO_Trigger_SingleStopChannel_Get(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Trigger_SingleStopChannel_Get', c_ushort)
#
#def LO_Trigger_SingleStopChannel_Set(self):
#    callDllFunc(self, 'afDigitizerDll_LO_Trigger_SingleStopChannel_Set', c_ushort)
#
#def LO_Options_Enable(self, Password):
#    callDllFunc(self, self.instr.sesson, Password,
#        Dllname='afDigitizerDll_LO_Options_Enable',
#        argtypes=[afDigitizerInstance_t, c_ulong])
#    self.update_log('LO_Options_Enable')
#
#def LO_Options_Disable(self, Password):
#    callDllFunc(self, self.instr.sesson, Password,
#        Dllname='afDigitizerDll_LO_Options_Disable',
#        argtypes=[afDigitizerInstance_t, c_ulong])
#    self.update_log('LO_Options_Disable')
#
#
#def LO_Options_Information(self, index, byref(pOptionNumber), OptionDescriptionBuffer, bufferlen):
#    callDllFunc(self, self.instr.sesson, index, byref(pOptionNumber), OptionDescriptionBuffer, bufferlen,
#        Dllname='afDigitizerDll_LO_Options_Information',
#        argtypes=[afDigitizerInstance_t, c_long, POINTER(c_ulong), c_char_p, c_long])
#    self.update_log('LO_Options_Information')
#
#def LO_Resource_FPGADescriptions(self, byref(Numbers[/*FPGACount*/]), */], byref(pCount)):
#    callDllFunc(self, self.instr.sesson, byref(Numbers[/*FPGACount*/]), */], byref(pCount),
#        Dllname='afDigitizerDll_LO_Resource_FPGADescriptions',
#        argtypes=[afDigitizerInstance_t, POINTER(c_ushort), c_char_p, POINTER(c_ushort)])
#    self.update_log('LO_Resource_FPGADescriptions')
#
#def LO_Resource_GetLastCalibrationDate(self, byref(Year), byref(Month), byref(Day), byref(Hour), byref(Minutes), byref(Seconds)):
#    callDllFunc(self, self.instr.sesson, byref(Year), byref(Month), byref(Day), byref(Hour), byref(Minutes), byref(Seconds),
#        Dllname='afDigitizerDll_LO_Resource_GetLastCalibrationDate',
#        argtypes=[afDigitizerInstance_t, POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort)])
#    self.update_log('LO_Resource_GetLastCalibrationDate')
#


#
#def Modulation_CDMA20001XDecimationRatio_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_CDMA20001XDecimationRatio_Get', c_ulong)
#
#def Modulation_CDMA20001XDecimationRatio_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_CDMA20001XDecimationRatio_Set', c_ulong)
#
#def Modulation_CDMA20001XDecimationRatioMin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_CDMA20001XDecimationRatioMin_Get', c_ulong)
#
#def Modulation_CDMA20001XDecimationRatioMax_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_CDMA20001XDecimationRatioMax_Get', c_ulong)
#
#def Modulation_Emu2319DecimationRatio_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_Emu2319DecimationRatio_Get', c_ulong)
#
#def Modulation_Emu2319DecimationRatio_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_Emu2319DecimationRatio_Set', c_ulong)
#
#def Modulation_Emu2319DecimationRatioMin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_Emu2319DecimationRatioMin_Get', c_ulong)
#
#def Modulation_Emu2319DecimationRatioMax_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_Emu2319DecimationRatioMax_Get', c_ulong)
#
#def Modulation_GSMDecimationRatio_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_GSMDecimationRatio_Get', c_ulong)
#
#def Modulation_GSMDecimationRatio_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_GSMDecimationRatio_Set', c_ulong)
#
#def Modulation_GSMDecimationRatioMin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_GSMDecimationRatioMin_Get', c_ulong)
#
#def Modulation_GSMDecimationRatioMax_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_GSMDecimationRatioMax_Get', c_ulong)
#
#def Modulation_UMTSDecimationRatio_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_UMTSDecimationRatio_Get', c_ulong)
#
#def Modulation_UMTSDecimationRatio_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_UMTSDecimationRatio_Set', c_ulong)
#
#def Modulation_UMTSDecimationRatioMin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_UMTSDecimationRatioMin_Get', c_ulong)
#
#def Modulation_UMTSDecimationRatioMax_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Modulation_UMTSDecimationRatioMax_Get', c_ulong)
#
#def RF_IFAttenuation_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFAttenuation_Get', c_ulong)
#
#def RF_IFAttenuation_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFAttenuation_Set', c_ulong)
#
#def RF_IFAttenuationMax_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFAttenuationMax_Get', c_ulong)
#
#def RF_IFAttenuationMin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFAttenuationMin_Get', c_ulong)
#
#def RF_IFAttenuationStep_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFAttenuationStep_Get', c_ulong)
#
#def RF_IFFrequency_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFFrequency_Get', c_double)
#
#afDigitizerDll_iffbIFFilterBypass_t = {
#    'iffbDisable' : 0,
#    'iffbEnable' : 1,
#    }
#
#def RF_IFFilterBypass_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFFilterBypass_Get', c_int)
#
#afDigitizerDll_iffbIFFilterBypass_t = {
#    'iffbDisable' : 0,
#    'iffbEnable' : 1,
#    }
#
#def RF_IFFilterBypass_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFFilterBypass_Set', c_int)
#
#def RF_IFInputLevel_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFInputLevel_Get', c_double)
#
#def RF_IFInputLevel_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFInputLevel_Set', c_double)
#
#def RF_IFInputLevelMax_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFInputLevelMax_Get', c_double)
#
#def RF_IFInputLevelMin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_IFInputLevelMin_Get', c_double)

#
#def RF_Channel_CentreFrequency_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_CentreFrequency_Get', c_double)
#
#def RF_Channel_CentreFrequency_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_CentreFrequency_Set', c_double)
#
#afDigitizerDll_lopLOPosition_t = {
#    'lopBelow' : 0,
#    'lopAbove' : 1,
#    }
#
#def RF_Channel_SetCentreFrequencyAndLOPosition(self, channel, CenterFrequency, LOPosition):
#    callDllFunc(self, self.instr.sesson, channel, CenterFrequency, LOPosition,
#        Dllname='afDigitizerDll_RF_Channel_SetCentreFrequencyAndLOPosition',
#        argtypes=[afDigitizerInstance_t, c_ushort, c_double, c_int])
#    self.update_log('RF_Channel_SetCentreFrequencyAndLOPosition')
#
#afDigitizerDll_femFrontEndMode_t = {
#    'femAuto' : 0,
#    'femAutoIF' : 1,
#    'femManual' : 2,
#    }
#
#def RF_Channel_FrontEndMode_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_FrontEndMode_Get', c_int)
#
#def RF_Channel_FrontEndMode_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_FrontEndMode_Set', c_int)
#
#def RF_Channel_IFInputLevel_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_IFInputLevel_Get', c_double)
#
#def RF_Channel_IFInputLevel_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_IFInputLevel_Set', c_double)
#
#def RF_Channel_IFInputLevelMax_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_IFInputLevelMax_Get', c_double)
#
#def RF_Channel_IFInputLevelMin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_IFInputLevelMin_Get', c_double)
#
#def RF_Channel_IFAttenuation_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_IFAttenuation_Get', c_ulong)
#
#def RF_Channel_IFAttenuation_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_IFAttenuation_Set', c_ulong)
#
#def RF_Channel_LevelCorrection_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_LevelCorrection_Get', c_double)
#
#def RF_Channel_LOFrequency_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_LOFrequency_Get', c_double)
#
#afDigitizerDll_lopLOPosition_t = {
#    'lopBelow' : 0,
#    'lopAbove' : 1,
#    }
#
#def RF_Channel_LOPosition_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_LOPosition_Get', c_int)
#
#afDigitizerDll_lopLOPosition_t = {
#    'lopBelow' : 0,
#    'lopAbove' : 1,
#    }
#
#def RF_Channel_LOPosition_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_LOPosition_Set', c_int)
#
#afDigitizerDll_lopLOPosition_t = {
#    'lopBelow' : 0,
#    'lopAbove' : 1,
#    }
#
#def RF_Channel_UserLOPosition_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_UserLOPosition_Get', c_int)
#
#afDigitizerDll_lopLOPosition_t = {
#    'lopBelow' : 0,
#    'lopAbove' : 1,
#    }
#
#def RF_Channel_UserLOPosition_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_UserLOPosition_Set', c_int)
#
#afDigitizerDll_lopLOPosition_t = {
#    'lopBelow' : 0,
#    'lopAbove' : 1,
#    }
#
#def RF_Channel_ActualLOPosition_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_ActualLOPosition_Get', c_int)
#
#def RF_Channel_PreAmpEnable_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_PreAmpEnable_Get', AFBOOL)
#
#def RF_Channel_PreAmpEnable_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_PreAmpEnable_Set', AFBOOL)
#
#def RF_Channel_RFInputLevel_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_RFInputLevel_Get', c_double)
#
#def RF_Channel_RFInputLevel_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_RFInputLevel_Set', c_double)
#
#def RF_Channel_RFInputLevelMax_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_RFInputLevelMax_Get', c_double)
#
#def RF_Channel_RFInputLevelMin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_RFInputLevelMin_Get', c_double)
#
#def RF_Channel_RFAttenuation_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_RFAttenuation_Get', c_ulong)
#
#def RF_Channel_RFAttenuation_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Channel_RFAttenuation_Set', c_ulong)
#
#def RF_Options_AvailableCount_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Options_AvailableCount_Get', c_ulong)
#
#def RF_Resource_FPGAConfiguration_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_FPGAConfiguration_Get', c_ushort)
#
#def RF_Resource_FPGAConfiguration_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_FPGAConfiguration_Set', c_ushort)
#
#def RF_Resource_FPGACount_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_FPGACount_Get', c_ushort)
#
#def RF_Resource_IsActive_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_IsActive_Get', AFBOOL)
#
#def RF_Resource_IsPlugin_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_IsPlugin_Get', AFBOOL)
#
#def RF_Resource_ModelCode_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_ModelCode_Get', c_long)
#
#def RF_Resource_PluginName_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_PluginName_Get', c_long)
#
#def RF_Resource_PluginName_Set(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_PluginName_Set', c_char_p)
#
#def RF_Resource_ResourceString_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_ResourceString_Get', c_long)
#
#def RF_Resource_SerialNumber_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_SerialNumber_Get', c_long)
#
#def RF_Resource_SessionID_Get(self):
#    callDllFunc(self, 'afDigitizerDll_RF_Resource_SessionID_Get', c_long)

#def RF_Options_Enable(self, password):
#    callDllFunc(self, self.instr.sesson, password,
#        Dllname='afDigitizerDll_RF_Options_Enable',
#        argtypes=[afDigitizerInstance_t, c_ulong])
#    self.update_log('RF_Options_Enable')
#
#def RF_Options_Disable(self, Password):
#    callDllFunc(self, self.instr.sesson, Password,
#        Dllname='afDigitizerDll_RF_Options_Disable',
#        argtypes=[afDigitizerInstance_t, c_ulong])
#    self.update_log('RF_Options_Disable')
#
#def RF_Options_CheckFitted(self, optionNumber, byref(pFitted)):
#    callDllFunc(self, self.instr.sesson, optionNumber, byref(pFitted),
#        Dllname='afDigitizerDll_RF_Options_CheckFitted',
#        argtypes=[afDigitizerInstance_t, c_long, POINTER(AFBOOL)])
#    self.update_log('RF_Options_CheckFitted')
#
#def RF_Options_Information(self, index, byref(pOptionNumber), OptionDescriptionBuffer, bufferlen):
#    callDllFunc(self, self.instr.sesson, index, byref(pOptionNumber), OptionDescriptionBuffer, bufferlen,
#        Dllname='afDigitizerDll_RF_Options_Information',
#        argtypes=[afDigitizerInstance_t, c_long, POINTER(c_ulong), c_char_p, c_long])
#    self.update_log('RF_Options_Information')
#
#def RF_Resource_FPGADescriptions(self, byref(Numbers[/*FPGACount*/]), */], byref(pCount)):
#    callDllFunc(self, self.instr.sesson, byref(Numbers[/*FPGACount*/]), */], byref(pCount),
#        Dllname='afDigitizerDll_RF_Resource_FPGADescriptions',
#        argtypes=[afDigitizerInstance_t, POINTER(c_ushort), c_char_p, POINTER(c_ushort)])
#    self.update_log('RF_Resource_FPGADescriptions')
#
#def RF_Resource_GetLastCalibrationDate(self, byref(Year), byref(Month), byref(Day), byref(Hour), byref(Minutes), byref(Seconds)):
#    callDllFunc(self, self.instr.sesson, byref(Year), byref(Month), byref(Day), byref(Hour), byref(Minutes), byref(Seconds),
#        Dllname='afDigitizerDll_RF_Resource_GetLastCalibrationDate',
#        argtypes=[afDigitizerInstance_t, POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort)])
#    self.update_log('RF_Resource_GetLastCalibrationDate')
#
#def RF_Routing_Reset(self):
#    callDllFunc(self, self.instr.sesson,
#        Dllname='afDigitizerDll_RF_Routing_Reset',
#        argtypes=[afDigitizerInstance_t])
#    self.update_log('RF_Routing_Reset')
#
#afDigitizerDll_rmRoutingMatrix_t = {
#    'rmPXI_TRIG_0' : 0,
#    'rmPXI_TRIG_1' : 1,
#    'rmPXI_TRIG_2' : 2,
#    'rmPXI_TRIG_3' : 3,
#    'rmPXI_TRIG_4' : 4,
#    'rmPXI_TRIG_5' : 5,
#    'rmPXI_TRIG_6' : 6,
#    'rmPXI_TRIG_7' : 7,
#    'rmPXI_STAR' : 8,
#    'rmPXI_LBL_0' : 9,
#    'rmPXI_LBL_1' : 10,
#    'rmPXI_LBL_2' : 11,
#    'rmPXI_LBL_3' : 12,
#    'rmPXI_LBL_4' : 13,
#    'rmPXI_LBL_5' : 14,
#    'rmPXI_LBL_6' : 15,
#    'rmPXI_LBL_7' : 16,
#    'rmPXI_LBL_8' : 17,
#    'rmPXI_LBL_9' : 18,
#    'rmPXI_LBL_10' : 19,
#    'rmPXI_LBL_11' : 20,
#    'rmPXI_LBL_12' : 21,
#    'rmLVDS_MARKER_1' : 22,
#    'rmLVDS_MARKER_2' : 23,
#    'rmLVDS_MARKER_3' : 24,
#    'rmLVDS_MARKER_4' : 25,
#    'rmLVDS_AUX_0' : 26,
#    'rmLVDS_AUX_1' : 27,
#    'rmLVDS_AUX_2' : 28,
#    'rmLVDS_AUX_3' : 29,
#    'rmLVDS_AUX_4' : 30,
#    'rmLVDS_SPARE_0' : 31,
#    'rmLVDS_SPARE_1' : 32,
#    'rmLVDS_SPARE_2' : 33,
#    'rmGND' : 34,
#    'rmINT_TRIG' : 35,
#    'rmTIMER' : 36,
#    'rmTIMER_SYNC' : 37,
#    'rmFRONT_SMB' : 38,
#    'rmCAPT_BUSY' : 39,
#    'rmLA_IN_0' : 40,
#    'rmLA_IN_1' : 41,
#    'rmLA_IN_2' : 42,
#    'rmLA_IN_3' : 43,
#    'rmLA_IN_4' : 44,
#    'rmLA_IN_5' : 45,
#    'rmLA_IN_6' : 46,
#    'rmLA_IN_7' : 47,
#    'rmLSTB_IN' : 48,
#    'rmLA_OUT_0' : 49,
#    'rmLA_OUT_1' : 50,
#    'rmLA_OUT_2' : 51,
#    'rmLA_OUT_3' : 52,
#    'rmLA_OUT_4' : 53,
#    'rmLA_OUT_5' : 54,
#    'rmLA_OUT_6' : 55,
#    'rmLA_OUT_7' : 56,
#    'rmSEQ_STB_IN' : 57,
#    'rmSEQ_RESET' : 58,
#    'rmSEQ_OUT_0' : 59,
#    'rmSEQ_OUT_1' : 60,
#    'rmSEQ_OUT_2' : 61,
#    'rmSEQ_OUT_3' : 62,
#    'rmSEQ_OUT_4' : 63,
#    'rmSEQ_OUT_5' : 64,
#    'rmSEQ_OUT_6' : 65,
#    'rmSEQ_OUT_7' : 66,
#    'rmSEQ_STB_OUT' : 67,
#    'rmSEQ_START' : 68,
#    'rmLST_BLANK' : 69,
#    'rmSW_TRIG' : 70,
#    'rmTIMER_TRIG' : 71,
#    'rmLA_SERIAL_OUT' : 72,
#    'rmLA_SERIAL_IN' : 73,
#    'rm_TRIG_BUSY' : 77,
#    }
#
#def RF_Routing_SetConnect(self, matrixOutput, matrixInput):
#    callDllFunc(self, self.instr.sesson, matrixOutput, matrixInput,
#        Dllname='afDigitizerDll_RF_Routing_SetConnect',
#        argtypes=[afDigitizerInstance_t, c_int, c_int])
#    self.update_log('RF_Routing_SetConnect')
#
#afDigitizerDll_rmRoutingMatrix_t = {
#    'rmPXI_TRIG_0' : 0,
#    'rmPXI_TRIG_1' : 1,
#    'rmPXI_TRIG_2' : 2,
#    'rmPXI_TRIG_3' : 3,
#    'rmPXI_TRIG_4' : 4,
#    'rmPXI_TRIG_5' : 5,
#    'rmPXI_TRIG_6' : 6,
#    'rmPXI_TRIG_7' : 7,
#    'rmPXI_STAR' : 8,
#    'rmPXI_LBL_0' : 9,
#    'rmPXI_LBL_1' : 10,
#    'rmPXI_LBL_2' : 11,
#    'rmPXI_LBL_3' : 12,
#    'rmPXI_LBL_4' : 13,
#    'rmPXI_LBL_5' : 14,
#    'rmPXI_LBL_6' : 15,
#    'rmPXI_LBL_7' : 16,
#    'rmPXI_LBL_8' : 17,
#    'rmPXI_LBL_9' : 18,
#    'rmPXI_LBL_10' : 19,
#    'rmPXI_LBL_11' : 20,
#    'rmPXI_LBL_12' : 21,
#    'rmLVDS_MARKER_1' : 22,
#    'rmLVDS_MARKER_2' : 23,
#    'rmLVDS_MARKER_3' : 24,
#    'rmLVDS_MARKER_4' : 25,
#    'rmLVDS_AUX_0' : 26,
#    'rmLVDS_AUX_1' : 27,
#    'rmLVDS_AUX_2' : 28,
#    'rmLVDS_AUX_3' : 29,
#    'rmLVDS_AUX_4' : 30,
#    'rmLVDS_SPARE_0' : 31,
#    'rmLVDS_SPARE_1' : 32,
#    'rmLVDS_SPARE_2' : 33,
#    'rmGND' : 34,
#    'rmINT_TRIG' : 35,
#    'rmTIMER' : 36,
#    'rmTIMER_SYNC' : 37,
#    'rmFRONT_SMB' : 38,
#    'rmCAPT_BUSY' : 39,
#    'rmLA_IN_0' : 40,
#    'rmLA_IN_1' : 41,
#    'rmLA_IN_2' : 42,
#    'rmLA_IN_3' : 43,
#    'rmLA_IN_4' : 44,
#    'rmLA_IN_5' : 45,
#    'rmLA_IN_6' : 46,
#    'rmLA_IN_7' : 47,
#    'rmLSTB_IN' : 48,
#    'rmLA_OUT_0' : 49,
#    'rmLA_OUT_1' : 50,
#    'rmLA_OUT_2' : 51,
#    'rmLA_OUT_3' : 52,
#    'rmLA_OUT_4' : 53,
#    'rmLA_OUT_5' : 54,
#    'rmLA_OUT_6' : 55,
#    'rmLA_OUT_7' : 56,
#    'rmSEQ_STB_IN' : 57,
#    'rmSEQ_RESET' : 58,
#    'rmSEQ_OUT_0' : 59,
#    'rmSEQ_OUT_1' : 60,
#    'rmSEQ_OUT_2' : 61,
#    'rmSEQ_OUT_3' : 62,
#    'rmSEQ_OUT_4' : 63,
#    'rmSEQ_OUT_5' : 64,
#    'rmSEQ_OUT_6' : 65,
#    'rmSEQ_OUT_7' : 66,
#    'rmSEQ_STB_OUT' : 67,
#    'rmSEQ_START' : 68,
#    'rmLST_BLANK' : 69,
#    'rmSW_TRIG' : 70,
#    'rmTIMER_TRIG' : 71,
#    'rmLA_SERIAL_OUT' : 72,
#    'rmLA_SERIAL_IN' : 73,
#    'rm_TRIG_BUSY' : 77,
#    }
#
#def RF_Routing_GetConnect(self, matrixOutput, byref(*pMatrixInput)):
#    callDllFunc(self, self.instr.sesson, matrixOutput, byref(*pMatrixInput),
#        Dllname='afDigitizerDll_RF_Routing_GetConnect',
#        argtypes=[afDigitizerInstance_t, c_int, POINTER(c_int)])
#    self.update_log('RF_Routing_GetConnect')
#
#def RF_Routing_SetOutputEnable(self, matrixOutput, outputEnable):
#    callDllFunc(self, self.instr.sesson, matrixOutput, outputEnable,
#        Dllname='afDigitizerDll_RF_Routing_SetOutputEnable',
#        argtypes=[afDigitizerInstance_t, c_int, AFBOOL])
#    self.update_log('RF_Routing_SetOutputEnable')
#
#def RF_Routing_GetOutputEnable(self, matrixOutput, byref(*pOutputEnable)):
#    callDllFunc(self, self.instr.sesson, matrixOutput, byref(*pOutputEnable),
#        Dllname='afDigitizerDll_RF_Routing_GetOutputEnable',
#        argtypes=[afDigitizerInstance_t, c_int, POINTER(AFBOOL)])
#    self.update_log('RF_Routing_GetOutputEnable')
#
#afDigitizerDll_rsRoutingScenario_t = {
#    'rsNONE' : 0,
#    'rsLVDS_AUX_TO_PXI_LBL' : 1,
#    }
#
#def RF_Routing_SetScenario(self, routingScenario):
#    callDllFunc(self, self.instr.sesson, routingScenario,
#        Dllname='afDigitizerDll_RF_Routing_SetScenario',
#        argtypes=[afDigitizerInstance_t, c_int])
#    self.update_log('RF_Routing_SetScenario')
#
#afDigitizerDll_rsRoutingScenario_t = {
#    'rsNONE' : 0,
#    'rsLVDS_AUX_TO_PXI_LBL' : 1,
#    }
#
#def RF_Routing_AppendScenario(self, routingScenario):
#    callDllFunc(self, self.instr.sesson, routingScenario,
#        Dllname='afDigitizerDll_RF_Routing_AppendScenario',
#        argtypes=[afDigitizerInstance_t, c_int])
#    self.update_log('RF_Routing_AppendScenario')
#
#afDigitizerDll_rsRoutingScenario_t = {
#    'rsNONE' : 0,
#    'rsLVDS_AUX_TO_PXI_LBL' : 1,
#    }
#
#def RF_Routing_RemoveScenario(self, routingScenario):
#    callDllFunc(self, self.instr.sesson, routingScenario,
#        Dllname='afDigitizerDll_RF_Routing_RemoveScenario',
#        argtypes=[afDigitizerInstance_t, c_int])
#    self.update_log('RF_Routing_RemoveScenario')
#
#def RF_Routing_GetScenarioList(self, byref(ScenarioList), bufferLen):
#    callDllFunc(self, self.instr.sesson, byref(ScenarioList), bufferLen,
#        Dllname='afDigitizerDll_RF_Routing_GetScenarioList',
#        argtypes=[afDigitizerInstance_t, POINTER(c_int), c_ulong])
#    self.update_log('RF_Routing_GetScenarioList')
#
#def Timer_Advance_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Timer_Advance_Get', c_ulong)
#
#def Timer_Advance_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Timer_Advance_Set', c_ulong)
#
#def Timer_Period_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Timer_Period_Get', c_double)
#
#def Timer_Period_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Timer_Period_Set', c_double)
#
#def Timer_SampleCounterMode_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Timer_SampleCounterMode_Get', AFBOOL)
#
#def Timer_SampleCounterMode_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Timer_SampleCounterMode_Set', AFBOOL)

#
#def Trigger_IntTriggerAbsTimeConst_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerAbsTimeConst_Get', c_double)
#
#def Trigger_IntTriggerAbsTimeConst_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerAbsTimeConst_Set', c_double)
#
#def Trigger_IntTriggerAbsThreshold_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerAbsThreshold_Get', c_double)
#
#def Trigger_IntTriggerAbsThreshold_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerAbsThreshold_Set', c_double)
#
#afDigitizerDll_itmIntTriggerMode_t = {
#    'itmAbsolute' : 0,
#    'itmRelative' : 1,
#    }
#
#def Trigger_IntTriggerMode_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerMode_Get', c_int)
#
#afDigitizerDll_itmIntTriggerMode_t = {
#    'itmAbsolute' : 0,
#    'itmRelative' : 1,
#    }
#
#def Trigger_IntTriggerMode_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerMode_Set', c_int)
#
#afDigitizerDll_itsIntTriggerSource_t = {
#    'itsIF' : 0,
#    'itsIQ' : 1,
#    }
#
#def Trigger_IntTriggerSource_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerSource_Set', c_int)
#
#afDigitizerDll_itsIntTriggerSource_t = {
#    'itsIF' : 0,
#    'itsIQ' : 1,
#    }
#
#def Trigger_IntTriggerSource_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerSource_Get', c_int)
#
#def Trigger_SetIntIQTriggerDigitalBandwidth(self, RequestBandwidth, SelectionMode, byref(pAchievedBandwidth)):
#    callDllFunc(self, self.instr.sesson, RequestBandwidth, SelectionMode, byref(pAchievedBandwidth),
#        Dllname='afDigitizerDll_Trigger_SetIntIQTriggerDigitalBandwidth',
#        argtypes=[afDigitizerInstance_t, c_double, c_int, POINTER(c_double)])
#    self.update_log('Trigger_SetIntIQTriggerDigitalBandwidth')
#
#def Trigger_IntTriggerRelFastTimeConst_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerRelFastTimeConst_Get', c_double)
#
#def Trigger_IntTriggerRelFastTimeConst_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerRelFastTimeConst_Set', c_double)
#
#def Trigger_IntTriggerRelSlowTimeConst_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerRelSlowTimeConst_Get', c_double)
#
#def Trigger_IntTriggerRelSlowTimeConst_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerRelSlowTimeConst_Set', c_double)
#
#def Trigger_IntTriggerRelThreshold_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerRelThreshold_Get', c_long)
#
#def Trigger_IntTriggerRelThreshold_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_IntTriggerRelThreshold_Set', c_long)
#
#afDigitizerDll_tsTrigSource_t = {
#    'tsPXI_TRIG_0' : 0,
#    'tsPXI_TRIG_1' : 1,
#    'tsPXI_TRIG_2' : 2,
#    'tsPXI_TRIG_3' : 3,
#    'tsPXI_TRIG_4' : 4,
#    'tsPXI_TRIG_5' : 5,
#    'tsPXI_TRIG_6' : 6,
#    'tsPXI_TRIG_7' : 7,
#    'tsPXI_STAR' : 8,
#    'tsPXI_LBL_0' : 9,
#    'tsPXI_LBL_1' : 10,
#    'tsPXI_LBL_2' : 11,
#    'tsPXI_LBL_3' : 12,
#    'tsPXI_LBL_4' : 13,
#    'tsPXI_LBL_5' : 14,
#    'tsPXI_LBL_6' : 15,
#    'tsPXI_LBL_7' : 16,
#    'tsPXI_LBL_8' : 17,
#    'tsPXI_LBL_9' : 18,
#    'tsPXI_LBL_10' : 19,
#    'tsPXI_LBL_11' : 20,
#    'tsPXI_LBL_12' : 21,
#    'tsLVDS_MARKER_0' : 22,
#    'tsLVDS_MARKER_1' : 23,
#    'tsLVDS_MARKER_2' : 24,
#    'tsLVDS_MARKER_3' : 25,
#    'tsLVDS_AUX_0' : 26,
#    'tsLVDS_AUX_1' : 27,
#    'tsLVDS_AUX_2' : 28,
#    'tsLVDS_AUX_3' : 29,
#    'tsLVDS_AUX_4' : 30,
#    'tsLVDS_SPARE_0' : 31,
#    'tsSW_TRIG' : 32,
#    'tsINT_TIMER' : 34,
#    'tsINT_TRIG' : 35,
#    'tsFRONT_SMB' : 36,
#    }
#
#def Trigger_UserReTrigSource_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_UserReTrigSource_Get', c_int)
#
#afDigitizerDll_tsTrigSource_t = {
#    'tsPXI_TRIG_0' : 0,
#    'tsPXI_TRIG_1' : 1,
#    'tsPXI_TRIG_2' : 2,
#    'tsPXI_TRIG_3' : 3,
#    'tsPXI_TRIG_4' : 4,
#    'tsPXI_TRIG_5' : 5,
#    'tsPXI_TRIG_6' : 6,
#    'tsPXI_TRIG_7' : 7,
#    'tsPXI_STAR' : 8,
#    'tsPXI_LBL_0' : 9,
#    'tsPXI_LBL_1' : 10,
#    'tsPXI_LBL_2' : 11,
#    'tsPXI_LBL_3' : 12,
#    'tsPXI_LBL_4' : 13,
#    'tsPXI_LBL_5' : 14,
#    'tsPXI_LBL_6' : 15,
#    'tsPXI_LBL_7' : 16,
#    'tsPXI_LBL_8' : 17,
#    'tsPXI_LBL_9' : 18,
#    'tsPXI_LBL_10' : 19,
#    'tsPXI_LBL_11' : 20,
#    'tsPXI_LBL_12' : 21,
#    'tsLVDS_MARKER_0' : 22,
#    'tsLVDS_MARKER_1' : 23,
#    'tsLVDS_MARKER_2' : 24,
#    'tsLVDS_MARKER_3' : 25,
#    'tsLVDS_AUX_0' : 26,
#    'tsLVDS_AUX_1' : 27,
#    'tsLVDS_AUX_2' : 28,
#    'tsLVDS_AUX_3' : 29,
#    'tsLVDS_AUX_4' : 30,
#    'tsLVDS_SPARE_0' : 31,
#    'tsSW_TRIG' : 32,
#    'tsINT_TIMER' : 34,
#    'tsINT_TRIG' : 35,
#    'tsFRONT_SMB' : 36,
#    }
#
#def Trigger_UserReTrigSource_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_UserReTrigSource_Set', c_int)
#
#afDigitizerDll_rsmReTrigSourceMode_t = {
#    'rsmAuto' : 0,
#    'rsmUser' : 1,
#    }
#
#def Trigger_ReTrigSourceMode_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_ReTrigSourceMode_Get', c_int)
#
#afDigitizerDll_rsmReTrigSourceMode_t = {
#    'rsmAuto' : 0,
#    'rsmUser' : 1,
#    }
#
#def Trigger_ReTrigSourceMode_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_ReTrigSourceMode_Set', c_int)
#
#afDigitizerDll_egpPolarity_t = {
#    'egpPositive' : 0,
#    'egpNegative' : 1,
#    }
#
#def Trigger_UserReTrigPolarity_Get(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_UserReTrigPolarity_Get', c_int)
#
#afDigitizerDll_egpPolarity_t = {
#    'egpPositive' : 0,
#    'egpNegative' : 1,
#    }
#
#def Trigger_UserReTrigPolarity_Set(self):
#    callDllFunc(self, 'afDigitizerDll_Trigger_UserReTrigPolarity_Set', c_int)


#def Trigger_GetTriggerSampleNumber(self, triggerNumber, byref(*pSampleNumber)):
#    callDllFunc(self, self.instr.sesson, triggerNumber, byref(*pSampleNumber),
#        Dllname='afDigitizerDll_Trigger_GetTriggerSampleNumber',
#        argtypes=[afDigitizerInstance_t, c_ulong, POINTER(c_ulong)])
#    self.update_log('Trigger_GetTriggerSampleNumber')
#
#def NotImplemented(self):
#    callDllFunc(self, self.instr.sesson,
#        Dllname='afDigitizerDll_NotImplemented',
#        argtypes=[afDigitizerInstance_t])
#    self.update_log('NotImplemented')
#
#def GetVbErrorInfo(self, byref(vbErrNo), vbErrSourceStrBuf, bufLen):
#    callDllFunc(self, self.instr.sesson, byref(vbErrNo), vbErrSourceStrBuf, bufLen,
#        Dllname='afDigitizerDll_GetVbErrorInfo',
#        argtypes=[afDigitizerInstance_t, POINTER(c_long), c_char_p, c_long])
#    self.update_log('GetVbErrorInfo')

