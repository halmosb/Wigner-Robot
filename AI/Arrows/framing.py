import cv2 as cv3
for iv in ("r1", "l1", "u1", "d1"):
    #xiv = "u0"
    video = cv3.VideoCapture(f"Learning Data/{iv}.avi")

    i = 0
    while True:
        succes, frame = video.read()
        if not succes:
            print(i)
            break
        cv3.imwrite(f"Learning Data/test/{iv}-{i:04}.jpg", frame)
        i+=1
