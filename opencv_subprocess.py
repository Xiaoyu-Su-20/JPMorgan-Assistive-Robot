import subprocess
import os
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="path to the vidoes")
    ap.add_argument("-o", "--output", required=True, help="path to the output folder")
    args = vars(ap.parse_args())

    input_path = args["input"]
    output_path = args["output"]

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

