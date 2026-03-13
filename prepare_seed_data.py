from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

from langcodes import Language

import link_fix
from pipeline_utils import (
    clean_bool_flag,
    clean_optional_float,
    clean_optional_int,
    clean_required_int,
    clean_text,
    clear_csv_files,
    ensure_directory,
    write_csv,
)


DATASET_DIR = Path("dataset")
PREPARED_DIR = Path("prepared_seed_data")
TRACK_GENRE_PATTERN = re.compile(r"'genre_id': '(\d+)'")
UNKNOWN_LICENSE_TITLE = "Unknown license"


def required_title(value: str, fallback: str) -> str:
    title = clean_text(value)
    return title or fallback


def process_language_code(code: str) -> str:
    language_code = clean_text(code)
    if language_code == "":
        return "Unknown"
    try:
        return Language.get(language_code).language_name("en").capitalize()
    except (KeyError, ValueError):
        return "Unknown"


def process_date(date_str: str) -> str:
    from datetime import datetime

    value = clean_text(date_str)
    if value == "":
        return ""
    for fmt in ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%d-%m-%Y")
        except ValueError:
            continue
    return ""


def process_duration(duration_str: str) -> str:
    value = clean_text(duration_str)
    if value == "":
        return ""
    parts = value.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = [int(part) for part in parts]
        return str(hours * 3600 + minutes * 60 + seconds)
    if len(parts) == 2:
        minutes, seconds = [int(part) for part in parts]
        return str(minutes * 60 + seconds)
    return clean_required_int(value)


def prepare_seed_data() -> None:
    link_fix.rebuild_link_fixed_datasets()
    clear_csv_files(PREPARED_DIR)
    ensure_directory(PREPARED_DIR)

    artist_rows, artist_ids = load_artists()
    album_rows, album_ids = load_albums()
    (
        license_rows,
        language_rows,
        track_rows,
        track_genre_rows,
        valid_track_ids,
        artist_listens,
    ) = load_tracks(album_ids, artist_ids)

    write_csv(
        PREPARED_DIR / "import_artist.csv",
        [
            "artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude",
            "artist_favorites",
            "artist_comments",
            "artist_listens",
            "artist_active_year_begin",
            "artist_active_year_end",
            "artist_url",
            "artist_website",
            "artist_wikipedia_page",
            "artist_handle",
            "artist_bio",
            "artist_members",
            "artist_associated_labels",
            "artist_related_projects",
            "artist_contact",
            "artist_donation_url",
            "artist_paypal_name",
            "artist_flattr_name",
            "artist_date_created",
            "artist_image_file",
        ],
        (
            {**row, "artist_listens": str(artist_listens.get(row["artist_id"], 0))}
            for row in artist_rows
        ),
    )
    write_csv(
        PREPARED_DIR / "import_album.csv",
        list(album_rows[0].keys()) if album_rows else [],
        album_rows,
    )
    write_csv(
        PREPARED_DIR / "import_license.csv",
        ["license_id", "license_title", "license_url"],
        license_rows,
    )
    write_csv(
        PREPARED_DIR / "import_language.csv",
        ["language_id", "language_code", "language_name", "language_handle"],
        language_rows,
    )
    write_csv(PREPARED_DIR / "import_track.csv", list(track_rows[0].keys()) if track_rows else [], track_rows)
    write_csv(
        PREPARED_DIR / "import_track_genre.csv",
        ["track_id", "genre_id"],
        track_genre_rows,
    )
    write_csv(
        PREPARED_DIR / "import_echonest.csv",
        [
            "track_id",
            "acousticness",
            "energy",
            "instrumentalness",
            "liveness",
            "speechiness",
            "valence",
            "danceability",
            "tempo",
            "artist_discovery",
            "artist_hottness",
            "artist_familiarity",
            "track_hottness",
            "track_currency",
        ],
        load_echonest(valid_track_ids),
    )
    write_csv(
        PREPARED_DIR / "import_genre.csv",
        ["genre_id", "genre_parent_id", "genre_title", "genre_handle", "genre_color", "top_level"],
        load_genres(),
    )


