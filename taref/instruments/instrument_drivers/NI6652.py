# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 14:33:04 2016

@author: Morran or Lumi blah
"""

from ctypes import c_long, byref, c_bool, WinDLL, c_char_p, create_string_buffer, c_double
from time import sleep
from pxi_backbone import PXI_Backbone, pp

class NISYNC_VAL_Lib(object):
    """dictionary object of constants since niSync does not have a COM library"""
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
    def __init__(self, reset=True):
        """uses PXI_Backbone initialization with appropriate arguments. resets the timing module if reset is True"""
        super(NI6652, self).__init__('niSync.dll', func_prefix='niSync_')
        if reset:
            self.reset()

    def create_object(self, address="PXI7::15::INSTR"):
        """creates the object and returns the session value"""
        self.address=address
        ses=c_long()
        self.do_func_no_session('init', address, False, False, byref(ses))
        return ses.value

    def reset(self):
        """resets the timing module. useful since closing it does not reset it"""
        self.do_func("reset")
    #msg=create_string_buffer(256)

    def get_error_message(self):
        """returns error message of timing module"""
        self.do_func('error_message', self.error_code, self.error_msg)
        return self.error_msg.value

    def connect_SW_trigger(self, terminal='PXI_Star1'): #PXI_Star5
        """connects a given terminal to the software trigger"""
        self.do_func('ConnectSWTrigToTerminal', 'GlobalSoftwareTrigger',
                    terminal, "SyncClkFullSpeed", 0, 0, c_double(0.0))

    def send_software_trigger(self):
        """sends the software trigger"""
        self.do_func('SendSoftwareTrigger', 'GlobalSoftwareTrigger')

    def send_many_triggers(self, n, sleep_time=0.1):
        """sends multiple software triggers with a pause in between each one"""
        for n in range(n):
            self.send_software_trigger()
            sleep(sleep_time)

    def disconnect_software_trigger(self, terminal='PXI_Star1'):
        """disconnects terminal from software trigger"""
        self.do_func('DisconnectSWTrigFromTerminal', 'GlobalSoftwareTrigger', terminal)

    def close(self):
        """closes the timing module"""
        self.do_func('close')

    def stop(self, reset=True):
        """stop resets the timing module if desired and then closes it"""
        if reset:
            self.reset()
        self.close()

if __name__=="__main__":
    try:
        m=NI6652()
        m.connect_SW_trigger()
        m.send_software_trigger()
    except Exception as e:
        m.close()
        raise e
    finally:
        if 0:
            m.close()
