import cv2

# Open the original video file
original_video = cv2.VideoCapture('input_video.avi')  # Replace 'path_to_original_video.mp4' with the actual path to your original video file

# Get the original video's properties
fps = original_video.get(cv2.CAP_PROP_FPS)
width = int(original_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(original_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

factor = 10

# Define the desired width and height for the resized video
desired_width = width//factor
desired_height = height//factor

# Create a VideoWriter object to write the resized frames to a new video file
resized_video = cv2.VideoWriter('resized_video.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (desired_width, desired_height))

# Read frames from the original video, resize each frame, and write it to the resized video
while True:
    ret, frame = original_video.read()
    if not ret:
        break
    
    # Resize the frame
    resized_frame = cv2.resize(frame, (desired_width, desired_height))
    
    # Write the resized frame to the resized video file
    resized_video.write(resized_frame)

# Release the video capture and video writer objects
original_video.release()
resized_video.release()

# Display a message indicating the process is complete
print("Resized video created successfully!")
