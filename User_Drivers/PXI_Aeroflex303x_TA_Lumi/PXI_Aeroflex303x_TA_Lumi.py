#!/usr/bin/env python

if 1:
    import InstrumentDriver
    from InstrumentConfig import InstrumentQuantity
else:
    import fakeInstrumentDriver as InstrumentDriver
    from fakeInstrumentConfig import InstrumentQuantity
import afdigitizer
reload(afdigitizer)
from afdigitizer import afDigitizer
import numpy as np
from time import time
 
__version__ = "0.0.1"
class Driver(InstrumentDriver.InstrumentWorker):
    """ This class implements a digitizer in the PXI rack"""

    digname_map={"RF Frequency"     : "frequency",
                 'Max input level'  : "input_level",
                 'Sampling rate'    : "sample_rate",
                 'LO Reference Mode': "LO_reference",
                 "Trigger Source"   : "trigger_source",
                 "Number of pretrigger samples": "pre_edge_trigger_samples",
                 "Timeout"          : "reclaim_timeout",
                 "Number of samples" : "num_samples",
                 "Averages per trigger" : "avgs_per_trig",
                 "Number of triggers"  : "num_trigs",
                 'LO Above or Below': "LO_position",
                 "Total number of samples" : "total_samples",
                 "Sampling time" : "sampling_time",
                 "Remove DC offset" : "dc_offset_remove",
                 }
            
    def performOpen(self, options={}):
        """Perform the operation of opening the instrument connection
            creates the object, clears data holders, boots instrument and sets modulation mode to generic"""
        
        try:
            self.log("before create")
            self.digitizer=afDigitizer()
            self.digitizer.parent=self
            self.digitizer.start_dig(lo_address=self.getValue('Local oscillator VISA'),
                                     dig_address=self.dComCfg['address'],
                                     lo_reference=self.getValue("LO Reference Mode"))
            self.log("after create")
            self.digitizer.pipelining_enable=True
            self.cTrace = None
            self.bBufferRead = self.getValue("Buffer read")
            self.fLevelCorrection=self.digitizer.level_correction
        except Exception as e:
            raise InstrumentDriver.CommunicationError(str(e))


    def performClose(self, bError=False, options={}):
        """Perform the close instrument connection operation.
            Checks if digitizer object exists (in case it was never opened)
            destroys object and deletes it"""
        if hasattr(self, 'digitizer'):
            try:
                self.digitizer.stop_dig()
                self.log('digitizer closed')
            except Exception as e:
                if not bError:
                    raise InstrumentDriver.CommunicationError(str(e))
            finally:
                try:
                    del self.digitizer
                    self.log('digitizer object successfully destroyed')
                except Exception as e:
                    raise InstrumentDriver.CommunicationError(str(e))

        
    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation. This function should
        return the actual value set by the instrument"""
        self.cTrace=None
        #self.log(type(quant.getValueString(value)))
        #self.log((quant.name, quant.datatype))


        try:
            if quant.name in self.digname_map:
                self.log((quant.name, value))
                if getattr(getattr(afDigitizer, self.digname_map[quant.name]), "fset", True) is not None:
                    if quant.datatype==2:
                        value=quant.getValueString(value)
                    setattr(self.digitizer, self.digname_map[quant.name], value)
               # except AttributeError:
               #     pass
#            elif quant.name == 'Cut out part of the trace':
#                self.bCutTrace = value    
#            elif quant.name == 'Start Sample':
#                self.nStartSample = int(value)
#            elif quant.name == 'Stop Sample':
#                self.nStopSample = int(value)
#            elif quant.name == 'Histogram path':
#                self.sHistPath = str(value)
#            elif quant.name == 'Histogram bin number':
#                self.nBins = value
#            elif quant.name == 'Collect IQ Histogram':
#                self.bCollectHistogram = value
#            elif quant.name == 'Remove DC offset':
#                self.digitizer.rf_remove_dc_offset_set(bool(value))
#                # combo, get index
                #if isinstance(value, (str, unicode)):
                #    valueIndex = quant.combo_defs.index(value)
                #else:
                #    valueIndex = long(value)
                #self.digitizer.trigger_source_set(valueIndex)             
#            elif quant.name == 'Trigger type':
#                # Dont do for SW
#                TriggerSourceValue = self.digitizer.trigger_source_get()
#                if TriggerSourceValue is not 32:                
#                    # combo, get index
#                    if isinstance(value, (str, unicode)):
#                        valueIndex = quant.combo_defs.index(value)
#                    else:
#                        valueIndex = int(value)
#                    self.digitizer.trigger_type_set(valueIndex)
#            elif quant.name == 'Trigger polarity':
#                 # Dont do for SW
#                TriggerSourceValue = self.digitizer.trigger_source_get()
#                if TriggerSourceValue is not 32: 
#                # combo, get index
#                    if isinstance(value, (str, unicode)):
#                        valueIndex = quant.combo_defs.index(value)
#                    else:
#                        valueIndex = int(value)
#                    self.digitizer.trigger_polarity_set(valueIndex)
            #elif quant.name=="Timeout":
            #    self.digitizer.capture_iq_reclaim_timeout_set(int(value))                
#                self.digitizer.trigger_pre_edge_trigger_samples_set(int(value))
#            #Only return I and Q vectors if needed, could be a big vector if many triggers and samples
            elif quant.name == "Buffer read":
                self.bBufferRead = value
#            elif quant.name == 'Retrieve raw data':
#                self.bRaw = value
            #elif quant.name == 'LO Reference Mode':
            #    # combo, get index
            #    if isinstance(value, (str, unicode)):
            #        valueIndex = quant.combo_defs.index(value)
            #    else:
            #        valueIndex = int(value)
            #    self.digitizer.lo_reference_set(valueIndex)
            #elif quant.name == 'LO Above or Below':
            #    # combo, get index
            #    if isinstance(value, (str, unicode)):
            #        valueIndex = quant.combo_defs.index(value)
            #    else:
            #        valueIndex = int(value)
                #self.digitizer.rf_userLOPosition_set(valueIndex)
#         
#            elif quant.name == 'Set IQ Bandwidth manually': 
#                self.bSetBandWidth = value
#            elif quant.name == 'IQ Bandwidth':
#                self.dBandWidthAim = value
#                self.bSetBandWidth = self.getValue('Set IQ Bandwidth manually')
#                if self.bSetBandWidth:
#                    self.dBandWidthAcc = self.digitizer.trigger_IQ_bandwidth_set(self.dBandWidthAim,self.nAbove)
#            elif quant.name == 'Bandwidth above or below': 
#                if isinstance(value, (str, unicode)):
#                    valueIndex = quant.combo_defs.index(value)
#                else:
#                    valueIndex = int(value)
#                self.nAbove = valueIndex
#                self.bSetBandWidth = self.getValue('Set IQ Bandwidth manually')
#                if self.bSetBandWidth:
#                    self.dBandWidthAcc = self.digitizer.trigger_IQ_bandwidth_set(self.dBandWidthAim,self.nAbove)
#                
            return value
        except Exception as e:
            raise InstrumentDriver.CommunicationError(str(e))


    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation. Resets cTrace on call number zero"""
        try:
            if quant.name in self.digname_map:
                if getattr(getattr(afDigitizer, self.digname_map[quant.name]), "fget", True) is not None:
                    value= getattr(self.digitizer, self.digname_map[quant.name])
            #elif quant.name == 'Total number of samples':
            #    return self.digitizer.total_samples #nTotalSamples  
            #elif quant.name == 'Sampling time':
            #    self.log(quant.name)
            #    return self.digitizer.sampling_time #fSamplingTime
