from threading import Thread
import socket
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import time

from UDPwebcam import UDPwebcam_receiver

def plotter(run, rec, fps_frame= 50) :
    t0 = time.time()
    nframe = 0  # the received frames
    fps =0
    while run():
        frame = rec.queue.get()
        #print(rec.header)
        nframe +=1
        fps_rate = 1/nframe + 1/fps_frame
        t1 = time.time()
        fps = fps_rate/(t1-t0) + (1-fps_rate)*fps
        t0=t1
        cv.imshow('recv', frame)
        cv.setWindowTitle('recv', f'received video, FPS={fps:.1f}, shape={rec.header["shape"]}')
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()

receiver = UDPwebcam_receiver(IP='192.168.137.1')
receiver.start()

rr=True
x = Thread(target=plotter, args=(lambda: rr, receiver))
x.start()

charin = ''
while charin != 'q':
    charin = input('press Enter to toggle start/stop, or q to quit: ')
    if receiver.control:
        receiver.stop()
    else:
        receiver.start()

receiver.start()
rr=False
x.join()
receiver.stop()


