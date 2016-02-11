# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:33:17 2016

@author: thomasaref
"""

from taref.tex.tex import TEX
from taref.core.shower import shower
tx=TEX()
tx.make_input_code()
tx.output_tex="""\pyb {summary}
    \section{Summary}
    This is an attempt at reducing the coupling by changing the spacing of the fingers pairs on the qubit IDT, pushing them to a higher frequency.
    The coupling appears reduced by an order of magnitude and the qubit seems to be operating as a qubit.
    Unfortunately, the qubit frequency is below the IDT listening/talking frequency so it is never directly on resonance (this could be easily fixed by having less resistive junctions). Speedy was also experiencing quite a bit of trouble with blockages so the temperature was often in the 50-80 mK range.

\pye

\pyb {second entry}
this is the second entry
\pye"""#.split("\n")
tx.process_source()
print tx.source_dict

tx.TEX_start()
tx.ext("summary")
tx.ext("second entry")

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
tx.add_mult_fig(tx.add_mult_fig, "test_colormap_plot.png")
tx.mult_fig_end()
tx.TEX_end()

#tx.make_tex_file()
#tx.compile_tex()

shower(tx)