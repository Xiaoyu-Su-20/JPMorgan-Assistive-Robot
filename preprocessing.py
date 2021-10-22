import cv2
import numpy as np
from PIL import Image


# write videos frame skipped; compute centroids; compare to key pointsss


def video_nth_frame_2(video_path, n):
    cap = cv2.VideoCapture(video_path)

    frame_lst = []

    count = 0
    while True:
        success, frame = cap.read()

        if not success:
            break

        if count % n == 0:
            frame_lst.append(frame)

        count += 1

    return frame_lst


frame_lst = video_nth_frame_2("videos/example_01.mp4", 3)
print(len(frame_lst))