def load_artists() -> tuple[list[dict[str, str]], set[str]]:
    rows: list[dict[str, str]] = []
    artist_ids: set[str] = set()

    with (DATASET_DIR / "link_fix_raw_artists.csv").open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            artist_id = clean_required_int(row["artist_id"])
            prepared_row = {
                "artist_id": artist_id,
                "artist_name": clean_text(row["artist_name"]),
                "artist_location": clean_text(row["artist_location"]),
                "artist_latitude": clean_optional_float(row["artist_latitude"]),
                "artist_longitude": clean_optional_float(row["artist_longitude"]),
                "artist_favorites": clean_required_int(row["artist_favorites"]),
                "artist_comments": clean_required_int(row["artist_comments"]),
                "artist_listens": "0",
                "artist_active_year_begin": clean_optional_int(row["artist_active_year_begin"]),
                "artist_active_year_end": clean_optional_int(row["artist_active_year_end"]),
                "artist_url": clean_text(row["artist_url"]),
                "artist_website": clean_text(row["artist_website"]),
                "artist_wikipedia_page": clean_text(row["artist_wikipedia_page"]),
                "artist_handle": clean_text(row["artist_handle"]),
                "artist_bio": clean_text(row["artist_bio"]),
                "artist_members": clean_text(row["artist_members"]),
                "artist_associated_labels": clean_text(row["artist_associated_labels"]),
                "artist_related_projects": clean_text(row["artist_related_projects"]),
                "artist_contact": clean_text(row["artist_contact"]),
                "artist_donation_url": clean_text(row["artist_donation_url"]),
                "artist_paypal_name": clean_text(row["artist_paypal_name"]),
                "artist_flattr_name": clean_text(row["artist_flattr_name"]),
                "artist_date_created": process_date(row["artist_date_created"]),
                "artist_image_file": clean_text(row["artist_image_file"]),
            }
            rows.append(prepared_row)
            artist_ids.add(artist_id)

    return rows, artist_ids


def load_albums() -> tuple[list[dict[str, str]], set[str]]:
    rows: list[dict[str, str]] = []
    album_ids: set[str] = set()

    with (DATASET_DIR / "link_fix_raw_albums.csv").open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            album_id = clean_required_int(row["album_id"])
            rows.append(
                {
                    "album_id": album_id,
                    "album_title": clean_text(row["album_title"]),
                    "album_date_release": process_date(row["album_date_released"]),
                    "album_date_created": process_date(row["album_date_created"]),
                    "album_listens": clean_required_int(row["album_listens"]),
                    "album_favorites": clean_required_int(row["album_favorites"]),
                    "album_comments": clean_required_int(row["album_comments"]),
                    "album_type": clean_text(row["album_type"]),
                    "album_url": clean_text(row["album_url"]),
                    "album_handle": clean_text(row["album_handle"]),
                    "album_information": clean_text(row["album_information"]),
                    "album_tracks": clean_required_int(row["album_tracks"]),
                    "album_producer": clean_text(row["album_producer"]),
                    "album_engineer": clean_text(row["album_engineer"]),
                    "album_image_file": clean_text(row["album_image_file"]),
                }
            )
            album_ids.add(album_id)

    return rows, album_ids


