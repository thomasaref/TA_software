# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 15:12:21 2014

@author: thomasaref
"""
# Adapting SAWbit paper plots to python for future analysis




from TA_Fundamentals import (e, h, hbar, kB, eps0, pi, c_eta,
                          epsinf, cos, sqrt, exp, empty, mean_and_remove_offset)
#from TA_constants import Check
from Atom_HDF5 import Read_HDF5
from atom.api import Float, Dict, ContainerList, Coerced, Bool
from numpy import array, ndarray

#from Atom_Plotter import Plotter
from Atom_Boss import master as mc
from Atom_Base import Slave

class Fig2a(Slave):
    plot_all=Bool(False)
    """ Fig. 2a, the IDT background trace with qubit off resonance ("det" for "detuned")."""
    S11_offset = Float(-31.12).tag(desc="Background S11 value, chosen to put the flat part of the detuned S11 (panel a) curve at 0dB")
    det_freq=Coerced(ndarray, [0], coercer=array).tag(plot=True, plot_label='Frequency (GHz)')
    det_S11=Coerced(ndarray, [0], coercer=array).tag(plot=True, xdata="det_freq", plot_label='S11 with qubit detuned (dB)')
    det_S11_avg=Coerced(ndarray, [0], coercer=array).tag(plot=True, xdata="det_freq", plot_label='S11 with qubit detuned (dB)')
    def __init__(self, **kwargs):
        super(Fig2a, self).__init__(**kwargs)
        for key in self.members().keys():
            if self.get_tag(key, 'plot', self.plot_all):
                self.boss.plottables.append(key)


       # self.boss.plot_list[0].ylabel=self.get_tag(name, "plot_label", name)

a=Fig2a(name="Fig2a")
a.add_plot()
a.S11_offset=-31.12

mc.read_hdf5=Read_HDF5(main_dir="Background with qubit off resonance 2013-11-12_065035") #'Fig2_Fluxmap', 'Background with qubit off resonance 2013-11-12_065035'
data=mc.read_hdf5.open_and_read()

a.det_freq=data['mag']['Frequency']/1.0e9

a.det_S11=data['mag']['Mag']
a.det_S11_avg=  mean_and_remove_offset(a.det_S11, a.S11_offset, dimension=1) #mean(det_S11_raw, 2) - S11_offset


a.add_line_plot('det_S11_avg')
#a.add_img_plot('det_S11')
mc.plot_list[0].show()

#plot.add_img_plot(mag_vec, yok, linspace(0, len(anr)-1, len(anr)))

# Plot Fig. 2a

#plot(det_freq/1e9, det_S11_trace_amp*100, 'b')
#axis([freq_range(1)/1e9, freq_range(2)/1e9, 42, 109])
#title('Fig. 2a')
#xlabel('frequency [GHz]')
#ylabel('S11 with qubit detuned [%]')



# -----------------------------------------------------------------------
# Fig. 2e, cross section through the zoomed-in fluxmap ("zcs" for "zoomed cross section")
# -----------------------------------------------------------------------

class Fig2e(Slave):
    """ Fig. 2e, cross section through the zoomed-in fluxmap ("zcs" for "zoomed cross section")"""
    S11_offset = Float(-31.12).tag(desc="Background S11 value, chosen to put the flat part of the detuned S11 (panel a) curve at 0dB")
    data=Dict()
    det_freq=Coerced(ndarray, [0], coercer=array).tag(plot=True)
    det_S11=Coerced(ndarray, [0], coercer=array).tag(plot=True, xdata="det_freq")
    det_phase=Coerced(ndarray, [0], coercer=array).tag(plot=True, xdata="det_freq")
    S11=Coerced(ndarray, [0], coercer=array).tag(plot=True, xdata="det_freq")
    freq=Coerced(ndarray, [0], coercer=array).tag(plot=True, xdata="det_freq")
    phase=Coerced(ndarray, [0], coercer=array).tag(plot=True, xdata="det_freq")
    yoko=Coerced(ndarray, [0], coercer=array).tag(plot=True, xdata="det_freq")

zcs=Fig2e(name="Fig2e")

zcs.S11_offset=-31.2  #-31.1420 # -31.180

mc.read_hdf5=Read_HDF5(main_dir='S11 flux map, upward transition 2013-11-12_004003')
data=mc.read_hdf5.open_and_read()
zcs.S11=data['mag']['Mag']
zcs.freq=data['mag']['Frequency']
zcs.yoko=data['mag']['Yoko voltage']
zcs.phase=data['phase']['Phase']

mc.read_hdf5=Read_HDF5(main_dir='Reference with qubit off resonance 2013-11-12_005929')
data=mc.read_hdf5.open_and_read()
zcs.det_S11=data["mag"]["Mag"]
zcs.det_phase=data['phase']['Phase']

#from TA_constants import flux_per_volt

from TA_GaAs102_constants import flux_per_volt
bfm_flux_offset = 0.1195
zfm_flux_offset =  bfm_flux_offset + 0.0018;      # X For now
zfm_flux = zcs.yoko*flux_per_volt - zfm_flux_offset;

#zcs_center_freq_range = [4.8060e9, 4.807e9] # Fluxmap flux index where the qubit is in tune, to average over.
#zcs_center_freq_index = 104:106

#zcs_center_freq_index = find(zfm_freq>=zcs_center_freq_range(1) & zfm_freq<=zcs_center_freq_range(2));


# Import raw data
#zfm_dir = fullfile(C.data_base_dir, 'Fig2_Fluxmap', 'S11 flux map, upward transition 2013-11-12_004003');
#zfm_detuned_dir = fullfile(C.data_base_dir, 'Fig2_Fluxmap', 'Reference with qubit off resonance 2013-11-12_005929');
#zfm_S11_raw = importdata(fullfile(zfm_dir, 'Mag.txt'));
#zfm_phase_raw = importdata(fullfile(zfm_dir, 'Phase.txt'));
#zfm_Vyoko_raw = importdata(fullfile(zfm_dir, 'Yoko voltage.txt'));
#zfm_freq_raw = importdata(fullfile(zfm_dir, 'Frequency.txt'));
#zfm_detuned_S11_raw = importdata(fullfile(zfm_detuned_dir, 'Mag.txt'));
#zfm_detuned_phase_raw = importdata(fullfile(zfm_detuned_dir, 'Phase.txt'));

## Process the raw imported data
#
#zfm_detuned_phase = zfm_detuned_phase_raw*pi/180;
#zfm_detuned_S11_dB = zfm_detuned_S11_raw - S11_offset;
#zfm_detuned_S11_amp = 10.^(zfm_detuned_S11_dB/20);
#zfm_detuned_S11_complex = mean(zfm_detuned_S11_amp*exp(1j*zfm_detuned_phase), 2);
#
#zfm_phase = zfm_phase_raw*pi/180;
#zfm_S11_dB = zfm_S11_raw - S11_offset;
#zfm_S11_amp = 10.^(zfm_S11_dB/20);
#zfm_S11_complex = zfm_S11_amp*exp(1j*zfm_phase);
#
#zfm_S11_minus_detuned_complex = zfm_S11_complex - repmat(zfm_detuned_S11_complex, 1, length(zfm_flux));
#
#

#zfm_flux_offset =  bfm_flux_offset + 0.0018      # X For now
#zfm_flux = zfm_Vyoko_raw*C.flux_per_volt - zfm_flux_offset
#
#zcs_flux = zfm_flux
#zcs_S11_minus_detuned_complex = mean(zfm_S11_minus_detuned_complex[104:106, :], 0)
#
#P_in = 1e-20;   # Power in watt
#d_omega = C.detuning(zcs_flux, C);
#
# Calculate the reflection simply
#N_in = P_in/C.hf0;
#zcs_S11_qubit_calc = C.r_qubit(d_omega, N_in, C);
#zcs_S11_minus_detuned_tot_calc = C.S11_IDT_no_IDT_ref(zcs_S11_qubit_calc, C);
#
#figure
#plot(zcs_flux, abs(zcs_S11_minus_detuned_complex), 'b.', zcs_flux, abs(zcs_S11_minus_detuned_tot_calc), 'r')
#xlabel('\Phi/\Phi_0')
#ylabel('S11 [amplitude units]')
#axis([zoom_flux_range(1), zoom_flux_range(2), S11_range(1), S11_range(2)])
#title('S11 zoomed cross section with background subtracted')

