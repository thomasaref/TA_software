# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:46:49 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read, TA88_Fund, qdt
from atom.api import Typed, Unicode, Float, observe, FloatRange, Int
from h5py import File
from taref.core.universal import Array
from numpy import float64, linspace, shape, reshape, squeeze, mean, angle, absolute, sin, pi
from taref.core.atom_extension import tag_Property
from taref.physics.units import dB
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from taref.core.agent import Operative
from taref.core.log import log_debug
from taref.physics.fundamentals import e, h
from scipy.optimize import leastsq

class Fitter(Operative):
     offset=FloatRange(-1.0, 1.0, -0.035).tag(tracking=True)
     flux_factor=FloatRange(0.01, 1.0, 0.2925).tag(tracking=True)

     @tag_Property(plot=True, private=True)
     def flux_parabola(self):
        flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)
        Ej=qdt.call_func("Ej", flux_over_flux0=flux_over_flux0)
        return qdt._get_fq(Ej, qdt.Ec)
         #return qdt.flux_parabola(voltage=self.yoko, offset=self.offset, flux_factor=self.flux_factor)

     yoko=Array().tag(unit="V", plot=True, label="Yoko", private=True)

     plotter=Typed(Plotter).tag(private=True)

     @observe("offset", "flux_factor")
     def update_plot(self, change):
         if change["type"]=="update":
             self.get_member("flux_parabola").reset(self)
             self.plotter.plot_dict["flux_parabola"].clt.set_ydata(self.flux_parabola)

             self.plotter.draw()

class Lyzer(TA88_Fund):
    rd_hdf=Typed(TA88_Read)

    comment=Unicode().tag(read_only=True, spec="multiline")

    rt_atten=Float(40)

    rt_gain=Float(23*2)

    frequency=Array().tag(unit="GHz", plot=True, label="Frequency")
    yoko=Array().tag(unit="V", plot=True, label="Yoko")
    Magcom=Array().tag(private=True)

    probe_frq=Float().tag(unit="GHz", label="Probe frequency", read_only=True)
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")

    pind=Int()


    @tag_Property(display_unit="dB", plot=True)
    def MagdB(self):
        return self.Magcom[:, :]/dB-mean(self.Magcom[:, 169:171], axis=1, keepdims=True)/dB

    @tag_Property(plot=True)
    def Phase(self):
        return angle(self.Magcom[:, :]-mean(self.Magcom[:, 169:170], axis=1, keepdims=True))

    @tag_Property( plot=True)
    def MagAbs(self):
        #return absolute(self.Magcom[:, :])
        return absolute(self.Magcom[:, :])**2#-mean(self.Magcom[:, 0:1], axis=1, keepdims=True))


    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0315/S1A1_TA88_coupling_search_midpeak.hdf5") #"Data_0312/S4A1_TA88_coupling_search.hdf5")

    def read_data(self):
        with File(self.rd_hdf.file_path, 'r') as f:
            print f["Traces"].keys()
            self.comment=f.attrs["comment"]
            print f["Instrument config"].keys()
            self.probe_frq=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs["Start frequency"]
            self.probe_pwr=f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs["Output power"]
            print f["Instrument config"]['Rohde&Schwarz Network Analyzer - IP: 169.254.107.192, RS VNA at localhost'].attrs
#
            print f["Data"]["Channel names"][:]
            Magvec=f["Traces"]["RS VNA - S21"]#[:]
            data=f["Data"]["Data"]
            print shape(data)
