# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:46:49 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read, TA88_Fund, qdt, TransLyzer, ReflLyzer, TransTimeLyzer, refl_fano, fano
from atom.api import Typed, Unicode, Float, observe, FloatRange, Int, Enum
from h5py import File
from taref.core.universal import Array
from numpy import float64, linspace, shape, reshape, squeeze, mean, angle, absolute, sin, pi
from taref.core.atom_extension import tag_Property
from taref.physics.units import dB
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from taref.core.agent import Operative
from taref.core.log import log_debug
from taref.physics.fundamentals import e, h
from scipy.optimize import leastsq
from numpy import array, log10, fft, exp


class S4A1_Midpeak(TransLyzer):
    def _default_name(self):
        return "S4A1_midpeak"

    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0316/S4A1_TA88_coupling_search_midpeak.hdf5")

    @tag_Property(sub=True)
    def indices(self):
        return range(65, 984+1)

class S1A4_Midpeak(TransLyzer):
    def _default_name(self):
        return "S1A4_midpeak"

    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0308/S1A4_TA88_coupling_search_midpeak.hdf5")

    @tag_Property(sub=True)
    def indices(self):
        return range(65, 984+1)

class S4A1_pulse(TransTimeLyzer):
    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0317/S4A1_freq_pulse_fluxswp.hdf5")
    def _default_name(self):
        return "D0317_timedomain"

    @tag_Property(sub=True)
    def indices(self):
        return range(9, 47+1)

class S1A1_Midpeak(ReflLyzer):
    def _default_name(self):
        return "S1A1_midpeak"

    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0315/S1A1_TA88_coupling_search_midpeak.hdf5")

    @tag_Property(sub=True)
    def indices(self):
        return range(65, 984+1)

class S4A4_Midpeak(ReflLyzer): #placeholder
    def _default_name(self):
        return "S4A4_midpeak"

    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0314/S4A4_TA88_coupling_search.hdf5") #"Data_0312/S4A1_TA88_coupling_search.hdf5")

class S4A4_Wide(ReflLyzer):
    def _default_name(self):
        return "S4A4_wide"

    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0314/S4A4_TA88_coupling_search.hdf5") #"Data_0312/S4A1_TA88_coupling_search.hdf5")

    @tag_Property()
    def p_guess(self):
        return [200e6,4.5e9, 0.002, 0.022, 0.1]

    def _default_fit_func(self):
        return refl_fano

    @tag_Property(sub=True)
    def indices(self):
        tlist=range(81, 120+1)
        tlist.extend(range(137, 145+1))
#       tlist.extend(range(137, 260+1))
        tlist.extend(range(245, 260+1))
        tlist.extend(range(269, 320+1))
        #tlist.extend(range(343, 345+1))
        tlist.extend(range(411, 449+1))
        tlist.extend(range(485, 498+1))
        return tlist#, [490]]#, [186]]

class S1A1_Wide(ReflLyzer):
    def _default_name(self):
        return "S1A1_wide"

    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0310/S1A1_TA88_coupling_search.hdf5") #"Data_0312/S4A1_TA88_coupling_search.hdf5")

    @tag_Property()
    def p_guess(self):
        return [200e6,4.5e9, 0.002, 0.022, 0.1]

    def _default_fit_func(self):
        return refl_fano

    @tag_Property(sub=True)
    def indices(self):
        tlist=range(81, 120+1)
        tlist.extend(range(137, 145+1))
#       tlist.extend(range(137, 260+1))
        tlist.extend(range(245, 260+1))
        tlist.extend(range(269, 320+1))
        #tlist.extend(range(343, 345+1))
        tlist.extend(range(411, 449+1))
        tlist.extend(range(485, 498+1))
        return tlist#, [490]]#, [186]]

class S1A4_Wide(TransLyzer):
    def _default_name(self):
        return "S1A4_wide"

    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0307/S1A4_TA88_coupling_search.hdf5")

    @tag_Property()
    def p_guess(self):
        return [200e6,4.5e9, 0.002, 0.022, 0.1]

    def _default_fit_func(self):
        return fano

    @tag_Property(sub=True)
    def indices(self):
        tlist=range(81, 120+1)
        tlist.extend(range(137, 145+1))
#       tlist.extend(range(137, 260+1))
        tlist.extend(range(245, 260+1))
        tlist.extend(range(269, 320+1))
        #tlist.extend(range(343, 345+1))
        tlist.extend(range(411, 449+1))
        tlist.extend(range(485, 498+1))
        return tlist#, [490]]#, [186]]

class S4A1_Wide(TransLyzer):
    def _default_name(self):
        return "S4A1_wide"

    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0312/S4A1_TA88_coupling_search.hdf5")

    @tag_Property()
    def p_guess(self):
        return [200e6,4.5e9, 0.002, 0.022, 0.1]

    def _default_fit_func(self):
        return fano

    @tag_Property(sub=True)
    def indices(self):
        tlist=range(81, 120+1)
        tlist.extend(range(137, 145+1))
#       tlist.extend(range(137, 260+1))
        tlist.extend(range(245, 260+1))
        tlist.extend(range(269, 320+1))
        #tlist.extend(range(343, 345+1))
        tlist.extend(range(411, 449+1))
        tlist.extend(range(485, 498+1))
        return tlist#, [490]]#, [186]]

class S3A4_Wide(TransLyzer):
    def _default_name(self):
        return "S3A4_wide"

    def _default_rd_hdf(self):
           return TA88_Read(main_file="Data_0322/S3A4A1_TA88_gate_wide_frq_fluxswp.hdf5")
    #@tag_Property(plot=True, sub=True)
    #def MagAbsFilt(self):
    #    return absolute(self.MagcomFilt-mean(self.MagcomFilt[0:1, :], axis=0, keepdims=True))

    port_name=Unicode('S11')
    VNA_name=Unicode("VNA")
    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            print f["Traces"].keys()
            Magvec=f["Traces"][self.VNA_name+" - {0}".format(self.port_name)]
            data=f["Data"]["Data"]
            self.comment=f.attrs["comment"]
            self.yoko=data[:,0,0].astype(float64)
            fstart=f["Traces"][self.VNA_name+' - {0}_t0dt'.format(self.port_name)][0][0]
            fstep=f["Traces"][self.VNA_name+' - {0}_t0dt'.format(self.port_name)][0][1]
            sm=shape(Magvec)[0]
            sy=shape(data)
            print sy
            s=(sm, sy[0], 1)#sy[2])
            Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
            Magcom=reshape(Magcom, s, order="F")
            self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            self.Magcom=squeeze(Magcom)
            self.stop_ind=len(self.yoko)-1

class S3A4_Midpeak(S3A4_Wide):
    def _default_name(self):
        return "S3A4_midpeak"

    def  _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0326/S3A4A1_gate_fluxswp_midpeak.hdf5")

class S3A1_Midpeak(S3A4_Wide):
    def _default_name(self):
        return "S3A1_midpeak"

    def  _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0326/S3A4A1_gate_fluxswp_midpeak.hdf5")

