import subprocess
import os

input_path = "C:/Users/sux/Desktop/people-counting-opencv/videos"
output_path = "C:/Users/sux/Desktop/openpose/input"


for file in os.listdir(input_path):
    if not file.endswith(".mp4"):
        continue
    subprocess.run(
        [
            "python",
            f"track.py",
            f"--prototxt=mobilenet_ssd/MobileNetSSD_deploy.prototxt",
            "--model=mobilenet_ssd/MobileNetSSD_deploy.caffemodel",
            f"--input=videos/{file}",
            f"--output={output_path}",
        ],
        text=True,
    )

