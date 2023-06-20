import cv2
import numpy as np

video_path = 'after_hardware_ststabilization.avi'
output_path = 'stabilized.avi'
output_size = (640, 480)

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, fps, output_size)

prev_frame = None

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_frame is None:
        prev_frame = gray
        continue

    # Calculate optical flow using Lucas-Kanade method
    lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    prev_pts = cv2.goodFeaturesToTrack(prev_frame, mask=None, maxCorners=200, qualityLevel=0.01, minDistance=10, blockSize=3)
    next_pts, status, _ = cv2.calcOpticalFlowPyrLK(prev_frame, gray, prev_pts, None, **lk_params)

    # Filter valid points and estimate affine transformation
    valid_prev_pts = prev_pts[status == 1]
    valid_next_pts = next_pts[status == 1]
    transform = cv2.estimateAffinePartial2D(valid_prev_pts, valid_next_pts)[0]

    if transform is not None:
        dx = transform[0, 2]
        dy = transform[1, 2]
        theta = np.arctan2(transform[1, 0], transform[0, 0]) * 180.0 / np.pi
        scale = transform[0, 0] / np.cos(theta * np.pi / 180.0)

        # Apply the estimated transformation to stabilize the frame
        M = np.float32([[scale, 0, dx], [0, scale, dy]])
        stabilized_frame = cv2.warpAffine(frame, M, output_size)

        out.write(stabilized_frame)

    prev_frame = gray

cap.release()
out.release()
cv2.destroyAllWindows()