#
            self.yoko=data[:,0,0].astype(float64)
            fstart=f["Traces"]['RS VNA - S21_t0dt'][0][0]
            fstep=f["Traces"]['RS VNA - S21_t0dt'][0][1]
            print shape(Magvec)
            sm=shape(Magvec)[0]
            sy=shape(data)
            s=(sm, sy[0], 1)#sy[2])
            print s
            Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]

            Magcom=reshape(Magcom, s, order="F")
            self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            print shape(Magcom)
            self.Magcom=squeeze(Magcom)
        with File("/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A88_cooldown210216/Data_0308/S1A4_TA88_coupling_search_midpeak.hdf5", "r") as f:
            Magvec=f["Traces"]["RS VNA - S21"]#[:]
            data=f["Data"]["Data"]
            yoko=data[:,0,0].astype(float64)
            fstart=f["Traces"]['RS VNA - S21_t0dt'][0][0]
            fstep=f["Traces"]['RS VNA - S21_t0dt'][0][1]
            sm=shape(Magvec)[0]
            sy=shape(data)
            s=(sm, sy[0], 1)#sy[2])
            Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
            Magcom=reshape(Magcom, s, order="F")
            frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            Magcom=squeeze(Magcom)
            return frequency, yoko, Magcom

        with File("/Users/thomasaref/Dropbox/Current stuff/Logbook/TA210715A45_cooldown270216/Data_0227/S4A4_TA88_wideSC1116unswitched.hdf5", "r") as f:
            Magvec=f["Traces"]["RS VNA - S21"]
            fstart=f["Traces"]['RS VNA - S21_t0dt'][0][0]
            fstep=f["Traces"]['RS VNA - S21_t0dt'][0][1]
            sm=shape(Magvec)[0]
            s=(sm, 1, 1)
            Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
            Magcom=reshape(Magcom, s, order="F")
            frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            Magcom=squeeze(Magcom)
        return frequency, Magcom
            #Magabs=Magcom[:, :, :]-mean(Magcom[:, 197:200, :], axis=1, keepdims=True)
