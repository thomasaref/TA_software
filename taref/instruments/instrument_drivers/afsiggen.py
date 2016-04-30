# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 12:37:18 2016

@author: thomasaref
"""

from pxi_backbone import PXI_Backbone
from ctypes import create_string_buffer, byref
#Code for generating COM module
#from comtypes.client import CreateObject
#s=CreateObject("afComSigGen.afCoSigGen")
from comtypes.gen import AFCOMSIGGENLib

class afSigGen(PXI_Backbone):
    #modulation_source_mapping=dict(CW=SG.afSigGenDll_msCW,
    #                                 LVDS=SG.afSigGenDll_msLVDS,
    #                                 ARB=SG.afSigGenDll_msARB,
    #                                 AM=SG.afSigGenDll_msAM,
    #                                 FM=SG.afSigGenDll_msFM,
    #                                 ExtAnalog=afSigGenDll_msExtAnalog)

    def __init__(self, lib_name, func_prefix=None):
        super(afSigGen, self).__init__(lib_name=='afSigGenDll_32.dll', com_lib=AFCOMSIGGENLib)

    def start(self, lo_resource_name, dig_resource_name):
        self.do_func('BootInstrument', self.session, lo_resource_name, dig_resource_name, False)
        #self.lo_reference_set(afSigGenDll_lormExternalTerminated)
        self.do_func('LO_Reference_Set', self.session, self.clib['lormExternalTerminated'])
        #self.mode_set(afSigGenDll_mManual)
        self.do_func('Mode_Set', self.session, self.clib["mManual"])
        #self.output = 'Off'
        #self.power = -30

    def stop(self):
        self.do_func('CloseInstrument', self.session)
        self.do_func("DestroyObject", self.session)

    def is_active_get(self):
        return self.get_func('IsActive_Get', self.session)

    def manual_modulation_source_set(self, src):
        self.do_func('Manual_ModulationSource_Set', self.session, self.clib[src])

    def manual_modulation_source_get(self):
        return self.get_func('Manual_ModulationSource_Get', self.session)

    def frequency_set(self, frequency):
        self.do_func('Manual_Frequency_Set', self.session, frequency)
        self.frequency=frequency

    def frequency_get(self):
        self.frequency=self.get_func('Manual_Frequency_Get', self.session)
        return self.frequency

    #get_func'Manual_FrequencyMax_Get(self.session, byref(pFrequency))
    def level_set(self, level):
        self.do_func('Manual_Level_Set', self.session, level)
        self.level=level

    def level_get(self):
        self.level=self.get_func('Manual_Level_Get', self.session)
        return self.level

    #def manual_arb_file_set(self, ArbFile=None):
    #    ArbFile = ArbFile or c_char()
    #    do_func('Manual_ArbFile_Set', self.session, byref(ArbFile))
    #    return (ArbFile.value)

    def arb_file_get(self, arbFileBuffer, arbFileBufLen):
        self.msg=create_string_buffer(256)
        self.do_func('Manual_ArbFile_Get', self.session, byref(self.msg), 256)
        return self.msg.value

    #def manual_arb_file_name_length_get(self, pArbFileBufLen=None):
    #    pArbFileBufLen = pArbFileBufLen or c_long()
    #    error = afSigGenDll_Manual_ArbFileNameLength_Get(self.session, byref(pArbFileBufLen))
    #    if error:
    #        self.get_error(error)
    #    return (pArbFileBufLen.value)

    def arb_stop_playing(self):
        self.do_func('Manual_ArbStopPlaying', self.session)

    def rf_state_set(self, state):
        self.do_func('Manual_RfState_Set', self.session, state)
        self.state=state

    def manual_rf_state_get(self):
        self.state=self.get_func('Manual_RfState_Get', self.session)
        return self.state


#from comtypes.client import CreateObject
#
#class afCOMSigGen(object):
#    def __init__(self, lib_name):
#        self.obj=CreateObject("afComSigGen.afCoSigGen")
#
#
#    def error_check(session, error_code):
#        if error_code==0:
#            print "No error: {}".format(error_code)
#            return
#        msg=get_error_message(session)
#        if error_code<0:
#            raise Exception("{0}: {1}".format(error_code, msg))
#        elif error_code>0:
#            print "WARNING: {0}: {1}".format(error_code, msg)
#
#
#
#
#
#s.IsActive
#
#s.ErrorCode
#s.ErrorMessage
#s.ErrorSource
#
#s.BootIntrument()
#s.ClearErrors(...)
#s.CloseInstrument()
#
#  ARB
# |      property ARB - retrieves an interface for configuration of the signal generator ARB
# |
# |  ARBControlMode
# |      Get property ARBControlMode
#
#s.Manual.Level #level
#s.Manual.LevelActual #actual level
#s.Manual.LevelMode  #leveling mode
#s.Manual.RfState #on off
#s.Manual.FrequencyMax  #max frequency of sig gen
#s.Manual.Frequency #current frequency
#
#s.Manual.ArbFile #name of arbfile
#
#s.ARB.SingleShotMode #when true runs only once
#s.ARB.SingleShotTrigger(...)
#s.ARB.StopPlaying(...)
#s.ARB.FilePlaying
#s.ARB.IsPlaying
#
#s.ARB.Catalogue.AddFile(...)
#s.ARB.Catalogue.DeleteAllFiles(...)
#s.ARB.Catalogue.DeleteFile(...)
#s.ARB.Catalogue.FindFile(...)
##s.ARB.Catalogue.GetFileNameByIndex(self_, *args, **kw)
#s.ARB.Catalogue.GetFileSampleRate(...)
#s.ARB.Catalogue.PlayFile(...)
#s.ARB.Catalogue.ReloadAllFiles(...)
#s.ARB.Catalogue.FileCount
#
#from comtypes.gen import AFCOMSIGGENLib as sg
#
#dict(CW=sg.afSigGenDll_msCW,
#     LVDS=sg.afSigGenDll_msLVDS,
#     ARB=sg.afSigGenDll_msARB,
#     AM=sg.afSigGenDll_msAM,
#     FM=sg.afSigGenDll_msFM,
#     ExtAnalog=afSigGenDll_msExtAnalog
#
#
#if 0:
#    s.Manual.Reset()
