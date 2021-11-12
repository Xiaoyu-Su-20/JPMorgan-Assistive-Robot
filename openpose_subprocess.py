import subprocess
import os
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-op", "--openpose_path", required=True, help="path to the openpose folder"
    )
    ap.add_argument(
        "-i", "--input", required=True, help="relative path to the input folder"
    )
    ap.add_argument(
        "-o", "--output", required=True, help="relative path to the output folder"
    )
    args = vars(ap.parse_args())

    openpose_path = args["openpose_path"]
    input_path = os.path.join(openpose_path, args["input"])
    output_path = os.path.join(openpose_path, args["output"])
    os.chdir(openpose_path)

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
                "--display=0",
                "--render_pose=0",
            ],
            text=True,
        )

