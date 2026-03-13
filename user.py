from __future__ import annotations

import ast
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import bcrypt
import pandas as pd

from pipeline_utils import clean_optional_float, clean_text, clear_csv_files, write_csv


USER_DATA_DIR = "prepared_seed_data/user"
PREPARED_LANGUAGE_PATH = Path("prepared_seed_data/import_language.csv")
PREPARED_GENRE_PATH = Path("prepared_seed_data/import_genre.csv")

FEELING_MAP = {
    "Calme": 0,
    "Équilibré(e)": 1,
    "Plein(e) d'énergie": 2,
}

MUSIC_PREFERENCE_MAP = {
    "L'ambiance musicale": 0,
    "Les paroles": 1,
    "Les deux / Sans préférence": 2,
}

MUSIC_STYLE_PREFERENCE_MAP = {
    "Plutôt acoustique / naturelle": 0,
    "Plutôt électronique / synthétique": 1,
    "Les deux / Sans préférence": 2,
}

CURRENT_MUSIC_TYPE_MAP = {
    "Neutres": 1,
    "Mélancoliques": 2,
    "Des morceaux joyeux": 3,
}

USUAL_LISTENING_MODE_MAP = {
    "Seul(e)": 1,
    "Avec les gens que vous côtoyez (amis, famille, collègues de travail...)": 2,
}

SURVEY_GENRE_TITLES = {
    "Pop": "Pop",
    "Rock": "Rock",
    "Hip-Hop": "Hip-Hop",
    "Soul-RnB": "Soul-RnB",
    "Électronique": "Electronic",
    "Classique": "Classical",
    "Blues": "Blues",
    "Jazz": "Jazz",
    "Folk": "Folk",
    "Country": "Country",
    "Musique expérimentale": "Experimental",
    "Instrumental": "Instrumental",
    "Easy Listening (Musique d'ascenseur)": "Easy Listening",
    "Old-Time / Historic": "Old-Time / Historic",
    "Musique du monde": "International",
    "Parlé (slam, poésie, podcast...)": "Spoken",
}

SURVEY_LANGUAGE_CODES = {
    "Anglais": "en",
    "Français": "fr",
    "Espagnol": "es",
    "Allemand": "de",
    "Italien": "it",
    "Portugais": "pt",
    "Russe": "ru",
    "Chinois": "zh",
    "Japonais": "ja",
    "Coréen": "ko",
    "Arabe": "ar",
    "Turc": "tr",
    "hindi": "hi",
    "Latin": "la",
    "Plutôt instrumental": "",
}


def generate_name(user_id: int) -> str:
    return f"User {user_id}"


def generate_email(user_id: int) -> str:
    return f"user{user_id}@example.com"


def generate_password_hash(user_id: int) -> str:
    password = f'MotDePasse{user_id}!'
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    # PHP expects the historical bcrypt $2y$ prefix even though Python emits $2b$.
    return password_hash.replace("$2b$", "$2y$", 1)


def generate_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def normalize_binary_choice(value: Any) -> str:
    text = clean_text(value)
    if text in {"1", "1.0", "true", "True"}:
        return "1"
    if text in {"0", "0.0", "false", "False"}:
        return "0"
    return text


