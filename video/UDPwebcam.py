from threading import Thread
from queue import Queue
import socket
import numpy as np
import cv2 as cv
import time


class UDPwebcam_sender :
    control = True
    def __init__(self, shape=None, bufsize=512, IP='127.0.0.1', port=65534, startCode = b'start') :
        #open socket
        self.addr=(IP, port)
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.startCode = startCode

        # open webcam
        self.cam = cv.VideoCapture(0)
        if shape is not None:
            width, height = shape
            self.cam.set(cv.CAP_PROP_FRAME_HEIGHT, height)
            self.cam.set(cv.CAP_PROP_FRAME_WIDTH, width)
        ret, frame = self.cam.read()
        if not ret:
            raise ValueError('camera seems not to work')
        self.shape = frame.shape

        #prepare metadata header
        metadata = self.startCode + (f'start:{self.shape}:').encode('utf-8')
        self.header = metadata + ((self.bufsize - len(metadata)) * 'a').encode('utf-8')

    def send_function(self) :
        print("Start thread: send")
        while(self.cam.isOpened() and UDPwebcam_sender.control):
            ret, frame = self.cam.read()
            if ret:
                self.sock.sendto(self.header, self.addr)
                data = frame.tobytes()
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
    def __init__(self, bufsize=512, IP='127.0.0.1', port=65534, startCode = b'start') :
        self.control = True
        self.queue = Queue()

        #open socket
        self.addr=(IP, port)
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.startCode = startCode
        self.sock.bind(self.addr)
        
    def receive_function(self) :
        print('Start thread: receive')
        chunks = []
        num_chunks = -1
        while self.control:
            chunk, _ = self.sock.recvfrom(self.bufsize)
            if chunk.startswith(self.startCode):
                headerlist = str(chunk).split(':')
                try:
                    shape=[int(n) for n in headerlist[1][1:-1].split(',')]
                    imgsize = shape[0]*shape[1]*shape[2]
                except:
                    continue
                num_chunks = imgsize/self.bufsize
                chunks = []
                #print('Got start')
            else:
                chunks.append(chunk)
            
            if len(chunks) == num_chunks:
                #print("Complete image")
                byte_frame = b''.join(chunks)
                frame = np.frombuffer(byte_frame, dtype=np.uint8).reshape(*shape)
                self.queue.queue.clear()
                self.queue.put(frame)
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
