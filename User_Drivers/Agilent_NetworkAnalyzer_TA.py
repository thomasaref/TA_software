#!/usr/bin/env python
"""Driver using IVI-COM. 
Make sure IVI-COM driver from Agilent/Keysight for VNA is installed as well as it's prerequisites, 
typically Keysight IO Suites and some form of VISA.
if compiling fails, try the GetModule command"""

#import InstrumentDriver
from InstrumentDriver import InstrumentWorker, CommunicationError
#from VISA_Driver import VISA_Driver
from InstrumentConfig import InstrumentQuantity
from numpy import log10, array
import numpy as np
#import visa
from comtypes.client import CreateObject#, GetModule
#from pythoncom import CoInitialize
from comtypes import CoInitialize


#Ensure module is created before importing
#Back up code to create module:
#GetModule("AgNA.dll")
try:
    import comtypes.gen.AgilentNALib as AgilentNALib
except ImportError:
    VNA=CreateObject('AgilentNA.AgilentNA')
    VNA.Release()
    import comtypes.gen.AgilentNALib as AgilentNALib


def cached_property(default_func):
    """a cached property decorator. only resets when set to None"""
    def get_value(self):
        if get_value.value is None:
            get_value.value=default_func(self)
        return get_value.value
    get_value.value=None

    def set_value(self, value):
        get_value.value=value
        
    return property(get_value, set_value)

def get_attr(self, name):
    obj=self
    for x in name.split('.'):
        obj = getattr(obj, x)
    return obj

def return_value(value):
    return value
    
class Prop(object):
    """Helper class for accessing instrument properties"""
    def __init__(self, obj, name, index=None, default=None, coercer=return_value):
        self.value=default
        self.index=index
        self.name=name
        self.obj=obj
        self.coercer=coercer
        
    #def __call__(self, instr, outside_name=None):
    #    if outside_name is None:
    #        outside_name=self.name
        #self.value=instr.getValue(self.name)
    #    instr.prop_dict[self.name]=outside_name
        #self.instr=instr
        
    def receive(self):
        if self.index is None:
            self.value=self.coercer(getattr(self.obj, self.name))
        else:
            self.value=self.coercer(getattr(self.obj, self.name)[self.index])
        #self.instr.log(self.value)
        return self.value

    def send(self, value):
        #self.instr.log("send {}".format(value))
        self.value=self.coercer(value)
        if self.index is None:
            setattr(self.obj, self.name, self.value)
        else:
            getattr(self.obj, self.name)[self.index]=self.value
        return self.value
            
def invert_dict(indict):
    return {obj:key for key, obj in indict.iteritems()}

#def add_inverse(indict):
#    return indict.update(invert_dict(indict))

def get_prop_dict(obj):
    prop_dict={}
    for name in dir(obj):
        if name not in dir(obj.__class__):
            if not name.startswith("_"):
                attr=getattr(obj, name)
                if isinstance(attr, Prop):
                    prop_dict[name]=attr
    #prop_dict.update(invert_dict(prop_dict))
    return prop_dict

def get_mapping(indict):
    def new_func(name):
        return indict.get(name, None)
    return new_func
 
TriggerModeDict={"Continuous" : AgilentNALib.AgilentNATriggerModeContinuous,
                 "Hold"       : AgilentNALib.AgilentNATriggerModeHold}
TriggerModeDict.update(invert_dict(TriggerModeDict))
                 
SweepModeDict = {'Swept'       :    AgilentNALib.AgilentNASweepModeSwept,
                 'Stepped'     :    AgilentNALib.AgilentNASweepModeStepped,
                 'FastStepped' :    AgilentNALib.AgilentNASweepModeFastStepped,
                 'FastSwept'   :    AgilentNALib.AgilentNASweepModeFastSwept}
SweepModeDict.update(invert_dict(SweepModeDict)) 

SweepTypeDict = {'LinFrequency' : AgilentNALib.AgilentNASweepTypeLinFrequency,
                 'LogFrequency' : AgilentNALib.AgilentNASweepTypeLogFrequency,
                 'Segment'      : AgilentNALib.AgilentNASweepTypeSegment,
                 'Power'        : AgilentNALib.AgilentNASweepTypePower,
                 'CWTime'       : AgilentNALib.AgilentNASweepTypeCWTime}
