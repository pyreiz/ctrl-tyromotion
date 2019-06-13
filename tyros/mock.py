#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 20:20:57 2019

@author: rgugg
"""
import random
import time
import socket
from datetime import datetime 
# %%
def amadeo_msg_generator():
    a = "<Amadeo>"  
    b = "</Amadeo>\r\n"
    t0 = t1 = time.time()
    while True:
        msg = '\t'.join([f'{random.random():.3f}' for _ in range(0,10,1)])    
        date = datetime.now().strftime("%H:%m:%S") + "\t"
        msg = ''.join((a, date, msg, b))
        msg = msg.replace('.',',')
        msg = msg.encode()
        t1 = time.time()
        yield msg
        while (t1-t0) < .05: #Amadeo has approx. 20Hz sampling rate
            t1 = time.time()
        t0 = t1

class Mock():
    def __init__(self, device="Amadeo", host="127.0.0.1", port=61585): 
        """
        port:int
            defaults to 61585 because 6 keeps it ourt the registered ports and 
            1585 is the year when Graz University was founded 
        """
        self.interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.interface.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.interface.bind((host, port))
        self.device = device
        
        if device == "Amadeo":
            self.generator = amadeo_msg_generator()
        
        print("Starting to mock", device)
    
    def run(self):
        self.interface.listen(1)
        t0 = time.time()        
        while True:
            (client, address) = self.interface.accept()
            if client:
                while True:
                    msg = next(self.generator)
                    t1 = time.time()
                    print(msg, t1-t0)
                    t0 = t1
                    try:
                        client.send(msg)
                    except ConnectionResetError as e:
                        print(e)
                        break
            
            
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(prog="python -m tyros.mock")
    parser.add_argument("--device",choices=["Amadeo"], required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=61585, type=int)
    args = parser.parse_args()
    m = Mock(device=args.device, host=args.host, port=args.port)
    m.run()