#            elif quant.name == 'Cut out part of the trace':
#                value = self.bCutTrace
#            elif quant.name == 'Start Sample':
#                value = self.nStartSample
#            elif quant.name == 'Stop Sample':
#                value = self.nStopSample
#            elif quant.name == 'Remove DC offset':
#                value = self.digitizer.rf_remove_dc_offset_get()
            #elif quant.name == 'Trigger type':
            #    value = self.digitizer.trigger_type_get()
            #    return quant.getValueString(value)
            #elif quant.name == 'LO Above or Below':
            #    value = self.digitizer.rf_userLOPosition_get()
            #    return quant.getValueString(value)
#            elif quant.name == 'Trigger polarity':
#                value = self.digitizer.trigger_polarity_get()
#                value = quant.getValueString(value)
            elif quant.name == "Buffer read":
                return self.bBufferRead
#            elif quant.name == 'Collect IQ Histogram':
#                value = self.bCollectHistogram
#            elif quant.name == 'Retrieve raw data':
#                value = self.bRaw
#            elif quant.name == 'Histogram bin number':
#                value = self.nBins
#            elif quant.name == 'Histogram path':
#                value = self.sHistPath
            elif quant.name == 'Trace':
                return self.getTraceDict()   
            elif quant.name == 'LC Trace':
                tstart=time()
                self.getTraceDict()
                self.log(time()-tstart)
                return {'y' : self.cTrace['y']*np.power(10.0, self.fLevelCorrection/20.0),
                        'dt': self.cTrace['dt'],
                        't0': self.cTrace['t0']}

