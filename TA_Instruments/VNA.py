# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 05:41:29 2014

@author: thomasaref
"""
from numpy import linspace
from threading import Thread
import numpy as np
from atom.api import Unicode, Float, Bool, Enum, Int, ContainerList, Callable
from GPIB import GPIB_Instrument, start_GPIB

def start_VNA(instr, address):
    instr.address=address
    start_GPIB(instr, address="",  timeout = 60)
    instr.measurement_type = 'S21'
    instr.hw_reset()

def hw_reset(self):
        self.hw_write("SYSTem:PRESet")
        self.hw_write("DISP:WINDow1:TITLe ON")
        self.hw_write("DISP:WINDow1:TRACe:DELete")
        self.hw_write("CALCulate1:PARameter:DEFine 'MyMag', {}".format(self.measurement_type))
        self.hw_write("DISPlay:WINDow1:TRACe1:FEED 'MyMag'")
        self.hw_write("CALCulate1:PARameter:SELect 'MyMag'")
        self.hw_write("CALCulate1:FORMat MLOG")
        self.hw_write("CALCulate1:PARameter:DEFine 'MyPhase', {}".format(self.measurement_type))
        self.hw_write("DISPlay:WINDow1:TRACe2:FEED 'MyPhase'")
        self.hw_write("CALCulate1:PARameter:SELect 'MyPhase'")
        self.hw_write("CALCulate1:FORMat PHASe")

def set_averages(instr, averages):
    if averages > 1:
        instr.average_state="On" #hw_write(":SENSe1:AVERage:STATe ON")
        instr.hw_write(":SENSe1:AVERage:COUNt {:d}".format(averages))
    else:
        instr.average_state="Off" #instr.hw_write(":SENSe1:AVERage:STATe OFF")

def get_averages(instr):
    instr.avg_state.receive()# = int(self.hw_ask("""SENSe1:AVERage:STATe?"""))
    if instr.avg_state=="On":
        return int(instr.hw_ask("""SENSe1:AVERage:COUNt?"""))
    else:
        return 1

class NetworkAnalyzer(GPIB_Instrument):
    booter=Callable(start_VNA)
    #ID = Unicode()
    #trace_ready = Event(False)
    #intermediate_data_available = Event()
    #mag_plot = Instance(Plot)
    #phase_plot = Instance(Plot)
    #capture_thread = Instance(Thread)

    start_freq = Float(10.0e6).tag(high=50.0e9, low=10.0e6, label = 'VNA start frequency', unit = 'Hz',
                                    GPIB_writes=":SENSe1:FREQuency:START {start_freq}")

    stop_freq = Float(50.0e9).tag(low=10.0e6, high=50.0e9, label = 'VNA stop frequency', unit = 'Hz',
                                   GPIB_writes=":SENSe1:FREQuency:STOP {stop_freq}")
    points = Float(1601).tag(low=1,high=16001, label = 'VNA frequency points',
                            GPIB_writes=":SENSe1:SWEep:POINts {points}")
    averages = Int(1).tag(low=1, high=1024, label = 'VNA averages',
                          set_cmd=set_averages, get_cmd=get_averages)
    average_state=Enum("Off", "On").tag(GPIB_writes=":SENSe1:AVERAGE:STATE {average_state}",
                                         GPIB_asks="SENSe1:AVERage:STATe?")
    power = Float(-27.0).tag(low=-27.0, high=20.0, label='VNA power', unit = 'dBm',
                              GPIB_writes=":SOURce1:POWer1 {power}")
    electrical_delay = Float(0).tag(label='VNA electrical delay', unit = 's',
                                    GPIB_writes=":CALCulate1:CORRection:EDELay:TIME {electrical_delay}")
    subtract_background = Bool(False)
    measurement_type = Enum('S11', 'S12', 'S21', 'S22')
    #start = Button()
    #adjust_electrical_delay = Button()
    #acquire_background = Button()
    freq = ContainerList().tag(label = 'Frequency')
    mag = ContainerList.tag(label='S21 Mag')
    phase = ContainerList.tag(label='S21 Phase')
    background_mag = ContainerList().tag(label='Background S21 Mag')
    compensated_mag = ContainerList().tag(label='BG compensated S21 Mag')

    #plotdata = Instance(ArrayPlotData)
    #prepared = CBool(False)
#    def __init__(self, resource_name):
#        super(NetworkAnalyzer, self).__init__()
#        self.ID = "Agilent VNA @ {}".format(resource_name)
#        self.hw_init(resource_name)
#        self.configure_traits()
#        self.on_trait_event(self.correct_electrical_delay, 'adjust_electrical_delay')
#        self.on_trait_event(self.start_measurement, 'start')
#    def prepare_measurement(self):
#        self.hw_reset()
#        self.hw_set_start_frequency()
#        self.hw_set_stop_frequency()
#        self.hw_set_points()
#        self.hw_set_power()
#        self.hw_set_electrical_delay()
#        self.hw_set_averages()
#        self.freq = Dataset('Frequency', data=linspace(self.start_freq, self.stop_freq, self.points), unit="Hz")
#        self.mag = DataXY('S12 mag', x=self.freq, y_label='Mag', y_unit="dB")
#        self.mag.y.data[:] = np.nan
#        self.phase = DataXY('S12 phase', x=self.freq, y_label='Phase', y_unit="deg")
#        self.phase.y.data[:] = np.nan
#        if self.background_mag is None:
#            self.background_mag = DataXY('S12 mag background', x=self.freq, y_label='Mag BG', y_unit="dB")
#            self.background_mag.y.data[:] = 0.0
#        if self.compensated_mag is None:
#            self.compensated_mag = DataXY('S12 mag (bg compensated)', x=self.freq, y_label='Mag - BG', y_unit="dB")
#            self.compensated_mag.y.data[:] = np.nan
#        if self.subtract_background:
#            self.plotdata = ArrayPlotData(freq=self.compensated_mag.x.data, mag=self.compensated_mag.y.data, phase=self.phase.y.data)
#        else:
#            self.plotdata = ArrayPlotData(freq=self.mag.x.data, mag=self.mag.y.data, phase=self.phase.y.data)
#        self.mag_plot = Plot(self.plotdata)
#        self.mag_plot.plot(("freq", "mag"))
#        self.phase_plot = Plot(self.plotdata)
#        self.phase_plot.plot(("freq", "phase"))
#        self.on_trait_event(self.replot, 'trace_ready', dispatch='ui')
#        self.prepared = True
#    def start_measurement(self):
#        print self.prepared
#        if not self.prepared:
#            self.prepare_measurement()
#        # Tell the instrument to begin measuring. While waithing for reults
#        self.capture_thread = Thread(target=self.hw_get_trace).start()
#    def replot(self):
#        if self.subtract_background:
#            self.plotdata.set_data('mag', self.compensated_mag.y.data)
#            self.plotdata.set_data('phase', self.phase.y.data)
#        else:
#            self.plotdata.set_data('mag', self.mag.y.data)
#            self.plotdata.set_data('phase', self.phase.y.data)
#    def hw_set_stop_frequency(self):
#        self.hw_write(":SENSe1:FREQuency:STOP {:.0f}".format(self.stop_freq))
#    def hw_set_points(self):
#        self.hw_write(":SENSe1:SWEep:POINts {:d}".format(self.points))
#    @on_trait_change('power')
#    def hw_set_power(self):
#        self.hw_write(":SOURce1:POWer1 {:.2f}".format(self.power))
#    @on_trait_change('electrical_delay')
#    def hw_set_electrical_delay(self):
#        self.hw_write(":CALCulate1:CORRection:EDELay:TIME {:.12e}".format(self.electrical_delay))
 #   @on_trait_change('averages')
#    def hw_set_averages(self):
#        if self.averages > 1:
#            self.hw_write(":SENSe1:AVERage:STATe ON")
#            self.hw_write(":SENSe1:AVERage:COUNt {:d}".format(self.averages))
#        else:
#            self.hw_write(":SENSe1:AVERage:STATe OFF")
    #@on_trait_change('start_freq')
    #def hw_set_start_freq(self, new):
    #    self.hw_write("SENSe1:FREQuency:START {:.0f}".format(new))
    #    #self.hw_write("SENSe1.FREQuency:START {:.0f}".format(new))
    #@on_trait_change('stop_freq')
    #def hw_set_stop_freq(self, new):
    #    self.hw_write(":SENSe1:FREQuency:STOP {:.0f}".format(new))
    #    #self.hw_write(":SENSe1.FREQuency:STOP {:.0f}".format(new))
    #@on_trait_change('bandwidth')
    #def hw_set_bandwidth(self, new):
    #    self.hw_write(":SENSe1:BANDwidth {:.0f}".format(new))
    #    #self.hw_write(":SENSe1:BANDwidth {:.0f}".format(new))
    #@on_trait_change('S12er')
    #def hw_set_power(self, new):
    #    self.hw_write(":SOURce1:POWer1 {:.2f}".format(new))
    #    #self.hw_write(":SOURce2:POWer2 {:.2f}".format(new))
    #@on_trait_change('points')
    #def hw_set_points(self, new):
    #    self.hw_write(":SENSe1:SWEep:POINts {:d}".format(new))
    #    #self.hw_write(":SENSe1:SWEep:POINts {:d}".format(new))
    #@on_trait_change('averages')
    #def hw_set_averages(self, new):
    #    if new > 1:
    #        self.hw_write(":SENSe1:AVERage:STATe ON")
    #        self.hw_write(":SENSe1:AVERage:COUNt {:d}".format(new))
    #    else:
    #        self.hw_write(":SENSe1:AVERage:STATe OFF")
    #@on_trait_change('electrical_delay')
    #def hw_set_electrical_delay(self, new):
    #    self.hw_write(":CALCulate1:CORRection:EDELay:TIME {:.12e}".format(new))
    def _acquire_background_fired(self):
        self.acquire_trace()
        self.background_mag.y.data = self.mag.y.data
        print('Acquired background!')
    def hw_get_trace(self):
        self.averages.receive()
        #num_pt = self.hw_ask("SENSe1:SWEep:POIN?")
        self.hw_write("SENSe1:SWE:GRO:COUN {:d}".format(self.averages))
        self.hw_write("ABORT")
        self.hw_write("SENSe1:AVERage:CLEar")
        self.hw_write("SENSe1:SWE:MODE GROUPS")
        #freq = np.linspace(self.start_freq, self.stop_freq, self.points)
        done = False

        while not done:
            try:
                done = int(self.hw_ask("*OPC?"))
            except:
                pass
        self.hw_write("CALCulate1:PARameter:SELect 'MyMag'")
        self.hw_write("FORMat:DATA REAL,32")
        #mag = Series(self.hw_ask_data("CALCulate1:DATA? FDATA"), index = freq)
        #mag = DataTrace('Mag', data = self.hw_ask_data("CALCulate1:DATA? FDATA"), indep = freq)
        mag_array = np.array(self.hw_ask_data("CALCulate1:DATA? FDATA"))
        self.hw_write("CALCulate1:PARameter:SELect 'MyPhase'")
        self.hw_write("FORMat:DATA REAL,32")
        #phase = Series(self.hw_ask_data("CALCulate1:DATA? FDATA"), index = freq)
        #phase = DataTrace('Phase', data = self.hw_ask_data("CALCulate1:DATA? FDATA"), indep = freq)
        phase_array = np.array(self.hw_ask_data("CALCulate1:DATA? FDATA"))
        self.mag.y.data = mag_array
        self.phase.y.data = phase_array
        self.compensated_mag.y.data = mag_array - self.background_mag.y.data
#        print("Measurement done!")
#        self.trace_ready = True
#    def acquire_trace(self):
#        if not self.prepared:
##            self.prepare_measurement()
#        self.hw_get_trace()
    def correct_electrical_delay(self):
        print('first acquisition...')
        self.acquire_trace()
        dph = np.diff(self.phase.y.data)
        df = np.diff(self.freq.data)
        der = dph/df
        self.electrical_delay = self.electrical_delay - 1/(360/np.median(der))
        print('second acquisition...')
        self.acquire_trace()
        dph = np.diff(self.phase.y.data)
        df = np.diff(self.freq.data)
        der = dph/df
        self.electrical_delay = self.electrical_delay - 1/(360/np.mean(der))
        print('Electrical delay adjusted!')
if __name__ == '__main__':
    NA = NetworkAnalyzer2('GPIB::16')
    NA.start_freq = 4.0e9
    NA.stop_freq = 5e9
    NA.points = 201
    NA.electrical_delay = 62.01e-9
    NA.power = -20