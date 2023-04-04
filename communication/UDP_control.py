from threading import Thread
import socket
import json


class UDPcontrol_server:

    def __init__(self, IP='192.168.137.1', port=6243, bufsize=1024):
        #open socket
        self.addr=(IP, port)
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.addr)

    def send(self, data):
        sendata = json.dumps(data).encode('utf-8')
        

class UDPcontrol_client:
    def __init__(self, IP='192.168.137.1', port=6243, bufsize=1024):
        #open socket
        self.addr=(IP, port)
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def start(self):
        print('Start thread: Control client')
        self.control = True
        self.thread = Thread(target=self.control_function)
        self.thread.start()
    
    def stop(self) :
        print('Stop thread: Control client')
        self.control=False

    def control_function(self):
        pass