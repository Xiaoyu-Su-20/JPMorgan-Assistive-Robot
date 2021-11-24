import os
import argparse
import subprocess
import shutil

ap = argparse.ArgumentParser()
ap.add_argument("-py", "--python_path", default="python")
ap.add_argument("-cvi", "--opencv_input", required=True)
ap.add_argument("-op", "--openpose_path", required=True)
ap.add_argument("-csv", "--csv_path", required=True)
args = vars(ap.parse_args())
python_path = args["python_path"]
opencv_input = args["opencv_input"]
openpose_path = args["openpose_path"]
csv_path = args["csv_path"]


assert "input" in os.listdir(
    openpose_path
), f"there is no folder called 'input' in {openpose_path}"
assert "output" in os.listdir(
    openpose_path
), f"there is no folder called 'output' in {openpose_path}"

subprocess.run(
    [
        f"{python_path}",
        f"opencv_subprocess.py",
        f"--input={opencv_input}",
        f"--output={openpose_path}/input",
        f"--python_path={python_path}",
    ],
    text=True,
)

subprocess.run(
    [
        f"{python_path}",
        f"openpose_subprocess.py",
        f"--openpose_path={openpose_path}",
        f"--input=input",
        f"--output=output",
    ],
    text=True,
)

subprocess.run(
    [
        f"{python_path}",
        f"get_feature_csv.py",
        f"--json_path={openpose_path}/output",
        f"--image_path={openpose_path}/input",
        f"--output={csv_path}",
    ],
    text=True,
)

# remove everything and recreate folders
shutil.rmtree(f"{openpose_path}/input")
shutil.rmtree(f"{openpose_path}/output")
os.makedirs(f"{openpose_path}/input")
os.makedirs(f"{openpose_path}/output")
