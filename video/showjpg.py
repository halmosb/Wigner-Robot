import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys

# Methods to show a jpg image in python using opencv

if len(sys.argv)>1:
    method = int(sys.argv[1])
else:
    method = 0
if method>2 or method <0:
    print('Not a valid method (choose 0,1 or 2)')
    exit()

if method == 0:
    # read image 
    image = cv2.imread('image.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # another method to convert to rgb from the cv2 native bgr
    #b,g,r = cv2.split(frame)
    #frame_rgb = cv2.merge((r,g,b))
    plt.imshow(image)
    plt.title('Matplotlib method')
    plt.show()
elif method == 1:
    # read image 
    image = cv2.imread('image.jpg')
    # show the image, provide window name first
    cv2.imshow('image window', image)
    cv2.setWindowTitle('image window', 'cv2 imread method')
    # add wait key. window waits until user presses a key
    cv2.waitKey(0)
    # and finally destroy/close all open windows
    cv2.destroyAllWindows()
elif method == 2:
    # Read single frame avi
    imagename = 'image.jpg'
    # for webcam use
    # imagename = 0
    cap = cv2.VideoCapture(imagename)
    rval, frame = cap.read()
    cv2.namedWindow("Input")
    cv2.imshow("Input", frame)
    cv2.setWindowTitle('Input', 'cv2 videocapture method')

    cv2.waitKey(0)

