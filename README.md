# Description
The root directory contains a pipeline that takes a folder of videos and output a csv file containing keypoints image of every frame of every video. It requires a local OpenPose software installed. The instructions can be found here: https://github.com/CMU-Perceptual-Computing-Lab/openpose. The folder needs to have a folder named "input" and a folder named "output". 

## Run a sample video
```
python track.py --prototxt mobilenet_ssd/MobileNetSSD_deploy.prototxt --model mobilenet_ssd/MobileNetSSD_deploy.caffemodel --input videos/xy_walking_1.mp4 --output videos
```

## Pipeline 

### Step 1: get images from videos 
python opencv_subprocess.py --input D:/video --output C:/Users/sux/Desktop/openpose/input

If you use a virtual environment, you need to specify your python path:

```
python opencv_subprocess.py --input C:/Users/sux/Desktop/people-counting-opencv/videos --output C:/Users/sux/Desktop/openpose/input --python_path E:/Python_envs/capstone_env/Scripts/python.exe
```

### Step 2: get keypoints json files from images 
```
python openpose_subprocess.py --openpose_path C:/Users/sux/Desktop/openpose --input input --output output
```

### Step 3: combine the keypoints and standardize them to get the final feature csv
```
python get_feature_csv.py --json_path C:/Users/sux/Desktop/openpose/output --image_path C:/Users/sux/Desktop/openpose/input --output C:/Users/sux/Desktop/openpose_feature.csv
```

### Data Visualization
```
python visualize.py --csv openpose_feature.csv --folder_name xy_lookaround_1_0 --output video.avi
```

### All in one go
python all_in_one.py -cvi D:/video_test -op C:/Users/sux/Desktop/openpose -csv C:/Users/sux/Desktop

## Original work
https://www.pyimagesearch.com/2018/08/13/opencv-people-counter/

https://github.com/CMU-Perceptual-Computing-Lab/openpose