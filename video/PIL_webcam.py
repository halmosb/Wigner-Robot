from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from threading import Thread
import time
import cv2

class ImageHandler() :
    def __init__(self, root, L=500, fps=50) :
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            print('camera could not be open (locked by other application...?)')
            exit(-1)

        self.root=root
        self.imlabel = Label(self.root)
        self.imlabel.pack()

        self.L= L
        self.dt = 1.0/fps
        self.run = True
        self.thread = Thread(target=self.updateImage)
        self.thread.start()

        self.root.bind("<Key>", self.handle_key_press)
        self.textlabel = Label(self.root, text=f'webcam')
        self.textlabel.pack(side='left')

    def handle_key_press(self, event):
        if event.keysym == 'Escape' or event.keysym == 'q':
            self.run = False
            self.thread.join()
            self.root.destroy()
        if event.keysym == 'Down':
            self.speed = self.speed/self.speedupfactor
            if self.speed <1 :
                self.speed=0
            self.textlabel.configure(text = f'webcam')
        if event.keysym == 'Up':
            if self.speed==0:
                self.speed=1
            else:
                self.speed = np.min([self.speed*self.speedupfactor,self.maxspeed])
            self.textlabel.configure(text = f'webcam')

 
    def updateImage(self) :
        while self.run:
            ret, frame = self.vid.read()
            if not ret:
                break
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.showImage(image)
            #time.sleep(self.dt)
        self.vid.release()

    def showImage(self,  image) :
        newsize = [int(n) for n in np.array(image.size)/np.max(np.array(image.size)/self.L)]
        image = image.resize(newsize)
        if self.run:
            photo = ImageTk.PhotoImage(image)

            self.imlabel.configure(image=photo)
            self.imlabel.image = photo


# Create the main window
root = Tk()
root.title("Image Viewer")

imH = ImageHandler(root)

root.mainloop()