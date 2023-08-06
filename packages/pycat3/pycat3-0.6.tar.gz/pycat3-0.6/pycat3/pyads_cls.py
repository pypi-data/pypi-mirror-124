import pyads
from time import sleep
import sys

class PyCat3:
    plc = pyads.Connection('127.0.0.1.1.1', 1)
    data = dict()
    def __init__(self, ip='127.0.0.1.1.1', port=851):
        PyCat3.plc = pyads.Connection(ip, port)
        PyCat3.plc.open()
        self.is_done = False
        
    def monitor(self, monitored_int=[], monitored_real=[], monitored_bool=[]):
        self.monitored_int = monitored_int
        self.monitored_real = monitored_real
        self.monitored_bool = monitored_bool
        self.run()
        
    def done(self):
        PyCat3.plc.close()
        self.is_done = True

    # Read tag
    def read_tag(self, tag):
        return PyCat3.plc.read_by_name(tag)

    # Write tag
    def write_tag(self, tag, val):
        PyCat3.plc.write_by_name(tag, val)

    # Call back for readig DINT tags
    @staticmethod
    @plc.notification(pyads.PLCTYPE_DINT) # 4 bytes
    def callback1(handle, name, timestamp, value):
        PyCat3.data.update({name : value})
        

    # Call back for reading LREAL tags
    @staticmethod
    @plc.notification(pyads.PLCTYPE_LREAL) # 8 bytes
    def callback2(handle, name, timestamp, value):
        PyCat3.data.update({name : value})
        

    # Call back for readig DINT tags
    @staticmethod
    @plc.notification(pyads.PLCTYPE_BOOL) # 4 bytes
    def callback3(handle, name, timestamp, value):
        PyCat3.data.update({name : value})
        
    def run(self):
        for tag in self.monitored_int:
            h1, u1 = PyCat3.plc.add_device_notification(tag, pyads.NotificationAttrib(4), self.callback1)

        for tag in self.monitored_real:
            h2, u2 = PyCat3.plc.add_device_notification(tag, pyads.NotificationAttrib(8), self.callback2)

        for tag in self.monitored_bool:
            h3, u3 = PyCat3.plc.add_device_notification(tag, pyads.NotificationAttrib(1), self.callback3)
            

class EdgeTrigger:
    def __init__(self, callback):
        self.value = None
        self.callback = callback

    def __call__(self, value):
        if value != self.value:
            self.callback(self.value, value)
        self.value = value