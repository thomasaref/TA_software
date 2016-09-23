# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 17:28:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read_NP, TA88_Lyzer, TA88_Read, qdt, ideal_qdt
from taref.physics.qdt import QDT
from taref.plotter.api import scatter, line,  LineFitter, Plotter
from atom.api import FloatRange, Typed, Unicode
from taref.core.universal import ODict
from numpy import append, linspace
from taref.core.api import tag_property, get_all_tags, get_tag
from taref.physics.fundamentals import h

npr=TA88_Read_NP(file_path=r"/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/D0629_flux_parabola.txt",
                 show_data_str=True)

a=TA88_Lyzer( name="fluxparabola",
             desc="flux parabola data",
             )
a.save_folder.main_dir=a.name

def flux_plots():
    data=npr.read()
    frequency=linspace(3.5e9, 7.5e9, 1000)
    freq=append(frequency/1e9, frequency/1e9)
    freq=append(freq, freq)
    V=qdt._get_Vfq0_many(f=frequency)[1]

    pl1=scatter(data[:, 0], data[:, 1], fig_width=6.0, fig_height=4.0, color="red", pl="fitVvsf")
    line(freq, V, pl=pl1, ylabel="Yoko (V)", xlabel="Frequency (GHz)")

    pl1.add_label("a)")

    V2=ideal_qdt._get_Vfq0_many(f=frequency)[1]

    pl2=scatter(data[:, 0], data[:, 1], fig_width=6.0, fig_height=4.0, color="red", pl="idealVvsf")
    line(freq, V2, pl=pl2, ylabel="Yoko (V)", xlabel="Frequency (GHz)")
    pl2.add_label("b)")

    pl3=scatter(data[:, 1], data[:, 0], fig_width=6.0, fig_height=4.0, color="red", pl="fitfvsV")
    line(V, freq, pl=pl3, xlabel="Yoko (V)", ylabel="Frequency (GHz)")
    pl3.add_label("c)")

    pl4=scatter(data[:, 1], data[:, 0], fig_width=6.0, fig_height=4.0, color="red", pl="idealfvsV")
    line(V2, freq, pl=pl4, xlabel="Yoko (V)", ylabel="Frequency (GHz)")
    pl4.add_label("d)")

    #pls=[pl1, pl2, pl3, pl4]

    #for pl in pls:
    return [pl1, pl2, pl3, pl4]

if __name__=="__main__":
    pls=flux_plots()
    #a.save_plots(pls)
    pls[0].show()
