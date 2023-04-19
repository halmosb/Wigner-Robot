from flask import Flask, render_template, Response
from time import sleep
from threading import Thread
import socket
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import time

from UDPwebcam import UDPwebcam_receiver

app = Flask(__name__)

class Control :
    t0 = time.time()
    nframe = 0  # the received frames
    fps =0
    fps_frame= 50
    IP='192.168.137.1'
    receiver = None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def gen():
        vid = cv.VideoCapture('lights_go.mp4')
        while True:
            success, frame = vid.read()
            if not success:
                break
            _, buffer = cv.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            sleep(0.05)
        vid.release()
#    def gen():
#        while True:
#            frame = Control.receiver.queue.get()
#            print(frame.shape)
#            #print(Control.receiver.header)
#            #nframe +=1
#            #fps_rate = 1/nframe + 1/Control.fps_frame
#            #t1 = time.time()
#            #fps = fps_rate/(t1-t0) + (1-fps_rate)*fps
#            #t0=t1
#            _, buffer = cv.imencode('.jpg', frame)
#            frame = buffer.tobytes()
#            yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#            sleep(0.04)
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    #Control.receiver = UDPwebcam_receiver()
    #Control.receiver.start()

    #app.run(host='0.0.0.0', port=8000)
    print("---> START APP <---")
    app.run(host='0.0.0.0')
