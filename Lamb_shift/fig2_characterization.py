# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Lyzer, TA88_Read, qdt, TA88_Read_NP, TA88_Save_NP
from numpy import array, absolute, squeeze, append, sqrt, pi, arccos, shape
from taref.physics.fundamentals import h
from taref.plotter.api import colormesh, line

a=TA88_Lyzer(on_res_ind=201, rd_hdf=TA88_Read(main_file="Data_0628/S4A4_just_gate_overnight_flux_swp.hdf5"))

a.filt.center=0
a.filt.halfwidth=200
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.01
a.flux_axis_type="flux" #"yoko"#"flux"
a.end_skip=10
a.fit_indices=[range(2, 14), range(15, 17), range(19,23), range(24, 26), range(29, 37), range(38, 39), range(44, 46), range(48, 52),
               range(54, 66), range(67, 69), range(70, 85), range(105, 107), range(108, 116), range(122, 129), [130], range(132, 134), [138],
 range(182,184), range(188, 193), range(217, 251+1), range(266, 275+1), range(314, 324+1)]
#a.flux_indices=[range(400,434), range(436, 610)]
#a.flux_indices=[range(200, 400)]
a.read_data()
#a.ifft_plot()

a.bgsub_type="dB" #"Complex" #"Abs"
if __name__=="__main__":
    a.filter_type="FFT"
    pl=a.magabs_colormesh(vmin=0.995, vmax=1.002, auto_zlim=False, cmap="afmhot", auto_ylim=False, y_min=3.6, y_max=7.4)#.show()
    a.qdt.qubit_type="transmon" #scb"
    line(a.flux_axis, a.qdt._get_flux_parabola(voltage=a.yoko, ng=0.0)/1e9, pl=pl).show()
    #colormesh(a.flux_axis, a.freq_axis)
    pl="colormeshy"
    for inds in a.fit_indices:
        pl=colormesh(a.yoko, a.frequency[inds], a.MagAbs[inds, :], cmap="afmhot",
                     #vmin=0.992, vmax=1.000, auto_zlim=False,
                     pl=pl)
    pl.show()


#a.bgsub_type="Complex"
if __name__=="__main2__":
    pl="magabs"
    pl1="centers"

if __name__=="__main2__":
    a.magabs_colormesh(vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False, pl="mag")

    #pl=colormesh(a.MagAbs.transpose())
    #colormesh(savgol_filter(a.MagAbs, 11, 3, axis=1).transpose(), pl=pl).show()
    #colormesh(array([savgol_filter(a.MagAbs[:, n], 5, 2) for n in range(len(a.yoko))]), pl=pl)
    #pl.show()
    if 0:

        pl=a.magabs_colormesh(vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False)

        a.filter_type="FFT"
        #colormesh(array([savgol_filter(a.MagAbs[:, n], 5, 2) for n in range(len(a.yoko[a.flux_indices]))]))
        a.magabs_colormesh(pl=pl)#.show()
    a.filter_type="Fit"

    pl=a.magabs_colormesh(pl=pl, vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False, fig_width=9, fig_height=6)
    a.widths_plot()
    centers=-a.qdt._get_fluxfq0(f=a.frequency[a.indices])
    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])<0.3]
    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])>0.1]
    print [a.indices[n] for n, fp in enumerate(a.fit_params[:-1]) if absolute(fp[1]-a.fit_params[n+1][1])>0.1]
    print shape(a.flat_indices)
    print shape(a.flat_flux_indices)
    print shape(a.MagAbsFilt_sq)
    pl1=a.center_plot()

if __name__=="__main2__":
    a.flux_indices=[range(200, 400)]#, range(436, 610)]
    fit1=a.fit_indices[:]
    a.fit_indices=[[1], range(4, 11), [15], range(17, 23), range(26, 28), range(29, 37), range(38, 41), range(42,53), range(56,68),
                   range(71,77), range(78,81), [84], range(104,107), range(108,111), [116], range(124,129), [138],
                   range(182,184), range(189,194),
                   range(218, 255), range(264, 285), range(310,325)]#, range(337,348)]
    #a.fit_indices=[range(2, 14), range(15, 17), range(19,23), range(24, 26), range(29, 37), range(38, 39), range(44, 46), range(48, 52),
    #           range(54, 66), range(67, 69), range(70, 85), range(105, 107), range(108, 116), range(122, 129), [130], range(132, 134), [138],
    #             range(189, 193), range(199, 200), range(217, 251+1), range(266, 275+1), range(314, 324+1)]

    a.fitter.fit_params=None
    reset_property(a, "fit_params", "MagAbsFit", "MagcomFilt", "Magcom")
    if 0:
        a.filter_type="None"

        pl=a.magabs_colormesh(pl=pl)

        a.filter_type="FFT"
        a.magabs_colormesh(pl=pl)#.show()
    a.filter_type="Fit"

    a.magabs_colormesh(pl=pl, vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False, fig_width=9, fig_height=6)#.show()
    centers=a.qdt._get_fluxfq0(f=a.frequency[a.indices])

    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])>0.3]

    pl1=a.center_plot(pl=pl1)




