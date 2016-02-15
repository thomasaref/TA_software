# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:33:17 2016

@author: thomasaref
"""

from taref.tex.tex import TEX
from taref.core.shower import shower
from TA88_fundamental import qdt, idt

tx=TEX(source_path="/Users/thomasaref/Dropbox/Current stuff/test_data/source/TA210715A88_source/TA210715A88_writeup.tex")
tx.save_file.file_name="TA210715A88_writeup"
tx.tex_title="Sample TA210715A88 in Lumi 12-10-15 cooldown"
tx.locals_dict=dict(idt=idt, qdt=qdt)
#sample holder 12


tx.TEX_start()
tx.ext("summary")
tx.ext("switch")

tx.add(r"\subsection{Qubit values}")
qubit_values=[[r"QDT"                                    ,  r"Value"                            ],
              [r"Finger type"                            ,  r"{0}".format(qdt.ft)               ],
              [r"Number of finger pairs, $N_{pq}$"       ,  r"{0}".format(qdt.Np)               ],
              [r"Overlap length, $W$"                    ,  r"{0} $\mu$m".format(qdt.W/1.0e-6)  ],
              [r"finger width, $a_q$"                    ,  r"{0} nm".format(qdt.a/1.0e-9)      ],
              [r"DC Junction Normal Resistance"          ,  r"{0} k$\Omega$".format(qdt.Rn)     ],
              [r"Metallization ratio"                    ,  r"{0}\%".format(qdt.eta)            ],
              [r"Coupling at IDT center frequency"""     ,  r"{0} GHz".format(qdt.G_f0/1.0e9)   ],
              [r"Coupling adjusted by $sinc^2$"            ,  r"{0} GHz".format(qdt.G_f)          ],
              [r"shunt capacitance"                      ,  r"{0} F".format(qdt.Cq)             ],
              [r"loop width"                             ,  r"{0} um".format(qdt.loop_width)    ],
              [r"loop height"                            ,  r"{0} um".format(qdt.loop_height)   ],
             ]
tx.make_table(qubit_values, r"|p{5 cm}|p{3 cm}|")

tx.add(r"\subsection{IDT values}")
idt_values=[[r"Talking/Listening IDTs"             ,  r"Value"                                 ],
            [r"Finger type"                        ,  r"{0}".format(idt.ft)                    ],
            [r"Number of finger pairs, $N_{p}$"    ,  r"{0}".format(idt.Np)                    ],
            [r"Overlap length, $W$"                ,  r"{0} $\mu$m".format(idt.W/1.0e-6)       ],
            [r"finger width, $a$"                  ,  r"{0} nm".format(idt.a/1.0e-9)           ],
            [r"Metallization ratio"                ,  r"{0}\%".format(idt.eta)                 ]
           ]
tx.make_table(idt_values, r"|p{5 cm}|p{3 cm}|")

tx.add(r"\subsection{Calculated qubit values}")
calc_qubit=[[r"Calculated values qubit"            ,  r"Value"                                     ,  r"Expression"                          , r"Comment"                     ],
            [r"Center frequency"                   ,  r"{0} GHz".format(qdt.f0)                    ,  r"$v/(8a_q)$"                          , r"speed over wavelength"       ],
            [r"Gap $\Delta(0)$"                    ,  r"200e-6 eV"                                 ,  r"$1.764 k_B T_c$"                     , r"BCS"                         ],
            [r"Critical current, $I_c$"            ,  r"{0} nA".format(qdt.Ic/1.0e-9)              ,  r"$\dfrac{\pi \Delta(0)}{2e}$"         , r"Ambegaokar Baratoff formula" ],
            [r"$E_{Jmax}$"                         ,  r"{0} GHz".format(qdt.Ejmax)                 ,  r"$\dfrac{\hbar I_c}{2e R_n}$"         , r"{}"                          ],
            [r"Capacitance from fingers $C_q$"     ,  r"{0} fF".format(qdt.Ct/1.0e-15)             ,  r"$\sqrt{2} W N_{pq} \epsilon_\infty$" , r"Morgan chp 1"                ],
            [r"\(E_c\)"                            ,  r"{0} MHz".format(qdt.Ec)                    ,  r"$\dfrac{e^2}{2 C}$"                  , r"Charging energy"             ],
            [r"Ejmax/Ec"                           ,  r"{0}".format(qdt.EjmaxdivEc)                ,  r"Ejmax/Ec"                            , r"transmon limit"              ],
            [r"Estimated max frequency of qubit"   ,  r"{0} GHz".format(qdt.fq_max)                ,  r"{}"                                  , r"full transmon expression"    ],
            [r"Estimated max frequency of qubit"   ,  r"{0} GHz".format(qdt.fq_max_full)           ,  r"{}"                                  , r"full transmon expression"    ],
            [r"Estimated flux/flux0"               ,  r"{0}".format(qdt.flux_over_flux0)           ,  r"{}"                                  , r"full transmon expression"    ],
            [r"loop area"                          ,  r"{0} $\mu$m$^2$".format(qdt.loop_height)    ,  r"{}"                                  , r"Area"                        ],
            [r"$E_J$"                              ,  r"{0} GHz".format(qdt.Ejmax/1.0e9)           ,  r"$\dfrac{\hbar I_c}{2e R_n}$"         , r"{}"                          ],
            [r"Ej/Ec"                              ,  r"{0}".format(qdt.EjdivEc)                   ,  r"Ej/Ec"                               , r"transmon limit"              ],
            [r"Working frequency"                  ,  r"{0} GHz".format(qdt.fq)                    ,  r"$v/(8a_q)$"                          , r"speed over wavelength"       ],
           ]
tx.make_table(calc_qubit, r"|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|")

tx.add(r"\subsection{Calculated IDT values}")
calc_idt=[[r"Calculated values IDT"          ,  r"Value"                            ,  r"Expression"                          , r"Comment"                ],
          [r"Center frequency"               ,  r"{0} GHz".format(idt.f0)           ,  r"$v/(8a)$"                            , r"speed over wavelength"  ],
          [r"Capacitance from fingers, $C$"  ,  r"{0} fF".format(idt.Ct/1.0e-15)    ,  r"$\sqrt{2} W N_{p} \epsilon_\infty$"  , r"Morgan chp 1"           ],
          [r"$Ga0$"                          ,  r"{0} $\Omega$".format(1.0/idt.Ga_0) ,  r"$\dfrac{1}{G_{a0}}$"                  , r"Electrical impedance"  ],
         ]
          #[r"F width at half max"            ,  r"115"                 ,  r"Ejmax/Ec"                            , r"transmon limit"         ]]
tx.make_table(calc_idt, r"|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|")


tx.mult_fig_start()
#tx.add_mult_fig(tx.add_mult_fig, "test_colormap_plot.png")
tx.mult_fig_end()
tx.include_image("fridgewiring", "Fridge Wiring", "fridgewiring")
tx.include_image("switchwiring", "Switch Wiring", "switchwiring")
#tx.include_image("test_colormap_plot.png", "image include test", "whats the label")
tx.TEX_end()

#tx.make_tex_file()
#tx.compile_tex()

shower(tx)