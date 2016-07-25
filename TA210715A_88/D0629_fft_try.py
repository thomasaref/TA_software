# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Lyzer, TA88_Read, qdt
from taref.plotter.api import colormesh, line, Plotter
from taref.core.api import set_tag, set_all_tags
from numpy import array, absolute, real, imag, nan_to_num, squeeze, append, sqrt, pi, mod, floor_divide, trunc, arccos, shape, float64, linspace, reshape
from atom.api import FloatRange
from taref.core.api import tag_property
from taref.plotter.api import LineFitter
#from taref.physics.fitting import refl_lorent
from taref.physics.fundamentals import h
from scipy.optimize import fsolve
from h5py import File

from taref.physics.filtering import Filter

def read_data(self):
    with File(self.rd_hdf.file_path, 'r') as f:
        print f["Traces"].keys()
        Magvec=f["Traces"]["test_osc - Ch1 - Data"]
        data=f["Data"]["Data"]
        self.comment=f.attrs["comment"]
        self.yoko=data[:,0,0].astype(float64)
        fstart=f["Traces"]['test_osc - Ch1 - Data_t0dt'][0][0]
        fstep=f["Traces"]['test_osc - Ch1 - Data_t0dt'][0][1]

        print fstart, fstep

        print shape(Magvec), shape(self.yoko)
        sm=shape(Magvec)[0]
        sy=shape(data)
        #print sy
        s=(sm, sy[0], 1)#sy[2])
        Magcom=Magvec[:,0, :]#+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        self.MagcomData=squeeze(Magcom)
        print shape(self.MagcomData)
        self.stop_ind=len(self.yoko)-1

a=TA88_Lyzer( on_res_ind=240, filt=Filter(center=2, halfwidth=10, reflect=False),#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA88_Read(main_file="Data_0629/S4A4_just_gate_FFT_high_frq_n20dBm.hdf5"),
        fit_indices=[range(48,154+1), range(276, 578+1)],
        )
#a.filt.center=0
#a.filt.halfwidth=50
#a.filt.reflect=True
#, window_ifft, fir_filt_prep, fir_filter, fir_freqz, fft_filt_prep, fft_filter, ifft_x


from scipy.signal import decimate, resample
from numpy import exp, log10
from time import time

a.read_data()
#a.filt.center=26
#a.filt.halfwidth=10
a.fitter.fit_type="lorentzian"
a.fitter.gamma=0.035
a.flux_axis_type="flux"
a.bgsub_type="dB"
a.end_skip=10
a.flux_indices=[range(0,41), range(43, 479), range(482, len(a.yoko))]
#a.bgsub_type="Abs"
if __name__=="__main__":
    a.magabs_colormesh()#.show()
    pl1=line(a.freq_axis, a.MagAbs[:, 234])

    a.filter_type="FFT"

    a.ifft_plot_time()

    pl=a.magabs_colormesh()
    line(a.freq_axis[a.indices], a.MagAbs[:, 234], pl=pl1, color="red")

    a.filter_type="Fit"

    a.magabs_colormesh(pl=pl)
    #line(a.freq_axis, a.MagAbs[:, 234], pl=pl1, color="green")

    a.widths_plot()
    a.center_plot()
    a.heights_plot()
    a.background_plot().show()

    a.magabs_colormesh(bgsub_type="Complex").show()
    b=Filter(N=len(a.frequency), center=0, halfwidth=50, reflect=False)
    print b.start_ind, b.stop_ind
    tstart=time()
    data=array([b.fft_filter(a.Magcom[:,n])[10:-10] for n in range(len(a.yoko))])
    print tstart-time()
    colormesh(10*log10(absolute(data))-10*log10(absolute(data[0, :])))[0]

    #tstart=time()
    ##data=array([fft_filter(a.Magcom[:, n], -49, 50, reflect=False)[10:-10] for n in range(len(a.yoko))])
    print tstart-time()

    #data=array([fft_filter(data[n, :], 0, 20)[10:-10] for n in range(500)])

    colormesh(10*log10(absolute(data))-10*log10(absolute(data[0, :])))[0].show()

    a.ifft_plot()
    a.filter_type="FIR"
    a.magabs_colormesh()#.show()
    a.bgsub_type="MagdB"
    a.magabs_colormesh()
    a.bgsub_type="Complex"
    a.magabs_colormesh()
    a.bgsub_type="MagAbs"
    a.magabs_colormesh().show()

    #T = 1.0 / 800.0
    #x = np.linspace(0.0, N*T, N)
    #y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
    #>>> yf = fft(y)
    #>>> xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

    #    N=len(fs)
    #    df=1.0/(fs[1]-fs[0])/2.0
    #    return linspace(-df/2.0, df/2.0, N)

    t=a.frequency
    f=4.468e9
    data=fft_filter(a.Magcom[:, 25], 4380, 4550)
    #fd=fir_filter(data, 4380, 4550, numtaps=1000)

    data=data[10:-10]*exp(-2.0j*pi*f*t[10:-10])
    q=200
    wi=window_ifft(data, shift=True)

    data=decimate(data, q=q, ftype="fir")
    #wi=window_ifft(data, shift=True)
    xd=ifft_x(t, shift=True)[::q]/q
    line(absolute(wi))
    pl, pf=line(absolute(data))
    #pl.show()

    filt=fir_filt_prep(20003, 4380, 4550, numtaps=1000)
    ff2=filt2=filt_prep(20003, 4380, 4550, shift=False)
    ff=fir_freqz(filt, 20003, shift=False)

    #pl, pf=line(ifft_x(t, shift=False), absolute(wi))

    #pl, pf=line(xd, absolute(wi))
    print "hih"
    #data=array([fft_filter(a.Magcom[:, n], 4380, 4550)[10:-10] for n in range(len(a.yoko))])
    data=a.Magcom[10:-10].transpose()
    data2d=data*exp(-2.0j*pi*f*t[10:-10])
    data2d1=decimate(data2d, q=q, ftype="fir")
    print "ho"
    colormesh(absolute(data2d1))
    pl.show()
    data2d=resample(data2d, q, axis=1)
    colormesh(absolute(data2d))

    pl, pf=line(absolute(data2d[177, :]))
    line(absolute(data2d[0, :]), pl=pl, color="red")

    #line(ff2*max(absolute(wi)), pl=pl)
    pl.show()

    #fd=fir_filter(data, 4380, 4550, numtaps=1000)
    #fd2=fft_filter(data, 4380, 4550)

    line(fd, pl=pl, color="red")
    line(real(fd2), pl=pl, color="green")
    line(imag(fd2), pl=pl, color="purple")
    pl.show()
    a.ifft_plot()#.show()
    #a.filter_type="FIR"
    def filt_compare(self, ind):
        pl, pf=line(self.frequency, self.Magcom[:, ind], label="MagAbs (unfiltered)", plotter="filtcomp_{}".format(self.name))
        line(self.frequency, self.MagcomFilt[:, ind], label="MagAbs (filtered)", plotter=pl)
        return pl

    filt_compare(a, 25).show()

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