if __name__=="__main2__":
    a.flux_indices=[range(610, 748), range(751, 758), range(761,800)]#, range(436, 610)]

    #a.fit_indices=list(set(fit1).union(set(fit2)))
    #a.fit_indices=[range(len(a.frequency))]
    a.fit_indices=[range(5,9), [11], range(15, 22), [23,24], range(30,35),
                   [36], range(44, 51), range(59, 62), [63, 64], [66], range(70, 72),
                   range(73, 75), range(76, 83), [87], range(104, 107), range(109, 111),
                   range(112, 116), range(124, 130), [138], range(182,184), range(189, 194), [201],
                   range(217, 253), range(265, 281), range(314, 326)]#, range(343, 350)]
    #a.fit_indices=[range(2, 14), range(15, 17), range(19,23), range(24, 26), range(29, 37), range(38, 39), range(44, 46), range(48, 52),
    #           range(54, 66), range(67, 69), range(70, 85), range(105, 107), range(108, 116), range(122, 129), [130], range(132, 134), [138],
    #             range(189, 193), range(199, 200), range(217, 251+1), range(266, 275+1), range(314, 324+1)]
    a.fitter.fit_params=None
    reset_property(a, "fit_params", "MagAbsFit", "MagcomFilt", "Magcom")
    if 0:
        a.filter_type="None"

        pl=a.magabs_colormesh(pl=pl)

        a.filter_type="FFT"
        a.magabs_colormesh(pl=pl)#.show()
    a.filter_type="Fit"

    a.magabs_colormesh(pl=pl, vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False)#.show()
    centers=a.qdt._get_fluxfq0(f=a.frequency[a.indices])

    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])>0.3]

    pl1=a.center_plot(pl=pl1)


if __name__=="__main2__":
    a.flux_indices=[range(0, 2), range(5,200)]#, range(436, 610)]
    a.fit_indices=[range(len(a.frequency))]

    a.fit_indices=[range(4, 7), [21], [47,48], [50], [72], [75], [78,79], [104], [109, 110],
                   range(137, 140), range(182,184),
                   range(188, 194), range(220,253), range(265, 282), range(314, 327)]

    a.fitter.fit_params=None
    reset_property(a, "fit_params", "MagAbsFit", "MagcomFilt", "Magcom")
    if 0:
        a.filter_type="None"

        pl=a.magabs_colormesh(pl=pl)#.show()

        a.filter_type="FFT"
        a.magabs_colormesh(pl=pl)#.show()
    a.filter_type="Fit"

    a.magabs_colormesh(pl=pl, vmin=0.995, vmax=1.005, cmap="nipy_spectral", auto_zlim=False)#.show()
    centers=a.qdt._get_fluxfq0(f=a.frequency[a.indices])

    print [a.indices[n] for n, fp in enumerate(a.fit_params) if absolute(fp[1]-centers[n])>0.3]


    pl1=a.center_plot(pl=pl1)

if __name__=="__main__2":
    nps=TA88_Save_NP(file_path=r"/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/discard/S2016_07_28_171620/meas.txt")
    nps.save(pl1.savedata())
    npr=TA88_Read_NP(file_path=nps.file_path, show_data_str=True)
    data=npr.read()
    scatter(data[:, 0], data[:, 1])
    #nps.data_buffer=pl1.savedata()
    pl1.show(nps, npr)

if __name__=="__main2__":
    pl.set_xlim(-6,6)
    pl.set_ylim(3.5, 7.5)
    pl.savefig(r"/Users/thomasaref/Dropbox (Clan Aref)/Current stuff/Logbook/TA210715A88_cooldown210216/tex_source_files/TA88_processed/", "fit_fluxmap")
    pl1.show()


