# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:33:17 2016

@author: thomasaref
"""

from taref.tex.tex import TEX
from taref.core.shower import shower
from TA88_fundamental import qdt, idt, ideal_qdt, ideal_idt
from taref.filer.read_file import Read_TXT

tx=TEX(source_path=r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/Lamb_shift_paper_source.tex")
#"/Users/thomasaref/Dropbox/Current stuff/test_data/source/TA210715A88_source/TA210715A88_writeup.tex")
tx.save_file.file_name="Lamb_shift_paper"
print tx.source_folder.dir_path
tx.tex_type="revtex 2 column"
#tx.locals_dict=dict(idt=idt, qdt=qdt)
#sample holder 12
include_all=False #True
include_text=False #True

def fft_plots(a, desc=None, label="None", caption="None"):
    if desc is None:
        desc=a.desc
    file_names=Read_TXT(file_path=a.save_file.file_path).read()
    tx.mult_fig_start()
    for fn in file_names:
        if fn!="":
            tx.add_mult_image(fn, label, caption, a.save_folder)
    tx.mult_fig_end(caption=desc+r" \\a) raw VNA data b) IFFT showing filter c) FFT filtered data d) Lorentzian fits with same scale as (c)")


tx.TEX_start()

if 1:
    tx.ext("abstract")
    tx.ext("introduction")
    tx.ext("experiment")
if 1:
    tx.include_image("fig1.png", "Setup", caption="sample caption")
if 1:
    from fig2_characterization2 import a as fig2
    tx.include_image("fig2", label="", caption="fig2 caption", source_folder=fig2.save_folder)

if 1:
    from fig3_lamb_shift2 import a as fig3
    tx.include_image("fig3", label="", caption="fig3 caption", source_folder=fig3.save_folder)

    from fig4_flux_swp import a as fig4
    tx.include_image("fig4", label="", caption="fig4 caption", source_folder=fig4.save_folder)

    tx.ext("results")
    tx.ext("theory")
    #tx.ext("supplementary")
    #tx.add(r"\FloatBarrier")
    tx.ext("discussion")

    tx.ext("conclusion")

    tx.add(r"\bibliographystyle{unsrt}")
    tx.add(r"\bibliography{lamb_shift_bib}")



if 0:
    tx.include_image("sample_images", label="sample_images",
        caption="sample caption")

    #tx.add(r"\FloatBarrier")
    from TA88_flux_parabola import a as fp #flux_plots
    file_names=Read_TXT(file_path=fp.save_file.file_path).read()

    #tx.add_mult_figs(flux_plots)
    #tx.mult_fig_end(caption = r"a) flux parabola with fit parameters b) flux parabola with design parameters c) transpose of (a) d) transpose of (b)")
    #tx.add(r"\FloatBarrier")

    tx.mult_fig_start()

    #tx.add_mult_image("fluxmap", "fluxmap", include_caption=True)
    tx.add_mult_image("fluxmap_w_peaks", "fluxmap_w_peaks", include_caption=True)
    tx.add_mult_image("fitfvsV", "fitfvsV", "", fp.save_folder)

    #tx.add_mult_image("fit_fluxmap", "fit_fluxmap", include_caption=True)
    #tx.add_mult_image("just_peaks", "just_peaks", include_caption=True)
    tx.mult_fig_end(caption=r"a) flux vs frequency colormap with peak locations as cyan points b) flux parabola fit to extracted peak locations")


    tx.ext("results")

    from D0316_S4A1_coupling_midpeak import a as d0316

    fft_plots(d0316)

    from TA88_widths_combine import a as wc
    from D1118b_trans_wide import a as d1118
    file_names=Read_TXT(file_path=wc.save_file.file_path).read()

    tx.mult_fig_start()
    tx.add_mult_image("FFT_magabs", "FFT_magabs", "", wc.save_folder, include_caption=False)
    tx.add_mult_image("Fit_magabs", "Fit_magabs", "", wc.save_folder, include_caption=False)
    tx.add_mult_image("combined_centers", "combined_centers", "", wc.save_folder, include_caption=False)
    tx.add_mult_image("combined_widths_zoom", "combined_widths_zoom", "", wc.save_folder, include_caption=False)
    tx.add_mult_image("center_Fit_None_d1118", "", "", d1118.save_folder)
    tx.add_mult_image("widths_Fit_None_d1118", "", "", d1118.save_folder)
    tx.mult_fig_end(caption="widths caption")


    tx.ext("theory")
    #tx.ext("supplementary")
    tx.add(r"\FloatBarrier")
if 0:
    from D1112_trans_pwr import a as d1112
    tx.mult_fig_start()
    tx.add_mult_image("plot__10", "pwr_TA53", "", d1112.save_folder)
    tx.add_mult_image("plot__11", "", "", d1112.save_folder)
    tx.mult_fig_end()
if 0:
    tx.include_image("testy_circuit_draw.png", "Anharmonicity", "anharm")
    #tx.add_mult_fig(anton_anharm_plot, "anton_anharm_plot.pdf", fig_width=6.0, fig_height=4.0)
    #tx.add_mult_image("anton_lamb_shift.png", "Lamb shift", "anharm")
    #tx.add_mult_fig(anton_lamb_shift_plot, "anton_lamb_shift_plot.pdf", fig_width=6.0, fig_height=4.0)
    #tx.mult_fig_end(caption="Comparison to Anton's plots")

    #tx.mult_fig_start()
    #tx.add_mult_fig(energy_level_plot, "energy_levels.pdf", qdt=qdt, fig_width=6.0, fig_height=4.0)
    #tx.add_mult_fig(anharm_plot, "theory_anharm.pdf", qdt=qdt, fig_width=6.0, fig_height=4.0)
if include_text:
    #tx.add(r"\FloatBarrier")
    tx.ext("switch")
    tx.add(r"\FloatBarrier")

if include_all:
    tx.add(r"\subsection{Wiring details}")
    tx.include_image("fridgewiring.png", "Fridge Wiring", "fridgewiring")
    tx.include_image("switchwiring", "Switch Wiring", "switchwiring")
    #tx.add(r"\FloatBarrier")

if include_text:
    tx.add(r"\FloatBarrier")
    tx.ext("sample")

if include_all:
    tx.include_image("sample_images", label="sample_images",
        caption="""Images of sister sample. There are two talking listening IDTs located 200 um and 300 um respectively from the QDT.
        The talking listening IDTs have finger widths 96 nm. The QDT has finger widths 80 nm. The SQUID is connected in a separate lithography step.""")


if include_text:
    tx.add(r"\FloatBarrier")
    tx.add(r"\section{Qubit parameters}")
    tx.add("""These tables show values taken from the numerical models for fitting.
    The first column is an expression or name for the quantity, the label column has more information when appropriate,
    the value column has the value used in fitting, the design column has the ideal value used in design, and the comment column contains extra information.""")

    tx.add(r"\subsection{Qubit material values}")
    tx.make_table(qdt.latex_table(['material', 'vf', 'Dvv', 'K2',  'epsinf', 'superconductor', 'Delta', 'Tc',], design=ideal_qdt),
                                   r"|p{3.5 cm}|p{3 cm}|p{3 cm}|p{3 cm}|p{3.5 cm}|")

    tx.add(r"\subsection{QDT IDT properties}")
    tx.make_table(qdt.latex_table(['ft', 'ft_mult', 'Np', 'N_IDT', 'Ct_mult', 'W', 'Ct', 'eta',
                                   'a', 'g', 'f0', 'lbda0', 'k0', 'p', 'L_IDT', 'Y0'], design=ideal_qdt),
                                   r"|p{3.5 cm}|p{3 cm}|p{3 cm}|p{3 cm}|p{3.5 cm}|")

    tx.add(r"\subsection{QDT Qubit  properties}")
    tx.make_table(qdt.latex_table([ 'fq_approx_max','fq_max',  'Ejmax',  'Ec', 'EjmaxdivEc',  'Ic','Rn', 'flux_factor', 'offset',
    'loop_height', "loop_width", "loop_area",
    ], design=ideal_qdt),
                                   r"|p{3.5 cm}|p{3 cm}|p{3 cm}|p{3 cm}|p{3.5 cm}|")

    tx.add(r"\subsection{QDT working frequency}")
    tx.make_table(qdt.latex_table(['f', 'lbda', 'k', 'X', 'Ej','EjdivEc', 'anharm','fq_approx','fq','fq2','voltage', 'flux_over_flux0','L'], design=ideal_qdt),
                                   r"|p{3.5 cm}|p{3 cm}|p{3 cm}|p{3 cm}|p{3.5 cm}|")


    tx.add(r"\subsection{QDT coupling}")
    tx.make_table(qdt.latex_table(['couple_mult','couple_factor', 'couple_factor0','coupling','Lamb_shift', 'Ga0_mult', 'Ga0', 'Ga', 'Ba'], design=ideal_qdt),
                                   r"|p{3.5 cm}|p{3 cm}|p{3 cm}|p{3 cm}|p{3.5 cm}|")

    tx.add(r"\subsection{extra IDT properties}")
    tx.make_table(qdt.latex_table(['couple_type','Lamb_shift_type', 'S_type', 'alpha0', 'alpha', 'fs',  'm', 's', 'YL',  'rs', 'ts', 'dloss1', 'dloss2', 'dL',  'Gs', 'N_fixed', 'fixed_freq_min', 'fixed_freq_max'], design=ideal_qdt),
                                   r"|p{3.5 cm}|p{3 cm}|p{3 cm}|p{3 cm}|p{3.5 cm}|")
    tx.add(r"\FloatBarrier")

if include_text:
    tx.ext("flux fitting")

if include_all:
    tx.add(r"\FloatBarrier")

    tx.mult_fig_start()
    tx.add_mult_image("fluxmap", "fluxmap", include_caption=True)
    tx.add_mult_image("fluxmap_w_peaks", "fluxmap_w_peaks", include_caption=True)
    tx.add_mult_image("fit_fluxmap", "fit_fluxmap", include_caption=True)
    tx.add_mult_image("just_peaks", "just_peaks", include_caption=True)
    tx.mult_fig_end(caption=r"a) raw flux vs frequency colormap b) flux vs frequency colormap with peak locations as cyan points c) Lorentzian fits of flux map d) peak locations with flux parabola fitting flux periodicity")

if include_all:
    from flux_parabola import a as fp #flux_plots
    file_names=Read_TXT(file_path=fp.save_file.file_path).read()

    tx.mult_fig_start()
    for fn in file_names:
        if fn!="":
            tx.add_mult_image(fn, fn, "", fp.save_folder)
    #tx.add_mult_figs(flux_plots)
    tx.mult_fig_end(caption = r"a) flux parabola with fit parameters b) flux parabola with design parameters c) transpose of (a) d) transpose of (b)")
    tx.add(r"\FloatBarrier")

if include_text:
    tx.ext("widths fitting")

if include_all:
    tx.add(r"\FloatBarrier")
    from widths_combine import a as wc
    file_names=Read_TXT(file_path=wc.save_file.file_path).read()

    tx.mult_fig_start()
    for fn in file_names[0:4]:
        if fn!="":
            tx.add_mult_image(fn, fn, "", wc.save_folder)
    tx.mult_fig_end(caption=r"a) centers of Lorentzians b) heights of Lorentzians c) HWFM of Lorentzians d)zoom of HWFM of Lorentzians")

    tx.mult_fig_start()
    for fn in file_names[4:]:
        if fn!="":
            tx.add_mult_image(fn, fn, "", wc.save_folder)
    tx.mult_fig_end(caption=r"a) combined filtered data colormaps (arbitrary color scales) b) Lorentzians fits colormap (arbitrary colorscales)")
    tx.add(r"\FloatBarrier")

if include_text:
    tx.ext("FFT filtered")

if include_all:
    tx.add(r"\FloatBarrier")
    from D0506_lowfrq34sidelobe import a as d0506 #d0506_plots
    #tx.add_mult_figs(d0506_plots)
    from D0316_S4A1_coupling_midpeak import a as d0316
    from D0514_highfrq1sidelobe import a as d0514
    from D0509_lowfrq2sidelobe import a as d0509
    from D0503_lowfrq1sidelobe import a as d0503
    from D0518_highfrq3sidelobe import a as d0518

    #needs work
    from D0629_fft_try import a as d0629


    lyzers=[
    d0506,
     d0509,
     d0503,
     d0316,
      d0514,
      d0518,
      d0629,
     #, d0629wg,
    ]
    for lyz in lyzers:
        fft_plots(lyz)
    tx.add(r"\FloatBarrier")



#if include_all:
#    from taref.physics.qdt import energy_level_plot, anton_anharm_plot, anton_lamb_shift_plot, anharm_plot

    #tx.mult_fig_start()
    #tx.add_mult_image("Anton_anharm.png", "Anharmonicity", "anharm")
    #tx.add_mult_fig(anton_anharm_plot, "anton_anharm_plot.pdf", fig_width=6.0, fig_height=4.0)
    #tx.add_mult_image("anton_lamb_shift.png", "Lamb shift", "anharm")
    #tx.add_mult_fig(anton_lamb_shift_plot, "anton_lamb_shift_plot.pdf", fig_width=6.0, fig_height=4.0)
    #tx.mult_fig_end(caption="Comparison to Anton's plots")

    #tx.mult_fig_start()
    #tx.add_mult_fig(energy_level_plot, "energy_levels.pdf", qdt=qdt, fig_width=6.0, fig_height=4.0)
    #tx.add_mult_fig(anharm_plot, "theory_anharm.pdf", qdt=qdt, fig_width=6.0, fig_height=4.0)
    #tx.mult_fig_end(caption="Theory plots based on QDT parameters")

#from TA88_fundamental import a as fund
#file_names=Read_TXT(file_path=fund.save_file.file_path).read()

if include_text:
    #tx.ext("qubit model")
    tx.add(r"\FloatBarrier")
    tx.add(r"\section{Theory}")
    tx.ext("theory compare")

    tx.include_image(file_names[9], label=file_names[9],
    caption="""Comparison of coupling from different models""",
    source_folder=fund.save_folder)

    tx.include_image(file_names[10], label=file_names[10],
    caption="""Comparison of Lamb shift from different models""",
    source_folder=fund.save_folder)
    tx.add(r"\FloatBarrier")
    tx.ext("useful relations")
    tx.ext("giant atom theory")
    tx.add(r"\FloatBarrier")
    tx.ext("sum")

if include_all:
    tx.include_image(file_names[11], label=file_names[11],
    caption="""Numerical Hilbert transforms compared to analytical formulas""",
    source_folder=fund.save_folder)
    tx.add(r"\FloatBarrier")

if include_text:
    tx.ext("double finger")
    tx.ext("IDT model")
    tx.ext("PtoS")
    tx.ext("FWHM")
    tx.ext("semiclassical model")

    tx.ext("surface charge")
    tx.add(r"\FloatBarrier")
    tx.ext("Legendre")

if include_all:
    tx.include_image(file_names[0], label=file_names[0],
    caption="""The first 30 Legendre polynomials evaluated at $0$, $0.25$, $0.5$ and $0.75$ are plotted as points along with the series expansion, recurrence relation, interpolated result for the Legendre functions.""",
    source_folder=fund.save_folder)

if include_text:
    tx.add(r"\FloatBarrier")
    tx.ext("element factor")

if include_all:
    tx.mult_fig_start()
    for fn in file_names[1:3]:
        if fn!="":
            tx.add_mult_image(fn, fn, "", fund.save_folder, include_caption=True)
    tx.mult_fig_end(caption=r"a) Element factor for single and double finger vs normalized frequency b) metallization ratio effect on element factor vs normalized frequency")

    tx.add(r"\FloatBarrier")
    tx.ext("verify element")

    tx.mult_fig_start()
    for fn in file_names[3:7]:
        if fn!="":
            tx.add_mult_image(fn, fn, "", fund.save_folder, include_caption=True)
    tx.mult_fig_end(caption="""a) Element factor extended evaluation to higher frequencies.
    b) surface charge via inverse Fourier transform as a function of position.
    c) corresponding surface voltage as a function of position.
    d) superposition of surface voltages for a double finger and single finger.""")
    #e) metallization effect on coupling
    #f) metallization effect on Lamb shift""")

    tx.add(r"\FloatBarrier")

