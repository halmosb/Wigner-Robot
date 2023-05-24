import cv2
import numpy as np
import copy

# Define color thresholds for object tracking
threshold = 0.9
lower_color = np.array([int(338*(1-threshold)), int(12.5*(1-threshold)), int(53*(1-threshold))])
upper_color = np.array([int(338*(1+threshold)), int(12.5*(1+threshold)), int(53*(1+threshold))])


# Define Canny edge detection thresholds
threshold1 = 50
threshold2 = 150

# Read the video file
video = cv2.VideoCapture('input_video6.avi')

while True:
    ret, frame = video.read()
    if not ret:
        break

    edges = cv2.Canny(frame, threshold1, threshold2)
    # Object Tracking
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Canny Edge Detection
    

    # Display Object Tracking and Edges
    cv2.imshow('Object Tracking', frame)
    cv2.imshow('Edges', edges)
    
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture and close the windows
video.release()
cv2.destroyAllWindows()
