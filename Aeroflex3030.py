# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 16:46:27 2014

@author: thomasaref
"""

from atom.api import Typed, Callable, Bool, Unicode, Float, Int, Enum, List, ContainerList
from Base_Atom import Instrument
import afDig

def start_af3030(instr, LoResource="", RfResource="", LO_Reference='OCXO'):
    instr.LoResource=LoResource
    instr.RfResource=RfResource
    instr.CreateObject(instr)
    instr.send('EepromCacheEnable', True)
    instr.BootInstrument(instr, LoResource=LoResource, RfResource=RfResource)
    #instr.send("LO_Reference", LO_Reference)
    instr.send('Modulation_Mode', "Generic") #defaults to generic=5
    instr.send("Capture_IQ_ReclaimTimeout", 10000)
    instr.send("Trigger_PreEdgeTriggerSamples", 100)
    instr.send("Modulation_GenericSamplingFrequency", 85.0e6)  #250.0e6
    instr.update_log("Boot finished")

def stop_af3030(instr):
    instr.Capture_IQ_Abort(instr)
    instr.CloseInstrument(instr)
    #print "Closed AF Digitizer"
    instr.DestroyObject(instr)
    #print "Destroyed the instrument reference"
    #object.instr.boss.update_log(object.instr, cmd="stop")

class af3030(Instrument): #using strict traits catches name typos
    session = Typed(afDig.afDigitizerInstance_t, ()) #afDigitizer()#0 #afDigitizerInstance_t()
    capture_ref=Typed(afDig.afDigitizerCaptureIQ_t)
    buffer_ref=Typed(afDig.afDigitizerBufferIQ_t)

    booter=Callable(start_af3030)
    closer=Callable(stop_af3030)

#    def _default_reserved_names(self):
#        members=Instrument.members().keys()
#        members.extend(('capture_ref', 'buffer_ref'))
#        return members

    def _default_label(self):
        return 'Aeroflex 3030 All'

    def _default_main_params(self):
        return ["EepromCacheEnable", "Modulation_Mode", "LO_Reference", "LO_ReferenceLocked", 'RF_CentreFrequency',#style="custom", label="Frequency"),
                'RF_RFInputLevel',#label="Max Input Level"),
                 'Trigger_Source', 'Trigger_SwTriggerMode', "Capture_IQ_ADCOverload", "Capture_IQ_CaptComplete", "Capture_IQ_CapturedSampleCount",
                 "Capture_IQ_ReclaimTimeout", "Capture_IQ_Resolution", "Capture_IQ_Abort", 'RF_LevelCorrection', 'avgs_per_trig','trig_to_avg', 'BUFFER_SIZE',
                 'num_samples','trig_timeout', 'Trigger_PreEdgeTriggerSamples', 'Trigger_EdgeGatePolarity',"Modulation_GenericSamplingFrequency"]#,
                  #"timeIQ", 'Mag_dB_LC']

    EepromCacheEnable=Bool().tag(set_cmd= afDig.EepromCacheEnable_Set, get_cmd=afDig.EepromCacheEnable_Get)

    CreateObject=Callable(afDig.CreateObject)
    DestroyObject=Callable(afDig.DestroyObject)

    BootInstrument=Callable(afDig.BootInstrument)
    LoResource=Unicode("PXI8::15::INSTR").tag(sub=True)
    RfResource=Unicode("PXI8::14::INSTR").tag(sub=True)
    LoIsPlugin=Bool(False).tag(sub=True)

    CloseInstrument=Callable(afDig.CloseInstrument)
    ClearErrors=Callable(afDig.ClearErrors)
    GetVersion=Int().tag(get_cmd=afDig.GetVersion)#, value=[0]))

    Capture_IQ_ADCOverload=Enum(False, True).tag(mapping={True : -1, False : 0}, 
                                            get_cmd=afDig.Capture_IQ_ADCOverload_Get)
    Capture_IQ_CaptComplete=Enum(True, False).tag(mapping={True : -1, False : 0},
                                      get_cmd=afDig.Capture_IQ_CaptComplete_Get)
    Capture_IQ_CapturedSampleCount=Int().tag(get_cmd=afDig.Capture_IQ_CapturedSampleCount_Get)
    #Capture_IQ_EventHandler=Typed(num_var, num_var(name='CaptIQ_EventHandler',
    #                                              set_cmd=afDig.Capture_IQ_EventHandler_Set,
    #                                              get_cmd=afDig.Capture_IQ_EventHandler_Get))
    #Capture_IQ_ListAddrCount=Typed(int_var, kwargs=dict(get_cmd=afDig.Capture_IQ_ListAddrCount_Get))
    Capture_IQ_ReclaimTimeout=Int(10).tag(set_cmd=afDig.Capture_IQ_ReclaimTimeout_Set,
                                      get_cmd=afDig.Capture_IQ_ReclaimTimeout_Get)
    Capture_IQ_Resolution=Enum('16Bit' ,'Auto').tag(mapping=afDig.afDigitizerDll_iqrIQResolution_t,
                               get_cmd=afDig.Capture_IQ_Resolution_Get,
                               set_cmd=afDig.Capture_IQ_Resolution_Set)
    Capture_IQ_TriggerCount=Int().tag(get_cmd=afDig.Capture_IQ_TriggerCount_Get)
    Capture_IQ_TriggerDetected=Enum(False, True).tag(mapping={True : -1, False : 0},
                                    get_cmd=afDig.Capture_IQ_TriggerDetected_Get)
    Capture_IQ_Abort=Callable(afDig.Capture_IQ_Abort)
    Capture_IQ_Cancel=Callable(afDig.Capture_IQ_Cancel)
    Capture_IQ_CaptMem=Callable(afDig.Capture_IQ_CaptMem)
    #Capture_IQ_CaptMemWithKey=Typed(func_var, kwargs=dict(name='CaptIQ_CaptMemWithKey',
    #                                                  set_cmd=afDig.Capture_IQ_CaptMemWithKey))
    Capture_IQ_GetAbsSampleTime=Float().tag(get_cmd=afDig.Capture_IQ_GetAbsSampleTime)
    #CaptIQ_GetCaptMemFromOffset=Typed(func_var, kwargs=dict(name='CaptIQ_GetCaptMemFromOffset',
    #                                                         set_cmd=afDig.Capture_IQ_GetCaptMemFromOffset))
    #CaptIQ_GetCaptMemFromOffsetWithKey=Typed(func_var, kwargs=dict(name='CaptIQ_GetCaptMemFromOffsetWithKey',
    #                                                               set_cmd=afDig.Capture_IQ_GetCaptMemFromOffsetWithKey))

    Capture_IQ_IssueBuffer=Callable(afDig.Capture_IQ_IssueBuffer)

    #CaptIQ_ReclaimBuffer=Typed(func_var, kwargs=dict(name='CaptIQ_ReclaimBuffer', run_cmd=afDig.Capture_IQ_ReclaimBuffer,
    #                                                 add_params=AP(capture_ref=capture_ref, buffer_ref_pointer=pointer(buffer_ref))))

    Capture_IQ_TriggerArm=Callable(afDig.Capture_IQ_TriggerArm)
    samples=Int().tag(sub=True)

    Capt_SampleDataType=Enum('IQData', 'IFData').tag(mapping=afDig.afDigitizerDll_sdtSampleDataType_t,
                                   get_cmd=afDig.Capture_SampleDataType_Get,
                                   set_cmd=afDig.Capture_SampleDataType_Set)

    Capt_PipeliningEnable=Enum(False, True).tag(mapping={True : -1, False : 0}, 
                                            get_cmd=afDig.Capture_PipeliningEnable_Get,
                                            set_cmd=afDig.Capture_PipeliningEnable_Set)
    Capt_TimeoutMode=Enum('Auto', 'User').tag(mapping=afDig.afDigitizerDll_ctmCaptureTimeoutMode_t,
                                get_cmd=afDig.Capture_TimeoutMode_Get,
                                set_cmd=afDig.Capture_TimeoutMode_Set)
    Capt_UserTimeout=Int().tag(get_cmd=afDig.Capture_UserTimeout_Get,
                          set_cmd=afDig.Capture_UserTimeout_Set)

    LO_Reference=Enum('OCXO', 'Internal', 'ExternalDaisy', 'ExternalTerminated').tag(
                                         mapping=afDig.afDigitizerDll_lormReferenceMode_t,
                                         get_cmd=afDig.LO_Reference_Get,
                                         set_cmd=afDig.LO_Reference_Set)

    LO_ReferenceLocked=Enum(True, False).tag(mapping={True : -1, False : 0},
                               get_cmd=afDig.LO_ReferenceLocked_Get)

    LO_LoopBandwidth=Enum('Normal', 'Narrow', 'Unspecified').tag(mapping=afDig.afDigitizerDll_lolbLoopBandwidth_t,
                                 get_cmd=afDig.LO_LoopBandwidth_Get,
                                 set_cmd=afDig.LO_LoopBandwidth_Set)

    LO_Temperature=Float().tag(get_cmd=afDig.LO_Resource_Temperature_Get)

    LO_Trigger_Mode=Enum('None', 'Advance', 'Toggle', 'Hop').tag(mapping=afDig.afDigitizerDll_lotmTriggerMode_t,
                                get_cmd=afDig.LO_Trigger_Mode_Get,
                                set_cmd=afDig.LO_Trigger_Mode_Set)

    #LO_Options_CheckFitted=Enumv( get_cmd=afDig.LO_Options_CheckFitted,
    #                                                   add_params=AP(OptionNumber=CInt())))

    Modulation_Mode=Enum('UMTS', 'GSM', 'CDMA20001x', 'Emu2319', 'Generic').tag(mapping=afDig.afDigitizerDll_mmModulationMode_t,
                                 get_cmd=afDig.Modulation_Mode_Get,
                                 set_cmd=afDig.Modulation_Mode_Set)

    Modulation_DecimatedSamplingFrequency=Float().tag(get_cmd=afDig.Modulation_DecimatedSamplingFrequency_Get)

    Modulation_UndecimatedSamplingFrequency=Float().tag(get_cmd=afDig.Modulation_UndecimatedSamplingFrequency_Get)

    Modulation_GenericDecimationRatio=Int().tag(get_cmd=afDig.Modulation_GenericDecimationRatio_Get,
                                           set_cmd=afDig.Modulation_GenericDecimationRatio_Set)

    Modulation_GenericDecimationRatioMin=Int().tag(get_cmd=afDig.Modulation_GenericDecimationRatioMin_Get)

    Modulation_GenericDecimationRatioMax=Int().tag(get_cmd=afDig.Modulation_GenericDecimationRatioMax_Get)

    Modulation_GenericSamplingFrequency=Float(5e7).tag(label="Modulation Generic Sampling Frequency", unit="Hz",
                                get_cmd=afDig.Modulation_GenericSamplingFrequency_Get,
                                set_cmd=afDig.Modulation_GenericSamplingFrequency_Set)

    Modulation_GenericSamplingFrequencyMax=Float().tag(get_cmd=afDig.Modulation_GenericSamplingFrequencyMax_Get)

    Modulation_GenericSamplingFrequencyMin=Float().tag(get_cmd=afDig.Modulation_GenericSamplingFrequencyMin_Get)

    Modulation_GenericSamplingFreqNumerator=Float().tag(get_cmd=afDig.Modulation_GenericSamplingFreqNumerator_Get)

    Modulation_GenericSamplingFreqDenominator=Int().tag(get_cmd=afDig.Modulation_GenericSamplingFreqDenominator_Get)

    #Modulation_GenericSamplingFreqRatio=Typed(float_var, kwargs=dict(name='Modulation_GenericSamplingFreqRatio',
    #                                                                  set_cmd=afDig.Modulation_SetGenericSamplingFreqRatio,
    #                                                                  add_params=AP(numerator=CInt(), denominator=CInt())))


    RF_AutoFlatnessMode=Enum('Disable', 'Enable').tag(mapping=afDig.afDigitizerDll_afmAutoFlatnessMode_t,
                                                get_cmd=afDig.RF_AutoFlatnessMode_Get,
                                                set_cmd=afDig.RF_AutoFlatnessMode_Set)

    RF_AutoTemperatureOptimization=Enum('Disable', 'Enable').tag(mapping=afDig.afDigitizerDll_atoAutoTemperatureOptimization_t,
                                         get_cmd=afDig.RF_AutoTemperatureOptimization_Get,
                                         set_cmd=afDig.RF_AutoTemperatureOptimization_Set)

    RF_CentreFrequency=Float(2.0e9).tag(label='Center Frequency',
                               unit='Hz',
                               get_cmd=afDig.RF_CentreFrequency_Get,
                               set_cmd=afDig.RF_CentreFrequency_Set)

#afDigitizerDll_lopLOPosition_t = {'LO Below' : 0, 'LO Above' : 1}
#def RF_SetCentreFrequencyAndLOPosition'RF_SetCentreFrequencyAndLOPosition', mapp=afDigitizerDll_lopLOPosition_t,
#add_params=AP((self, CenterFrequency)
#set_cmd=RF_SetCentreFrequencyAndLOPosition:

    RF_CentreFrequencyLOAboveMax=Float().tag(get_cmd=afDig.RF_CentreFrequencyLOAboveMax_Get)


    RF_CentreFrequencyLOBelowMin=Float().tag(get_cmd=afDig.RF_CentreFrequencyLOBelowMin_Get)

    RF_CentreFrequencyMax=Float().tag(get_cmd=afDig.RF_CentreFrequencyMax_Get)

    RF_CentreFrequencyMin=Float().tag(get_cmd=afDig.RF_CentreFrequencyMin_Get)

    RF_CurrentChannel=Int().tag(get_cmd=afDig.RF_CurrentChannel_Get,
                                            set_cmd=afDig.RF_CurrentChannel_Set)

    RF_DividedLOFrequency=Float().tag(get_cmd=afDig.RF_DividedLOFrequency_Get)

    RF_ExternalReference=Enum('Lock To 10MHz', 'Free Run').tag(mapping=afDig.afDigitizerDll_erExternalReference_t,
                               get_cmd=afDig.RF_ExternalReference_Get,
                               set_cmd=afDig.RF_ExternalReference_Set)

    RF_FrontEndMode=Enum('Auto', 'AutoIF', 'Manual').tag(mapping=afDig.afDigitizerDll_femFrontEndMode_t,
                          get_cmd=afDig.RF_FrontEndMode_Get,
                          set_cmd=afDig.RF_FrontEndMode_Set)

    RF_InputSource=Enum('IFInput', 'RFInput').tag(mapping=afDig.afDigitizerDll_isInputSource_t,
                         get_cmd=afDig.RF_InputSource_Get,
                         set_cmd=afDig.RF_InputSource_Set)

    RF_LevelCorrection=Float().tag(get_cmd=afDig.RF_LevelCorrection_Get)

    RF_LOFrequency=Float().tag(get_cmd=afDig.RF_LOFrequency_Get)

    RF_LOOffset=Float().tag(get_cmd=afDig.RF_LOOffset_Get)

    RF_LOPosition=Enum('LO Below', 'LO Above').tag(mapping=afDig.afDigitizerDll_lopLOPosition_t,
                                 get_cmd=afDig.RF_LOPosition_Get,
                                 set_cmd=afDig.RF_LOPosition_Set)

    RF_UserLOPosition=Enum('LO Below', 'LO Above').tag(mapping=afDig.afDigitizerDll_lopLOPosition_t,
                                 get_cmd=afDig.RF_UserLOPosition_Get,
                                 set_cmd=afDig.RF_UserLOPosition_Set)

    RF_ActualLOPosition=Enum('LO Below', 'LO Above').tag(mapping=afDig.afDigitizerDll_lopLOPosition_t,
                                 get_cmd=afDig.RF_ActualLOPosition_Get)

    RF_LOPositionMode=Enum('LO Below', 'LO Above').tag(mapping=afDig.afDigitizerDll_lopmLOPositionMode_t,
                                                  get_cmd=afDig.RF_LOPositionMode_Get,
                                                  set_cmd=afDig.RF_LOPositionMode_Set)

    RF_PreAmpEnable=Enum(True, False).tag(mapping=afDig.TrueFalse, get_cmd=afDig.RF_PreAmpEnable_Get,
                                                set_cmd=afDig.RF_PreAmpEnable_Set)

    RF_AutoPreAmpSelection=Enum(True, False).tag(mapping=afDig.TrueFalse,
                                                 get_cmd=afDig.RF_AutoPreAmpSelection_Get,
                                                 set_cmd=afDig.RF_AutoPreAmpSelection_Set)

    RF_RemoveDCOffset=Enum(True, False).tag(mapping=afDig.TrueFalse,
                                            get_cmd=afDig.RF_RemoveDCOffset_Get,
                                            set_cmd=afDig.RF_RemoveDCOffset_Set)


    RF_Reference=Enum('Internal', 'External Daisy', 'External PCI Backplane').tag(
                                 mapping=afDig.afDigitizerDll_rfrmReferenceMode_t,
                                 get_cmd=afDig.RF_Reference_Get,
                                 set_cmd=afDig.RF_Reference_Set)
    RF_ReferenceLocked=Bool().tag(get_cmd=afDig.RF_ReferenceLocked_Get)

    RF_RFAttenuation=Int().tag(get_cmd=afDig.RF_RFAttenuation_Get,
                               set_cmd=afDig.RF_RFAttenuation_Set)

    RF_RFAttenuationMax=Int().tag(get_cmd=afDig.RF_RFAttenuationMax_Get)

    RF_RFAttenuationMin=Int().tag(get_cmd=afDig.RF_RFAttenuationMin_Get)

    RF_RFAttenuationStep=Int().tag(get_cmd=afDig.RF_RFAttenuationStep_Get)

    RF_RFInputLevel=Float(0).tag(label='Max Input Level', unit='dBm',
                           get_cmd=afDig.RF_RFInputLevel_Get,
                           set_cmd=afDig.RF_RFInputLevel_Set)

    RF_RFInputLevelMax=Float().tag(get_cmd=afDig.RF_RFInputLevelMax_Get)
    RF_RFInputLevelMin=Float().tag(get_cmd=afDig.RF_RFInputLevelMin_Get)

    RF_SampleFrequency=Float().tag(get_cmd=afDig.RF_SampleFrequency_Get)

    RF_DitherEnable=Bool().tag(get_cmd=afDig.RF_DitherEnable_Get,
                               set_cmd=afDig.RF_DitherEnable_Set)
    RF_DitherAvailable=Bool().tag(get_cmd=afDig.RF_DitherAvailable_Get)

    RF_Resource_Temperature=Float().tag(get_cmd=afDig.RF_Resource_Temperature_Get)

    RF_Routing_ScenarioListSize=Int().tag(get_cmd=afDig.RF_Routing_ScenarioListSize_Get)

    RF_OptimizeTemperatureCorrection=Callable(afDig.RF_OptimizeTemperatureCorrection)

    #RF_Bandwidth=Typed(func_var, kwargs=dict(name='RF_Bandwidth', get_cmd=afDig.RF_GetBandwidth,
    #                                add_params=AP(centreFreq=CFloat(), span=CFloat(), flatness=CInt())))

    #RF_RecommendedLOPosition=Enumv(name='RF_RecommendedLOPosition', mapp=afDig.afDigitizerDll_lopLOPosition_t,
    #                                                        get_cmd=afDig.RF_GetRecommendedLOPosition,
    #                                                        add_params=AP(digitizerFreq=CFloat(), signalFreq=CFloat())))

    Trigger_Count=Int().tag(get_cmd=afDig.Trigger_Count_Get)

    Trigger_Detected=Bool().tag(get_cmd=afDig.Trigger_Detected_Get)

    Trigger_EdgeGatePolarity=Enum('Positive', 'Negative').tag(label='Trigger Edge Gate Polarity',
                                   mapping=afDig.afDigitizerDll_egpPolarity_t,
                                   get_cmd=afDig.Trigger_EdgeGatePolarity_Get,
                                   set_cmd=afDig.Trigger_EdgeGatePolarity_Set)

    Trigger_HoldOff=Int().tag(get_cmd=afDig.Trigger_HoldOff_Get,
                         set_cmd=afDig.Trigger_HoldOff_Set)

    Trigger_OffsetDelay=Int().tag(get_cmd=afDig.Trigger_OffsetDelay_Get,
                              set_cmd=afDig.Trigger_OffsetDelay_Set)

    Trigger_PostGateTriggerSamples=Int().tag(get_cmd=afDig.Trigger_PostGateTriggerSamples_Get,
                               set_cmd=afDig.Trigger_PostGateTriggerSamples_Set)

    Trigger_PreEdgeTriggerSamples=Int().tag(get_cmd=afDig.Trigger_PreEdgeTriggerSamples_Get,
                                             set_cmd=afDig.Trigger_PreEdgeTriggerSamples_Set)

    Trigger_Source=Enum('SW_TRIG', 'FRONT_SMB', 'PXI_TRIG_0', 'PXI_TRIG_1', 'PXI_TRIG_2', 'PXI_TRIG_3', 'PXI_TRIG_4',
                        'PXI_TRIG_5', 'PXI_TRIG_6', 'PXI_TRIG_7', 'PXI_STAR',
                        'PXI_LBL_0', 'PXI_LBL_1', 'PXI_LBL_2', 'PXI_LBL_3', 'PXI_LBL_4', 'PXI_LBL_5',
                        'PXI_LBL_6', 'PXI_LBL_7', 'PXI_LBL_8', 'PXI_LBL_9', 'PXI_LBL_10', 'PXI_LBL_11', 'PXI_LBL_12',
                        'LVDS_MARKER_0', 'LVDS_MARKER_1', 'LVDS_MARKER_2', 'LVDS_MARKER_3',
                        'LVDS_AUX_0', 'LVDS_AUX_1', 'LVDS_AUX_2', 'LVDS_AUX_3', 'LVDS_AUX_4',
                        'LVDS_SPARE_0', 'INT_TIMER', 'INT_TRIG').tag(
                         mapping=afDig.afDigitizerDll_tsTrigSource_t,
                         get_cmd=afDig.Trigger_Source_Get,
                         set_cmd=afDig.Trigger_Source_Set)

    Trigger_SwTriggerMode=Enum('Immediate', 'Armed').tag(mapping=afDig.afDigitizerDll_swtSwTrigMode_t,
                                get_cmd=afDig.Trigger_SwTriggerMode_Get,
                                set_cmd=afDig.Trigger_SwTriggerMode_Set)

    Trigger_TType=Enum('Edge', 'Gate').tag(mapping=afDig.afDigitizerDll_ttTrigType_t,
                        get_cmd=afDig.Trigger_TType_Get,
                        set_cmd=afDig.Trigger_TType_Set)

    Trigger_Arm=Callable(afDig.Trigger_Arm)
    numberOfSamples=Int(100).tag(sub=True)

    IQ=List(['I', 'Q']).tag(get_cmd=afDig.capture_iq_capt_mem)
    nSamples=Int(100).tag(sub=True)

    timeIQ=List(default=['time', 'I']).tag(get_cmd=afDig.buffer_read)
    avgs_per_trig=Int(2000).tag(sub=True, label="Averages per trigger")
    trig_to_avg=Int(1).tag(sub=True, label="Triggers to average")
    BUFFER_SIZE=Int(20000000).tag(sub=True, label="Maximum buffer size")
    num_samples=Int(5000).tag(sub=True, label="Number of samples")
    trig_timeout=Int(1000).tag(sub=True, label="Trig waiting in ms")
    time=ContainerList(default=[0]).tag(sub=True, unit="s")
    I=ContainerList(default=[0]).tag(sub=True, unit="V")
    Q=ContainerList(default=[0]).tag(sub=True, unit="V")
    meanP=Float()
    #Enumv(mapping=afDig.afDigitizerDll_lmLVDSMode_t,
#    mapping={True : -1, False : 0},
    LVDS_AuxiliaryMode= Enum('Tristate', 'Input', 'Output').tag(mapping=afDig.afDigitizerDll_lmLVDSMode_t,
                             get_cmd= afDig.LVDS_AuxiliaryMode_Get,
                             set_cmd=afDig.LVDS_AuxiliaryMode_Set)

    LVDS_ClockEnable=Enum(True, False).tag(mapping={True : -1, False : 0},
                 get_cmd=afDig.LVDS_ClockEnable_Get, set_cmd=afDig.LVDS_ClockEnable_Set)

    LVDS_DataMode=Enum('Tristate', 'Input', 'Output').tag(mapping=afDig.afDigitizerDll_lmLVDSMode_t,
                  get_cmd=afDig.LVDS_DataMode_Get, set_cmd=afDig.LVDS_DataMode_Set)

    LVDS_DataDelay=Float().tag(get_cmd=afDig.LVDS_DataDelay_Get)

    LVDS_MarkerMode=Enum('Tristate', 'Input', 'Output').tag(mapping=afDig.afDigitizerDll_lmLVDSMode_t,
                     get_cmd=afDig.LVDS_MarkerMode_Get, set_cmd=afDig.LVDS_MarkerMode_Set)

    LVDS_SamplingRateModeAvailable=Enum(True, False).tag(mapping={True : -1, False : 0},
                                  get_cmd=afDig.LVDS_SamplingRateModeAvailable_Get)

   # LVDS_SamplingRateMode=Enumv(mapping=afDig.afDigitizerDll_lsrmLvdsSamplingRateMode_t, get_cmd=afDig.LVDS_SamplingRateMode_Get,
   #                        set_cmd=afDig.LVDS_SamplingRateMode_Set)

   # LVDS_SamplingRate=Strv(get_cmd=afDig.LVDS_SamplingRate_Get)

   # LVDS_ClockRate=Enumv(mapping=afDig.afDigitizerDll_lcrLvdsClockRate_t, get_cmd=afDig.LVDS_ClockRate_Get, set_cmd=afDig.LVDS_ClockRate_Set)

#    Q=Typed(arr_var, arr_var(name="Q", unit="V",  plot=True))
#    Mag_vec=Typed(arr_var, arr_var(name="Mag_vec", unit="V",  plot=True))
#    Mag_rms=Typed(arr_var, arr_var(name="Mag_rms", unit="V",  plot=True))
#    Phase=Typed(arr_var, arr_var(name="Phase", unit="deg",  plot=True))
#    Mag_dB_LC=Typed(arr_var, arr_var(name="Mag_dB_LC", unit="V",  plot='z'))

#                                                                   I=I,
#                                                                   Q=Q,
#                                                                   Mag_vec=Mag_vec,
#                                                                   Mag_rms=Mag_rms,
#                                                                   Phase=Phase,
#                                                                   Mag_dB_LC=Mag_dB_LC
#                                                                   ),
#                                                       add_params=AP(avgs_per_trig=avgs_per_trig,
#                                                                                 trig_to_avg=trig_to_avg,
#                                                                                 num_samples=num_samples,
#                                                                                 trig_timeout=trig_timeout,
#                                                                                 pretrig_samples=Trigger_PreEdgeTriggerSamples,
#                                                                                 sampling_rate=Modulation_GenericSamplingFrequency,
#                                                                                 level_correction=RF_LevelCorrection,
#                                                                                 BUFFER_SIZE=BUFFER_SIZE),
#                                                       get_cmd=afDig.buffer_read,
#                                                       plot='hide'))
 #250.0e6

   # def __init__(self, boss, lo_resource_name="PXI8::15::INSTR", dig_resource_name="PXI8::14::INSTR", OCXO=False):
        #self.session = afDig.afDigitizerTyped_t()
        #self.lo_resource_name=lo_resource_name
        #self.dig_resource_name=dig_resource_name

        #self.time=arr_var(name="Time", unit="s", value=[0])
        #self.I=arr_var(name="I", unit="V", value=[0])
        #self.Q=arr_var(name="Q", unit="V", value=[0])
        #self.Mag_vec=arr_var(name="Mag_vec", unit="V", value=[0])
        #self.Mag_rms=arr_var(name="Mag_rms", unit="V", value=[0])
        #self.Phase=arr_var(name="Phase", unit="deg", value=[0])
        #self.Mav_vec_dB=arr_var(name="Mag_vec_dB", unit="V", value=[0])
        #self.timeIQ=link_var(value={"time": self.time,
        #                            "I": self.I,
        #                            "Q": self.Q,
        #                            "Mag_vec": self.Mag_vec,
                                    #'Mag_rms': self.Mag_rms,
                                    #'Phase': self.Phase,
         #                           "Mag_vec_dB": self.Mag_vec_dB},
         #                    name="timeIQ",
         #                    get_cmd=afDig.buffer_read)
#
#        super(Aeroflex3030All, self).__init__(boss=boss)
#
#        afDig.CreateObject(self)
#        self.EepromCacheEnable.send(True)
#        afDig.BootInstrument(self, LoResource=self.lo_resource_name, RfResource=self.dig_resource_name)
#        if OCXO:
#            self.LO_Reference.send('OCXO')
#        else:
#            self.LO_Reference.send('ExternalDaisy')
#        self.Modulation_Mode.send("Generic") #defaults to generic=5
#        self.CaptIQ_ReclaimTimeout.send(10000)
#        self.Trigger_PreEdgeTriggerSamples.send(100)
#        self.Modulation_GenericSamplingFrequency.send(85.0e6) #250.0e6



#print afDig.afDigitizerDll_lmLVDSMode_t,
class Aeroflex3030(af3030):
    def _default_label(self):
        return 'Aeroflex 3030'

    def _default_main_params(self):
        return ["EepromCacheEnable", "Modulation_Mode", "LO_Reference", "LO_ReferenceLocked", 'RF_CentreFrequency',#style="custom", label="Frequency"),
                'RF_RFInputLevel',#label="Max Input Level"),
                 'Trigger_Source', 'Trigger_SwTriggerMode', "Capture_IQ_ADCOverload",  "Capture_IQ_CapturedSampleCount",
                 "Capture_IQ_ReclaimTimeout", "Capture_IQ_Resolution", "Capture_IQ_Abort", 'RF_LevelCorrection', 'avgs_per_trig','trig_to_avg', 'BUFFER_SIZE',
                 'num_samples','trig_timeout', 'Trigger_PreEdgeTriggerSamples', 'Trigger_EdgeGatePolarity',"Modulation_GenericSamplingFrequency",
                  "timeIQ", 'time', 'I', 'LVDS_AuxiliaryMode', 'LVDS_ClockEnable', 'LVDS_DataMode', 'LVDS_DataDelay','LVDS_MarkerMode',
                  'LVDS_SamplingRateModeAvailable', 'Capture_IQ_TriggerArm', 'Capture_IQ_TriggerDetected',  "Capture_IQ_CaptComplete", 'IQ', 'meanP',  'Capture_IQ_Abort', 'Trigger_Arm', 'Trigger_Detected', ]
                    #'LVDS_SamplingRate', 'LVDS_ClockRate']

if __name__=="__main__":
   # from Boss import Boss
   # B=Boss(save_file='test_acq_dig.hdf5')
    a=Aeroflex3030()
    #a.boot()
    #print a.LO_Reference.mapping
    #print a.LO_Reference.enum_val
    #a.LO_Reference.send('OXCO')
    #a.Modulation_Mode.send("Generic") #defaults to generic=5
    #a.LVDS_DataMode.value='Output'
    #a.LVDS_MarkerMode.value='Input'
    a.show()
    #a.RF_CentreFrequency.send(2.0e9)
#    a.input_level.send(-10.0)
#    a.mod_gen_samp_freq.send(250.0e6)
#    a.trig_source.send(32) #front smb #32 ) software trigger 36
#    a.trig_edge_polarity.send(0) #Rising
#    a.trig_pre_edge_samples.send(pretrigger_samples)
#    a.capt_iq_reclaim_timeout.send(timeout*1000)
    #a.timeIQ.receive()




