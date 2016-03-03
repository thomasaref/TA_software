# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:46:49 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read, TA88_Fund, qdt
from atom.api import Typed, Unicode, Float, observe, FloatRange
from h5py import File
from taref.core.universal import Array
from numpy import float64, linspace, shape, reshape, squeeze, mean, angle, absolute
from taref.core.atom_extension import tag_Property
from taref.physics.units import dB
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from taref.core.agent import Operative

class Fitter(Operative):
     offset=FloatRange(-1.0, 1.0, -0.037).tag(tracking=True)
     flux_factor=FloatRange(0.01, 1.0, 0.2945).tag(tracking=True)

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

    rt_atten=Float(60)

    rt_gain=Float(26*2)

    frequency=Array().tag(unit="GHz", plot=True, label="Frequency")
    yoko=Array().tag(unit="V", plot=True, label="Yoko")
    Magcom=Array().tag(private=True)

    probe_frq=Float().tag(unit="GHz", label="Probe frequency", read_only=True)
    probe_pwr=Float().tag(label="Probe power", read_only=True, display_unit="dBm/mW")



    @tag_Property(display_unit="dB", plot=True)
    def MagdB(self):
        return self.Magcom[:, :]/dB

    @tag_Property(plot=True)
    def Phase(self):
        return angle(self.Magcom[:, :])#-mean(self.Magcom[:, 297:303], axis=1, keepdims=True))

    @tag_Property( plot=True)
    def MagAbs(self):
        #return absolute(self.Magcom[:, :])
        return absolute(self.Magcom[:, :])#-mean(self.Magcom[:, 599:600], axis=1, keepdims=True))


    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0223/S4A1_TA88_coilswp_4to5GHz.hdf5")

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
            s=(sm, sy[0], sy[2])
            print s
            Magcom=Magvec[:,0,:]+1j*Magvec[:,1,:]
            Magcom=reshape(Magcom, s, order="F")
            self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
            print shape(Magcom)
            self.Magcom=squeeze(Magcom)
            #Magabs=Magcom[:, :, :]-mean(Magcom[:, 197:200, :], axis=1, keepdims=True)

