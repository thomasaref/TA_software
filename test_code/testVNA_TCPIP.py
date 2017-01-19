# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 13:56:03 2016

@author: Morran or Lumi
"""
from comtypes.client import CreateObject
#import comtypes.client as cl
#print dir(cl)

#for threading:
#from pythoncom import CoInitialize
#        CoInitialize()
#import comtypes
#print dir(comtypes)

#from comtypes.client import GetModule
#To create module:
#print GetModule("AgNA.dll")

#.Interop')
import comtypes.gen.AgilentNALib as AgilentNALib
#print dir(AgNALib)
#print dir(AgNALib.AgilentNA)
#from comtypes.client import gen_dir
#print gen_dir

#digitizer
#c=CreateObject('afComDigitizer.afCoDigitizer')
#a=GetModule(r'C:\Program Files (x86)\Aeroflex\PXI\Bin\afComDigitizer.dll')
#b=CreateObject(a.afCoDigitizer)
  def writeVNA(self, input_str):
        self.log("WriteString: {0}".format(input_str))
        self.VNA.System2.WriteString(input_str)
        
    def readVNA(self):
        value=self.VNA.System2.ReadString()
        self.log("ReadString: {0}".format(value))
        return value

    def askVNA(self, input_str):
        self.writeVNA(input_str)
        return self.readVNA()
        
def askVNA(input_str):
    VNA.System2.WriteString(input_str)
    VNA.System2.ReadString()
def invert_dict(indict):
    return {obj:key for key, obj in indict.iteritems()}

SweepMode = {'Swept'     :    AgilentNALib.AgilentNASweepModeSwept,
           'Stepped'     :    AgilentNALib.AgilentNASweepModeStepped,
           'FastStepped' :    AgilentNASweepModeFastStepped,
           'FastSwept'   :    AgilentNASweepModeFastSwept}

SweepType = {'LinFrequency' : AgilentNALib.AgilentNASweepTypeLinFrequency,
             'LogFrequency' : AgilentNASweepTypeLogFrequency,
             'Segment' : AgilentNASweepTypeSegment,
             'Power' : AgilentNASweepTypePower,
             'CWTime' : AgilentNASweepTypeCWTime}


if 1:
    VNA=CreateObject("AgilentNA.AgilentNA")
    #PS2 = CreateObject( "LambdaGenPS.LambdaGenPS")
    #print dir(VNA)
    #print help(VNA)
    VNA.Initialize( "TCPIP::129.16.115.134::5025::SOCKET", False, False, "")
    #print dir(VNA)
    #print dir(VNA.Channels)
    VNA.Channels["Channel1"].Averaging
    VNA.Channels["Channel1"].Points
    VNA.Channels["Channel1"].ClearAverage()
    VNA.Channels["Channel1"].AveragingFactor
    VNA.Channels["Channel1"].StimulusRange.Stop
    VNA.Channels["Channel1"].StimulusRange.Start
    VNA.Channels["Channel1"].StimulusRange.Span
    VNA.Channels["Channel1"].StimulusRange.Center
    VNA.System2.WriteString(":OUTP 0")
    def testrun():
        Chan.ClearAverage()
        for n in range(3):
            Chan.TriggerSweep(1000)
            VNA.System2.WaitForOperationComplete(10000)

# values for enumeration 'AgilentNASweepModeEnum'
AgilentNASweepModeSwept = 0
AgilentNASweepModeStepped = 1
AgilentNASweepModeFastStepped = 2
AgilentNASweepModeFastSwept = 3


# values for enumeration 'AgilentNASweepTypeEnum'
AgilentNASweepTypeLinFrequency = 0
AgilentNASweepTypeLogFrequency = 1
AgilentNASweepTypeSegment = 2
AgilentNASweepTypePower = 3
AgilentNASweepTypeCWTime = 4


# values for enumeration 'AgilentNATriggerModeEnum'
AgilentNATriggerModeHold = 1
AgilentNATriggerModeContinuous = 0
 
    AgilentNALib.AgilentNATriggerModeContinuous
    AgilentNALib.AgilentNATriggerModeHold
    meas=VNA.Channels["Channel1"].Measurements["Measurement1"]
    VNA.Channels["Channel1"].SweepTime

VNA.Channels["Channel1"].SweepTimeAuto
VNA.Channels["Channel1"].SweepType
VNA.Channels["Channel1"].SweepMode

    meas.Create(1,1)
    meas.Format=0
    meas.FetchComplex()
    meas.FetchX()
    meas.Trace.AutoScale()
    
    VNA.Channels["Channel1"].TriggerMode


    print help(VNA)#.Channels)
    print VNA.Channels['Channel1'].SourcePower.Level[1]
    #print dir(VNA.Channels['Channel1'].SourcePower.Level)
    #print help(VNA.Channels['Channel1'].SourcePower.Level)

    VNA.Channels['Channel1'].SourcePower.Level[1]=-27

    print VNA.Channels['Channel1'].SourcePower.Level(1)
    print dir(VNA)
    
    print VNA.Channels["Channel1"].IFBandwidth

    #print help(VNA)
    #print VNA.Identity.InstrumentModel
    #>>> PS2.Output.VoltageLimit = 5
    #>>> PS2.Output.CurrentLimit = 1
    #>>> PS2.Output.Enabled = True
    #>>> PS2.Output.MeasureVoltage( )
    #5.0019999999999998
    #>>> PS2.Identity.InstrumentModel
    #u'GEN30-25-IEMD'
    #>>> PS2.Utility.Reset( )
    #0

    VNA.Close( )
    
    VNA.Release( ) 
#import visa
#VNA = visa.instrument("TCPIP::129.16.115.134::5025::SOCKET")
#print(keithley.ask("*IDN?"))

#import visa
#rm = visa.ResourceManager()
#keithley = rm.open_resource("TCPIP::129.16.115.134::5025::SOCKET")
#print dir(keithley)
#keithley.read_termination="\r\n" #visa.CR+visa.LF
#keithley.write_termination="\r\n"
#
#print keithley.resource_info
#print keithley.open()
#print dir(keithley)
#print keithley.visa_attributes_classes
#print keithley.get_visa_attribute('AttrVI_ATTR_TERMCHAR')
##print(keithley.query("*IDN?"))
#print keithley.close()
#rm.close()