from numpy import array, log10, fft, exp
if __name__=="__main__":
    a=Lyzer()
    frq, yok, mag=a.read_data()
    c=Fitter()
    c.yoko=a.yoko[:]
    b=Plotter()
    bb=Plotter()
    #b.colormesh("magabs2", yok, frq, absolute(mag))
    #b.line_plot("bg", bgf, bgmc/dB)
    def magdB_colormesh():
        b.colormesh("magdB", a.yoko, a.frequency, a.MagdB)
        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        b.set_ylim(4e9, 5.85e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    def magabs_colormesh():
        b.colormesh("magabs", a.yoko, a.frequency, a.MagAbs)
        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        #b.line_plot("flux_parabola", c.flux_parabola, c.flux_parabola, color="orange", alpha=0.4)

        b.set_ylim(4e9, 5.85e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"
    c.plotter=b

    def phase_colormesh():
        b.colormesh("phase", a.yoko, a.frequency, a.Phase)
        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        b.set_ylim(4e9, 5e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    def magabs_cs():
        #b.line_plot("magabs_cs", a.frequency, a.MagAbs[:, 0])
        #b.line_plot("magabs_cs", a.frequency, a.MagAbs[:, 257])
        if 0:
            myifft=fft.ifft(a.Magcom[:,500])
            b.line_plot("ifft", absolute(myifft))
            myifft=fft.ifft(a.Magcom[:,0])
            b.line_plot("ifft", absolute(myifft))
            myifft=fft.ifft(a.Magcom[:,257])
            b.line_plot("ifft", absolute(myifft))

        if 0:
            myifft=fft.ifft(mag[:,219])
            b.line_plot("ifft2", absolute(myifft))
            myifft=fft.ifft(mag[:,0])
            b.line_plot("ifft2", absolute(myifft))
            myifft=fft.ifft(mag[:,500])
            b.line_plot("ifft2", absolute(myifft))
        if 0:
            myifft=fft.ifft(a.Magcom[:,500])
            myifft[50:-50]=0.0
            #myifft[:20]=0.0
            #myifft[-20:]=0.0
            bg=fft.fft(myifft)
            filt=[]
            for n in range(len(a.yoko)):
                myifft=fft.ifft(a.Magcom[:,n])
                #b.line_plot("ifft", absolute(myifft))
                myifft[50:-50]=0.0
                #myifft[:20]=0.0
                #myifft[-20:]=0.0
                filt.append(absolute(fft.fft(myifft)-bg))
            b.colormesh("filt", a.frequency, a.yoko, filt)
        if 1:
            myifft=fft.ifft(mag[:,500])
            myifft[40:-40]=0.0
            myifft[:20]=0.0
            myifft[-20:]=0.0
            bg=fft.fft(myifft)
            filt=[]
            for n in range(len(yok)):
                myifft=fft.ifft(mag[:,n])
                #b.line_plot("ifft", absolute(myifft))
                myifft[50:-50]=0.0
                #myifft[:20]=0.0
                #myifft[-20:]=0.0
                filt.append(absolute(fft.fft(myifft)))
            b.colormesh("filt", frq, yok, filt)

    def magabs_cs_fit():
        def lorentzian(x,p):
            return p[2]*(1.0-1.0/(1.0+((x-p[1])/p[0])**2))+p[3]

        def fano(x, p):
            return p[2]*(((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

        def refl_fano(x, p):
            return p[2]*(1.0-((p[4]*p[0]+x-p[1])**2)/(p[0]**2+(x-p[1])**2))+p[3]

        def onebounce(x,p):
            w=2*pi*x
            k=2.0*pi*x/3488.0
            Cc=0.0
            D=500.0e-6
            D1=300.0e-6
            D2=200.0e-6
            S12q=((p[4]*p[0]/6.28+(x-p[1])*2*pi)**2)/(p[0]**2+(p[4]*p[0]/6.28+x-p[1])**2)
            S11q=1.0/(p[0]**2+(p[4]*p[0]/6.28+x-p[1])**2)
            S11=p[5]
            return p[2]*absolute(exp(1.0j*k*D)*S12q*(1+exp(2.0j*k*D1)*S11q*S11+exp(2.0j*k*D2)*S11q*S11+
            exp(2.0j*k*D)*S11**2*S12q**2)+2.0j*w*Cc*50.0)**2+p[3]

        def allbounces(x,p):
            w=2*pi*x
            k=2.0*pi*x/3488.0
            Cc=0.0
            D=500.0e-6
            D1=300.0e-6
            D2=200.0e-6

            return p[2]*absolute(exp(1.0j*k*D)*S12q*(-2.0
                +1.0/(1.0-exp(2.0j*k*D1)*S11q*S11)
                +1.0/(1.0- exp(2.0j*k*D2)*S11q*S11)
                +1.0/(1- exp(2.0j*k*D)*S11**2*S12q**2))
                +2.0j*w*Cc*50.0)

        def residuals(p,y,x):
            err = y - lorentzian(x,p)
            return err

        def residuals2(p,y,x):
            return y - fano(x,p)

        def residuals3(p,y,x):
            return y - refl_fano(x,p)

        p = [200e6,4.5e9, 0.002, 0.022, 0.1, 0.1]

        indices=[range(81, 120+1), range(137, 260+1), range(269, 320+1), range(411, 449+1)]#, [490]]#, [186]]
        indices=[range(len(a.frequency))]
        widths=[]
        freqs=[]
        freq_diffs=[]
        fanof=[]
        filt=[]
        for n in range(len(yok)):
            myifft=fft.ifft(mag[:,n])
                #b.line_plot("ifft", absolute(myifft))
            myifft[50:-50]=0.0
                #myifft[:20]=0.0
                #myifft[-20:]=0.0
            filt.append(absolute(fft.fft(myifft))**2)
        filt=array(filt).transpose()
        for ind_list in indices:
            for n in ind_list:
                pbest = leastsq(residuals3, p, args=(a.MagAbs[n, :], c.flux_parabola[:]), full_output=1)
                best_parameters = pbest[0]
                print best_parameters
                if 0:#n % 8==0:
                    bb.scatter_plot("magabs_flux", c.flux_parabola[:]*1e-9, a.MagAbs[n, :], label="{}".format(n), linewidth=0.2, marker_size=0.8)
                    bb.line_plot("lorentzian", c.flux_parabola*1e-9, refl_fano(c.flux_parabola,best_parameters), label="fit {}".format(n), linewidth=0.5)
                if 1:#absolute(best_parameters[1]-a.frequency[n])<2e8:
                    freqs.append(a.frequency[n])
                    freq_diffs.append(absolute(best_parameters[1]-a.frequency[n]))
                    widths.append(absolute(best_parameters[0]))
                    fanof.append(absolute(best_parameters[4]))
        if 1:
            widths2=[]
            freqs2=[]
            freq_diffs2=[]
            fano2=[]
            flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=yok, offset=-0.037, flux_factor=0.2925)
            Ej=qdt.call_func("Ej", flux_over_flux0=flux_over_flux0)
            flux_par=qdt._get_fq(Ej, qdt.Ec)
            magabs=absolute(mag)**2
            for n in range(len(frq)):
                pbest = leastsq(residuals2,p,args=(filt[n, :], flux_par[:]), full_output=1)
                best_parameters = pbest[0]
                print best_parameters
                if 0:#n==539 or n==554:#n % 10:
                    b.line_plot("magabs_flux", flux_par*1e-9, (magabs[n, :]-best_parameters[3])/best_parameters[2], label="{}".format(n), linewidth=0.2)
                    b.line_plot("lorentzian", flux_par*1e-9, fano(flux_par,best_parameters), label="fit {}".format(n), linewidth=0.5)
                if 1:#absolute(best_parameters[1]-frq[n])<1.5e8:
                    freqs2.append(frq[n])
                    freq_diffs2.append(absolute(best_parameters[1]-frq[n]))
                    widths2.append(absolute(best_parameters[0]))
                    fano2.append(absolute(best_parameters[4]))

        b.line_plot("widths", freqs, widths, label="-110 dBm")
        b.scatter_plot("widths2", freqs2, widths2, color="red", label="-130 dBm")
        vf=3488.0
        p=[1.0001, 0.5, 0.3, 1.0e-15, 0.001]
        Np=9
        K2=0.048
        f0=5.348e9
        def fourier(x, p):
            w=2*pi*x
            k=2.0*pi*x/3488.0
            D=500.0e-6
            D1=300.0e-6
            D2=200.0e-6
            G_f=0.5*Np*K2*f0*(sin(Np*pi*(x-f0)/f0)/(Np*pi*(x-f0)/f0))**2

            return G_f*absolute(exp(1.0j*k*D)*p[0]*(1+exp(2.0j*k*D1)*(p[1]+1.0j*p[2])+exp(2.0j*k*D2)*(p[1]+1.0j*p[2]))
            +2.0j*w*p[3]*50.0)+p[4]
            #exp(2.0j*k*D)*(p[1]+1.0j*p[2]))+


        def resid(p,y,x):
            #return y - onebounce(x,p)
            return y - fourier(x,p)
        #pbest=leastsq(resid, p, args=(absolute(widths2[318:876]), frq[318:876]), full_output=1)
        #print pbest[0]
        #b.line_plot("fourier", frq, fourier(frq, pbest[0]))
        #pi*vf/2*x=D
        from scipy.signal import lombscargle
        #lombscargle(freqs2[318:876], widths2[318:876])
        #bb.line_plot("fft", #frq[318:876]*fft.fftfreq(len(frq[318:876]), d=frq[1]-frq[0]),
        #absolute(fft.fft(widths2[318:876])))
        frqdiffs=linspace(0.01, 500e6, 1000)
        #bb.line_plot("ls", frqdiffs, lombscargle(array(freqs2[285:828]), array(widths2[285:828]), frqdiffs ))
        #bb.line_plot("ls", frqdiffs, lombscargle(array(freqs[318:876]), array(widths[318:876]), frqdiffs))

        bb.line_plot("fft2", absolute(fft.ifft(widths2[285:828])))
        bb.line_plot("fft", absolute(fft.ifft(widths[285:828])))

        bbb=Plotter()
        #bbb.scatter_plot("wid", freqs2, widths2)
        myifft=fft.ifft(widths2[285:828])
        myifft[12:-12]=0.0
        bbb.line_plot("ff", freqs2[285:828], absolute(fft.fft(myifft)))
        #b.line_plot("ff", freqs2[285:828], absolute(fft.fft(myifft)))

        #bb.line_plot("fft2", absolute(fft.fft(widths[52:155])))

        #b.line_plot("fano", freqs, fano)
        #b.line_plot("fano", freqs2, fano2)

        #f0=5.37e9
        freq=linspace(4e9, 5e9, 1000)
        #G_f=0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*sin(pi*(freq-f0)/f0)))**2
        #b.scatter_plot("freq_test", freqs, freq_diffs)

        class Fitter3(Operative):
            base_name="fitter"
            mult=FloatRange(0.001, 5.0, 0.82).tag(tracking=True)
            f0=FloatRange(4.0, 6.0, 5.348).tag(tracking=True)
            offset=FloatRange(0.0, 100.0, 18.0).tag(tracking=True)

            @tag_Property(plot=True, private=True)
            def G_f(self):
                f0=self.f0*1.0e9
                return self.offset*1e6+self.mult*0.5*Np*K2*f0*(sin(Np*pi*(freq-f0)/f0)/(Np*pi*(freq-f0)/f0))**2

            @observe("f0", "mult", "offset")
            def update_plot(self, change):
                if change["type"]=="update":
                    self.get_member("G_f").reset(self)
                    b.plot_dict["G_f"].clt.set_ydata(self.G_f)
                    b.draw()

        d=Fitter3()
        b.line_plot("G_f", freq, d.G_f, label="theory")

    #magabs_cs()
    #magdB_colormesh()
    #magabs_colormesh()
    magabs_cs_fit()
    if 1:
        from numpy import exp, pi, sqrt, sin, log10, log, argmax, array, cos
        class Fitter2(Operative):
            base_name="fitter"
            vf=FloatRange(3000.0, 4000.0, 3488.0).tag(tracking=True)
            tD=FloatRange(0.0, 2000.0, 500.0).tag(tracking=True)
            ZS=FloatRange(10.0, 100.0, 44.38).tag(tracking=True)
            epsinf=FloatRange(1.0, 10.0, 4.0).tag(tracking=True)
            K2=FloatRange(0.01, 0.1, 0.02458).tag(tracking=True)
            f0=FloatRange(4.0, 6.0, 5.25).tag(tracking=True)
            Cc=FloatRange(0.00001, 100.0, 26.5).tag(tracking=True)
            bg_off=FloatRange(-50.0, 0.0, -24.0).tag(tracking=True)
            bg_slope=FloatRange(-10.0, 10.0, 0.0).tag(tracking=True)
            apwr=Float(1.9)
            avalue=FloatRange(0.0, 1.0, 0.0).tag(tracking=True)
            Lk=FloatRange(0.00001, 100.0, 1.0).tag(tracking=True)

            @tag_Property(plot=True, private=True)
            def R(self):
                 f=a.frequency
                 w=2*pi*f
                 #vf=self.vf
                 #lbda=vf/f
                 #att=(self.avalue*(f/1.0e9)**self.apwr)*1.0e6/vf*log(10.0)/20.0
                 #k=2*pi/lbda+1.0j*att
                 #tL=k*self.tD*1.0e-6
                 #L=1/(qdt.Ct*(2*pi*c.flux_parabola)**2)
                 #GL=1.0/ZL
                 epsinf=self.epsinf*1.0e-10
                 W=25.0e-6
                 Dvv=self.K2/2.0
                 f0=self.f0*1.0e9
                 w0=2*pi*f0
                 Np=9
                 X=Np*pi*(f-f0)/f0
                 Ga0=3.11*w0*epsinf*W*Dvv*Np**2
                 Ct=sqrt(2.0)*Np*W*epsinf
                 #Cc=self.Cc*1.0e-15
                 #VcdivV=self.VcdivV
                 #L=1/(C*(wq**2.0))
                 #Lk=self.Lk*Np*1e-9
                 Ga=Ga0*(sin(X)/X)**2.0
                 Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
                 lamb=1e9*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)
                 return lamb

                 flux_over_flux0=(a.yoko-c.offset)*c.flux_factor
                 R=[]
                 R2=[]
                 print Ct
                 #return Ba/w
                 for fof0 in flux_over_flux0:
                     Ej=qdt.Ejmax*absolute(cos(pi*fof0))
                     Ec=e**2/(2.0*Ct)
                     E0 =  sqrt(8.0*Ej*Ec)*0.5 - Ec/4.0
                     E1 =  sqrt(8.0*Ej*Ec)*1.5 - (Ec/12.0)*(6.0+6.0+3.0)#+lamb*h
                     fq=(E1-E0)/h
                     L=1/(qdt.Ct*(2*pi*fq)**2)
                     R.append(absolute(Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*L)))**2)# for l in L]#+1.0j*(VcdivV)*w*Cc)
                     fqq=fq-Ec/2.0/h#-lamb
                     L=1/(qdt.Ct*(2*pi*fqq)**2)
                     R2.append(absolute(Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*L)))**2)# for l in L]#+1.0j*(VcdivV)*w*Cc)

                 return R, R2

                 #Npq=9
                 #f0q=5.45e9
                 #def coup(fq):
                 #    X=Npq*pi*(f-f0q)/f0q
                 #    return 1.0e9*(sin(X)/X)**2
                 #return [1.0/(1.0+((f-fc)/coup(fc))**2) for fc in c.flux_parabola] #1.0j*w*Ct+1.0/(1.0j*w*l)))**2 for l in L]

                 #return [1.0/(1.0+((f*Ba/+f-fc)/coup(fc))**2) for fc in c.flux_parabola] #1.0j*w*Ct+1.0/(1.0j*w*l)))**2 for l in L]

                 #return [absolute(Ga/(Ga+1.0j*w*Ct+1.0/(1.0j*w*l)))**2 for l in L]
                 #return [absolute(Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*l)))**2 for l in L]#+1.0j*(VcdivV)*w*Cc)
                 #return [c.flux_parabola[argmax(absolute(Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*l))), axis=0)] for l in L]#+1.0j*(VcdivV)*w*Cc)
    d=Fitter2()

    #b.scatter_plot("fluxtry", a.frequency, c.flux_parabola[argmax(array(d.R).transpose(), axis=1)])
    #b.colormesh("fluxtry", a.yoko, a.frequency, array(d.R[0]).transpose()+array(d.R[1]).transpose())
    #b.colormesh("fluxtry2", a.yoko, a.frequency, array(d.R[1]).transpose())

    #b.line_plot("fluxtry",  a.frequency+1.05e9, a.frequency)#.transpose())
    #b.line_plot("fluxtry",  a.frequency, d.R[1])#.transpose())

    if 0:
        from numpy import exp, pi, sqrt, sin, log10, log

        b.line_plot("off res", a.frequency, 10.0*log10(absolute(a.Magcom[:, 300])), linewidth=0.5)

        f=linspace(4.0e9, 5.0e9, 5000)

        class Fitter2(Operative):
            base_name="fitter"
            vf=FloatRange(3000.0, 4000.0, 3488.0).tag(tracking=True)
            tD=FloatRange(0.0, 2000.0, 500.0).tag(tracking=True)
            ZS=FloatRange(10.0, 100.0, 44.38).tag(tracking=True)
            epsinf=FloatRange(1.0, 10.0, 2.989).tag(tracking=True)
            K2=FloatRange(0.01, 0.1, 0.02458).tag(tracking=True)
            f0=FloatRange(4.0, 5.0, 4.447).tag(tracking=True)
            Cc=FloatRange(0.00001, 100.0, 26.5).tag(tracking=True)
            bg_off=FloatRange(-50.0, 0.0, -24.0).tag(tracking=True)
            bg_slope=FloatRange(-10.0, 10.0, 0.0).tag(tracking=True)
            apwr=Float(1.9)
            avalue=FloatRange(0.0, 1.0, 0.0).tag(tracking=True)
            Lk=FloatRange(0.00001, 100.0, 1.0).tag(tracking=True)

            @tag_Property(plot=True, private=True)
            def R(self):

                 w=2*pi*f
                 vf=self.vf
                 lbda=vf/f
                 att=(self.avalue*(f/1.0e9)**self.apwr)*1.0e6/vf*log(10.0)/20.0
                 k=2*pi/lbda+1.0j*att
                 tL=k*self.tD*1.0e-6
                 ZL=self.ZS
                 GL=1.0/ZL
                 epsinf=self.epsinf*1.0e-10
                 W=25.0e-6
                 Dvv=self.K2/2.0
                 f0=self.f0*1.0e9
                 w0=2*pi*f0
                 Np=36
                 X=Np*pi*(f-f0)/f0
                 Ga0=3.11*w0*epsinf*W*Dvv*Np**2
                 Ct=sqrt(2.0)*Np*W*epsinf
                 Cc=self.Cc*1.0e-15
                 #VcdivV=self.VcdivV
                 #L=1/(C*(wq**2.0))
                 Lk=self.Lk*Np*1e-9
                 Ga=Ga0*(sin(X)/X)**2.0
                 Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)

                 Y=Ga+1.0j*Ba+1.0j*w*Ct+1.0/(1.0j*w*Lk)
                 Y1=Y
                 Y2=Y[:]
                 Y3=1.0j*w*Cc
                 S33Full=(Y2+1/ZL-ZL*(Y1*Y3+Y2*Y3+Y1*Y2)-Y1)/(2*Y3+Y2+1.0/ZL+ZL*(Y1*Y3+Y2*Y3+Y1*Y2)+Y1)

                 S11=Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/ZL+1.0/(1.0j*w*Lk))#+1.0j*(VcdivV)*w*Cc)
                 S33= S33Full#(1/ZL-Y)/(1/ZL+Y)
                 S13=1.0j*sqrt(2*Ga*GL)/(Ga+1.0j*Ba+ 1.0j*w*Ct+1.0/ZL+1.0/(1.0j*w*Lk))#+1.0j*(VcdivV)*w*Cc)

                 S11q=Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/ZL+1.0/(1.0j*w*Lk))#+1.0j*(VcdivV)*w*Cc)
                 S13q=1.0j*sqrt(2*Ga*GL)/(Ga+1.0j*Ba+ 1.0j*w*Ct+1.0/ZL+1.0/(1.0j*w*Lk))

                 #S21C=2.0/(2.0+1.0/(1.0j*w*Cc*ZL))
                 S21C=2.0*Y3/(2.0*Y3+Y2+Y1+1/ZL+ZL*(Y1*Y3+Y2*Y3+Y1*Y2))
                 crosstalk=S21C*S13q*S13/(exp(-1.0j*tL)-S11*exp(1.0j*tL)*S11q)

                 return S33 + S13**2/(exp(-2.0j*tL)/S11q-S11)+crosstalk

            plotter=Typed(Plotter).tag(private=True)

            @observe("vf", "tD", "ZS", "epsinf", "K2", "f0", "Cc", "apwr", "avalue", "bg_off", "Lk", "bg_slope")
            def update_plot(self, change):
                if change["type"]=="update":
                     self.get_member("R").reset(self)
                     self.plotter.plot_dict["R_theory"].clt.set_ydata(20.0*log10(absolute(self.R))+self.bg_off+self.bg_slope*f*1e-9)
                     self.plotter.draw()

        d=Fitter2()
        b.line_plot("R_theory", f, 20.0*log10(absolute(d.R))+d.bg_off, linewidth=0.5)
        d.plotter=b

    shower(b)


