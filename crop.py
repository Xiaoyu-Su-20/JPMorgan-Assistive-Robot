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

# playground --------------------------------------------------
def get_reshaped_rects(lst, max_height, max_width):
    new_lst = []
    for x1, y1, x2, y2 in lst:
        height = y2 - y1
        width = x2 - x1
        h_add_one, w_add_one = 0, 0
        if height % 2 != 0:
            h_add_one = 1
        if width % 2 != 0:
            w_add_one = 1
        y2 = y2 + (max_height - height) // 2 + h_add_one
        y1 = y1 - (max_height - height) // 2
        x2 = x2 + (max_width - width) // 2 + w_add_one
        x1 = x1 - (max_width - width) // 2
        new_lst.append((x1, y1, x2, y2))
    return new_lst