if include_text:
    tx.ext("sumRAMy")

    tx.ext("RAM")
    tx.ext("rs")
    tx.ext("PtoS proofs")
    tx.ext("TtoP")

tx.TEX_end()

#tx.make_tex_file()
#tx.compile_tex()
#tx.show()
#qdt.show()
tx.make_and_show()
#shower(tx)


#['flux_parabola',
# 'fq0',   'fluxfq0',  'GL',  'transmon_energy_levels',
# 'voltage_from_flux_par',  'Vfq0_many', 'n_energy',
#'VfFWHM',
# 'fFWHM',

# 'flux_from_fq',
# 'dephasing',
# 'fluxfFWHM',

#  'ng',
# 'EkdivEc',   'voltage_from_flux_par_many',    'Vfq0',   'Nstates',
# 'order']




#tx.make_table(ideal_qdt.latex_table(["ft", "Np", "ef", "W", "a", "Rn", "max_coupling", "coupling", "Ct", "loop_width", "loop_height"]), r"|p{4 cm}|p{4 cm}|p{4 cm}|p{4 cm}|p{4 cm}|")


#tx.make_table(ideal_qdt.latex_table(["f0", "Np", "Ic", "Ejmax", "Ct", "Ec", "EjmaxdivEc", "fq_max",
#                               "fq_approx_max", "flux_over_flux0", "loop_area", "Ej", "EjdivEc", "fq"]), r"|p{4 cm}|p{4 cm}|p{4 cm}|p{4 cm}|p{4 cm}|")

