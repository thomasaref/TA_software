# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:33:17 2016

@author: thomasaref
"""

from taref.tex.tex import TEX
from taref.core.shower import shower

tx=TEX(source_path="/Users/thomasaref/Dropbox/Current stuff/test_data/source/TA210715A88_source/TA210715A88_writeup.tex")
tx.save_file.file_name="TA210715A88_writeup"
tx.tex_title="Sample TA210715A88 in Lumi 12-10-15 cooldown"

tx.TEX_start()
tx.ext("summary")
tx.ext("switch")

qubit_values=[[r"Qubit"                                  ,  r"{}"                             ],
                      [r"Finger type"                            ,  r"double finger"                  ],
                      [r"Number of finger pairs, $N_{pq}$"      ,  r"9"                              ],
                      [r"Overlap length, $W$"                   ,  r"25 $\mu$m"                      ],
                      [r"finger width, $a_q$"                   ,  r"80 nm"                           ],
                      [r"DC Junction Resistances"               ,  r"8.93 k$\Omega$, 9.35k$\Omega$"  ],
                      [r"Metallization ratio"                   ,  r"50\%"                           ]]


tx.add(r"\subsection{Qubit values}")
tx.make_table(qubit_values, r"|p{5 cm}|p{3 cm}|")

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