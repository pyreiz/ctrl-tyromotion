import socket
import time
import pylsl
from xml.etree import ElementTree
from itertools import chain
# %%
def decode(msg):
    msg = msg.decode("ascii").strip()
    xml = ElementTree.fromstring(msg)
    return xml

def convert(xml):        
    msg = xml.text        
    msg = msg.replace(",",".")
    parts = msg.split('\t')
    return [float(x) for x in parts[1:]]

def make_outlet(device:str="Amadeo"):
    if device == "Amadeo":
        info = pylsl.StreamInfo(name="tyroS",
                                type="mixed",
                                channel_count=10,
                                nominal_srate=20,
                                channel_format="float32",
                                source_id="tyromotion")
        
        acq = info.desc().append_child("acquisition")
        acq.append_child_value('manufacturer', 'tyromotion')
        acq.append_child_value('model', str(device))     
        acq.append_child_value('compensated_lag', '0')
        channels = info.desc().append_child("channels")
        # position goes from -1 (mechanical limit flexion) to 
        # 0 (mechanical limit extension)
        # force is in N, negative is in direction of flexion, 
        # positive in  direction of extension
        finger_names = ["pollex", "index", "medius", "anularius", "minimus"]
        types = chain((f"extension" for x in range(1,6,1)),
                      (f"force" for x in range(1,6,1)))
        units = chain(("au" for x in range(1,6,1)),
                      ("N" for x in range(1,6,1)))
        names = chain((f"position_{f}" for f in finger_names),
                       (f"force_{f}" for f in finger_names))
        for c, u, t in zip(names, units, types):
                    channels.append_child("channel") \
                    .append_child_value("label", c) \
                    .append_child_value("unit", u) \
                    .append_child_value("type", t)   
    
    
    print("Robotic device was changed, resetting Outlet")
    print(info.as_xml())
    return pylsl.StreamOutlet(info)

class Client():

    _device = None
    
    def __init__(self, host="127.0.0.1", port=61585):
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port   
        self.is_connected = False 
        
    def connect(self):
        self.interface.connect((self.host, self.port))
        self.is_connected = True
       
    def close(self):
        self.interface.close()
        self.is_connected = False
 
    @property
    def device(self):
        return self._device
    
    @device.setter
    def device(self, newdevice:str):        
        if self._device != newdevice:
            print(newdevice)
            self._outlet = make_outlet(newdevice)
            self._device = newdevice
        
    def _receive(self):
        msg = bytes("", "ascii")
        while len(msg)<2:
            msg += self.interface.recv(1)            
        while msg[-2:] != b"\r\n":
            msg += self.interface.recv(1)
        tstamp = pylsl.local_clock()        
        return decode(msg), tstamp

    def receive(self):
        xml, tstamp = self._receive()
        self.device = xml.tag
        chunk = convert(xml)
        return chunk, tstamp
        
    
    def push(self, chunk, tstamp=None):
        if tstamp is None:
            tstamp = pylsl.local_clock()        
        self._outlet.push_sample(chunk, tstamp)
    
if __name__ == "__main__":
    client = Client()
    while not client.is_connected:
        try:
            client.connect()
        except Exception as e:
            print(e)
    while True:
        chunk, tstamp = client.receive()        
        print(chunk, "at ", tstamp)
        client.push(chunk, tstamp)
        
        
