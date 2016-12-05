# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:36:21 2016

@author: thomasaref
"""




from D0514_highfrq1sidelobe import a as d0514
from D0316_S4A1_coupling_midpeak import a as d0316
from D0629_fft_try import a as d0629
#from D0629_wide_gate_fluxswp import a as d0629wg
from D0506_lowfrq34sidelobe import a as d0506
from D0509_lowfrq2sidelobe import a as d0509
from D0503_lowfrq1sidelobe import a as d0503
from D0518_highfrq3sidelobe import a as d0518

from numpy import array, linspace, absolute
from taref.plotter.api import line, colormesh

from TA88_fundamental import qdt, TA88_Lyzer
from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read


a=TA88_Lyzer( name="combo",
             desc="combined data",
             )
a.save_folder.main_dir="fig3_ls"

lyzers=[d0514, d0316, d0629, d0518, d0506, d0509, d0503#, d0629wg,
]

b=TA53_VNA_Pwr_Lyzer(name="d1118", on_res_ind=301,
        rd_hdf=TA53_Read(main_file="Data_1118/S3A4_trans_swp_n5n15dBm.hdf5"),
        #fit_indices=[range(850, 2300)], #range(48,154+1), range(276, 578+1)],
         desc="transmission power sweep",
         offset=-0.1,
         swp_type="yoko_first",
        )
b.filt.center=0 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
b.filt.halfwidth=100 #8 #10
b.fitter.gamma=0.3 #0.035
b.flux_axis_type="fq" #
b.end_skip=10
#a.flux_indices=[range(len(a.yoko)-1)]
b.pwr_ind=1

def combo_plots():
    for d in lyzers:
        d.filter_type="FFT"
        d.bgsub_type="dB"
        d.show_quick_fit=False
        d.read_data()
    pl="fig3"
    for d in lyzers:
        pl=d.center_plot(pl=pl, color="red", nrows=2, ncols=2, auto_xlim=False, auto_ylim=False)
    frequency=linspace(3.8e9, 6.05e9, 1000)
    V=qdt._get_fq0(f=frequency)#[1]
    #line(frequency/1e9, V/1e9, pl=pl,  ylabel="Qubit frequency (GHz)", xlabel="Frequency (GHz)")
    #line(frequency/1e9, frequency/1e9-qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="purple", xlabel="Frequency (GHz)",
    #     ylabel="HWFM (GHz)")
    qdt.gate_type="constant"
    line(frequency/1e9, frequency/1e9-qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="blue", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")
    line(array([3.75, 6.1]), array([3.75, 6.1]), pl=pl, color="green")

    pl.set_xlim(3.75, 6.1)
    pl.set_ylim(3.75, 6.1)
    #pl.add_label("a)")

    pl1="combined_heights"
    for d in lyzers:
        pl1=d.heights_plot(pl=pl1)
    pl1.yscale="log"
    pl1.xlabel="Frequency (GHz)"
    pl1.ylabel="Lorentzian height (a.u.)"
    pl1.set_xlim(3.8, 6.05)
    pl1.set_ylim(1e-8, 1e-3)
    pl1.add_label("b)")

    pl1="combined_backgrounds"
    for d in lyzers:
        pl1=d.background_plot(pl=pl1)

    pl1="comb_widths"
    for d in lyzers:
        pl1=d.widths_plot(pl=pl1, color="red")
    #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="blue", xlabel="Frequency (GHz)",
    #     ylabel="HWFM (GHz)")
    qdt.gate_type="capacitive"
    #co=qdt._get_coupling(f=frequency)/1.0/1e9
    line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl1, color="purple", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")
    qdt.gate_type="constant"
    line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl1, color="green", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")

    #co=(co+(idt.sinc(f=frequency)**2)*qdt._get_coupling(f=frequency)/1.0/1e9)/(1.0+(idt.sinc(f=frequency)**2))

    #line(frequency/1e9, co, plotter=pl, color="blue", xlabel="Frequency (GHz)",
    #     ylabel="HWFM (GHz)")

    dephasing=qdt.dephasing
    #deph_slope=qdt.dephasing_slope
    #qdt.dephasing=0.0
    #qdt.dephasing_slope=0.0
    #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="green")
    pl1.set_xlim(3.8, 6.05)
    pl1.set_ylim(-0.05, 1.15)
    pl1.add_label("c)")

    pl.nplot=2
    for d in lyzers:
        pl=d.widths_plot(pl=pl, color="red")
    qdt.dephasing=dephasing
    line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="blue", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")
    qdt.dephasing=0.0
    line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="green")
    pl.set_xlim(3.75, 6.1)
    pl.set_ylim(-0.01, 0.1)
    #pl.add_label("d)")
    if 0:
        pl="FFT_magabs"
        pl1="Fit_magabs"
        for d in lyzers:
            d.filter_type="Fit"
            pl1, pf=d.magabs_colormesh(pl=pl1, pf_too=True)#, cmap="nipy_spectral")
            d.filter_type="FFT"
            pl=d.magabs_colormesh(pl=pl, auto_zlim=False, vmin=pf.vmin, vmax=pf.vmax)#, cmap="nipy_spectral")
        pl.set_xlim(3.8, 6.05)
        pl.set_ylim(3.8, 6.05)
        pl.add_label("a)")
        pl1.set_xlim(3.8, 6.05)
        pl1.set_ylim(3.8, 6.05)
        pl1.add_label("b)")
        pls.append(pl)
        pls.append(pl1)

    b.read_data()

    b.filter_type="None"
    pl_raw=b.magabs_colormesh()
    b.bgsub_type="dB"
    b.magabs_colormesh()
    #pl1=colormesh(absolute(a.MagcomData[:, :, 30]))

    pl_ifft=b.ifft_plot()#.show()
    #a.pwr_ind=22

    b.filter_type="FFT"
    pl_fft=b.magabs_colormesh()#.show()
    b.bgsub_type="None"
    pl1=b.magdB_colormesh()
    pl2=b.magabs_colormesh()
    b.filter_type="Fit"
    b.magabs_colormesh(pl=pl2)
    b.magdB_colormesh(pl=pl1)
    pl.nplot=3
    pl_centers=b.center_plot(auto_xlim=False, x_min=3.75, x_max=5.1, auto_ylim=False, y_min=3.75, y_max=5.1,
                             xlabel="Frequency (GHz)", ylabel="Qubit Frequency (GHz)", pl=pl)
    line(array([3.5, 5.5]), array([3.5, 5.5]), pl=pl_centers, color="green")
    pl.nplot=4
    pl_widths=b.widths_plot(auto_xlim=False, x_min=3.75, x_max=5.1, auto_ylim=False, y_min=0.1, y_max=0.6,
                            xlabel="Frequency (GHz)", ylabel="$\Gamma/2\pi$ (GHz)", pl=pl)#.show()


    return pl

if __name__=="__main__":
    pl=combo_plots()
    a.save_plots([pl])

    pl.show()