#tx.make_table(idt.latex_table(["material", "epsinf", "vf", "K2", "Dvv"]), r"|p{4 cm}|p{4 cm}|p{4 cm}|p{4 cm}|")

#qubit_values=[[r"QDT"                                    ,  r"Value"                            ],
#              [r"Finger type"                            ,  r"{0}".format(qdt.ft)               ],
#              [r"Number of finger pairs, $N_{pq}$"       ,  r"{0}".format(qdt.Np)               ],
#              [r"Overlap length, $W$"                    ,  r"{0} $\mu$m".format(qdt.W/1.0e-6)  ],
#              [r"finger width, $a_q$"                    ,  r"{0} nm".format(qdt.a/1.0e-9)      ],
#              [r"DC Junction Normal Resistance"          ,  r"{0} k$\Omega$".format(qdt.Rn)     ],
#              [r"Metallization ratio"                    ,  r"{0}\%".format(qdt.eta)            ],
#              [r"Coupling at IDT center frequency"""     ,  r"{0} GHz".format(qdt.G_f0/1.0e9)   ],
#              [r"Coupling adjusted by $sinc^2$"            ,  r"{0} GHz".format(qdt.G_f)          ],
#              [r"shunt capacitance"                      ,  r"{0} F".format(qdt.Cq)             ],
#              [r"loop width"                             ,  r"{0} um".format(qdt.loop_width)    ],
#              [r"loop height"                            ,  r"{0} um".format(qdt.loop_height)   ],
#             ]
#tx.make_table(qubit_values, r"|p{5 cm}|p{3 cm}|")

