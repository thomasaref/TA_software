# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Two_Tone_Pwr_Lyzer, TA53_Read, qdt
from numpy import (absolute,  trunc, arccos, shape, float64, linspace, reshape,
                   squeeze, argmax, array, log10, swapaxes, amax, angle)
from taref.plotter.api import colormesh, scatter, line
from h5py import File
from taref.core.api import process_kwargs
from taref.physics.filtering import Filter


def read_data(self):
    with File(self.rd_hdf.file_path, 'r') as f:
        self.comment=f.attrs["comment"]

        Magvec=f["Traces"]["{0} - {1}".format(self.VNA_name, self.port_name)]
        data=f["Data"]["Data"]
        print shape(Magvec) #91*11=1001
        print shape(data)
        self.frq2=data[:, 0, 0].astype(float64)
        self.yoko=data[0, 1, :].astype(float64)

        sm=shape(Magvec)[0]
        s=(sm, self.frq2.shape[0], self.yoko.shape[0])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        fstart=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][0]
        fstep=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][1]
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        print Magcom.shape
        Magcom=swapaxes(Magcom, 1, 2)
        self.MagcomData=squeeze(Magcom)
        self.stop_ind=len(self.yoko)-1
        self.filt.N=len(self.frequency)

a=TA53_VNA_Two_Tone_Pwr_Lyzer(name="d1110", on_res_ind=117,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1110/S1A4_all_two_tone_pwr.hdf5"), #long_test.hdf5"), #
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="Gate to IDT low frequency",
         offset=-0.3,
         read_data=read_data,
         #swp_type="yoko_first",
        )
a.filt.center=28 #71 #28*0 #141 #106 #58 #27 #139 #106 #  #137
a.filt.halfwidth=10 #8 #10
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.1 #0.035
a.flux_axis_type="yoko" #"flux" #"fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"
a.end_skip=20
a.flux_indices=[range(len(a.yoko)-1)]

a.save_folder.main_dir=a.name

a.read_data()
a.pwr2_ind=0
if 0:
    #a.pwr_ind=39
    print a.yoko.shape, a.frq2.shape
a.filter_type="None"
pl1=colormesh(absolute(a.MagcomData[:, :, 80]))
a.frq2_ind=80
def ifft_plot(self, **kwargs):
    process_kwargs(a, kwargs, pl="hannifft_{0}_{1}_{2}".format(a.filter_type, a.bgsub_type, a.name))
    on_res=absolute(self.filt.window_ifft(self.MagcomData[:,self.on_res_ind, self.frq2_ind]))
    strt=absolute(self.filt.window_ifft(self.MagcomData[:,self.start_ind, self.frq2_ind]))
    stop=absolute(self.filt.window_ifft(self.MagcomData[:,self.stop_ind, self.frq2_ind]))

    pl=line(self.time_axis, self.filt.fftshift(on_res),  color="red",
           plot_name="onres_{}".format(self.on_res_ind),label="{:.4g}".format(self.on_res_ind), **kwargs)
    line(self.time_axis, self.filt.fftshift(strt), pl=pl, linewidth=1.0, color="purple",
         plot_name="strt {}".format(self.start_ind), label="{:.4g}".format(self.start_ind))
    line(self.time_axis, self.filt.fftshift(stop), pl=pl, linewidth=1.0, color="blue",
         plot_name="stop {}".format(self.stop_ind), label="{:.4g}".format(self.stop_ind))

    self.filt.N=len(on_res)
    filt=self.filt.freqz
    #filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
    top=max([amax(on_res), amax(strt), amax(stop)])
    line(self.time_axis, filt*top, plotter=pl, color="green", label="wdw")
    pl.xlabel=kwargs.pop("xlabel", self.time_axis_label)
    pl.ylabel=kwargs.pop("ylabel", "Mag abs")
    return pl

pl2=ifft_plot(a)#.show()

