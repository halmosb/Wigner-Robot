import keyboard

while True:
    kin = keyboard.read_key()
    print(kin)
    if  kin == "space":
        print("Quit")
        break

#import cv2
#import numpy as np
#
#canvas = 240+ np.zeros((200,200,3), np.uint8)
#
#font = cv2.FONT_HERSHEY_SIMPLEX
#  
## org
#org = (50, 50)
#  
## fontScale
#fontScale = 1
#   
## Blue color in BGR
#color = (255, 0, 0)
#  
## Line thickness of 2 px
#thickness = 2
#
#cv2.putText(canvas, "press a key", org, font, fontScale, color, thickness, cv2.LINE_AA)
#cv2.imshow("keyboard input", canvas)
#
#while True:
#    kk = cv2.waitKey(0)
#    print(kk)
#    if kk &0xFF == ord('q'):
#        break