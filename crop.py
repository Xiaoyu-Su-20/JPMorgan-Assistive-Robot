import cv2
import numpy as np

cap = cv2.VideoCapture("videos/walking.mp4")

# (x, y, w, h) = cv2.boundingRect(c)
# cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 20)
# roi = frame[y:y+h, x:x+w]

while True:
    ret, frame = cap.read()
    # (height, width) = frame.shape[:2]
    a = np.random.randint(100, 200, size=2)
    sky = frame[0 : a[0], 0 : a[1]]
    cv2.imshow("Video", sky)

    if cv2.waitKey(1) == 27:
        exit(0)
