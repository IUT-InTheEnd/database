from __future__ import annotations

import ast
import json
from datetime import datetime
from typing import Any

import bcrypt
import pandas as pd

from pipeline_utils import clean_optional_float, clean_text, clear_csv_files, write_csv


USER_DATA_DIR = "user_data_clean"


def generate_name(user_id: int) -> str:
    return f"User {user_id}"


def generate_email(user_id: int) -> str:
    return f"user{user_id}@example.com"


def generate_password_hash(user_id: int) -> str:
    password = f"password{user_id}"
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


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
    return {
        "Calme": 0,
        "Équilibré(e)": 1,
        "Plein(e) d'énergie": 2,
    }.get(feeling)


def transform_music_preference(preference: str) -> int | None:
    return {
        "L'ambiance musicale": 0,
        "Les paroles": 1,
        "Les deux / Sans préférence": 2,
    }.get(preference)


def transform_music_style_preference(style: str) -> int | None:
    return {
        "Plutôt acoustique / naturelle": 0,
        "Plutôt électronique / synthétique": 1,
        "Les deux / Sans préférence": 2,
    }.get(style)


def transform_current_music_type(music_type: str) -> int:
    return {
        "Neutres": 1,
        "Mélancoliques": 2,
        "Des morceaux joyeux": 3,
    }.get(music_type, 0)


def transform_usual_listening_mode(mode: str) -> int | None:
    return {
        "Seul(e)": 1,
        "Avec les gens que vous côtoyez (amis, famille, collègues de travail...)": 2,
    }.get(mode)


def transform_genres(genres: list[str]) -> list[int]:
    genre_map = {
        "Pop": 10,
        "Rock": 12,
        "Hip-Hop": 21,
        "Soul-RnB": 14,
        "Électronique": 15,
        "Classique": 5,
        "Blues": 3,
        "Jazz": 4,
        "Folk": 17,
        "Country": 9,
        "Musique expérimentale": 38,
        "Instrumental": 1235,
        "Easy Listening (Musique d'ascenseur)": 13,
        "Old-Time / Historic": 8,
        "Musique du monde": 2,
        "Parlé (slam, poésie, podcast...)": 20,
    }
    return [genre_map[genre] for genre in genres if genre in genre_map]


def transform_languages(languages: list[str]) -> list[int]:
    language_map = {
        "Anglais": 1,
        "Français": 15,
        "Espagnol": 2,
        "Allemand": 32,
        "Italien": 22,
        "Portugais": 5,
        "Russe": 43,
        "Chinois": 25,
        "Japonais": 20,
        "Coréen": 34,
        "Arabe": 9,
        "Turc": 6,
        "hindi": 18,
        "Latin": 46,
        "Plutôt instrumental": 1235,
    }
    return [language_map[language] for language in languages if language in language_map]


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


def build_user_genres_rows(df: pd.DataFrame) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for _, row in df.iterrows():
        user_id = int(row["user_id"])
        for genre_id in transform_genres(parse_list(row["current_genres"])):
            rows.append({"user_id": user_id, "genre_id": genre_id})
    return rows


def build_user_language_rows(df: pd.DataFrame) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for _, row in df.iterrows():
        user_id = int(row["user_id"])
        for language_id in transform_languages(parse_list(row["song_languages"])):
            rows.append({"user_id": user_id, "language_id": language_id})
    return rows


def main() -> None:
    clear_csv_files(USER_DATA_DIR, keep={"user_pref.csv"})
    df = pd.read_csv("dataset/clean_answers.csv", keep_default_na=False)

    if "user_id" not in df.columns:
        df.insert(0, "user_id", range(1, len(df) + 1))

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
        build_user_genres_rows(df),
    )
    write_csv(
        f"{USER_DATA_DIR}/parle.csv",
        ["user_id", "language_id"],
        build_user_language_rows(df),
    )


if __name__ == "__main__":
    main()