if __name__=="__main2__":
    from taref.physics.filtering import Filter
    from numpy import absolute
    b=Filter(center=0, halfwidth=40, reflect=False, N=len(a.yoko))
    #Magcom=a.Magcom.transpose()
    Magfilt=array([b.fft_filter(a.Magcom[m,:]) for m in range(len(a.frequency[a.indices]))])#.transpose()
    pl=line(b.fftshift(absolute(b.window_ifft(a.Magcom[261, :]))), color="red")
    line(b.fftshift(absolute(b.window_ifft(a.Magcom[240, :]))), pl=pl)
    pl=colormesh(a.MagAbs)
    colormesh(absolute(Magfilt)[:, 10:-10]).show()
    colormesh((absolute(Magfilt).transpose()-absolute(Magfilt[:,20])).transpose()[:, 10:-10]).show()
    a.bgsub_type="Complex"
    pl, pf=line(a.MagAbs[:, 517])
    line(a.MagAbs[:, 519], color="red", pl=pl)
    line(a.MagAbs[:, 521], color="green", pl=pl)

    pl, pf=line(a.freq_axis, a.qdt._get_VfFWHM(f=a.frequency)[0],  color="blue")
    line(a.freq_axis, a.qdt._get_VfFWHM(f=a.frequency)[1],  color="green", pl=pl)

    line(a.freq_axis, a.qdt._get_VfFWHM(f=a.frequency)[2],  color="red", pl=pl)

    line(a.freq_axis, a.qdt._get_Vfq0(f=a.frequency),  color="purple", pl=pl)

    a.magabs_colormesh()
    a.bgsub_type="Abs"
    a.magabs_colormesh().show()

    a.hann_ifft_plot()
    def magdB_colormesh(self):
        pl, pf=colormesh(self.yoko, self.frequency/1e9, (self.MagdB.transpose()-self.MagdB[:,0]).transpose(), plotter="magabs_{}".format(self.name))
        pl.set_ylim(min(self.frequency/1e9), max(self.frequency/1e9))
        pl.set_xlim(min(self.yoko), max(self.yoko))
        pl.xlabel="Yoko (V)"
        pl.ylabel="Frequency (GHz)"
        return pl
    a.magabsfilt_colormesh()
    magdB_colormesh(a).show()
    a.magabs_colormesh().show()

    def magabs_colormesh2(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
        fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])

        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
        pl, pf=colormesh(fq_vec, self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0]), plotter=pl)
        pf.set_clim(-0.3, 0.1)
        #pl.set_xlim(min(self.frequency/1e9), max(self.frequency/1e9))
        pl.set_ylim(min(self.yoko), max(self.yoko))

        pl.ylabel="Yoko (V)"
        pl.xlabel="Frequency (GHz)"
        return pl

    def magabs_colormesh(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
        fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])
        freq, frq2=flux_parabola(self.yoko, offset, 0.16, Ejmax, qdt.Ec)

        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
        pl, pf=colormesh(freq, fq_vec, (self.MagdB.transpose()-self.MagdB[:, 0]).transpose(), plotter=pl)
        pf.set_clim(-0.3, 0.1)
        line([min(freq), max(freq)], [min(freq), max(freq)], plotter=pl)
        flux_o_flux0=flux_over_flux0(self.yoko, offset, flux_factor)
        qEj=Ej(Ejmax, flux_o_flux0)
        EjdivEc=qEj/qdt.Ec
        ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)

        frq2=qdt.call_func("lamb_shifted_anharm", EjdivEc=EjdivEc)/h
        line(ls_fq, ls_fq2, plotter=pl)

        #pl.set_xlim(min(self.frequency/1e9), max(self.frequency/1e9))
        #pl.set_ylim(min(self.yoko), max(self.yoko))

        pl.ylabel="Yoko (V)"
        pl.xlabel="Frequency (GHz)"
        return pl

    def line_cs(self, ind=210):
        print self.frequency[ind]/1e9
        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_cs_{}".format(self.name))
        pl, pf=line(self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0])[:, ind], plotter=pl, linewidth=1.0)
        pl.xlabel="Yoko (V)"
        pl.ylabel="Magnitude (dB)"
        return pl

    #def flux_par(self, pl, offset, flux_factor):
    #    set_tag(qdt, "EjdivEc", log=False)
    #    set_tag(qdt, "Ej", log=False)
    #    set_tag(qdt, "offset", log=False)
    #    set_tag(qdt, "flux_factor", log=False)
    #
    #    print qdt.max_coupling, qdt.coupling_approx
    #    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    #    Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0)
    #    EjdivEc=Ej/qdt.Ec
    #    #fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    #    ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
    #    ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
    #    line(self.yoko, ls_fq/1e9, plotter=pl, color="blue", linewidth=0.5, label=r"$\Delta_{1,0}$")
    #    line(self.yoko, ls_fq2/1e9, plotter=pl, color="red", linewidth=0.5, label=r"$\Delta_{2,1}$")
    #    #pl.set_ylim(-1.0, 0.6)
    #    #pl.set_xlim(0.7, 1.3)
    #    return pl

    from taref.physics.qubit import  flux_parabola, Ej_from_fq, voltage_from_flux, flux_over_flux0, Ej
    from taref.physics.qdt import lamb_shifted_anharm, calc_freq_shift, lamb_shifted_fq, lamb_shifted_fq2

    def fq2(Ej, Ec):
        E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
        #E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
        E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
        return (E2-E0)/h/2

    def Ej_from_fq2(fq2, Ec):
        return (((2*h*fq2+3.0*Ec)/2.0)**2)/(8.0*Ec)

    def flux_par4(self, offset=-0.08, flux_factor=0.16, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
        set_all_tags(qdt, log=False)
        flux_o_flux0=flux_over_flux0(self.yoko, offset, flux_factor)
        qEj=Ej(Ejmax, flux_o_flux0)
        #flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        freq, frq2=flux_parabola(self.yoko, offset, flux_factor, Ejmax, qdt.Ec)
        fq1=lamb_shifted_fq2(qEj/qdt.Ec, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv)
        line(self.yoko, freq, plotter=pl, linewidth=1.0, alpha=0.5)
        line(self.yoko, fq1/2, plotter=pl, linewidth=1.0, alpha=0.5)

    def flux_par3(self, offset=-0.08, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.7, pl=None):
        set_all_tags(qdt, log=False)
        flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        #print flux_o_flux0-pi/2*trunc(flux_o_flux0/(pi/2.0))
        #Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
        #EjdivEc=Ej/qdt.Ec
        fq_vec=array([sqrt(f*(f+1.0*qdt.call_func("calc_Lamb_shift", fqq=f))) for f in self.frequency])
        fq_vec=array([f-qdt.call_func("calc_Lamb_shift", fqq=f) for f in self.frequency])
        fq_vec=array([sqrt(f*(f+alpha*calc_freq_shift(f, qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for f in self.frequency])
        Ej=Ej_from_fq(fq_vec, qdt.Ec)
        flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
        flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
        flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax)+pi)
        flux_d_flux0=append(flux_d_flux0, arccos(Ej/Ejmax)-pi)

        if pl is not None:
            volt=voltage_from_flux(flux_d_flux0, offset, flux_factor)
            freq=s3a4_wg.frequency[:]/1e9
            freq=append(freq, freq) #append(freq, append(freq, freq)))
            freq=append(freq, freq)
            #freq=append(freq, freq)
            line(freq, volt, plotter=pl, linewidth=1.0, alpha=0.5)
            Ejdivh=Ej/h
            w0=4*Ejdivh*(1-sqrt(1-fq_vec/(2*Ejdivh)))
            EjdivEc=Ej/qdt.Ec
            #print -(w0**2)/(8*Ejdivh)

            ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
            E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
            fq2=(E2-E1)/h
            f_vec=lamb_shifted_anharm(EjdivEc, qdt.ft, qdt.Np, qdt.f0, qdt.epsinf, qdt.W, qdt.Dvv)
            print f_vec/h
            ah=-ls_fq2/2#-fq2)
            #fq_vec=array([sqrt((f-ah[n])*(f-ah[n]+alpha*calc_freq_shift(f-ah[n], qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for n, f in enumerate(self.frequency)])
            fq_vec=array([f/2-qdt.call_func("calc_Lamb_shift", fqq=f/2) for f in self.frequency])
            coup=qdt.call_func("calc_coupling", fqq=self.frequency)
            print coup
            volt=array([
              voltage_from_flux(arccos(Ej_from_fq(f-f_vec[c]/h/2, qdt.Ec)/Ejmax), offset, flux_factor)
              for c,f in enumerate(self.frequency)])
            #freq=nan_to_num(freq)/1e9
            #print freq
            freq=s3a4_wg.frequency[:]/1e9

            #freq=(s3a4_wg.frequency[:]+coup)/1e9
            #freq=append(freq, freq)
            #freq=append(freq, freq)
            #Ej=Ej_from_fq(fq_vec, f_vec/h)
            #flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
            #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
            #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax)+pi)
            #flux_d_flux0=append(flux_d_flux0, arccos(Ej/Ejmax)-pi)

            #freq=append(freq, freq)
            #fq_vec+=f_vec/h/2
            #fq2_vec=fq2(Ej, qdt.Ec)
            #Ej=Ej_from_fq(fq_vec, qdt.Ec) #qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
            #Ej=Ej_from_fq(fq_vec, qdt.Ec)
            #flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
            #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
            #volt=voltage_from_flux(flux_d_flux0, offset, flux_factor)
            line(freq, volt, plotter=pl, plot_name="second", color="green", linewidth=1.0, alpha=0.5)
        #flux_d_flux0.append(-)
        return voltage_from_flux(flux_d_flux0, offset, flux_factor)

    print shape(flux_par3(s3a4_wg, 0.0, 0.3, qdt.Ejmax))#, shape(self.frequency)
    def flux_par2(self, offset, flux_factor, Ejmax):
        set_all_tags(qdt, log=False)
        flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
        EjdivEc=Ej/qdt.Ec
        fq_vec=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
        results=[]
        for fq in fq_vec:
            def Ba_eqn(x):
                return x[0]**2+2.0*x[0]*qdt.call_func("calc_Lamb_shift", fqq=x[0])-fq**2
            results.append(fsolve(Ba_eqn, fq))
        return squeeze(results)/1e9

    #flux_par2(s3a4_wg, 0.0, 0.18, qdt.Ejmax)

    def flux_par(self, offset, flux_factor, Ejmax):
        set_all_tags(qdt, log=False)
    #    set_tag(qdt, "EjdivEc", log=False)
    #    set_tag(qdt, "Ej", log=False)
    #    set_tag(qdt, "offset", log=False)
    #    set_tag(qdt, "flux_factor", log=False)
        flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
        EjdivEc=Ej/qdt.Ec
        fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
        ls=qdt.call_func("calc_Lamb_shift", fqq=fq)
        return fq/1e9
        ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
        ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
        return ls_fq/1e9#, ls_fq2/1e9

    pl=magabs_colormesh(s3a4_wg).show()
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_colormap.png")
    flux_par4(s3a4_wg, pl=pl)#.show()#, f0=5.45e9, alpha=1.0)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_colormap_bothpar.png")

    #pl=line_cs(s3a4_wg, 190)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_5p4.pdf")
    #pl=line_cs(s3a4_wg, 210)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_5p6.pdf")
    #pl=line_cs(s3a4_wg, 239)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_5p89.pdf")
    #pl=line_cs(s3a4_wg, 246)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_5p96.pdf")
    #pl=line_cs(s3a4_wg, 256)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_cs_6p06.pdf")


    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_colormap_bothpar.png")
    pl.show()

    class Fitter(LineFitter):
        Ejmax=FloatRange(0.001, 100.0, qdt.Ejmax/h/1e9).tag(tracking=True)
        offset=FloatRange(-5.0, 5.0, 0.0).tag(tracking=True)
        flux_factor=FloatRange(0.1, 5.0, 0.3).tag(tracking=True)
        f0=FloatRange(4.0, 6.0, qdt.f0/1e9).tag(tracking=True)
        alpha=FloatRange(0.1, 2.0, 1.0).tag(tracking=True)

        def _default_plotter(self):
            if self.plot_name=="":
                self.plot_name=self.name
            freq=s3a4_wg.frequency[:]/1e9
            freq=append(freq, freq)
            freq=append(freq, freq)
            pl1, pf=line(freq, self.data, plot_name=self.plot_name, plotter=pl)
            self.plot_name=pf.plot_name
            return pl1

        @tag_Property(private=True)
        def data(self):
            return flux_par3(s3a4_wg, offset=self.offset, flux_factor=self.flux_factor, Ejmax=self.Ejmax*h*1e9, f0=self.f0*1e9, alpha=self.alpha)

    d=Fitter()
    d.show(d.plotter)

    #s3a4_wg
    #s3a4_mp.magabsfilt_colormesh("filtcolormesh S3A4 mp")
    #s3a4_mp.magdBfilt_colormesh("filtdB S1A4 wide")
    #s3a4_mp.magdBfiltbgsub_colormesh("filtdBbgsub S1A4 wide")
            #a2.filt_compare(a2.start_ind, bb2)
    #s3a4_mp.filt_compare("filt_compare_off_res", s3a4_mp.start_ind)
    #s3a4_mp.filt_compare("filt_compare_on_res", s3a4_mp.on_res_ind)
    #s3a4_mp.ifft_plot("ifft_S3A4 midpeak")
    #s3a4_mp.ifft_dif_plot("ifft__dif_S1A4 wide")