#tx.add(r"\subsection{IDT values}")
#idt_values=[[r"Talking/Listening IDTs"             ,  r"Value"                                 ],
#            [r"Finger type"                        ,  r"{0}".format(idt.ft)                    ],
#            [r"Number of finger pairs, $N_{p}$"    ,  r"{0}".format(idt.Np)                    ],
#            [r"Overlap length, $W$"                ,  r"{0} $\mu$m".format(idt.W/1.0e-6)       ],
#            [r"finger width, $a$"                  ,  r"{0} nm".format(idt.a/1.0e-9)           ],
#            [r"Metallization ratio"                ,  r"{0}\%".format(idt.eta)                 ]
#           ]
#tx.make_table(idt_values, r"|p{5 cm}|p{3 cm}|")
#
#tx.add(r"\subsection{Calculated qubit values}")
#calc_qubit=[[r"Calculated values qubit"            ,  r"Value"                                     ,  r"Expression"                          , r"Comment"                     ],
#            [r"Center frequency"                   ,  r"{0} GHz".format(qdt.f0)                    ,  r"$v/(8a_q)$"                          , r"speed over wavelength"       ],
#            [r"Gap $\Delta(0)$"                    ,  r"200e-6 eV"                                 ,  r"$1.764 k_B T_c$"                     , r"BCS"                         ],
#            [r"Critical current, $I_c$"            ,  r"{0} nA".format(qdt.Ic/1.0e-9)              ,  r"$\dfrac{\pi \Delta(0)}{2e}$"         , r"Ambegaokar Baratoff formula" ],
#            [r"$E_{Jmax}$"                         ,  r"{0} GHz".format(qdt.Ejmax)                 ,  r"$\dfrac{\hbar I_c}{2e R_n}$"         , r"{}"                          ],
#            [r"Capacitance from fingers $C_q$"     ,  r"{0} fF".format(qdt.Ct/1.0e-15)             ,  r"$\sqrt{2} W N_{pq} \epsilon_\infty$" , r"Morgan chp 1"                ],
#            [r"\(E_c\)"                            ,  r"{0} MHz".format(qdt.Ec)                    ,  r"$\dfrac{e^2}{2 C}$"                  , r"Charging energy"             ],
#            [r"Ejmax/Ec"                           ,  r"{0}".format(qdt.EjmaxdivEc)                ,  r"Ejmax/Ec"                            , r"transmon limit"              ],
#            [r"Estimated max frequency of qubit"   ,  r"{0} GHz".format(qdt.fq_max)                ,  r"{}"                                  , r"full transmon expression"    ],
#            [r"Estimated max frequency of qubit"   ,  r"{0} GHz".format(qdt.fq_approx_max)           ,  r"{}"                                  , r"full transmon expression"    ],
#            [r"Estimated flux/flux0"               ,  r"{0}".format(qdt.flux_over_flux0)           ,  r"{}"                                  , r"full transmon expression"    ],
#            [r"loop area"                          ,  r"{0} $\mu$m$^2$".format(qdt.loop_height)    ,  r"{}"                                  , r"Area"                        ],
#            [r"$E_J$"                              ,  r"{0} GHz".format(qdt.Ejmax/1.0e9)           ,  r"$\dfrac{\hbar I_c}{2e R_n}$"         , r"{}"                          ],
#            [r"Ej/Ec"                              ,  r"{0}".format(qdt.EjdivEc)                   ,  r"Ej/Ec"                               , r"transmon limit"              ],
#            [r"Working frequency"                  ,  r"{0} GHz".format(qdt.fq)                    ,  r"$v/(8a_q)$"                          , r"speed over wavelength"       ],
#           ]
#
#tx.add(r"\subsection{Calculated IDT values}")
#calc_idt=[[r"Calculated values IDT"          ,  r"Value"                            ,  r"Expression"                          , r"Comment"                ],
#          [r"Center frequency"               ,  r"{0} GHz".format(idt.f0)           ,  r"$v/(8a)$"                            , r"speed over wavelength"  ],
#          [r"Capacitance from fingers, $C$"  ,  r"{0} fF".format(idt.Ct/1.0e-15)    ,  r"$\sqrt{2} W N_{p} \epsilon_\infty$"  , r"Morgan chp 1"           ],
#          [r"$Ga0$"                          ,  r"{0} $\Omega$".format(1.0/idt.Ga0) ,  r"$\dfrac{1}{G_{a0}}$"                  , r"Electrical impedance"  ],
#         ]
#          #[r"F width at half max"            ,  r"115"                 ,  r"Ejmax/Ec"                            , r"transmon limit"         ]]
#tx.make_table(calc_idt, r"|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|")