#            elif quant.name == 'Power trace':
#                value = self.getTraceDict(self.getPTrace())
#            elif quant.name == 'AvgTrace':
#                value = self.getTraceAvg()
#            elif quant.name == 'Power mean unaveraged':
#                value = self.getPowerMeanUnAvg()
#            elif quant.name == 'Voltage mean unaveraged':
#                value = self.getMeanUnAvg()    
#            # Only return I and Q vectors if needed, could be a big vector if many triggers and samples
#            elif quant.name == 'Raw data':
#                if self.bRaw:
#                    value = self.getRawData()
#            elif quant.name == 'IQ Bandwidth':
#                value = self.dBandWidthAcc
#            elif quant.name == 'Bandwidth above or below': 
#                #value = quant.getValueString(self.nAbove)
#                value = 0
#            elif quant.name == 'Set IQ Bandwidth manually':
#                value = self.bSetBandWidth
#            elif quant.name == 'AvgPower':
#                value = self.getAvgPower()
            elif quant.name == 'Level correction':
                self.fLevelCorrection=self.digitizer.level_correction
                return self.fLevelCorrection
            return value
        except Exception as e:
            raise InstrumentDriver.CommunicationError(str(e))

    def getTraceDict(self):
        """Return the signal along with its time vector"""
        if self.cTrace is None:
            sampling_rate=self.getValue("Sampling rate")
            num_pretriggers=self.getValue("Number of pretrigger samples")
            self.checkADCOverload()
            if self.bBufferRead:
                self.cTrace=InstrumentQuantity.getTraceDict(self.digitizer.buffer_capture(), 
                                t0=-num_pretriggers/sampling_rate, dt=1/sampling_rate)
            else:
                self.cTrace=InstrumentQuantity.getTraceDict(self.digitizer.full_captmem(), 
                                t0=-num_pretriggers/sampling_rate, dt=1/sampling_rate)                    
        return self.cTrace
                                               
#    # Check if the ADC overloaded and if it was put the max input level to +30dBm and raise an error
    def checkADCOverload(self):
        if self.digitizer.ADC_overload: #check_ADCOverload():
            self.log('ADC Overload!', 30)
