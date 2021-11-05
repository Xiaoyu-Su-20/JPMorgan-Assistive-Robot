import subprocess
import os

openpose_path = "C:\\Users\sux\Desktop\openpose"

input_path = os.path.join(openpose_path, "input")
output_path = os.path.join(openpose_path, "output")

for img_folder in os.listdir(input_path):
    input_path = os.path.join("input", img_folder)
    output_path = os.path.join("output", f"keypoints_{img_folder}")

    subprocess.run(
        [
            "bin\OpenPoseDemo.exe",
            f"--image_dir={input_path}",
            f"--write_json={output_path}",
            "--disable_blending",
        ],
        text=True,
    )

