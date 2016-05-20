# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 14:09:24 2016

@author: Morran or Lumi
"""

from ctypes import WinDLL, c_float, get_errno, get_last_error, create_string_buffer, Structure, c_long, c_double, POINTER, c_char_p, c_void_p,  byref, pointer

class Pack(Structure):
    _fields_ = [
                ('IQ_file_format', c_long),
                ('IQ_data_format', c_long),
            ('input_sampling_rate', c_float),
            ('output_sampling_rate', c_float),
            ('signal_bandwidth', c_float),
            ('oversampling_factor', c_float), #must be >=1
            ('marker_type', c_long),
            ('scaling_factor', c_float),
            ('marker_file_name', c_void_p)]

IQ_file_format_dict={'User IQ' : 12, 'User I and Q' : 13}

IQ_data_format_dict={'14-bit signed integer': 21,
                     '14-bit unsigned integer' : 22,
                     '16-bit signed integer' : 23,
                     '16-bit unsigned integer' : 24,
                     '32-bit signed integer' : 25,
                     '32-bit unsigned integer' : 26,
                     'IEEE 32-bit float' :27,
                     'ASCII' : 28}

marker_type_dict={'No Markers' : 41, 'Marker File' : 42}

class af302xCPackager(object):
    def __init__(self, lib_name='af302xCPackager', IQ_file_format='User I and Q', IQ_data_format='ASCII',
                 input_sampling_rate=2.0e8, output_sampling_rate=None, signal_bandwidth=1.0e8, oversampling_factor=1.0,
                 marker_type='No Markers', scaling_factor=100.0, marker_file_name=None,
                 I_file_name='TA_pyI.txt', Q_file_name='TA_pyQ.txt', aiq_file_name='TA_pyaiq.aiq',
                 description='pyARB',
                 dir_path=r"C:\Users\Morran or Lumi\Documents\Thomas"+"\\", waveform=None):

        self.msg=create_string_buffer(256)
        self.afP=WinDLL('af302xCPackager')

        if output_sampling_rate is None:
            output_sampling_rate=input_sampling_rate

        self.p=Pack(IQ_file_format=IQ_file_format_dict[IQ_file_format],
                    IQ_data_format=IQ_data_format_dict[IQ_data_format],
                    input_sampling_rate=input_sampling_rate,
                    output_sampling_rate=output_sampling_rate,
                    signal_bandwidth=signal_bandwidth,
                    oversampling_factor=oversampling_factor,
                    marker_type=marker_type_dict[marker_type],
                    scaling_factor=scaling_factor,
                    #marker_file_name=r'C:\Users\Morran or Lumi\Documents\Thomas\tom_marker.mkr'
                    )

        self.I_file_name=I_file_name
        self.Q_file_name=Q_file_name
        self.aiq_file_name=aiq_file_name
        self.description=description
        self.dir_path=dir_path
        if waveform is not None:
            self.save_waveform(waveform)
            
    def get_error_message(self, error_code):
        """utility function that returns last error message"""
        self.afP.GetPackagerErrorString(error_code, self.msg)
        return self.msg.value
    
    def error_check(self):
        """utility function for error checking"""
        if self.error_code==0:
            print "[{0}] No error: {1}".format(str(type(self)), self.error_code)
            return
        msg=self.get_error_message()
        err_msg="[{name}] {code}: {msg}".format(str(type(self)), code=self.error_code, msg=msg)
        if self.error_code>0:
            print "WARNING: "+err_msg
            return
        raise Exception("ERROR: "+err_msg)

#    def gen_waveform(self):
#        temp=[str(0) for n in range(300)]
#        #a.extend([str(1) for n in range(300)])
#        temp[10]='1'
#        temp=','.join(temp)
#        return temp, temp

    @property
    def group_IQ(self):
        return self.p.IQ_file_format==IQ_file_format_dict['User IQ']

    @property
    def I_file_path(self):
        return self.dir_path+self.I_file_name

    @property
    def Q_file_path(self):
        if self.group_IQ:
            return ""
        return self.dir_path+self.Q_file_name

    @property
    def aiq_file_path(self):
        return self.dir_path+self.aiq_file_name

    def save_waveform(self, waveform):
        Q=None
        if self.group_IQ:
            I=waveform
        else:
            I, Q=waveform
        with open(self.I_file_path, 'w') as f:
            f.write(I)
        if Q is not None:
            with open(self.Q_file_path, 'w') as f:
                f.write(Q)

    def marker_file(self):
        pass
    #        if os.path.isfile(sMpath):
        #            del(sMpath)
        #with open('tom_marker.mkr', 'w') as Mref:
        #    Mref.write('FrameLength=' + str(4) + '\r\n')
        #    Mref.write('Oversampling=1  \r\nDecimation=1 \r\nMkr1=General \r\nMarker 1 \r\n')
        #    Mref.write(str(0) + ',' + str(3) + '\r\n')

    def package_waveform(self, waveform=None):
        if waveform is not None:
            self.save_waveform(waveform)
        self.error_code=self.afP.PackageToAiq(self.I_file_path, self.Q_file_path,
                               self.aiq_file_path, self.description,
                               byref(self.p))
        self.error_check()

if __name__=="__main__":
    a=af302xCPackager()
    a.package_waveform()

