# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Lyzer, TA88_Read#, qdt
from taref.plotter.api import colormesh, line, Plotter, scatter
from taref.core.api import set_tag, set_all_tags
from numpy import array, squeeze, append, sqrt, pi, mod, floor_divide, trunc, arccos, shape, linspace, interp, absolute, fft, log10, angle, unwrap
from atom.api import FloatRange
from taref.core.api import tag_property
from taref.plotter.api import LineFitter
from taref.physics.fundamentals import h#, filt_prep

from time import time
a=TA88_Lyzer(name="d0509", on_res_ind=256, VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0509/S1A4_lowfrq_trans_2_sidelobe.hdf5"),
            desc="S1A4 low frequency side lobe 2",
            #offset=-0.035,
            fit_indices=[range(93, 298+1)], #[range(30,580+1)]) #33, 70
            )
#print s3a4_wg.filt_center, s3a4_wg.filt_halfwidth, s3a4_wg.filt_start_ind, s3a4_wg.filt_end_ind
a.filt.center=28
a.filt.halfwidth=15
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.01
a.flux_axis_type="flux"
a.end_skip=10

a.save_folder.main_dir=a.name

if __name__=="__main__":
    pls=a.fft_plots()
    a.save_plots(pls)
    pls[0].show()

if __name__=="__main__":
    a.filter_type="FFT"
    pl=a.magabs_colormesh()
    a.filter_type="Fit"
    a.magabs_colormesh(pl=pl)
    a.ifft_plot()
    a.ifft_plot_time()
    #pl=a.magabs_colormesh()#magabs_colormesh3(s3a4_wg)
    #pl=a.hann_ifft_plot()
    #pl=a.ifft_plot()
    #a.filt_compare(a.on_res_ind)
    #filt=filt_prep(601, s3a4_wg.filt_start_ind, s3a4_wg.filt_end_ind)
    #line(filt*0.001, plotter=pl)
    #colormesh(s3a4_wg.MagAbsFilt)#, plotter="magabsfilt_{}".format(self.name))
    #pl=a.magabsfilt_colormesh()
    #line(a.frequency, a.ls_f)[0].show()
    a.widths_plot().show()
    a.center_plot()
    a.heights_plot()
    a.background_plot().show()
    a.magabsfilt_colormesh().show()
    #a.magdBfilt_colormesh()
    #a.magdBfiltbgsub_colormesh()

    def flux_par3(self, offset=-0.0, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.0, pl=None):
        #fq_vec=array([f-self.qdt._get_Lamb_shift(f=f, f0=f0) for f in self.frequency])
        fq_vec=array([sqrt(f*(f-2*self.qdt._get_Lamb_shift(f=f))) for f in self.frequency])
        Ej=self.qdt._get_Ej_get_fq(fq=fq_vec) #Ej_from_fq(fq_vec, qdt.Ec)
        flux_d_flux0=self.qdt._get_flux_over_flux0_get_Ej(Ej=Ej)
        #flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
        #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
        #flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax)+pi)
        #flux_d_flux0=append(flux_d_flux0, arccos(Ej/Ejmax)-pi)

        return self.qdt._get_voltage(flux_over_flux0=flux_d_flux0, offset=offset, flux_factor=flux_factor)

    def plot_widths(self, plotter=None):
        print "first fit"
        tstart=time()
        fq_vec=array([sqrt(f*(f-2*self.qdt._get_Lamb_shift(f=f))) for f in self.frequency])

        #fit_p=self.fano_fit(263, fq_vec)
        #print self.p_guess, fit_p

        #fit=lorentzian(fq_vec, fit_p[1:])
        #pl, pf=line(fq_vec, self.MagAbsFilt_sq[263, :])
        #line(fq_vec, fit, plotter=pl, color="red")
        #pl.show()
        fit_params=self.full_fano_fit(fq_vec)
        pl, pf=scatter(self.frequency, absolute(fit_params[1, :]), color="red", label=self.name, plot_name="widths_{}".format(self.name))

        line(self.frequency, self.qdt._get_coupling(self.frequency)+18e6, plotter=pl)

        pl, pf=scatter(self.frequency, fit_params[2, :], color="red", label=self.name, plot_name="widths_{}".format(self.name))
        line(self.frequency, fq_vec, #flux_par3(self),
        plotter=pl)
        print "fit second", tstart-time()
        tstart=time()

        fq_vec=array([sqrt(f*(f-2*self.qdt._get_Lamb_shift(f=f))) for f in self.frequency])

        pl, pf = scatter(fit_params[2, :], fq_vec, color="red")
        #flux_d_flux0=self.qdt._get_flux_over_flux0(voltage=self.yoko, offset=0.0)
        fq=self.qdt._get_flux_parabola(voltage=self.yoko, offset=0.0)
        line(self.yoko, fq, plotter=pl)
        #fit_params=self.full_fano_fit2()
        #def rpt_fit2(self):
        #    MagAbsFilt_sq=self.MagAbsFilt**2
        #    return rpt_fit(lorentzian2, self.p_guess, MagAbsFilt_sq[440, :], self.yoko)
        #fit2_p=rpt_fit2(self)
        #print fit2_p
        #fit2=lorentzian2(self.yoko, *fit2_p)
        #line(self.yoko, fit2, plotter=pl, color="green")
        #scatter(absolute(fit_params[1, :]), color="red", label=self.name, plot_name="widths_{}".format(self.name))
        print "fit third", tstart-time()
        tstart=time()
        #fit_params=self.full_fano_fit3()
        #scatter(absolute(fit_params[1, :]), color="red", label=self.name, plot_name="widths_{}".format(self.name))
        print "fit done", tstart-time()

    #flux_par3(s3a4_wg, pl=pl)
    #magfilt_cmesh(s3a4_wg)
    #ifft_plot(s3a4_wg)
    print "start"
    #fit_params=s3a4_wg.full_fano_fit2()
    print "done"
    #scatter(absolute(fit_params[1, :]))
    plot_widths(a)
    pl.show()


    def magabs_colormesh2(self, f0=5.35e9, alpha=0.45, pl=None):
        fq_vec=array([sqrt(f*(f-2*qdt.call_func("Lamb_shift", f=f, f0=f0, couple_mult=alpha))) for f in self.frequency])
        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
        pl, pf=colormesh(self.yoko, fq_vec/1e9, (self.MagdB.transpose()-self.MagdB[:, 0]).transpose(), plotter=pl)
        pf.set_clim(-0.3, 0.1)
        pl.set_ylim(min(fq_vec/1e9), max(fq_vec/1e9))
        pl.set_xlim(min(self.yoko), max(self.yoko))

        pl.ylabel="Yoko (V)"
        pl.xlabel="Frequency (GHz)"
        return pl

    def magabs_colormesh3(self, f0=5.35e9, alpha=0.45, pl=None):
        fq_vec=array([sqrt(f*(f-2*qdt.call_func("Lamb_shift", f=f, f0=f0, couple_mult=alpha))) for f in self.frequency])
        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
        pl, pf=colormesh(self.yoko, self.frequency/1e9, absolute((self.Magcom.transpose()-self.Magcom[:, 0]).transpose()), plotter=pl)
        #pf.set_clim(-0.3, 0.1)
        #pl.set_ylim(min(fq_vec/1e9), max(fq_vec/1e9))
        #pl.set_xlim(min(self.yoko), max(self.yoko))

        pl.ylabel="Yoko (V)"
        pl.xlabel="Frequency (GHz)"
        return pl

    def ifft_plot(self):
        Magcom=(self.Magcom.transpose()-self.Magcom[:, 0]).transpose()
        p, pf=line(absolute(fft.ifft(Magcom[:,self.on_res_ind])), plotter="ifft_{}".format(self.name),
               plot_name="onres_{}".format(self.on_res_ind),label="i {}".format(self.on_res_ind))
        line(absolute(fft.ifft(Magcom[:,self.start_ind])), plotter=p,
             plot_name="strt {}".format(self.start_ind), label="i {}".format(self.start_ind))
        line(absolute(fft.ifft(Magcom[:,self.stop_ind])), plotter=p,
             plot_name="stop {}".format(self.stop_ind), label="i {}".format(self.stop_ind))

    def new_flux(self, offset=-0.07, flux_factor=0.16, Ejmax=h*43.0e9, C=qdt.Ct, pl=None):
        flx_d_flx0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        Ec=qdt.call_func("Ec", Cq=C)
        qEj=qdt.call_func("Ej", Ejmax=Ejmax, flux_over_flux0=flx_d_flx0)

        E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=qEj/Ec, Ec=Ec, n_energy=3)
        fq=(E1-E0)/h
        pl, pf=line(self.yoko, fq/1e9, plotter=pl, linewidth=1.0)

        qdt.couple_mult=0.55*3
        EjdivEc=linspace(0.1, 300, 3000)
        E0p, E1p, E2p=qdt.call_func("lamb_shifted_transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
        ls_fq=(E1p-E0p)/h
        ls_fq2=(E2p-E1p)/h
        ls_fq20=(E2p-E0p)/h
        anharm=ls_fq2-ls_fq
        anh=interp(fq, ls_fq, ls_fq20)
        pl, pf=line(self.yoko, anh/1e9/2, plotter=pl, linewidth=1.0)

        return pl

    def line_cs2(self, ind=210, f0=5.35e9, alpha=0.45):
        fq_vec=array([sqrt(f*(f-2*qdt.call_func("Lamb_shift", f=f, f0=f0, couple_mult=alpha))) for f in self.frequency])
        print self.frequency[ind]/1e9, fq_vec[ind]/1e9
        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_cs_{}".format(self.name))
        pl, pf=line(self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0])[:, ind], plotter=pl, linewidth=1.0)
        pl.xlabel="Yoko (V)"
        pl.ylabel="Magnitude (dB)"
        return pl

    def magabs_colormesh(self):
        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
        pl, pf=colormesh(self.frequency/1e9, self.yoko, (self.MagdB.transpose()-self.MagdB[:, 0]), plotter=pl)
        pf.set_clim(-0.3, 0.1)
        pl.set_xlim(min(self.frequency/1e9), max(self.frequency/1e9))
        pl.set_ylim(min(self.yoko), max(self.yoko))

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

    #from taref.physics.qubit import  flux_parabola, Ej_from_fq, voltage_from_flux
    #from taref.physics.qdt import lamb_shifted_anharm, calc_freq_shift

    def fq2(Ej, Ec):
        E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
        #E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)
        E2 =  sqrt(8.0*Ej*Ec)*2.5 - (Ec/12.0)*(6.0*2**2+6.0*2+3.0)
        return (E2-E0)/h/2

    def Ej_from_fq2(fq2, Ec):
        return (((2*h*fq2+3.0*Ec)/2.0)**2)/(8.0*Ec)

    def flux_par3(self, offset=-0.07, flux_factor=0.52, Ejmax=h*44.0e9, f0=5.35e9, alpha=0.0, C=qdt.Ct, pl=None):
        set_all_tags(qdt, log=False)
        #flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
        #print flux_o_flux0-pi/2*trunc(flux_o_flux0/(pi/2.0))
        #Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
        #EjdivEc=Ej/qdt.Ec
        #fq_vec=array([sqrt(f*(f+1.0*qdt.call_func("calc_Lamb_shift", fqq=f))) for f in self.frequency])
        fq_vec=array([f-qdt.call_func("Lamb_shift", f=f, f0=f0) for f in self.frequency])
        fq_vec=array([sqrt(f*(f-2*qdt.call_func("Lamb_shift", f=f, f0=f0, couple_mult=alpha))) for f in self.frequency])
        Ec=qdt.call_func("Ec", Cq=C)
        Ej=qdt._get_Ej(fq=fq_vec, Ec=Ec) #Ej_from_fq(fq_vec, qdt.Ec)
        flux_d_flux0=arccos(Ej/Ejmax)#-pi/2
        flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax))
        flux_d_flux0=append(flux_d_flux0, -arccos(Ej/Ejmax)+pi)
        flux_d_flux0=append(flux_d_flux0, arccos(Ej/Ejmax)-pi)

        if pl is not None:
            volt=qdt._get_voltage(flux_over_flux0=flux_d_flux0, offset=offset, flux_factor=flux_factor)
            freq=s3a4_wg.frequency[:]/1e9
            freq=append(freq, freq) #append(freq, append(freq, freq)))
            freq=append(freq, freq)
            #freq=append(freq, freq)
            line(freq, volt, plotter=pl, linewidth=1.0, alpha=0.5)
            #EjdivEc=Ej/qdt.Ec
            #ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
            #E0, E1, E2=qdt.call_func("transmon_energy_levels", EjdivEc=EjdivEc, n_energy=3)
            #fq2=(E2-E1)/h
            #f_vec=lamb_shifted_anharm(EjdivEc, qdt.ft, qdt.Np, qdt.f0, qdt.epsinf, qdt.W, qdt.Dvv)
            #ah=-ls_fq2/2#-fq2)
            #fq_vec=array([sqrt((f-ah[n])*(f-ah[n]+alpha*calc_freq_shift(f-ah[n], qdt.ft, qdt.Np, f0, qdt.epsinf, qdt.W, qdt.Dvv))) for n, f in enumerate(self.frequency)])
            #fq_vec=array([f/2-qdt.call_func("calc_Lamb_shift", fqq=f/2) for f in self.frequency])

            #freq=(s3a4_wg.frequency[:]-1.45e9)/1e9
            #freq=append(freq, freq)
            #freq=append(freq, freq)
            #Ej=Ej_from_fq(fq_vec, qdt.Ec)
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
            #line(freq, volt, plotter=pl, plot_name="second", color="green", linewidth=1.0, alpha=0.5)
        #flux_d_flux0.append(-)
        return qdt._get_voltage(flux_over_flux0=flux_d_flux0, offset=offset, flux_factor=flux_factor)

    #print shape(flux_par3(s3a4_wg, 0.0, 0.3, qdt.Ejmax))#, shape(self.frequency)
    #def flux_par2(self, offset, flux_factor, Ejmax):
    #    set_all_tags(qdt, log=False)
    #    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    #    Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
    #    EjdivEc=Ej/qdt.Ec
    #    fq_vec=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    #    results=[]
    #    for fq in fq_vec:
    #        def Ba_eqn(x):
    #            return x[0]**2+2.0*x[0]*qdt.call_func("calc_Lamb_shift", fqq=x[0])-fq**2
    #        results.append(fsolve(Ba_eqn, fq))
    #    return squeeze(results)/1e9
    #
    ##flux_par2(s3a4_wg, 0.0, 0.18, qdt.Ejmax)
    #
    #def flux_par(self, offset, flux_factor, Ejmax):
    #    set_all_tags(qdt, log=False)
    ##    set_tag(qdt, "EjdivEc", log=False)
    ##    set_tag(qdt, "Ej", log=False)
    ##    set_tag(qdt, "offset", log=False)
    ##    set_tag(qdt, "flux_factor", log=False)
    #    flux_o_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=offset, flux_factor=flux_factor)
    #    Ej=qdt.call_func("Ej", flux_over_flux0=flux_o_flux0, Ejmax=Ejmax)
    #    EjdivEc=Ej/qdt.Ec
    #    fq=qdt.call_func("fq", Ej=EjdivEc*qdt.Ec)
    #    ls=qdt.call_func("calc_Lamb_shift", fqq=fq)
    #    return fq/1e9
    #    ls_fq=qdt.call_func("lamb_shifted_fq", EjdivEc=EjdivEc)
    #    ls_fq2=qdt.call_func("lamb_shifted_fq2", EjdivEc=EjdivEc)
    #    return ls_fq/1e9#, ls_fq2/1e9
    from taref.physics.fundamentals import fft_filter
    def magfilt_cmesh(self, f0=5.35e9, alpha=0.45):
        Magcom=self.Magcom #(self.Magcom.transpose()-self.Magcom[:, 0]).transpose()
        fq_vec=self.frequency #array([sqrt(f*(f-2*qdt.call_func("Lamb_shift", f=f, f0=f0, couple_mult=alpha))) for f in self.frequency])

        Magfilt=array([fft_filter(Magcom[:,n], self.filt_start_ind, self.filt_end_ind) for n in range(len(self.yoko))]).transpose()
        Magfilt2=array([fft_filter(Magcom[:,n], 0, 34) for n in range(len(self.yoko))]).transpose()

        pl=Plotter(fig_width=9.0, fig_height=6.0, name="magabs_{}".format(self.name))
        pl, pf=colormesh(self.yoko, fq_vec/1e9, (absolute(Magfilt.transpose()-0.0*Magfilt[:,0])).transpose(), plotter=pl)


    if __name__=="__main2__":
        pl=magabs_colormesh3(s3a4_wg)
        #flux_par3(s3a4_wg, pl=pl)
        magfilt_cmesh(s3a4_wg)
        ifft_plot(s3a4_wg)
        print "start"
        fit_params=s3a4_wg.full_fano_fit2()
        print "done"
        scatter(absolute(fit_params[1, :]))
        s3a4_wg.plot_widths()
        pl.show()
        #new_flux(s3a4_wg, pl=pl).show()
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_colormap.png")
    #flux_par3(s3a4_wg, pl=pl)#.show()#, f0=5.45e9, alpha=1.0)
    #pl.savefig(dir_path="/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Graphs_0425/",
    #           fig_name="wide_gate_colormap_bothpar.png")
    #pl=line_cs2(s3a4_wg, ind=156)

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
    print qdt.Ct, qdt.Cq
    pl.show()

    class Fitter(LineFitter):
        Ejmax=FloatRange(0.001, 100.0, qdt.Ejmax/h/1e9).tag(tracking=True)
        offset=FloatRange(-5.0, 5.0, 0.0).tag(tracking=True)
        flux_factor=FloatRange(0.1, 5.0, 0.3).tag(tracking=True)
        f0=FloatRange(4.0, 6.0, qdt.f0/1e9).tag(tracking=True)
        alpha=FloatRange(0.0, 2.0, 0.0*qdt.couple_mult).tag(tracking=True)
        Ct=FloatRange(0.1, 10.0, 1.3).tag(tracking=True)

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
            return flux_par3(s3a4_wg, offset=self.offset, flux_factor=self.flux_factor,
                             C=self.Ct*1e-13, Ejmax=self.Ejmax*h*1e9, f0=self.f0*1e9, alpha=self.alpha)

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

