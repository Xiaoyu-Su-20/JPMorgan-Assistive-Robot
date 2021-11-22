import pandas as pd
import numpy as np

path = "openpose_feature_66.csv"

df = pd.read_csv(path)

num = df["folder_name"].nunique()

df = df.drop(
    [f"c{i}" for i in range(25)] + ["folder_name", "frame_num", "width", "height"],
    axis=1,
)
# normalize

print(max(df.max()))
