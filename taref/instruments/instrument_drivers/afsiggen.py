# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 12:37:18 2016

@author: thomasaref
"""

from pxi_backbone import PXI_Backbone, pp
from ctypes import create_string_buffer, byref, c_double, c_ulong, c_long

if 0:  #Code for generating COM module
    from comtypes.client import CreateObject
    s=CreateObject("afComSigGen.afCoSigGen")
from comtypes.gen import AFCOMSIGGENLib

class afSigGen(PXI_Backbone):
    def __init__(self):
        super(afSigGen, self).__init__(lib_name='afSigGenDll_32.dll', com_lib=AFCOMSIGGENLib)

    mode=pp('Mode', prefix='m') #Manual
    LO_reference=pp('LO_Reference', prefix='lorm') #OXCO, ExternalTerminated, ExternalDaisy, Internal
    modulation_source=pp('Manual_ModulationSource', prefix='ms') #CW, LVDS, ARB, AM, FM, ExtAnalog
    frequency=pp('Manual_Frequency', dtype=c_double)
    level=pp('Manual_Level', dtype=c_double)
    level_mode=pp("Manual_LevelMode", prefix="lm") #Auto, Frozen, Peak, Rms,

    #level_max=pp("Manual_LevelMax", dtype=c_double)
    output=pp('Manual_RfState', prefix=bool)

    arb_external_trigger_enable=pp('ARB_ExternalTrigger_Enable', prefix=bool)
    arb_external_trigger_gated=pp('ARB_ExternalTrigger_Gated', prefix=bool)
    arb_external_trigger_negative_edge=pp('ARB_ExternalTrigger_NegativeEdge', prefix=bool)

    arb_single_shot_mode=pp('ARB_SingleShotMode', prefix=bool)

    def arb_single_shot_trigger(self):
        self.do_func('ARB_SingleShotTrigger')

    def arb_add_file(self, filename):
        self.do_func('ARB_Catalogue_AddFile', filename)

    def arb_delete_file(self, filename):
        self.do_func('ARB_Catalogue_DeleteFile', filename)

    def arb_delete_all_files(self):
        self.do_func('ARB_Catalogue_DeleteAllFiles')

    def arb_file_sample_rate_get(self, filename):
        return self.get_func('ARB_Catalogue_GetFileSampleRate', filename, dtype=c_ulong)

    def arb_play_file(self, filename):
        self.do_func('ARB_Catalogue_PlayFile', filename)

    def arb_reload_all_files(self):
        self.do_func('ARB_Catalogue_ReloadAllFiles')

    @property
    def arb_is_playing(self):
        return self.get_func('ARB_IsPlaying_Get', prefix=bool)

    def arb_stop_playing(self):
        self.do_func('ARB_StopPlaying')

    #def ARB_find_file(self, filename):
    #    self.get_func('ARB_Catalogue_FindFile')

    def start(self, lo_address="3010S1", sig_address="3025S1", plugin=False):
        self.address=sig_address
        self.lo_address=lo_address
        self.do_func("ClearErrors")
        self.do_func('BootInstrument', lo_address, sig_address, plugin)
        self.LO_reference='ExternalTerminated'
        self.mode='Manual'

    def stop(self):
        self.do_func('CloseInstrument')
        self.do_func("DestroyObject")

    @property
    def reference_locked(self):
        return self.get_func('LO_ReferenceLocked_Get', prefix=bool)

    @property
    def is_active(self):
        return self.get_func('IsActive_Get', prefix=bool)

    @property
    def frequency_max(self):
        return self.get_func('Manual_FrequencyMax_Get', dtype=c_double)

    def reset(self):
        self.do_func("Manual_Reset")
        
    def scenario_set(self, scen):
        self.set_func("RF_Routing_SetScenario", scen, prefix="rs")
    
    def scenario_remove(self, scen):
        self.set_func('RF_Routing_RemoveScenario', scen, prefix="rs")
 
    def scenario_append(self, scen):
        self.set_func('RF_Routing_AppendScenario', scen, prefix="rs")
        
    #def get_scen_list_size(self):
    #    return self.get_func("RF_Routing_ScenarioListSize_Get", dtype=c_ulong)
        
    def scenario_list_get(self, n=None):
        if n is None:
            n=self.get_func("RF_Routing_ScenarioListSize_Get", dtype=c_ulong)
        scen_list=(c_long*n)()
        self.do_func("RF_Routing_GetScenarioList", byref(scen_list), n)
        return [self.clib.get_map(item, "rs") for item in scen_list]
        #return scen_list[:]
    #def manual_arb_file_set(self, ArbFile):
    #    self.set_func('Manual_ArbFile_Set', byref(ArbFile))
    #    return (ArbFile.value)

    #@property
    #def manual_arb_file(self, arbFileBuffer, arbFileBufLen):
    #    self.msg=create_string_buffer(256)
    #    self.do_func('Manual_ArbFile_Get', byref(self.msg), 256)
    #    return self.msg.value

    #@property
    #def manual_arb_file_name_length(self):
    #    return self.get_func('Manual_ArbFileNameLength')

    #def manual_arb_stop_playing(self):
    #    self.do_func('Manual_ArbStopPlaying')

if __name__=='__main__':
    a=afSigGen()
    a.start()
    if 0:
        r"C:\Users\Morran or Lumi\Documents\Thomas\tom_out.aiq"
        a.arb_add_file(r"C:\Users\Morran or Lumi\Documents\Thomas\tom_out.aiq")
        a.arb_play_file(r"C:\Users\Morran or Lumi\Documents\Thomas\tom_out.aiq")
        a.arb_stop_playing()
        a.modulation_source="CW"
    #a.get_func('LO_Reference_Get', prefix="lorm")
    #a.get_func('LO_ReferenceLocked_Get', prefix=bool)

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