if 1:
    double_filt= array([[a.filt.fft_filter(a.MagcomData[:,n, m]) for n in range(len(a.yoko)-1)] for m in range(len(a.frq2))])#.transpose()
    print double_filt.shape
    double_filt=swapaxes(double_filt, 0, 2)

    print double_filt.shape
    #colormesh(self.freq_axis[a.end_skip:-a.end_skip], self.frq2, absolute(double_filt[a.end_skip:-a.end_skip, :, 10]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    #pl=colormesh(a.frq2, a.pwr2, absolute(double_filt[493, :, :]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    print a.frequency[245]
    print a.frq2
    #[colormesh(10*log10(absolute(double_filt[fi, :, :])/absolute(double_filt[245, :, :]))) for fi in range(0, 500, 20)]
    colormesh( absolute(double_filt[245, :, :]))#.show()a.frq2, a.yoko,
    colormesh(absolute(double_filt[a.end_skip:-a.end_skip, :, 55])).show()
    colormesh(10*log10(absolute(double_filt[a.end_skip:-a.end_skip, :, 55]).transpose()/absolute(double_filt[a.end_skip:-a.end_skip, 179, 80])))#.show()

    #pl4=colormesh(a.yoko[:-1], a.pwr2, absolute(double_filt[457, :, 1,:]).transpose())#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    #pl5=colormesh(a.yoko[:-1], a.pwr2, absolute(double_filt[457, :, 2,:]).transpose())#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))

    #fi=0

    ps1=[colormesh(absolute(double_filt[a.end_skip:-a.end_skip, :, fi])-absolute(double_filt[a.end_skip:-a.end_skip, :, 80]),
                   pl="f{0:.3f}.jpg".format(a.frq2[fi]/1e9)) for fi in range(0, 81, 3)]

    #a.yoko, a.frequency[a.end_skip:-a.end_skip],
    #ps1.append(colormesh(a.yoko, a.pwr2, absolute(double_filt[86, :, fi,:]).transpose(),
    #                     pl="f{0:.3f}.jpg".format(a.frq2[fi]/1e9)))

    for p in ps1:
        p.title=p.name[:-3]
    pl2.show()
    fi=1
    ps2=[colormesh(a.yoko[:-1], a.frequency[a.end_skip:-a.end_skip],
                  absolute(double_filt[a.end_skip:-a.end_skip, :, fi, i]), pl="f{0:.3f}p{1}.jpg".format(a.frq2[fi]/1e9, a.pwr2[i])) for i in range(11)]
    ps2.append(colormesh(a.yoko[:-1], a.pwr2, absolute(double_filt[86, :, fi,:]).transpose(),
                         pl="f{0:.3f}.jpg".format(a.frq2[fi]/1e9)))

    for p in ps2:
        p.title=p.name[:-3]

    fi=2
    ps3=[colormesh(a.yoko[:-1], a.frequency[a.end_skip:-a.end_skip],
                  absolute(double_filt[a.end_skip:-a.end_skip, :, fi, i]), pl="f{0:.3f}p{1}.jpg".format(a.frq2[fi]/1e9, a.pwr2[i])) for i in range(11)]
    ps3.append(colormesh(a.yoko[:-1], a.pwr2, absolute(double_filt[86, :, fi,:]).transpose(),
                         pl="f{0:.3f}.jpg".format(a.frq2[fi]/1e9)))

    for p in ps3:
        p.title=p.name[:-3]

    #p10=colormesh(absolute(double_filt[a.end_skip:-a.end_skip, :, 0, 10]).transpose())#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    #p8=colormesh(a.yoko[:-1], a.frequency[a.end_skip:-a.end_skip], absolute(double_filt[a.end_skip:-a.end_skip, :, fi, 8]))#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    #p7=colormesh(a.yoko[:-1], a.frequency[a.end_skip:-a.end_skip], absolute(double_filt[a.end_skip:-a.end_skip, :, fi, 7]))#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))

    #p6=colormesh(absolute(double_filt[a.end_skip:-a.end_skip, :, 0, 6]).transpose())#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    #p4=colormesh(absolute(double_filt[a.end_skip:-a.end_skip, :, 0, 4]).transpose())#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    #p2=colormesh(absolute(double_filt[a.end_skip:-a.end_skip, :, 0, 2]).transpose())#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    #p0=colormesh(absolute(double_filt[a.end_skip:-a.end_skip, :, 0, 0]).transpose())#.show() #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))

    #colormesh(absolute(double_filt[93, :, :]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
    #colormesh(absolute(double_filt[880, :, :]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))

