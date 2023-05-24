import cv2
import numpy as np

def stabilize_video(input_file, output_file):
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

    # Create a VideoWriter object to save the stabilized video
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    phase_prev = np.angle(np.fft.fft2(prev_frame))

    # Loop through the frames and stabilize the video
    while True:
        success, frame = video.read()
        if not success:
            break
        fftframe = np.fft.fft2(frame)

        # Calculate the phase difference between consecutive frames
        dphase = np.angle(fftframe) - phase_prev

        # Shift the current frame based on the phase difference
        shifted_frame = np.abs(np.fft.ifft2( np.abs(fftframe) * np.exp(1j * dphase) ) )

        # Convert the shifted frame to the BGR color space
        stabilized_frame = cv2.convertScaleAbs(shifted_frame)

        # Write the stabilized frame to the output video
        out.write(stabilized_frame)

        # Set the current frame as the previous frame for the next iteration
        prev_frame = frame.copy()

    # Release the video capture and writer objects
    video.release()
    out.release()

    print("Video stabilization complete.")


# Example usage
input_file = "input_video.avi"
output_file = "output_video.avi"
stabilize_video(input_file, output_file)