if __name__=="__main__":
    slow=0#False
    wp=Plotter()

    if 0:
        s4a1_mp=S4A1_Midpeak(filt_start_ind=5, filt_end_ind=52, on_res_ind=260)
        s4a1_mp.read_data()
        #b1=Plotter()
        s4a1_mp.magabs_colormesh("colormesh S4A1")
        s4a1_mp.magabsfilt_colormesh("filtcolormesh S4A1")
        s4a1_mp.filt_compare("filt_compare_off_res", s4a1_mp.start_ind )
        s4a1_mp.filt_compare("filt_compare_on_res", s4a1_mp.on_res_ind)
        s4a1_mp.ifft_plot("ifft_S4A1")

        if slow:
            s4a1_mp.plot_widths(wp)

    if 0:
        s1a4_mp=S1A4_Midpeak(filt_start_ind=5, filt_end_ind=52, on_res_ind=219)
        s1a4_mp.read_data()
        #s1a4_mp.magabs_colormesh("colormesh S1A4")
        #s1a4_mp.magabsfilt_colormesh("filtcolormesh S1A4")
        #s1a4_mp.ifft_plot("ifft_S1A4")

        #a2.filt_compare(a2.start_ind, plotter="S1A4 filt_compare_off_res")
        #a2.filt_compare(a2.on_res_ind, plotter="S1A4 filt_compare_on_res")
        if slow:
            s1a4_mp.plot_widths(wp)

    if 0:
        ps4a1=S4A1_pulse(f_ind=25, on_res_ind=260)#filt_start_ind=5, filt_end_ind=52, on_res_ind=219)
        ps4a1.read_data()
        ps4a1.magabs_colormesh("S4A1 time magabs")
        ps4a1.magabsfilt_colormesh("filtcolormesh S4A1_time")
        #a2.filt_compare(a2.start_ind, bb2)
        ps4a1.filt_compare("filt_compare_off_res", ps4a1.start_ind)
        ps4a1.filt_compare("filt_compare_on_res", ps4a1.on_res_ind)
        if slow:
            ps4a1.plot_widths(wp)
        print ps4a1.probe_pwr
    if 0:
        s1a1_mp=S1A1_Midpeak(filt_start_ind=33, filt_end_ind=58, on_res_ind=260)
        s1a1_mp.read_data()
        s1a1_mp.magabs_colormesh("S1A1 magabs")
        s1a1_mp.magabsfilt_colormesh("filtcolormesh S1A1")
        #a2.filt_compare(a2.start_ind, bb2)
        #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
        #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
        s1a1_mp.ifft_plot("ifft_S1A1")
        if slow:
            s1a1_mp.plot_widths(wp)

    if 0:
        s4a4_w=S4A4_Wide(filt_start_ind=0, filt_end_ind=240, on_res_ind=240) #80, 116
        s4a4_w.read_data()
        s4a4_w.magabs_colormesh("S4A4 magabs")
        s4a4_w.magabsfilt_colormesh("filtcolormesh S4A4")
        s4a4_w.magdBfilt_colormesh("filtdB S1A1 wide")
        s4a4_w.magdBfiltbgsub_colormesh("filtdBbgsub S1A1 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
        #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
        s4a4_w.ifft_plot("ifft_S4A4")

        if slow:
            s4a4_w.plot_widths(wp)

    if 0:
        s1a1_w=S1A1_Wide(filt_start_ind=0, filt_end_ind=240, on_res_ind=240) #140, 240
        s1a1_w.read_data()
        s1a1_w.magabs_colormesh("S1A1 magabs")
        s1a1_w.magabsfilt_colormesh("filtcolormesh S1A1 wide")
        s1a1_w.magdBfilt_colormesh("filtdB S1A1 wide")
        s1a1_w.magdBfiltbgsub_colormesh("filtdBbgsub S1A1 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
        #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
        s1a1_w.ifft_plot("ifft_S1A1 wide")

        if slow:
            s1a1_w.plot_widths(wp)
    if 0:
        s1a4_w=S1A4_Wide(filt_start_ind=90, filt_end_ind=190, on_res_ind=238)
        s1a4_w.read_data()
        #s1a4_w.magabs_colormesh("S1A4 wide magabs")
        s1a4_w.magdBfilt_colormesh("filtdB S1A4 wide")
        s1a4_w.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")

        #a2.filt_compare(a2.start_ind, bb2)
        #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
        #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
        s1a4_w.ifft_plot("ifft_S1A4 wide")

        if slow:
            s1a4_w.plot_widths(wp)

    if 0:
        s4a1_w=S4A1_Wide(filt_start_ind=90, filt_end_ind=190, on_res_ind=238)
        s4a1_w.read_data()
        s4a1_w.magabs_colormesh("S4A1 wide magabs")
        s4a1_w.magabsfilt_colormesh("filtcolormesh S4A1 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
        #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
        s4a1_w.ifft_plot("ifft_S1A4 wide")

        if slow:
            s4a1_w.plot_widths(wp)

    if 0:
        s3a4_w=S3A4_Wide(filt_start_ind=170, filt_end_ind=495, on_res_ind=490)
        s3a4_w.read_data()
        s3a4_w.magabs_colormesh("S3A1 wide magabs")
        s3a4_w.magabsfilt_colormesh("filtcolormesh S4A1 wide")
        s3a4_w.magdBfilt_colormesh("filtdB S1A4 wide")
        s3a4_w.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
        #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
        s3a4_w.ifft_plot("ifft_S1A4 wide")
        s3a4_w.ifft_dif_plot("ifft__dif_S1A4 wide")

        #if slow:
        #    s4a1_w.plot_widths(wp)
    if 0:
        s3a4_mp=S3A4_Midpeak(filt_start_ind=20, filt_end_ind=35, on_res_ind=260, VNA_name='TA VNA2',
                  rd_hdf=TA88_Read(main_file="Data_0327/S3A4A1_gate_fluxswp_midpeak_0dBm.hdf5")) #20, 35
        s3a4_mp.read_data()
        s3a4_mp.magabs_colormesh("S3A4 midpeak magabs")
        s3a4_mp.magabsfilt_colormesh("filtcolormesh S3A4 mp")
        s3a4_mp.magdBfilt_colormesh("filtdB S1A4 wide")
        s3a4_mp.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        s3a4_mp.filt_compare("filt_compare_off_res", s3a4_mp.start_ind)
        s3a4_mp.filt_compare("filt_compare_on_res", s3a4_mp.on_res_ind)
        s3a4_mp.ifft_plot("ifft_S3A4 midpeak")
        s3a4_mp.ifft_dif_plot("ifft__dif_S1A4 wide")
        #print self.agent_dict.iter
        print s3a4_mp.get_agents(Operative)
        print isinstance(s3a4_mp, Operative)
        print isinstance(s3a4_mp, TransLyzer)
        print isinstance(s3a4_mp, TransTimeLyzer)

        #print dir(s3a4_mp.agent_dict["ifft_S3A4 midpeak"])
        print s3a4_mp.plots

    if 0:

        s3a1_mp=S3A1_Midpeak(filt_start_ind=28, filt_end_ind=40, on_res_ind=260, VNA_name='TA VNA2', port_name='S21',
                             rd_hdf=TA88_Read(main_file="Data_0327/S3A4A1_gate_fluxswp_midpeak_0dBm.hdf5")) #29, 40
        s3a1_mp.read_data()
        s3a1_mp.magabs_colormesh("S3A4 midpeak magabs")
        s3a1_mp.magabsfilt_colormesh("filtcolormesh S3A4 mp")
        s3a1_mp.magdBfilt_colormesh("filtdB S1A4 wide")
        s3a1_mp.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        s3a1_mp.filt_compare("filt_compare_off_res", s3a1_mp.start_ind)
        s3a1_mp.filt_compare("filt_compare_on_res", s3a1_mp.on_res_ind)
        s3a1_mp.ifft_plot("ifft_S1A4 wide")
        s3a1_mp.ifft_dif_plot("ifft__dif_S1A4 wide")

    if 0:
        s3a4_mp=S3A4_Midpeak(filt_start_ind=95, filt_end_ind=144, on_res_ind=286, VNA_name='TA VNA2',
                  rd_hdf=TA88_Read(main_file="Data_0328/S3A4A1_gate_fluxswp_0dBm.hdf5")) #20, 35
        s3a4_mp.read_data()
        s3a4_mp.magabs_colormesh("S3A4 midpeak magabs")
        s3a4_mp.magabsfilt_colormesh("filtcolormesh S3A4 mp")
        s3a4_mp.magdBfilt_colormesh("filtdB S1A4 wide")
        s3a4_mp.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        s3a4_mp.filt_compare("filt_compare_off_res", s3a4_mp.start_ind)
        #s3a4_mp.filt_compare("filt_compare_on_res", s3a4_mp.on_res_ind)
        s3a4_mp.filt_compare("filt_compare_on_res", 260)
        #s3a4_mp.filt_compare("filt_compare_on_res", 236)


        s3a4_mp.ifft_plot("ifft_S3A4 midpeak")
        s3a4_mp.ifft_dif_plot("ifft__dif_S1A4 wide")
        #print self.agent_dict.iter
        print s3a4_mp.get_agents(Operative)
        print isinstance(s3a4_mp, Operative)
        print isinstance(s3a4_mp, TransLyzer)
        print isinstance(s3a4_mp, TransTimeLyzer)

        #print dir(s3a4_mp.agent_dict["ifft_S3A4 midpeak"])
        print s3a4_mp.plots

    if 0:

        s3a1_mp=S3A1_Midpeak(filt_start_ind=121, filt_end_ind=170, on_res_ind=286, VNA_name='TA VNA2', port_name='S21',
                             rd_hdf=TA88_Read(main_file="Data_0328/S3A4A1_gate_fluxswp_0dBm.hdf5")) #29, 40
        s3a1_mp.read_data()
        s3a1_mp.magabs_colormesh("S3A4 midpeak magabs")
        s3a1_mp.magabsfilt_colormesh("filtcolormesh S3A4 mp")
        s3a1_mp.magdBfilt_colormesh("filtdB S1A4 wide")
        s3a1_mp.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        s3a1_mp.filt_compare("filt_compare_off_res", s3a1_mp.start_ind)
        #s3a1_mp.filt_compare("filt_compare_on_res", s3a1_mp.on_res_ind)
        s3a1_mp.filt_compare("filt_compare_on_res", 260)
        #s3a1_mp.filt_compare("filt_compare_on_res", 236)

        s3a1_mp.ifft_plot("ifft_S1A4 wide")
        s3a1_mp.ifft_dif_plot("ifft__dif_S1A4 wide")


    if 0:
        s3a4_w=S3A4_Wide(filt_start_ind=0, filt_end_ind=495, on_res_ind=260, VNA_name='TA VNA2',
                         rd_hdf=TA88_Read(main_file="Data_0329/S3A4A1_widegate_fluxswp_higherpwr.hdf5")) #29, 40)
        s3a4_w.read_data()
        s3a4_w.magabs_colormesh("S3A1 wide magabs")
        s3a4_w.magabsfilt_colormesh("filtcolormesh S4A1 wide")
        s3a4_w.magdBfilt_colormesh("filtdB S1A4 wide")
        s3a4_w.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
        #a2.filt_compare(a2.start_ind, bb2)
        #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
        #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
        s3a4_w.ifft_plot("ifft_S1A4 wide")
        s3a4_w.ifft_dif_plot("ifft__dif_S1A4 wide")

        #if slow:
        #    s4a1_w.plot_widths(wp)

    Np=9
    K2=0.048
    freq=linspace(4e9, 5e9, 1000)
    class Fitter3(Operative):
        base_name="fitter"
        mult=FloatRange(0.001, 5.0, 0.82).tag(tracking=True)
        f0=FloatRange(4.0, 6.0, 5.348).tag(tracking=True)
        offset=FloatRange(0.0, 100.0, 18.0).tag(tracking=True)

        @tag_Property(plot=True, private=True)
        def G_f(self):
            f0=self.f0*1.0e9
            return self.offset*1e6+self.mult*0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*pi*(freq-f0)/f0))**2

        @observe("f0", "mult", "offset")
        def update_plot(self, change):
            if change["type"]=="update":
                self.get_member("G_f").reset(self)
                wp.plot_dict["G_f"].clt.set_ydata(self.G_f)
                wp.draw()

    d=Fitter3()
    wp.line_plot("G_f", freq, d.G_f, label="theory")


class S3A4_Power(TransLyzer):
    def _default_name(self):
        return "S3A4_power"

    def _default_rd_hdf(self):
           return TA88_Read(main_file="Data_0404/S3A4A1_gate_pwr_swp_midpeak.hdf5")
    #@tag_Property(plot=True, sub=True)
    #def MagAbsFilt(self):
    #    return absolute(self.MagcomFilt-mean(self.MagcomFilt[0:1, :], axis=0, keepdims=True))

    pwi=Int(8)
    fqi=Int(280)
    port_name=Unicode('S11')
    VNA_name=Unicode("VNA")

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            print f["Traces"].keys()
            Magvec=f["Traces"][self.VNA_name+" - {0}".format(self.port_name)]
            data=f["Data"]["Data"]
            self.comment=f.attrs["comment"]
            self.pwr=data[:,0,0].astype(float64)
            self.yoko=data[0,1,:].astype(float64)

            print shape(data)
            print shape(self.yoko)
            fstart=f["Traces"][self.VNA_name+' - {0}_t0dt'.format(self.port_name)][0][0]
            fstep=f["Traces"][self.VNA_name+' - {0}_t0dt'.format(self.port_name)][0][1]
            sm=shape(Magvec)[0]
            sy=shape(data)
            print sy
            s=(sm, sy[0], sy[2])
            print s
            Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
            Magcom=reshape(Magcom, s, order="F")
            self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            Magcom=squeeze(Magcom)
            self.Magcom=Magcom[:, 10, :]
            self.stop_ind=len(self.yoko)-1
            return array([[self.fft_filter_full(m, n, Magcom) for n in range(len(self.yoko))] for m in range(len(self.pwr))]).transpose()


    #@tag_Property(plot=True, sub=True)
    #def MagdBFiltbgsub(self):
    #    return self.MagAbsFilt/mean(self.MagAbsFilt[:, :, 0:5], axis=1, keepdims=True)
    #    return self.MagdBFilt-10.0*log10(mean(self.MagAbsFilt[:, :, 0:5], axis=1, keepdims=True))

    @tag_Property(plot=True, sub=True)
    def MagcomFilt(self):
        return array([self.fft_filter(n) for n in range(len(self.yoko))]).transpose()

    def fft_filter_full(self, m, n, Magcom):
        myifft=fft.ifft(Magcom[:, m, n])
        myifft[self.filt_end_ind:-self.filt_end_ind]=0.0
        if self.filt_start_ind!=0:
            myifft[:self.filt_start_ind]=0.0
            myifft[-self.filt_start_ind:]=0.0
        #return angle(myifft[44])
        return absolute(myifft[69])
        #return max(absolute(myifft))
        return fft.fft(myifft)
if 0:
    s3a4_pow=S3A4_Power(filt_start_ind=8, filt_end_ind=16, on_res_ind=42, VNA_name='ta', port_name='S21')#,
                     #rd_hdf=TA88_Read(main_file="Data_0329/S3A4A1_widegate_fluxswp_higherpwr.hdf5")) #29, 40)
    mg=s3a4_pow.read_data()
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), self.pwr, self.yoko, mg)#angle(mg[250, :, :]))
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        #plotter.xlabel="Yoko (V)"
        #plotter.ylabel="Frequency (Hz)"
        #plotter.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_pow, Plotter(), mg)

