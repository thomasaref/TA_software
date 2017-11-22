# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 13:26:14 2017

@author: thomasaref
"""

from TA88_fundamental import TA88_VNA_Lyzer, TA88_VNA_Pwr_Lyzer, TA88_Read, qdt as qdt88, idt as idt88, TA88_Read_NP, TA88_Save_NP, bg_A4, bg_A1
from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, idt, qdt

from taref.plotter.api import colormesh, line, scatter, Plotter
from numpy import log10, absolute, linspace, mean, sqrt
from D0527_trans_careful import MagcomFilt as MagcomFilt88
from D0527_trans_careful import a as d0527
from D0317_S4A1_frq_pulse_flux import a as d0317
from matplotlib.pyplot import colorbar#, tight_layout

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


pl="pwr_sat"

fig_width=7.2
fig_height=5.0

c.save_folder.main_dir="sup_fig3_pwr_sat"



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
b.save_folder.main_dir="sup_fig3_pwr_sat"

if 1:
    a=TA88_VNA_Pwr_Lyzer(name="d0222", on_res_ind=370, VNA_name="RS VNA",
                  rd_hdf=TA88_Read(main_file="Data_0222/S4A1_TA88_powswp.hdf5"),
                  desc="looking", swp_type="yoko_first",
                                flux_factor=qdt.flux_factor*1000.0/560.0,

                )

    a.filt.center=14
    a.filt.halfwidth=5
    a.fitter.fit_type="lorentzian"
    a.fitter.gamma=0.05 #0.01
    a.flux_axis_type="flux" #"yoko" #"fq" #"flux"
    a.end_skip=10
    #b.save_folder.main_dir=b.name

if __name__=="__main__":

    
    #pl.nplot=4
    a.read_data()
    b.read_data()

    #b.filter_type="None"
    #pl_raw=b.magabs_colormesh()
    #pl_ifft=b.ifft_plot()#.show()

    b.filter_type="FFT"

    pl=Plotter(name="pwr_sat", nrows=2, ncols=2)
    onres=(20*log10(absolute(b.MagcomFilt[69, :, :])).transpose()-bg_A4(b.freq_axis[69]*1e9)).transpose()
    
    pl, pf=colormesh(b.flux_axis, b.pwr-30-60, 10**(onres/20.0).transpose(), 
                  ylabel="Power (dBm) ", xlabel=r"$\Phi/\Phi_0$",
                  auto_xlim=False, x_min=0.35, x_max=0.5, 
                  auto_ylim=False, y_min=-30-90, y_max=10-90, nrows=2, ncols=2, nplot=1, pl=pl, pf_too=True, fig_width=fig_width, fig_height=fig_height)

    ax=pl.axes
    ax.set_yticks(linspace(-30.0-90, 10.0-90, 3))
    ax.set_xticks(linspace(0.38, 0.48, 3))
    
    #b.pwr, b.freq_axis[a.end_skip:-b.end_skip], 10**(onres/20.0), #absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 635, :]),
    #              ylabel="Frequency (GHz)", xlabel=r"Power (dBm")#.show()
    pl.nplot=2
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


    if 1:
        print a.comment
        scatter(absolute(a.MagcomFilt[50, 370, :]))
        print a.frequency[50]
        colormesh(absolute(a.MagcomFilt[a.end_skip:-a.end_skip, 362, :]))#.show()
        
        pl.nplot=3
        pl1=colormesh(a.flux_axis, a.pwr-40-60, absolute(a.MagcomFilt[50, :, :]).transpose(), 
                       auto_xlim=False, x_min=0.33, x_max=0.40, 
                      auto_ylim=False, y_min=-30-110, y_max=10-110,)
                      
        ax=pl.axes
        ax.set_yticks(linspace(-30.0-110, 10.0-110, 3))
        ax.set_xticks(linspace(0.34, 0.38, 3))              

        onres=20*log10(absolute(a.MagcomFilt[50, :, :]))+10-bg_A1(a.frequency[50])
        colormesh(a.flux_axis, a.pwr-40-60, absolute(10**(onres/20.0)).transpose(),
                   pl=pl, auto_xlim=False, x_min=0.33, x_max=0.40, 
                      auto_ylim=False, y_min=-30-100, y_max=10-100, ylabel="Power (dBm) ", xlabel=r"$\Phi/\Phi_0$")
        #b.save_plots([pl1])
        print a.pwr
        print a.flux_axis.shape
        #pl1.show()
        pl.nplot=4
        onres=20*log10(absolute(a.MagcomFilt[50, 362, :]))+10-bg_A1(a.frequency[50])
        offres=20*log10(absolute(a.MagcomFilt[50, 0, :]))+10-bg_A1(a.frequency[50])
        scatter(a.pwr-40-60, absolute(onres-offres))
        pl_pwr_sat=scatter(a.pwr-40-60, (absolute(10**(onres/20.0)-10**(offres/20.0))), pl=pl,
                  auto_ylim=False, y_min=0.0, y_max=0.2, marker_size=10.0,
                  auto_xlim=False, x_min=-30-110, x_max=10-90, xlabel="Power (dBm)", ylabel=r"$|\Delta S_{21}|$",)#/0.18)
        ax=pl.axes
        #ax=pl.figure.add_subplot(pl.nrows, pl.ncols, 4)
        ax.set_xticks(linspace(-30.0-110, 10.0-90, 3))
        ax.set_yticks(linspace(0.0, 0.20, 3))

        a.ifft_plot()




    pl.figure.tight_layout()
    b.save_plots([pl])#, pl1])
    
    pl.show()


if 0:
    nskip=50
    d0527.read_data()
    magfilt88=MagcomFilt88(d0527)
    magabs88=absolute(magfilt88)
    #line(d0527.frequency/1e9, magabs88)

    pl88=scatter(d0527.frequency[::nskip]/1e9, 20.0*log10(magabs88[::nskip])-bg_A4(d0527.frequency[::nskip]),
               facecolor="blue", edgecolor="blue", pl=pl88, nrows=2, ncols=3, nplot=1,
               fig_width=fig_width, fig_height=fig_height, marker_size=10)

    (S11, S12, S13,
     S21, S22, S23,
     S31, S32, S33)=idt88._get_simple_S(f=d0527.frequency)
    S13xS31=S13*S31
    print idt88.Np, idt88.K2
    print idt88.f0
    print d0527.comment
    print -d0527.fridge_atten+d0527.fridge_gain-d0527.rt_atten+d0527.rt_gain-10

    line(d0527.frequency/1e9, 20*log10(absolute(S13xS31))-4, color="red", pl=pl88,
         auto_ylim=False, y_min=-40, y_max=0,
         auto_xlim=False, x_min=4.2, x_max=4.7, xlabel="Frequency (GHz)",
         ylabel="Transmission (dB)", linewidth=1.0,
        )#.show()


    pl88.axes.set_xticks(linspace(4.2, 4.7, 3))
    pl88.axes.set_yticks(linspace(-40, 0, 5))

    d0317.read_data()
    cdata=10.0**((20.0*log10(mean(absolute(d0317.MagcomData[64:76, :, 0]), axis=0))-d0317.probe_pwr)/20.0)

    pl88.axes.plot(d0317.frequency/1e9, 
               20*log10(cdata)+10-1.0-bg_A1(d0317.frequency), "x", 10,
             color="green")


    pl88.nplot=2
    c.read_data()
    c.filter_type="FFT"
    print c.MagcomFilt.shape
    cdata=(20*log10(absolute(c.MagcomFilt[:,:])).transpose()-bg_A4(c.frequency)).transpose()
    flux_axis=c.flux_axis[c.flat_flux_indices]
    freq_axis=c.freq_axis[c.indices]
    #pl, pf=colormesh(flux_axis, freq_axis, (cdata[d1118.end_skip:-d1118.end_skip, :]/1.0),
    #                 pl=pl, pf_too=True, auto_zlim=False,
    #                 auto_xlim=False, x_min=0.35, x_max=0.5,
    #                 auto_ylim=False, y_min=4.1, y_max=4.8, vmin=-65.0, vmax=-15.0)

    pl88, pf88=colormesh(flux_axis, freq_axis, cdata[c.end_skip:-c.end_skip, :], #10**(cdata[c.end_skip:-c.end_skip, :]/20.0),
                         pl=pl88, pf_too=True, auto_zlim=False,
                               auto_xlim=False, x_min=0.25, x_max=0.45,
                               auto_ylim=False, y_min=4.342, y_max=4.558, vmin=-15.0, vmax=-35.0)

    cbr=colorbar(pf88.clt, ax=pl88.axes)
    cbr.set_label("$|S_{21}|$  (dB)", size=8, labelpad=-10)
    cbr.set_ticks(linspace(-20.0, -30.0, 2))
    pl88.axes.set_xticks(linspace(0.25, 0.45, 3))
    pl88.axes.set_yticks(linspace(4.35, 4.55, 5))
    pl88.axes.set_ylabel("Frequency (GHz)")
    pl88.axes.set_xlabel("$\Phi/\Phi_0$")
    
                
#    cbr=colorbar(pf.clt, ax=pl.axes)
#    cbr.set_label("$|S_{21}|$ (dB)", size=8, labelpad=-10)
#    cbr.set_ticks(linspace(-60, -20, 2))
#    pl.axes.set_xticks(linspace(0.38, 0.48, 3))
#    pl.axes.set_yticks(linspace(4.2, 4.7, 3))
#    pl.axes.set_ylabel("Frequency (GHz)")
#    pl.axes.set_xlabel("$\Phi/\Phi_0$")

    pl88.nplot=3

    magabs=10**(cdata[:,:]/20.0)
    c.fitter.full_fit(x=flux_axis, y=magabs**2, indices=[558], #d1118.flat_indices,
                          gamma=c.fitter.gamma)
    #if self.calc_p_guess:
    #            self.fitter.make_p_guess(self.flux_axis[self.flat_flux_indices], y=self.MagAbsFilt_sq, indices=self.flat_indices, gamma=self.fitter.gamma)
    fit_params=c.fitter.fit_params

    MagAbsFit=sqrt(c.fitter.reconstruct_fit(flux_axis, fit_params))
    #colormesh(flux_axis/pi, freq_axis[d1118.flat_indices], 20*log10(MagAbsFit), pl=pltest) 
       
    line(flux_axis, 20*log10(MagAbsFit.transpose()), #10**(cdata[456, :]/20.0),
         pl=pl88,
          color="red")
    scatter( flux_axis, cdata[558, :], #magabs[473, :], #10**(cdata[456, :]/20.0),
        pl=pl88,
        auto_xlim=False, x_min=0.3, x_max=0.4,
        auto_ylim=False, y_min=-25, #0.0,
        y_max=-15, #0.2, 
            ylabel="$|S_{21}|$  (dB)", xlabel="$\Phi/\Phi_0 $", marker_size=10)
    pl88.axes.set_xticks(linspace(0.3, 0.4, 3))
    pl88.axes.set_yticks(linspace(-25, -15, 3))#0.0, 0.2, 3))

    pl88.figure.tight_layout()

    c.save_plots([pl88])#, pl1])
    pl88.show()
