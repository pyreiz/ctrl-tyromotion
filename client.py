import socket
import time
import pylsl
# %%
class Client():

    def __init__(self, host="127.0.0.1", port=7777):
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        
    def connect(self):
        self.interface.connect((self.host, self.port))

    def close(self):
        self.interface.close()
    
    def receive(self):
        msg = bytes("", "ascii")
        while len(msg)<2:
            msg += self.interface.recv(1)
            
        while msg[-2:] != b"\r\n":
            msg += self.interface.recv(1)
        tstamp = pylsl.local_clock()        
        return msg, tstamp
    
    def decode(self, msg):
        msg = msg.decode("ascii").strip()
        msg = msg.replace("<Amadeo>","")
        msg = msg.replace("</Amadeo>", "")
        msg = msg.replace(",",".")
        parts = msg.split('\t')
        time.sleep(0.01)
        return [float(x) for x in parts[1:]]
    
if __name__ == "__main__":
    client = Client()
    client.connect()
    info = pylsl.StreamInfo(name="AmadeoTyroS",
                                type="Force",
                                channel_count=10,
                                nominal_srate=20,
                                channel_format="float32",
                                source_id="tyromotion")

    #outlet = pylsl.StreamOutlet(info)
    while True:
        time.sleep(0.01)
        msg, tstamp = client.receive()
        data = client.decode(msg)
        print(data, "at ", tstamp)
        #outlet.push_chunk(data, tstamp)
        
        