if 0:
    s3a4_pow=S3A4_Power(filt_start_ind=11, filt_end_ind=17, on_res_ind=91, VNA_name='ta', port_name='S21',
                     rd_hdf=TA88_Read(main_file="Data_0405/S3A4A1_gate_pwr_swp_midpeak.hdf5")) #29, 40)
    mg=s3a4_pow.read_data()
    s3a4_pow.magabs_colormesh("S3A1 wide magabs")
    s3a4_pow.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_pow.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_pow.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
    s3a4_pow.ifft_plot("ifft_S1A4 wide")
    s3a4_pow.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), self.pwr, self.yoko, angle(mg[250,  :, :]))
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        #plotter.xlabel="Yoko (V)"
        #plotter.ylabel="Frequency (Hz)"
        #plotter.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_pow, Plotter(), mg)
#    s3a4_pow.magabs_colormesh("S3A1 wide magabs")
#    s3a4_pow.magabsfilt_colormesh("filtcolormesh S4A1 wide")
#    s3a4_pow.magdBfilt_colormesh("filtdB S1A4 wide")
#    s3a4_pow.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
#    #a2.filt_compare(a2.start_ind, bb2)
#    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
#    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
#    s3a4_pow.ifft_plot("ifft_S1A4 wide")
#    s3a4_pow.ifft_dif_plot("ifft__dif_S1A4 wide")

if 0:
    s3a4_pow=S3A4_Power(filt_start_ind=13, filt_end_ind=18, on_res_ind=131, VNA_name='RS VNA', port_name='S21',
                     rd_hdf=TA88_Read(main_file="Data_0406/S3A1_gate_listen_fft.hdf5")) #29, 40)
    mg=s3a4_pow.read_data()
    s3a4_pow.magabs_colormesh("S3A1 wide magabs")
    s3a4_pow.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_pow.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_pow.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
    s3a4_pow.ifft_plot("ifft_S1A4 wide")
    s3a4_pow.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), self.pwr, self.yoko, absolute(mg[ :, :]))
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_pow, Plotter(), mg)

