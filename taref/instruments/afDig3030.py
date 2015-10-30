# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 15:39:32 2014

@author: Speedy
"""
from atom.api import Typed
from Base_Atom import Instrument,
import afD

def start_af3030(instr, resourceName, idquery=False, resetdevice=True):
    instr.af3030_init(instr, resourceName, idquery, resetdevice)

def stop_af3030(instr):
    instr.af303_close()

class af3030(Instrument): #using strict traits catches name typos
    session = Typed(afD.af3030Instance, ()) #afDigitizer()#0 #afDigitizerInstance_t()
    booter=Callable(start_af3030)
    closer=Callable(stop_af3030)

    def _default_label(self):
        return 'Aeroflex 3030 All'

    def _default_main_params(self):
        return ["EepromCacheEnable", "Modulation_Mode", "LO_Reference", "LO_ReferenceLocked", 'RF_CentreFrequency',#style="custom", label="Frequency"),
                'RF_RFInputLevel',#label="Max Input Level"),
                 'Trigger_Source', 'Trigger_SwTriggerMode', "CaptIQ_ADCOverload", "CaptIQ_CaptComplete", "CaptIQ_CapturedSampleCount",
                 "CaptIQ_ReclaimTimeout", "CaptIQ_IQ_Resolution", "CaptIQ_Abort", 'RF_LevelCorrection', 'avgs_per_trig','trig_to_avg', 'BUFFER_SIZE',
                 'num_samples','trig_timeout', 'Trigger_PreEdgeTriggerSamples', 'Trigger_EdgeGatePolarity',"Modulation_GenericSamplingFrequency"]#,
                  #"timeIQ", 'Mag_dB_LC']

    EepromCacheEnable=Bool().tag(set_cmd= afDig.EepromCacheEnable_Set, get_cmd=afDig.EepromCacheEnable_Get)

    af3030_init=Callable(af3030_init)
    resourceName=Unicode("PXI8::14::INSTR").tag(sub=True)
    idquery=Bool(False).tag(sub=True)
    resetdevice=Bool(True).tag(sub=True)

    af3030_close=Callable(afD.af3030_close)

    LevelCorrModuleChan=Float().tag(get_cmd=af3030_getLevelCorrModuleChan)
    channel=Int(-1).tag(sub=True)

    LevelCorrModule=Float().tag(get_cmd=af3030_getLevelCorrModule)

    SampleDataType=Enum('IQ_DATA', 'IF_DATA').tag(mapping=afD.Sample_Data_Types,
                                    get_cmd=afD.af3030_getSampleDataType)
    #af3030_LVDS={'INPUT': 0, 'TRISTATE':1, 'OUTPUT':3}

    RfInputLevel=Float().tag(set_cmd=afD.af3030_setRfInputLevel,
                             get_cmd=afD.af3030_getRfInputLevel)

    capture_iq_capt_mem=ContainerList().tag(get_cmd=capture_iq_capt_mem)
    nSamples=Int().tag(sub=True)

    captMem=Callable(captMem)
    samples=Int().tag(sub=True)
    iqBuffer=ContainerList().tag(sub=True)

    CaptureComplete=Bool(False).tag(get_cmd=af3030_getCaptureComplete)
    TriggerDetected=Bool().tag(get_cmd=af3030_getTriggerDetected)

    swTriggerMode=Enum().tag(get_cmd=af3030_getSwTriggerMode)

    SampleDataOutputFormat=Enum().tag(get_cmd=af3030_getSampleDataOutputFormat)
    AdcOverloadLevel=Float().tag(get_cmd=af3030_getAdcOverloadLevel)
    RfAttenuation=Int().tag(get_cmd=af3030_getRfAttenuation)

if __name__=="__main__":
    t=af3030()
#    try:
    t.boot()
    print t.session
    #print af3030_getSampleDataType(t)
    #print af3030_getSampleDataOutputFormat(t)
    #afDigitizerDll_Capture_IQ_TriggerArm(...)

    #afDigitizerDll_Capture_IQ_TriggerDetected_Get(...)
    #print af3030_getSwTriggerMode(t)
    #print af3030_getCaptureComplete(t)
    #print af3030_getTriggerDetected(t)
    t.capture_iq_capt_mem.receive(1000)
    I=[]
    Q=[]
    for i, item in enumerate(d):
        if i % 2 ==0:
            I.append(item)
        else:
            Q.append(item)
    for rfil in [-20, -10, 0, 10]:
        af3030_setRfInputLevel(t, RFInputLevel=rfil)
        ol=af3030_getAdcOverloadLevel(t)
        print 'ADC overload level {}'.format(ol)
        il=af3030_getRfInputLevel(t)
        print 'RF input level {}'.format(il)
        atten=af3030_getRfAttenuation(t)
        print 'Attenuation {}'.format(atten)
        meanI=mean(I)#/(2**15-1)#*(10**il/20)*1000 #ol #32767 #65535
        meanQ=mean(Q)#/(2**15-1)#*(10**il/20)*1000
        lc=af3030_getLevelCorrModule(t)
        meanIQ=sqrt(meanI**2+meanQ**2)/(32767)
        Power=10*log10(meanIQ**2)+lc-il#+atten
        #print (10**il/20)
        #print (10**ol/20)
        #print il-lc
        #print I, Q
        print Power
        print "level correction: {}".format(lc)
    #print af3030_getCaptureComplete(t)
    #print af3030_getTriggerDetected(t)
#        afDigitizerDll_Capture_IQ_CaptComplete_Get(...)

 #       afDigitizerDll_Capture_IQ_CaptMem(...)
 #   finally:


    af3030_close(t)

#    d=af3030_getLevelCorrModule(t)
#    print d
#    print af3030_getRfInputLevel(t)
#    af3030_setRfInputLevel(t, RFInputLevel=10.0)
#    print af3030_getRfInputLevel(t)
#    print af3030_getLevelCorrModule(t)

#    1
#1.2824481152   1.28221332282
#0.0
#-20.0
#-11.7685518848  -11.7687866772

    #10
    #11.7131525504    11.7122133228