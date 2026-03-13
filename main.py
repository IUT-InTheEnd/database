from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import psycopg2
import psycopg2.extras

import prepare_seed_data
import user
from pipeline_utils import clean_text, is_missing


PREPARED_DIR = Path("prepared_seed_data")
USER_DATA_DIR = Path("user_data_clean")
BATCH_SIZE = 1000


def connection_db() -> psycopg2.extensions.connection:
    conn = psycopg2.connect(
        dbname="InTheEnd_DB",
        user="InTheEnd_User",
        password="InTheEnd_Password",
        host="localhost",
        port="25000",
        connection_factory=psycopg2.extras.LoggingConnection,
    )
    conn.initialize(sys.stderr)
    return conn


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the Muse database.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Regenerate prepared CSV artifacts from source datasets before loading the database.",
    )
    return parser.parse_args()


def execute_sql_file(cursor: psycopg2.extensions.cursor, path: str) -> None:
    with open(path, "r", encoding="utf-8") as handle:
        cursor.execute(handle.read())


def execute_sql_statements(cursor: psycopg2.extensions.cursor, path: str) -> None:
    with open(path, "r", encoding="utf-8") as handle:
        for statement in handle.read().split(";"):
            sql = statement.strip()
            if sql:
                cursor.execute(sql)


def copy_csv_to_table(cursor: psycopg2.extensions.cursor, csv_path: Path, table_name: str) -> None:
    with csv_path.open("r", encoding="utf-8") as handle:
        cursor.copy_expert(
            f"COPY {table_name} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)",
            handle,
        )


def require_prepared_files() -> None:
    required_files = [
        PREPARED_DIR / "import_artist.csv",
        PREPARED_DIR / "import_album.csv",
        PREPARED_DIR / "import_license.csv",
        PREPARED_DIR / "import_language.csv",
        PREPARED_DIR / "import_track.csv",
        PREPARED_DIR / "import_track_genre.csv",
        PREPARED_DIR / "import_echonest.csv",
        PREPARED_DIR / "import_genre.csv",
        USER_DATA_DIR / "user.csv",
        USER_DATA_DIR / "user_profile.csv",
        USER_DATA_DIR / "user_genres_favoris.csv",
        USER_DATA_DIR / "parle.csv",
        USER_DATA_DIR / "user_pref.csv",
    ]
    missing_files = [str(path) for path in required_files if not path.exists()]
    if missing_files:
        missing = "\n".join(missing_files)
        raise FileNotFoundError(
            "Missing prepared CSV artifacts. Run `python3 main.py --rebuild` first.\n"
            f"{missing}"
        )


def rebuild_prepared_artifacts() -> None:
    print("Rebuilding prepared music seed data...")
    prepare_seed_data.main()
    print("Prepared music seed data rebuilt.")

    print("Rebuilding prepared user CSVs...")
    user.main()
    print("Prepared user CSVs rebuilt.")


def load_import_tables(cursor: psycopg2.extensions.cursor) -> None:
    execute_sql_file(cursor, "sql/table_import.sql")
    import_files = {
        "import_artist": PREPARED_DIR / "import_artist.csv",
        "import_album": PREPARED_DIR / "import_album.csv",
        "import_license": PREPARED_DIR / "import_license.csv",
        "import_language": PREPARED_DIR / "import_language.csv",
        "import_track": PREPARED_DIR / "import_track.csv",
        "import_track_genre": PREPARED_DIR / "import_track_genre.csv",
        "import_echonest": PREPARED_DIR / "import_echonest.csv",
        "import_genre": PREPARED_DIR / "import_genre.csv",
    }
    for table_name, csv_path in import_files.items():
        print(f"Loading {csv_path} into {table_name}...")
        copy_csv_to_table(cursor, csv_path, table_name)


def optional_int(value: str) -> int | None:
    text = clean_text(value)
    return None if text == "" else int(text)


def optional_float(value: str) -> float | None:
    text = clean_text(value)
    return None if text == "" else float(text)


