from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from threading import Thread
import time
import cv2
from UDPwebcam import UDPwebcam_receiver
import socket
import json
import os

class sendChanel() :
    def __init__(self, settings) :
        print("initiate send channel")
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_address = (settings['IP'], settings['control_port'])
        self.tcp_socket.bind(server_address)
        
        self.speed = [0,0]
        self.angles = settings["default-angles"]
        self.dangle = settings["dangle"]
        self.acc = settings['acc']
        self.dec = settings['dec']
        self.maxSpeed = settings['maxSpeed']
        self.back_acc = settings['back_acc']
        self.back_dec = settings['back_dec']
        self.maxBackSpeed = settings['maxBackSpeed']
        self.turnV = settings['turnV']
        self.maxturnV = settings['maxturnV']
    
        self.tcp_socket.listen(1)
        print("Waiting for connection")
        self.connection, client = self.tcp_socket.accept()
    
    def close(self) :
        print("close send channel")
        self.sendControl(message='end')
        self.connection.close()
        self.tcp_socket.close()

    def accelerateCar(self, sgn) :
        if sgn == 0:
            self.speed= [0,0]
            self.sendControl()
            return
        
        if self.speed[0] >= 0:
            if sgn > 0:
                self.speed[0] += self.acc
                if self.speed[0] > self.maxSpeed:
                    self.speed[0] = self.maxSpeed
            else :
                self.speed[0] -= self.dec
        if self.speed[0] < 0:
            if sgn < 0:
                self.speed[0] -= self.back_acc
                if self.speed[0] < -self.maxBackSpeed:
                    self.speed[0] = -self.maxBackSpeed
            else :
                self.speed[0] += self.back_dec
        print(f'accelerateCar: {sgn}, {self.speed}, {self.acc}')
        self.sendControl()
    
    def breakCar(self) : 
        self.speed= [0,0]
        self.sendControl()

    def turnCar(self, sgn) :
        print(f'turnCar: {sgn}, {self.speed}')
        if sgn == 0:
            self.speed[1] = 0
        elif sgn > 0:
            self.speed[1] += self.turnV
            if self.speed[1] > self.maxturnV:
                self.speed[1] = self.maxturnV
        else:
            self.speed[1] -= self.turnV
            if self.speed[1] < -self.maxturnV:
                self.speed[1] = -self.maxturnV
        self.sendControl()

    def sendControl(self, message="speed", parameter="") :
        try:
            dictr = {
                'message' : message,
                'speed' : self.speed,
                "angles" : self.angles,
                "parameter" : parameter,
            }
            print(json.dumps(dictr).encode('utf-8'))
            self.connection.sendall(json.dumps(dictr).encode('utf-8'))
        except:
            print('send failed')
            #if input("Stop?")=="I":
            exit(216)

    def turn_servo(self, directions):
        self.angles = [max(min(self.angles[i]+self.dangle*directions[i], 180), 0) for i in range(3)]
        self.sendControl()
    
    def reset_servo(self):
        self.angles = settings["default-angles"]
        self.sendControl()

class receiveChanel() :
    def __init__(self, root, settings) :
        print("initiate receive channel")

        self.receiver = UDPwebcam_receiver(bufsize = settings['bufsize'], IP = settings['IP'], port= settings['webcam_port'])
        self.receiver.start()

        self.root=root
        self.imlabel = Label(self.root)
        self.imlabel.pack()

        self.L= settings['window_size']
        self.run = True
        self.thread = Thread(target=self.updateImage)
        self.thread.start()

        self.textlabel = Label(self.root, text=f'webcam')
        self.textlabel.pack(side='left')

        self.dislabel = Label(self.root, text = f'd = {self.receiver.dist} cm')
        self.dislabel.pack(side = "right")

        self.is_record = False
        self.recorded_video = None

        self.rec_label = Label(self.root, text = f'recording = {self.is_record}')
        self.rec_label.pack(side = "left")


 
    def close(self) :
        print("close receive channel")

        self.run = False
        self.thread.join()
        self.receiver.stop()

    def updateImage(self) :
        while self.run:
            jpgrec = self.receiver.queue.get()
            frame = cv2.imdecode(jpgrec, cv2.IMREAD_UNCHANGED)
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            self.showImage(image)
            if self.is_record:
                self.recorded_video.write(np.array(frame))
                #print(np.array(image).shape)

    def showImage(self,  image) :
        newsize = [int(n) for n in np.array(image.size)/np.max(np.array(image.size)/self.L)]
        image = image.resize(newsize)
        if self.run:
            photo = ImageTk.PhotoImage(image)

            self.imlabel.configure(image=photo)
            self.imlabel.image = photo

            self.dislabel.configure(text = f'd = {self.receiver.dist:.1f} cm')


