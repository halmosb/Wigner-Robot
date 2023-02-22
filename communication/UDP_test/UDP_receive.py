import socket
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import time



addr = ("127.0.0.1", 65534)
buf = 512
code = b'start'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(addr)
chunks = []
num_chunks = -1
while True:
    chunk, _ =s.recvfrom(buf)
    if chunk.startswith(code):
        headerlist = str(chunk).split(':')
        try:
            shape=[int(n) for n in headerlist[1][1:-1].split(',')]
            imgsize = shape[0]*shape[1]*shape[2]
        except:
            continue
        num_chunks = imgsize/buf
        chunks = []
        print('Got start')
    else:
        chunks.append(chunk)
    
    if len(chunks) == num_chunks:
        print("Complete image")
        byte_frame = b''.join(chunks)
        frame = np.frombuffer(
           byte_frame, dtype=np.uint8).reshape(shape[0], shape[1], shape[2])
        cv.imshow('recv', frame)
    
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    



    """
while True:
    head, _ = s.recvfrom(buf)
    if head.startswith(code):
        headerlist = str(head).split(':')
        shape=[int(n) for n in headerlist[1][1:-1].split(',')]
        imgsize = shape[0]*shape[1]*shape[2]
        num_chunks = imgsize/buf

        
        chunks = []
        success=True
        while len(chunks) < num_chunks:
            chunk, _ = s.recvfrom(buf)
            if chunk.startswith(code):
                success=False
                break 
            chunks.append(chunk)
        if success :
            byte_frame = b''.join(chunks)
            frame = np.frombuffer(
                byte_frame, dtype=np.uint8).reshape(shape[0], shape[1], shape[2])
            cv.imshow('recv', frame)
        else :
            print('Package loss')

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
"""

s.close()

"""
    start = False
    while len(chunks) < num_of_chunks:
        chunk, _ = s.recvfrom(buf)
        if start:
            chunks.append(chunk)
        elif chunk.startswith(code):
            start = True

    byte_frame = b''.join(chunks)

    frame = np.frombuffer(
        byte_frame, dtype=np.uint8).reshape(height, width, 3)

    cv.imshow('recv', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


while True:
    chunk, _ = s.recvfrom(buf)
    print(chunk)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

s.close()
"""