def required_int(value: str) -> int:
    text = clean_text(value)
    return int(text or "0")


def import_csv_values(
    cursor: psycopg2.extensions.cursor,
    csv_path: Path,
    insert_query: str,
    row_builder,
) -> None:
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        buffer: list[tuple[object, ...]] = []
        for row in reader:
            buffer.append(row_builder(row))
            if len(buffer) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query, buffer)
                buffer.clear()
        if buffer:
            psycopg2.extras.execute_values(cursor, insert_query, buffer)


def import_user_profile(cursor: psycopg2.extensions.cursor) -> None:
    insert_query = """
        INSERT INTO user_profile (
            user_profile_id,
            music_envy_today,
            feeling,
            music_preference,
            music_style_preference,
            music_reason,
            listening_context,
            current_music_type,
            usual_listening_mode,
            likes_discovery,
            attend_live_concert,
            repeat_listening,
            explicit_ok,
            avg_song_length,
            avg_daily_listen_time,
            recommanded_artists
        ) VALUES %s
    """
    import_csv_values(
        cursor,
        USER_DATA_DIR / "user_profile.csv",
        insert_query,
        lambda row: (
            required_int(row["user_profile_id"]),
            clean_text(row["music_envy_today"]),
            required_int(row["feeling"]),
            required_int(row["music_preference"]),
            required_int(row["music_style_preference"]),
            clean_text(row["music_reason"]),
            clean_text(row["listening_context"]),
            optional_int(row["current_music_type"]),
            required_int(row["usual_listening_mode"]),
            required_int(row["likes_discovery"]),
            required_int(row["attend_live_concert"]),
            required_int(row["repeat_listening"]),
            required_int(row["explicit_ok"]),
            float(clean_text(row["avg_song_length"]) or "0"),
            float(clean_text(row["avg_daily_listen_time"]) or "0"),
            clean_text(row["recommended_artists"]),
        ),
    )


def import_users(cursor: psycopg2.extensions.cursor) -> None:
    insert_query = """
        INSERT INTO "user" (
            id,
            name,
            email,
            email_verified_at,
            password,
            remember_token,
            created_at,
            updated_at,
            user_age,
            user_job,
            user_plays_music,
            user_gender,
            user_instruments,
            user_music_contexts,
            profile_id
        ) VALUES %s
    """
    import_csv_values(
        cursor,
        USER_DATA_DIR / "user.csv",
        insert_query,
        lambda row: (
            required_int(row["id"]),
            clean_text(row["name"]),
            clean_text(row["email"]),
            clean_text(row["email_verified_at"]) or None,
            clean_text(row["password"]),
            clean_text(row["remember_token"]) or None,
            clean_text(row["created_at"]) or None,
            clean_text(row["updated_at"]) or None,
            optional_float(row["user_age"]),
            clean_text(row["user_job"]),
            clean_text(row["user_plays_music"]),
            clean_text(row["user_gender"]),
            clean_text(row["user_instruments"]),
            clean_text(row["user_music_contexts"]),
            required_int(row["profile_id"]),
        ),
    )


def import_simple_relation(
    cursor: psycopg2.extensions.cursor,
    csv_path: Path,
    insert_query: str,
    columns: tuple[str, str],
) -> None:
    import_csv_values(
        cursor,
        csv_path,
        insert_query,
        lambda row: (required_int(row[columns[0]]), required_int(row[columns[1]])),
    )


def import_user_privacy(cursor: psycopg2.extensions.cursor) -> None:
    cursor.execute('SELECT id FROM "user" ORDER BY id')
    user_ids = [(row[0],) for row in cursor.fetchall()]
    if user_ids:
        psycopg2.extras.execute_values(
            cursor,
            "INSERT INTO user_privacy (id) VALUES %s",
            user_ids,
        )


