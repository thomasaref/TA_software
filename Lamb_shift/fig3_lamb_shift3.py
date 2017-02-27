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

from numpy import array, linspace, absolute, sqrt
from taref.plotter.api import line, colormesh, scatter

from taref.core.api import process_kwargs

from TA88_fundamental import qdt, TA88_Lyzer, TA88_VNA_Lyzer, TA88_Read
from TA53_fundamental import TA53_VNA_Pwr_Lyzer, TA53_Read

colormesh(qdt.MagAbs)

a=TA88_Lyzer( name="combo",
             desc="combined data",
             )
a.save_folder.main_dir="fig3_ls3"

lyzers=[d0514, d0316, d0629, d0518, d0506, d0509, d0503#, d0629wg,
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
b.fitter.gamma=0.3/10 #0.035
b.flux_axis_type="fq" #"flux"#"fq" #
b.end_skip=10
#a.flux_indices=[range(len(a.yoko)-1)]
b.pwr_ind=1

def center_plot(self, **kwargs):
    process_kwargs(self, kwargs, pl="center_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))

    pl=scatter(self.freq_axis[self.flat_indices], -(array([fp[1] for fp in self.fit_params])-self.freq_axis[self.flat_indices]), **kwargs)

    #pl=scatter(self.freq_axis[self.flat_indices], array([fp[1] for fp in self.fit_params]), **kwargs)

    #    if self.show_quick_fit:

    #        if self.flux_axis_type=="fq":
    #            line(self.freq_axis[self.indices], self.ls_f[self.indices]/1e9, plotter=pl, color="red", linewidth=1.0)
    #        elif self.flux_axis_type=="yoko":
    #            line(self.freq_axis[self.indices], self.qdt._get_Vfq0(f=self.frequency[self.indices]), plotter=pl, color="red", linewidth=1.0)
    #        else:
    #            line(self.freq_axis, self.qdt._get_fluxfq0(f=self.frequency), plotter=pl, color="red", linewidth=1.0)
    #        if self.fitter.p_guess is not None:
    #            line(self.freq_axis[self.indices], array([pg[1] for pg in self.fitter.p_guess]), pl=pl, color="green", linewidth=1.0) #self.voltage_from_frequency(self.qdt._get_coupling(self.frequency)), plotter=pl, color="red")
    return pl

def combo_plots():
    pl="fig3"

    if 1:
        for d in lyzers:
            d.filter_type="FFT"
            #d.bgsub_type="dB"
            d.show_quick_fit=False
            d.flux_axis_type="fq" #"flux"
            #d.fitter.gamma=d.fitter.gamma/10
            d.read_data()
        for d in lyzers:
            pl=center_plot(d, pl=pl, color="red", nrows=1, ncols=3, nplot=2, fig_width=7.3, fig_height=2.5,
                           auto_xlim=False, auto_ylim=False)

            #pl=d.center_plot(pl=pl, color="red", nrows=2, ncols=2, auto_xlim=False, auto_ylim=False)
        frequency=linspace(3.5e9, 6.5e9, 1000)
        qdt.gate_type="constant"

        line(frequency/1e9, qdt._get_Lamb_shift(f=frequency)/1.0/1e9, color="red", pl=pl)
        #V=qdt._get_fq0(f=frequency)#[1]
        #line(frequency/1e9, V/1e9, pl=pl,  ylabel="Qubit frequency (GHz)", xlabel="Frequency (GHz)")
        #line(frequency/1e9, frequency/1e9-qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="purple", xlabel="Frequency (GHz)",
        #     ylabel="HWFM (GHz)")
        qdt.gate_type="constant"
        #line(qdt._get_fluxfq0(f=frequency), frequency/1e9, plotter=pl, color="red")

        #line(frequency/1e9, frequency/1e9-qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="blue")
        line(array([3.5, 6.5]), array([-1.5, 1.5])-0.3, pl=pl, color="green", linestyle="dashed")

        #pl.set_xlim(3.75, 6.1)
        pl.set_xlim(3.5, 6.5)

        pl.set_ylim(-1, 1.5)

        #pl.set_ylim(3.75, 6.1)
        #pl.add_label("a)")
        pl.axes.set_xlabel("Frequency (GHz)")
        pl.axes.set_ylabel("$\Delta/2\pi, \, \Gamma/2 \pi$ (GHz)")
        #pl.show()
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
            pl1=d.widths_plot(pl=pl, color="black", facecolor="black", edgecolor="black",)
        #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="blue", xlabel="Frequency (GHz)",
        #     ylabel="HWFM (GHz)")
        #qdt.gate_type="capacitive"
        #co=qdt._get_coupling(f=frequency)/1.0/1e9
        #line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl1, color="purple")
        qdt.gate_type="capacitive"
        #co=qdt._get_coupling(f=frequency)/1.0/1e9
        #line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="purple")
        #qdt.gate_type="constant"
        line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl,
             color="purple")


        #co=(co+(idt.sinc(f=frequency)**2)*qdt._get_coupling(f=frequency)/1.0/1e9)/(1.0+(idt.sinc(f=frequency)**2))

        #line(frequency/1e9, co, plotter=pl, color="blue", xlabel="Frequency (GHz)",
        #     ylabel="HWFM (GHz)")

        dephasing=qdt.dephasing
        #deph_slope=qdt.dephasing_slope
        #qdt.dephasing=0.0
        #qdt.dephasing_slope=0.0
        #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="green")
        #pl1.set_xlim(3.8, 6.05)
        #pl1.set_ylim(-0.05, 1.15)
        #pl1.add_label("c)")

        pl.nplot=3
        for d in lyzers:
            pl=d.widths_plot(pl=pl, color="black", facecolor="black", edgecolor="black",)
        #qdt.dephasing=dephasing
        #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="blue")
        qdt.gate_type="capacitive"
        #co=qdt._get_coupling(f=frequency)/1.0/1e9
        #line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="purple")
        #qdt.gate_type="constant"
        line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl,
             color="purple")

        #qdt.dephasing=0.0
        #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="green")
        pl.set_xlim(3.75, 6.1)
        pl.set_ylim(-0.01, 0.1)
        #pl.add_label("d)")
        pl.axes.set_xlabel("Frequency (GHz)")
        pl.axes.set_ylabel("$\Gamma/2\pi$ (GHz) ")


        pl.nplot=1
        if 0:
            pl2="FFT_magabs"
            pl1="Fit_magabs"
            f=d.frequency
            from numpy import pi
            f=linspace(3e9, 8e9, 501)
            fqq=linspace(2e9, 9e9, 2001)
            magcom=array([qdt._get_simple_S(f=f, YL=-1.0j/f*qdt.Ct*2*pi*fq**2) for fq in fqq])[:, 0, :]

            pl=colormesh(fqq/1e9, f/1e9, 1-absolute(magcom).transpose(),  pl=pl)
            for d in lyzers:
                d.filter_type="Fit"
                pl1, pf=d.magabs_colormesh(pl=pl1, pf_too=True)#, cmap="nipy_spectral")
                d.bgsub_type="dB"
                d.filter_type="FFT"
                pl2=d.magdB_colormesh(pl=pl2, auto_zlim=False, vmin=-3.0, vmax=0.0)#, cmap="nipy_spectral")
                new_fp=[[fp[0], fp[1], 1.0, 0.0] for fp in d.fit_params]
                new_magabs=sqrt(d.fitter.reconstruct_fit(d.flux_axis[d.flat_flux_indices], new_fp))

                #process_kwargs(self, kwargs, pl="magabs_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
                flux_axis=d.flux_axis[d.flat_flux_indices]
                #freq_axis=d.freq_axis[d.indices]
                start_ind=0
                for ind in d.fit_indices:
                    pl=colormesh(flux_axis, d.freq_axis[ind], new_magabs[start_ind:start_ind+len(ind), :],  pl=pl)
                    start_ind+=len(ind)


            pl.set_xlim(3.8, 6.05)
            pl.set_ylim(3.8, 6.05)
            pl2.set_xlim(3.8, 6.05)
            pl2.set_ylim(3.8, 6.05)
            pl2.add_label("a)")
            pl1.set_xlim(3.8, 6.05)
            pl1.set_ylim(3.8, 6.05)
            pl1.add_label("b)")
            #pls.append(pl)
            #pls.append(pl1)

    def MagAbsFit(self):
        return sqrt(self.fitter.reconstruct_fit(self.flux_axis[self.flat_flux_indices], self.fit_params))

    def magabs_colormesh(self, **kwargs):
        flux_axis=self.flux_axis[self.flat_flux_indices]
        freq_axis=self.freq_axis[self.indices]
        start_ind=0
        for ind in self.fit_indices:
            pl=colormesh(flux_axis, self.freq_axis[ind], self.MagAbs[start_ind:start_ind+len(ind), :],  **kwargs)
            start_ind+=len(ind)


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
    #pl=center_plot(b, color="red", auto_xlim=False, x_min=3.75, x_max=5.1,
    #                         auto_ylim=False, y_min=3.75, y_max=5.1, pl=pl, nrows=1, ncols=3, nplot=3)
    b.qdt.gate_type="constant"
    b.qdt.K2=0.032

    line(frequency/1e9, b.qdt._get_Lamb_shift(f=frequency)/1.0/1e9, color="red", pl=pl)
    line(array([3.5, 6.5]), array([-1.5, 1.5])+0.5, pl=pl, color="green", linestyle="dashed")


    #pl=b.center_plot(color="red", auto_xlim=False, x_min=3.75, x_max=5.1,
    #                         auto_ylim=False, y_min=3.75, y_max=5.1, pl=pl, nrows=2, ncols=2, nplot=3)

    #pl.nplot=4
    pl_widths=b.widths_plot(color="black", facecolor="black", edgecolor="black", auto_xlim=False, x_min=3.5, x_max=5.5,
                            auto_ylim=False, y_min=-0.5, y_max=0.5, pl=pl)#.show()

    #pl.nplot=1

    b.pwr_ind=0
    b.fit_indices=[ range(7, 42), range(79, 120), range(171, 209), range(238, 291), #range(558, 603),
                   range(629, 681),
                   range(715, 764), range(803, 835),
                     range(879, 915), range(953, 960), range(963, 985)]

    b.get_member("fit_params").reset(b)
    b.get_member("MagcomFilt").reset(b)
    b.fitter.fit_params=None
    pl_centers=center_plot(b, color="red", auto_xlim=False, x_min=3.5, x_max=5.5,
                             auto_ylim=False, y_min=-0.3, y_max=0.3, pl=pl)

    #pl_centers=b.center_plot(color="red", auto_xlim=False, x_min=3.75, x_max=5.1,
    #                         auto_ylim=False, y_min=3.75, y_max=5.1, pl=pl)

    b.qdt.gate_type="constant"
    frequency=linspace(3.5e9, 5.5e9, 1000)
    line(frequency/1e9, frequency/1e9-b.qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="blue")
    line(array([3.5, 5.5]), array([3.5, 5.5]), pl=pl_centers, color="green")
    #pl.axes.set_xlabel("Frequency (GHz)")
    #pl.axes.set_ylabel("Qubit Frequency (GHz)")
    #pl.nplot=4
    pl_widths=b.widths_plot(color="black", facecolor="black", edgecolor="black", auto_xlim=False, x_min=3.5, x_max=5.5,
                            auto_ylim=False, y_min=-0.3, y_max=0.5, pl=pl)#.show()
    #qdt.gate_type="constant"
    b.qdt.gate_type="capacitive"
    #b.qdt.gate_type="constant"
        #co=qdt._get_coupling(f=frequency)/1.0/1e9
    line(frequency/1e9, b.qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="purple")
    #b.qdt.gate_type="constant"
    #line(frequency/1e9, b.qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="green")

    #line(frequency/1e9, b.qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="green")

    pl.axes.set_xlabel("Frequency (GHz)")
    pl.axes.set_ylabel("$\Delta/2\pi, \, \Gamma/2 \pi$ (GHz)")
    pl.figure.text(0.0, 0.95, "a)")
    pl.figure.text(0.0, 0.45, "b)")
    pl.figure.text(0.5, 0.95, "c)")
    pl.figure.text(0.5, 0.45, "d)")

