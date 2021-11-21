import pandas as pd
import matplotlib.pyplot as plt
from utils import color_map, line_set
import argparse
import cv2
import os

img_folder = "visualized_img"
my_dpi = 100


def video_from_img_folder(img_folder, video_path, fps, delete_img=True):
    images = [img for img in os.listdir(img_folder) if img.endswith(".png")]
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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-n",
        "--folder_name",
        required=True,
        help="the name of the original video, first column of the openpose_feature.csv",
    )
    ap.add_argument(
        "-c", "--csv", required=False, help="specify path to csv if using another csv",
    )
    ap.add_argument(
        "-o", "--output", required=True, help="path to output video",
    )
    ap.add_argument(
        "-f", "--fps", required=False, help="determine the video FPS",
    )
    args = vars(ap.parse_args())

    folder_name = args["folder_name"]
    video_path = args["output"]
    video_fps = 10 if args.get("fps") is None else int(args.get("fps"))
    csv = "openpose_feature.csv" if args.get("csv") is None else args.get("csv")
    # read data
    df = pd.read_csv(csv)
    df = df[df["folder_name"] == folder_name].reset_index()

    # rescale backwards
    for i in range(25):
        df[f"x{i}"] = (df[f"x{i}"] + 0.5) * 100
        df[f"y{i}"] = (df[f"y{i}"] + 0.5) * 200

    # generate pictures for all frame
    for ix, row in df.iterrows():
        plt.figure(figsize=(200 / my_dpi, 400 / my_dpi), dpi=my_dpi)
        img = plt.imread("utils/dark.jpg")
        null_set = set([])

        # plot circles
        for ix, color in color_map.items():
            point = row[f"x{ix}"], row[f"y{ix}"]
            # if the point is not identified, skip
            if point[0] == 0 and point[1] == 0:
                null_set.add(ix)
                continue
            plt.plot(*point, marker="o", color=color)

        # plot lines
        for t in line_set:
            # if either of the point is not identified, skip
            if t[0] in null_set or t[1] in null_set:
                continue
            p0 = row[f"x{t[0]}"], row[f"y{t[0]}"]
            p1 = row[f"x{t[1]}"], row[f"y{t[1]}"]
            plt.plot([p0[0], p1[0]], [p0[1], p1[1]], color=t[2])

        plt.imshow(img)
        plt.savefig(f"{img_folder}/frame{ix}.png")
        plt.close()

    video_from_img_folder(img_folder, video_path, video_fps, delete_img=True)
