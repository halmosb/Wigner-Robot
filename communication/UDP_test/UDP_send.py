import socket
import numpy as np
import cv2 as cv
import time


addr = ("127.0.0.1", 65534)

buf = 512
width = 640
height = 480
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)
metadata = f'start:{height,width,3}:'
header = (metadata + (buf - len(metadata)) * 'a').encode('utf-8')

"""
cv.imshow('image',img)
while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
"""

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        s.sendto(header, addr)
        data = frame.tobytes()
        for i in range(0, len(data), buf):
            s.sendto(data[i:i+buf], addr)
        #print('sent frame')
        # cv.imshow('send', frame)
        # if cv.waitKey(1) & 0xFF == ord('q'):
            # break
    else:
        break
s.close()