if 0:
    s3a4_pow=S3A4_Power(filt_start_ind=40, filt_end_ind=55, on_res_ind=80, VNA_name='RS VNA', port_name='S21',
                     rd_hdf=TA88_Read(main_file="Data_0407/S3A1_gate_listen_fft2.hdf5")) #29, 40)
    mg=s3a4_pow.read_data()
    s3a4_pow.magabs_colormesh("S3A1 wide magabs")
    s3a4_pow.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_pow.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_pow.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
    s3a4_pow.ifft_plot("ifft_S1A4 wide")
    s3a4_pow.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), self.pwr, self.yoko, mg[ :, :])
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_pow, Plotter(), mg)
#    s3a4_pow.magabs_colormesh("S3A1 wide magabs")
#    s3a4_pow.magabsfilt_colormesh("filtcolormesh S4A1 wide")
#    s3a4_pow.magdBfilt_colormesh("filtdB S1A4 wide")
#    s3a4_pow.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
#    #a2.filt_compare(a2.start_ind, bb2)
#    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
#    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
#    s3a4_pow.ifft_plot("ifft_S1A4 wide")
#    s3a4_pow.ifft_dif_plot("ifft__dif_S1A4 wide")
class S3A4_TwoTone(TransLyzer):
    def _default_name(self):
        return "S3A4_twotone"

    def _default_rd_hdf(self):
           return TA88_Read(main_file="Data_0408/S3S4A1_twotone_fft_swp1.hdf5")
    #@tag_Property(plot=True, sub=True)
    #def MagAbsFilt(self):
    #    return absolute(self.MagcomFilt-mean(self.MagcomFilt[0:1, :], axis=0, keepdims=True))

    pwi=Int(8)
    fqi=Int(280)
    port_name=Unicode('S21')
    VNA_name=Unicode("RS VNA")

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            print f["Traces"].keys()
            Magvec=f["Traces"][self.VNA_name+" - {0}".format(self.port_name)]
            data=f["Data"]["Data"]
            self.comment=f.attrs["comment"]
            self.frq2=data[:,0,0].astype(float64)
            self.yoko=data[0,1,:].astype(float64)

            print shape(data)
            print shape(self.yoko)
            fstart=f["Traces"][self.VNA_name+' - {0}_t0dt'.format(self.port_name)][0][0]
            fstep=f["Traces"][self.VNA_name+' - {0}_t0dt'.format(self.port_name)][0][1]
            sm=shape(Magvec)[0]
            sy=shape(data)
            print sy
            s=(sm, sy[0], sy[2])
            print s
            Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
            Magcom=reshape(Magcom, s, order="F")
            self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            Magcom=squeeze(Magcom)
            self.Magcom=Magcom[:, 10, :]
            self.stop_ind=len(self.yoko)-1
            return array([[self.fft_filter_full(m, n, Magcom) for n in range(len(self.yoko))] for m in range(len(self.frq2))]).transpose()


    #@tag_Property(plot=True, sub=True)
    #def MagdBFiltbgsub(self):
    #    return self.MagAbsFilt/mean(self.MagAbsFilt[:, :, 0:5], axis=1, keepdims=True)
    #    return self.MagdBFilt-10.0*log10(mean(self.MagAbsFilt[:, :, 0:5], axis=1, keepdims=True))

    @tag_Property(plot=True, sub=True)
    def MagcomFilt(self):
        return array([self.fft_filter(n) for n in range(len(self.yoko))]).transpose()

    def fft_filter_full(self, m, n, Magcom):
        myifft=fft.ifft(Magcom[:, m, n])
        myifft[self.filt_end_ind:-self.filt_end_ind]=0.0
        if self.filt_start_ind!=0:
            myifft[:self.filt_start_ind]=0.0
            myifft[-self.filt_start_ind:]=0.0
        return angle(myifft[44])
        return absolute(myifft[44])
        return fft.fft(myifft)

if 0:
    s3a4_2t=S3A4_TwoTone(filt_start_ind=25, filt_end_ind=55, on_res_ind=80)#, VNA_name='RS VNA', port_name='S21',
                     #rd_hdf=TA88_Read(main_file="Data_0407/S3A1_gate_listen_fft2.hdf5")) #29, 40)
    mg=s3a4_2t.read_data()
    s3a4_2t.magabs_colormesh("S3A1 wide magabs")
    s3a4_2t.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_2t.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_2t.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
    s3a4_2t.ifft_plot("ifft_S1A4 wide")
    s3a4_2t.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), self.frq2, self.yoko, mg[ :, :])
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_2t, Plotter(), mg)

if 0:
    s3a4_2t=S3A4_TwoTone(filt_start_ind=15, filt_end_ind=35, on_res_ind=71,#, VNA_name='RS VNA', port_name='S21',
                     rd_hdf=TA88_Read(main_file="Data_0410/S3S4A1_twotone_fft_swp3.hdf5")) #29, 40)
    mg=s3a4_2t.read_data()
    s3a4_2t.magabs_colormesh("S3A1 wide magabs")
    s3a4_2t.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_2t.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_2t.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
    s3a4_2t.ifft_plot("ifft_S1A4 wide")
    s3a4_2t.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), self.frq2, self.yoko, (mg.transpose()-mean(mg[ :, 0:5], axis=1)).transpose())
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_2t, Plotter(), mg)

if 0:
    s3a4_2t=S3A4_TwoTone(filt_start_ind=15, filt_end_ind=35, on_res_ind=61,#, VNA_name='RS VNA', port_name='S21',
                     rd_hdf=TA88_Read(main_file="Data_0411/S3S4A1_twotone_fft_swp4.hdf5")) #29, 40)
    mg=s3a4_2t.read_data()
    s3a4_2t.magabs_colormesh("S3A1 wide magabs")
    s3a4_2t.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_2t.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_2t.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
    s3a4_2t.ifft_plot("ifft_S1A4 wide")
    s3a4_2t.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), self.frq2, self.yoko, (mg.transpose()-mean(mg[ :, 0:5], axis=1)).transpose())
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_2t, Plotter(), mg)

if 0:
    s3a4_2t=S3A4_TwoTone(filt_start_ind=58, filt_end_ind=495, on_res_ind=1193,#, VNA_name='RS VNA', port_name='S21',
                     rd_hdf=TA88_Read(main_file="Data_0412/S3S4A1_trans_sideband_fluxswp.hdf5")) #29, 40)
    mg=s3a4_2t.read_data()
    s3a4_2t.magabs_colormesh("S3A1 wide magabs")
    s3a4_2t.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_2t.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_2t.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    s3a4_2t.filt_compare("filt_compare_off_res", s3a4_2t.start_ind)
    s3a4_2t.filt_compare("filt_compare_on_res", s3a4_2t.on_res_ind)
    s3a4_2t.ifft_plot("ifft_S1A4 wide")
    s3a4_2t.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.line_plot("magabs_{}".format(self.name), mg)#self.frq2, self.yoko,
        #(mg.transpose()-mean(mg[ :, 0:5], axis=1)).transpose())
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_2t, Plotter(), mg)

if 0:
    s3a4_2t=S3A4_TwoTone(filt_start_ind=18, filt_end_ind=28, on_res_ind=7,#, VNA_name='RS VNA', port_name='S21',
                     rd_hdf=TA88_Read(main_file="Data_0414/S3S4A1_two_tone_test1.hdf5")) #29, 40)
    mg=s3a4_2t.read_data()
    s3a4_2t.magabs_colormesh("S3A1 wide magabs")
    s3a4_2t.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_2t.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_2t.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
    s3a4_2t.ifft_plot("ifft_S1A4 wide")
    s3a4_2t.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), self.frq2, self.yoko, mg) #(mg.transpose()-mean(mg[ :, 0:5], axis=1)).transpose())
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    magpow_colormesh(s3a4_2t, Plotter(), mg)

if 1:
    s3a4_pow=S3A4_Power(filt_start_ind=65, filt_end_ind=73, on_res_ind=10, VNA_name='RS VNA', port_name='S21',
                     rd_hdf=TA88_Read(main_file="Data_0415/S3S4A1_lowpwr_midpeak.hdf5")) #29, 40)
    mg=s3a4_pow.read_data()
    #Plotter().colormesh("blah", s3a4_pow.MagdB[1, :, 0:80].transpose()-s3a4_pow.MagdB[1, :, 81])
    #Plotter().line_plot("blah", s3a4_pow.pwr, s3a4_pow.MagdB[0, :, 30]-s3a4_pow.MagdB[0, :, 81])

    s3a4_pow.magabs_colormesh("S3A1 wide magabs")
    s3a4_pow.magabsfilt_colormesh("filtcolormesh S4A1 wide")
    s3a4_pow.magdBfilt_colormesh("filtdB S1A4 wide")
    s3a4_pow.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
    #a2.filt_compare(a2.start_ind, bb2)
    #s1a1_mp.filt_compare("filt_compare_off_res", s1a1_mp.start_ind)
    #s1a1_mp.filt_compare("filt_compare_on_res", s1a1_mp.on_res_ind)
    s3a4_pow.ifft_plot("ifft_S1A4 wide")
    #s3a4_pow.ifft_dif_plot("ifft__dif_S1A4 wide")
    print shape(mg)

    Plotter().colormesh("mag", 10*log10(mg)-10*log10(mg[28, :]))
    #for n in range(len(s3a4_pow.pwr)):
    #    Plotter().colormesh("pwr{}".format(n), absolute(mg[:, :, n]).transpose())#/absolute(mg[:,28,n]))

    def magpow_colormesh(self, plotter, mg):
        print shape(mg)
        plotter.colormesh("magabs_{}".format(self.name), 10*log10(absolute(mg[100, :, :]))-10*log10(absolute(mg[100,28, :])))
        print self.yoko
        #plotter.set_ylim(min(self.frequency), max(self.frequency))
        #plotter.set_xlim(min(self.yoko), max(self.yoko))
        plotter.mpl_axes.xlabel="Yoko (V)"
        plotter.mpl_axes.ylabel="Frequency (Hz)"
        plotter.mpl_axes.title="Magabs fluxmap {}".format(self.name)

    #magpow_colormesh(s3a4_pow, Plotter(), mg)