def load_tracks(
    album_ids: set[str],
    artist_ids: set[str],
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    set[str],
    dict[str, int],
]:
    license_map: dict[tuple[str, str], str] = {}
    language_map: dict[str, str] = {}
    license_rows: list[dict[str, str]] = []
    language_rows: list[dict[str, str]] = []
    track_rows: list[dict[str, str]] = []
    track_genre_rows: list[dict[str, str]] = []
    valid_track_ids: set[str] = set()
    artist_listens: dict[str, int] = defaultdict(int)

    with (DATASET_DIR / "link_fix_raw_tracks.csv").open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            album_id = clean_required_int(row["album_id"])
            artist_id = clean_required_int(row["artist_id"])
            track_id = clean_required_int(row["track_id"])
            if album_id not in album_ids or artist_id not in artist_ids:
                continue

            license_title = clean_text(row["license_title"]) or UNKNOWN_LICENSE_TITLE
            license_key = (license_title, clean_text(row["license_url"]))
            if license_key not in license_map:
                license_id = str(len(license_map) + 1)
                license_map[license_key] = license_id
                license_rows.append(
                    {
                        "license_id": license_id,
                        "license_title": license_title,
                        "license_url": license_key[1],
                    }
                )
            language_code = clean_text(row["track_language_code"])
            if language_code not in language_map:
                language_id = str(len(language_map) + 1)
                language_name = process_language_code(language_code)
                language_map[language_code] = language_id
                language_rows.append(
                    {
                        "language_id": language_id,
                        "language_code": language_code,
                        "language_name": language_name,
                        "language_handle": language_name.lower().replace(" ", "_"),
                    }
                )

            listens = clean_required_int(row["track_listens"])
            valid_track_ids.add(track_id)
            artist_listens[artist_id] += int(listens)
            track_rows.append(
                {
                    "track_id": track_id,
                    "track_title": required_title(row["track_title"], f"Untitled track {track_id}"),
                    "track_duration": process_duration(row["track_duration"]),
                    "track_date_created": process_date(row["track_date_created"]),
                    "track_date_recorded": process_date(row["track_date_recorded"]),
                    "track_composer": clean_text(row["track_composer"]),
                    "track_lyricist": clean_text(row["track_lyricist"]),
                    "track_publisher": clean_text(row["track_publisher"]),
                    "track_listens": listens,
                    "track_favorites": clean_required_int(row["track_favorites"]),
                    "track_comments": clean_required_int(row["track_comments"]),
                    "track_interest": clean_required_int(row["track_interest"]),
                    "track_copyright_c": clean_text(row["track_copyright_c"]),
                    "track_copyright_p": clean_text(row["track_copyright_p"]),
                    "track_explicit": clean_text(row["track_explicit"]),
                    "track_explicit_note": clean_text(row["track_explicit_notes"]),
                    "track_instrumental": clean_bool_flag(row["track_instrumental"]),
                    "track_language_code": language_code,
                    "track_url": clean_text(row["track_url"]),
                    "track_file": clean_text(row["track_file"]),
                    "track_image_file": clean_text(row["track_image_file"]),
                    "license_id": license_map[license_key],
                    "artist_id": artist_id,
                    "album_id": album_id,
                    "language_id": language_map[language_code],
                }
            )

            for genre_id in TRACK_GENRE_PATTERN.findall(clean_text(row["track_genres"])):
                track_genre_rows.append({"track_id": track_id, "genre_id": genre_id})

    return (
        license_rows,
        language_rows,
        track_rows,
        track_genre_rows,
        valid_track_ids,
        dict(artist_listens),
    )


def load_echonest(valid_track_ids: set[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with (DATASET_DIR / "clean_echonest.csv").open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            track_id = clean_required_int(row["track_id"])
            if track_id not in valid_track_ids:
                continue
            rows.append(
                {
                    "track_id": track_id,
                    "acousticness": clean_optional_float(row["echonest_audio_features_acousticness"]),
                    "energy": clean_optional_float(row["echonest_audio_features_energy"]),
                    "instrumentalness": clean_optional_float(row["echonest_audio_features_instrumentalness"]),
                    "liveness": clean_optional_float(row["echonest_audio_features_liveness"]),
                    "speechiness": clean_optional_float(row["echonest_audio_features_speechiness"]),
                    "valence": clean_optional_float(row["echonest_audio_features_valence"]),
                    "danceability": clean_optional_float(row["echonest_audio_features_danceability"]),
                    "tempo": clean_optional_float(row["echonest_audio_features_tempo"]),
                    "artist_discovery": clean_optional_float(row["echonest_social_features_artist_discovery"]),
                    "artist_hottness": clean_optional_float(row["echonest_social_features_artist_hotttnesss"]),
                    "artist_familiarity": clean_optional_float(row["echonest_social_features_artist_familiarity"]),
                    "track_hottness": clean_optional_float(row["echonest_social_features_song_hotttnesss"]),
                    "track_currency": clean_optional_float(row["echonest_social_features_song_currency"]),
                }
            )
    return rows


def load_genres() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with (DATASET_DIR / "raw_genres.csv").open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            parent_id = clean_optional_int(row["genre_parent_id"])
            rows.append(
                {
                    "genre_id": clean_required_int(row["genre_id"]),
                    "genre_parent_id": parent_id,
                    "genre_title": clean_text(row["genre_title"]),
                    "genre_handle": clean_text(row["genre_handle"]),
                    "genre_color": clean_text(row["genre_color"]),
                    "top_level": "true" if parent_id == "" else "false",
                }
            )
    return rows


def main() -> None:
    prepare_seed_data()


if __name__ == "__main__":
    main()