#            self.nOverloads = self.nOverloads + 1
#        else:
#		self.nOverloads = 0
#  
#        if self.nOverloads > 3:
#            self.digitizer.rf_rf_input_level_set(30)
#            raise InstrumentDriver.CommunicationError('ADC overloaded three times hence the measurement is stopped and the max input level on the digitizer is put to +30 dBm')
#            
#            
#        
#    def getPTrace(self):
#        """Return the power in time as a vector, resample the signal if needed"""
#        # check if old value exists
#        if self.vPTrace is None:
#            # get new trace
#            self.sampleAndAverage()
#        # return and clear old value for selected signal
#        vTrace = self.vPTrace
#        self.vPTrace = None
#        return vTrace
#
#    def getRawData(self):
#        """Return the raw unaveraged data, if needed resample the signal"""
#        # check if old value exists
#        if self.cRaw is None:
#            # get new trace
#            self.sampleAndAverage()
#        # return and clear old value for selected signal
#        vVector = self.cRaw
#        self.cRaw = None
#        return vVector    
#    
#    def getAvgPower(self):
#        """Return the averaged power in Watts, resample the signal if necessary"""
#        if self.dPower is None:
#            self.sampleAndAverage()
#        vPower = self.dPower
#        self.dPower = None
#        return vPower                     
#
#    def getTraceAvg(self):
#        """Return the averaged signal as a complex number I+j*Q, resample the signal if necessary"""
#        # check if old value exists
#        if self.cAvgSignal is None:
#            self.sampleAndAverage()
#        # return and clear old value for selected signal
#        value = self.cAvgSignal
#        self.cAvgSignal = None
#        return value  
#        
#    def getPowerMeanUnAvg(self):
#        """Return the unaveraged power mean, resample the signal if necessary"""
#        # check if old value exists
#        if self.vPowerMeanUnAvg is None:
#            self.sampleAndAverage()
#        # return and clear old value for selected signal
#        value = self.vPowerMeanUnAvg
#        self.vPowerMeanUnAvg = None
#        return value
#        
#    def getMeanUnAvg(self):
#        """Return the unaveraged voltage mean, resample the signal if necessary"""
#        # check if old value exists
#        if self.vMeanUnAvg is None:
#            self.sampleAndAverage()
#        # return and clear old value for selected signal
#        value = self.vMeanUnAvg
#        self.vMeanUnAvg = None
#        return value  
#                          
    def sample(self):
        self.checkADCOverload()
        self.log(self.TriggerSource)
        if self.TriggerSource not in(32, 'SW_TRIG'):        
            self.digitizer.trigger_arm_set(self.nTotalSamples*2)
        i_avgd = np.zeros(self.nSamples)
        q_avgd = np.zeros(self.nSamples)            
        #vI = np.zeros(self.nStopSample-self.nStartSample+1)
        #vQ = np.zeros(self.nStopSample-self.nStartSample+1)  
        samples=self.nSamples
        avgs=self.nAverages_per_trigger
        total_samples=self.nTotalSamples
        two_total=2*self.nTotalSamples
        #self.log("acq started")
        for avgidx in range(0, self.nTriggers):
            if self.TriggerSource in(32, 'SW_TRIG'):
                while self.digitizer.data_capture_complete_get()==False:
                    self.thread().msleep(1)
                (lI, lQ) = self.digitizer.capture_iq_capt_mem(total_samples)
                if avgidx < (self.nTriggers-1):
                    self.digitizer.trigger_arm_set(two_total)
            else:
                (lI, lQ) = self.digitizer.capture_iq_capt_mem(total_samples)
            i_avgd += np.mean(np.array(lI).reshape(avgs, samples), axis=0)
            q_avgd += np.mean(np.array(lQ).reshape(avgs, samples), axis=0)
        #self.log("acq stopped")                
        i_avgd = i_avgd/self.nTriggers
        q_avgd = q_avgd/self.nTriggers
        cpx_avgd = i_avgd + 1j*q_avgd
        return cpx_avgd                
