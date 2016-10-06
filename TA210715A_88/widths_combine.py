# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:36:21 2016

@author: thomasaref
"""

from D0514_highfrq1sidelobe import a as d0514
from D0316_S4A1_coupling_midpeak import a as d0316
from D0629_fft_try import a as d0629
from D0629_wide_gate_fluxswp import a as d0629wg
from D0506_lowfrq34sidelobe import a as d0506
from D0509_lowfrq2sidelobe import a as d0509
from D0503_lowfrq1sidelobe import a as d0503
from D0518_highfrq3sidelobe import a as d0518

from numpy import sqrt, linspace, absolute
from atom.api import FloatRange
from taref.plotter.fitter import LineFitter2
from taref.plotter.api import line, colormesh
from taref.core.api import tag_property

from TA88_fundamental import qdt, TA88_Lyzer, idt

a=TA88_Lyzer( name="combined",
             desc="combined data",
             )
a.save_folder.main_dir=a.name

lyzers=[d0514, d0316, d0629, d0518, d0506, d0509, d0503#, d0629wg,
]

def theory_Splot():
    frequency=linspace(3.8e9, 6.05e9, 1000)
    fq=linspace(3.8e9, 6.05e9, 1000)


    L=qdt._get_L(fq=fq)

    S11_arr=[]
    S33_arr=[]
    for f in frequency:
        (S11, S12, S13,
         S21, S22, S23,
         S31, S32, S33)=qdt._get_simple_S_qdt(f=f, L=L)
        S11_arr.append(S11)
        S33_arr.append(sqrt(1-absolute(S11)**2))

if __name__=="__main2__":
    colormesh(frequency, fq, absolute(S11_arr))
    colormesh(frequency, fq, absolute(S33_arr)).show()

def combo_plots():
    pls=[]
    for d in lyzers:
        d.filter_type="FFT"
        d.bgsub_type="dB"
        d.show_quick_fit=False
        d.read_data()


    pl="combined_centers"
    for d in lyzers:
        pl=d.center_plot(pl=pl, color="red")
    frequency=linspace(3.8e9, 6.05e9, 1000)
    V=qdt._get_fq0(f=frequency)#[1]
    #line(frequency/1e9, V/1e9, pl=pl,  ylabel="Qubit frequency (GHz)", xlabel="Frequency (GHz)")
    line(frequency/1e9, frequency/1e9-qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="purple", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")
    qdt.gate_type="constant"
    line(frequency/1e9, frequency/1e9-qdt._get_Lamb_shift(f=frequency)/1.0/1e9, plotter=pl, color="green", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")

    pl.set_xlim(3.8, 6.05)
    pl.set_ylim(3.8, 6.05)
    pl.add_label("a)")
    pls.append(pl)

    pl="combined_heights"
    for d in lyzers:
        pl=d.heights_plot(pl=pl)
    pl.yscale="log"
    pl.xlabel="Frequency (GHz)"
    pl.ylabel="Lorentzian height (a.u.)"
    pl.set_xlim(3.8, 6.05)
    pl.set_ylim(1e-8, 1e-3)
    pl.add_label("b)")
    pls.append(pl)

    pl="combined_backgrounds"
    for d in lyzers:
        pl=d.background_plot(pl=pl)

    pl="combined_widths"
    for d in lyzers:
        pl=d.widths_plot(pl=pl, color="red")
    #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="blue", xlabel="Frequency (GHz)",
    #     ylabel="HWFM (GHz)")
    qdt.gate_type="capacitive"
    co=qdt._get_coupling(f=frequency)/1.0/1e9
    line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="purple", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")
    qdt.gate_type="constant"
    line(frequency/1e9, qdt._get_coupling(f=frequency)/1.0/1e9, plotter=pl, color="green", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")

    co=(co+(idt.sinc(f=frequency)**2)*qdt._get_coupling(f=frequency)/1.0/1e9)/(1.0+(idt.sinc(f=frequency)**2))

    #line(frequency/1e9, co, plotter=pl, color="blue", xlabel="Frequency (GHz)",
    #     ylabel="HWFM (GHz)")

    dephasing=qdt.dephasing
    qdt.dephasing=0.0
    #line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="green")
    pl.set_xlim(3.8, 6.05)
    pl.set_ylim(-0.05, 1.15)
    pl.add_label("c)")
    pls.append(pl)

    pl="combined_widths_zoom"
    for d in lyzers:
        pl=d.widths_plot(pl=pl, color="red")
    qdt.dephasing=dephasing
    line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="blue", xlabel="Frequency (GHz)",
         ylabel="HWFM (GHz)")
    qdt.dephasing=0.0
    line(frequency/1e9, qdt._get_fFWHM(f=frequency)[2]/2.0/1e9, plotter=pl, color="green")
    pl.set_xlim(3.8, 6.05)
    pl.set_ylim(-0.05, 0.15)
    pl.add_label("d)")
    pls.append(pl)
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

#
#    pl="Fit magabs"
#    for d in lyzers:
#        d.filter_type="Fit"
#        pl=d.magdB_colormesh(pl=pl)#, auto_zlim=False, vmin=0.5, vmax=1.02, cmap="nipy_spectral")
#    pl.set_xlim(3.8, 6.05)
#    pl.set_ylim(3.8, 6.05)
#    pls.append(pl)
    return pls

if __name__=="__main__":
    pls=combo_plots()
    #a.save_plots(pls)

    pls[0].show()

