# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:51:36 2015

@author: thomasaref
"""
dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A45_cooldown1/writeup/"
file_name="TA210715A45_writeup.tex"

from TEX_functions import TEX, read_tex, extract_block



tex_source="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A45_cooldown1/tikztry.tex"
#print extract_block("sam", str_list)
 
#print extract_block("bob", str_list)    

if 1:            
    tx=TEX(dir_path, file_name, tex_source)
    
    tx.ext("summary")
#    tx.add(r"\section{Summary}")
#    tx.add(r"""This is an attempt at reducing the coupling by changing the spacing of
#     the fingers pairs on the qubit IDT, pushing them to a higher frequency. The coupling appears reduced by an order of 
#     magnitude and the qubit seems to be operating as a qubit. Unfortunately, the qubit frequency is below the IDT listening/talking
#     frequency so it is never directly on resonance (this could be easily fixed by having less resistive junctions).
#    Speedy was also experiencing quite a bit of trouble with blockages so the temperature was often in the 50-80 mK range.""")
#    tx.add("")

if 0:    
    qubit_values=[[r"Qubit"                                  ,  r"{}"                             ],
                  [r"Finger type"                            ,  r"double finger"                  ], 
                  [r"Number of finger pairs, $N_{pq}$"      ,  r"9"                              ],
                  [r"Overlap length, $W$"                   ,  r"25 $\mu$m"                      ],
                  [r"finger width, $a_q$"                   ,  r"80 nm"                           ],
                  [r"DC Junction Resistances"               ,  r"8.93 k$\Omega$, 9.35k$\Omega$"  ],
                  [r"Metallization ratio"                   ,  r"50\%"                           ]]
    
    
    tx.add(r"\subsection{Qubit values}")
    tx.make_table(qubit_values, r"|p{5 cm}|p{3 cm}|")
    
    tx.add(r"\subsection{IDT values}")
    idt_values=[[r"Talking/Listening IDTs"             ,  r"{}"              ],
                [r"Finger type"                        ,  r"double finger"   ], 
                [r"Number of finger pairs, $N_{p}$"    ,  r"36"              ],
                [r"Overlap length, $W$"                ,  r"25 $\mu$m"       ],
                [r"finger width, $a$"                  ,  r"96 nm"           ],
                [r"Metallization ratio"                ,  r"50\%"            ]]
    tx.make_table(idt_values, r"|p{5 cm}|p{3 cm}|")
    
    tx.add(r"\subsection{Calculated qubit values}")
    
    calc_qubit=[[r"Calculated values qubit"         ,  r"Value"                ,  r"Expression"                          , r"Comment"                     ],
                [r"Center frequency"                ,  r"5.45 GHz"             ,  r"$v/(8a_q)$"                          , r"speed over wavelength"       ],
                [r"Gap $\Delta(0)$"                 ,  r"200e-6 eV"            ,  r"$1.764 k_B T_c$"                     , r"BCS"                         ],
                [r"Normal resistance, $R_n$"        ,  r"9.14 kOhms"           ,  r"mean(DC junction resistances)"       , r"Tunable"                     ],
                [r"Critical current, $I_c$"         ,  r"35 nA"                ,  r"$\dfrac{\pi \Delta(0)}{2e}$"         , r"Ambegaokar Baratoff formula" ],
                [r"$E_{Jmax}$"                         ,  r"0.82 K, 17 GHz"       ,  r"$\dfrac{\hbar I_c}{2e R_n}$"         , r"{}"                          ],
                [r"Capacitance from fingers $C_q$"  ,  r"130 fF"               ,  r"$\sqrt{2} W N_{pq} \epsilon_\infty$" , r"Morgan chp 1"                ],
                [r"\(E_c\)"                         ,  r"{7.2 mK,} {150 MHz}"  ,  r"$\dfrac{e^2}{2 C}$"                  , r"Charging energy"             ],
                [r"Ejmax/Ec"                        ,  r"115"                  ,  r"Ejmax/Ec"                            , r"transmon limit"              ],
                [r"Estimated max frequency of qubit",  r"4.37 GHz"             ,  r"{}"                                  , r"full transmon expression"    ]]
    
    tx.make_table(calc_qubit, r"|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|")
    
    tx.add(r"\subsection{Calculated IDT values}")
    
    
    calc_idt=[[r"Calculated values IDT"          ,  r"Value"               ,  r"Expression"                          , r"Comment"                ],
              [r"Center frequency"               ,  r"4.54 GHz"            ,  r"$v/(8a)$"                            , r"speed over wavelength"  ],
              [r"Capacitance from fingers, $C$"  ,  r"518 fF"              ,  r"$\sqrt{2} W N_{p} \epsilon_\infty$"  , r"Morgan chp 1"           ],
              [r"$Ga0$"                          ,  r"{7.2 mK,} {150 MHz}" ,  r"$\dfrac{e^2}{2 C}$"                  , r"Charging energy"        ],
              [r"F width at half max"            ,  r"115"                 ,  r"Ejmax/Ec"                            , r"transmon limit"         ]]
    
    tx.make_table(calc_idt, r"|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|")
    
    
    tx.add("\pagebreak")
    tx.add(r"\subsection{Setup}")
    tx.include_image("TA210715A46_setup.png", caption="Set-up")
    tx.include_image("TA210715A46_cooldownlogpic.png", caption="Fridge")
    
    
    tx.add("\pagebreak")
    tx.add(r"\subsection{Theory summary}")
    tx.add(r"""The flux parabola shown on the curves is done by assuming $E_J= E_{Jmax} |\cos(\pi \Phi/\Phi_0)|$ 
    where $\Phi/\Phi_0$
    is extracted from the flux voltage by adding a small offset of 0.1V or 
    less (the offset can vary between data sets if there is a flux jump) and multiplying by 0.193 
    (determined by matching up to flux periodicity).
     
     The resulting frequency is $f=(E_1-E_0)/h$ where $$E_0=0.5\sqrt(8 E_J E_C) - E_C/4$$
     $$E_1 =1.5\sqrt(8 E_J E_C) - (E_C/12)(6+6+3)$$
    
     The corresponding detuning from a frequency, $f_0$, I am talking/listening to is
     $$\Delta \omega = 2 \pi (f-f_0)$$ 
     
     The qubit reflection is :
     $$|R| = \left| \left(-\dfrac{\Gamma}{2\gamma} \right) \dfrac{1+i \Delta \omega/\gamma}{1 + (\Delta \omega/\gamma)^2 + 2N_{in}/\gamma)}\right|$$
     where $\gamma=\Gamma/2$ and $\Gamma=2 \pi \times 50 MHz$, i.e. $\gamma$ is the total coupling which is being assumed dominated entirely by the acoustic coupling
    $\Gamma$ of 50 MHz with no dephasing or electrical coupling. $N_{in}$ is the linear power divided by $hf_0$.
    
    The fits are more to show that the `flavor' of the data is captured using the qubit reflection expression 
    than to be exact fits. A suppressed coupling on the order of 50 MHz gives a good
    description of the data. 
    
    As shown in the theory graphs below, the coupling without sinc function suppression 
    would be 1.0 GHz while at the frequency we are working at it is should be either 50 or 100 MHz following eq 24 in Anton's
    PRA. The $N$ that appears in Anton's paper is the number of coupling points and I'm unclear whether
    this should be number of finger pairs, $N_p$, or number of fingers. Semiclassically, I would expect the sinc$^2$ behavior
    of the coupling to be the same as the sinc$^2$ dependence of $G_a$ which indicates $N/2=N_p$. On the other hand, one needs
    a pair of fingers to couple to the SAW which would indicate $N=N_p$ though this implies a double frequency sinc function 
    compared to other SAW related sinc functions.
     """)
    
    from Theory_141015 import couple_theory, couple_theory_zoom
    tx.mult_fig_start()
    tx.add_mult_fig(couple_theory, "couple_theory.png")
    caption=tx.add_mult_fig(couple_theory_zoom, "couple_theory_zoom.png")
    tx.mult_fig_end(caption)
    
    from TA210715A46_Fund import print_fundamentals
    print_fundamentals()
    
    tx.add("\pagebreak")
    tx.add(r"\section{Data}")
    tx.add(r"\subsection{Transmission and reflection}")
    
    from D1005_refl import cs_dB_meanyoko_refl
    from D1005_transandrefl import cs_dB_meanyoko_trans
    
    tx.mult_fig_start()
    tx.add_mult_fig(cs_dB_meanyoko_refl, "cs_dB_meanyoko_refl.png")
    caption=tx.add_mult_fig(cs_dB_meanyoko_trans, "cs_dB_meanyoko_trans.png")
    tx.mult_fig_end(caption)
    
    tx.add(r"\subsection{Initial reflection fluxmap}")
    
    tx.add(r"""This data showed there was flux dependence in the reflection data from the IDT.
     Subtracting the background off resonance at flux=-2.56V and plotting the absolute yields the clearer representation. 
     Interference fringes are clearly visible in the response.""")
    
    from D1005_refl_fluxmap_andpower import plotdB_colormap, plotabs_colormap, cs_abs
    tx.mult_fig_start()
    tx.add_mult_fig(plotdB_colormap, "refl_dB_fluxmap_0.png", pwi=0)
    tx.add_mult_fig(plotabs_colormap, "refl_abs_fluxmap_0.png", pwi=0)
    tx.add_mult_fig(plotdB_colormap, "refl_dB_fluxmap_3.png", pwi=3)
    tx.add_mult_fig(plotabs_colormap, "refl_abs_fluxmap_3.png", pwi=3)
    tx.add_mult_fig(plotdB_colormap, "refl_dB_fluxmap_7.png", pwi=7)
    caption=tx.add_mult_fig(plotabs_colormap, "refl_abs_fluxmap_7.png", pwi=7)
    tx.mult_fig_end(caption)
    
    tx.add(r"""The behavior of the crosssections of the absolute response can roughly be captured if
    I assume an additional 6 dB loss on top of the 87 dB of line attenuation measured at room temperature.""")
    
    tx.mult_fig_start()
    tx.add_mult_fig(cs_abs, "reflhigh_cs_0.png", fqi=106, pwi=0)
    tx.add_mult_fig(cs_abs, "reflhigh_cs_3.png", fqi=106, pwi=3)
    caption=tx.add_mult_fig(cs_abs, "reflhigh_cs_7.png", fqi=106, pwi=7)
    tx.mult_fig_end(caption)
    
    tx.add("\pagebreak")
    tx.add(r"\subsection{Reflection time domain flux sweeps}")
    tx.add(r"""This data confirms that the flux dependence is primarily acoustic. The flux dependence 
    does not show up until significant time has passed after the electrical excitation is applied. The pulse should take on the order
    of 115 ns to travel the 400 $\mu$m from the reflection IDT to the qubit and back. It's difficult to see anything
    115 ns after the pulse starts but this is probably due to a combination of noise and the signal needing time to build up, as in the GaAs case.
    After the pulse is switched off, there is a clearly visible step feature that correspond to 115 ns that is different between the max and min graphs.""")
    
    from D1006_refl_time_domain import maxandmin_intime, time_cuts, plotmapdBtime, plotmaptime
    
    tx.mult_fig_start()
    tx.add_mult_fig(plotmaptime, "refl_time_abs_fluxmap.png", width=0.49)
    tx.add_mult_fig(plotmapdBtime, "refl_time_dB_fluxmap.png", width=0.49)
    tx.add_mult_fig(time_cuts, "refl_time_cuts.png", width=0.49)
    tx.add_mult_fig(maxandmin_intime, "refl_maxmin_intime.png", width=0.49)
    tx.mult_fig_end(caption)
    
    
    tx.add("\pagebreak")
    tx.add(r"\subsection{Gate flux sweeps}")
    tx.add(r"""This data is similar to the listening/spike plots we did on the GaAs sample. I dropped the frequency to explore if the frequency parabola of
    the qubit matches experimentally predicted values and it seems to. Unfortunately, the talking/listening IDT is very bad at picking up SAW
    in this range.""")
    
    from D1006_gatefluxswp import gate_bgsub_colormesh, gate_bgsub_colormesh_wparabola
    
    tx.mult_fig_start()
    tx.add_mult_fig(gate_bgsub_colormesh, "gate_bgsub_colormesh.png", pwi=5, width=0.49)
    caption=tx.add_mult_fig(gate_bgsub_colormesh_wparabola, "gate_bgsub_colormesh_wparabola.png", pwi=5, width=0.49)
    tx.mult_fig_end(caption)
    
    
    tx.add("\pagebreak")
    tx.add(r"\subsection{Low frequency reflection flux sweeps}")
    tx.add(r"""This is what the reflection looks like at lower frequencies where there isn't much signal but one can see the parabola. I have plotted the parabola on the flux map and some 
    rough fits to the crosssections assuming 50 MHz coupling and no power input.""")
    
    from D1007_refl_fluxswp_lowfrq import cs_refl_lowfrq, cm_refl_lowfrq, cm_refl_lowfrq_parabola
    
    
    tx.mult_fig_start()
    tx.add_mult_fig(cm_refl_lowfrq, "cm_refl_lowfrq.png", pwi=4)
    caption=tx.add_mult_fig(cm_refl_lowfrq_parabola, "cm_refl_lowfrq_parabola.png", pwi=4)
    tx.mult_fig_end(caption)
    
    tx.mult_fig_start()
    tx.add_mult_fig(cs_refl_lowfrq, "cs_refl_lowfrq_103_4.png", fqi=103, pwi=4)
    tx.add_mult_fig(cs_refl_lowfrq, "cs_refl_lowfrq_85_4.png", fqi=85, pwi=4)
    tx.add_mult_fig(cs_refl_lowfrq, "cs_refl_lowfrq_199_4.png", fqi=199, pwi=4)
    caption=tx.add_mult_fig(cs_refl_lowfrq, "cs_refl_lowfrq_185_4.png", fqi=185, pwi=4)
    #tx.add_mult_fig(cs_refl_lowfrq, "cs_refl_lowfrq_95_4.png", fqi=95, pwi=4)
    #caption=tx.add_mult_fig(cs_refl_lowfrq, "cs_refl_lowfrq_65_4.png", fqi=65, pwi=4)
    tx.mult_fig_end(caption)
    
    tx.add("\pagebreak")
    tx.add(r"\subsection{Power saturation}")
    tx.add(r"""I tried acquiring a power saturation from reflection data directly at 4.285 GHz which is a frequency where I seem to have signal but should still cross the parabola. 
    This proved impractical since the signal I get from the IDT in the frequency is so weak. What did seem to work eventually 
    was probing at a higher frequency with low power while driving at 4.285 GHz and changing the power. I have included a rough fit assuming 50 MHz coupling though there would be some additional
    loss that I have not included.""")
    
    from D1010_refl_powsat import VNA_twotonesat, VNA_twotone_colormesh
    tx.mult_fig_start()
    tx.add_mult_fig(VNA_twotone_colormesh, "VNA_twotone_colormesh.png", width=0.49)
    caption=tx.add_mult_fig(VNA_twotonesat, "VNA_twotonesat.png", width=0.49)
    tx.mult_fig_end(caption)
    
tx.make_tex_file()