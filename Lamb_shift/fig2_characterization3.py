# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""



from TA88_fundamental import TA88_VNA_Lyzer, TA88_Read, qdt as qdt88, idt as idt88, TA88_Read_NP, TA88_Save_NP, bg_A4, bg_A1
from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, idt, qdt
from numpy import diag, mean, log10, array, absolute, squeeze, append, sqrt, pi, arccos, shape, linspace, argmin
from taref.physics.fundamentals import h
from taref.plotter.api import colormesh, line, scatter
from taref.physics.filtering import Filter
from D0527_trans_careful import a as d0527
from D1122_trans_direct import a as d1122
from D1122_trans_direct import MagcomFilt
from D0527_trans_careful import MagcomFilt as MagcomFilt88

from D0317_S4A1_frq_pulse_flux import a as d0317
from taref.core.api import process_kwargs
from matplotlib.pyplot import colorbar#, tight_layout

idt.Np=56
idt.f0=4.46e9 #4.452
idt.K2=0.032

a=TA88_VNA_Lyzer(on_res_ind=201, rd_hdf=TA88_Read(main_file="Data_0628/S4A4_just_gate_overnight_flux_swp.hdf5"))

a.filt.center=0
a.filt.halfwidth=200
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.01
a.flux_axis_type="flux" #"yoko"#"flux"
a.end_skip=10
a.fit_indices=[range(2, 14), range(15, 17), range(19,23), range(24, 26), range(29, 37), range(38, 39), range(44, 46), range(48, 52),
               range(54, 66), range(67, 69), range(70, 85), range(105, 107), range(108, 116), range(122, 129), [130], range(132, 134), [138],
 range(182,184), range(188, 193), range(217, 251+1), range(266, 275+1), range(314, 324+1)]
#a.flux_indices=[range(400,434), range(436, 610)]
#a.flux_indices=[range(200, 400)]
a.filter_type="FFT"

a.bgsub_type="dB" #"Complex" #"Abs"
a.save_folder.main_dir="fig2_characterization3"

b=TA53_VNA_Pwr_Lyzer(name="d1112", on_res_ind=635,
        rd_hdf=TA53_Read(main_file="Data_1112/S3A4_trans_pwr_swp.hdf5"),
         desc="transmission power sweep", offset=-0.15, swp_type="yoko_first",
        )
b.filt.center=0 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
b.filt.halfwidth=12 #8 #10
b.flux_axis_type="flux" #"fq" #
#b.bgsub_type="Complex" #"Abs" #"dB"
b.end_skip=10
b.pwr_ind=22

c=TA88_VNA_Lyzer(name="S4A1_midpeak",
             desc="S4A1 Main peak",
                   on_res_ind=260,
              #VNA_name='RS VNA', port_name='S21',
              rd_hdf=TA88_Read(main_file="Data_0316/S4A1_TA88_coupling_search_midpeak.hdf5"),
              fit_indices=[range(65, 984+1)],
              flux_factor=a.qdt.flux_factor*1000.0/560.0,
              offset=-0.045
              )
c.filt.center=31
c.filt.halfwidth=22
c.fitter.fit_type="lorentzian"
c.fitter.gamma=0.055 #0.01
c.flux_axis_type="flux" #"fq" #"flux"
c.end_skip=10


d=TA88_VNA_Lyzer(name="S4A1_wide",
             desc="S4A1 wide",
                   on_res_ind=260,
              VNA_name='RS VNA', port_name='S21',
              rd_hdf=TA88_Read(main_file="Data_0312/S4A1_TA88_coupling_search.hdf5"),
              #fit_indices=[range(65, 984+1)],
              #fit_func=lorentzian,
              flux_factor=qdt.flux_factor*1000.0/560.0,
              offset=-0.045
              )#, fit_type="yoko")
d.filt.center=129
d.filt.halfwidth=30
d.fitter.fit_type="lorentzian"
d.fitter.gamma=0.055 #0.01
d.flux_axis_type="flux" #"fq" #"flux"
d.end_skip=10
d.filter_type="FFT"

d1118=TA53_VNA_Pwr_Lyzer(name="d1118", on_res_ind=301,
        rd_hdf=TA53_Read(main_file="Data_1118/S3A4_trans_swp_n5n15dBm.hdf5"),
        fit_indices=[ #range(7, 42), range(79, 120), range(171, 209), range(238, 296),
                     range(316, 358),range(391, 518), range(558, 603),
                    # range(629, 681), range(715, 771), range(790, 845),
                    # range(872, 921), range(953, 960), range(963, 985)
                     ],
         desc="transmission power sweep",
         offset=-0.07,
         swp_type="yoko_first",
        )
d1118.filt.center=0 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
d1118.filt.halfwidth=100 #8 #10
d1118.fitter.gamma=0.3/10 #0.035
d1118.flux_axis_type="flux"#"fq" #
d1118.end_skip=10
d1118.pwr_ind=1

fig_width=7.2
fig_height=5.0



