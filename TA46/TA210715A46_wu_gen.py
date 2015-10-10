# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:51:36 2015

@author: thomasaref
"""
dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/writeup/"
file_name="TA210715A46_writeup.tex"

from TEX_functions import TEX
        
tx=TEX(dir_path, file_name)

tx.add(r"\section{Summary}")
tx.add(r"""This is an attempt at reducing the coupling by changing the spacing of
 the fingers pairs on the qubit IDT, pushing them to a higher frequency.""")
tx.add("")

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
            [r"Ej\_max"                         ,  r"0.82 K, 17 GHz"       ,  r"$\dfrac{\hbar I_c}{2e R_n}$"         , r"{}"                          ],
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




from TA210715A46_Fund import print_fundamentals
print_fundamentals()

tx.add(r"\section{Data}")
tx.add(r"\subsection{Initial reflection fluxmap}")

tx.add(r"This initial data showed there was flux dependence in the reflection from the IDT.")

from D1005_refl_fluxmap_andpower import plotdB_colormap, plotabs_colormap
tx.include_figure(plotdB_colormap, "refl_dB_fluxmap_0.png", pwi=0)

tx.include_figure(plotdB_colormap, "refl_dB_fluxmap_3.png", pwi=3)

tx.include_figure(plotdB_colormap, "refl_dB_fluxmap_7.png", pwi=7)

tx.include_figure(plotabs_colormap, "refl_abs_fluxmap_0.png", pwi=0)

tx.include_figure(plotabs_colormap, "refl_abs_fluxmap_3.png", pwi=3)

tx.include_figure(plotabs_colormap, "refl_abs_fluxmap_7.png", pwi=7)

tx.add(r"\subsection{Reflection time domain flux sweeps}")
tx.add(r"""This data confirms that the flux dependence is primarily acoustic. The flux dependence 
does not show up until significant time has passed after the electrical excitation is applied. The pulse should take on the order
of 115 ns to travel the 400 $\mu$ from the reflection IDT to the qubit and back. It's difficult to see anything
115 ns after the pulse starts but this is probably due to a combination of noise and the signal needing time to build up, as in the GaAs case.
After the pulse is switched off, there is a clearly visible step feature that correspond to 115 ns that is different between the max and min graphs.""")

from D1006_refl_time_domain import     maxandmin_intime, time_cuts, plotmapdBtime, plotmaptime

tx.include_figure(plotmaptime, "refl_time_abs_fluxmap.png")

tx.include_figure(plotmapdBtime, "refl_time_dB_fluxmap.png")

tx.include_figure(time_cuts, "refl_time_cuts.png")

tx.include_figure(maxandmin_intime, "refl_maxmin_intime.png")

tx.make_tex_file()