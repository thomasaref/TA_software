# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 17:54:17 2014

@author: thomasaref
"""

from ctypes import c_char_p, WinDLL, c_long, byref, Structure, c_float, POINTER, c_ulong,\
    c_void_p, create_string_buffer, c_int, c_double, pointer, c_ushort, c_uint, c_uint16, c_int16, c_uint32
from numpy import linspace, zeros, mean, absolute, angle, log10, array, sqrt
import time
STRING = c_char_p
_lib = WinDLL('af3030_32')
AFBOOL = c_uint
af3030Instance=c_ulong

class afDigitizerBufferIQ_t(Structure): #Mirrors a struct in C
    _fields_ = [('iBuffer', POINTER(c_float)),
                ('qBuffer', POINTER(c_float)),
                ('samples', c_ulong),
                ('userData', c_void_p),]

def getDllFunc(name, argtypes=[af3030Instance], restype=c_long):
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
        af3030_error_message = getDllFunc('af3030_error_message',
                                argtypes = [c_ulong, c_long, c_char_p])
        af3030_error_message(session, errorcode, errorDescription )
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
        if 'argtypes' not in kwargs.keys():
            kwargs['argtypes']=[af3030Instance]
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
            obj=getDllFunc(name=Dllname, argtypes=[af3030Instance, valtype])
            value=args[2]
            error=obj(instr.session, valtype(value))
            get_error(instr.session, error)
        elif Dllname[-3:]=='Get':
            obj = getDllFunc(name=Dllname, argtypes=[af3030Instance, POINTER(valtype)])
            dValue = valtype()
            error = obj(instr.session, byref(dValue))
            get_error(instr.session, error)
            return dValue.value
        else:
            print "Bad Dllname! Doesn't end in Set or Get!"

def af3030_init(instr, resourceName, idquery=False, resetdevice=True):
    callDllFunc(instr, resourceName, idquery, resetdevice, byref(instr.session),
                Dllname='af3030_init',
                argtypes=[c_char_p, AFBOOL, AFBOOL, POINTER(af3030Instance)])

def af3030_close(instr):
    callDllFunc(instr, instr.session,
                Dllname='af3030_close',
                argtypes=af3030Instance)

def af3030_getLevelCorrModuleChan(instr, channel=-1):
        refLevel_dBfsd=c_double()
        obj=getDllFunc(name='af3030_getLevelCorrModuleChan',
                       argtypes=[af3030Instance, POINTER(c_double), c_int])
        error=obj(instr.session, refLevel_dBfsd, channel)
        get_error(instr.session, error)
        return refLevel_dBfsd.value

def af3030_getLevelCorrModule(instr):
    return callDllFunc(instr, instr.session,
        Dllname='af3030_getLevelCorrModule',
        argtypes=[af3030Instance, POINTER(c_double)], valtype=c_double)

def af3030_getSampleDataType(instr):
    return callDllFunc(instr, instr.session,
        Dllname='af3030_getSampleDataType',
        argtypes=[af3030Instance, POINTER(c_uint)], valtype=c_uint)
#from C:\Program Files (x86)\IVI Foundation\VISA\WinNT\include\af3030_lib_const
af3030_LVDS={'INPUT': 0, 'TRISTATE':1, 'OUTPUT':3}
Sample_Data_Types={'IF_DATA': 0, 'IQ_DATA':1}

def af3030_setRfInputLevel(instr, RFInputLevel):
    callDllFunc(instr, instr.session, c_double(RFInputLevel),
                Dllname='af3030_setRfInputLevel',
                argtypes=[af3030Instance, c_double])

def af3030_getRfInputLevel(instr):
    return callDllFunc(instr, instr.session,
                Dllname='af3030_getRfInputLevel',
                argtypes=[af3030Instance, POINTER(c_double)], valtype=c_double)

def capture_iq_capt_mem(instr, nSamples):
        # define buffer type
        samples=nSamples*2
        typeBuffer = c_int16*samples
        iqBuffer = typeBuffer()
        af3030_captMem(instr, 2*nSamples, iqBuffer)
        return iqBuffer

def af3030_captMem(instr, samples, iqBuffer):
    return callDllFunc(instr, instr.session, samples, byref(iqBuffer),
                       Dllname='af3030_captMem',
                       argtypes=[af3030Instance, c_uint32, POINTER(c_int16)])

def af3030_getCaptureComplete(instr):
     return callDllFunc(instr, instr.session, Dllname='af3030_getCaptureComplete',
                        argtypes=[af3030Instance, POINTER(AFBOOL)], valtype=AFBOOL)

def af3030_getTriggerDetected(instr):
     return callDllFunc(instr, instr.session,
                        Dllname='af3030_getTriggerDetected',
                        argtypes=[af3030Instance, POINTER(c_uint)], valtype=c_uint)

def af3030_getSwTriggerMode(instr):
     return callDllFunc(instr, instr.session,
                        Dllname='af3030_getSwTriggerMode',
                        argtypes=[af3030Instance, POINTER(c_uint)], valtype=c_uint)

def af3030_getSampleDataOutputFormat(instr):
    return callDllFunc(instr, instr.session,
                       Dllname='af3030_getSampleDataOutputFormat',
                       argtypes=[af3030Instance, POINTER(c_uint16)], valtype=c_uint16)

def af3030_getAdcOverloadLevel(instr):
    return callDllFunc(instr, instr.session,
                       Dllname='af3030_getAdcOverloadLevel',
                       argtypes=[af3030Instance, POINTER(c_double)], valtype=c_double)

def af3030_getRfAttenuation(instr):
    return callDllFunc(instr, instr.session,
                       Dllname='af3030_getRfAttenuation',
                       argtypes=[af3030Instance, POINTER(c_uint32)], valtype=c_uint32)

#Sample Data Output Format
#----------------------------------------------------------------------------*/
#define af3030_OUTPUT_DATA_16_BIT		0
#define af3030_OUTPUT_DATA_32_BIT		1

#define af3030_TRIG_SW_IMMEDIATE			0 //Immediate capture the data (wait while capture)
#define af3030_TRIG_SW_ARMED				1 //Arm (and Trigger) before capturing the data
#To calculate the absolute input RF signal power associated with captured IQ data pair,
        #perform the following calculation (with I and Q scaled between -1.0 to +1.0):-

#Power (in dBm) = 10*log(I^2 + Q^2) + level correction figure