if __name__=="__main__":
    a=Lyzer()
    a.read_data()
    c=Fitter()
    c.yoko=a.yoko[:]
    b=Plotter()
    def magdB_colormesh():
        b.colormesh("magdB", a.yoko, a.frequency, a.MagdB)
        b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        b.set_ylim(4.0e9, 5.0e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"

    def magabs_colormesh():
        flux_over_flux0=qdt.call_func("flux_over_flux0", voltage=a.yoko, offset=c.offset, flux_factor=c.flux_factor)
        b.colormesh("magabs", flux_over_flux0, a.frequency*1e-9, a.MagAbs)
        #b.line_plot("flux_parabola", flux_over_flux0, c.flux_parabola, color="orange", alpha=0.4)
        #b.set_ylim(4.4e9, 4.5e9)
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
        b.line_plot("magabs_cs", c.flux_parabola*1e-9, a.MagAbs[903, :])
        b.xlabel="Qubit Frequency (GHz)"
        b.ylabel="$|S_{2_1}|$"
        b.title="Transmission cross-section"
        #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)
        #b.set_xlim(0, 7e9)
        #b.set_ylim(0, 0.02)

    def magabs_cs2():
        #b.line_plot("magabs_cs", a.frequency*1e-9, a.MagAbs[:, 362])
        #b.line_plot("magabs_cs", a.frequency*1e-9, a.MagAbs[:, 0])
        bg=mean(a.Magcom[:, 0:50], axis=1)
        from scipy.signal import deconvolve
        from numpy import polydiv
        #from numpy import
        print shape(deconvolve(a.Magcom[:, 362], bg)[1])
        print shape(a.frequency[1:]*1e-9)
        b.line_plot("magabs_sub", a.frequency[:]*1e-9,  absolute(mean(a.Magcom[:, 342:382], axis=1))-absolute(bg)+0.02)#a.MagAbs[756:1093, 0])+0.02)
        #b.line_plot("magabs_sub", a.frequency[:]*1e-9,  absolute(deconvolve(a.Magcom[:, 360], bg)[1]))#a.MagAbs[756:1093, 0])+0.02)
        #b.line_plot("magabs_sub", a.frequency[:]*1e-9,  absolute(deconvolve(a.Magcom[:, 374], bg)[1]))#a.MagAbs[756:1093, 0])+0.02)
        #newabs=[]
        #for ind in range(601):
        #    newabs.append(absolute(a.Magcom[:, ind]-bg))
        #b.colormesh("magabs", a.frequency, a.yoko, newabs)
        #b.line_plot("magabs_sub", a.frequency[:]*1e-9, absolute(a.Magcom[:, 362]/bg))#a.MagAbs[756:1093, 0])+0.02)
        #b.line_plot("magabs_sub", a.frequency[:]*1e-9, absolute(a.Magcom[:, 366]/bg))#a.MagAbs[756:1093, 0])+0.02)

    #magdB_colormesh()
    #magabs_cs()
    #magabs_colormesh()
    #magabs_cs2()
    from scipy.optimize import leastsq # Levenberg-Marquadt Algorithm #
    from numpy import concatenate, polyfit

    def lorentzian(x,p):
        numerator =  (p[0]**2 )
        denominator = ( x - (p[1]) )**2 + p[0]**2
        y = -p[2]*(numerator/denominator)+p[3]
        return y

    def residuals(p,y,x):
        err = y - lorentzian(x,p)
        return err

    #ind_bg_low = (x > min(x)) & (x < 450.0)
    #ind_bg_high = (x > 590.0) & (x < max(x))

    #x_bg = concatenate((x[ind_bg_low],x[ind_bg_high]))
    #y_bg = concatenate((y[ind_bg_low],y[ind_bg_high]))
    #m, c = polyfit(x_bg, y_bg, 1)
    #background = m*x + c
    #y_bg_corr = y - background

    # initial values #
    p = [200e6,4.5e9, 0.02, 0.022]  # [hwhm, peak center, intensity] #

    # optimization #
    pbest = leastsq(residuals,p,args=(a.MagAbs[903, :], c.flux_parabola), full_output=1)
    best_parameters = pbest[0]
    print pbest[0]

    print a.frequency[903]
    # fit to data #
    fit = lorentzian(c.flux_parabola,best_parameters)
    #b.line_plot("lorentzian", c.flux_parabola*1e-9, fit)

    from numpy import exp, pi, sqrt, sin, log10, log, array
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
        bg=FloatRange(0.0, 1.0, 1.0).tag(tracking=True)
        apwr=Float(1.9)
        avalue=FloatRange(0.0, 1.0, 0.0).tag(tracking=True)

        phase_0=FloatRange(-pi, pi, 0.0).tag(tracking=True)
        ed=FloatRange(0.00001, 100.0, 0.2).tag(tracking=True)

        @tag_Property(private=True)
        def flatten(self):
            m=0
            flattener=[]
            for n, f in enumerate(a.frequency):
                phase=self.phase_0+self.ed*(f*1e-9-4.0)-2*pi*m
                if a.Phase[n, 600]-phase>pi:
                    m+=1
                    phase=self.phase_0+self.ed*(f*1e-9-4.0)-2*pi*m
                elif a.Phase[n, 600]-phase<-pi:
                    m-=1
                    phase=self.phase_0+self.ed*(f*1e-9-4.0)-2*pi*m

                flattener.append(a.Phase[n,600]-phase)
            return array(flattener)

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

             Ga=Ga0*(sin(X)/X)**2.0
             Ba=Ga0*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)

             Y=Ga+1.0j*Ba+1.0j*w*Ct
             Y1=Y
             Y2=Y[:]
             Y3=1.0j*w*Cc
             S33Full=(Y2+1/ZL-ZL*(Y1*Y3+Y2*Y3+Y1*Y2)-Y1)/(2*Y3+Y2+1.0/ZL+ZL*(Y1*Y3+Y2*Y3+Y1*Y2)+Y1)

             S11=Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/ZL)#+1.0j*(VcdivV)*w*Cc)
             S33= S33Full#(1/ZL-Y)/(1/ZL+Y)
             S13=1.0j*sqrt(2*Ga*GL)/(Ga+1.0j*Ba+ 1.0j*w*Ct+1.0/ZL)#+1.0j*(VcdivV)*w*Cc)

             S11q=Ga/(Ga+1.0j*Ba+1.0j*w*Ct+1.0/ZL)#+1.0j*(VcdivV)*w*Cc)
             S13q=1.0j*sqrt(2*Ga*GL)/(Ga+1.0j*Ba+ 1.0j*w*Ct+1.0/ZL)

             #S21C=2.0/(2.0+1.0/(1.0j*w*Cc*ZL))
             S21C=2.0*Y3/(2.0*Y3+Y2+Y1+1/ZL+ZL*(Y1*Y3+Y2*Y3+Y1*Y2))

             crosstalk=S21C*S13q*S13/(exp(-1.0j*tL)-S11*exp(1.0j*tL)*S11q)

             #return S33 + S13**2/(exp(-2.0j*tL)/S11q-S11)+crosstalk

             return S21C+S13*exp(1.0j*tL)*S13q/(1.0-S11q*exp(2.0j*tL)*S11)+crosstalk

        plotter=Typed(Plotter).tag(private=True)

        @observe("vf", "tD", "ZS", "epsinf", "K2", "f0", "Cc", "apwr", "avalue", "bg", "ed", "phase_0")
        def update_plot(self, change):
            if change["type"]=="update":
                 self.get_member("R").reset(self)
                 self.plotter.plot_dict["R_theory"].clt.set_ydata(d.bg*angle(self.R))
                 self.get_member("flatten").reset(self)
                 self.plotter.plot_dict["DB_cs"].clt.set_ydata(self.flatten)
                 self.plotter.draw()

    d=Fitter2()

    b.line_plot("DB_cs", a.frequency, d.flatten, linewidth=0.5)
    b.line_plot("R_theory", f, d.bg*angle(d.R), linewidth=0.5)
    d.plotter=b
    shower(b)