SweepTypeDict.update(invert_dict(SweepTypeDict)) 
            
__version__ = "0.0.1"

#class Error(Exception):
#    pass

class Driver(InstrumentWorker):
    """ This class implements the Agilent 5230 PNA driver"""

    @cached_property
    def cData(self):
        return {} #self.acquire_data()
    
    @cached_property
    def t0(self):
        return self.StartFrequency.receive()
    
    @cached_property
    def dt(self):
        return (self.StopFrequency.receive()-self.StartFrequency.receive())/(self.Points.receive()-1)  

    @cached_property
    def S_enabled(self):
        return {name[:3] : self.getValue(name) for name in self.S_enabled_names}

    @cached_property
    def S_enabled_names(self):
        return tuple('{0} - Enabled'.format(name) for name in self.measDict)
        
        
    #@property
    #def eSweepType(self):
    #    return self.getValue('Sweep type')
        
    #@property
    #def fStartFrequency(self):
    #    startFreq = self.getValue("Start frequency")
    #    if self.eSweepType == 'Log':
    #        return log10(startFreq)
    #    return startFreq

    #@property
    #def fStopFrequency(self):
    #    stopFreq=self.getValue("Stop frequency")
    #    if self.eSweepType == 'Log':
    #        return log10(stopFreq) 
    #    return stopFreq

    #@property
    #def bWaitTrace(self):
    #    return self.getValue('Wait for new trace')

    #@property    
    #def bAverage(self):
        #return self.ch1.Averaging
    #    return self.getValue('Average')
                    
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

    def acquire_data(self):
        self.ch1.ClearAverage()
        if self.Averaging.value:
            numTriggers=self.AveragingFactor.value
        else:
            numTriggers=1
        self.log(numTriggers)
        for n in range(numTriggers):
            #if self.needs_abort:
            #    break
            self.log(n)
            self.log(self.ch1.TriggerSweep(1000))
            self.log(self.VNA.System2.WaitForOperationComplete(10000))
        for key in self.measDict:
            self.log((key, self.S_enabled[key]))
            if self.S_enabled[key]:
                data=array(self.measDict[key].FetchComplex())
                self.cData[key]=data[0]+1.0j*data[1]
                if 0:
                    self.measDict[key].FetchX()
                    self.measDict[key].Trace.AutoScale()
        #self.needs_abort=False
        
    def VNAabort(self):
        self.VNA.Channels.Abort()
        self.VNA.Status.Clear()
        self.writeVNA("CALC:PAR:DEL:ALL")
        self.ch1.TriggerMode=TriggerModeDict['Hold']
        #self.needs_abort=True
                
    def performOpen(self, options={}):
        """Perform the operation of opening the instrument connection. Initializes a measurement param dictionary
        and calls the generic VISA_Driver open
        Calls an IVI-COM driver. importing of library is delayed"""
        
        CoInitialize()
        self.VNA=CreateObject('AgilentNA.AgilentNA')
        self.log("VNA object created")
        self.VNA.Initialize( "TCPIP::129.16.115.134::5025::SOCKET", False, False, "")
        self.log("VNA Initialized")
        
        self.ch1=self.VNA.Channels["Channel1"]
        self.VNAabort()
        #self.needs_abort=False
        self.measDict=dict(S11=self.ch1.Measurements["Measurement1"],
                           S21=self.ch1.Measurements["Measurement2"],
                           S12=self.ch1.Measurements["Measurement3"],
                           S22=self.ch1.Measurements["Measurement4"])
        #sAll=self.askVNA("CALC:PAR:CAT:EXT?")
        #t=sAll[1:-1].split(",")
        #self.log({t[i]:t[i+1] for i in range(0, len(t), 2)})  
        #
        #self.ch1.TriggerMode=TriggerModeDict['Hold']                       
        #self.prop_dict={}
        self.Averaging=Prop(self.ch1, 'Averaging')
        self.IFBandwidth=Prop(self.ch1, 'IFBandwidth')
        self.Points=Prop(self.ch1, "Points", coercer=int)
        self.AveragingFactor=Prop(self.ch1, "AveragingFactor", coercer=int)
        self.StopFrequency=Prop(self.ch1.StimulusRange, "Stop")
        self.StartFrequency=Prop(self.ch1.StimulusRange, "Start")
        self.Span=Prop(self.ch1.StimulusRange, "Span")
        self.CenterFrequency=Prop(self.ch1.StimulusRange, "Center")
        self.OutputPower=Prop(self.ch1.SourcePower, "Level", 1)
        #self.OutputPower2=Prop(self.ch1.SourcePower, "Level", 2)
        self.prop_dict=get_prop_dict(self)
        for key in self.prop_dict:
            getattr(self, key).value=self.getValue(key)

        #self.prop_mapping=get_mapping(prop_dict)
                    
        #self.log(self.prop_dict)
        #VNA.Channels["Channel1"].SweepTimeAuto
        #VNA.Channels["Channel1"].SweepType
        #VNA.Channels["Channel1"].SweepMode

        #VNA.Channels["Channel1"].SweepTime    
