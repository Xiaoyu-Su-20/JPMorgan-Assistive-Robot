import subprocess
import os

openpose_path = "C:/Users/sux/Desktop/openpose"
os.chdir(openpose_path)

input_path = os.path.join(openpose_path, "input")
output_path = os.path.join(openpose_path, "output")

for img_folder in os.listdir(input_path):
    input_folder_path = os.path.join(input_path, img_folder)
    output_folder_path = os.path.join(output_path, f"keypoints_{img_folder}")
    print(img_folder)
    subprocess.run(
        [
            f"{openpose_path}\\bin\\OpenPoseDemo.exe",
            f"--image_dir={input_folder_path}",
            f"--write_json={output_folder_path}",
            "--disable_blending",
        ],
        text=True,
    )