if __name__=="__main__":
    pl="fig2"
    pl88="fig2_TA88"

    d0527.filter_type="None"
    d0527.read_data()
    plbg="fig2_sup"
    plbg=line(d0527.frequency/1e9, 20*log10(absolute(d0527.MagcomData[:, 0]))-bg_A4(d0527.frequency),
            color="green", alpha=1.0, linewidth=0.5,
            nrows=2, ncols=3, nplot=1, pl=plbg, fig_width=fig_width, fig_height=fig_height)#.show()


    plbg.nplot=2
    line(d0527.frequency/1e9, 20*log10(absolute(d0527.MagcomData[:, 0]))-bg_A4(d0527.frequency),
            color="green", pl=plbg)#.show()

    #pl=line(a.frequency, 10*log10(absolute(a.MagcomData[:, 1])))#.show()

    #pl=line(a.frequency, a.MagdB)#.show()

    magfilt88=MagcomFilt88(d0527)
    magabs88=absolute(magfilt88)
    line(d0527.frequency/1e9, magabs88)
    nskip=50
    pl88=scatter(d0527.frequency[::nskip]/1e9, 20.0*log10(magabs88[::nskip])-bg_A4(d0527.frequency[::nskip]),
               facecolor="blue", edgecolor="blue", pl=pl88, nrows=2, ncols=3, nplot=1,
               fig_width=fig_width, fig_height=fig_height, marker_size=10)

    magfilt=MagcomFilt(d1122)
    magabs=absolute(magfilt)

    pl=scatter(d1122.frequency[::nskip]/1e9, 20.0*log10(magabs[::nskip])-bg_A4(d1122.frequency[::nskip]),
               facecolor="blue", edgecolor="blue", pl=pl, nrows=2, ncols=3, nplot=1,
               fig_width=fig_width, fig_height=fig_height, marker_size=10)
    
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
    #idt.Np=56
    #idt.f0=4.46e9 #4.452
    #idt.K2=0.032
    #idt.Np=36.5
    #idt.f0=4.452e9



    (S11, S12, S13,
     S21, S22, S23,
     S31, S32, S33)=idt88._get_simple_S(f=d0527.frequency)
    S13xS31=S13*S31
    print idt.Np, idt.K2
    print idt.f0
    print d0527.comment
    print -d0527.fridge_atten+d0527.fridge_gain-d0527.rt_atten+d0527.rt_gain-10

    line(d0527.frequency/1e9, 20*log10(absolute(S13xS31))-4, color="red", pl=pl88,
         auto_ylim=False, y_min=-40, y_max=0,
         auto_xlim=False, x_min=4.2, x_max=4.7, xlabel="Frequency (GHz)",
         ylabel="Transmission (dB)", linewidth=1.0,
        )#.show()


    pl88.axes.set_xticks(linspace(4.2, 4.7, 3))
    pl88.axes.set_yticks(linspace(-40, 0, 5))

    (S11, S12, S13,
     S21, S22, S23,
     S31, S32, S33)=idt._get_simple_S(f=d1122.frequency)
    
    line(d1122.frequency/1e9, 20*log10(absolute(S13*S31))-4-5, color="red", pl=pl,
         auto_ylim=False, y_min=-60, y_max=-10,
         auto_xlim=False, x_min=4.1, x_max=4.8, xlabel="Frequency (GHz)",
         ylabel="$|S_{21}|$ (dB)", linewidth=1.0,
        )#.show()
    pl.axes.set_xticks(linspace(4.2, 4.7, 3))
    pl.axes.set_yticks(linspace(-60, -10, 6))
   
    plbg.nplot=1
    line(d0527.frequency/1e9, 20*log10(absolute(S13xS31))-4, color="red", pl=plbg,
               auto_ylim=False, y_min=-80, y_max=0,
               auto_xlim=False, x_min=3.85, x_max=5.5, xlabel="Frequency (GHz) ",
             ylabel="Transmission (dB) ",)

    #line(a.frequency, angle(magfilt))


    #ifft_plot(a)#.show()

    d0317.read_data()
    cdata=10.0**((20.0*log10(mean(absolute(d0317.MagcomData[64:76, :, 0]), axis=0))-d0317.probe_pwr)/20.0)

    pl88.axes.plot(d0317.frequency/1e9, 
               20*log10(cdata)+10-1.0-bg_A1(d0317.frequency), "x", 10,
             color="green")

    cdata=10.0**((20.0*log10(mean(absolute(d0317.MagcomData[64:76, :, :]), axis=0))-d0317.probe_pwr)/20.0)
    cdata2=(20*log10(cdata).transpose()+10-1.0-bg_A1(d0317.frequency)).transpose()
    #cdata=(20*log10(absolute(d0317.MagcomData[64:76, :, :])-bg_A1(c.frequency)).transpose()
    #    flux_axis=c.flux_axis[c.flat_flux_indices]
    #    freq_axis=c.freq_axis[c.indices]
    plbg.nplot=6
    plbg, pfbg=colormesh(d0317.flux_axis, d0317.freq_axis,
                     10**(cdata2/20.0), pl=plbg,
                         pf_too=True, auto_zlim=False,
                                   auto_xlim=False, x_min=0.65, x_max=1.5,
                                   auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12)

    cbr=colorbar(pfbg.clt, ax=plbg.axes)
    cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
    cbr.set_ticks(linspace(0.0, 0.12, 2))
    plbg.axes.set_xticks(linspace(0.7, 1.5, 3))
    plbg.axes.set_yticks(linspace(4.35, 4.55, 5))
    plbg.axes.set_ylabel("Frequency (GHz)")
    plbg.axes.set_xlabel("$\Phi/\Phi_0$")

    #scatter(d0317.frequency/1e9, 
    #           20*log10(cdata)+10-1.0-bg_A1(d0317.frequency),
    #        pl=plbg, color="purple", marker="x")

    #a.save_plots([pl,])
    #pl.show()

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

    #a.read_data()
    b.read_data()

    #pl, pf=a.magabs_colormesh(vmin=0.995, vmax=1.002, auto_zlim=False, cmap="afmhot",
    #                          auto_ylim=False, y_min=3.5, y_max=7.5,
    #                          auto_xlim=False, x_min=-3, x_max=3,
    #                      nrows=2, ncols=2, nplot=1, pl=pl, pf_too=True,
    #                      fig_width=5.0, fig_height=4.0,
    #                      )#.show()
    #line(a.flux_axis, a.qdt._get_flux_parabola(voltage=a.yoko, ng=0.0)/1e9, pl=pl)#.show()

    #pl.axes.yaxis.labelpad=-5
    #pl.axes.xaxis.labelpad=-5

    #pl.ncols=2
    #cbr=colorbar(pf.clt, ax=pl.axes, label="$S_{33}$")
    #print dir(cbr)
    #cbr.set_label("$|S_{11}|$", size=8, labelpad=-10)
    #cbr.set_ticks(linspace(0.995, 1.002, 2))
    #pl.axes.set_xticks(linspace(-3, 3, 4))
    #pl.axes.set_yticks(linspace(3.5, 7.5, 5))
    #pl.figure.text(0.0, 0.95, "a)")
    #pl.figure.text(0.53, 0.95, "b)")
    #pl.figure.text(0.0, 0.45, "c)")
    #pl.figure.text(0.53, 0.45, "d)")

    #cbr.set_ticklabels()
    #tight_layout()

    #raise Exception
    #pl.ylabel="Frequency (GHz)"
    #pl.xlabel="$\Phi/\Phi_0$"
    #colormesh(a.flux_axis, a.freq_axis)
    #pl="colormeshy"
    #colormesh(a.flux_axis, a.frequency[a.end_skip:-a.end_skip]/1e9, a.MagAbs[:, :], vmin=0.995, vmax=1.002, auto_zlim=False, cmap="afmhot", auto_ylim=False, y_min=3.6, y_max=7.4, pl=pl).show()
    #for inds in a.fit_indices:
    #    pl=colormesh(a.flux_axis, a.frequency[inds]/1e9, a.MagAbs[inds, :], cmap="afmhot",
    #                 vmin=0.995, vmax=1.002, auto_zlim=False,
    #                 pl=pl)
    #pl.show()

    b.filter_type="None"
    pl_raw=b.magabs_colormesh()
    pl_ifft=b.ifft_plot()#.show()

    b.filter_type="FFT"
    pl_fft=b.magabs_colormesh()#.show()
    pl_pwr_frq=colormesh(b.pwr, b.freq_axis[b.end_skip:-b.end_skip], absolute(b.MagcomFilt[b.end_skip:-b.end_skip, 635, :]),
                  ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    pl_pwr_color=colormesh(b.flux_axis, b.pwr, absolute(b.MagcomFilt[69, :, :]).transpose(),
                  ylabel="Power (dBm)", xlabel=b.flux_axis_label, #pl=pl,
                  auto_ylim=False, y_min=-30, y_max=10,
                  auto_xlim=False, x_min=1.0, x_max=2.5,
                  auto_zlim=True)


    #pl.nplot=6
    print b.comment
#    pl_pwr_sat=scatter(b.pwr-30-60, 100*absolute(absolute(b.MagcomFilt[69, 635, :])-absolute(b.MagcomFilt[69,0, :])),
#                xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}| \times 100$", pl=pl,
#                  auto_ylim=False, y_min=100*0.0, y_max=100*0.015, marker_size=3.0,
#                  auto_xlim=False, x_min=-30-90, x_max=10-90)#.show()

    from TA88_fundamental import bg_A1, bg_A4

    onres=(20*log10(absolute(b.MagcomFilt[69, :, :])).transpose()-bg_A4(b.freq_axis[69]*1e9)).transpose()

    pl.nplot=4
    pl3=colormesh(b.flux_axis, b.pwr-30-60, 10**(onres/20.0).transpose(), pl=pl,
                  ylabel="Power (dBm) ", xlabel=r"$\Phi/\Phi_0$ ",
                  auto_xlim=False, x_min=0.35, x_max=0.5, 
                  auto_ylim=False, y_min=-30-90, y_max=10-90)

    ax=pl.axes
    ax.set_yticks(linspace(-30.0-90, 10.0-90, 3))
    ax.set_xticks(linspace(0.38, 0.48, 3))
    
    #b.pwr, b.freq_axis[a.end_skip:-b.end_skip], 10**(onres/20.0), #absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 635, :]),
    #              ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()

    pl.nplot=5
    qdt.N_dim=8*2
    phi_mult=1
    qdt.phi_arr=linspace(0.35, 0.5, 101*phi_mult)*pi
    qdt.do_ls=False
    #a.harm_osc=True
    qdt.atten=110 #83+20
    print qdt.Ec
    #a.Ec = 0.22e9/1*h # Charging energy.
    #a.Ejmax = 1*22.2e9*h # Maximum Josephson energy.
    print qdt.gamma
    #a.gamma = 38.2059e6 # Acoustic relaxation rate of the transmon.
    qdt.gamma_el=qdt.gamma #0.750e6 #electric relaxation rate
    qdt.gamma_phi = 0.00e6 # Dephasing rate of the transmon.
    print qdt.fd, qdt.Zc
    #a.fd = 4.5066e9#/1e6 # Drive frequency.
    #a.Ct=150e-15/3
    #a.Cc=2e-15
    #a.Zc=50.0
    qdt.acoustic_plot=True #False
    #pwr=-100.0
    #Omega=a.Omega_arr[0]
    #fd=4.5e9 #a.frq_arr[15]

    #def find_expect(vg, self=a, fd=fd, pwr=pwr):
    #    return self.find_expect(vg=vg, fd=fd, pwr=pwr)
    #qdt.funcer=find_expect
    do_simul=True
    if do_simul:
        colormesh(qdt.phi_arr/pi, qdt.pwr_arr-90, 0.11*(1-absolute(qdt.fexpt2)), cmap="RdBu_r", pl=pl,
                  ylabel="Power (dBm)", xlabel=r"$\Phi/\Phi_0$",
                  auto_xlim=False, x_min=0.35, x_max=0.5, 
                  auto_ylim=False, y_min=-30-90, y_max=10-90)
    else:
        pl3=colormesh(b.flux_axis, b.pwr-30-60, 10**(onres/20.0).transpose(), pl=pl,
                  ylabel="Power (dBm)", xlabel=r"$\Phi/\Phi_0$",
                  auto_xlim=False, x_min=0.35, x_max=0.5, 
                  auto_ylim=False, y_min=-30-90, y_max=10-90)

    ax=pl.axes
    ax.set_yticks(linspace(-30.0-90, 10.0-90, 3))
    ax.set_xticks(linspace(0.38, 0.48, 3))
                  
    pl.nplot=6
    onres=20*log10(absolute(b.MagcomFilt[69, 635, :]))-bg_A4(b.frequency[69])
    offres=20*log10(absolute(b.MagcomFilt[69, 0, :]))-bg_A4(b.frequency[69])
    scatter(b.pwr-30-60, absolute(onres-offres))
    #scatter(b.pwr-30-60, 10**(absolute(onres-offres)/20.0))
    scatter(b.pwr-30-60, absolute(10**(onres/20.0)-10**(offres/20.0)))
    #scatter(b.pwr-30-60, absolute(10**(onres/20.0)))


    pl_pwr_sat=scatter(b.pwr-30-60, absolute(10**(onres/20.0)-10**(offres/20.0)),
                xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$", pl=pl,
                  auto_ylim=False, y_min=0.0, y_max=0.12, marker_size=10.0,
                  auto_xlim=False, x_min=-30-90, x_max=10-90)#.show()


    ax=pl.axes
    #ax=pl.figure.add_subplot(pl.nrows, pl.ncols, 4)
    ax.set_xticks(linspace(-30.0-90, 10.0-90, 3))
    ax.set_yticks(linspace(0.0, 0.10, 3))
    if do_simul:
        line(qdt.pwr_arr-90, 0.115*absolute(qdt.fexpt2[:, 68*phi_mult]), pl=pl, color="green") #127/4
        #line(qdt.pwr_arr-90, 0.12*absolute(qdt.fexpt2[:, 68*phi_mult+1]), pl=pl, color="black")
        #line(qdt.pwr_arr-90, 0.12*absolute(qdt.fexpt2[:, 68*phi_mult-1]), pl=pl, color="green")
    dw=0
    g=qdt.gamma/2.0
    pwr_fridge=qdt.pwr_arr-qdt.atten-11
    pwr_lin=0.001*10**(pwr_fridge/10.0)

    N=pwr_lin/(h*qdt.fd)#*abs(const.S21_0/(1+const.S22_0*exp(2i*const.theta_L)))^2

    def r_qubit(N):
        return -sqrt(qdt.gamma_el*g/2.0)/g*(1+1j*dw/g)/(1.0+dw**2/g**2+2*N/g*(qdt.gamma_el/(2.0*g)))
    line(qdt.pwr_arr-90, 0.11*absolute(r_qubit(N)), pl=pl, color="red")#.show()
    
    pl.nplot=2
    d1118.read_data()
    d1118.filter_type="FFT"
    cdata=(20*log10(absolute(d1118.MagcomFilt[:,:,1])).transpose()-bg_A4(d1118.frequency)).transpose()
    flux_axis=d1118.flux_axis[d1118.flat_flux_indices]
    freq_axis=d1118.freq_axis[d1118.indices]
    pl, pf=colormesh(flux_axis, freq_axis, (cdata[d1118.end_skip:-d1118.end_skip, :]/1.0),
                     pl=pl, pf_too=True, auto_zlim=False,
                     auto_xlim=False, x_min=0.35, x_max=0.5,
                     auto_ylim=False, y_min=4.1, y_max=4.8, vmin=-65.0, vmax=-15.0)

    pltest, pftest=colormesh(flux_axis, freq_axis, (cdata[d1118.end_skip:-d1118.end_skip, :]/1.0),
                     pl="test_colormesh", pf_too=True, auto_zlim=False,
                     auto_xlim=False, x_min=0.4, x_max=0.5,
                     auto_ylim=False, y_min=4.1, y_max=4.8, vmin=-65.0, vmax=-15.0)

    
    magabs=10**(cdata[:,:]/20.0)
    d1118.fitter.full_fit(x=flux_axis, y=magabs**2, indices=[473], #d1118.flat_indices,
                          gamma=d1118.fitter.gamma)
    #if self.calc_p_guess:
    #            self.fitter.make_p_guess(self.flux_axis[self.flat_flux_indices], y=self.MagAbsFilt_sq, indices=self.flat_indices, gamma=self.fitter.gamma)
    fit_params=d1118.fitter.fit_params

    MagAbsFit=sqrt(d1118.fitter.reconstruct_fit(flux_axis, fit_params))
    #colormesh(flux_axis/pi, freq_axis[d1118.flat_indices], 20*log10(MagAbsFit), pl=pltest) 
                   
    cbr=colorbar(pf.clt, ax=pl.axes)
    cbr.set_label("$|S_{21}|$ (dB)", size=8, labelpad=-10)
    cbr.set_ticks(linspace(-60, -20, 2))
    pl.axes.set_xticks(linspace(0.38, 0.48, 3))
    pl.axes.set_yticks(linspace(4.2, 4.7, 3))
    pl.axes.set_ylabel("Frequency (GHz)")
    pl.axes.set_xlabel("$\Phi/\Phi_0$")

    if 1:
        #frq1=c.freq_axis[595]
        pl.nplot=3
        #flux_axis=c.flux_axis[c.flat_flux_indices]
        #freq_axis=c.freq_axis[c.indices]
            
        #c.filter_type="Fit"
        #cdata2=(20*log10(c.MagAbs).transpose()-bg_A1(c.frequency[c.indices])).transpose()
        #start_ind=0
            #c.magabs_colormesh(pl=plbg)

    if 1:
        #ind=argmin(absolute(frq1-c.freq_axis))-1

        line(flux_axis, MagAbsFit.transpose(), #10**(cdata[456, :]/20.0),
             pl=pl,
              color="red")
        scatter( flux_axis, magabs[473, :], #10**(cdata[456, :]/20.0),
            pl=pl,
            auto_xlim=False, x_min=0.35, x_max=0.5,
            auto_ylim=False, y_min=0.0, y_max=0.2, 
                ylabel="$|S_{21}|$", xlabel="$\Phi/\Phi_0 $", marker_size=10)
        pl.axes.set_xticks(linspace(0.38, 0.48, 3))
        pl.axes.set_yticks(linspace(0.0, 0.2, 3))

    
    if 1:
        c.read_data()
        plbg.nplot=4
        c.filter_type="None"

        cdata=(20*log10(c.MagAbs).transpose()-bg_A1(c.frequency)).transpose()
        flux_axis=c.flux_axis[c.flat_flux_indices]
        freq_axis=c.freq_axis[c.indices]
        plbg, pfbg=colormesh(flux_axis, freq_axis, 10**(cdata[:, :]/20.0), pl=plbg,
                         pf_too=True, auto_zlim=False,
                                   auto_xlim=False, x_min=0.65, x_max=1.5,
                                   auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12)
        #pl, pf=c.magabs_colormesh(pl=pl, pf_too=True, auto_zlim=False,
        #                           auto_xlim=False, x_min=0.65, x_max=1.5,
        #                           auto_ylim=True, vmin=0.0, vmax=0.02)
        cbr=colorbar(pfbg.clt, ax=plbg.axes)
        cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
        cbr.set_ticks(linspace(0.0, 0.12, 2))
        plbg.axes.set_xticks(linspace(0.7, 1.5, 3))
        plbg.axes.set_yticks(linspace(4.35, 4.55, 5))
        plbg.axes.set_ylabel("Frequency (GHz)")
        plbg.axes.set_xlabel("$\Phi/\Phi_0$")
  
       
        c.filter_type="FFT"
        print c.MagcomFilt.shape
        print c.frequency.shape
        cdata=(20*log10(absolute(c.MagcomFilt)).transpose()-bg_A1(c.frequency)).transpose()
        flux_axis=c.flux_axis[c.flat_flux_indices]
        freq_axis=c.freq_axis[c.indices]
        pl88, pf88=colormesh(flux_axis, freq_axis, 10**(cdata[c.end_skip:-c.end_skip, :]/20.0),
                             pl=pl88, pf_too=True, auto_zlim=False,
                                   auto_xlim=False, x_min=0.65, x_max=1.5,
                                   auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12)

        cbr=colorbar(pf88.clt, ax=pl88.axes)
        cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
        cbr.set_ticks(linspace(0.0, 0.12, 2))
        pl88.axes.set_xticks(linspace(0.7, 1.5, 3))
        pl88.axes.set_yticks(linspace(4.35, 4.55, 5))
        pl88.axes.set_ylabel("Frequency (GHz)")
        pl88.axes.set_xlabel("$\Phi/\Phi_0$")


        plbg.nplot=5
        plbg, pfbg=colormesh(flux_axis, freq_axis, 10**(cdata[c.end_skip:-c.end_skip, :]/20.0), 
                             pl=plbg,
                         pf_too=True, auto_zlim=False,
                                   auto_xlim=False, x_min=0.65, x_max=1.5,
                                   auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12)

        #pl, pf=c.magabs_colormesh(pl=pl, pf_too=True, auto_zlim=False,
        #                           auto_xlim=False, x_min=0.65, x_max=1.5,
        #                           auto_ylim=True, vmin=0.0, vmax=0.02)
        cbr=colorbar(pfbg.clt, ax=plbg.axes)
        cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
        cbr.set_ticks(linspace(0.0, 0.12, 2))
        plbg.axes.set_xticks(linspace(0.7, 1.5, 3))
        plbg.axes.set_yticks(linspace(4.35, 4.55, 5))
        plbg.axes.set_ylabel("Frequency (GHz)")
        plbg.axes.set_xlabel("$\Phi/\Phi_0$")

        #plbg.nplot=6

        #c.filter_type="Fit"
        #print c.MagcomFilt.shape
        #print c.frequency.shape
        #c.magabs_colormesh(pl=plbg)
        #flux_axis=c.flux_axis[c.flat_flux_indices]
        #freq_axis=d.freq_axis[d.indices]
        #start_ind=0

        #for ind in c.fit_indices:
            #cdata=(20*log10(absolute(c.Magcom)).transpose()-bg_A1(c.frequency)).transpose()
            #new_magabs=10**(cdata/20.0)
        
        #    plbg, pfbg=colormesh(flux_axis, c.freq_axis[ind],
        #                         new_magabs[start_ind:start_ind+len(ind), :],  
        #                        pl=plbg, pf_too=True, auto_zlim=False,
        #                           auto_xlim=False, x_min=0.65, x_max=1.5,
        #                           auto_ylim=False, y_min=4.342, y_max=4.558,
        #                           vmin=0.0, vmax=0.12)
        #    start_ind+=len(ind)

        #plbg, pfbg=colormesh(flux_axis, freq_axis, 10**(cdata[c.end_skip:-c.end_skip, :]/20.0), 
        #                     pl=plbg,
        #                 pf_too=True, auto_zlim=False,
        #                           auto_xlim=False, x_min=0.65, x_max=1.5,
        #                           auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12)

        #pl, pf=c.magabs_colormesh(pl=pl, pf_too=True, auto_zlim=False,
        #                           auto_xlim=False, x_min=0.65, x_max=1.5,
        #                           auto_ylim=True, vmin=0.0, vmax=0.02)
        #cbr=colorbar(pfbg.clt, ax=plbg.axes)
        #cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
        #cbr.set_ticks(linspace(0.0, 0.12, 2))
        #plbg.axes.set_xticks(linspace(0.7, 1.5, 3))
        #plbg.axes.set_yticks(linspace(4.35, 4.55, 5))
        #plbg.axes.set_ylabel("Frequency (GHz)")
        #plbg.axes.set_xlabel("$\Phi/\Phi_0$")

        if 0:
            frq1=c.freq_axis[595]
            pl.nplot=3
            flux_axis=c.flux_axis[c.flat_flux_indices]
            freq_axis=c.freq_axis[c.indices]
            
            c.filter_type="Fit"
            cdata2=(20*log10(c.MagAbs).transpose()-bg_A1(c.frequency[c.indices])).transpose()
            start_ind=0
            #c.magabs_colormesh(pl=plbg)

        if 0:
            ind=argmin(absolute(frq1-c.freq_axis))-1

            line(flux_axis, 10**(cdata2[ind, :]/20.0), pl=pl,
                                       auto_xlim=False, x_min=0.65, x_max=1.5,
                                       auto_ylim=False, y_min=0.0, y_max=0.12, color="red")
            scatter(flux_axis, 10**(cdata[595, :]/20.0), pl=pl,
                                       auto_xlim=False, x_min=0.65, x_max=1.5,
                                       auto_ylim=False, y_min=0.0, y_max=0.12, 
                                       xlabel="$|S_{21}|$", ylabel="$\Phi/\Phi_0$")
            pl.axes.set_xticks(linspace(0.7, 1.5, 3))
            pl.axes.set_yticks(linspace(0.0, 0.1, 5))

        if 0:
            plbg.nplot=6
            for ind in c.fit_indices:
                plbg, pfbg=colormesh(flux_axis, c.freq_axis[ind], 10**(cdata[start_ind:start_ind+len(ind), :]/20.0),
                                  pl=plbg,
                             pf_too=True, auto_zlim=False,
                                       auto_xlim=False, x_min=0.65, x_max=1.5,
                                       auto_ylim=False, y_min=4.342, y_max=4.558, vmin=0.0, vmax=0.12)
                start_ind+=len(ind)
        if 0:
            ind=argmin(absolute(frq1-c.freq_axis))-1

            line(flux_axis, 10**(cdata2[ind, :]/20.0), pl=pl,
                                       auto_xlim=False, x_min=0.65, x_max=1.5,
                                       auto_ylim=False, y_min=0.0, y_max=0.12, color="red")
            scatter(flux_axis, 10**(cdata[595, :]/20.0), pl=pl,
                                       auto_xlim=False, x_min=0.65, x_max=1.5,
                                       auto_ylim=False, y_min=0.0, y_max=0.12, 
                                       xlabel="$|S_{21}|$", ylabel="$\Phi/\Phi_0$")
            pl.axes.set_xticks(linspace(0.7, 1.5, 3))
            pl.axes.set_yticks(linspace(0.0, 0.1, 5))
                                     
        #pl, pf=colormesh(flux_axis, freq_axis, 10**(cdata[c.end_skip:-c.end_skip, :]/20.0),
        #pl, pf=c.magabs_colormesh(pl=pl, pf_too=True, auto_zlim=False,
        #                           auto_xlim=False, x_min=0.65, x_max=1.5,
        #                           auto_ylim=True, vmin=0.0, vmax=0.02)
        if 0:
            cbr=colorbar(pfbg.clt, ax=plbg.axes)
            cbr.set_label("$|S_{21}|$", size=8, labelpad=-10)
            cbr.set_ticks(linspace(0.0, 0.12, 2))
            plbg.axes.set_xticks(linspace(0.7, 1.5, 3))
            #pl.axes.set_yticks(linspace(4.35, 4.55, 5))
            plbg.axes.set_ylabel("Frequency (GHz)")
            plbg.axes.set_xlabel("$\Phi/\Phi_0$")


    if 1:
        d.read_data()
        d.bgsub_type="dB"
        pl1, pf1=d.magdB_colormesh(auto_zlim=False, vmin=-3.0, vmax=0.0,
                              auto_ylim=False, y_min=4.2, y_max=4.9,
                              auto_xlim=False, x_min=0.7, x_max=1.5,
                              fig_width=5.0, fig_height=4.0, pf_too=True,
                              )
        cbr=colorbar(pf1.clt, ax=pl1.axes)
        cbr.set_label("$\Delta S_{21}$ [dB]", size=8, labelpad=-10)
        cbr.set_ticks(linspace(-3.0, 0.0, 2))

        pl1.axes.set_xticks(linspace(0.7, 1.5, 5))
        pl1.axes.set_yticks(linspace(4.2, 4.8, 4))


    pl.figure.tight_layout()
    plbg.figure.tight_layout()

    a.save_plots([pl, plbg])#, pl1])

    pl.show()



#a.bgsub_type="Complex"
if __name__=="__main2__":
    pl="magabs"
    pl1="centers"

if __name__=="__main2__":
    a.magabs_colormesh(vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False, pl="mag")

    #pl=colormesh(a.MagAbs.transpose())
    #colormesh(savgol_filter(a.MagAbs, 11, 3, axis=1).transpose(), pl=pl).show()
    #colormesh(array([savgol_filter(a.MagAbs[:, n], 5, 2) for n in range(len(a.yoko))]), pl=pl)
    #pl.show()
    if 0:

        pl=a.magabs_colormesh(vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False)

        a.filter_type="FFT"
        #colormesh(array([savgol_filter(a.MagAbs[:, n], 5, 2) for n in range(len(a.yoko[a.flux_indices]))]))
        a.magabs_colormesh(pl=pl)#.show()
    a.filter_type="Fit"

    pl=a.magabs_colormesh(pl=pl, vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False, fig_width=9, fig_height=6)
    a.widths_plot()
    centers=-a.qdt._get_fluxfq0(f=a.frequency[a.indices])
    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])<0.3]
    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])>0.1]
    print [a.indices[n] for n, fp in enumerate(a.fit_params[:-1]) if absolute(fp[1]-a.fit_params[n+1][1])>0.1]
    print shape(a.flat_indices)
    print shape(a.flat_flux_indices)
    print shape(a.MagAbsFilt_sq)
    pl1=a.center_plot()