#    
#        meas.Create(1,1)
#        meas.Format=0

#        
#        VNA.Channels["Channel1"].TriggerMode
    def performClose(self, bError=False, options={}):
        self.VNAabort()
        self.VNA.Close( )
        self.log("VNA Closed")
        self.VNA.Release()
        self.log("VNA object released")
        
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation. This function should
        return the actual value set by the instrument. Runs standard VISA set except
        for enabling S parameters and wait for new trace"""
        attr=getattr(self, quant.name, None)
        if attr is not None:
            return attr.send(value)
        elif quant.name == "Output enabled":
            if value:
                self.writeVNA(":OUTP 1")
            else:
                self.writeVNA(":OUTP 0")
        
        elif quant.name in self.S_enabled_names:
            key=quant.name[:3]
            if value:
                ReceiverPort=int(key[1])
                SourcePort=int(key[2])
                self.log((ReceiverPort, SourcePort))
                self.measDict[key].Create(ReceiverPort, SourcePort)
                self.measDict[key].Format=0
            else:
                if self.S_enabled[key]:
                    self.measDict[key].Delete()
            self.S_enabled[key]=value
        elif quant.name == "Abort":
            self.abort()
                # old-type handling of traces
                #if param in self.dMeasParam:
                    # clear old measurements for this parameter
                #    for name in self.dMeasParam[param]:
                #        self.writeVNA("CALC:PAR:DEL '{0}'".format(name))
                # create new measurement, if enabled is true
                #if value:
                #    newName = 'LabC_{0}'.format(param)
                #    self.writeVNA("CALC:PAR:EXT '{0}','{1}'".format(newName, param))
                #    iTrace = 1 + ['S11', 'S21', 'S12', 'S22'].index(param)
                #    self.writeVNA("DISP:WIND:TRAC{0}:FEED '{1}'".format(iTrace, newName))
                #    self.dMeasParam[param] = [newName]
    #        self.hw_write("DISP:WINDow1:TRACe:DELete")
    #        self.hw_write("CALCulate1:PARameter:DEFine 'MyMag', {}".format(self.measurement_type))
    #        self.hw_write("DISPlay:WINDow1:TRACe1:FEED 'MyMag'")
    #        self.hw_write("CALCulate1:PARameter:SELect 'MyMag'")
    #        self.hw_write("CALCulate1:FORMat MLOG")
    #        self.hw_write("CALCulate1:PARameter:DEFine 'MyPhase', {}".format(self.measurement_type))
    #        self.hw_write("DISPlay:WINDow1:TRACe2:FEED 'MyPhase'")
    #        self.hw_write("CALCulate1:PARameter:SELect 'MyPhase'")
    #        self.hw_write("CALCulate1:FORMat PHASe")
            #elif quant.name in ("Wait for new trace",):
            #    self.log(options)
            #elif quant.name not in ('Wait for new trace',):
                # run standard VISA case
            #    value = VISA_Driver.performSetValue(self, quant, value, sweepRate, options)
        return value


    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation"""
        self.log(options)
        self.log(self.isFirstCall(options))

        attr=getattr(self, quant.name, None)
        if attr is not None:
            return attr.receive()
        elif quant.name == "Output enabled":
            return bool(int(self.askVNA(":OUTP?")))
        elif quant.name in self.S_enabled_names:            
            key=quant.name[:3]#('S11 - Enabled', 'S21 - Enabled', 'S12 - Enabled', 'S22 - Enabled'):
            return self.S_enabled[key]
            #return self.getValue(quant.name)                  
                # update list of channels in use
                #self.getActiveMeasurements()
                # get selected parameter
                #param = quant.name[:3]
                #value = param in self.dMeasParam
        elif quant.name in self.measDict: #('S11', 'S21', 'S12', 'S22'):
            if self.isFirstCall(options):
                #resets cData on first call
                self.cData=None
            if quant.name not in self.cData:
                #resets cData if parameter not in data
                self.acquire_data()
            data=self.cData.get(quant.name, [])
            #if data==[]:
            #    return InstrumentQuantity.getTraceDict()
            #if quant.name in self.cData:
            self.log(InstrumentQuantity.getTraceDict.__doc__)
            return InstrumentQuantity.getTraceDict(data, t0=self.t0, dt=self.dt)
            #else:
                    # not enabled, return empty array
                #    value = InstrumentQuantity.getTraceDict([])
                #return self.cData[quant.name]
                    #if options.get("call_no", 0)==0:
                    #self.dMeasParam={}
                    # check if channel is on
                    #if quant.name not in self.dMeasParam:
                    # get active measurements again, in case they changed
                #    self.getActiveMeasurements()
                #if quant.name in self.dMeasParam:
                #    if self.getModel() in ('E5071C',):
                        # new trace handling, use trace numbers
                #        self.writeVNA("CALC:PAR%d:SEL" % self.dMeasParam[quant.name])
                #    else:
                        # old parameter handing, select parameter (use last in list)
                #        sName = self.dMeasParam[quant.name][-1]
                #        self.writeVNA("CALC:PAR:SEL '%s'" % sName)
                    # if not in continous mode, trig from computer
                #    bWaitTrace = self.getValue('Wait for new trace')
                #    bAverage = self.getValue('Average')
                    # wait for trace, either in averaging or normal mode
                #    if bWaitTrace:
                #        if bAverage:
                            # set channels 1-4 to set event when average complete (bit 1 start)
                #            self.writeVNA(':SENS:AVER:CLE;:STAT:OPER:AVER1:ENAB 30;:ABOR;:SENS:AVER:CLE;')
                #        else:
                #            self.writeVNA(':ABOR;:INIT:CONT OFF;:INIT:IMM;')
                #            self.writeVNA('*OPC')
                        # wait some time before first check
                #        self.thread().msleep(30)
                #        bDone = False
                #        while (not bDone) and (not self.isStopped()):
                            # check if done
                #            if bAverage:
                #                sAverage = self.askVNA('STAT:OPER:AVER1:COND?')
                #                bDone = int(sAverage)>0
                #            else:
                #                stb = int(self.askVNA('*ESR?'))
                #                bDone = (stb & 1) > 0
                #            if not bDone:
                #                self.thread().msleep(100)
                        # if stopped, don't get data
                #        if self.isStopped():
                #            self.writeVNA('*CLS;:INIT:CONT ON;')
                #            return []
                    # get data as float32, convert to numpy array
                #    if self.getModel() in ('E5071C',):
                #        # new trace handling, use trace numbers
                #        self.writeVNA(':FORM:DATA REAL32;:CALC:SEL:DATA:SDAT?')#, bCheckError=False)
                #    else:
                        # old parameter handing
               #         self.writeVNA(':FORM REAL,32;CALC:DATA? SDATA')#, bCheckError=False)
               #     sData = self.readVNA()#ignore_termination=True)
               #     self.log(sData)
               #     if bWaitTrace and not bAverage:
               #         self.writeVNA(':INIT:CONT ON;')
                    # strip header to find # of points
               #     i0 = sData.find('#')
               #     nDig = int(sData[i0+1])
               #     nByte = int(sData[i0+2:i0+2+nDig])
               #     nData = nByte/4
               #     nPts = nData/2
                    # get data to numpy array
               #     vData = np.frombuffer(sData[(i0+2+nDig):(i0+2+nDig+nByte)],
               #                           dtype='>f', count=nData)
                    # data is in I0,Q0,I1,Q1,I2,Q2,.. format, convert to complex
