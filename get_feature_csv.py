import json
import os
import re
import pandas as pd
import cv2
from functools import reduce
import argparse
import numpy as np


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
            if len(data) == 0:
                continue
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
        try:
            height, width, _ = im.shape
        except:
            print(f"{img_path}/{img_folder_name}/frame{frame_num}.jpg")
            raise Exception

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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-j",
        "--json_path",
        required=True,
        help="path to the folder containing JSON folders",
    )
    ap.add_argument(
        "-i",
        "--image_path",
        required=True,
        help="path to the folder containing image folders",
    )
    ap.add_argument("-o", "--output", required=True, help="output path to the csv file")
    args = vars(ap.parse_args())

    # for all keypoints JSON folder in the output folder, get the feature matrix
    json_path = args["json_path"]
    img_path = args["image_path"]

    all_data = []
    for folder in os.listdir(json_path):
        if folder.startswith("keypoints"):
            full_folder_path = os.path.join(json_path, folder)
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
        # if the pixel values exceed the image boundary, ignore them
        df[f"x{i}"] = np.where(df[f"x{i}"] > df["width"], 0, df[f"x{i}"])
        df[f"x{i}"] = np.where(df[f"y{i}"] > df["height"], 0, df[f"x{i}"])
        df[f"y{i}"] = np.where(df[f"x{i}"] > df["width"], 0, df[f"y{i}"])
        df[f"y{i}"] = np.where(df[f"y{i}"] > df["height"], 0, df[f"y{i}"])
        # normalize
        df[f"x{i}"] = df[f"x{i}"] / df["width"] - 0.5
        df[f"y{i}"] = df[f"y{i}"] / df["height"] - 0.5
    num = df["folder_name"].nunique()
    df.to_csv(f"{args['output']}/openpose_feature_{num}.csv", index=False)

