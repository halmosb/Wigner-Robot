import cv2
import numpy as np

def stabilize_video(input_file, output_file):
    # Open the video file
    video = cv2.VideoCapture(input_file)

    # Get the first frame
    success, prev_frame = video.read()
    if not success:
        print("Error opening video file.")
        return

    # Get the video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a VideoWriter object to save the stabilized video
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Parameters for Lucas-Kanade optical flow
    lk_params = dict(winSize=(10, 10), maxLevel=4, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Convert the first frame to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Initialize the previous good points
    prev_points = cv2.goodFeaturesToTrack(prev_gray, maxCorners=20, qualityLevel=0.01, minDistance=15)

    # Loop through the frames and stabilize the video
    while True:
        success, frame = video.read()
        if not success:
            break

        # Convert the current frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate the optical flow
        current_points, status, error = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_points, None, **lk_params)

        # Select only the good points
        good_new = current_points[status == 1]
        good_prev = prev_points[status == 1]

        # Calculate the transformation matrix using RANSAC
        transform, _ = cv2.estimateAffinePartial2D(good_prev, good_new, method=cv2.RANSAC)

        # Apply the transformation matrix to the current frame
        stabilized_frame = cv2.warpAffine(frame, transform, (width, height))

        # Write the stabilized frame to the output video
        out.write(stabilized_frame)

        # Set the current frame as the previous frame for the next iteration
        prev_gray = gray.copy()
        prev_points = good_new.reshape(-1, 1, 2)

    # Release the video capture and writer objects
    video.release()
    out.release()

    print("Video stabilization complete.")


# Example usage
input_file = "input_video.avi"
output_file = "output_video.avi"
m0 = "m0.avi"
stabilize_video(input_file, m0)
for i in range(10):
    stabilize_video(f'm{i}.avi', f'm{i+1}.avi')
    print(i)
stabilize_video('m10.avi', output_file)