#            # The raw data is stored as a long array, continously appending the newly aquired data
#            if self.bRaw or self.bCollectHistogram:            
#                if i == 0:
#                    vectorI = np.array(lI)*np.power(10,dLevelCorrection/20)
#                    vectorQ = np.array(lQ)*np.power(10,dLevelCorrection/20)
#                else:
#                    vectorI = np.append(vectorI, np.array(lI)*np.power(10,dLevelCorrection/20))
#                    vectorQ = np.append(vectorQ, np.array(lQ)*np.power(10,dLevelCorrection/20))
#            
#           
#            # We add the aquired data to the vI and vQ arrays
#            # Fold the data  
#            reshapedI = np.array(lI).reshape(nAvgPerTrigger, self.nSamples+nPreTriggers)[:,range(self.nStartSample-1, self.nStopSample)]
#            reshapedQ = np.array(lQ).reshape(nAvgPerTrigger, self.nSamples+nPreTriggers)[:,range(self.nStartSample-1, self.nStopSample)]
#            vI = vI + np.mean(reshapedI, axis=0)
#            vQ = vQ + np.mean(reshapedQ, axis=0)
#            vI2 = vI2 + np.mean(reshapedI**2, axis=0)        
#            vQ2 = vQ2 + np.mean(reshapedQ**2, axis=0)   
#            vPowerMean[i*nAvgPerTrigger:(i+1)*nAvgPerTrigger] = np.mean(reshapedI**2, axis=1)+np.mean(reshapedQ**2, axis=1)
#            vIMean[i*nAvgPerTrigger:(i+1)*nAvgPerTrigger] = np.mean(reshapedI, axis=1)
#            vQMean[i*nAvgPerTrigger:(i+1)*nAvgPerTrigger] = np.mean(reshapedQ, axis=1)
#        
#        # Average the sum of vI and vQ using the number of triggers and do level correction
#        vI = vI/self.nTriggers*np.power(10,dLevelCorrection/20)
#        vQ = vQ/self.nTriggers*np.power(10,dLevelCorrection/20)
#        vIMean = vIMean*np.power(10,dLevelCorrection/20)
#        vQMean = vQMean*np.power(10,dLevelCorrection/20)
#        vI2 = vI2/self.nTriggers*np.power(10,dLevelCorrection/10)/1000 #why is this divided by 1000??
#        vQ2 = vQ2/self.nTriggers*np.power(10,dLevelCorrection/10)/1000
#        vPowerMean = vPowerMean*np.power(10,dLevelCorrection/10)/1000
#        
#        self.vMeanUnAvg = vIMean+1j*vQMean
#        # Create the time trace
#        self.cTrace = vI+1j*vQ            
            
