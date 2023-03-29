#import the opencv library
import cv2
import time
import matplotlib.pyplot as plt

fps_frame= 50
t0 = time.time()
nframe = 0  # the received frames
fps =0

# define a video capture object
vid = cv2.VideoCapture(0)
if not vid.isOpened():
    print('camera could not be open (locked by other application...?)')
    exit(-1)

vid.set(cv2.CAP_PROP_FRAME_WIDTH, 128)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 72)

while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
  
    # convert the frame into jpg
    success, jpgimage = cv2.imencode('.jpg', frame)

    # convert back to pixel array
    frame1 = cv2.imdecode(jpgimage, cv2.IMREAD_UNCHANGED)
#    frame1=frame

    nframe +=1
    fps_rate = 1/nframe + 1/fps_frame
    t1 = time.time()
    if t1!=t0 :
        fps = fps_rate/(t1-t0) + (1-fps_rate)*fps
    fpsn = fps
    t0=t1

    # Display the resulting frame
    cv2.imshow('frame', frame1)
    cv2.setWindowTitle('frame', f'video FPS={fpsn:.1f}')

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
