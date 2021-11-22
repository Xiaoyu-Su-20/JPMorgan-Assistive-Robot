color_map = {
    0: "#cb0072",
    1: "#c20d00",
    2: "#9e3500",
    3: "#a67000",
    4: "#caca00",
    5: "#89ce00",
    6: "#33a200",
    7: "#009600",
    8: "#c00401",
    9: "#00bf40",
    10: "#00bf81",
    12: "#008cd2",
    13: "#0046d3",
}
line_set = set(
    [
        (0, 1, "#990033"),
        (1, 2, "#993300"),
        (2, 3, "#996600"),
        (3, 4, "#999900"),
        (1, 5, "#669900"),
        (5, 6, "#339900"),
        (6, 7, "#009900"),
        (1, 8, "#990000"),
        (8, 9, "#009933"),
        (9, 10, "#009966"),
        (8, 12, "#006699"),
        (12, 13, "#003399"),
    ]
)

openpose_to_ntu_map = {
    1: 21,
    2: 9,
    3: 10,
    4: 11,
    5: 5,
    6: 6,
    7: 7,
    8: 1,
    9: 17,
    10: 18,
    11: 19,
    22: 20,
    23: 20,
    12: 13,
    13: 14,
    14: 15,
    19: 16,
    20: 16,
    0: 4,
}

import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os

img_folder = "visualized_img"
folder_name = "whisperInEar_386"

df = pd.read_csv("ntu2openpose_vis.csv")
df = df[df["folder_name"] == folder_name].reset_index()
# rescale backwards
for i in range(25):
    df[f"x{i}"] = (df[f"x{i}"] + 0.5) * 100
    df[f"y{i}"] = (df[f"y{i}"] + 0.5) * 200

for ix, row in df.iterrows():
    img = plt.imread("utils/dark.jpg")
    null_set = set([])
    for i, color in color_map.items():
        real_i = openpose_to_ntu_map[i] - 1
        point = row[f"x{real_i}"], row[f"y{real_i}"]
        # if the point is not identified, skip
        if point[0] == 0 and point[1] == 0:
            null_set.add(i)
            continue
        plt.plot(*point, marker="o", color=color)

    # plot lines
    for t in line_set:
        # if either of the point is not identified, skip
        if t[0] in null_set or t[1] in null_set:
            continue
        real_t = (openpose_to_ntu_map[t[0]] - 1, openpose_to_ntu_map[t[1]] - 1, t[2])
        p0 = row[f"x{real_t[0]}"], row[f"y{real_t[0]}"]
        p1 = row[f"x{real_t[1]}"], row[f"y{real_t[1]}"]
        plt.plot([p0[0], p1[0]], [p0[1], p1[1]], color=real_t[2])

    plt.imshow(img)
    plt.savefig(f"{img_folder}/{ix}.png")
    plt.close()


def video_from_img_folder(img_folder, video_path, fps, delete_img=True):
    images = [img for img in os.listdir(img_folder) if img.endswith(".png")]
    images.sort(key=lambda x: int(os.path.splitext(x)[0]))
    print(images)
    frame = cv2.imread(os.path.join(img_folder, images[0]))
    height, width, _ = frame.shape

    video = cv2.VideoWriter(video_path, 0, fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(img_folder, image)))

    if delete_img:
        for file in os.listdir(img_folder):
            os.remove(os.path.join(img_folder, file))

    cv2.destroyAllWindows()
    video.release()


video_from_img_folder(img_folder, f"{folder_name}.avi", 10, delete_img=True)
