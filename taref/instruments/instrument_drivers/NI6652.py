# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 14:33:04 2016

@author: Morran or Lumi
"""

from ctypes import c_long, byref, c_bool, WinDLL, c_char_p, create_string_buffer, c_double
from time import sleep
from pxi_backbone import PXI_Backbone, pp

class NISYNC_VAL_Lib(object):
    NISYNC_VAL_SWTRIG_GLOBAL="GlobalSoftwareTrigger"
    NISYNC_VAL_PXISTAR1="PXI_Star1"
    NISYNC_VAL_PXISTAR5="PXI_Star5"
    NISYNC_VAL_PFI0="PFI0"
    NISYNC_VAL_SYNC_CLK_FULLSPEED="SyncClkFullSpeed"

    NISYNC_VAL_DONT_INVERT=0
    NISYNC_VAL_INVERT=1

    NISYNC_VAL_UPDATE_EDGE_RISING=0
    NISYNC_VAL_UPDATE_EDGE_FALLING=1

class NI6652(PXI_Backbone):
    def __init__(self):
        super(NI6652, self).__init__('niSync.dll', func_prefix='niSync_')#,
                  #com_lib=NISYNC_VAL_Lib, const_prefix="NISYNC_VAL_")

    def create_object(self, address="PXI7::15::INSTR"):
        self.address=address
        ses=c_long()
        self.do_func_no_session('init', address, False, False, byref(ses))
        return ses.value

    #msg=create_string_buffer(256)

    def get_error_message(self, error_code):
        self.do_func('error_message', self.error_code, self.error_msg)
        return self.error_msg.value

    def connect_SW_trigger(self):
        self.do_func('ConnectSWTrigToTerminal', 'GlobalSoftwareTrigger',
                    'PXI_Star5', "SyncClkFullSpeed", 0, 0, c_double(0.0))

    def send_software_trigger(self):
        self.do_func('SendSoftwareTrigger', 'GlobalSoftwareTrigger')

    def send_many_triggers(self, n):
         for n in range(n):
             self.send_software_trigger()
             sleep(0.1)

    def disconnect_software_trigger(self):
        self.do_func('DisconnectSWTrigFromTerminal', 'GlobalSoftwareTrigger', 'PXI_Star1')

    #_lib.niSync_ConnectSWTrigToTerminal(session, 'GlobalSoftwareTrigger', 'PXI_Star1', "SyncClkFullSpeed", 0, 0, c_double(0.0))
    def close(self):
        self.do_func('close')

if __name__=="__main__":
    try:
        m=NI6652()
        m.connect_SW_trigger()
        m.send_software_trigger()
    finally:
        if 0:
            m.close()
