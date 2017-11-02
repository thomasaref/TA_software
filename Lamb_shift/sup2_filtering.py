# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 13:01:25 2017

@author: thomasaref
"""

from numpy import log10, absolute, mean, linspace, array, sqrt, diag, pi
from TA88_fundamental import TA88_VNA_Lyzer, TA88_Read, qdt as qdt88, idt as idt88, TA88_Read_NP, TA88_Save_NP, bg_A4, bg_A1
from D0527_trans_careful import a as d0527
from D0527_trans_careful import MagcomFilt as MagcomFilt88
from taref.plotter.api import colormesh, line, scatter
from D0317_S4A1_frq_pulse_flux import a as d0317
from matplotlib.pyplot import colorbar#, tight_layout

fig_width=7.2
fig_height=5.0

c=TA88_VNA_Lyzer(name="S4A1_midpeak",
             desc="S4A1 Main peak",
                   on_res_ind=260,
              #VNA_name='RS VNA', port_name='S21',
              rd_hdf=TA88_Read(main_file="Data_0316/S4A1_TA88_coupling_search_midpeak.hdf5"),
              fit_indices=[range(65, 984+1)],
              flux_factor=qdt88.flux_factor*1000.0/560.0,
              offset=-0.045
              )
c.filt.center=31
c.filt.halfwidth=22
c.fitter.fit_type="lorentzian"
c.fitter.gamma=0.055 #0.01
c.flux_axis_type="flux" #"fq" #"flux"
c.end_skip=10

c.save_folder.main_dir="sup2_filtering"



if __name__=="__main__":
    nskip=50

    d0527.filter_type="None"
    d0527.read_data()
    d0317.read_data()

    magfilt88=MagcomFilt88(d0527)
    magabs88=absolute(magfilt88)

    plbg="fig2_sup"
    plbg=line(d0527.frequency/1e9, 20*log10(absolute(d0527.MagcomData[:, 0]))-bg_A4(d0527.frequency),
            color="green", alpha=1.0, linewidth=0.5,
            nrows=2, ncols=3, nplot=1, pl=plbg, fig_width=fig_width, fig_height=fig_height)#.show()


    plbg.nplot=2
    line(d0527.frequency/1e9, 20*log10(absolute(d0527.MagcomData[:, 0]))-bg_A4(d0527.frequency),
            color="green", pl=plbg)#.show()
            
            
    plbg.nplot=1
    line(d0527.frequency[::nskip]/1e9, 20.0*log10(magabs88[::nskip])-bg_A4(d0527.frequency[::nskip]),
               color="blue",
               #facecolor="red", edgecolor="red",
               pl=plbg)
    plbg.nplot=2
    line(d0527.frequency[::nskip]/1e9, 20.0*log10(magabs88[::nskip])-bg_A4(d0527.frequency[::nskip]),
               color="blue",
               auto_ylim=False, y_min=-40, y_max=0,
               auto_xlim=False, x_min=4.2, x_max=4.7, xlabel="Frequency (GHz)",
               ylabel="Transmission (dB)",
               #facecolor="red", edgecolor="red",
               pl=plbg)

    plbg.nplot=1
    (S11, S12, S13,
     S21, S22, S23,
     S31, S32, S33)=idt88._get_simple_S(f=d0527.frequency)
    S13xS31=S13*S31
     
    
    line(d0527.frequency/1e9, 20*log10(absolute(S13xS31))-4, color="red", pl=plbg,
               auto_ylim=False, y_min=-80, y_max=0,
               auto_xlim=False, x_min=3.85, x_max=5.5, xlabel="Frequency (GHz) ",
             ylabel="Transmission (dB) ",)

    cdata=10.0**((20.0*log10(mean(absolute(d0317.MagcomData[64:76, :, :]), axis=0))-d0317.probe_pwr)/20.0)
    cdata2=(20*log10(cdata).transpose()+10-1.0-bg_A1(d0317.frequency)).transpose()
    #cdata=(20*log10(absolute(d0317.MagcomData[64:76, :, :])-bg_A1(c.frequency)).transpose()
    #    flux_axis=c.flux_axis[c.flat_flux_indices]
    #    freq_axis=c.freq_axis[c.indices]
    plbg.nplot=6
    plbg, pfbg=colormesh(d0317.flux_axis/pi, d0317.freq_axis,
                     10**(cdata2/20.0), pl=plbg,
                         pf_too=True, auto_zlim=False,
                                   auto_xlim=False, x_min=0.65/3.14, x_max=1.5/3.14,
                                   auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12*2)

    cbr=colorbar(pfbg.clt, ax=plbg.axes)
    cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
    cbr.set_ticks(linspace(0.0, 0.12*2, 2))
    plbg.axes.set_xticks(linspace(0.25, 0.45, 3))
    plbg.axes.set_yticks(linspace(4.35, 4.55, 5))
    plbg.axes.set_ylabel("Frequency (GHz)")
    plbg.axes.set_xlabel("$\Phi/\Phi_0$")
    
    print idt88.Np, idt88.K2
    print idt88.f0
    print d0527.comment
    print -d0527.fridge_atten+d0527.fridge_gain-d0527.rt_atten+d0527.rt_gain-10
    
    def ifft_plot(self, plbg, **kwargs):
        #process_kwargs(self, kwargs, pl="hannifft_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
        on_res=10*log10(absolute(self.filt.window_ifft(self.MagcomData[:,0])))

        line(self.time_axis-0.05863, self.filt.fftshift(on_res),  color="purple",
               plot_name="onres_{}".format(self.on_res_ind), alpha=0.8, label="IFFT", pl=plbg, **kwargs)

        self.filt.N=len(on_res)
        filt=self.filt.freqz
        #filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
        top=36.0#amax(on_res)
        if 1:
            line(self.time_axis-0.05863, filt*top-70, plotter=plbg, color="green",
                 linestyle="solid", label="Filter window",
                 auto_xlim=False, x_min=-0.2, x_max=1.0,
                 auto_ylim=False, y_min=-65, y_max=-15,)
        plbg.xlabel=kwargs.pop("xlabel", "Time ($\mu \mathrm{s}$)")
        plbg.ylabel=kwargs.pop("ylabel", "IFFT (dB)")

        IFFT_trans_t=array([0.05863,   0.2,  0.337,   0.48,  0.761, 1.395, 1.455])-0.05863
        IFFT_trans_d=array([0.0, 500.0, 1000.0, 1500.0, 2500.0, 4500,  200+2500+2500-300])/1000.0

        pulse_t=(array([8.7e-8, 2.64e-7, 3.79e-7, 4.35e-7, 6.6e-7])-8.7e-8)*1e6
        pulse_d=array([0.0, 600.0, 1000.0, 1200.0, 2000.0])/1000.0


        from scipy.optimize import curve_fit, leastsq

        t=list(IFFT_trans_t)
        t.extend(pulse_t)
        d=list(IFFT_trans_d)
        d.extend(pulse_d)

        def fit_func(x, a, b):
            return a*x + b

        params, pcov = curve_fit(fit_func, t, d)

        print params, pcov
        perr = sqrt(diag(pcov))
        print "std", perr
        def residuals(p, y, x):
            """residuals of fitting function"""
            return y-p[0]*x+p[1]
        p_guess=[3.488, 0.0]
        pbest= leastsq(residuals, p_guess, args=(array(d), array(t)), full_output=1)
        print pbest
        #raise Exception
        #[a, b] = params[0]
        #pl.axes.plot(IFFT_trans_t, IFFT_trans_d, "bo", markersize=3,)#, pl=pl)
        #pl.axes.plot(pulse_t, pulse_d, "x", c="red", markersize=3)#, pl=pl)                
        t=linspace(0,2,1001) #self.time_axis-0.05863

        #line(t, 3488.0*t/1000.0, pl=pl, color="black", linestyle="dashed", linewidth=1.0)
        #pl.axes.set_ylim(-0.2, 3.0)
        #pl.axes.set_xlim(-0.2, 1.0)
        #pl.axes.set_xticks(linspace(0.0, 1.0, 3))
        #pl.axes.set_yticks(linspace(0.0, 3.0, 4))

        ax2 = plbg.axes.twinx()
        ax2.plot(array([0.05863,   0.2,  0.337,   0.48,  0.761, 1.395, 1.455])-0.05863,
                array([0.0, 500.0, 1000.0, 1500.0, 2500.0, 4500,  200+2500+2500-300])/1000.0, ".",
                label="IFFT peak")#, marker_size=4.0)
        t=linspace(0,2,1001) #self.time_axis-0.05863
        ax2.plot(t, 3488.0*t/1000.0, color="black", linestyle="dashed",  label="$d=v_ft$")

        t=array([8.7e-8, 2.64e-7, 3.79e-7, 4.35e-7, 6.6e-7])-8.7e-8
        ax2.plot(t*1e6, array([0.0, 600.0, 1000.0, 1200.0, 2000.0])/1000.0, "x", color="red",
                #facecolor="red", edgecolor="red",
                 label="100 ns pulse",
                #marker_size=4.0,
                 )
        ax2.set_ylabel('Distance (mm)')
        ax2.set_ylim(-0.2, 3.0)
        ax2.set_xlim(-0.2, 1.0)
        #pl.legend()
        #b.line_plot("spd_fit", t*1e6,  (t*qdt.vf)*1e6, label="(3488 m/s)t")

        return plbg
    #pl.nplot=2
    plbg.nplot=3
    d0527.time_axis_type="time"
    ifft_plot(d0527, plbg)
    
    if 1:
        c.read_data()
        plbg.nplot=4
        c.filter_type="None"

        cdata=(20*log10(c.MagAbs).transpose()-bg_A1(c.frequency)).transpose()
        flux_axis=c.flux_axis[c.flat_flux_indices]
        freq_axis=c.freq_axis[c.indices]
        plbg, pfbg=colormesh(flux_axis, freq_axis, 10**(cdata[:, :]/20.0), pl=plbg,
                         pf_too=True, auto_zlim=False,
                                   auto_xlim=False, x_min=0.65/3.14, x_max=1.5/3.14,
                                   auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12)
        #pl, pf=c.magabs_colormesh(pl=pl, pf_too=True, auto_zlim=False,
        #                           auto_xlim=False, x_min=0.65, x_max=1.5,
        #                           auto_ylim=True, vmin=0.0, vmax=0.02)
        cbr=colorbar(pfbg.clt, ax=plbg.axes)
        cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
        cbr.set_ticks(linspace(0.0, 0.12, 2))
        plbg.axes.set_xticks(linspace(0.25, 0.45, 3))
        plbg.axes.set_yticks(linspace(4.35, 4.55, 5))
        plbg.axes.set_ylabel("Frequency (GHz)")
        plbg.axes.set_xlabel("$\Phi/\Phi_0$")
  
       
        c.filter_type="FFT"
        print c.MagcomFilt.shape
        print c.frequency.shape
        cdata=(20*log10(absolute(c.MagcomFilt)).transpose()-bg_A1(c.frequency)).transpose()
        flux_axis=c.flux_axis[c.flat_flux_indices]
        freq_axis=c.freq_axis[c.indices]
        
        

        plbg.nplot=5
        plbg, pfbg=colormesh(flux_axis, freq_axis, 10**(cdata[c.end_skip:-c.end_skip, :]/20.0), 
                             pl=plbg,
                         pf_too=True, auto_zlim=False,
                                   auto_xlim=False, x_min=0.65/3.14, x_max=1.5/3.14,
                                   auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12)

        #pl, pf=c.magabs_colormesh(pl=pl, pf_too=True, auto_zlim=False,
        #                           auto_xlim=False, x_min=0.65, x_max=1.5,
        #                           auto_ylim=True, vmin=0.0, vmax=0.02)
        cbr=colorbar(pfbg.clt, ax=plbg.axes)
        cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
        cbr.set_ticks(linspace(0.0, 0.12, 2))
        plbg.axes.set_xticks(linspace(0.25, 0.45, 3))
        plbg.axes.set_yticks(linspace(4.35, 4.55, 5))
        plbg.axes.set_ylabel("Frequency (GHz)")
        plbg.axes.set_xlabel("$\Phi/\Phi_0$")


    plbg.figure.tight_layout()

    c.save_plots([plbg])#, pl1])

    plbg.show()

             
               
               
    