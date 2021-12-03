import pandas as pd
import os


os.chdir("C:/users/sux/desktop")


def get_category_summary(df):
    cats = ["lookaround", "playwithphone", "phonecall", "wavehand"]
    dic = {cat: 0 for cat in cats}
    # get unique folder names
    ids = df["folder_name"].unique()
    # count lookaround, playwithphone, phonecall, wavehand
    for id in ids:
        for cat in cats:
            # if find the substring in
            if cat in id:
                dic[cat] += 1
                break
    print("total number of identifiable id is", sum(dic.values()))
    return dic


df = pd.DataFrame()

for file in os.listdir():
    if file.startswith("openpose") and file.endswith(".csv"):
        cur_df = pd.read_csv(file)
        print(cur_df["folder_name"].nunique())
        df = pd.concat([df, cur_df])
        print(file)

print(get_category_summary(df))

# num = df["folder_name"].nunique()
# df.to_csv(f"openpose_feature_{num}.csv", index=False)