if __name__=="__main2__":
    a.flux_indices=[range(200, 400)]#, range(436, 610)]
    fit1=a.fit_indices[:]
    a.fit_indices=[[1], range(4, 11), [15], range(17, 23), range(26, 28), range(29, 37), range(38, 41), range(42,53), range(56,68),
                   range(71,77), range(78,81), [84], range(104,107), range(108,111), [116], range(124,129), [138],
                   range(182,184), range(189,194),
                   range(218, 255), range(264, 285), range(310,325)]#, range(337,348)]
    #a.fit_indices=[range(2, 14), range(15, 17), range(19,23), range(24, 26), range(29, 37), range(38, 39), range(44, 46), range(48, 52),
    #           range(54, 66), range(67, 69), range(70, 85), range(105, 107), range(108, 116), range(122, 129), [130], range(132, 134), [138],
    #             range(189, 193), range(199, 200), range(217, 251+1), range(266, 275+1), range(314, 324+1)]

    a.fitter.fit_params=None
    reset_property(a, "fit_params", "MagAbsFit", "MagcomFilt", "Magcom")
    if 0:
        a.filter_type="None"

        pl=a.magabs_colormesh(pl=pl)

        a.filter_type="FFT"
        a.magabs_colormesh(pl=pl)#.show()
    a.filter_type="Fit"

    a.magabs_colormesh(pl=pl, vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False, fig_width=9, fig_height=6)#.show()
    centers=a.qdt._get_fluxfq0(f=a.frequency[a.indices])

    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])>0.3]

    pl1=a.center_plot(pl=pl1)




