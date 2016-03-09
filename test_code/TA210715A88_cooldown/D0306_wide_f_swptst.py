# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 10:46:49 2016

@author: thomasaref
"""

from TA88_fundamental import TA88_Read, TA88_Fund, qdt
from atom.api import Typed, Unicode, Float, observe, FloatRange, Int
from h5py import File
from taref.core.universal import Array
from numpy import float64, linspace, shape, reshape, squeeze, mean, angle, absolute
from taref.core.atom_extension import tag_Property
from taref.physics.units import dB
from taref.plotter.fig_format import Plotter
from taref.core.shower import shower
from taref.core.agent import Operative
from taref.core.log import log_debug
from taref.physics.fundamentals import e, h

class Fitter(Operative):
     offset=FloatRange(-1.0, 1.0, -0.04).tag(tracking=True)
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

    pind=Int()


    @tag_Property(display_unit="dB", plot=True)
    def MagdB(self):
        return self.Magcom[:, :]/dB

    @tag_Property(plot=True)
    def Phase(self):
        return angle(self.Magcom[:, :]-mean(self.Magcom[:, 169:170], axis=1, keepdims=True))

    @tag_Property( plot=True)
    def MagAbs(self):
        #return absolute(self.Magcom[:, :])
        return absolute(self.Magcom[:, :]-mean(self.Magcom[:, 249:251], axis=1, keepdims=True))


    def _default_rd_hdf(self):
        return TA88_Read(main_file="Data_0306/S4A4_TA88_wide_f_flux_swp.hdf5")

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
            s=(sm,  sy[0], 1)
            print s
            Magcom=Magvec[:,0,:]+1j*Magvec[:,1, :]

            #Magcom=reshape(Magcom, s, order="F")
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
        #b.set_ylim(4e9, 5.85e9)
        b.xlabel="Yoko (V)"
        b.ylabel="Frequency (Hz)"
        b.title="Reflection fluxmap"
    def magabs_colormesh2():
        b.colormesh("magabs", c.flux_parabola, a.frequency, a.MagAbs)
        b.line_plot("flux_parabola", c.flux_parabola, c.flux_parabola, color="orange", alpha=0.4)
        b.set_ylim(4e9, 5.85e9)
        b.xlabel="Qubit Frequency (Hz)"
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
        b.line_plot("magabs_cs", a.frequency, absolute(a.Magcom[:, 250]))
        #b.line_plot("flux_parabola", c.yoko, c.flux_parabola, color="orange", alpha=0.4)

    #magabs_cs()
    #magdB_colormesh()
    magabs_colormesh()
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
                 lamb=Np*1e9*(sin(2.0*X)-2.0*X)/(2.0*X**2.0)


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
    #b.colormesh("fluxtry2", a.yoko, a.frequency, array(d.R[0]).transpose())

    #b.line_plot("fluxtry",  a.frequency, d.R)#.transpose())
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


