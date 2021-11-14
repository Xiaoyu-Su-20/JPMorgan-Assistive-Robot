import subprocess
import os
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to the videos")
    ap.add_argument("-o", "--output", required=True, help="path to the output folder")
    ap.add_argument("-py", "--python_path", default="python", help="path to python")
    args = vars(ap.parse_args())

    input_path = args["input"]
    output_path = args["output"]
    python_path = args["python_path"]

    for file in os.listdir(input_path):
        if not file.endswith(".mp4"):
            continue
        subprocess.run(
            [
                f"{python_path}",
                f"track.py",
                f"--prototxt=mobilenet_ssd/MobileNetSSD_deploy.prototxt",
                "--model=mobilenet_ssd/MobileNetSSD_deploy.caffemodel",
                f"--input=videos/{file}",
                f"--output={output_path}",
            ],
            text=True,
        )