shower(wp)#
#def fano(x, p):
#    return p[2]*(((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]
#
#def refl_fano(x, p):
#    return p[2]*(1.0-((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]
#
#def fano_residuals(p,y,x):
#    return y - fano(x,p)
#
#def refl_fano_residuals(p,y,x):
#    return y - refl_fano(x,p)
#
#fano_dict={"Transmission" : (fano, fano_residuals),
#           "Reflection"   : (refl_fano, refl_fano_residuals)}
#
#ind_dict={"Transmission" : 30,
#          "Reflection"   : 37}
#
#class Lyzer(TA88_Fund):
#    rd_hdf=Typed(TA88_Read)
#    rt_atten=Float(40)
#    rt_gain=Float(23*2)
#    comment=Unicode().tag(read_only=True, spec="multiline")
#    frequency=Array().tag(unit="GHz", plot=True, label="Frequency")
#    yoko=Array().tag(unit="V", plot=True, label="Yoko")
#    Magcom=Array()#.tag()
#    offset=Float(-0.035)
#    flux_factor=Float(0.2925)
#    on_res_ind=Int()
#    start_ind=Int()
#    stop_ind=Int()
#    filt_ind=Int(52)
#
#    fit_type=Enum("Transmission", "Reflection")
#
#    @tag_Property()
#    def indices(self):
#        return [range(81, 120+1), range(137, 260+1), range(269, 320+1), range(411, 449+1)]#, [490]]#, [186]]
#
#    @tag_Property(plot=True)
#    def flux_par(self):
#        flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)
#        Ej=qdt.call_func("Ej", flux_over_flux0=flux_over_flux0)
#        return qdt._get_fq(Ej, qdt.Ec)
#
#    @tag_Property(plot=True)
#    def p_guess(self):
#        return [200e6,4.5e9, 0.002, 0.022, 0.1]
#
#    def full_fano_fit(self):
#        p = [200e6,4.5e9, 0.002, 0.022, 0.1]
#        fit_func, resid_func=fano_dict[self.fit_type]
#        var=self.MagAbsFilt**2
#        flux_par=self.flux_par
#        freqs=self.frequency
#        log_debug("started fano fitting")
#        fit_params=[self.fano_fit(n, var, flux_par, freqs, resid_func, p)  for n in range(len(self.frequency))]
#        fit_params=array(zip(*fit_params))
#        log_debug("ended fano fitting")
#        return fit_params
#
#    def plot_widths(self, plotter):
#        fit_params=self.full_fano_fit()
#        #print shape(zip(*fit_params))
#        plotter.scatter_plot("widths_{}".format(self.name), fit_params[0, :], absolute(fit_params[1, :]), color="red", label="-130 dBm")
#
#    def fano_fit(self, n, var, flux_par, frq, resid_func, p):
#        pbest= leastsq(resid_func, p, args=(var[n, :], flux_par), full_output=1)
#        best_parameters = pbest[0]
#        #log_debug(best_parameters)
#        if 0:#n==539 or n==554:#n % 10:
#            b.line_plot("magabs_flux", flux_par*1e-9, (magabs[n, :]-best_parameters[3])/best_parameters[2], label="{}".format(n), linewidth=0.2)
#            b.line_plot("lorentzian", flux_par*1e-9, fano(flux_par,best_parameters), label="fit {}".format(n), linewidth=0.5)
#        return (frq[n], best_parameters[0], best_parameters[1]-frq[n], best_parameters[2], best_parameters[3])
#
#    @tag_Property(plot=True)
#    def MagAbs(self):
#        return absolute(self.Magcom[:, :])
#
#    @tag_Property(plot=True)
#    def MagAbsFilt(self):
#        return absolute(self.MagcomFilt[:, :])
#
#    @tag_Property(plot=True)
#    def MagAbsFilt_sq(self):
#        return self.MagAbsFilt**2
#
#    @tag_Property(plot=True)
#    def MagcomFilt(self):
#        #return array([self.ifft_peak(n) for n in range(len(self.yoko))])
#        return array([self.fft_filter(n) for n in range(len(self.yoko))]).transpose()
#
#    def ifft_peak(self, n):
#        ind=ind_dict[self.fit_type]
#        return fft.ifft(self.Magcom[:,n])[ind]
#
#    def fft_filter(self, n):
#        #return self.Magcom[:, n]
#        myifft=fft.ifft(self.Magcom[:,n])
#        myifft[self.filt_ind:-self.filt_ind]=0.0
#        myifft[:5]=0.0
#        myifft[-5:]=0.0
#        return fft.fft(myifft)
#
#    def magabs_colormesh(self, plotter=None):
#        if plotter is None:
#            plotter=self.plotter
#        plotter.colormesh("magabs_{}".format(self.name), self.yoko, self.frequency, self.MagAbs)
#        plotter.set_ylim(min(self.frequency), max(self.frequency))
#        plotter.set_xlim(min(self.yoko), max(self.yoko))
#        plotter.xlabel="Yoko (V)"
#        plotter.ylabel="Frequency (Hz)"
#        plotter.title="Magabs fluxmap {}".format(self.name)
#
#    def ifft_plot(self, plotter=None):
#        if plotter is None:
#            plotter=self.plotter
#        plotter.line_plot("ifft_{}".format(self.name), absolute(fft.ifft(self.Magcom[:,self.on_res_ind])))
#        plotter.line_plot("ifft_{}".format(self.name), absolute(fft.ifft(self.Magcom[:,self.start_ind])))
#        plotter.line_plot("ifft_{}".format(self.name), absolute(fft.ifft(self.Magcom[:,self.stop_ind])))
#
#    def filt_compare(self, ind, plotter=None):
#        if plotter is None:
#            plotter=self.plotter
#        plotter.line_plot("magabs_{}".format(self.name), self.frequency, self.MagAbs[:, ind])
#        plotter.line_plot("magabs_{}".format(self.name), self.frequency, self.MagAbsFilt[:, ind])
#
#    def magabsfilt_colormesh(self, plotter=None):
#        if plotter is None:
#            plotter=self.plotter
#        plotter.colormesh("magabsfilt_{}".format(self.name), self.yoko, self.frequency, self.MagAbsFilt)
#        plotter.set_ylim(min(self.frequency), max(self.frequency))
#        plotter.set_xlim(min(self.yoko), max(self.yoko))
#        plotter.xlabel="Yoko (V)"
#        plotter.ylabel="Frequency (Hz)"
#        plotter.title="Magabs fluxmap {}".format(self.name)
#
#    def _default_main_params(self):
#        return ["rt_atten", "fridge_atten", "fridge_gain", "rt_gain", "comment", "flux_factor", "offset", "fit_type"]
#
#    def read_data(self):
#        with File(self.rd_hdf.file_path, 'r') as f:
#            Magvec=f["Traces"]["RS VNA - S21"]
#            data=f["Data"]["Data"]
#            self.comment=f.attrs["comment"]
#            self.yoko=data[:,0,0].astype(float64)
#            fstart=f["Traces"]['RS VNA - S21_t0dt'][0][0]
#            fstep=f["Traces"]['RS VNA - S21_t0dt'][0][1]
#            sm=shape(Magvec)[0]
#            sy=shape(data)
#            print sy
#            s=(sm, sy[0], 1)#sy[2])
#            Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
#            Magcom=reshape(Magcom, s, order="F")
#            self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
#            self.Magcom=squeeze(Magcom)
#            self.stop_ind=len(self.yoko)-1
#
#class S1A1_Midpeak(Lyzer):
#    def _default_name(self):
#        return "S1A1_midpeak"
#
#    def _default_rd_hdf(self):
#        return TA88_Read(main_file="Data_0315/S1A1_TA88_coupling_search_midpeak.hdf5")
#
#    def _default_on_res_ind(self):
#        return 257
#
#    def _default_fit_type(self):
#        return "Reflection"
#
#class S4A1_Midpeak2(Lyzer):
#    def _default_name(self):
#        return "S4A1_midpeak"
#
#    def _default_rd_hdf(self):
#        return TA88_Read(main_file="Data_0316/S4A1_TA88_coupling_search_midpeak.hdf5")
#
#    def _default_fit_type(self):
#        return "Transmission"
#
#    def _default_on_res_ind(self):
#        return 263
#
#class S1A4_Midpeak(Lyzer):
#    def _default_name(self):
#        return "S1A4_midpeak"
#
#    def _default_rd_hdf(self):
#        return TA88_Read(main_file="Data_0308/S1A4_TA88_coupling_search_midpeak.hdf5")
#
#    def _default_on_res_ind(self):
#        return 219
#
#    def _default_fit_type(self):
#        return "Transmission"
#
#class S4A4_Midpeak(Lyzer):
#    def _default_name(self):
#        return "S4A4_midpeak"
#
#    def _default_rd_hdf(self):
#        return TA88_Read(main_file="Data_0314/S4A4_TA88_coupling_search_midpeak.hdf5")
#
#    def _default_fit_type(self):
#        return "Reflection"
#
#    #@tag_Property(display_unit="dB", plot=True)
#    #def MagdB(self):
#    #    return self.Magcom[:, :]/dB-mean(self.Magcom[:, 169:171], axis=1, keepdims=True)/dB
#
#    #@tag_Property(plot=True)
#    #def Phase(self):
#    #    return angle(self.Magcom[:, :]-mean(self.Magcom[:, 169:170], axis=1, keepdims=True))
#
#    #    return absolute(self.Magcom[:, :])**2#-mean(self.Magcom[:, 0:1], axis=1, keepdims=True))
#
#
#if __name__=="__main2__":
#    a=S1A1_Midpeak()
#    a.read_data()
#    #b=Plotter()
#    #a.magabs_colormesh(b)
#    #a.magabsfilt_colormesh(b)
#    #bb=Plotter()
#    #a.ifft_plot(bb)
#    #b1=Plotter()
#    #a.filt_compare(a.start_ind, b1)
#    #b2=Plotter()
#    #a.filt_compare(a.on_res_ind, b2)
#    #b3=Plotter()
#    #a.plot_widths(b3)
#    a12=S4A1_Midpeak2()
#    a12.read_data()
#    a12.filt_compare(a1.start_ind, b2)
#    a12.filt_compare(a1.on_res_ind, b3)
#    #a12.magabs_colormesh(b1)
#    a12.magabsfilt_colormesh(b1)
#
#    #a1.plot_widths(b3)
#    a2=S1A4_Midpeak()
#    a2.read_data()
#    #a2.ifft_plot(bb)
#    #a2.plot_widths(b3)
#
#
#    #a3=S4A4_Midpeak()
#    #a3.read_data()
#    #a3.plot_widths(b3)
#
#    Np=9
#    K2=0.048
#    freq=linspace(4e9, 5e9, 1000)
#    class Fitter3(Operative):
#        base_name="fitter"
#        mult=FloatRange(0.001, 5.0, 0.82).tag(tracking=True)
#        f0=FloatRange(4.0, 6.0, 5.348).tag(tracking=True)
#        offset=FloatRange(0.0, 100.0, 18.0).tag(tracking=True)
#
#        @tag_Property(plot=True, private=True)
#        def G_f(self):
#            f0=self.f0*1.0e9
#            return self.offset*1e6+self.mult*0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*pi*(freq-f0)/f0))**2
#
#        @observe("f0", "mult", "offset")
#        def update_plot(self, change):
#            if change["type"]=="update":
#                self.get_member("G_f").reset(self)
#                b3.plot_dict["G_f"].clt.set_ydata(self.G_f)
#                b3.draw()
#
#    d=Fitter3()
#    b3.line_plot("G_f", freq, d.G_f, label="theory")
#    #b.colormesh("magabs2", yok, frq, absolute(mag))
#    #b.line_plot("bg", bgf, bgmc/dB)
#    def magdB_colormesh():
#        b.colormesh("magdB", a.yoko, a.frequency, a.MagdB)
#        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
#        b.set_ylim(4e9, 5.85e9)
#        b.xlabel="Yoko (V)"
#        b.ylabel="Frequency (Hz)"
#        b.title="Reflection fluxmap"
#
#    def magabs_colormesh():
#        b.colormesh("magabs", a.yoko, a.frequency, a.MagAbs)
#        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
#        #b.line_plot("flux_parabola", c.flux_parabola, c.flux_parabola, color="orange", alpha=0.4)
#
#        b.set_ylim(4e9, 5.85e9)
#        b.xlabel="Yoko (V)"
#        b.ylabel="Frequency (Hz)"
#        b.title="Reflection fluxmap"
#    #c.plotter=b
#
#    def phase_colormesh():
#        b.colormesh("phase", a.yoko, a.frequency, a.Phase)
#        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
#        b.set_ylim(4e9, 5e9)
#        b.xlabel="Yoko (V)"
#        b.ylabel="Frequency (Hz)"
#        b.title="Reflection fluxmap"
#
#    def magabs_cs():
#        #b.line_plot("magabs_cs", a.frequency, a.MagAbs[:, 0])
#        #b.line_plot("magabs_cs", a.frequency, a.MagAbs[:, 257])
#
#        if 0:
#            myifft=fft.ifft(a.Magcom[:,500])
#            myifft[50:-50]=0.0
#            #myifft[:20]=0.0
#            #myifft[-20:]=0.0
#            bg=fft.fft(myifft)
#            filt=[]
#            for n in range(len(a.yoko)):
#                myifft=fft.ifft(a.Magcom[:,n])
#                #b.line_plot("ifft", absolute(myifft))
#                myifft[50:-50]=0.0
#                #myifft[:20]=0.0
#                #myifft[-20:]=0.0
#                filt.append(absolute(fft.fft(myifft)-bg))
#            b.colormesh("filt", a.frequency, a.yoko, filt)
#        if 1:
#            myifft=fft.ifft(mag[:,500])
#            myifft[40:-40]=0.0
#            myifft[:20]=0.0
#            myifft[-20:]=0.0
#            bg=fft.fft(myifft)
#            filt=[]
#            for n in range(len(yok)):
#                myifft=fft.ifft(mag[:,n])
#                #b.line_plot("ifft", absolute(myifft))
#                myifft[50:-50]=0.0
#                #myifft[:20]=0.0
#                #myifft[-20:]=0.0
#                filt.append(absolute(fft.fft(myifft)))
#            b.colormesh("filt", frq, yok, filt)
#
#    def magabs_cs_fit():
#        def lorentzian(x,p):
#            return p[2]*(1.0-1.0/(1.0+((x-p[1])/p[0])**2))+p[3]
#
#        def fano(x, p):
#            return p[2]*(((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]
#
#        def refl_fano(x, p):
#            return p[2]*(1.0-((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]
#
#        def onebounce(x,p):
#            w=2*pi*x
#            k=2.0*pi*x/3488.0
#            Cc=0.0
#            D=500.0e-6
#            D1=300.0e-6
#            D2=200.0e-6
#            S12q=((p[4]*p[0]/6.28+(x-p[1])*2*pi)**2)/(p[0]**2+(p[4]*p[0]/6.28+x-p[1])**2)
#            S11q=1.0/(p[0]**2+(p[4]*p[0]/6.28+x-p[1])**2)
#            S11=p[5]
#            return p[2]*absolute(exp(1.0j*k*D)*S12q*(1+exp(2.0j*k*D1)*S11q*S11+exp(2.0j*k*D2)*S11q*S11+
#            exp(2.0j*k*D)*S11**2*S12q**2)+2.0j*w*Cc*50.0)**2+p[3]
#
#        def allbounces(x,p):
#            w=2*pi*x
#            k=2.0*pi*x/3488.0
#            Cc=0.0
#            D=500.0e-6
#            D1=300.0e-6
#            D2=200.0e-6
#
#            return p[2]*absolute(exp(1.0j*k*D)*S12q*(-2.0
#                +1.0/(1.0-exp(2.0j*k*D1)*S11q*S11)
#                +1.0/(1.0- exp(2.0j*k*D2)*S11q*S11)
#                +1.0/(1- exp(2.0j*k*D)*S11**2*S12q**2))
#                +2.0j*w*Cc*50.0)
#
#        def residuals(p,y,x):
#            err = y - lorentzian(x,p)
#            return err
#
#        def residuals2(p,y,x):
#            return y - fano(x,p)
#
#        def residuals3(p,y,x):
#            return y - refl_fano(x,p)
#
#        p = [200e6,4.5e9, 0.002, 0.022, 0.1, 0.1]
#
#        indices=[range(81, 120+1), range(137, 260+1), range(269, 320+1), range(411, 449+1)]#, [490]]#, [186]]
#        indices=[range(len(a.frequency))]
#        widths=[]
#        freqs=[]
#        freq_diffs=[]
#        fanof=[]
#        filt=[]
#        for n in range(len(yok)):
#            myifft=fft.ifft(mag[:,n])
#                #b.line_plot("ifft", absolute(myifft))
#            myifft[50:-50]=0.0
#                #myifft[:20]=0.0
#                #myifft[-20:]=0.0
#            filt.append(absolute(fft.fft(myifft))**2)
#        filt=array(filt).transpose()
#        for ind_list in indices:
#            for n in ind_list:
#                pbest = leastsq(residuals3, p, args=(a.MagAbs[n, :], c.flux_parabola[:]), full_output=1)
#                best_parameters = pbest[0]
#                print best_parameters
#                if 0:#n % 8==0:
#                    bb.scatter_plot("magabs_flux", c.flux_parabola[:]*1e-9, a.MagAbs[n, :], label="{}".format(n), linewidth=0.2, marker_size=0.8)
#                    bb.line_plot("lorentzian", c.flux_parabola*1e-9, refl_fano(c.flux_parabola,best_parameters), label="fit {}".format(n), linewidth=0.5)
#                if 1:#absolute(best_parameters[1]-a.frequency[n])<2e8:
#                    freqs.append(a.frequency[n])
#                    freq_diffs.append(absolute(best_parameters[1]-a.frequency[n]))
#                    widths.append(absolute(best_parameters[0]))
#                    fanof.append(absolute(best_parameters[4]))
#        if 1:
#            widths2=[]
#            freqs2=[]
#            freq_diffs2=[]
#            fano2=[]
#            flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=yok, offset=-0.037, flux_factor=0.2925)
#            Ej=qdt.call_func("Ej", flux_over_flux0=flux_over_flux0)
#            flux_par=qdt._get_fq(Ej, qdt.Ec)
#            magabs=absolute(mag)**2
#            for n in range(len(frq)):
#                pbest = leastsq(residuals2,p,args=(filt[n, :], flux_par[:]), full_output=1)
#                best_parameters = pbest[0]
#                print best_parameters
#                if 0:#n==539 or n==554:#n % 10:
#                    b.line_plot("magabs_flux", flux_par*1e-9, (magabs[n, :]-best_parameters[3])/best_parameters[2], label="{}".format(n), linewidth=0.2)
#                    b.line_plot("lorentzian", flux_par*1e-9, fano(flux_par,best_parameters), label="fit {}".format(n), linewidth=0.5)
#                if 1:#absolute(best_parameters[1]-frq[n])<1.5e8:
#                    freqs2.append(frq[n])
#                    freq_diffs2.append(absolute(best_parameters[1]-frq[n]))
#                    widths2.append(absolute(best_parameters[0]))
#                    fano2.append(absolute(best_parameters[4]))
#
#        b.line_plot("widths", freqs, widths, label="-110 dBm")
#        b.scatter_plot("widths2", freqs2, widths2, color="red", label="-130 dBm")
#        vf=3488.0
#        p=[1.0001, 0.5, 0.3, 1.0e-15, 0.001]
#        Np=9
#        K2=0.048
#        f0=5.348e9
#        def fourier(x, p):
#            w=2*pi*x
#            k=2.0*pi*x/3488.0
#            D=500.0e-6
#            D1=300.0e-6
#            D2=200.0e-6
#            G_f=0.5*Np*K2*f0*(sin(Np*pi*(x-f0)/f0)/(Np*pi*(x-f0)/f0))**2
#
#            return G_f*absolute(exp(1.0j*k*D)*p[0]*(1+exp(2.0j*k*D1)*(p[1]+1.0j*p[2])+exp(2.0j*k*D2)*(p[1]+1.0j*p[2]))
#            +2.0j*w*p[3]*50.0)+p[4]
#            #exp(2.0j*k*D)*(p[1]+1.0j*p[2]))+
#
#
#        def resid(p,y,x):
#            #return y - onebounce(x,p)
#            return y - fourier(x,p)
#        #pbest=leastsq(resid, p, args=(absolute(widths2[318:876]), frq[318:876]), full_output=1)
#        #print pbest[0]
#        #b.line_plot("fourier", frq, fourier(frq, pbest[0]))
#        #pi*vf/2*x=D
#        from scipy.signal import lombscargle
#        #lombscargle(freqs2[318:876], widths2[318:876])
#        #bb.line_plot("fft", #frq[318:876]*fft.fftfreq(len(frq[318:876]), d=frq[1]-frq[0]),
#        #absolute(fft.fft(widths2[318:876])))
#        frqdiffs=linspace(0.01, 500e6, 1000)
#        #bb.line_plot("ls", frqdiffs, lombscargle(array(freqs2[285:828]), array(widths2[285:828]), frqdiffs ))
#        #bb.line_plot("ls", frqdiffs, lombscargle(array(freqs[318:876]), array(widths[318:876]), frqdiffs))
#
#        bb.line_plot("fft2", absolute(fft.ifft(widths2[285:828])))
#        bb.line_plot("fft", absolute(fft.ifft(widths[285:828])))
#
#        bbb=Plotter()
#        #bbb.scatter_plot("wid", freqs2, widths2)
#        myifft=fft.ifft(widths2[285:828])
#        myifft[12:-12]=0.0
#        bbb.line_plot("ff", freqs2[285:828], absolute(fft.fft(myifft)))
#        #b.line_plot("ff", freqs2[285:828], absolute(fft.fft(myifft)))
#
#        #bb.line_plot("fft2", absolute(fft.fft(widths[52:155])))
#
#        #b.line_plot("fano", freqs, fano)
#        #b.line_plot("fano", freqs2, fano2)
#
#        #f0=5.37e9
#
#        #G_f=0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*sin(pi*(freq-f0)/f0)))**2
#        #b.scatter_plot("freq_test", freqs, freq_diffs)
#
#
#
#    #magabs_cs()
#    #magdB_colormesh()
#    #magabs_colormesh()
#    #magabs_cs_fit()
#    if 0:
#        from numpy import exp, pi, sqrt, sin, log10, log, argmax, array, cos
#        class Fitter2(Operative):
#            base_name="fitter"
#            vf=FloatRange(3000.0, 4000.0, 3488.0).tag(tracking=True)
#            tD=FloatRange(0.0, 2000.0, 500.0).tag(tracking=True)
#            ZS=FloatRange(10.0, 100.0, 44.38).tag(tracking=True)
#            epsinf=FloatRange(1.0, 10.0, 4.0).tag(tracking=True)
#            K2=FloatRange(0.01, 0.1, 0.02458).tag(tracking=True)
#            f0=FloatRange(4.0, 6.0, 5.25).tag(tracking=True)
#            Cc=FloatRange(0.00001, 100.0, 26.5).tag(tracking=True)
#            bg_off=FloatRange(-50.0, 0.0, -24.0).tag(tracking=True)
#            bg_slope=FloatRange(-10.0, 10.0, 0.0).tag(tracking=True)
#            apwr=Float(1.9)
#            avalue=FloatRange(0.0, 1.0, 0.0).tag(tracking=True)
#            Lk=FloatRange(0.00001, 100.0, 1.0).tag(tracking=True)
#
#            @tag_Property(plot=True, private=True)
#            def R(self):
#                 f=a.frequency
#                 w=2*pi*f
#                 #vf=self.vf
#                 #lbda=vf/f
#                 #att=(self.avalue*(f/1.0e9)**self.apwr)*1.0e6/vf*log(10.0)/20.0
#                 #k=2*pi/lbda+1.0j*att
#                 #tL=k*self.tD*1.0e-6
#                 #L=1/(qdt.Ct*(2*pi*c.flux_parabola)**2)
#                 #GL=1.0/ZL
#                 epsinf=self.epsinf*1.0e-10
#                 W=25.0e-6
#                 Dvv=self.K2/2.0
#                 f0=self.f0*1.0e9
#                 w0=2*pi*f0
#                 Np=9
#                 X=Np*pi*(f-f0)/f0
#                 Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#                 Ct=sqrt(2.0)*Np*W*epsinf
#                 #Cc=self.Cc*1.0e-15
#                 #VcdivV=self.VcdivV
#                 #L=1/(C*(wq**2.0))
#                 #Lk=self.Lk*Np*1e-9
#                 Ga=Ga0*(sin(X)/X)**2.0
#                 Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#                 lamb=1e9*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#                 return lamb
#
#                 flux_over_flux0=(a.yoko-c.offset)*c.flux_factor
#                 R=[]
#                 R2=[]
#                 print Ct
#                 #return Ba/w
#                 for fof0 in flux_over_flux0:
#                     Ej=qdt.Ejmax*absolute(cos(pi*fof0))
#                     Ec=e**2/(2.0*Ct)
#                     E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
#                     E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)#+lamb*h
#                     fq=(E1-E0)/h
#                     L=1/(qdt.Ct*(2*pi*fq)**2)
#                     R.append(absolute(Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*L)))**2)# for l in L]#+1.0j*(VcdivV)*w*Cc)
#                     fqq=fq-Ec/2.0/h#-lamb
#                     L=1/(qdt.Ct*(2*pi*fqq)**2)
#                     R2.append(absolute(Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*L)))**2)# for l in L]#+1.0j*(VcdivV)*w*Cc)
#
#                 return R, R2
#
#                 #Npq=9
#                 #f0q=5.45e9
#                 #def coup(fq):
#                 #    X=Npq*pi*(f-f0q)/f0q
#                 #    return 1.0e9*(sin(X)/X)**2
#                 #return [1.0/(1.0+((f-fc)/coup(fc))**2) for fc in c.flux_parabola] #1.0j*w*Ct+1.0/(1.0j*w*l)))**2 for l in L]
#
#                 #return [1.0/(1.0+((f*Ba/+f-fc)/coup(fc))**2) for fc in c.flux_parabola] #1.0j*w*Ct+1.0/(1.0j*w*l)))**2 for l in L]
#
#                 #return [absolute(Ga/(Ga+1.0j*w*Ct+1.0/(1.0j*w*l)))**2 for l in L]
#                 #return [absolute(Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*l)))**2 for l in L]#+1.0j*(VcdivV)*w*Cc)
#                 #return [c.flux_parabola[argmax(absolute(Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*l))), axis=0)] for l in L]#+1.0j*(VcdivV)*w*Cc)
#    #d=Fitter2()
#
#    #b.scatter_plot("fluxtry", a.frequency, c.flux_parabola[argmax(array(d.R).transpose(), axis=1)])
#    #b.colormesh("fluxtry", a.yoko, a.frequency, array(d.R[0]).transpose()+array(d.R[1]).transpose())
#    #b.colormesh("fluxtry2", a.yoko, a.frequency, array(d.R[1]).transpose())
#
#    #b.line_plot("fluxtry",  a.frequency+1.05e9, a.frequency)#.transpose())
#    #b.line_plot("fluxtry",  a.frequency, d.R[1])#.transpose())
#
#    if 0:
#        from numpy import exp, pi, sqrt, sin, log10, log
#
#        b.line_plot("off res", a.frequency, 10.0*log10(absolute(a.Magcom[:, 300])), linewidth=0.5)
#
#        f=linspace(4.0e9, 5.0e9, 5000)
#
#        class Fitter2(Operative):
#            base_name="fitter"
#            vf=FloatRange(3000.0, 4000.0, 3488.0).tag(tracking=True)
#            tD=FloatRange(0.0, 2000.0, 500.0).tag(tracking=True)
#            ZS=FloatRange(10.0, 100.0, 44.38).tag(tracking=True)
#            epsinf=FloatRange(1.0, 10.0, 2.989).tag(tracking=True)
#            K2=FloatRange(0.01, 0.1, 0.02458).tag(tracking=True)
#            f0=FloatRange(4.0, 5.0, 4.447).tag(tracking=True)
#            Cc=FloatRange(0.00001, 100.0, 26.5).tag(tracking=True)
#            bg_off=FloatRange(-50.0, 0.0, -24.0).tag(tracking=True)
#            bg_slope=FloatRange(-10.0, 10.0, 0.0).tag(tracking=True)
#            apwr=Float(1.9)
#            avalue=FloatRange(0.0, 1.0, 0.0).tag(tracking=True)
#            Lk=FloatRange(0.00001, 100.0, 1.0).tag(tracking=True)
#
#            @tag_Property(plot=True, private=True)
#            def R(self):
#
#                 w=2*pi*f
#                 vf=self.vf
#                 lbda=vf/f
#                 att=(self.avalue*(f/1.0e9)**self.apwr)*1.0e6/vf*log(10.0)/20.0
#                 k=2*pi/lbda+1.0j*att
#                 tL=k*self.tD*1.0e-6
#                 ZL=self.ZS
#                 GL=1.0/ZL
#                 epsinf=self.epsinf*1.0e-10
#                 W=25.0e-6
#                 Dvv=self.K2/2.0
#                 f0=self.f0*1.0e9
#                 w0=2*pi*f0
#                 Np=36
#                 X=Np*pi*(f-f0)/f0
#                 Ga0=3.11*w0*epsinf*W*Dvv*Np**2
#                 Ct=sqrt(2.0)*Np*W*epsinf
#                 Cc=self.Cc*1.0e-15
#                 #VcdivV=self.VcdivV
#                 #L=1/(C*(wq**2.0))
#                 Lk=self.Lk*Np*1e-9
#                 Ga=Ga0*(sin(X)/X)**2.0
#                 Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
#
#                 Y=Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*Lk)
#                 Y1=Y
#                 Y2=Y[:]
#                 Y3=1.0j*w*Cc
#                 S33Full=(Y2+1/ZL-ZL*(Y1*Y3+Y2*Y3+Y1*Y2)-Y1)/(2*Y3+Y2+1.0/ZL+ZL*(Y1*Y3+Y2*Y3+Y1*Y2)+Y1)
#
#                 S11=Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/ZL+1.0/(1.0j*w*Lk))#+1.0j*(VcdivV)*w*Cc)
#                 S33= S33Full#(1/ZL-Y)/(1/ZL+Y)
#                 S13=1.0j*sqrt(2*Ga*GL)/(Ga+1.0j*Ba+ 1.0j*w*Ct+1.0/ZL+1.0/(1.0j*w*Lk))#+1.0j*(VcdivV)*w*Cc)
#
#                 S11q=Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/ZL+1.0/(1.0j*w*Lk))#+1.0j*(VcdivV)*w*Cc)
#                 S13q=1.0j*sqrt(2*Ga*GL)/(Ga+1.0j*Ba+ 1.0j*w*Ct+1.0/ZL+1.0/(1.0j*w*Lk))
#
#                 #S21C=2.0/(2.0+1.0/(1.0j*w*Cc*ZL))
#                 S21C=2.0*Y3/(2.0*Y3+Y2+Y1+1/ZL+ZL*(Y1*Y3+Y2*Y3+Y1*Y2))
#                 crosstalk=S21C*S13q*S13/(exp(-1.0j*tL)-S11*exp(1.0j*tL)*S11q)
#
#                 return S33 + S13**2/(exp(-2.0j*tL)/S11q-S11)+crosstalk
#
#            plotter=Typed(Plotter).tag(private=True)
#
#            @observe("vf", "tD", "ZS", "epsinf", "K2", "f0", "Cc", "apwr", "avalue", "bg_off", "Lk", "bg_slope")
#            def update_plot(self, change):
#                if change["type"]=="update":
#                     self.get_member("R").reset(self)
#                     self.plotter.plot_dict["R_theory"].clt.set_ydata(20.0*log10(absolute(self.R))+self.bg_off+self.bg_slope*f*1e-9)
#                     self.plotter.draw()
#
#        d=Fitter2()
#        #b.line_plot("R_theory", f, 20.0*log10(absolute(d.R))+d.bg_off, linewidth=0.5)
#        #d.plotter=b
#
#    shower(b1)
#

