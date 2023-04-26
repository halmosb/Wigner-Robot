from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from threading import Thread
import time
import cv2
from UDPwebcam import UDPwebcam_receiver

class ImageHandler() :
    def __init__(self, root, receiver, L=500, fps=50) :
        self.receiver = receiver
        self.root=root
        self.imlabel = Label(self.root)
        self.imlabel.pack()

        self.L= L
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
            self.receiver.stop()
            self.root.destroy()
        if event.keysym == 'Down':
            self.textlabel.configure(text = f'Down')
        if event.keysym == 'Up':
            self.textlabel.configure(text = f'Up')

 
    def updateImage(self) :
        while self.run:
            frame = self.receiver.queue.get()
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.showImage(image)

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

receiver = UDPwebcam_receiver()
receiver.start()

imH = ImageHandler(root, receiver)

root.mainloop()