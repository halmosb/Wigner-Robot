import cv2
import numpy as np

kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

# Apply the sharpening effect using the filter2D() function


def shi_tomasi(image):
    # Load the image
    # = cv2.imread(f'../../Video_dir/frame{frame}.jpg')  # Replace 'path_to_your_image.jpg' with the actual path to your image file
    #image = cv2.blur(image, (5, 5))
    #image = cv2.filter2D(image, -1, kernel)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
    # Parameters for corner detection
    max_corners = 15  # Maximum number of corners to detect
    quality_level = 0.1  # Minimum accepted quality of corners
    min_distance = 10  # Minimum distance between detected corners

    # Perform corner detection using Good Features to Track
    corners = cv2.goodFeaturesToTrack(gray, max_corners, quality_level, min_distance)

    # Convert the corners to integer coordinates
    corners = np.int0(corners)

    # Draw circles around the detected corners
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
    return image


video = cv2.VideoCapture("after_hardware_ststabilization.avi")

fps = video.get(cv2.CAP_PROP_FPS)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# Create a VideoWriter object to save the stabilized video
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("good_features_to_track.avi", fourcc, fps, (width, height))

while True:
    success, frame = video.read()
    if not success:
        break
    
    out.write(shi_tomasi(frame))

video.release()
out.release()