pls=[pl1, pl2]#, pl3, pl4, pl5]

if __name__=="__main__":
    pls.extend(ps1)
    pls.extend(ps2)
    pls.extend(ps3)
    #a.save_plots(pls)

pl1.show()

a.filter_type="FFT"
print a.MagcomFilt.shape
if 0:
    track_ind=argmax(absolute(a.MagcomFilt[a.end_skip:-a.end_skip, :, :]), axis=1)
    print track_ind
    print track_ind.shape
    line(track_ind[:, 11])

    magtrack=array([a.MagcomFilt[n, track_ind[n, 11], :] for n, q in enumerate(a.frequency[a.end_skip:-a.end_skip])])
    print magtrack.shape
    colormesh(10*log10(absolute(magtrack).transpose()/absolute(magtrack[:,1])))#.show()
    colormesh(absolute(magtrack).transpose())#.show()

    #colormesh(absolute(a.MagcomFilt[:, track_ind, :])).show()
colormesh(absolute(a.MagcomFilt[:,:, 3])).show()
colormesh(10*log10(absolute(a.MagcomFilt[465, :, :]).transpose()/absolute(a.MagcomFilt[465, :, 3])))#.show()
yok_ind=81
colormesh(absolute(a.MagcomFilt[a.end_skip:-a.end_skip, yok_ind, :]).transpose())#.show()
colormesh(10*log10(absolute(a.MagcomFilt[a.end_skip:-a.end_skip, yok_ind, :]).transpose()/absolute(a.MagcomFilt[a.end_skip:-a.end_skip, yok_ind, 3])))#.show()
print a.frq2[[0, 63, 107, 143]]
colormesh(absolute(a.MagcomFilt[a.end_skip:-a.end_skip,:, 0]))

colormesh(absolute(a.MagcomFilt[a.end_skip:-a.end_skip,:, 65]))
colormesh(absolute(a.MagcomFilt[a.end_skip:-a.end_skip,:, 107])) #.transpose()/absolute(a.MagcomFilt[a.end_skip:-a.end_skip,0, 85])))
colormesh(absolute(a.MagcomFilt[a.end_skip:-a.end_skip,:, 143])).show() #.transpose()/absolute(a.MagcomFilt[a.end_skip:-a.end_skip,0, 85])))

colormesh(10*log10(absolute(a.MagcomFilt[a.end_skip:-a.end_skip,:, 85]).transpose()/absolute(a.MagcomFilt[a.end_skip:-a.end_skip,0, 85])))
colormesh(10*log10(absolute(a.MagcomFilt[a.end_skip:-a.end_skip,:, 65]).transpose()/absolute(a.MagcomFilt[a.end_skip:-a.end_skip,0, 65])))
colormesh(10*log10(absolute(a.MagcomFilt[a.end_skip:-a.end_skip,:, 105]).transpose()/absolute(a.MagcomFilt[a.end_skip:-a.end_skip,0, 105]))).show()

#colormesh(10*log10(absolute(a.MagcomFilt[465, :, :]).transpose()/absolute(a.MagcomFilt[465, :, 3])))#.show()

colormesh(absolute(a.MagcomFilt[100*2, :, :]))#.show()
colormesh(absolute(a.MagcomFilt[150*2, :, :]))#.show()
colormesh(absolute(a.MagcomFilt[200*2, :, :]))#.show()
colormesh(absolute(a.MagcomFilt[250*2, :, :]))#.show()
colormesh(absolute(a.MagcomFilt[300*2, :, :]))#.show()
colormesh(absolute(a.MagcomFilt[350*2, :, :]))#.show()
colormesh(absolute(a.MagcomFilt[400*2, :, :]))#.show()
colormesh(absolute(a.MagcomFilt[450*2, :, :]))#.show()
#a.pwr2_ind=1
#colormesh(absolute(a.MagcomFilt[50*2, :, :, a.pwr2_ind]))#.show()
#colormesh(absolute(a.MagcomFilt[100*2, :, :, a.pwr2_ind]))#.show()
#colormesh(absolute(a.MagcomFilt[150*2, :, :, a.pwr2_ind]))#.show()
#colormesh(absolute(a.MagcomFilt[200*2, :, :, a.pwr2_ind]))#.show()
#colormesh(absolute(a.MagcomFilt[250*2, :, :, a.pwr2_ind]))#.show()
#colormesh(absolute(a.MagcomFilt[300*2, :, :, a.pwr2_ind]))#.show()
#colormesh(absolute(a.MagcomFilt[350*2, :, :, a.pwr2_ind]))#.show()
#colormesh(absolute(a.MagcomFilt[400*2, :, :, a.pwr2_ind]))#.show()
#colormesh(absolute(a.MagcomFilt[450*2, :, :, a.pwr2_ind]))#.show()


    #
    #colormesh(absolute(a.MagcomFilt[235, :, :]))#.show()
    #
    #colormesh(a.frq2, a.yoko, absolute(a.MagcomFilt[289, :, :]))#.show()
    #
    #colormesh(absolute(a.MagcomFilt[:, :, 50]))#.show()