#    pl.nplot=4
#
#    c=TA88_VNA_Lyzer(on_res_ind=215,# VNA_name="RS VNA", filt_center=15, filt_halfwidth=15,
#        rd_hdf=TA88_Read(main_file="Data_0704/S4A4_gate_flux_swp.hdf5"))
#
#    c.filt.center=40#0 #107
#    c.filt.halfwidth=60
#    #a.fitter.fit_type="lorentzian"
#    #a.fitter.gamma=0.01
#    c.flux_axis_type="flux"#"yoko"#
#    c.end_skip=10
#    c.read_data()
#    #a.ifft_plot()
#
#    c.bgsub_type="dB"
#    #a.bgsub_type="Complex"
#    c.filter_type="FFT"
#    line(c.freq_axis[c.indices], c.MagAbs[:, 222], pl=pl,
#                             auto_xlim=False, y_min=0.96, y_max=1.02,
#                             auto_ylim=False, x_min=3.5, x_max=7.5)
    #c.magabs_colormesh(vmin=0.987, vmax=1.00, cmap="afmhot",
    #                   auto_zlim=False, pl=pl,
    #                   auto_xlim=False, x_min=0.0, x_max=1.5,
    #                   auto_ylim=False, y_min=3.5, y_max=7.5)#.show()


    pl.figure.tight_layout()
    return pl

if __name__=="__main__":
    pl=combo_plots()
    a.save_plots([pl])

    pl.show()

