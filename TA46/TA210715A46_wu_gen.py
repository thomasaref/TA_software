# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 13:51:36 2015

@author: thomasaref
"""
dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A46_cooldown1/writeup/"
file_name="TA210715A46_writeup.tex"

from TEX_functions import TEX
        
tx=TEX(dir_path, file_name)

tex=[]
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
r"|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|}"

calc_qubit=[[r"Calculated values qubit", "Value"      ,  "Expression"        , "Comment"                 ],
            [r"Center frequency"       , r"5.45 GHz"  ,  r"$v/(8a_q)$"       , "speed over wavelength"   ],
            [r"Gap $\Delta(0)$"        , r"200e-6 eV" ,  r"$1.764 k_B T_c$"  , "BCS"                     ],
            [r"Normal resistance, $R_n$", "9.14 kOhms", "mean(DC junction resistances)" , "Tunable"      ],
            [r"Critical current, $I_c$",  "35 nA",      "$\dfrac{\pi \Delta(0)}{2e}$",  "Ambegaokar Baratoff formula"],
            [r"Ej\_max"                  ,  r"0.82 K, 17 GHz", r"$\dfrac{\hbar I_c}{2e R_n}$" , r"{}" ],
             
tex.append(r"\hline")
tex.append(r"Capacitance from fingers $C_q$ & 130 fF & $\sqrt{2} W N_{pq} \epsilon_\infty$ & Morgan chp 1 \\")
tex.append(r"\hline")
tex.append(r"\(E_c\) & {7.2 mK,} {150 MHz} & $\dfrac{e^2}{2 C}$ & Charging energy \\")
tex.append(r"\hline")
tex.append(r"Ejmax/Ec & 115 & Ejmax/Ec & transmon limit \\")
tex.append(r"\hline")
tex.append(r"Estimated max frequency of qubit & 4.37 GHz & {} & full transmon expression \\")
tex.append(r"\hline")
tex.append(r"\end{tabular}")

tex.append(r"\subsection{Calculated IDT values}")
tex.append(r"\begin{tabular}{|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|}")
tex.append(r"\hline")
tex.append(r"Calculated values IDT & Value & Expression & Comment\\")
tex.append(r"\hline")
tex.append(r"Center frequency & 4.54 GHz & $v/(8a)$ & speed over wavelength\\")
tex.append(r"\hline")
tex.append(r"Capacitance from fingers $C$ & 518 fF & $\sqrt{2} W N_{p} \epsilon_\infty$ & Morgan chp 1 \\")
tex.append(r"\hline")
tex.append(r"$Ga0$ & {7.2 mK,} {150 MHz} & $\dfrac{e^2}{2 C}$ & Charging energy \\")
tex.append(r"\hline")
tex.append(r"F width at half max & 115 & Ejmax/Ec & transmon limit \\")
tex.append(r"\hline")
tex.append(r"\end{tabular}")



#tex.append(r"\begin{tabular}{|p{5 cm}|p{3 cm}|}")
#tex.append(r"\hline")
#tex.append(r"Talking/Listening IDTs & {} \\")
#tex.append(r"\hline")
#tex.append(r"Finger type & double finger\\")
#tex.append(r"\hline")
#tex.append(r"Number of finger pairs, $N_p$ & 36\\")
#tex.append(r"\hline")
#tex.append(r"Overlap length, $W$ & 25 $\mu$m\\")
#tex.append(r"\hline")
#tex.append(r"finger width, $a$ & 96 nm\\")
#tex.append(r"\hline")
#tex.append(r"Metallization ratio & 50\%\\")
#tex.append(r"\hline")
#tex.append(r"\end{tabular}")
#
#tex.append(r"\subsection{Sample values}")
#tex.append(r"\begin{tabular}{|p{5 cm}|p{3 cm}|}")
#tex.append(r"\hline")
#tex.append(r"Talking/Listening IDTs & {} \\")
#tex.append(r"\hline")
#tex.append(r"Distance qubit to reflection IDT & 200 $\mu$m\\")
#tex.append(r"\hline")
#tex.append(r"Distance qubit to transmission IDT & 300 $\mu$m\\")
#tex.append(r"\hline")
#tex.append(r"Speed of SAW & 3488 m/s\\")
#tex.append(r"\hline")
#tex.append(r"Capacitance per finger pair, $\epsilon_\infty$ & $46\epsilon_0$\\")
#tex.append(r"\hline")
#tex.append(r"Metallization ratio & 50\%\\")
#tex.append(r"\hline")
#tex.append(r"\end{tabular}")
#tex.append(r"")

#tex.append(r"\subsection{Calculated qubit values}")
#tex.append(r"\begin{tabular}{|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|}")
#tex.append(r"\hline")
#tex.append(r"Calculated values qubit & Value & Expression & Comment\\")
#tex.append(r"\hline")
#tex.append(r"Center frequency & 5.45 GHz & $v/(8a_q)$ & speed over wavelength\\")
#tex.append(r"\hline")
#tex.append(r"Gap $\Delta(0)$ & 200e-6 eV & $1.764 k_B T_c$ & BCS\\")
#tex.append(r"\hline")
#tex.append(r"Normal resistance, $R_n$ & 9.14 kOhms & mean(DC junction resistances) & Tunable \\")
#tex.append(r"\hline")
#tex.append(r"Critical current, $I_c$ & 35 nA &  $\dfrac{\pi \Delta(0)}{2e}$ & Ambegaokar Baratoff formula \\")
#tex.append(r"\hline")
#tex.append(r"Ej\_max & 0.82 K, 17 GHz & $\dfrac{\hbar I_c}{2e R_n}$ & {} \\")
#tex.append(r"\hline")
#tex.append(r"Capacitance from fingers $C_q$ & 130 fF & $\sqrt{2} W N_{pq} \epsilon_\infty$ & Morgan chp 1 \\")
#tex.append(r"\hline")
#tex.append(r"\(E_c\) & {7.2 mK,} {150 MHz} & $\dfrac{e^2}{2 C}$ & Charging energy \\")
#tex.append(r"\hline")
#tex.append(r"Ejmax/Ec & 115 & Ejmax/Ec & transmon limit \\")
#tex.append(r"\hline")
#tex.append(r"Estimated max frequency of qubit & 4.37 GHz & {} & full transmon expression \\")
#tex.append(r"\hline")
#tex.append(r"\end{tabular}")
#
#tex.append(r"\subsection{Calculated IDT values}")
#tex.append(r"\begin{tabular}{|p{3 cm}|p{3 cm}|p{3 cm}|p{3 cm}|}")
#tex.append(r"\hline")
#tex.append(r"Calculated values IDT & Value & Expression & Comment\\")
#tex.append(r"\hline")
#tex.append(r"Center frequency & 4.54 GHz & $v/(8a)$ & speed over wavelength\\")
#tex.append(r"\hline")
#tex.append(r"Capacitance from fingers $C$ & 518 fF & $\sqrt{2} W N_{p} \epsilon_\infty$ & Morgan chp 1 \\")
#tex.append(r"\hline")
#tex.append(r"$Ga0$ & {7.2 mK,} {150 MHz} & $\dfrac{e^2}{2 C}$ & Charging energy \\")
#tex.append(r"\hline")
#tex.append(r"F width at half max & 115 & Ejmax/Ec & transmon limit \\")
#tex.append(r"\hline")
#tex.append(r"\end{tabular}")

tex.append(r"\section{Graphs}")
tex.append(r"\subsection{SEM BDT}")

tx.ext(tex)

from TA210715A46_Fund import print_fundamentals
print_fundamentals()

#from TA46_refll_fluxmap import refl_fluxmap
#tx.include_figure(refl_fluxmap, "foo.png", "my foo", "foolabel")

tx.make_tex_file()