from taref.core.api import process_kwargs
from taref.physics.filtering import Filter
from numpy import amax, array, swapaxes, angle, log10
filt=Filter(center=5, halfwidth=15)
#a.pwr2_ind=1
a.frq2_ind=0



if 0:
    def ifft_plot(self, **kwargs):
        process_kwargs(self, kwargs, pl="hannifft_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
        on_res=absolute(filt.window_ifft(self.MagcomData[50,:, 91]))
        #strt=absolute(self.filt.window_ifft(self.Magcom[:,self.start_ind]))
        #stop=absolute(self.filt.window_ifft(self.Magcom[:,self.stop_ind]))

        pl=line(filt.fftshift(on_res),  color="red",
               plot_name="onres_{}".format(self.on_res_ind),label="{:.4g}".format(self.flux_axis[self.on_res_ind]), **kwargs)
        #line(self.time_axis, self.filt.fftshift(strt), pl=pl, linewidth=1.0, color="purple",
        #     plot_name="strt {}".format(self.start_ind), label="{:.4g}".format(self.flux_axis[self.start_ind]))
        #line(self.time_axis, self.filt.fftshift(stop), pl=pl, linewidth=1.0, color="blue",
        #     plot_name="stop {}".format(self.stop_ind), label="{:.4g}".format(self.flux_axis[self.stop_ind]))

        filt.N=len(on_res)
        filt_frq=filt.freqz
        #filt=filt_prep(len(on_res), self.filt_start_ind, self.filt_end_ind)
        top=amax(on_res)#, amax(strt), amax(stop)])
        line(filt_frq*top, plotter=pl, color="green", label="wdw")
        pl.xlabel=kwargs.pop("xlabel", self.time_axis_label)
        pl.ylabel=kwargs.pop("ylabel", "Mag abs")
        if 1:
            double_filt= array([[filt.fft_filter(a.MagcomFilt[m,:, n]) for n in range(len(a.frq2))] for m in a.flat_indices])#.transpose()
            print double_filt.shape
            double_filt=swapaxes(double_filt, 1, 2)
            endskip=2

            colormesh(absolute(double_filt[a.end_skip:-a.end_skip, 56, :]).transpose()-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
            colormesh(absolute(double_filt[a.end_skip:-a.end_skip, 58, :]).transpose()-absolute(double_filt[a.end_skip:-a.end_skip, 58, 134]).transpose())#-absolute(double_filt[250, 10:-10, 134]))
            colormesh(absolute(double_filt[a.end_skip:-a.end_skip, 60, :]).transpose()-absolute(double_filt[a.end_skip:-a.end_skip, 60, 134]).transpose())#-absolute(double_filt[450, 10:-10, 134]))
            print a.yoko[58]
            colormesh(absolute(double_filt[a.end_skip:-a.end_skip, 20, :]).transpose()-absolute(double_filt[a.end_skip:-a.end_skip, 20, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
            colormesh(absolute(double_filt[a.end_skip:-a.end_skip, 45, :]).transpose()-absolute(double_filt[a.end_skip:-a.end_skip, 45, 134]).transpose())#-absolute(double_filt[250, 10:-10, 134]))
            colormesh(absolute(double_filt[a.end_skip:-a.end_skip, 70, :]).transpose()-absolute(double_filt[a.end_skip:-a.end_skip, 70, 134]).transpose())#-absolute(double_filt[450, 10:-10, 134]))


            colormesh(absolute(a.MagcomData[50, :, :]).transpose())
            pl=colormesh(absolute(a.MagcomFilt[50, endskip:-endskip, :]).transpose())
            colormesh(absolute(double_filt[50, endskip:-endskip, :]).transpose(), pl=pl)#-absolute(double_filt[50, 10:-10, 134]))
            colormesh(absolute(double_filt[250, endskip:-endskip, :]).transpose())#-absolute(double_filt[250, 10:-10, 134]))
            colormesh(absolute(double_filt[450, endskip:-endskip, :]).transpose())#-absolute(double_filt[450, 10:-10, 134]))



            colormesh(absolute(double_filt[50, endskip:-endskip, :]).transpose()/absolute(double_filt[50, endskip:-endskip, 134]))
            colormesh(absolute(double_filt[250, endskip:-endskip, :]).transpose()/absolute(double_filt[250, endskip:-endskip, 134]))
            colormesh(absolute(double_filt[450, endskip:-endskip, :]).transpose()/absolute(double_filt[450, endskip:-endskip, 134]))

            colormesh(angle(double_filt[50, 10:-10, :]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
            colormesh(angle(double_filt[250, 10:-10, :]).transpose())#-absolute(double_filt[250, 10:-10, 134]))
            colormesh(angle(double_filt[450, 10:-10, :]).transpose())#-absolute(double_filt[450, 10:-10, 134]))

            #colormesh(absolute(double_filt[:, :, 75]))
            #colormesh(absolute(double_filt[:, :, 50]))
            #colormesh(absolute(double_filt[:, :, 25]))

        return pl
    ifft_plot(a).show()


    colormesh(absolute(a.MagcomFilt[250, :, :])).show()
    colormesh(absolute(a.MagcomFilt[293, :, :, 0]))#.show()
    colormesh(absolute(a.MagcomFilt[370, :, :, 0]))#.show()

    colormesh(absolute(a.MagcomFilt[293, :, :, 3]))#.show()
    colormesh(absolute(a.MagcomFilt[370, :, :, 3]))#.show()

    colormesh(absolute(a.MagcomFilt[293, :, 30, :]))#.show()

    colormesh(absolute(a.MagcomFilt[55, :, :, 0]))#.show()
    colormesh(absolute(a.MagcomFilt[55, :, :, 1]))#.show()
    colormesh(absolute(a.MagcomFilt[55, :, :, 2]))#.show()
    colormesh(absolute(a.MagcomFilt[55, :, :, 3]))#.show()

    colormesh(absolute(a.MagcomFilt[:, 30, :, 0]))#.show()
    colormesh(absolute(a.MagcomFilt[:, 30, :, 1]))#.show()
    colormesh(absolute(a.MagcomFilt[:, 30, :, 2]))#.show()
    colormesh(absolute(a.MagcomFilt[:, 30, :, 3]))#.show()


    a.filter_type="FFT"

    #a.pwr_ind=10
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind])).show()
    #a.pwr_ind=9
    #a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    #a.pwr_ind=8
    #a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    offset=0
    a.pwr_ind=15+offset
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    a.pwr_ind=14+offset
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    a.pwr_ind=13+offset
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    a.pwr_ind=12+offset
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    a.pwr_ind=11+offset
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    a.pwr_ind=10+offset
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    a.pwr_ind=9+offset
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind]))
    a.pwr_ind=8+offset
    a.magabs_colormesh(pl=str(a.pwr[a.pwr_ind])).show()

    #a.filter_type="Fit"
    #pl, pf=a.magabs_colormesh(fig_width=6.0, fig_height=4.0, pf_too=True)
                                   #auto_zlim=False, vmin=0.0, vmax=0.02)
    #a.widths_plot()
    #a.center_plot()#.show()
    #a.filter_type="FFT"
    a.magabs_colormesh(fig_width=6.0, fig_height=4.0).show()

if __name__=="__main2__":
    pls=a.fft_plots()
    #a.save_plots(pls)
    pls[0].show()