#                    mC = vData.reshape((nPts,2))
#                    vComplex = mC[:,0] + 1j*mC[:,1]
#                    # get start/stop frequencies
#                    startFreq = self.fStartFrequency #self.readValueFromOther('Start frequency')
#                    stopFreq = self.fStopFrereadValueFromOther('Stop frequency')
#                    sweepType = self.readValueFromOther('Sweep type')
#                    # if log scale, take log of start/stop frequencies
#                    if sweepType == 'Log':
#                        startFreq = np.log10(startFreq)
#                        stopFreq = np.log10(stopFreq)
#                    # create a trace dict
#                    value = InstrumentQuantity.getTraceDict(vComplex, t0=startFreq,
#                                                   dt=(stopFreq-startFreq)/(nPts-1))
#                else:
#                    # not enabled, return empty array
#                    value = InstrumentQuantity.getTraceDict([])
            #elif quant.name in ('Wait for new trace',):
                # do nothing, return local value
            #    value = quant.getValue()
            #else:
                # for all other cases, call VISA driver
            #    value = VISA_Driver.performGetValue(self, quant, options)
        return value


#    def getActiveMeasurements(self):
#        """Retrieve and a list of measurement/parameters currently active"""
#        # proceed depending on model
#        #sAll = self.askAndLog(
#        sAll=self.askVNA("CALC:PAR:CAT:EXT?")
#        t=sAll[1:-1].split(",")
#        {t[i+1]:t[i] for i in range(0, len(t), 2)}
#
#        # strip "-characters
#        sAll = sAll[1:-1]
#        # parse list, format is channel, parameter, ...
#        self.dMeasParam = {}
#        lAll = sAll.split(',')
#        nMeas = len(lAll)//2
#        for n in range(nMeas):
#            sName = lAll[2*n]
#            sParam = lAll[2*n + 1]
#            if sParam not in self.dMeasParam:
#                # create list with current name
#                self.dMeasParam[sParam] = [sName,]
#            else:
#                # add to existing list
#                self.dMeasParam[sParam].append(sName)