pressed_l = False
pressed_b = False

def handle_key_press(event, root, sendCh, recCh):
    global pressed_l, pressed_b
    
    if event.keysym == 'b':
        pressed_l = False
        if pressed_b:
            sendCh.sendControl("buzzer", "whole")
            pressed_b = False
        else:
            pressed_b = True
        return
    if event.keysym == 'l':
        pressed_b = False
        if pressed_l:
            sendCh.sendControl("dot", "animation")
            pressed_l = False
        else:
            pressed_l = True
        return
    if event.keysym == 'v' and pressed_b:
        sendCh.sendControl('buzzer', 'violent')
    if event.keysym == 'n' and pressed_b:
        sendCh.sendControl('buzzer', 'nino')
    if  event.keysym == 'y' and pressed_b:
        sendCh.sendControl('buzzer', 'supermario')
    if event.keysym == 'c' and pressed_l:
        sendCh.sendControl("dot", "clear")
    
    pressed_l = False
    pressed_b = False
    
    
    if event.keysym == 'Escape' or event.keysym == 'q':
        recCh.close()
        sendCh.close()
        root.destroy()
        return

    if event.keysym == 'Down':
        sendCh.accelerateCar(-1)
        recCh.textlabel.configure(text = f'speed = {sendCh.speed[0]}')
        return
    if event.keysym == 'Up':
        sendCh.accelerateCar(1)
        recCh.textlabel.configure(text = f'speed = {sendCh.speed[0]}')
        return
    if event.keysym == 'Right':
        sendCh.turnCar(1)
        recCh.textlabel.configure(text = f'speed = {sendCh.speed[0]}, turn right')
        return
    if event.keysym == 'Left':
        sendCh.turnCar(-1)
        recCh.textlabel.configure(text = f'speed = {sendCh.speed[0]}, turn left')
        return
    if event.keysym == 'space':
        sendCh.breakCar()
        sendCh.reset_servo()
        recCh.textlabel.configure(text = f'speed = {sendCh.speed[0]}, break')
    
    if event.keysym == "a":
        sendCh.turn_servo([0,1,0])
    if event.keysym == "d":
        sendCh.turn_servo([0,-1,0])
    if event.keysym == "s":
        sendCh.turn_servo([0,0, 1])
    if event.keysym == "w":
        sendCh.turn_servo([0,0,-1])
    if event.keysym == "o":
        sendCh.turn_servo([1,0,0])
    if event.keysym == "p":
        sendCh.turn_servo([-1,0,0])
    
    if event.keysym == 'm':
        sendCh.sendControl('measure')
    if event.keysym == 'u':
        if recCh.is_record:
            recCh.recorded_video.release()
        else:
            recCh.recorded_video = cv2.VideoWriter(f'../video/robot-video-cam-{time.time()}.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (640,480))
        recCh.is_record = not recCh.is_record
        recCh.rec_label.configure(text = f'recording = {recCh.is_record}')



def handle_key_release(event, root, sendCh, recCh):
    sendCh.turnCar(0)

#os.system('xset r off')

# Create the main window
with open('settings.json') as f:
    settings = json.load(f)

root = Tk()
root.title("Image Viewer")

sc = sendChanel(settings)
rc = receiveChanel(root, settings)
root.bind("<Key>", lambda event: handle_key_press(event, root, sc, rc))

root.mainloop()