if __name__=="__main2__":
    a.flux_indices=[range(610, 748), range(751, 758), range(761,800)]#, range(436, 610)]

    #a.fit_indices=list(set(fit1).union(set(fit2)))
    #a.fit_indices=[range(len(a.frequency))]
    a.fit_indices=[range(5,9), [11], range(15, 22), [23,24], range(30,35),
                   [36], range(44, 51), range(59, 62), [63, 64], [66], range(70, 72),
                   range(73, 75), range(76, 83), [87], range(104, 107), range(109, 111),
                   range(112, 116), range(124, 130), [138], range(182,184), range(189, 194), [201],
                   range(217, 253), range(265, 281), range(314, 326)]#, range(343, 350)]
    #a.fit_indices=[range(2, 14), range(15, 17), range(19,23), range(24, 26), range(29, 37), range(38, 39), range(44, 46), range(48, 52),
    #           range(54, 66), range(67, 69), range(70, 85), range(105, 107), range(108, 116), range(122, 129), [130], range(132, 134), [138],
    #             range(189, 193), range(199, 200), range(217, 251+1), range(266, 275+1), range(314, 324+1)]
    a.fitter.fit_params=None
    reset_property(a, "fit_params", "MagAbsFit", "MagcomFilt", "Magcom")
    if 0:
        a.filter_type="None"

        pl=a.magabs_colormesh(pl=pl)

        a.filter_type="FFT"
        a.magabs_colormesh(pl=pl)#.show()
    a.filter_type="Fit"

    a.magabs_colormesh(pl=pl, vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False)#.show()
    centers=a.qdt._get_fluxfq0(f=a.frequency[a.indices])

    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])>0.3]

    pl1=a.center_plot(pl=pl1)


