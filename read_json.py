import json
import os
import re
import pandas as pd


def get_feature_matrix(folder_path):
    """
    Args:
        folder_path (str): the path to the folder that contains JSON file 
        for each frame.

    Returns:
        lst: nested list representing feature matrix
    """
    feature = []
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
            feature.append((keypoints, frame_num))

    feature = sorted(feature, key=lambda x: x[1])
    feature = [[i[1]] + i[0] for i in feature]

    return feature


# for all keypoints JSON folder in the output folder, get the feature matrix
path = "C:\\Users\sux\Desktop\openpose\output"
for folder in os.listdir(path):
    if folder.startswith("keypoints"):
        full_folder_path = os.path.join(path, folder)
        features = get_feature_matrix(full_folder_path)
    print("done")


# print(features)

