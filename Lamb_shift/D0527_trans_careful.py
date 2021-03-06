# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_VNA_Lyzer, TA88_Read, idt, bg_A1, bg_A4#, qdt
from taref.plotter.api import colormesh, line, Plotter, scatter
from taref.core.api import set_tag, set_all_tags, get_all_tags, get_tag
from numpy import sin, reshape, amax, exp, array, squeeze, append, sqrt, pi, mod, floor_divide, trunc, arccos, shape, linspace, interp, absolute, fft, log10, angle, unwrap
from atom.api import FloatRange, Int, Float, Typed, Unicode
from taref.core.api import tag_property, process_kwargs
#from taref.core.universal import ODict
from h5py import File
from taref.plotter.api import LineFitter
from taref.physics.fundamentals import h#, filt_prep
from taref.physics.idt import IDT
from time import time

def read_data(self):
    with File(self.rd_hdf.file_path, 'r') as f:
        Magvec=f["Traces"]["{0} - {1}".format(self.VNA_name, self.port_name)]
        data=f["Data"]["Data"]
        print data.shape
        print Magvec.shape
        #if self.swp_type=="pwr_first":
        #    self.pwr=data[:, 0, 0].astype(float64)
        #    self.yoko=data[0,1,:].astype(float64)
        #elif self.swp_type=="yoko_first":
        #    self.pwr=data[0, 1, :].astype(float64)
        #    self.yoko=data[:, 0, 0].astype(float64)
        self.comment=f.attrs["comment"]
        fstart=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][0]
        fstep=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][1]

        sm=shape(Magvec)[0]
        sy=shape(data)
        s=(sm, sy[0], sy[2])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        #if self.swp_type=="pwr_first":
        #    Magcom=swapaxes(Magcom, 1, 2)
        self.MagcomData=squeeze(Magcom)#[:, 2, :]
        print self.MagcomData.shape
        #self.stop_ind=len(self.yoko)-1
        self.filt.N=len(self.frequency)

a=TA88_VNA_Lyzer( name="d0527", on_res_ind=0, VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0527/S1A4_careful_trans.hdf5"),
            offset=0.07,
            #fit_type="yoko",
            rt_atten=30.0,#indices=range(50, 534),
            read_data=read_data,
            ) #33, 70
#print s3a4_wg.filt_center, s3a4_wg.filt_halfwidth, s3a4_wg.filt_start_ind, s3a4_wg.filt_end_ind

a.filt.center=731
a.filt.halfwidth=200
a.save_folder.main_dir=a.name
b=TA88_VNA_Lyzer(on_res_ind=0, VNA_name="RS VNA",
              rd_hdf=TA88_Read(main_file="Data_0531/S4A4_careful_unswitched.hdf5"),
            offset=0.07,
            #fit_type="yoko",
            rt_atten=30.0,#indices=range(50, 534),
            read_data=read_data,
            ) #33, 70
b.filt.center=0
b.filt.halfwidth=200
#def bg_A4(frequency):
#    return interp(frequency, b.frequency, 20*log10(absolute(b.MagcomData[:, 0])))