if __name__=="__main2__":
    a.flux_indices=[range(0, 2), range(5,200)]#, range(436, 610)]
    a.fit_indices=[range(len(a.frequency))]

    a.fit_indices=[range(4, 7), [21], [47,48], [50], [72], [75], [78,79], [104], [109, 110],
                   range(137, 140), range(182,184),
                   range(188, 194), range(220,253), range(265, 282), range(314, 327)]

    a.fitter.fit_params=None
    reset_property(a, "fit_params", "MagAbsFit", "MagcomFilt", "Magcom")
    if 0:
        a.filter_type="None"

        pl=a.magabs_colormesh(pl=pl)#.show()

        a.filter_type="FFT"
        a.magabs_colormesh(pl=pl)#.show()
    a.filter_type="Fit"

    a.magabs_colormesh(pl=pl, vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False)#.show()
    centers=a.qdt._get_fluxfq0(f=a.frequency[a.indices])

    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])>0.3]


    pl1=a.center_plot(pl=pl1)

if __name__=="__main__2":
    nps=TA88_Save_NP(file_path=r"/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/discard/S2016_07_28_171620/meas.txt")
    nps.save(pl1.savedata())
    npr=TA88_Read_NP(file_path=nps.file_path, show_data_str=True)
    data=npr.read()
    scatter(data[:, 0], data[:, 1])
    #nps.data_buffer=pl1.savedata()
    pl1.show(nps, npr)

