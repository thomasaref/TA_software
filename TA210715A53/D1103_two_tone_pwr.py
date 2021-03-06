# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:55:33 2016

@author: thomasaref
"""

from TA53_fundamental import TA53_VNA_Two_Tone_Pwr_Lyzer, TA53_Read, qdt
from numpy import absolute,  trunc, arccos, shape, float64, linspace, reshape, squeeze, argmax, array, log10
from taref.plotter.api import colormesh, scatter, line
from h5py import File

from taref.filer.save_file import Save_HDF5


def read_data(self):
    #sf=Save_HDF5(file_path=self.rd_hdf.folder.dir_path+"/"+"long_test.hdf5")
    with File(self.rd_hdf.file_path, 'r') as f:
        self.comment=f.attrs["comment"]

        Magvec=f["Traces"]["{0} - {1}".format(self.VNA_name, self.port_name)]
        data=f["Data"]["Data"]
        print shape(Magvec[:]) #91*11=1001
        print shape(data)

        self.yoko=data[:, 0, 0].astype(float64)
        self.frq2=data[0, 1, :201].astype(float64)
        self.pwr2=data[0,2, ::201].astype(float64)

        print self.yoko.shape
        print self.frq2.shape
        print self.pwr2.shape
        #print self.rd_hdf.folder.dir_path
        #sf.buffer_save(self.yoko, name="yoko")
        #sf.buffer_save(self.frq2, name="frq2")
        #sf.buffer_save(self.pwr2, name="pwr2")

        sm=shape(Magvec)[0]
        #sy=shape(data)
        s=(sm, self.yoko.shape[0], self.frq2.shape[0], self.pwr2.shape[0])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        #sf.buffer_save(Magcom, name="Magcom")

        print Magcom.shape
        #raise Exception
        #if self.swp_type=="pwr_first":
        #    self.pwr=data[:, 0, 0].astype(float64)
        #    self.yoko=data[0,1,:].astype(float64)
        #elif self.swp_type=="yoko_first":
        #    self.pwr=data[0, 1, :].astype(float64)
        #    self.yoko=data[:, 0, 0].astype(float64)
        fstart=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][0]
        fstep=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][1]

        #sm=shape(Magvec)[0]
        #sy=shape(data)
        #s=(sm, sy[0], sy[2])
        #Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        #Magcom=reshape(Magcom, s, order="F")
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        #if self.swp_type=="pwr_first":
        #Magcom=swapaxes(Magcom, 1, 2)
        self.MagcomData=squeeze(Magcom)#[:, 2, :]
        self.stop_ind=len(self.yoko)-1
        self.filt.N=len(self.frequency)

def read_data2(self):
    with File(self.rd_hdf.file_path, 'r') as f:
        print f["Data"].keys() #["frq2"]
        print f["Data"]["yoko"]['0']['0'][:]
        raise Exception
        Magvec=f["Traces"]["{0} - {1}".format(self.VNA_name, self.port_name)]
        data=f["Data"]["Data"]
        print shape(Magvec[:]) #91*11=1001
        print shape(data)

        self.yoko=data[:, 0, 0].astype(float64)
        self.frq2=data[0, 1, :201].astype(float64)
        self.pwr2=data[0,2, ::201].astype(float64)

        print self.yoko.shape
        print self.frq2.shape
        print self.pwr2.shape
        print self.rd_hdf.folder.dir_path
        sf.save(self.yoko, name="yoko")
        sf.save(self.frq2, name="frq2")
        sf.save(self.pwr2, name="pwr2")

        sm=shape(Magvec)[0]
        #sy=shape(data)
        s=(sm, self.yoko.shape[0], self.frq2.shape[0], self.pwr2.shape[0])
        Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        Magcom=reshape(Magcom, s, order="F")
        sf.save(Magcom, name="Magcom")

        print Magcom.shape
        raise Exception
        #if self.swp_type=="pwr_first":
        #    self.pwr=data[:, 0, 0].astype(float64)
        #    self.yoko=data[0,1,:].astype(float64)
        #elif self.swp_type=="yoko_first":
        #    self.pwr=data[0, 1, :].astype(float64)
        #    self.yoko=data[:, 0, 0].astype(float64)
        self.comment=f.attrs["comment"]
        fstart=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][0]
        fstep=f["Traces"]['{0} - {1}_t0dt'.format(self.VNA_name, self.port_name)][0][1]

        #sm=shape(Magvec)[0]
        #sy=shape(data)
        #s=(sm, sy[0], sy[2])
        #Magcom=Magvec[:,0, :]+1j*Magvec[:,1, :]
        #Magcom=reshape(Magcom, s, order="F")
        self.frequency=linspace(fstart, fstart+fstep*(sm-1), sm)
        #if self.swp_type=="pwr_first":
        #Magcom=swapaxes(Magcom, 1, 2)
        self.MagcomData=squeeze(Magcom)#[:, 2, :]
        self.stop_ind=len(self.yoko)-1
        self.filt.N=len(self.frequency)

a=TA53_VNA_Two_Tone_Pwr_Lyzer(name="d1013", on_res_ind=33,#read_data=read_data, # VNA_name="RS VNA",
        rd_hdf=TA53_Read(main_file="Data_1103/S1A4_all_close_two_tone_pwr_long.hdf5"), #long_test.hdf5"), #
        #fit_indices=[range(48,154+1), range(276, 578+1)],
         desc="Gate to IDT low frequency",
         offset=-0.3,
         read_data=read_data,
         #swp_type="yoko_first",
        )
a.filt.center=57 #27 #139 #106 #  #137
a.filt.halfwidth=15
a.fitter.fit_type="refl_lorentzian"
a.fitter.gamma=0.1 #0.035
a.flux_axis_type="yoko" #"flux" #"fq" #
#a.bgsub_type="Complex" #"Abs" #"dB"

a.end_skip=20
#a.flux_indices=[range(479, 712)] #range(0,41), range(43, 479), range(482, len(a.yoko))]
#a.bgsub_type="dB" #"Abs"

a.save_folder.main_dir=a.name

a.read_data()
a.pwr2_ind=0
if 0:
    #a.pwr_ind=39
    print a.yoko.shape, a.frq2.shape
a.filter_type="None"
colormesh(absolute(a.MagcomData[:, :, 10, 0])) #.transpose()-absolute(a.MagcomData[:, 300, 10]))#.show()
    #a.magabs_colormesh(fig_width=6.0, fig_height=4.0)#.show()
    #scatter(absolute(a.MagcomFilt[170, 192, :]))
    #scatter(absolute(a.MagcomFilt[170, :, 3]))
    #a.ifft_plot(fig_width=6.0, fig_height=4.0)#.show() #, time_axis_type="time",
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
colormesh(absolute(a.MagcomFilt[:,:, 3]))
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

def ifft_plot(self, **kwargs):
    process_kwargs(self, kwargs, pl="hannifft_{0}_{1}_{2}".format(self.filter_type, self.bgsub_type, self.name))
    on_res=absolute(self.filt.window_ifft(self.MagcomData[:,self.on_res_ind, self.frq2_ind, self.pwr2_ind]))
    strt=absolute(self.filt.window_ifft(self.MagcomData[:,self.start_ind, self.frq2_ind, self.pwr2_ind]))
    stop=absolute(self.filt.window_ifft(self.MagcomData[:,self.stop_ind, self.frq2_ind, self.pwr2_ind]))

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
    if 0:
        double_filt= array([[self.filt.fft_filter(a.MagcomData[:,n, m]) for n in range(len(a.frq2))] for m in range(len(a.pwr2))])#.transpose()
        print double_filt.shape
        double_filt=swapaxes(double_filt, 0, 2)
        print double_filt.shape
        print a.pwr2[10]
        colormesh(self.freq_axis[a.end_skip:-a.end_skip], self.frq2, absolute(double_filt[a.end_skip:-a.end_skip, :, 10]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
        pl=colormesh(a.frq2, a.pwr2, absolute(double_filt[493, :, :]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
        print a.frequency[493]
        colormesh(absolute(double_filt[329, :, :]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
        colormesh(absolute(double_filt[93, :, :]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))
        colormesh(absolute(double_filt[880, :, :]).transpose()) #-absolute(double_filt[a.end_skip:-a.end_skip, 56, 134]).transpose())#-absolute(double_filt[50, 10:-10, 134]))

    return pl
ifft_plot(a).show()

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
