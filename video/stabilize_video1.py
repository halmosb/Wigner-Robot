import cv2
import numpy as np
import os

def strInt(n, ndigits = 3) :
    mask = ndigits*'0'
    ss = str(n)
    return mask[:ndigits-len(ss)] + ss

def stabilize_video(input_file, output_directory):
    if not os.path.isdir(output_directory):
        print(f'creating {output_directory}')
        os.mkdir(output_directory)

    # Open the video file
    video = cv2.VideoCapture(input_file)

    # Check if the video file was opened successfully
    if not video.isOpened():
        print("Error opening video file.")
        return

    # Get the first frame
    success, prev_frame = video.read()
    if not success:
        print("Error reading the first frame.")
        return

    # Get the video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frameNumber = 0

    # Loop through the frames and stabilize the video
    while True:
        success, frame = video.read()
        if not success:
            break
        
        cv2.imwrite(f"{output_directory}/frame{strInt(frameNumber)}.jpg", frame) 
        frameNumber += 1


    # Release the video capture and writer objects
    video.release()

    print("Writig frames is complete.")


# Example usage
input_file = "input_video.avi"
output_dir = "Video_dir"
stabilize_video(input_file, output_dir)
