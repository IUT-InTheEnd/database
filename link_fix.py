from __future__ import annotations

from pathlib import Path

import pandas as pd


DATASET_DIR = Path("dataset")


def rebuild_link_fixed_datasets() -> None:
    rebuild_link_fixed_tracks()
    rebuild_link_fixed_artists()
    rebuild_link_fixed_albums()


def rebuild_link_fixed_tracks() -> None:
    source = DATASET_DIR / "raw_tracks.csv"
    target = DATASET_DIR / "link_fix_raw_tracks.csv"
    df = pd.read_csv(source, dtype=str, keep_default_na=False)

    track_file_mask = df["track_file"].ne("")
    df.loc[track_file_mask, "track_file"] = (
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/"
        + df.loc[track_file_mask, "track_file"]
    )

    track_image_mask = df["track_image_file"].ne("")
    df.loc[track_image_mask, "track_image_file"] = (
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/"
        + df.loc[track_image_mask, "track_image_file"].str[34:]
    )

    df.to_csv(target, index=False)


def rebuild_link_fixed_artists() -> None:
    source = DATASET_DIR / "raw_artists.csv"
    target = DATASET_DIR / "link_fix_raw_artists.csv"
    df = pd.read_csv(source, dtype=str, keep_default_na=False)

    artist_ids = pd.to_numeric(df["artist_id"], errors="coerce")
    image_mask = artist_ids.lt(24540) & df["artist_image_file"].ne("")
    df.loc[image_mask, "artist_image_file"] = (
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/"
        + df.loc[image_mask, "artist_image_file"].str[34:]
    )

    df.to_csv(target, index=False)


def rebuild_link_fixed_albums() -> None:
    source = DATASET_DIR / "raw_albums.csv"
    target = DATASET_DIR / "link_fix_raw_albums.csv"
    df = pd.read_csv(source, dtype=str, keep_default_na=False)

    album_ids = pd.to_numeric(df["album_id"], errors="coerce")
    image_mask = album_ids.lt(23284) & df["album_image_file"].ne("")
    df.loc[image_mask, "album_image_file"] = (
        "https://files.freemusicarchive.org/storage-freemusicarchive-org/"
        + df.loc[image_mask, "album_image_file"].str[34:]
    )

    df.to_csv(target, index=False)