def import_user_preferences(cursor: psycopg2.extensions.cursor) -> None:
    with (USER_DATA_DIR / "user_pref.csv").open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        track_buffer: list[tuple[int, int]] = []
        artist_buffer: list[tuple[int, int]] = []
        album_buffer: list[tuple[int, int]] = []
        for row in reader:
            if any(is_missing(row[column]) for column in ("user_id", "track_id", "album_id", "artist_id")):
                continue
            user_id = required_int(row["user_id"])
            track_buffer.append((user_id, required_int(row["track_id"])))
            artist_buffer.append((user_id, required_int(row["artist_id"])))
            album_buffer.append((user_id, required_int(row["album_id"])))

            if len(track_buffer) >= BATCH_SIZE:
                flush_user_preferences(cursor, track_buffer, artist_buffer, album_buffer)
        flush_user_preferences(cursor, track_buffer, artist_buffer, album_buffer)


def flush_user_preferences(
    cursor: psycopg2.extensions.cursor,
    track_buffer: list[tuple[int, int]],
    artist_buffer: list[tuple[int, int]],
    album_buffer: list[tuple[int, int]],
) -> None:
    if track_buffer:
        psycopg2.extras.execute_values(
            cursor,
            "INSERT INTO ajoute_favori (user_id, track_id) VALUES %s ON CONFLICT DO NOTHING",
            track_buffer,
        )
        track_buffer.clear()
    if artist_buffer:
        psycopg2.extras.execute_values(
            cursor,
            "INSERT INTO user_prefere_artiste (user_id, artist_id) VALUES %s ON CONFLICT DO NOTHING",
            artist_buffer,
        )
        artist_buffer.clear()
    if album_buffer:
        psycopg2.extras.execute_values(
            cursor,
            "INSERT INTO user_ajoute_album_favoris (user_id, album_id) VALUES %s ON CONFLICT DO NOTHING",
            album_buffer,
        )
        album_buffer.clear()


def import_user_data(cursor: psycopg2.extensions.cursor) -> None:
    print("Importing user profile data...")
    import_user_profile(cursor)
    print("Importing users...")
    import_users(cursor)
    print("Creating user privacy rows...")
    import_user_privacy(cursor)
    print("Importing favorite genres...")
    import_simple_relation(
        cursor,
        USER_DATA_DIR / "user_genres_favoris.csv",
        "INSERT INTO ajoute_genre_favoris (user_id, genre_id) VALUES %s",
        ("user_id", "genre_id"),
    )
    print("Importing spoken languages...")
    import_simple_relation(
        cursor,
        USER_DATA_DIR / "parle.csv",
        "INSERT INTO user_parle (user_id, language_id) VALUES %s",
        ("user_id", "language_id"),
    )
    print("Importing favorite tracks, artists, and albums...")
    import_user_preferences(cursor)


def drop_import_tables(cursor: psycopg2.extensions.cursor) -> None:
    cursor.execute(
        """
        DROP TABLE IF EXISTS import_artist;
        DROP TABLE IF EXISTS import_album;
        DROP TABLE IF EXISTS import_track;
        DROP TABLE IF EXISTS import_genre;
        DROP TABLE IF EXISTS import_echonest;
        DROP TABLE IF EXISTS import_license;
        DROP TABLE IF EXISTS import_language;
        DROP TABLE IF EXISTS import_track_genre;
        """
    )


def main() -> None:
    args = parse_args()
    if args.rebuild:
        rebuild_prepared_artifacts()

    require_prepared_files()

    conn = connection_db()
    try:
        cursor = conn.cursor()
        print("Creating database schema...")
        execute_sql_file(cursor, "sql/bdd.sql")
        print("Creating triggers and functions...")
        execute_sql_file(cursor, "sql/trigger_bdd.sql")
        print("Loading prepared import tables...")
        load_import_tables(cursor)
        print("Importing core tables...")
        execute_sql_statements(cursor, "sql/import_tables.sql")
        print("Importing user data...")
        import_user_data(cursor)
        print("Dropping import tables...")
        drop_import_tables(cursor)
        print("Fixing sequences...")
        execute_sql_file(cursor, "sql/fix_sequence.sql")
        conn.commit()
    finally:
        conn.close()

    print("Seed completed.")


if __name__ == "__main__":
    main()