#    def sampleAndAverage(self):
#        """Sample the signal, calc I+j*Q theta and store it in the driver object"""
#        self.checkADCOverload()
#        # Check which trigger source is being used
#        TriggerSourceValue = self.digitizer.trigger_source_get()
#        
#        # Convert the number of samples and triggers to integers
#        nPreTriggers = int(self.getValue('Number of pretrigger samples'))
#        nAvgPerTrigger = self.nAverages_per_trigger
#        nTotalSamples = self.nSamples*nAvgPerTrigger+nPreTriggers
#        dLevelCorrection = self.digitizer.rf_level_correction_get()
#        # If the stop sample is set to high, set it to nSamples
#        if self.bCutTrace:
#            if self.nStopSample > self.nSamples:
#                self.nStopSample = self.nSamples
#        else: #If we don't want to cut the trace, set start value to 1 and stop value to the last
#            self.nStartSample = 1
#            self.nStopSample = self.nSamples
#        
#        # If the Trigger source is not in 32 = SW trigger, we want to arm the trigger
#        if TriggerSourceValue is not 32:        
#            # Arm the trigger with 2*inSamples        
#            self.digitizer.trigger_arm_set(nTotalSamples*2)
#
#        
#        # Define two vectors that will be used to collect the raw data
#        vI = np.zeros(self.nStopSample-self.nStartSample+1)
#        vQ = np.zeros(self.nStopSample-self.nStartSample+1)         
#        vI2 = np.zeros(self.nStopSample-self.nStartSample+1)
#        vQ2 = np.zeros(self.nStopSample-self.nStartSample+1) 
#        vPowerMean = np.zeros(nAvgPerTrigger*self.nTriggers)
#        vIMean = np.zeros(nAvgPerTrigger*self.nTriggers)
#        vQMean = np.zeros(nAvgPerTrigger*self.nTriggers)
#        # For each trigger, we collect the data
#        for i in range(0, self.nTriggers):
#            
#            # number 32 corresponds to SW_TRIG, the only trigger mode without external signal             
#            if TriggerSourceValue is not 32:
#                while self.digitizer.data_capture_complete_get()==False:
#                    #Sleep some time in between checks
#                    self.thread().msleep(1)
#
#                
#                #Capture the I and Q data
#                (lI, lQ) = self.digitizer.capture_iq_capt_mem(nTotalSamples)
#                
#                #Re-arm the trigger to prepare the digitizer for the next iteration                                  
#                if i < (self.nTriggers-1):
#                    self.digitizer.trigger_arm_set(nTotalSamples*2)
#                
#            else:
#                #Capture the I and Q data for SW-trig
#                
#                (lI, lQ) = self.digitizer.capture_iq_capt_mem(nTotalSamples)
#                
#            # The raw data is stored as a long array, continously appending the newly aquired data
#            if self.bRaw or self.bCollectHistogram:            
#                if i == 0:
#                    vectorI = np.array(lI)*np.power(10,dLevelCorrection/20)
#                    vectorQ = np.array(lQ)*np.power(10,dLevelCorrection/20)
#                else:
#                    vectorI = np.append(vectorI, np.array(lI)*np.power(10,dLevelCorrection/20))
#                    vectorQ = np.append(vectorQ, np.array(lQ)*np.power(10,dLevelCorrection/20))
#            
#           
#            # We add the aquired data to the vI and vQ arrays
#            # Fold the data  
#            reshapedI = np.array(lI).reshape(nAvgPerTrigger, self.nSamples+nPreTriggers)[:,range(self.nStartSample-1, self.nStopSample)]
#            reshapedQ = np.array(lQ).reshape(nAvgPerTrigger, self.nSamples+nPreTriggers)[:,range(self.nStartSample-1, self.nStopSample)]
#            vI = vI + np.mean(reshapedI, axis=0)
#            vQ = vQ + np.mean(reshapedQ, axis=0)
#            vI2 = vI2 + np.mean(reshapedI**2, axis=0)        
#            vQ2 = vQ2 + np.mean(reshapedQ**2, axis=0)   
#            vPowerMean[i*nAvgPerTrigger:(i+1)*nAvgPerTrigger] = np.mean(reshapedI**2, axis=1)+np.mean(reshapedQ**2, axis=1)
#            vIMean[i*nAvgPerTrigger:(i+1)*nAvgPerTrigger] = np.mean(reshapedI, axis=1)
#            vQMean[i*nAvgPerTrigger:(i+1)*nAvgPerTrigger] = np.mean(reshapedQ, axis=1)
#        
#        # Average the sum of vI and vQ using the number of triggers and do level correction
#        vI = vI/self.nTriggers*np.power(10,dLevelCorrection/20)
#        vQ = vQ/self.nTriggers*np.power(10,dLevelCorrection/20)
#        vIMean = vIMean*np.power(10,dLevelCorrection/20)
#        vQMean = vQMean*np.power(10,dLevelCorrection/20)
#        vI2 = vI2/self.nTriggers*np.power(10,dLevelCorrection/10)/1000 #why is this divided by 1000??
#        vQ2 = vQ2/self.nTriggers*np.power(10,dLevelCorrection/10)/1000
#        vPowerMean = vPowerMean*np.power(10,dLevelCorrection/10)/1000
#        
#        self.vMeanUnAvg = vIMean+1j*vQMean
#        # Create the time trace
#        self.cTrace = vI+1j*vQ
#        self.vPTrace = (vI2+vQ2)
#        self.vPowerMeanUnAvg = vPowerMean
#        # Return the non averaged vectors if wanted
#        if self.bRaw:
#            self.cRaw = vectorI + 1j*vectorQ
#        
#        # If we want to collect IQ histogram        
#        if self.bCollectHistogram:
#            
#          vHistogram = self.CollectHistogram(self.nBins,vectorI, vectorQ)
#          
#          f = h5py.File('C:\\temp\\Histogram_' + str(int(self.getValue('Sampling rate'))) + 'Hz_' + time.strftime("%y_%m_%d_%H_%M_%S")+'.hdf5','w')
#          f.create_dataset('Histogram',data=vHistogram[0])
#          f.create_dataset('Iedges',data=vHistogram[1])
#          f.create_dataset('Qedges',data=vHistogram[2])
#          f.close()
#        # Remove the big vectors (if any)
#        if self.bRaw or self.bCollectHistogram:
#            vectorI = None
#            vectorQ = None
#
#        # Finally, we store the avgeraged signal     
#        self.cAvgSignal = np.average(vIMean)+1j*np.average(vQMean)
#        self.dPower = np.average(vI2)+np.average(vQ2)
#        
#    def CollectHistogram(self,nBins,vI,vQ):
#        
#        # Find maximum values in the vectors of I and Q to use for distributing the data in the histogram bins
#        vectorImax = np.max(np.abs(vI))
#        vectorQmax = np.max(np.abs(vQ))
#        
#        # Calculate a start value and step based on the maximum I or Q value and the number of bins
#        dStartValue = -np.max((vectorImax,vectorQmax))
#        dStep = (2*np.abs(dStartValue))/(self.nBins+1)
#            
#        # Construct the I and Q edge vectors for the histogram
#        Iedges = np.zeros(self.nBins+1)
#        Qedges = np.zeros(self.nBins+1)
#            
#        for i in range(0,len(Iedges)):
#            Iedges[i] = dStartValue + i*dStep
#            Qedges[i] = dStartValue + i*dStep
#        
#        #Next, we create a histogram with the raw I and Q data as input
#        H, Iedges, Qedges = np.histogram2d(vQ, vI, bins=(Iedges, Qedges))
#        
#        return [H, Iedges, Qedges]
#        
    def capture_to_buffer(self):
        self.checkADCOverload()