def ifft_plot(self, **kwargs):
    process_kwargs(self, kwargs, pl="hannifft_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
    on_res=10*log10(absolute(self.filt.window_ifft(self.MagcomData[:,0])))

    pl=line(self.time_axis-0.05863, self.filt.fftshift(on_res),  color="purple",
           plot_name="onres_{}".format(self.on_res_ind), alpha=0.8, label="IFFT", **kwargs)

    self.filt.N=len(on_res)
    filt=self.filt.freqz
    #filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
    top=36.0#amax(on_res)
    line(self.time_axis-0.05863, filt*top-70, plotter=pl, color="green",
         linestyle="dotted", label="Filter window")
    pl.xlabel=kwargs.pop("xlabel", self.time_axis_label)
    pl.ylabel=kwargs.pop("ylabel", "Mag abs")

    scatter(array([0.05863,   0.2,  0.337,   0.48,  0.761, 1.395, 1.455])-0.05863,
            array([0.0, 500.0, 1000.0, 1500.0, 2500.0, 4500,  200+2500+2500-300])/100.0-60,
            marker_size=4.0, pl=pl, label="IFFT peak")
    t=linspace(0,2,1001) #self.time_axis-0.05863
    line(t, 3488.0*t/100.0-60, pl=pl, color="black", linestyle="dashed", auto_xlim=False, x_min=-0.2, x_max=1.0,
         auto_ylim=False, y_min=-65, y_max=-15, label="$d=v_ft$")

    t=array([8.7e-8, 2.64e-7, 3.79e-7, 4.35e-7, 6.6e-7])-8.7e-8
    scatter(t*1e6, array([0.0, 600.0, 1000.0, 1200.0, 2000.0])/100.0-60, pl=pl,
            facecolor="red", edgecolor="red", label="100 ns pulse",
            marker_size=4.0)
    pl.legend()
    #b.line_plot("spd_fit", t*1e6,  (t*qdt.vf)*1e6, label="(3488 m/s)t")

    return pl

def MagcomFilt(self):
    if self.filt.filter_type=="FIR":
        return self.filt.fir_filter(self.MagcomData[:, 0])
    return self.filt.fft_filter(self.MagcomData[:, 0])

if __name__=="__main__":
    a.read_data()
    b.read_data()

    a.filter_type="None"
    a.time_axis_type="time"
    print a.MagAbs.shape
    def bg(x):
        return bg_A4(x)
        return interp(x, b.frequency, 20*log10(absolute(b.MagcomData[:, 0])))
    pl=line(a.frequency, 20*log10(absolute(a.MagcomData[:, 0]))-bg(a.frequency), color="cyan")#.show()
    bg_pl=line(b.frequency, 20*log10(absolute(b.MagcomData[:, 0])), color="cyan")#.show()
    line(b.frequency, 20*log10(absolute(b.MagcomData[:, 1])), color="red", pl=bg_pl)#.show()
    line(b.frequency, bg(a.frequency), color="green", pl=bg_pl)#.show()
    line(b.frequency, 20*log10(absolute(MagcomFilt(b))), pl=bg_pl, color="purple")
    print b.comment

    #pl=line(a.frequency, 10*log10(absolute(a.MagcomData[:, 1])))#.show()

    #pl=line(a.frequency, a.MagdB)#.show()

    magfilt=MagcomFilt(a)
    magabs=absolute(magfilt)
    line(a.frequency, magabs)
    nskip=50
    pl=scatter(a.frequency[::nskip], 20.0*log10(magabs[::nskip])-bg(a.frequency[::nskip]), facecolor="red", edgecolor="red", pl=pl)
    #idt.Np=56
    #idt.f0=4.46e9 #4.452
    #idt.K2=0.032
    idt.Np=36.5
    #idt.f0=4.452e9



    (S11, S12, S13,
     S21, S22, S23,
     S31, S32, S33)=idt._get_simple_S(f=a.frequency)
    print idt.Np, idt.K2
    print idt.f0
    print a.comment
    print -a.fridge_atten+a.fridge_gain-a.rt_atten+a.rt_gain-10

    line(a.frequency, 20*log10(absolute(S13*S31))-4*1, color="green", pl=pl,
         auto_ylim=False, y_min=-40, y_max=-10*0,
         auto_xlim=False, x_min=4e9, x_max=5e9, xlabel="Frequency (Hz)", ylabel="Transmission (dB)",
        title="Pickup IDT (37 fingers)")#.show()

    line(a.frequency, angle(magfilt))

    X=idt.Np*pi*(a.frequency-idt.f0)/idt.f0

    #line(a.frequency, 20*log10(0.5*(sin(X)/(X))**2), pl=pl)


    ifft_plot(a)#.show()

    from D0317_S4A1_frq_pulse_flux import a as c
    from numpy import mean
    c.read_data()
    print c.comment
    cdata=10.0**((20.0*log10(mean(absolute(c.MagcomData[64:76, :, 0]), axis=0))-c.probe_pwr)/20.0)
    pl=scatter(c.frequency, 20*log10(cdata)+10-1.0-bg_A1(c.frequency),
            pl=pl, color="purple", marker="x")

    #pl=scatter(c.frequency, 20*log10(mean(absolute(c.MagcomData[64:76, :, 0]), axis=0))+0*8.5-bg(c.frequency),
    #        pl=pl, color="purple", marker="x")

    #a.save_plots([pl,])
    pl.show()

if __name__=="__main__":

    #b.filt_compare(a.on_res_ind)
    print a.net_loss, a.rt_atten
    #pl=a.magabs_colormesh()#magabs_colormesh3(s3a4_wg)
    #pl=a.hann_ifft_plot()
    pl=a.ifft_plot()#.show()
    pl=a.filt_compare(a.on_res_ind)#.show()
    #line(a.frequency, 20*log10(absolute(idt._get_S13(f=a.frequency))), plotter=pl)[0].show()

    class IDTFitter(IDT):
        base_name="idt_fitter"

        plotter=Typed(Plotter).tag(private=True)
        plot_name=Unicode().tag(private=True)
        data_dict=ODict().tag(private=True)

        def __setattr__(self, name, value):
            super(IDTFitter, self).__setattr__(name, value)
            self.update_plot(dict(type="update"))

        def _default_plotter(self):
            if self.plot_name=="":
                self.plot_name=self.name
            pl=Plotter(name=self.name)
            for param in get_all_tags(self, "plot"):
                print param
                pl, pf=line(*getattr(self, param), plot_name=get_tag(self, param, "plot"), plotter=pl, pf_too=True)
                self.data_dict[param]=pf.plot_name
            return pl

        def update_plot(self, change):
            if change["type"]=="update":
                print self.data_dict
                for param, plot_name in self.data_dict.iteritems():
                    print param, plot_name
                    self.get_member(param).reset(self)
                    self.plotter.plot_dict[plot_name].alter_xy(*getattr(self,param))

        @tag_property(private=True)
        def frequency(self):
            return linspace(3.5e9, 7.5e9, 1000)

        @tag_property(private=True, plot="flux_par")
        def data(self):
            (S11, S12, S13,
             S21, S22, S23,
             S31, S32, S33)=self._get_simple_S(f=self.frequency)
            return self.frequency, 20*log10(absolute(S13))

    idt=IDTFitter(name="fitting_idt",
            material='LiNbYZ',
            ft="double",
            a=96.0e-9, #f0=5.35e9,
            Np=36,
            W=25.0e-6,
            eta=0.5,
            plot_name="transmission")
    #qdt.f0=5.32e9 #5.35e9
    #idt.fixed_freq_max=20.0*idt.f0

    #qdt.Ct=1.25e-13
    #idt.K2=0.038
    idt.S_type="simple"
    #qdt.couple_type="sinc^2"
    #qdt.Lamb_shift_type="formula"
    #qdt.Np=9.5
    pl1=idt.plotter
    line(a.frequency, a.MagdB[:, 0]+8.26+3, linewidth=0.5, pl=pl1, color="red").show()

    from taref.plotter.fitter import LineFitter2

    class Fitter(LineFitter2):
        Np=Float(a.idt.Np)#.tag(tracking=True)
        f0=Float(a.idt.f0/1e9)#.tag(tracking=True)
        loss=Float( -11.0)#.tag(tracking=True)
        L=FloatRange(400.0, 600.0, 500.0).tag(tracking=True)
        dloss1=Float(0.0)
        dloss2=Float(0.0)
        C=Float(a.idt.C)
        K2=Float(a.idt.K2)
        dL=Float(a.idt.dL)
        eta=Float(a.idt.eta)


        def _default_plotter(self):
            line(*self.data, plot_name=self.plot_name, plotter=pl, color="green", linewidth=0.3, alpha=0.6)
            return pl

        def _default_plot_name(self):
            return "myplot"

        @tag_property(private=True)
        def data(self):
            return a.frequency, 20*log10(absolute(exp(-1j*2*pi*a.frequency/a.idt.vf*self.L*1e-6)*a.qdt._get_propagation_loss(f0=self.f0*1e9, dloss1=self.dloss1, dloss2=self.dloss2)*a.idt._get_S13(f=a.frequency,
                                                  f0=self.f0*1e9, Np=self.Np, C=self.C, K2=self.K2, dL=self.dL, eta=self.eta)))+self.loss

    d=Fitter()
    d.plotter.show()
    #filt=filt_prep(601, s3a4_wg.filt_start_ind, s3a4_wg.filt_end_ind)
    #line(filt*0.001, plotter=pl)
    colormesh(a.MagAbsFilt)[0].show()#, plotter="magabsfilt_{}".format(self.name))

    a.magabsfilt_colormesh().show()
    #a.magabsfit_colormesh(pl=pl)
    #pl=a.magphasefilt_colormesh().show()
    #a.magabsfilt2_colormesh()
    a.widths_plot()
    pl=a.center_plot()
    a.heights_plot()
    a.background_plot()#.show()

    from taref.plotter.fitter import LineFitter2

    class Fitter(LineFitter2):
        Ejmax=Float(a.qdt.Ejmax/h/1e9)#.tag(tracking=True)
        offset=Float(a.offset)#.tag(tracking=True)
        flux_factor=Float(a.flux_factor)#.tag(tracking=True)
        f0=Float(a.qdt.f0/1e9)#.tag(tracking=True)
        alpha=Float( 1.0)#.tag(tracking=True)
        Ct=Float(a.qdt.C*1e13)#.tag(tracking=True)

        def _default_plotter(self):
            line(*self.data, plot_name=self.plot_name, plotter=pl, color="green", linewidth=0.3, alpha=0.6)
            return pl

        def _default_plot_name(self):
            return "myplot"

#        @tag_property(private=True)
#        def freq(self):
#            freq=append(a.frequency, a.frequency)
#            freq=append(freq, freq)
#            return freq


        @tag_property(private=True)
        def data(self):
            ls_f=array([sqrt(f*(f-self.alpha*2*a.qdt._get_Lamb_shift(f=f, f0=self.f0*1e9))) for f in a.frequency])#, couple_mult, K2, Np)
            Ec=a.qdt._get_Ec(C=self.Ct*1e-13)
            Ej=a.qdt._get_Ej_get_fq(fq=ls_f, Ec=Ec)
            flux_d_flux0=a.qdt._get_flux_over_flux0_get_Ej(Ej=Ej, Ejmax=self.Ejmax*h*1e9)
            #flux_d_flux0=append(fdf0, -fdf0)
            #flux_d_flux0=append(flux_d_flux0, -fdf0+pi)
            #flux_d_flux0=append(flux_d_flux0, fdf0-pi)
            return a.frequency/1e9, a.qdt._get_voltage(flux_over_flux0=flux_d_flux0, offset=self.offset, flux_factor=self.flux_factor)

            #return flux_par3(s3a4_wg, offset=self.offset, flux_factor=self.flux_factor,
            #                 C=self.Ct*1e-13, Ejmax=self.Ejmax*h*1e9, f0=self.f0*1e9, alpha=self.alpha)

    d=Fitter()
    d.plotter.show()

    #colormesh(plotter=pl)
    #a.magdBfilt_colormesh()
    #a.magdBfiltbgsub_colormesh()#[0].show()


    from taref.plotter.fitter import LineFitter

    class Indexer(LineFitter):
        ind=Int(263).tag(spec="spinbox")

        @tag_property(plot="lorentx", sub=True)
        def data(self):
            fit_p=a.fano_fit(self.ind, a.fq)
            #print a.p_guess, fit_p
            return a.fq, lorentzian(a.fq, fit_p)

        @tag_property(plot="adata", sub=True)
        def adata(self):
            print a.MagAbsFilt_sq[self.ind, -1]
            return a.fq, a.MagAbsFilt_sq[self.ind, :]

        @tag_property(plot="adata2", sub=True)
        def adata2(self):
            print a.MagAbsFilt_sq[260, 50]
            return a.fq, a.MagAbsFilt_sq[260, :]

    d=Indexer()
    d.plotter
    #d.ind=230
    #for param, plot_name in d.data_dict.iteritems():
    #    print param, plot_name
    #    d.get_member(param).reset(d)
    #    if param=="adata":
    #        d.plotter.plot_dict[plot_name].alter_xy(*getattr(d,param))

    #from taref.core.api import get_all_tags
    #pl=None
    #for param in get_all_tags(d, "plot"):
    #    print param
    #    pl, pf=line(*getattr(d, "adata"), plot_name="adad", plotter=pl)

    #print d.adata
    d.show()

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

        fit_p=self.fano_fit(263, self.fq)
        print self.p_guess, fit_p

        fit=lorentzian(self.fq, fit_p[1:])
        pl, pf=line(self.fq, self.MagAbsFilt_sq[263, :])
        line(self.fq, fit, plotter=pl, color="red")
        pl.show()
        fit_params=self.full_fano_fit(self.fq)
        pl, pf=scatter(self.frequency, absolute(fit_params[1, :]), color="red", label=self.name, plot_name="widths_{}".format(self.name))

        line(self.frequency, self.qdt._get_coupling(self.frequency)+0*18e6, plotter=pl)

        #pl, pf=scatter(self.frequency, fit_params[2, :], color="red", label=self.name, plot_name="widths_{}".format(self.name))
        #line(self.frequency, fq_vec, #flux_par3(self),
        #plotter=pl)
        print "fit second", tstart-time()
        tstart=time()

        #fq_vec=array([sqrt(f*(f-2*self.qdt._get_Lamb_shift(f=f))) for f in self.frequency])

        #pl, pf = scatter(fit_params[2, :], fq_vec, color="red")
        #flux_d_flux0=self.qdt._get_flux_over_flux0(voltage=self.yoko, offset=0.0)
        #fq=self.qdt._get_flux_parabola(voltage=self.yoko, offset=0.0)
        #line(self.yoko, fq, plotter=pl)
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

