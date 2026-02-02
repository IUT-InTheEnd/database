import pandas as pd

df = pd.read_csv("./dataset/raw_tracks.csv")

df["track_file"] = "https://files.freemusicarchive.org/storage-freemusicarchive-org/" + df["track_file"]

df["track_image_file"] = "https://files.freemusicarchive.org/storage-freemusicarchive-org/" + df["track_image_file"].str[34:]

df.to_csv("./dataset/link_fix_raw_tracks.csv",index=False)