def parse_list(raw: Any) -> list[str]:
    value = clean_text(raw)
    if value == "":
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        try:
            parsed = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            parsed = [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(parsed, list):
        return [clean_text(item) for item in parsed if clean_text(item) != ""]
    cleaned = clean_text(parsed)
    return [cleaned] if cleaned else []


def transform_feeling(feeling: str) -> int | None:
    return FEELING_MAP.get(feeling)


def transform_music_preference(preference: str) -> int | None:
    return MUSIC_PREFERENCE_MAP.get(preference)


def transform_music_style_preference(style: str) -> int | None:
    return MUSIC_STYLE_PREFERENCE_MAP.get(style)


def transform_current_music_type(music_type: str) -> int:
    return CURRENT_MUSIC_TYPE_MAP.get(music_type, 0)


def transform_usual_listening_mode(mode: str) -> int | None:
    return USUAL_LISTENING_MODE_MAP.get(mode)


def load_genre_ids_by_title() -> dict[str, int]:
    if not PREPARED_GENRE_PATH.exists():
        raise FileNotFoundError(
            "Missing prepared genre data. Run `python3 prepare_seed_data.py` or `python3 main.py --rebuild` first."
        )

    genre_ids_by_title: dict[str, int] = {}
    with PREPARED_GENRE_PATH.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            title = clean_text(row["genre_title"])
            if title != "":
                genre_ids_by_title[title] = int(row["genre_id"])
    return genre_ids_by_title


def transform_genres(genres: list[str], genre_ids_by_title: dict[str, int]) -> list[int]:
    genre_ids: list[int] = []
    for genre in genres:
        genre_title = SURVEY_GENRE_TITLES.get(genre, "")
        if genre_title and genre_title in genre_ids_by_title:
            genre_ids.append(genre_ids_by_title[genre_title])
    return genre_ids


def load_language_ids_by_code() -> dict[str, int]:
    if not PREPARED_LANGUAGE_PATH.exists():
        raise FileNotFoundError(
            "Missing prepared language data. Run `python3 prepare_seed_data.py` or `python3 main.py --rebuild` first."
        )

    language_ids_by_code: dict[str, int] = {}
    with PREPARED_LANGUAGE_PATH.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            code = clean_text(row["language_code"])
            if code != "":
                language_ids_by_code[code] = int(row["language_id"])
    return language_ids_by_code


def transform_languages(languages: list[str], language_ids_by_code: dict[str, int]) -> list[int]:
    language_ids: list[int] = []
    for language in languages:
        language_code = SURVEY_LANGUAGE_CODES.get(language, "")
        if language_code and language_code in language_ids_by_code:
            language_ids.append(language_ids_by_code[language_code])
    return language_ids


def build_user_rows(df: pd.DataFrame, timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        user_id = int(row["user_id"])
        rows.append(
            {
                "id": user_id,
                "name": generate_name(user_id),
                "email": generate_email(user_id),
                "email_verified_at": timestamp,
                "password": generate_password_hash(user_id),
                "remember_token": "",
                "created_at": timestamp,
                "updated_at": timestamp,
                "user_age": clean_optional_float(row["age"]),
                "user_job": clean_text(row["job_status"]),
                "user_gender": clean_text(row["gender"]),
                "user_plays_music": normalize_binary_choice(row["plays_music"]),
                "user_instruments": clean_text(row["instruments"]),
                "user_music_contexts": clean_text(row["listening_contexts"]),
                "profile_id": user_id,
            }
        )
    return rows


def build_user_profile_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        user_id = int(row["user_id"])
        rows.append(
            {
                "user_profile_id": user_id,
                "music_envy_today": clean_text(row["music_mood_today"]),
                "feeling": transform_feeling(clean_text(row["current_feeling"])),
                "music_preference": transform_music_preference(clean_text(row["music_preference"])),
                "music_style_preference": transform_music_style_preference(clean_text(row["music_style_preference"])),
                "music_reason": clean_text(row["music_reason"]),
                "listening_context": clean_text(row["listening_contexts"]),
                "current_music_type": transform_current_music_type(clean_text(row["current_music_type"])),
                "usual_listening_mode": transform_usual_listening_mode(clean_text(row["usual_listening_mode"])),
                "likes_discovery": clean_text(row["likes_discovery"]),
                "attend_live_concert": clean_text(row["attend_live_concert"]),
                "repeat_listening": clean_text(row["repeat_listening"]),
                "explicit_ok": clean_text(row["explicit_ok"]),
                "avg_song_length": clean_optional_float(row["avg_song_length"]),
                "avg_daily_listen_time": clean_optional_float(row["avg_daily_listen_time"]),
                "recommended_artists": clean_text(row["recommended_artists"]),
            }
        )
    return rows


def build_user_genres_rows(df: pd.DataFrame, genre_ids_by_title: dict[str, int]) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for _, row in df.iterrows():
        user_id = int(row["user_id"])
        for genre_id in transform_genres(parse_list(row["current_genres"]), genre_ids_by_title):
            rows.append({"user_id": user_id, "genre_id": genre_id})
    return rows


def build_user_language_rows(df: pd.DataFrame, language_ids_by_code: dict[str, int]) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for _, row in df.iterrows():
        user_id = int(row["user_id"])
        for language_id in transform_languages(parse_list(row["song_languages"]), language_ids_by_code):
            rows.append({"user_id": user_id, "language_id": language_id})
    return rows


def main() -> None:
    clear_csv_files(USER_DATA_DIR, keep={"user_pref.csv"})
    df = pd.read_csv("dataset/clean_answers.csv", keep_default_na=False)

    if "user_id" not in df.columns:
        df.insert(0, "user_id", range(1, len(df) + 1))

    genre_ids_by_title = load_genre_ids_by_title()
    language_ids_by_code = load_language_ids_by_code()
    timestamp = generate_timestamp()
    write_csv(
        f"{USER_DATA_DIR}/user.csv",
        [
            "id",
            "name",
            "email",
            "email_verified_at",
            "password",
            "remember_token",
            "created_at",
            "updated_at",
            "user_age",
            "user_job",
            "user_gender",
            "user_plays_music",
            "user_instruments",
            "user_music_contexts",
            "profile_id",
        ],
        build_user_rows(df, timestamp),
    )
    write_csv(
        f"{USER_DATA_DIR}/user_profile.csv",
        [
            "user_profile_id",
            "music_envy_today",
            "feeling",
            "music_preference",
            "music_style_preference",
            "music_reason",
            "listening_context",
            "current_music_type",
            "usual_listening_mode",
            "likes_discovery",
            "attend_live_concert",
            "repeat_listening",
            "explicit_ok",
            "avg_song_length",
            "avg_daily_listen_time",
            "recommended_artists",
        ],
        build_user_profile_rows(df),
    )
    write_csv(
        f"{USER_DATA_DIR}/user_genres_favoris.csv",
        ["user_id", "genre_id"],
        build_user_genres_rows(df, genre_ids_by_title),
    )
    write_csv(
        f"{USER_DATA_DIR}/parle.csv",
        ["user_id", "language_id"],
        build_user_language_rows(df, language_ids_by_code),
    )


if __name__ == "__main__":
    main()