#        #TriggerSourceValue = self.digitizer.trigger_source_get()
#        self.nPreTriggers #= int(self.getValue('Number of pretrigger samples'))
#        self.nAverages_per_trigger
#        nTotalSamples = self.nSamples*nAvgPerTrigger+nPreTriggers
        #dLevelCorrection = self.digitizer.rf_level_correction_get()
#        
#        #pretrigger_samples = int(self.getValue('Number of pretrigger samples'))
#        sample_rate =self.getValue('Sampling rate')        
#        nSamples = int(self.getValue('Number of samples'))
#        t_data = np.linspace(-self.nPreTriggers, nSamples-pretrigger_samples, nSamples)/sample_rate #1.0e6
#        self.AvgTrace['AvgTrace - t'] = t_data
        #self.timeout=10
#        #ref_amplitude=-10.0
#        #center_frequency = 5.0e9 #Dig center frequency 'Hz'
#        #sample_rate = 250.0e6
#        #pretrigger_samples =200
#        #pretrigger_samples = int(self.getValue('Number of pretrigger samples'))
#        #sample_rate =self.getValue('Sampling rate')        
#        #inSamples = int(self.nSamples)
#        #samples =5000
#        self.nSamples = int(self.getValue('Number of samples'))
#        self.nAverages_per_trigger=int(self.getValue('Averages per trigger')) #2000
#        self.nTriggers = int(self.getValue('Number of triggers')) #       triggers_to_average=1
#
#        #trigger_source = 36 #front smb #32 #Software #"Software"# attr.trigsource_to_afdig)
#            #trigsource = Aeroflex_trigsource(attr.trigsource_to_afdig.keys())
#        #trigger_edge = 0 #"Rising" #, attr.trigedge_to_afdig)
#            #Aeroflex_trigedge(attr.trigedge_to_afdig.keys())
#
#   
#        #self.t_data = np.linspace(-pretrigger_samples, self.nSamples-pretrigger_samples, self.nSamples)/sample_rate #1.0e6
        #self.digitizer.capture_iq_reclaim_timeout_set(self.timeout*1000)
        #if self.nTotalSamples> afDigitizerWrapper.BUFFER_SIZE:
        #    raise InstrumentDriver.CommunicationError('The total number of samples exceeds the buffer size')
        
                
        i_avgd = np.zeros(self.nSamples)
        q_avgd = np.zeros(self.nSamples)
        samples=self.nSamples
        avgs=self.nAverages_per_trigger
        timeout=self.fTimeout
        tot_samps=int(self.nTotalSamples)
        capture_ref=[c_long() for avgidx in range(self.nTriggers)]
        #buffer_ref=range(self.nTriggers)
        #buffer_ref_pointer=range(self.nTriggers)
        #i_buffer=range(self.nTriggers)
        #q_buffer=range(self.nTriggers)
        i_buffer = np.zeros(tot_samps, dtype=c_float)
        q_buffer = np.zeros(tot_samps, dtype=c_float)
        i_ctypes = i_buffer.ctypes.data_as(POINTER(c_float))
        q_ctypes = q_buffer.ctypes.data_as(POINTER(c_float))
        buffer_ref = afDigitizerBufferIQ_t(i_ctypes, q_ctypes, tot_samps)
        buffer_ref_pointer = pointer(buffer_ref)

        start_idx=self.nTriggers-1
        self.log("acq started")
        for avgidx in range(1+start_idx):#self.nTriggers):
            #self.log(avgidx)
            self.digitizer.capture_iq_issue_buffer(buffer_ref=buffer_ref, capture_ref=capture_ref[avgidx], 
                                               timeout = timeout)

        for avgidx in range(self.nTriggers):
            self.digitizer.capture_iq_reclaim_buffer(capture_ref=capture_ref[avgidx],
                                                     buffer_ref_pointer=buffer_ref_pointer)
            if avgidx+start_idx < (self.nTriggers-1):
                self.digitizer.capture_iq_issue_buffer(buffer_ref=buffer_ref, capture_ref=capture_ref[avgidx+start_idx+1], 
                                               timeout = timeout)
                                                     
            if buffer_ref_pointer:
                #self.log("BUFFER POINTER OK - Trigger {}".format(avgidx))
                total_samples = buffer_ref.samples
            else:
                self.log("NO BUFFER!", 30)
                samples = 0
                
            i_avgd += np.mean(i_buffer[:total_samples].reshape(avgs, samples), axis=0)
            q_avgd += np.mean(q_buffer[:total_samples].reshape(avgs, samples), axis=0)
        self.log("acq stopped")                
        i_avgd = i_avgd/self.nTriggers
        q_avgd = q_avgd/self.nTriggers
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
        #cpx_avgd=self.digitizer.buffer_capture(self.nAverages_per_trigger, self.nSamples, self.nTriggers, self.timeout)
#        
#        
#        vI= np.real(cpx_avgd)*np.power(10,dLevelCorrection/20)
#        vQ = np.imag(cpx_avgd)*np.power(10,dLevelCorrection/20) 
#        cpx_scld=cpx_avgd*np.power(10,dLevelCorrection/20)    
#        self.AvgTrace['AvgTrace - I'] = np.real(cpx_scld)
#        self.AvgTrace['AvgTrace - Q'] = np.imag(cpx_scld)
#        self.AvgTrace['AvgTrace - Magvec'] =  np.absolute(cpx_scld) #np.sqrt((vI**2) + (vQ**2))  
#        self.AvgTrace['AvgTrace - Phase']=np.angle(cpx_scld, deg=True)
#        self.AvgTrace['Amplitude - R']=np.mean(np.absolute(cpx_scld))
#if __name__ == '__main__':
#    a=Driver(lo_address='3011D1', dig_address='3036D1', plugin=False, modulation_mode="Generic", lo_reference="OCXO")
#
