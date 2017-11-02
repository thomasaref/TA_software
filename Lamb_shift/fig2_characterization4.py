# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""



from TA88_fundamental import TA88_VNA_Lyzer, TA88_Read, qdt as qdt88, idt as idt88, TA88_Read_NP, TA88_Save_NP, bg_A4, bg_A1
from TA88_fundamental import bg_A1, bg_A4

from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, idt, qdt
from numpy import diag, mean, log10, array, absolute, squeeze, append, sqrt, pi, arccos, shape, linspace, argmin
from taref.physics.fundamentals import h
from taref.plotter.api import colormesh, line, scatter
from D1122_trans_direct import a as d1122
from D1122_trans_direct import MagcomFilt

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
a.save_folder.main_dir="fig2_characterization4"

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
              flux_factor=qdt.flux_factor*1000.0/560.0,
              offset=-0.045
              )
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
fig_height=2.5



if __name__=="__main__":
    pl="fig2"

    nskip=50

    magfilt=MagcomFilt(d1122)
    magabs=absolute(magfilt)

    pl=scatter(d1122.frequency[::nskip]/1e9, 20.0*log10(magabs[::nskip])-bg_A4(d1122.frequency[::nskip]),
               facecolor="blue", edgecolor="blue", pl=pl, nrows=1, ncols=3, nplot=1,
               fig_width=fig_width, fig_height=fig_height, marker_size=10)
    
    #idt.Np=56
    #idt.f0=4.46e9 #4.452
    #idt.K2=0.032
    #idt.Np=36.5
    #idt.f0=4.452e9




    (S11, S12, S13,
     S21, S22, S23,
     S31, S32, S33)=idt._get_simple_S(f=d1122.frequency)
    
    print d1122.comment
    print -d1122.fridge_atten+d1122.fridge_gain-d1122.rt_atten+d1122.rt_gain-10
    print -d1122.fridge_atten, d1122.fridge_gain, -d1122.rt_atten, d1122.rt_gain, -10
    
    line(d1122.frequency/1e9, 20*log10(absolute(S13*S31))-4-5, color="red", pl=pl,
         auto_ylim=False, y_min=-60, y_max=-10,
         auto_xlim=False, x_min=4.1, x_max=4.8, xlabel="Frequency (GHz)",
         ylabel="$|S_{21}|$ (dB)", linewidth=1.0,
        )
    pl.axes.set_xticks(linspace(4.2, 4.7, 3))
    pl.axes.set_yticks(linspace(-60, -10, 6))
   
    b.read_data()

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


    onres=(20*log10(absolute(b.MagcomFilt[69, :, :])).transpose()-bg_A4(b.freq_axis[69]*1e9)).transpose()


    if 0:
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

    pl.nplot=3


    line(flux_axis, 20*log10(MagAbsFit.transpose()), #10**(cdata[456, :]/20.0),
         pl=pl,
          color="red")
    scatter( flux_axis, cdata[473, :], #10**(cdata[456, :]/20.0),
        pl=pl,
        auto_xlim=False, x_min=0.35, x_max=0.5,
        auto_ylim=False, y_min=-30.0, y_max=-15.0, 
            ylabel="$|S_{21}|$ (dB)", xlabel="$\Phi/\Phi_0 $", marker_size=10)
    pl.axes.set_xticks(linspace(0.38, 0.48, 3))
    pl.axes.set_yticks(linspace(-10.0, -30.0, 3))

    if 0:
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

    a.save_plots([pl])#, pl1])

    pl.show()

