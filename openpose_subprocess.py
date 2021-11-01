import subprocess
import os

openpose_path = "C:\\Users\sux\Desktop\openpose"
os.chdir(openpose_path)

input_path = os.path.join(openpose_path, "input")
output_path = os.path.join(openpose_path, "output")

for img_folder in os.listdir(input_path):
    input_path = os.path.join("input", img_folder)
    output_path = os.path.join("output", img_folder)

    subprocess.run(
        [
            "bin\OpenPoseDemo.exe",
            f"--image_dir={input_path}",
            f"--write_images={output_path}",
            "--disable_blending",
            "--display=0",
        ],
        text=True,
    )

