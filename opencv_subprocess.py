import subprocess
import os

input_path = "C:/Users/sux/Desktop/people-counting-opencv/videos"

for file in os.listdir(input_path):
    if not file.endswith(".mp4"):
        continue
    print(os.getcwd())
    subprocess.run(
        [
            "python",
            f"track.py",
            f"--prototxt=mobilenet_ssd/MobileNetSSD_deploy.prototxt",
            "--model=mobilenet_ssd/MobileNetSSD_deploy.caffemodel",
            f"--input=videos/{file}",
        ],
        text=True,
    )

