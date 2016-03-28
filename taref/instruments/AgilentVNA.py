# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 05:41:29 2014

@author: thomasaref
"""
from numpy import linspace, array, log10, absolute
#from threading import Thread
from atom.api import Unicode, Float, Bool, Enum, Int, Value, observe, Dict, Typed
from taref.instruments.instrument import Instrument, booter, closer
from taref.core.atom_extension import get_tag, set_tag, log_func, get_all_tags, tag_Callable, get_map, private_property
from taref.core.universal import Array
from taref.physics.units import GHz
from comtypes.client import CreateObject
from taref.core.log import log_debug
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from time import sleep
#from comtypes import COMError
#Ensure module is created before importing
#Back up code to create module:
#GetModule("AgNA.dll")
#try:
import comtypes.gen.AgilentNALib as AgilentNALib

#except ImportError:
#    VNA=CreateObject('AgilentNA.AgilentNA')
#    VNA.Release()
#    import comtypes.gen.AgilentNALib as AgilentNALib

def invert_dict(indict):
    return {obj:key for key, obj in indict.iteritems()}

#def add_inverse(indict):
#    return indict.update(invert_dict(indict))

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

def askVNA(VNA, VNA_string):
    VNA.System2.WriteString(VNA_string)
    return VNA.System2.ReadString()


def pass_ask_it(instr, name):
    """get pass function. used as place holder."""
    def pass_ask(instr, **kwargs):
        return getattr(instr, name)
    pass_ask=log_func(pass_ask, name)
    pass_ask.log_message="PASS ASK: {0} {1}: "+name
    return pass_ask
    
def pass_write_it(instr, name):
    """send pass function. used as place holder"""
    def pass_write(instr, **kwargs):
        setattr(instr, name, kwargs[name])
    pass_write=log_func(pass_write, name)
    pass_write.log_message="PASS WRITE: {0} {1}: "+name
    pass_write.run_params.append(name)
    return pass_write 
   
class COM_Instrument(Instrument):
    """Instrument specialization to deal with COM drivers"""
    def COM_ask_it(self, name, aka):
        """returns custom COM_ask using alias aka"""
        obj, param, index=self.get_ptr(aka)
        if index is None:
            def COM_ask(self, **kwargs):
                return getattr(obj, param) #instr.session.ask(GPIB_string.format(**kwargs))
        else:
            def COM_ask(self, **kwargs):
                return getattr(obj, param)[index] #instr.session.ask(GPIB_string.format(**kwargs))
        COM_ask=log_func(COM_ask, name)
        COM_ask.log_message="COM ASK: {0} {1}: "+name
        return COM_ask
    
    def COM_write_it(self, name, aka):
        """returns custom COM_write with using alias aka"""
        obj, param, index=self.get_ptr(aka)
        if index is None:
            def COM_write(self, **kwargs):
                setattr(obj, param, kwargs[name])
        else:
            def COM_write(self, **kwargs):
                getattr(obj, param)[index]=kwargs[name]
        COM_write=log_func(COM_write, name)
        COM_write.log_message="COM WRITE: {0} {1}: "+name
        COM_write.run_params.append(name)
        return COM_write

    def get_ptr(self, name):
        """gets pointer to obj and param from alias. can handle multiple dots in path but not brackets.
        param can be indexed with an integer"""
        name_list=name.split(".")
        param=name_list[-1]
        index=None
        if "[" in param:
            param, div, index=param.partition("]")[0].partition("[")
            index=int(index)
        obj=self
        for x in name_list[1:-1]:
            obj = getattr(obj, x)
        return obj, param, index
    
    def extra_setup(self, param, typer):
        super(Instrument, self).extra_setup(param, typer)
        aka = get_tag(self, param, "aka")
        if aka!=None:
            do=get_tag(self, param, "do", False)
            readwrite=get_tag(self, param, "ReadWrite", "Both")
            if readwrite in ("Both", "Write"):
                set_tag(self, param, set_cmd=pass_write_it(self, param), do=do)
            if readwrite in ("Both", "Read"):
                set_tag(self, param, get_cmd=pass_ask_it(self, param), do=do)  
    
    def postboot(self):
        for param in get_all_tags(self, "aka"):
            aka = get_tag(self, param, "aka")
            if get_tag(self, param, "set_cmd") is not None:
                set_tag(self, param, set_cmd=self.COM_write_it(param, aka))
            if get_tag(self, param, "get_cmd") is not None:
                set_tag(self, param, get_cmd=self.COM_ask_it(param, aka))
        for param in self.all_params:
            if get_tag(self, param, 'get_cmd') is not None:
                log_debug(param)
                self.receive(param)        
                
class AgilentNetworkAnalyzer(COM_Instrument):
    base_name="E8354B"
    
    @private_property
    def S_names(self):
        return ('S11', 'S21', 'S12', 'S22')
    
    @private_property
    def main_params(self):
        return ["doS11", "doS21", "doS12", "doS22", "trigger_mode", "VNA_abort", "start_freq", "stop_freq",
                "points", "averaging", "averages", 'timeout', "power", 'clear_average', 'acquire_data', 'error_query']
     #::inst0::INSTR"
     #enable SICL in system settings
     #"TCPIP::129.16.115.134::5025::SOCKET"                
    address=Unicode("TCPIP::129.16.115.134").tag(sub=True, no_spacer=True)
    simulate=Bool(False).tag(sub=True) 
    VNA=Value().tag(private=True, desc="a link to the session of the instrument.")
    ch1=Value().tag(private=True, desc="link to main instrument channel")
    measS11=Value().tag(private=True, desc="link to measurements")
    measS12=Value().tag(private=True, desc="link to measurements")
    measS21=Value().tag(private=True, desc="link to measurements")
    measS22=Value().tag(private=True, desc="link to measurements")

    trace_plot=Typed(Plotter).tag(private=True)
    
    def update_trace_plot(self):
        self.trace_plot.plot_dict["trace_mag S21"].clt.set_xdata(self.freq)
        S21dB=20.0*log10(absolute(self.S21))
        if self.simulate:
            S21dB=absolute(self.S21)
        self.trace_plot.plot_dict["trace_mag S21"].clt.set_ydata(S21dB)
        if min(self.freq)!=max(self.freq):
            self.trace_plot.set_xlim(min(self.freq), max(self.freq))
        if min(S21dB)!=max(S21dB):
            self.trace_plot.set_ylim(min(S21dB), max(S21dB))
        self.trace_plot.draw()

    def _default_trace_plot(self):
        tp=Plotter(name=self.name+' trace plot')
        tp.line_plot('trace_mag S21', self.freq, 20.0*log10(absolute(self.S21)))
        return tp
    
    doS11=Bool(False)
    doS21=Bool(False)
    doS12=Bool(False)
    doS22=Bool(False)
    do_freq=Bool(False)
    timeout=Int(10000)
    
    #clear_average=Bool(True).tag(sub=True)
    
    @observe("doS11", "doS21", "doS21", "doS22")
    def observe_doSs(self, change):
        log_debug(change)
        if change['type']=='update':
            Sname=change["name"][2:]
            if change.get("oldvalue", False):
                log_debug('del old meas')
                log_debug(getattr(self, 'meas'+Sname).Delete())
                self.error_query()
            elif change["value"]:
                ReceiverPort=int(Sname[1])
                SourcePort=int(Sname[2])
                log_debug(ReceiverPort, SourcePort)
                if Sname not in self.query_measurements().values():
                    self.VNA_write("CALC:PAR:DEF:EXT MEAS{0},{0}".format(Sname))
                log_debug(getattr(self, 'meas'+Sname).Create(ReceiverPort, SourcePort))
                self.error_query()
                print self.query_measurements()
                sleep(1)
                getattr(self, 'meas'+Sname).Format=0
        #self.error_query()

    def query_measurements(self):
        sAll=self.VNA_ask("CALC:PAR:CAT:EXT?")[1:-1]
        if self.simulate:
            sAll='NO CATALOG'
        if sAll=='NO CATALOG':
            return {}
        t=sAll.split(",")
        return {t[i]:t[i+1] for i in range(0, len(t), 2)}

        
    def VNA_read(self):
        """calls VNA ReadString"""
        return self.VNA.System2.ReadString()
    
    def VNA_write(self, VNA_string, **kwargs):
        """calls VNA WriteString using string formatting by kwargs"""
        self.VNA.System2.WriteString(VNA_string.format(**kwargs))
    
    def VNA_ask(self, VNA_string, **kwargs):
        """calls VNA WriteString followed by VNA ReadString"""
        self.VNA_write(VNA_string, **kwargs)
        return self.VNA_read()
    
    @tag_Callable()    
    def VNA_abort(self):
        self.VNA.Channels.Abort()
        self.VNA_write("CALC:PAR:DEL:ALL")
        self.VNA.Status.Clear()
        
        #self.ch1.TriggerMode=TriggerModeDict['Hold']
          
    @booter
    def booter(self, address):
        self.VNA=CreateObject("AgilentNA.AgilentNA")
        init_list=['Simulate={0}'.format(self.simulate),
                   #'QueryInstrStatus=true'
                   ]
        init_str=','.join(init_list)
        print init_str
        log_debug(self.VNA.Initialize(self.address, False, False, init_str)) 
        self.ch1=self.VNA.Channels["Channel1"]
        self.VNA_abort()
        #self.VNA_write("CALC:PAR:DEL:ALL")
        self.error_query()
        #log_debug(self.VNA.System2.WaitForOperationComplete(self.timeout))
        #self.error_query()
        self.measS11=self.ch1.Measurements["Measurement1"]
        self.measS21=self.ch1.Measurements["Measurement2"]
        self.measS12=self.ch1.Measurements["Measurement3"]
        self.measS22=self.ch1.Measurements["Measurement4"]
        
        #sleep(1)
        #self.measS11.Create(1, 1)
        #self.error_query()
        #sleep(1)
        #self.measS11.Delete()
                                    
        self.error_query()
    @tag_Callable()    
    def error_query(self):
        for n in range(11):
            err_query=self.VNA.Utility.ErrorQuery()
            log_debug(err_query, n=3)
            if err_query[0]==0:
                break

    def clear_all_traces(self):
        self.VNA.System2.WriteString("CALC:PAR:DEL:ALL")
                    
                            
#    def close_measurement(self, key):
#        try:
#            self.meas_dict[key].Delete()
#        except COMError as e:
#            log_debug(e)
#            
#    def close_all_measurements(self):
#        for key in self.meas_dict:
#            self.close_measurement(key)
            
    @closer
    def closer(self):
        for key in self.S_names:
            if getattr(self, 'do'+key):
                log_debug(getattr(self, 'meas'+key).Delete())
        #self.VNA_abort()        
        log_debug(self.VNA.Close())
        for n in range(10):
            log_debug(n)
            if self.VNA.Release()==0:
                break
    #VNA.Channels["Channel1"].StimulusRange.Span
    #VNA.Channels["Channel1"].StimulusRange.Center
    #VNA.System2.WriteString(":OUTP 0")
        
    @tag_Callable()
    def clear_average(self):
        self.ch1.ClearAverage()
    
#    def acq2(self):
#        log_debug('acq2 started')
#        self.ch1.TriggerMode=1
#        self.ch1.ClearAverage()
#        for n in range(self.averages):
#            self.ch1.TriggerSweep(1000)
#            self.VNA.System2.WaitForOperationComplete(10000)
#        log_debug('acq2 stopped') 
#    
#    def acq(self):
#        log_debug('acq started')
#        self.VNA_write("SENSE:SWE:GRO:COUN {}".format(self.averages))
#
#        self.ch1.ClearAverage()
#        self.VNA.System2.WriteString("SENSE:SWE:MODE GROUPS")
#        getattr(self, 'meas'+'S21').Trace.AutoScale()
#        try:
#            log_debug(self.VNA.System2.WaitForOperationComplete(30000))
#            #print self.error_query()
#        except Exception as e:
#            raise Exception(str(e))
#        log_debug('acq stopped') 
    @tag_Callable()    
    def acquire_data(self):
        self.trigger_mode='Hold'
        #if get_tag(self, "clear_average", "do"):
        self.clear_average()
        if self.averaging:
            numTriggers=self.averages
        else:
            numTriggers=1
        for n in range(numTriggers):
            log_debug(n)
            if self.abort:
                break
            self.ch1.TriggerSweep(1000)
            self.VNA.System2.WaitForOperationComplete(self.timeout)
            
            if n==9:
                for key in self.S_names:
                    if getattr(self, "do"+key):
                        getattr(self, 'meas'+key).Trace.AutoScale()
                           
        for key in self.S_names:
            if getattr(self, "do"+key):
                data=array(getattr(self, 'meas'+key).FetchComplex())
                setattr(self, key, data[0]+1.0j*data[1])
                log_debug(getattr(self, key))
                if self.do_freq:
                    self.freq=getattr(self, 'meas'+key).FetchX()
        if not self.do_freq:
            self.freq=linspace(self.start_freq, self.stop_freq, self.points)
        self.update_trace_plot()
                #print list(frq)==list(self.freq)
            
    start_freq = Float(4.0e9).tag(high=50.0e9, low=10.0e6, label = 'VNA start frequency', unit2 = 'GHz', 
                                    aka="self.ch1.StimulusRange.Start", show_value=True)

    stop_freq = Float(5.0e9).tag(low=10.0e6, high=50.0e9, label = 'VNA stop frequency', unit2 = 'GHz',
                                   aka="self.ch1.StimulusRange.Stop", show_value=False)
    points = Int(1601).tag(low=1, high=20001, label = 'VNA frequency points',
                            aka="self.ch1.Points")
    averages = Int(1).tag(low=1, high=50000, label = 'VNA averages',
                          aka="self.ch1.AveragingFactor")
    averaging=Bool(True).tag(aka="self.ch1.Averaging")
    power = Float(-27.0).tag(low=-27.0, high=0.0, label='VNA power', display_unit = 'dBm',
                              aka="self.ch1.SourcePower.Level[1]")
    #electrical_delay = Float(0).tag(label='VNA electrical delay', unit = 's',
    #                                GPIB_writes=":CALCulate1:CORRection:EDELay:TIME {electrical_delay}")
    #subtract_background = Bool(False)
    #measurement_type = Enum('S11', 'S12', 'S21', 'S22')
    #start = Button()
    #adjust_electrical_delay = Button()
    #acquire_background = Button()
    freq = Array().tag(label = 'Frequency', sub=True)
    S11 = Array().tag(sub=True)
    S12 = Array().tag(sub=True)
    S21 = Array().tag(sub=True)
    S22 = Array().tag(sub=True)
    
    trigger_mode=Enum('Continuous', 'Hold').tag(mapping=TriggerModeDict, aka="self.ch1.TriggerMode")
    
if __name__ == '__main__':
   # print get_ptr(1, "self.ch1.StimulusRange.Start")
    if 1:
        VNA = AgilentNetworkAnalyzer(simulate=True)
        VNA.trace_plot
        #b=Plotter()
        #b.line_plot('data', VNA.freq, 20.0*log10(absolute(VNA.S21)))
        shower(VNA)
        try:
            if 0:
                VNA.boot()
                print VNA.ch1.StimulusRange.Start
                print VNA.get_ptr("self.ch1.SourcePower.Level[1]")
                print VNA.receive("power")
                VNA.power=-27.0
                print VNA.receive("power")
                print VNA.power
                VNA.start_freq=4.0e9
                VNA.stop_freq=5.0e9
                VNA.points=1001
                VNA.averages=101
                #VNA.send("start_freq")
                print VNA.ch1.StimulusRange.Start
                VNA.VNA_write(":OUTP 1")
                print VNA.VNA_ask("OUTP?")
                #VNA.doS11=True
                VNA.doS21=True
                VNA.acquire_data()
                #VNA.acq2()
                
                #VNA.trigger_mode='Hold'
                #print get_map(VNA, 'trigger_mode')
                #print get_map(VNA, 'trigger_mode', 0)
                
                VNA.close()
        except Exception as e:
            print e
            VNA.VNA_abort()
        finally:
            AgilentNetworkAnalyzer.clean_up()
            

        
    #NA.start_freq = 4.0e9
    #NA.stop_freq = 5e9
    #NA.points = 201
    #NA.electrical_delay = 62.01e-9
    #NA.power = -20    
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
    #def _acquire_background_fired(self):
    #    self.acquire_trace()
    #    self.background_mag.y.data = self.mag.y.data
    #    print('Acquired background!')
#    def hw_get_trace(self):
#        self.averages.receive()
#        #num_pt = self.hw_ask("SENSe1:SWEep:POIN?")
#        self.hw_write("SENSe1:SWE:GRO:COUN {:d}".format(self.averages))
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
##        print("Measurement done!")
##        self.trace_ready = True
##    def acquire_trace(self):
##        if not self.prepared:
###            self.prepare_measurement()
##        self.hw_get_trace()
#    def correct_electrical_delay(self):
#        print('first acquisition...')
#        self.acquire_trace()
#        dph = np.diff(self.phase.y.data)
#        df = np.diff(self.freq.data)
#        der = dph/df
#        self.electrical_delay = self.electrical_delay - 1/(360/np.median(der))
#        print('second acquisition...')
#        self.acquire_trace()
#        dph = np.diff(self.phase.y.data)
#        df = np.diff(self.freq.data)
#        der = dph/df
#        self.electrical_delay = self.electrical_delay - 1/(360/np.mean(der))
#        print('Electrical delay adjusted!')
