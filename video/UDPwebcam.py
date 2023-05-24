from threading import Thread
from queue import Queue
import socket
import numpy as np
import cv2 as cv
import time
import json


class UDPwebcam_sender :
    control = True
    def __init__(self, shape=None, bufsize=1024, IP='127.0.0.1', port=65534):
        #open socket
        self.addr=(IP, port)
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dist = 0

        # open webcam
        self.cam = cv.VideoCapture(0)
        if shape is not None:
            width, height = shape
            self.cam.set(cv.CAP_PROP_FRAME_HEIGHT, height)
            self.cam.set(cv.CAP_PROP_FRAME_WIDTH, width)
        ret, frame = self.cam.read()
        if not ret:
            raise ValueError('camera does not seem to work')
        self.info = {
            "frame": "start",
            "shape": frame.shape,
            "bufsize": self.bufsize
        }

    def send_function(self) :
        print("Start thread: send")
        while(self.cam.isOpened() and UDPwebcam_sender.control):
            ret, frame = self.cam.read()
            if ret:
                success, jpgimage = cv.imencode('.jpg', frame)
                jpgimage = jpgimage.reshape(-1)
                nframes = int(len(jpgimage)/self.bufsize)+1
                self.info.update({
                    'len': len(jpgimage),
                    'nframes' : nframes,
                    'distance': self.dist
                })
                #prepare metadata header
                metadata = json.dumps(self.info).encode('utf-8')
                header = metadata + ((self.bufsize - len(metadata)) * 'a').encode('utf-8')
                self.sock.sendto(header, self.addr)
                data = np.concatenate((jpgimage, np.zeros(nframes*self.bufsize-len(jpgimage), dtype=np.uint8) )).tobytes()
                for i in range(0, len(data), self.bufsize):
                    self.sock.sendto(data[i:i+self.bufsize], self.addr)
            else:
                break
        print("Stop thread: send")

    def start(self) :
        UDPwebcam_sender.control = True
        self.thread = Thread(target=self.send_function)
        self.thread.start()
    
    def stop(self) :
        UDPwebcam_sender.control=False

    def __del__(self) :
        self.cam.release()
        self.sock.close()


class UDPwebcam_receiver :
    def __init__(self, bufsize=2048, IP='127.0.0.1', port=65534) :
        self.control = True
        self.queue = Queue()
        self.dist = 0

        #open socket
        self.addr=(IP, port)
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.startCode = b'{"frame": "start"'
        self.sock.bind(self.addr)
        
    def receive_function(self) :
        print('Start thread: receive')
        chunks = []
        num_chunks = -1
        while self.control:
            message, _ = self.sock.recvfrom(self.bufsize)
            #print(message)
            if message.startswith(self.startCode):
                self.header = json.loads(message.decode('utf-8').rstrip('a'))
                jpglen=self.header['len']
                num_chunks = self.header['nframes']
                self.bufsize = self.header['bufsize']
                self.dist = self.header["distance"]
                chunks = []
                #print('Got start')

            else:
                chunks.append(message)
            
            if len(chunks) == num_chunks:
                #print("Complete image")
                jpgrec = np.frombuffer((b''.join(chunks)), dtype=np.uint8)[:jpglen]
                #frame = cv.imdecode(jpgrec, cv.IMREAD_UNCHANGED)
                self.queue.queue.clear()
                self.queue.put(jpgrec)
        print('Stop thread: receive')
        

    def start(self) :
        print('UDPwebcam_receiver.start')
        self.control=True
        self.thread = Thread(target=self.receive_function)
        self.thread.start()
    
    def stop(self) :
        print('UDPwebcam_receiver.stop')
        self.control=False

    def __del__(self) :
        self.sock.close()
