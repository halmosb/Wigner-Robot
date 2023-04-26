from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import numpy as np
from threading import Thread
import time

class ImageHandler() :
    def __init__(self, root, x =  None, L=500, v = 10,radius = 50, bgcolor = (211,211,211), fgcolor=(255,69,0), fps=25) :
        self.imlabel = Label(root)
        self.imlabel.pack()

        self.L= L
        if x is None:
            self.x = np.random.randint(self.L,size=(2,))
        else:
            self.x = x
        self.speed = v
        self.speedupfactor = 1.05
        self.maxspeed = 50
        self.radius = radius
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.dt = 1.0/fps
        self.run = True
        self.thread = Thread(target=self.updateImage)
        self.thread.start()
        self.showImage(self.createImage())

        root.bind("<Key>", self.handle_key_press)
        self.textlabel = Label(root, text=f'speed= {self.speed}')
        self.textlabel.pack(side='left')

    def handle_key_press(self, event):
        print(event.keysym)
        if event.keysym == 'Escape' or event.keysym == 'q':
            self.run = False
            self.thread.join()
            root.destroy()
        if event.keysym == 'Down':
            self.speed = self.speed/self.speedupfactor
            if self.speed <1 :
                self.speed=0
            self.textlabel.configure(text = f'speed= {self.speed:.1f}')
        if event.keysym == 'Up':
            if self.speed==0:
                self.speed=1
            else:
                self.speed = np.min([self.speed*self.speedupfactor,self.maxspeed])
            self.textlabel.configure(text = f'speed= {self.speed:.1f}')

 
    def updateImage(self) :
        while self.run:
            nn = np.random.random(size=(2,))-0.5
            self.x = np.array([ int(xi)%self.L for xi in self.x + self.speed*nn/np.linalg.norm(nn)])
            self.showImage(self.createImage())
            time.sleep(self.dt)

    def createImage(self) :
        width = self.L
        height = self.L
        image = Image.new("RGB", (width, height), self.bgcolor)
        draw = ImageDraw.Draw(image)
        draw.ellipse((self.x[0] - self.radius, self.x[1] - self.radius, self.x[0] + self.radius, self.x[1] + self.radius), fill=self.fgcolor)
        return image

    def showImage(self,  image) :
        newsize = [int(n) for n in np.array(image.size)/np.max(np.array(image.size)/self.L)]
        image = image.resize(newsize)
        photo = ImageTk.PhotoImage(image)

        self.imlabel.configure(image=photo)
        self.imlabel.image = photo


# Create the main window
root = Tk()
root.title("Image Viewer")

imH = ImageHandler(root)

root.mainloop()