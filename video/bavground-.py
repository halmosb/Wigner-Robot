import cv2

# Create a background subtractor object
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Open a video file or capture video from a camera
video = cv2.VideoCapture('input_video4.avi')  # Replace 'path_to_your_video.mp4' with the actual path to your video file

while True:
    ret, frame = video.read()
    if not ret:
        break
    
    # Apply background subtraction
    fg_mask = bg_subtractor.apply(frame)
    
    # Display the foreground mask
    cv2.imshow('Foreground Mask', fg_mask)
    
    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break

# Release the video capture and close windows
video.release()
cv2.destroyAllWindows()