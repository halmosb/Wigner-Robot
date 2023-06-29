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
from control import Control
import copy
from queue import Queue
import torch
from torch import nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from statistics import mode

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 3, 4, 1)
        self.conv2 = nn.Conv2d(3, 3, 4, 1)
        self.conv3 = nn.Conv2d(3, 3, 4, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(45, 20)
        self.fc2 = nn.Linear(20, 4)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.conv3(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        #x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        #x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output
    
transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])

model_path = '../AI/Arm/Models/0001.model'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device ="cpu"
model = torch.jit.load(model_path).to(device)
model.eval()

#model = Net().to(device)
#model.load_state_dict(torch.load(model_path))
#exit(0)

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
            #self.speed[1] *= (-1) TODO
            self.speed[1] -= self.turnV
            if self.speed[1] > self.maxturnV:
                self.speed[1] = self.maxturnV
            elif self.speed[1]  < -self.maxturnV:
                self.speed[1] = -self.maxturnV
        self.sendControl()

    def sendControl(self, message="speed", parameter="", log = True) :
        try:
            dictr = {
                'message' : message,
                'speed' : self.speed,
                "angles" : self.angles,
                "parameter" : parameter,
            }
            if log:
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
    def __init__(self, root, settings, sc) :
        print("initiate receive channel")

        self.receiver = UDPwebcam_receiver(bufsize = settings['bufsize'], IP = settings['IP'], port= settings['webcam_port'])
        self.receiver.start()

        self.root=root
        self.imlabel = Label(self.root)
        self.imlabel.pack()
        self.sendCh = sc

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

        self.pred_label = Label(self.root, text = "")
        self.pred_label.pack(side="right")

        self.rec_label = Label(self.root, text = f'recording = {self.is_record}')
        self.rec_label.pack(side = "left")

        self.prevdir = []
        #print(self.sendCh)
 
    def close(self) :
        print("close receive channel")

        self.run = False
        self.thread.join()
        self.receiver.stop()

    def updateImage(self) :
        while self.run:
            if self.receiver.dist < settings["emergency_break_distance"]:
                if not Control.breakCar and self.sendCh.speed[0] > 0:
                    Control.breakCar = True
                    self.sendCh.sendControl("buzzer", "nino")
                    self.sendCh.breakCar()
            else:
                Control.breakCar = False
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
            image2 = copy.deepcopy(image)
    
            center_x = 590
            center_y = 50
            radius = 300
            color = (255, 0, 0)  # Red color
            if self.is_record and int(time.time())%2 == 0:
                draw = ImageDraw.Draw(image2)
                draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=color)

            photo = ImageTk.PhotoImage(image2)
            self.imlabel.configure(image=photo)
            self.imlabel.image = photo

            self.dislabel.configure(text = f'd = {self.receiver.dist:.1f} cm')
            #self.pred_label.configure(text=model(transform(image.resize((64, 48))).to(device)))
            pred = ["up", "down", "left", "right","center"][int(torch.max(model(transform(image.resize((64, 48)).convert('L')).unsqueeze(0).to(device)), 1)[1].item())]
            self.pred_label.configure(text=pred)
            if len(self.prevdir) >= settings["max_dir_queue_size"]:
                self.prevdir.pop(0)
            self.prevdir.append(pred)
            print(self.prevdir)
            if Control.send_AI_dot:
                if self.prevdir.count(mode(self.prevdir)) >= 0.7*settings["max_dir_queue_size"]:
                    self.sendCh.sendControl("dot", pred, False)
                else:
                    self.sendCh.sendControl("dot", "line", False)


pressed_l = False
pressed_b = False

def handle_key_press(event, root, sendCh, recCh):
    global pressed_l, pressed_b
    
    if event.keysym.lower() == 'b':
        pressed_l = False
        if pressed_b:
            sendCh.sendControl("buzzer", "whole")
            pressed_b = False
        else:
            pressed_b = True
        return
    if event.keysym.lower() == 'l':
        pressed_b = False
        if pressed_l:
            sendCh.sendControl("dot", "animation")
            pressed_l = False
        else:
            pressed_l = True
        return
    if event.keysym.lower() == 'v' and pressed_b:
        sendCh.sendControl('buzzer', 'violent')
    if event.keysym.lower() == 'n' and pressed_b:
        sendCh.sendControl('buzzer', 'nino')
    if  event.keysym.lower() == 'y' and pressed_b:
        sendCh.sendControl('buzzer', 'supermario')
    if event.keysym.lower() == 'c' and pressed_l:
        sendCh.sendControl("dot", "clear")
    
    pressed_l = False
    pressed_b = False
    
    
    if event.keysym == 'Escape' or event.keysym.lower() == 'q':
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
    
    if event.keysym.lower() == "a": 
        sendCh.turn_servo([0,1,0])
    if event.keysym.lower() == "d":
        sendCh.turn_servo([0,-1,0])
    if event.keysym.lower() == "s":
        sendCh.turn_servo([0,0, 1])
    if event.keysym.lower() == "w":
        sendCh.turn_servo([0,0,-1])
    if event.keysym.lower() == "o":
        sendCh.turn_servo([1,0,0])
    if event.keysym.lower() == "p":
        sendCh.turn_servo([-1,0,0])
    
    if event.keysym.lower() == 'm':
        sendCh.sendControl("measure")
    if event.keysym.lower() == 't':
        
        popup = Tk()
        entry = Entry(popup)
        entry.bind("<Return>", lambda e: method(popup, entry, sendCh))
        entry.pack()
        entry.focus_set()
        popup.mainloop()

    if event.keysym.lower() == 'u':
        if recCh.is_record:
            recCh.recorded_video.release()
        else:
            recCh.recorded_video = cv2.VideoWriter(f'../video/robot-video-cam-{time.time()}.avi', cv2.VideoWriter_fourcc(*'MJPG'), 30, (640,480))
        recCh.is_record = not recCh.is_record
        recCh.rec_label.configure(text = f'recording = {recCh.is_record}')


def method(popup, entry, sendCh):
    sendCh.sendControl("say", entry.get())
    popup.destroy()

def handle_key_release(event, root, sendCh, recCh):
    sendCh.turnCar(0)

#os.system('xset r off')

# Create the main window
with open('settings.json') as f:
    settings = json.load(f)

root = Tk()
root.title("W. H. I. L. E. T. R. U. E.")

sc = sendChanel(settings)
rc = receiveChanel(root, settings, sc)
root.bind("<Key>", lambda event: handle_key_press(event, root, sc, rc))

root.mainloop()