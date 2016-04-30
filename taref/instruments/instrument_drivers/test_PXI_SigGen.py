# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:58:23 2016

@author: Morran or Lumi
"""

from ctypes import WinDLL, create_string_buffer, Structure, c_long, c_double

_lib = WinDLL('afSigGenDll_32.dll')
error_msg=create_string_buffer(256)

def get_error_message(session):
    _lib.afSigGenDll_ErrorMessage_Get(session, error_msg, 256)
    return error_msg.value

def error_check(session, error_code):
    if error_code==0:
        print "No error: {}".format(error_code)
        return
    msg=get_error_message(session)
    if error_code<0:
        raise Exception("{0}: {1}".format(error_code, msg))
    elif error_code>0:
        print "WARNING: {0}: {1}".format(error_code, msg)

def do_func(func_name, *args):
    error_code=getattr(_lib, "afDigitizerDll_"+func_name)(*args)
    error_check(args[0], error_code)

def get_func(func_name, *args, **kwargs):
    temp=kwargs.get("dtype", c_long)()
    args=args+(byref(temp),)
    do_func(func_name, *args)
    return temp.value


from comtypes.client import CreateObject

def error_check(session, error_code):
    if error_code==0:
        print "No error: {}".format(error_code)
        return
    msg=get_error_message(session)
    if error_code<0:
        raise Exception("{0}: {1}".format(error_code, msg))
    elif error_code>0:
        print "WARNING: {0}: {1}".format(error_code, msg)



s=CreateObject("afComSigGen.afCoSigGen")

s.IsActive

s.ErrorCode
s.ErrorMessage
s.ErrorSource

s.BootIntrument()
s.ClearErrors(...)
s.CloseInstrument()

  ARB
 |      property ARB - retrieves an interface for configuration of the signal generator ARB
 |
 |  ARBControlMode
 |      Get property ARBControlMode

s.Manual.Level #level
s.Manual.LevelActual #actual level
s.Manual.LevelMode  #leveling mode
s.Manual.RfState #on off
s.Manual.FrequencyMax  #max frequency of sig gen
s.Manual.Frequency #current frequency

s.Manual.ArbFile #name of arbfile

s.ARB.SingleShotMode #when true runs only once
s.ARB.SingleShotTrigger(...)
s.ARB.StopPlaying(...)
s.ARB.FilePlaying
s.ARB.IsPlaying

s.ARB.Catalogue.AddFile(...)
s.ARB.Catalogue.DeleteAllFiles(...)
s.ARB.Catalogue.DeleteFile(...)
s.ARB.Catalogue.FindFile(...)
#s.ARB.Catalogue.GetFileNameByIndex(self_, *args, **kw)
s.ARB.Catalogue.GetFileSampleRate(...)
s.ARB.Catalogue.PlayFile(...)
s.ARB.Catalogue.ReloadAllFiles(...)
s.ARB.Catalogue.FileCount

from comtypes.gen import AFCOMSIGGENLib as sg

dict(CW=sg.afSigGenDll_msCW,
     LVDS=sg.afSigGenDll_msLVDS,
     ARB=sg.afSigGenDll_msARB,
     AM=sg.afSigGenDll_msAM,
     FM=sg.afSigGenDll_msFM,
     ExtAnalog=afSigGenDll_msExtAnalog


if 0:
    s.Manual.Reset()
