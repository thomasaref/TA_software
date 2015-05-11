# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 01:34:33 2014

@author: thomasaref
"""

from TestInstrument import Test_Instrument
from Boss import boss

a=Test_Instrument(name="blah")
b=Test_Instrument(name="bob", view="Field")
boss.boot_all()
def measfunc():
    a.voltage=3
    b.power=2
boss.run=measfunc
boss.show()

from numpy import linspace
choice=0

if choice==1:
    from anritsu_rf_pulser import AnritsuRFPulser
    from Yoko import Yoko
    from aeroflex_iq import AeroflexIQ
    dig = AeroflexIQ("3011D1", "3035D1")
    dig.boot()
    dig.center_frequency = 4.483e9
    dig.ref_amplitude = 0
    dig.trigger_source = 'Front SMB'
    dig.trigger_edge = 'Rising'
    dig.sample_rate = 200000000
    dig.samples = 500
    dig.pretrigger_samples = 100
    dig.averages_per_trigger = 50000

    yoko = Yoko("GPIB::11")
    yoko.boot()
    yoko.voltage=-0.3
    yoko.output = 'on'
    yoko.ramp()

    a = AnritsuRFPulser("GPIB::8")
    a.boot()
    a.freq = 4.483e9
    a.power = -17
    a.pulsing = 'Internal'
    a.pulse_time = 500e-9
    a.pulse_rate = 400000
    a.leveling = True

    def measfunc():
        for power in linspace(-40, -10, 51):
            a.power=power
            dig.group.receive()
    boss.run=measfunc
    boss.show()

    ## -------- FLUX vs FREQUENCY map --------
if choice==2:

    from NetworkAnalyzer import NetworkAnalyzer
    from Yoko import Yoko
    from anritsu_rf_pulser import AnritsuRFPulser
    #a = AnritsuRFPulser("GPIB::8")
    #a.output = 'Off'
    #G = GeneralStepper()
    #
    vna = NetworkAnalyzer('GPIB::16')
    vna.start_freq = 4.6066e9
    vna.stop_freq = 5.0066e9
    vna.points = 601
    vna.electrical_delay = 53.4255e-9 #54.9550e-9 #55.175e-9 #58.201e-9 #91.05e-9# #59.70e-09
    vna.power=-20.0

    yok = Yoko("GPIB::11")
    yok.voltage = 0
    yok.output = 'on'
    yok.ramp(-5)
    def measfunc():
        for voltage in linspace(-5.0, 5.0, 2001):
            yok.voltage=voltage
            vna.receive('trace')
    boss.run_measurement=measfunc
    boss.show()

# -------- IQ mapping FLUX and PROBE POWER
if choice==3:
    from Yoko import Yoko
    #from anritsu_rf_pulser import AnritsuRFPulser
    from iq_point import IQPointSource
    from aeroflex_gen import AeroflexGen
    from time import sleep
    f0 = 4.8066e9

    probe = AeroflexGen("3010S1", "3025S1")
    probe.power = -10.0
    probe.freq = f0

    yok = Yoko("GPIB::11")
    yok.output = 'On'

    iq = IQPointSource("3011D1", "3035D1")
    iq.center_frequency = f0
    iq.ref_amplitude = -10
    iq.sample_rate = 5000000
    iq.averages = 500000

    probe.output="On"

    def measfunc():
        for voltage in linspace(-0.6, -0.2, 81):
            yok.voltage=voltage
            sleep(0.05)
            for power in linspace(-60.0, 0.0, 121):
                probe.power=power
                iq.receive('trace')

    boss.run_measurement=measfunc
    boss.show()

## -------- TWO-TONE SPECTROSCOPY --------
if choice==4:
    #from NetworkAnalyzer2 import NetworkAnalyzer2
    from Yoko import Yoko
    from anritsu_rf_pulser import AnritsuRFPulser
    from iq_point import IQPointSource
    from aeroflex_gen import AeroflexGen
 #   from basic_point import PointSource

    f0 = 4.8066e9
    #probe = AnritsuRFPulser("GPIB::17")
    probe = AeroflexGen("3010S1", "3025S1")
    probe.power =-10.0
    probe.freq = f0

    control = AnritsuRFPulser("GPIB0::8::INSTR") #"GPIB::8")
    control.power = -50.0
    control.pulsing = 'Off'
    control.freq = f0
    control.leveling = True

    yok = Yoko("GPIB0::11::INSTR")#"GPIB::11")
    yok.output = 'on'

    iq = IQPointSource("3011D1", "3035D1")
    iq.center_frequency = f0
    iq.ref_amplitude = -10
    iq.sample_rate = 5000000
    iq.averages = 3000000

    probe.output='On'
    control.output='On'

    def measfunc(outer="control freq", outer_start=4.2e9, outer_stop=5.4e9, outer_steps=241,
                 inner="yoko voltage", inner_start=-0.8, inner_stop=-0.5, inner_steps=151):
        for freq in linspace(outer_start, outer_stop, outer_steps):
            control.freq=freq
            sleep(0.001)
            for voltage in linspace(inner_start, inner_stop, inner_steps):
                yok.voltage=voltage
                iq.receive('trace')
    boss.comment="testing something with 10 dB attenuation, low pass filters and so forth"
    boss.run=measfunc
    boss.show()


# -------- SPECTRUM WITH FIXED PROBE FREQUENCY
if choice==5:
    from aeroflex_spectrum import AeroflexSpectrum
    from new_yoko import Yoko
    from anritsu_rf_pulser import AnritsuRFPulser
    f0 = 4.8066e9
    df = 100000
    s = AeroflexSpectrum("3011D1", "3035D1")
    s.start_freq = f0-df
    s.stop_freq = f0+df
    s.ref_amplitude = 0
    s.rbw = 1000
    s.averages = 100
#
#
    a = AnritsuRFPulser("GPIB::8")
    a.power = -20.0
    a.pulsing = 'Off'
    a.freq = f0
    a.leveling = True
#
    yok = Yoko("GPIB::11")
    yok.voltage = 0.0
    yok.output = 'on'

    def measfunc(start=-30, stop=0, steps=61):
        for power in linspace(-30, 0, 61):
            a.power=power
            s.receive('trace')
    boss.run_measurement=measfunc
    boss.show()

# -------- SHOT NOISE THERMOMETRY --------
#    from new_yoko import Yoko
#    from aeroflex_spectrum import AeroflexSpectrum
#
#    G = GeneralStepper()
#    s = AeroflexSpectrum("3011D1", "3035D1")
#    s.start_freq = 4.999e9
#    s.stop_freq = 5.001e9
#    s.ref_amplitude = -90
#    s.rbw = 1000
#    s.averages = 100
#    yok = Yoko("GPIB::11")
#    time.sleep(1)
#    yok.voltage = 0.0
#    time.sleep(1)
#    yok.output = 'on'
#    time.sleep(1)
#
#
#    #a.freq = 4.55e9
#    #a.power = -10
#    #a.pulsing = 'Off'
#    #a.leveling = True
#    #a.output = 'On'
#    G.step_instrument = yok
#    G.sweep_instrument = s
#    G.step_parameter = 'voltage'
#    G.start_value = 0.0
#    G.stop_value = 3.0
#    G.step_points = 101
#    G.sweep_data = ['spectrum']
#    ##

## -------- IQ --------
#    from anritsu_rf_pulser import AnritsuRFPulser
#    from new_yoko import Yoko
#    from aeroflex_iq_lightweight import AeroflexIQ
#    #from aeroflex_gen import AeroflexGen
#
#    f0 = 4.8066e9
#    #control = AeroflexGen("3010S1", "3025S1")
#    #control.power = -20.0
#    #control.freq = f0
#
#    a = AnritsuRFPulser("GPIB::8")
#    G = GeneralStepper()
#    dig = AeroflexIQ("3011D1", "3035D1")
#    dig.center_frequency = f0
#    dig.ref_amplitude = -10
#    dig.trigger_source = 'Front SMB'
#    dig.trigger_edge = 'Rising'
#    dig.sample_rate = 200e6
#    dig.samples = 500
#    dig.pretrigger_samples = 90
#    dig.averages_per_trigger = 50000
#    dig.triggers_to_average = 100
#    yok = Yoko("GPIB::11")
#    time.sleep(1)
#    yok.voltage =0.0
#    time.sleep(1)
#    #yok.voltage = -1.5
#    #time.sleep(1)
#    yok.output = 'on'
#    time.sleep(1)
#    #dummy = DummyStepInstr()
#    a.freq = f0
#    a.power = -20.0
#    #a.voltage = 0.005
#    a.pulsing = 'Internal'
#    a.pulse_time = 1000e-9
#    a.pulse_rate = 400000
#    a.leveling = True
#
#    G.step_instrument =   yok #dummy
#    G.sweep_instrument = dig
#    G.step_parameter = 'voltage' #dummy'
#    G.start_value = -1.0 #0.01 #-1.6
#    G.stop_value = 0.0
#    G.step_points =201 #34 #391
#    G.sweep_data = ['Mag', 'Phase']
#    #control.output='On'
#    a.output = 'On'
## -------- IQ, listening, no probing --------
##PXI clibration measurement
## Big amp. 10 dB atten from PXI source to PXI input, 30 dB before amps
    #from NetworkAnalyzer2 import NetworkAnalyzer2
    from new_yoko import Yoko
    from general_tracer import GeneralTracer
    #from anritsu_rf_pulser import AnritsuRFPulser
    from iq_point import IQPointSource
    from aeroflex_gen import AeroflexGen
    #from basic_point import PointSource
#
    G = GeneralStepper()
#
    f0 = 4.8066e9
#
    #probe = AnritsuRFPulser("GPIB::17")
    probe = AeroflexGen("3010S1", "3025S1")
    probe.power = -10.0
    probe.freq = f0

    #control = AnritsuRFPulser("GPIB::8")
    #control.voltage = 0.01
    #control.power=-15
    #control.pulsing = 'Off'
    #control.freq = f0
    #control.leveling = True

    yok = Yoko("GPIB::11")
    time.sleep(1)
    yok.output = 'on'
    time.sleep(1)

    dummy = DummyStepInstr()

    iq = IQPointSource("3011D1", "3035D1")
    #iq = PointSource()
    iq.center_frequency = f0
    iq.ref_amplitude = -10
    iq.sample_rate = 5000000
    iq.averages = 5000000
    tracer = GeneralTracer(is_sub_measurement=True)
    tracer.step_instrument = probe
    tracer.step_parameter = 'power'
    tracer.start_value = -60.0
    tracer.stop_value = 0.0
    tracer.step_points = 121
    #tracer.step_instrument = yok
    #tracer.step_parameter = 'voltage'
    #tracer.start_value = -0.6
    #tracer.stop_value = -0.2
    #tracer.step_points = 81
    tracer.step_pause = 0.05
    tracer.data_instrument = iq
    tracer.data_names = ['Mag_rms', 'Mag_vec', 'Phase', 'I', 'Q']

    #G.step_instrument = yok
    #G.step_parameter = 'voltage'
    #G.sweep_instrument = tracer
    #G.start_value = -0.6
    #G.stop_value = -0.2
    #G.step_points = 81
    G.step_instrument = dummy #probe #control
    G.step_parameter = 'dummy' #'voltage'
    G.sweep_instrument = tracer
    G.start_value = -30.0
    G.stop_value = -20.0
    G.step_points = 2
    probe.output='On'

    #yok.ramp(-5.2) #remember to ramp back to zero at end of measurement

    #control.output='Off'
    #time.sleep(1)
    #yok.voltage = -0.6
    #time.sleep(1)
    #yok.voltage = -2.0
    #time.sleep(1)
    #yok.voltage = -3.0
    #time.sleep(1)
    #yok.voltage = -4.0
    #time.sleep(1)
    #yok.voltage = -5.0
    #time.sleep(1)

## -------- Freqsyncer IQ, listening, no probing --------
#    from new_yoko import Yoko
#    from general_tracer import GeneralTracer
#    from iq_point import IQPointSource
#    from aeroflex_gen import AeroflexGen
#    from FreqSyncer import FreqSyncer
#    G = GeneralStepper()
#
#    f0 = 4.8066e9
#
#    probe = AeroflexGen("3010S1", "3025S1")
#    probe.power = -10.0
#    probe.freq = f0
#
#    yok = Yoko("GPIB::11")
#    time.sleep(1)
#    yok.output = 'on'
#    yok.voltage = 0.0 #0.45
#    time.sleep(1)
#    #yok.ramp(0.45) #remember to ramp back to zero at end of measurement
#
#    dummy = DummyStepInstr()
#
#    iq = IQPointSource("3011D1", "3035D1")
#    iq.center_frequency = f0
#    iq.ref_amplitude = -10
#    iq.sample_rate = 5000000
#    iq.averages = 500000
#
#    fsync = FreqSyncer()
#    fsync.dig = iq
#    fsync.source = probe
#
#    tracer = GeneralTracer(is_sub_measurement=True)
#    tracer.step_instrument = fsync #dummy
#    tracer.step_parameter = 'freq' #'dummy'
#    tracer.start_value = 4.7566e9
#    tracer.stop_value = 4.8566e9
#    tracer.step_points = 501
#
#    tracer.step_pause = 0.05
#    tracer.data_instrument = iq
#    tracer.data_names = ['Mag_rms', 'Mag_vec', 'Phase', 'I', 'Q']
#
#    G.step_instrument = dummy #fsync
#    G.step_parameter = 'dummy' #'freq'
#    G.sweep_instrument = tracer
#    G.start_value = 1 #4.7566e9
#    G.stop_value = 2 #4.8566e9
#    G.step_points = 2
#    probe.output='On'

# -------- IQ, listening, no probing from Test PXI crosssection--------
#    #from NetworkAnalyzer2 import NetworkAnalyzer2
#    from new_yoko import Yoko
#    from general_tracer import GeneralTracer
#    #from anritsu_rf_pulser import AnritsuRFPulser
#    from iq_point import IQPointSource
#    from aeroflex_gen import AeroflexGen
#    #from basic_point import PointSource
##
#    G = GeneralStepper()
##
#    f0 = 4.8066e9
##
#    #probe = AnritsuRFPulser("GPIB::17")
#    probe = AeroflexGen("3010S1", "3025S1")
#    probe.power = -10.0
#    probe.freq = f0
#
#    #control = AnritsuRFPulser("GPIB::8")
#    #control.voltage = 0.01
#    #control.power=-15
#    #control.pulsing = 'Off'
#    #control.freq = f0
#    #control.leveling = True
#
#    yok = Yoko("GPIB::11")
#    time.sleep(1)
#    yok.output = 'on'
#    time.sleep(1)
#
#    dummy = DummyStepInstr()
#
#    iq = IQPointSource("3011D1", "3035D1")
#    #iq = PointSource()
#    iq.center_frequency = f0
#    iq.ref_amplitude = -10
#    iq.sample_rate = 5000000
#    iq.averages = 500000
#    tracer = GeneralTracer(is_sub_measurement=True)
#    tracer.step_instrument = dummy #probe
#    tracer.step_parameter = 'dummy' #'power'
#    tracer.start_value = -20.0
#    tracer.stop_value = -10.0
#    tracer.step_points = 2
#    #tracer.step_instrument = yok
#    #tracer.step_parameter = 'voltage'
#    #tracer.start_value = 1.1
#    #tracer.stop_value = 1.5
#    #tracer.step_points = 81
#    tracer.step_pause = 0.05 #0.001
#    tracer.data_instrument = iq
#    tracer.data_names = ['Mag_rms', 'Mag_vec', 'Phase', 'I', 'Q']
#
#    G.step_instrument = yok
#    G.step_parameter =  'voltage'
#    G.sweep_instrument = tracer
#    G.start_value = -0.6 #-5.2
#    G.stop_value = -0.4  #6.0
#    G.step_points = 201 #22401
#    #G.step_instrument = dummy #probe #control
#    #G.step_parameter = 'dummy' #'voltage'
#    #G.sweep_instrument = tracer
#    #G.start_value = -30.0
#    #G.stop_value = -20.0
#    #G.step_points = 2
#    probe.output='On'
#    #control.output='Off'
#    #time.sleep(1)
#    #yok.voltage = -1.0
#    #time.sleep(1)
#    #yok.voltage = -2.0
#    #time.sleep(1)
#    #yok.voltage = -3.0
#    #time.sleep(1)
#    #yok.voltage = -4.0
#    #time.sleep(1)
#    #yok.voltage = -5.0
#    #time.sleep(1)

## -------- IQ, listening, no probing 2 --------
#    #from NetworkAnalyzer2 import NetworkAnalyzer2
#    from new_yoko import Yoko
#    from general_tracer import GeneralTracer
#    from anritsu_rf_pulser import AnritsuRFPulser
#    from iq_point import IQPointSource
#    from aeroflex_gen import AeroflexGen
#    from basic_point import PointSource
##
#    G = GeneralStepper()
##
#    f0 = 4.8066e9
##
#    #probe = AnritsuRFPulser("GPIB::17")
#    probe = AeroflexGen("3010S1", "3025S1")
#    probe.power = -10.0
#    probe.freq = f0
#
#    control = AnritsuRFPulser("GPIB::8")
#    control.power=-15.0
#    #control.voltage = 0.095
#    control.pulsing = 'Off'
#    control.freq = f0
#    control.leveling = True
#
#    yok = Yoko("GPIB::11")
#    time.sleep(1)
#    yok.output = 'on'
#    time.sleep(1)
#
#    iq = IQPointSource("3011D1", "3035D1")
#    #iq = PointSource()
#    iq.center_frequency = f0
#    iq.ref_amplitude = -10
#    iq.sample_rate = 5000000
#    iq.averages = 1000000
#    tracer = GeneralTracer(is_sub_measurement=True)
#    tracer.step_instrument = yok
#    tracer.step_parameter = 'voltage'
#    tracer.start_value = -0.705
#    tracer.stop_value = -0.5
#    tracer.step_points = 2
#    tracer.step_pause = 0.001
#    tracer.data_instrument = iq
#    tracer.data_names = ['Mag_rms', 'Mag_vec', 'Phase', 'I', 'Q']
#
#    G.step_instrument = control
#    G.step_parameter = 'power'
#    G.sweep_instrument = tracer
#    G.start_value = -40.0 #14.2066e9
#    G.stop_value = -10.0 #14.8066e9
#    G.step_points = 601
#    probe.output='Off'
#    control.output='On'

# -------- DSA --------
    #from anritsu_rf_pulser import AnritsuRFPulser
    #from new_yoko import Yoko
    ##from aeroflex_iq import AeroflexIQ
    ##from dsa8200 import DSA8200
    #from dsa8200_threaded import DSA8200
    #f0 = 4.8066e9
    #a = AnritsuRFPulser("GPIB::8")
    #G = GeneralStepper()
    #dsa=DSA8200("GPIB0::3::INSTR")
    #dsa.numMeas=5000  #5000 (4096)
    ##dig = AeroflexIQ("3011D1", "3035D1")
    ##dig.center_frequency = f0
    ##dig.ref_amplitude = -50
    ##dig.trigger_source = 'Front SMB'
    ##dig.trigger_edge = 'Rising'
    ##dig.sample_rate = 200e6
    ##dig.samples = 250
    ##dig.pretrigger_samples = 20
    ##dig.averages_per_trigger = 100000
    ##
    #yok = Yoko("GPIB::11")
    #time.sleep(1)
    #yok.voltage = -0.7
    #time.sleep(1)
    #yok.output = 'on'
    #time.sleep(1)
    #a.freq = f0
    #a.power = 0
    ##a.voltage=0.06
    #a.pulsing = 'Internal'
    #a.pulse_time = 100e-9
    #a.pulse_rate = 400000
    #a.leveling = True
    #
    ##G.step_instrument = yok
    ##G.sweep_instrument = dsa
    ##G.step_parameter = 'voltage'
    ##G.start_value = -0.8
    ##G.stop_value = -0.6
    ##G.step_points = 3
    ##G.sweep_data = ['Voltage']
    ##
    #G.step_instrument = a
    #G.sweep_instrument = dsa
    #G.step_parameter = 'freq'
    #G.start_value = 4.7866e9
    #G.stop_value = 4.8266e9
    #G.step_points = 3
    #G.sweep_data = ['Voltage']
    #
    #a.output = 'On'

### -------- IQ TWO-TONE SPECTROSCOPY 2nd round--------
#    #from NetworkAnalyzer2 import NetworkAnalyzer2
#    from new_yoko import Yoko
#    from general_tracer import GeneralTracer
#    from anritsu_rf_pulser import AnritsuRFPulser
#    from iq_point import IQPointSource
#    from aeroflex_gen import AeroflexGen
#    from basic_point import PointSource
##
#    G = GeneralStepper()
##
#    f0 = 4.8066e9
##
#    #probe = AnritsuRFPulser("GPIB::17")
#    probe = AeroflexGen("3010S1", "3025S1")
#    probe.power = -10.0
#    probe.freq = f0
#
#    control = AnritsuRFPulser("GPIB::8")
#    control.power = -24.0
#    control.pulsing = 'Off'
#    control.freq = f0
#    control.leveling = True
#
#    yok = Yoko("GPIB::11")
#    time.sleep(1)
#    yok.output = 'on'
#    time.sleep(1)
#
#    iq = IQPointSource("3011D1", "3035D1")
#    #iq = PointSource()
#    iq.center_frequency = f0
#    iq.ref_amplitude = -30
#    iq.sample_rate = 5000000
#    iq.averages = 3000000
#    tracer = GeneralTracer(is_sub_measurement=True)
#    tracer.step_instrument = yok
#    tracer.step_parameter = 'voltage'
#    tracer.start_value = -0.8
#    tracer.stop_value = -0.5
#    tracer.step_points = 151
#    tracer.step_pause = 0.001
#    tracer.data_instrument = iq
#    tracer.data_names = ['Mag_rms', 'Mag_vec', 'Phase', 'I', 'Q']
#
#    G.step_instrument = control
#    G.step_parameter = 'freq'
#    G.sweep_instrument = tracer
#    G.start_value = 4.2e9
#    G.stop_value = 5.4e9
#    G.step_points = 241
#    probe.output='On'
#    control.output='On'
##

##### -------- TWO-TONE SPECTROSCOPY reversed --------
##    #from NetworkAnalyzer2 import NetworkAnalyzer2
#    from new_yoko import Yoko
#    from general_tracer import GeneralTracer
#    from anritsu_rf_pulser import AnritsuRFPulser
#    from iq_point import IQPointSource
#    from aeroflex_gen import AeroflexGen
#    from basic_point import PointSource
#
#    G = GeneralStepper()
#
#    f0 = 4.8066e9
#
#    probe = AnritsuRFPulser("GPIB0::8::INSTR")
#    probe.power =-20.0
#    probe.freq = f0
#
##    control = AnritsuRFPulser("GPIB0::8::INSTR") #"GPIB::8")
#    control = AeroflexGen("3010S1", "3025S1")
#    control.power = -24.0
##    control.pulsing = 'Off'
#    control.freq = f0
##    control.leveling = True
#
#    yok = Yoko("GPIB0::11::INSTR")#"GPIB::11")
#    time.sleep(1)
#    yok.output = 'on'
#    time.sleep(1)
#
#    iq = IQPointSource("3011D1", "3035D1")
##    #iq = PointSource()
#    iq.center_frequency = f0
#    iq.ref_amplitude = -30
#    iq.sample_rate = 5000000
#    iq.averages = 30000
#    tracer = GeneralTracer(is_sub_measurement=True)
#    tracer.step_instrument = control
#    tracer.step_parameter = 'freq'
#    tracer.start_value = 4.2e9
#    tracer.stop_value = 5.4e9
#    tracer.step_points = 241
#    tracer.step_pause = 0.001
#    tracer.data_instrument = iq
#    tracer.data_names = ['Mag_rms', 'Mag_vec', 'Phase', 'I', 'Q']
#
#    G.step_instrument = yok
#    G.step_parameter = 'voltage'
#    G.sweep_instrument = tracer
#    G.start_value = -0.8
#    G.stop_value = -0.5
#    G.step_points = 151
#    probe.output='On'
#    control.output='On'