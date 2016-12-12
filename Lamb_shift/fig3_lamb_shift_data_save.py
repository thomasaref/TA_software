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
from D0523_mainlobe import a as d0523
from numpy import array, linspace, absolute
from taref.plotter.api import line, colormesh, scatter

from TA88_fundamental import qdt, TA88_Lyzer
from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read, TA53_Save_NP, TA53_Read_NP


a=TA88_Lyzer( name="combo",
             desc="combined data",
             )
a.save_folder.main_dir="fig3_ls"

lyzers=[d0514, d0523, d0629, d0518, d0506, d0509, d0503#d0316, d0629wg,
]

b=TA53_VNA_Pwr_Lyzer(name="d1118", on_res_ind=301,
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
b.filt.center=0 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
b.filt.halfwidth=100 #8 #10
b.fitter.gamma=0.035 #0.3
b.flux_axis_type="yoko" #"fq" #
b.end_skip=10
#a.flux_indices=[range(len(a.yoko)-1)]
b.pwr_ind=1


def combo_plots():
    pl="fig3"

    if 1:
        for d in lyzers:
            d.filter_type="FFT"
            #d.bgsub_type="dB"
            d.show_quick_fit=False
            d.flux_axis_type="yoko"
            d.read_data()
        plcTA88="centers_TA88"
        for d in lyzers:
            plcTA88=d.center_plot(pl=plcTA88, color="red", nrows=1, ncols=1, auto_xlim=False, auto_ylim=False)
        frequency=linspace(3.8e9, 6.05e9, 1000)
        #V=qdt._get_fq0(f=frequency)#[1]
        #line(frequency/1e9, V/1e9, pl=pl,  ylabel="Qubit frequency (GHz)", xlabel="Frequency (GHz)")
        #line(frequency/1e9, frequency/1e9-qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="purple", xlabel="Frequency (GHz)",
        #     ylabel="HWFM (GHz)")
        qdt.gate_type="constant"
        pl=line(frequency/1e9, frequency/1e9-qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="blue")
        line(array([3.75, 6.1]), array([3.75, 6.1]), pl=pl, color="green")

        pl.set_xlim(3.75, 6.1)
        pl.set_ylim(3.75, 6.1)
        #pl.add_label("a)")
        pl.axes.set_xlabel("Frequency (GHz)")
        pl.axes.set_ylabel("Qubit Frequency (GHz)")

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
        #qdt.gate_type="capacitive"
        #co=qdt._get_coupling(f=frequency)/1.0/1e9
        #line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl1, color="purple")
        qdt.gate_type="constant"
        line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl1, color="green")

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

        #pl.nplot=2
        plwTA88="widths_TA88"
        for d in lyzers:
            plwTA88=d.widths_plot(pl=plwTA88, color="red")
        #qdt.dephasing=dephasing
        #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="blue")
        qdt.gate_type="capacitive"
        #co=qdt._get_coupling(f=frequency)/1.0/1e9
        line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="blue")
        qdt.gate_type="constant"
        line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="green")

        #qdt.dephasing=0.0
        #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="green")
        pl.set_xlim(3.75, 6.1)
        pl.set_ylim(-0.01, 0.1)
        #pl.add_label("d)")
        pl.axes.set_xlabel("Frequency (GHz)")
        pl.axes.set_ylabel("$\Gamma/2\pi$ (GHz)")


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
    b.show_quick_fit=False
    #pl_raw=b.magabs_colormesh()
    #b.bgsub_type="dB"
    #b.magabs_colormesh()
    #pl1=colormesh(absolute(a.MagcomData[:, :, 30]))

    #pl_ifft=b.ifft_plot()#.show()
    #a.pwr_ind=22

    b.filter_type="FFT"
    #pl_fft=b.magabs_colormesh()#.show()
    b.bgsub_type="None"
    #pl1=b.magdB_colormesh()
    #pl2=b.magabs_colormesh()
    b.filter_type="Fit"
    #b.magabs_colormesh(pl=pl2)
    #b.magdB_colormesh(pl=pl1)
    #pl.nplot=3
    plcTA53="centers_TA53"
    plcTA53=b.center_plot(color="red", auto_xlim=False, x_min=3.75, x_max=5.1,
                             auto_ylim=False, y_min=3.75, y_max=5.1, pl=plcTA53, nrows=1, ncols=1, nplot=1)

    #pl.nplot=4
    plwTA53="widths_TA53"
    plwTA53=b.widths_plot(color="red", auto_xlim=False, x_min=3.75, x_max=5.1,
                            auto_ylim=False, y_min=0.1, y_max=0.6, pl=plwTA53)#.show()

    #pl.nplot=3

    b.pwr_ind=0
    b.fit_indices=[ range(7, 42), range(79, 120), range(171, 209), range(238, 291), #range(558, 603),
                   range(629, 681),
                   range(715, 764), range(803, 835),
                     range(879, 915), range(953, 960), range(963, 985)]

    b.get_member("fit_params").reset(b)
    b.get_member("MagcomFilt").reset(b)
    b.fitter.fit_params=None
    pl_centers=b.center_plot(color="red", auto_xlim=False, x_min=3.75, x_max=5.1,
                             auto_ylim=False, y_min=3.75, y_max=5.1, pl=plcTA53)

    b.qdt.gate_type="constant"
    frequency=linspace(3.5e9, 5.5e9, 1000)
    line(frequency/1e9, frequency/1e9-b.qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="blue")
    line(array([3.5, 5.5]), array([3.5, 5.5]), pl=pl, color="green")
    pl.axes.set_xlabel("Frequency (GHz)")
    pl.axes.set_ylabel("Qubit Frequency (GHz)")
    #pl.nplot=4
    pl_widths=b.widths_plot(color="red", auto_xlim=False, x_min=3.75, x_max=5.1,
                            auto_ylim=False, y_min=0.1, y_max=0.6, pl=plwTA53)#.show()
    #qdt.gate_type="constant"
    b.qdt.gate_type="capacitive"
        #co=qdt._get_coupling(f=frequency)/1.0/1e9
    line(frequency/1e9, b.qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl1, color="blue")
    b.qdt.gate_type="constant"
    line(frequency/1e9, b.qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl1, color="green")

    #line(frequency/1e9, b.qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="green")

    pl.axes.set_xlabel("Frequency (GHz)")
    pl.axes.set_ylabel("$\Gamma/2\pi$ (GHz)")
    #pl.figure.text(0.0, 0.95, "a)")
    #pl.figure.text(0.0, 0.45, "b)")
    #pl.figure.text(0.5, 0.95, "c)")
    #pl.figure.text(0.5, 0.45, "d)")

    #pl.figure.tight_layout()
    return plcTA88, plwTA88, plcTA53, plwTA53

if __name__=="__main__":
    plcTA88, plwTA88, plcTA53, plwTA53=combo_plots()
    #a.save_plots([pl])
if __name__=="__main__":
    nps=TA53_Save_NP()
    nps.folder.main_dir="fig3_ls"

    names={"centers_TA88" : plcTA88,
           "widths_TA88"  : plwTA88,
           "centers_TA53" : plcTA53,
           "widths_TA53"  : plwTA53}

    for name in names:
        nps.file_name=name
        nps.save(names[name].savedata())
        npr=TA53_Read_NP(file_path=nps.file_path, show_data_str=True)
        data=npr.read()
        scatter(data[:, 0], data[:, 1])
    #nps.data_buffer=pl1.savedata()
    #pl1.show(nps, npr)
    plwTA53.show()

