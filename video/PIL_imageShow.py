from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import os

def showImage(imlabel, image, L) :
    newsize = [int(n) for n in np.array(image.size)/np.max(np.array(image.size)/500)]
    image = image.resize(newsize)
    photo = ImageTk.PhotoImage(image)

    imlabel.configure(image=photo)
    imlabel.image = photo


# Create the main window
root = Tk()
root.title("Image Viewer")

# Create a label to display the image
imlabel = Label(root)
imlabel.pack()

textlabel = Label(root, text="show a video")
textlabel.pack()

# Load the image using PIL
path = '/home/jakovac/Work/WignerAI/Robot/Wigner-Robot/video/Images/'
images = dir_list = os.listdir(path)
imcnt = 0
showImage(imlabel, Image.open(path + images[imcnt]), L=500)

# Define a function to handle the key press event
def handle_key_press(event):
    global imcnt
    # Do something when the key is pressed
    print("Key pressed:", event.keysym)
    if event.keysym == 'Escape' or event.keysym == 'q':
        root.destroy()
    if event.keysym == 'Down':
        imcnt = (imcnt-1)%len(images)
        showImage(imlabel, Image.open(path + images[imcnt]), L=500)

# Bind the key press event to the function
root.bind("<Key>", handle_key_press)

# Run the main event loop
root.mainloop()