#    def hw_get_trace(self):
#        avg_state = int(self.hw_ask("""SENSe1:AVERage:STATe?"""))
#        if avg_state:
#            num_avg = int(self.hw_ask("""SENSe1:AVERage:COUNt?"""))
#        else:
#            num_avg = 1
#        #num_pt = self.hw_ask("SENSe1:SWEep:POIN?")
#        self.hw_write("SENSe1:SWE:GRO:COUN {:d}".format(num_avg))
#        self.hw_write("ABORT") self.VNA.Channels.Abort()
#        self.hw_write("SENSe1:AVERage:CLEar") #VNA.Channels["Channel1"].ClearAverage()
#        self.hw_write("SENSe1:SWE:MODE GROUPS")
#        #freq = np.linspace(self.start_freq, self.stop_freq, self.points)
#        done = False
#
#        while not done:
#            try:
#                done = int(self.hw_ask("*OPC?"))
#            except:
#                pass
#        self.hw_write("CALCulate1:PARameter:SELect 'MyMag'")
#        self.hw_write("FORMat:DATA REAL,32")
#        #mag = Series(self.hw_ask_data("CALCulate1:DATA? FDATA"), index = freq)
#        #mag = DataTrace('Mag', data = self.hw_ask_data("CALCulate1:DATA? FDATA"), indep = freq)
#        mag_array = np.array(self.hw_ask_data("CALCulate1:DATA? FDATA"))
#        self.hw_write("CALCulate1:PARameter:SELect 'MyPhase'")
#        self.hw_write("FORMat:DATA REAL,32")
#        #phase = Series(self.hw_ask_data("CALCulate1:DATA? FDATA"), index = freq)
#        #phase = DataTrace('Phase', data = self.hw_ask_data("CALCulate1:DATA? FDATA"), indep = freq)
#        phase_array = np.array(self.hw_ask_data("CALCulate1:DATA? FDATA"))
#        self.mag.y.data = mag_array
#        self.phase.y.data = phase_array
#        self.compensated_mag.y.data = mag_array - self.background_mag.y.data
#        print("Measurement done!")
#        self.trace_ready = True

if __name__ == '__main__':
    pass
