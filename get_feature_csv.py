import json
import os
import re
import pandas as pd
import cv2
from functools import reduce


def get_feature_matrix(img_path, folder_path):
    """
    Args:
        folder_path (str): the path to the folder that contains JSON file 
        for each frame.

    Returns:
        feature_lst: nested list representing feature matrix
    """
    feature_lst = []
    keypoints_folder_name = os.path.basename(folder_path)
    img_folder_name = re.findall("(?<=keypoints_)(.*)", keypoints_folder_name)[0]

    for file in os.listdir(folder_path):
        # get the frame number
        frame_num = int(re.findall("\d+", file)[0])
        with open(os.path.join(folder_path, file)) as f:
            data = json.load(f)["people"]
            # sometimes there can be multiple identified skeleton in a single frame
            # only one is the one we want
            # we'll choose the one with the least number of zeros across keypoint values
            min_zeros_idx = 0
            if len(data) > 1:
                min_zeros = float("inf")
                for idx, person in enumerate(data):
                    cur_zeros = person["pose_keypoints_2d"].count(0)
                    if cur_zeros < min_zeros:
                        min_zeros = cur_zeros
                        min_zeros_idx = idx

            keypoints = data[min_zeros_idx]["pose_keypoints_2d"]

        # read the corresponding image and get the width and height
        im = cv2.imread(f"{img_path}/{img_folder_name}/frame{frame_num}.jpg")
        height, width, _ = im.shape

        # append all attributes to the feature_lst
        feature_lst.append(
            {
                "frame_num": frame_num,
                "keypoints": keypoints,
                "height_width": [height, width],
            }
        )

    feature_lst = sorted(feature_lst, key=lambda x: x["frame_num"])
    feature_lst = [
        [img_folder_name] + [i["frame_num"]] + i["height_width"] + i["keypoints"]
        for i in feature_lst
    ]

    return feature_lst


# for all keypoints JSON folder in the output folder, get the feature matrix
path = "C:\\Users\sux\Desktop\openpose\output"
img_path = "C:\\Users\sux\Desktop\openpose\input"

all_data = []
for folder in os.listdir(path):
    if folder.startswith("keypoints"):
        full_folder_path = os.path.join(path, folder)
        features = get_feature_matrix(img_path, full_folder_path)
        all_data.extend(features)
df = pd.DataFrame(all_data)
coordinates_cols = [[f"x{i}", f"y{i}", f"c{i}"] for i in range(25)]
coordinates_cols = reduce(lambda x, y: x + y, coordinates_cols)
cols = ["folder_name", "frame_num", "height", "width"] + coordinates_cols
df.columns = cols

# normalize the data by scaling the width and height to 1, then subtract every coordinates
# by the coordinates of the centorid
# basically, we want the coordinates of the keypoints when centroid is (0,0) and
# both the width and the height are 1
for i in range(25):
    df[f"x{i}"] = df[f"x{i}"] / df["width"] - 0.5
    df[f"y{i}"] = df[f"y{i}"] / df["height"] - 0.5

df.to_csv("C:/Users/sux/desktop/data.csv", index=False)


# print(features)