if __name__=="__main2__":
    pl.set_xlim(-6,6)
    pl.set_ylim(3.5, 7.5)
    pl.savefig(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/", "fit_fluxmap")
    pl1.show()


if __name__=="__main2__":
    from taref.physics.filtering import Filter
    from numpy import absolute
    b=Filter(center=0, halfwidth=40, reflect=False, N=len(a.yoko))
    #Magcom=a.Magcom.transpose()
    Magfilt=array([b.fft_filter(a.Magcom[m,:]) for m in range(len(a.frequency[a.indices]))])#.transpose()
    pl=line(b.fftshift(absolute(b.window_ifft(a.Magcom[261, :]))), color="red")
    line(b.fftshift(absolute(b.window_ifft(a.Magcom[240, :]))), pl=pl)
    pl=colormesh(a.MagAbs)
    colormesh(absolute(Magfilt)[:, 10:-10]).show()
    colormesh((absolute(Magfilt).transpose()-absolute(Magfilt[:,20])).transpose()[:, 10:-10]).show()
    a.bgsub_type="Complex"
    pl, pf=line(a.MagAbs[:, 517])
    line(a.MagAbs[:, 519], color="red", pl=pl)
    line(a.MagAbs[:, 521], color="green", pl=pl)

    pl, pf=line(a.freq_axis, a.qdt._get_VfFWHM(f=a.frequency)[0],  color="blue")
    line(a.freq_axis, a.qdt._get_VfFWHM(f=a.frequency)[1],  color="green", pl=pl)

    line(a.freq_axis, a.qdt._get_VfFWHM(f=a.frequency)[2],  color="red", pl=pl)

    line(a.freq_axis, a.qdt._get_Vfq0(f=a.frequency),  color="purple", pl=pl)

    a.magabs_colormesh()
    a.bgsub_type="Abs"
    a.magabs_colormesh().show()

    a.hann_ifft_plot()
    def magdB_colormesh(self):
        pl, pf=colormesh(self.yoko, self.frequency/1e9, (self.MagdB.transpose()-self.MagdB[:,0]).transpose(), plotter="magabs_{}".format(self.name))
        pl.set_ylim(min(self.frequency/1e9), max(self.frequency/1e9))
        pl.set_xlim(min(self.yoko), max(self.yoko))
        pl.xlabel="Yoko (V)"
        pl.ylabel="Frequency (GHz)"
        return pl
    a.magabsfilt_colormesh()
    magdB_colormesh(a).show()
    a.magabs_colormesh().show()

    def magabs_colormesh2(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
        fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])

        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
        pl, pf=colormesh(fq_vec, self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0]), plotter=pl)
        pf.set_clim(-0.3, 0.1)
        #pl.set_xlim(min(self.frequency/1e9), max(self.frequency/1e9))
        pl.set_ylim(min(self.yoko), max(self.yoko))

        pl.ylabel="Yoko (V)"
        pl.xlabel="Frequency (GHz)"
        return pl

    def magabs_colormesh(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
        fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])
        freq, frq2=flux_parabola(self.yoko, offset, 0.16, Ejmax, qdt.Ec)

        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
        pl, pf=colormesh(freq, fq_vec, (self.MagdB.transpose()-self.MagdB[:, 0]).transpose(), plotter=pl)
        pf.set_clim(-0.3, 0.1)
        line([min(freq), max(freq)], [min(freq), max(freq)], plotter=pl)
        flux_o_flux0=flux_over_flux0(self.yoko, offset, flux_factor)
        qEj=Ej(Ejmax, flux_o_flux0)
        EjdivEc=qEj/qdt.Ec
        ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)

        frq2=qdt.call_func("lamb_shifted_anharm", EjdivEc=EjdivEc)/h
        line(ls_fq, ls_fq2, plotter=pl)

        #pl.set_xlim(min(self.frequency/1e9), max(self.frequency/1e9))
        #pl.set_ylim(min(self.yoko), max(self.yoko))

        pl.ylabel="Yoko (V)"
        pl.xlabel="Frequency (GHz)"
        return pl

    def line_cs(self, ind=210):
        print self.frequency[ind]/1e9
        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_cs_{}".format(self.name))
        pl, pf=line(self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0])[:, ind], plotter=pl, linewidth=1.0)
        pl.xlabel="Yoko (V)"
        pl.ylabel="Magnitude (dB)"
        return pl

    #def flux_par(self, pl, offset, flux_factor):
    #    set_tag(qdt, "EjdivEc", log=False)
    #    set_tag(qdt, "Ej", log=False)
    #    set_tag(qdt, "offset", log=False)
    #    set_tag(qdt, "flux_factor", log=False)
    #
    #    print qdt.max_coupling, qdt.coupling_approx
    #    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    #    Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0)
    #    EjdivEc=Ej/qdt.Ec
    #    #fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    #    ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
    #    ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
    #    line(self.yoko, ls_fq/1e9, plotter=pl, color="blue", linewidth=0.5, label=r"$\Delta_{1,0}$")
    #    line(self.yoko, ls_fq2/1e9, plotter=pl, color="red", linewidth=0.5, label=r"$\Delta_{2,1}$")
    #    #pl.set_ylim(-1.0, 0.6)
    #    #pl.set_xlim(0.7, 1.3)
    #    return pl

    from taref.physics.qubit import  flux_parabola, Ej_from_fq, voltage_from_flux, flux_over_flux0, Ej
    from taref.physics.qdt import lamb_shifted_anharm, calc_freq_shift, lamb_shifted_fq, lamb_shifted_fq2

    def fq2(Ej, Ec):
        E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
        #E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
        E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
        return (E2-E0)/h/2

    def Ej_from_fq2(fq2, Ec):
        return (((2*h*fq2+3.0*Ec)/2.0)**2)/(8.0*Ec)

    def flux_par4(self, offset=-0.08, flux_factor=0.16, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
        set_all_tags(qdt, log=False)
        flux_o_flux0=flux_over_flux0(self.yoko, offset, flux_factor)
        qEj=Ej(Ejmax, flux_o_flux0)
        #flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        freq, frq2=flux_parabola(self.yoko, offset, flux_factor, Ejmax, qdt.Ec)
        fq1=lamb_shifted_fq2(qEj/qdt.Ec, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv)
        line(self.yoko, freq, plotter=pl, linewidth=1.0, alpha=0.5)
        line(self.yoko, fq1/2, plotter=pl, linewidth=1.0, alpha=0.5)

    def flux_par3(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
        set_all_tags(qdt, log=False)
        flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        #print flux_o_flux0-pi/2*trunc(flux_o_flux0/(pi/2.0))
        #Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
        #EjdivEc=Ej/qdt.Ec
        fq_vec=array([sqrt(f*(f+1.0*qdt.call_func("calc_Lamb_shift", fqq=f))) for f in self.frequency])
        fq_vec=array([f-qdt.call_func("calc_Lamb_shift", fqq=f) for f in self.frequency])
        fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])
        Ej=Ej_from_fq(fq_vec, qdt.Ec)
        flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
        flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
        flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax)+pi)
        flux_d_flux0=append(flux_d_flux0, arccos(Ej/Ejmax)-pi)

        if pl is not None:
            volt=voltage_from_flux(flux_d_flux0, offset, flux_factor)
            freq=s3a4_wg.frequency[:]/1e9
            freq=append(freq, freq) #append(freq, append(freq, freq)))
            freq=append(freq, freq)
            #freq=append(freq, freq)
            line(freq, volt, plotter=pl, linewidth=1.0, alpha=0.5)
            Ejdivh=Ej/h
            w0=4*Ejdivh*(1-sqrt(1-fq_vec/(2*Ejdivh)))
            EjdivEc=Ej/qdt.Ec
            #print -(w0**2)/(8*Ejdivh)

            ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
            E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
            fq2=(E2-E1)/h
            f_vec=lamb_shifted_anharm(EjdivEc, qdt.ft, qdt.Np, qdt.f0, qdt.epsinf, qdt.W, qdt.Dvv)
            print f_vec/h
            ah=-ls_fq2/2#-fq2)
            #fq_vec=array([sqrt((f-ah[n])*(f-ah[n]+alpha*calc_freq_shift(f-ah[n], qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for n, f in enumerate(self.frequency)])
            fq_vec=array([f/2-qdt.call_func("calc_Lamb_shift", fqq=f/2) for f in self.frequency])
            coup=qdt.call_func("calc_coupling", fqq=self.frequency)
            print coup
            volt=array([
              voltage_from_flux(arccos(Ej_from_fq(f-f_vec[c]/h/2, qdt.Ec)/Ejmax), offset, flux_factor)
              for c,f in enumerate(self.frequency)])
            #freq=nan_to_num(freq)/1e9
            #print freq
            freq=s3a4_wg.frequency[:]/1e9

            #freq=(s3a4_wg.frequency[:]+coup)/1e9
            #freq=append(freq, freq)
            #freq=append(freq, freq)
            #Ej=Ej_from_fq(fq_vec, f_vec/h)
            #flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
            #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
            #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax)+pi)
            #flux_d_flux0=append(flux_d_flux0, arccos(Ej/Ejmax)-pi)

            #freq=append(freq, freq)
            #fq_vec+=f_vec/h/2
            #fq2_vec=fq2(Ej, qdt.Ec)
            #Ej=Ej_from_fq(fq_vec, qdt.Ec) #qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
            #Ej=Ej_from_fq(fq_vec, qdt.Ec)
            #flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
            #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
            #volt=voltage_from_flux(flux_d_flux0, offset, flux_factor)
            line(freq, volt, plotter=pl, plot_name="second", color="green", linewidth=1.0, alpha=0.5)
        #flux_d_flux0.append(-)
        return voltage_from_flux(flux_d_flux0, offset, flux_factor)

    print shape(flux_par3(s3a4_wg, 0.0, 0.3, qdt.Ejmax))#, shape(self.frequency)
    def flux_par2(self, offset, flux_factor, Ejmax):
        set_all_tags(qdt, log=False)
        flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
        EjdivEc=Ej/qdt.Ec
        fq_vec=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
        results=[]
        for fq in fq_vec:
            def Ba_eqn(x):
                return x[0]**2+2.0*x[0]*qdt.call_func("calc_Lamb_shift", fqq=x[0])-fq**2
            results.append(fsolve(Ba_eqn, fq))
        return squeeze(results)/1e9

    #flux_par2(s3a4_wg, 0.0, 0.18, qdt.Ejmax)

    def flux_par(self, offset, flux_factor, Ejmax):
        set_all_tags(qdt, log=False)
    #    set_tag(qdt, "EjdivEc", log=False)
    #    set_tag(qdt, "Ej", log=False)
    #    set_tag(qdt, "offset", log=False)
    #    set_tag(qdt, "flux_factor", log=False)
        flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
        EjdivEc=Ej/qdt.Ec
        fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
        ls=qdt.call_func("calc_Lamb_shift", fqq=fq)
        return fq/1e9
        ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
        return ls_fq/1e9#, ls_fq2/1e9

    pl=magabs_colormesh(s3a4_wg).show()
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_colormap.png")
    flux_par4(s3a4_wg, pl=pl)#.show()#, f0=5.45e9, alpha=1.0)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_colormap_bothpar.png")

    #pl=line_cs(s3a4_wg, 190)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_5p4.pdf")
    #pl=line_cs(s3a4_wg, 210)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_5p6.pdf")
    #pl=line_cs(s3a4_wg, 239)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_5p89.pdf")
    #pl=line_cs(s3a4_wg, 246)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_5p96.pdf")
    #pl=line_cs(s3a4_wg, 256)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_6p06.pdf")


    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_colormap_bothpar.png")
    pl.show()

    class Fitter(LineFitter):
        Ejmax=FloatRange(0.001, 100.0, qdt.Ejmax/h/1e9).tag(tracking=True)
        offset=FloatRange(-5.0, 5.0, 0.0).tag(tracking=True)
        flux_factor=FloatRange(0.1, 5.0, 0.3).tag(tracking=True)
        f0=FloatRange(4.0, 6.0, qdt.f0/1e9).tag(tracking=True)
        alpha=FloatRange(0.1, 2.0, 1.0).tag(tracking=True)

        def _default_plotter(self):
            if self.plot_name=="":
                self.plot_name=self.name
            freq=s3a4_wg.frequency[:]/1e9
            freq=append(freq, freq)
            freq=append(freq, freq)
            pl1, pf=line(freq, self.data, plot_name=self.plot_name, plotter=pl)
            self.plot_name=pf.plot_name
            return pl1

        @tag_Property(private=True)
        def data(self):
            return flux_par3(s3a4_wg, offset=self.offset, flux_factor=self.flux_factor, Ejmax=self.Ejmax*h*1e9, f0=self.f0*1e9, alpha=self.alpha)

    d=Fitter()
    d.show(d.plotter)

    #s3a4_wg
    #s3a4_mp.magabsfilt_colormesh("filtcolormesh S3A4 mp")
    #s3a4_mp.magdBfilt_colormesh("filtdB S1A4 wide")
    #s3a4_mp.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
            #a2.filt_compare(a2.start_ind, bb2)
    #s3a4_mp.filt_compare("filt_compare_off_res", s3a4_mp.start_ind)
    #s3a4_mp.filt_compare("filt_compare_on_res", s3a4_mp.on_res_ind)
    #s3a4_mp.ifft_plot("ifft_S3A4 midpeak")
    #s3a4_mp.ifft_dif_plot("ifft__dif_S1A4 wide")

