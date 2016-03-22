#!/usr/bin/env python

import InstrumentDriver
from VISA_Driver import VISA_Driver
from InstrumentConfig import InstrumentQuantity
import numpy as np

__version__ = "0.0.1"

class Error(Exception):
    pass

class Driver(VISA_Driver):
    """ This class implements the Agilent 5230 PNA driver"""

    def performOpen(self, options={}):
        """Perform the operation of opening the instrument connection. Initializes a measurement param dictionary
        and calls the generic VISA_Driver open"""
        self.dMeasParam = {}
        self.log(options)
        VISA_Driver.performOpen(self, options=options)

        #self.resource_name = resource_name
        #self.session = visa.instrument(resource_name, lock = lock, timeout = timeout, send_end=send_end, values_format=visa.single | visa.big_endian)
        #self.session.term_chars = visa.CR + visa.LF
        #self.session.clear()
        #if reset:
        #    self.session.hw_write("*RST")
        #if selftest:
        #    if int(self.session.hw_ask("*TST?")):
        #        raise InstrumentError("%s did not pass the selftest."%str(self))
        #if identify:
        #    self.instr_id = self.hw_ask("*IDN?")

#    def hw_reset(self):
#        self.hw_write("SYSTem:PRESet")
#        self.hw_write("DISP:WINDow1:TITLe ON")
#        self.hw_write("DISP:WINDow1:TRACe:DELete")
#        self.hw_write("CALCulate1:PARameter:DEFine 'MyMag', {}".format(self.measurement_type))
#        self.hw_write("DISPlay:WINDow1:TRACe1:FEED 'MyMag'")
#        self.hw_write("CALCulate1:PARameter:SELect 'MyMag'")
#        self.hw_write("CALCulate1:FORMat MLOG")
#        self.hw_write("CALCulate1:PARameter:DEFine 'MyPhase', {}".format(self.measurement_type))
#        self.hw_write("DISPlay:WINDow1:TRACe2:FEED 'MyPhase'")
#        self.hw_write("CALCulate1:PARameter:SELect 'MyPhase'")
#        self.hw_write("CALCulate1:FORMat PHASe")

    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation. This function should
        return the actual value set by the instrument"""
        # update visa commands for triggers
        if quant.name in ('S11 - Enabled', 'S21 - Enabled', 'S12 - Enabled',
                          'S22 - Enabled'):
            self.getActiveMeasurements()
            param = quant.name[:3]
            # old-type handling of traces
            if param in self.dMeasParam:
                # clear old measurements for this parameter
                for name in self.dMeasParam[param]:
                    self.writeAndLog("CALC:PAR:DEL '%s'" % name)
            # create new measurement, if enabled is true
            if value:
                newName = 'LabC_%s' % param
                self.writeAndLog("CALC:PAR:EXT '%s','%s'" % (newName, param))
                # show on PNA screen
                iTrace = 1 + ['S11', 'S21', 'S12', 'S22'].index(param)
#                sPrev = self.askAndLog('DISP:WIND:CAT?')
#                if sPrev.find('EMPTY')>0:
#                    # no previous traces
#                    iTrace = 1
#                else:
#                    # previous traces, add new
#                    lTrace = sPrev[1:-1].split(',')
#                    iTrace = int(lTrace[-1]) + 1
                self.writeAndLog("DISP:WIND:TRAC%d:FEED '%s'" % (iTrace, newName))
                # add to dict with list of measurements
                self.dMeasParam[param] = [newName]
        elif quant.name in ('Wait for new trace',):
            # do nothing
            pass
        else:
            # run standard VISA case
            value = VISA_Driver.performSetValue(self, quant, value, sweepRate, options)
        return value


    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation"""
        # check type of quantity
        if quant.name in ('S11 - Enabled', 'S21 - Enabled', 'S12 - Enabled',
                          'S22 - Enabled'):
            # update list of channels in use
            self.getActiveMeasurements()
            # get selected parameter
            param = quant.name[:3]
            value = param in self.dMeasParam
        elif quant.name in ('S11', 'S21', 'S12', 'S22'):
            # check if channel is on
            if quant.name not in self.dMeasParam:
                # get active measurements again, in case they changed
                self.getActiveMeasurements()
            if quant.name in self.dMeasParam:
                if self.getModel() in ('E5071C',):
                    # new trace handling, use trace numbers
                    self.writeAndLog("CALC:PAR%d:SEL" % self.dMeasParam[quant.name])
                else:
                    # old parameter handing, select parameter (use last in list)
                    sName = self.dMeasParam[quant.name][-1]
                    self.writeAndLog("CALC:PAR:SEL '%s'" % sName)
                # if not in continous mode, trig from computer
                bWaitTrace = self.getValue('Wait for new trace')
                bAverage = self.getValue('Average')
                # wait for trace, either in averaging or normal mode
                if bWaitTrace:
                    if bAverage:
                        # set channels 1-4 to set event when average complete (bit 1 start)
                        self.writeAndLog(':SENS:AVER:CLE;:STAT:OPER:AVER1:ENAB 30;:ABOR;:SENS:AVER:CLE;')
                    else:
                        self.writeAndLog(':ABOR;:INIT:CONT OFF;:INIT:IMM;')
                        self.writeAndLog('*OPC')
                    # wait some time before first check
                    self.thread().msleep(30)
                    bDone = False
                    while (not bDone) and (not self.isStopped()):
                        # check if done
                        if bAverage:
                            sAverage = self.askAndLog('STAT:OPER:AVER1:COND?')
                            bDone = int(sAverage)>0
                        else:
                            stb = int(self.askAndLog('*ESR?'))
                            bDone = (stb & 1) > 0
                        if not bDone:
                            self.thread().msleep(100)
                    # if stopped, don't get data
                    if self.isStopped():
                        self.writeAndLog('*CLS;:INIT:CONT ON;')
                        return []
                # get data as float32, convert to numpy array
                if self.getModel() in ('E5071C',):
                    # new trace handling, use trace numbers
                    self.write(':FORM:DATA REAL32;:CALC:SEL:DATA:SDAT?', bCheckError=False)
                else:
                    # old parameter handing
                    self.write(':FORM REAL,32;CALC:DATA? SDATA', bCheckError=False)
                sData = self.read(ignore_termination=True)
                if bWaitTrace and not bAverage:
                    self.writeAndLog(':INIT:CONT ON;')
                # strip header to find # of points
                i0 = sData.find('#')
                nDig = int(sData[i0+1])
                nByte = int(sData[i0+2:i0+2+nDig])
                nData = nByte/4
                nPts = nData/2
                # get data to numpy array
                vData = np.frombuffer(sData[(i0+2+nDig):(i0+2+nDig+nByte)],
                                      dtype='>f', count=nData)
                # data is in I0,Q0,I1,Q1,I2,Q2,.. format, convert to complex
                mC = vData.reshape((nPts,2))
                vComplex = mC[:,0] + 1j*mC[:,1]
                # get start/stop frequencies
                startFreq = self.readValueFromOther('Start frequency')
                stopFreq = self.readValueFromOther('Stop frequency')
                sweepType = self.readValueFromOther('Sweep type')
                # if log scale, take log of start/stop frequencies
                if sweepType == 'Log':
                    startFreq = np.log10(startFreq)
                    stopFreq = np.log10(stopFreq)
                # create a trace dict
                value = InstrumentQuantity.getTraceDict(vComplex, t0=startFreq,
                                               dt=(stopFreq-startFreq)/(nPts-1))
            else:
                # not enabled, return empty array
                value = InstrumentQuantity.getTraceDict([])
        elif quant.name in ('Wait for new trace',):
            # do nothing, return local value
            value = quant.getValue()
        else:
            # for all other cases, call VISA driver
            value = VISA_Driver.performGetValue(self, quant, options)
        return value


    def getActiveMeasurements(self):
        """Retrieve and a list of measurement/parameters currently active"""
        # proceed depending on model
        sAll = self.askAndLog("CALC:PAR:CAT:EXT?")
        # strip "-characters
        sAll = sAll[1:-1]
        # parse list, format is channel, parameter, ...
        self.dMeasParam = {}
        lAll = sAll.split(',')
        nMeas = len(lAll)//2
        for n in range(nMeas):
            sName = lAll[2*n]
            sParam = lAll[2*n + 1]
            if sParam not in self.dMeasParam:
                # create list with current name
                self.dMeasParam[sParam] = [sName,]
            else:
                # add to existing list
                self.dMeasParam[sParam].append(sName)

#    def hw_get_trace(self):
#        avg_state = int(self.hw_ask("""SENSe1:AVERage:STATe?"""))
#        if avg_state:
#            num_avg = int(self.hw_ask("""SENSe1:AVERage:COUNt?"""))
#        else:
#            num_avg = 1
#        #num_pt = self.hw_ask("SENSe1:SWEep:POIN?")
#        self.hw_write("SENSe1:SWE:GRO:COUN {:d}".format(num_avg))
#        self.hw_write("ABORT")
#        self.hw_write("SENSe1:AVERage:CLEar")
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
