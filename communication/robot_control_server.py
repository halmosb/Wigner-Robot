import socket
import json
import keyboard
import numpy as np
import time
import cv2 as cv
from tkinter import Tk, Canvas
from threading import Thread

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
        mas = cv.waitKey(1)
        if mas & 0xFF == ord('q'):
            break
        else:
            print(mas)
    cv.destroyAllWindows()

receiver = UDPwebcam_receiver(IP='192.168.137.1')
receiver.start()

rr=True
x = Thread(target=plotter, args=(lambda: rr, receiver))
x.start()

# Set up a TCP/IP server
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 
server_address = ('192.168.137.1', 8100)
tcp_socket.bind(server_address)
# 
tcp_socket.listen(1)
print("Waiting for connection")
connection, client = tcp_socket.accept()
print(f'connected to {client}')
message = 'start'

speed  = np.array([0,0], dtype=float)
kin = ' '

receiver = UDPwebcam_receiver(IP='192.168.137.1')
receiver.start()


"""

while kin != 'q':
    kin = keyboard.read_key()
    if receiver.control:
        receiver.stop()
    else:
        receiver.start()
    if kin == 'up' :
        dv = np.array([1,0], dtype=float)
    elif kin == 'down' :
        dv = np.array([-1,0], dtype=float)
    elif kin == 'right' :
        dv = np.array([0,1], dtype=float)
    elif kin == 'left' :
        dv = np.array([0,-1], dtype=float)
    elif kin == 'space' :
        dv = -speed
    elif kin == 'q' :
        dv = np.array([0,0], dtype=float)
    else:
        continue
    speed = np.array([ min( max(speed[i] + dv[i] ,-100.0),100.0) for i in range(2) ])
    print(f'speed = {speed}')
    dd = {
        'message' : kin,
        'speed' : list(speed)
    }
    connection.sendall(json.dumps(dd).encode('utf-8'))
    time.sleep(0.1)
#    except:
#        print('send failed')

"""
receiver.start()
connection.close()
tcp_socket.close()

rr=False
x.join()
receiver.stop()
 