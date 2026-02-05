import pandas as pd
import os

# fix links raw tracks
if os.path.exists("./dataset/link_fix_raw_tracks.csv") == False:
    df1 = pd.read_csv("./dataset/raw_tracks.csv", dtype=str)

    df1.loc[df1["track_file"].notna(), "track_file"] = (
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/"
        + df1.loc[df1["track_file"].notna(), "track_file"]
    )
    df1.loc[df1["track_file"].isna(), "track_file"] = None

    df1.loc[df1["track_image_file"].notna(), "track_image_file"] = (
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/"
        + df1.loc[df1["track_image_file"].notna(), "track_image_file"].str[34:]
    )
    df1.loc[df1["track_image_file"].isna(), "track_image_file"] = None
    
    df1.to_csv("./dataset/link_fix_raw_tracks.csv",index=False)

# fix links raw artists
if os.path.exists("./dataset/link_fix_raw_artists.csv") == False:
    df2 = pd.read_csv("./dataset/raw_artists.csv", dtype=str)

    df2.loc[df2["artist_image_file"].notna(), "artist_image_file"] = (
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/"
        + df2.loc[df2["artist_image_file"].notna(), "artist_image_file"].str[34:]
    )
    df2.loc[df2["artist_image_file"].isna(), "artist_image_file"] = None

    df2.to_csv("./dataset/link_fix_raw_artists.csv",index=False)

# fix links raw albums
if os.path.exists("./dataset/link_fix_raw_albums.csv") == False:
    df3 = pd.read_csv("./dataset/raw_albums.csv", dtype=str)
    
    df3.loc[df3["album_image_file"].notna(), "album_image_file"] = (
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/"
        + df3.loc[df3["album_image_file"].notna(), "album_image_file"].str[34:]
    )
    df3.loc[df3["album_image_file"].isna(), "album_image_file"] = None
    
    df3.to_csv("./dataset/link_fix_raw_albums.csv",index=False)
