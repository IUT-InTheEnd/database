import pandas as pd
import json
import ast
import csv
import math
import os

def main():
    df = pd.read_csv("dataset/clean_answers.csv")

    # Suppression des anciens fichiers
    if not os.path.exists("user_data_clean"):
        os.makedirs("user_data_clean")
    else:
        for filename in os.listdir("user_data_clean"):
            file_path = os.path.join("user_data_clean", filename)
            if os.path.isfile(file_path) and filename.lower().endswith(".csv"):
                os.remove(file_path)

    # --- FIX ---
    # user_id au début du header car absent dans le CSV d'origine
    if "user_id" not in df.columns:
        df.insert(0, "user_id", range(1, len(df) + 1))

    def generate_pseudo(user_id):
        return f"user_{user_id}"

    def generate_password(user_id):
        return f"pass_{user_id}"

    # --- MAPPINGS ---

    def transform_fealing(feeling):
        return {
            "Calme": 0,
            "Équilibré(e)": 1,
            "Plein(e) d'énergie": 2
        }.get(feeling)

    def transform_music_preference(pref):
        return {
            "L'ambiance musicale": 0,
            "Les paroles": 1,
            "Les deux / Sans préférence": 2
        }.get(pref)

    def transform_music_style_preference(style):
        return {
            "Plutôt acoustique / naturelle": 0,
            "Plutôt électronique / synthétique": 1,
            "Les deux / Sans préférence": 2
        }.get(style)

    def transform_current_music_type(music_type):
        return {
            "Neutres": 1,
            "Mélancoliques": 2,
            "Des morceaux joyeux": 3
        }.get(music_type, 0)

    def transform_usual_listening_mode(mode):
        return {
            "Seul(e)": 1,
            "Avec les gens que vous côtoyez (amis, famille, collègues de travail...)": 2
        }.get(mode)

    def transform_genres(genres):
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
            "Parlé (slam, poésie, podcast...)": 20
        }
        return [genre_map[g] for g in genres if g in genre_map]

    def transform_languages(languages):
        langues_map = {
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
            "Latin": 46
        }
        return [langues_map[l] for l in languages if l in langues_map]


    # ---------------------------------------------------------
    # 1) TABLE USER
    # ---------------------------------------------------------

    user_rows = []

    for _, row in df.iterrows():
        user_rows.append({
            "user_id": row["user_id"],
            "user_pseudo": generate_pseudo(row["user_id"]),
            "user_password": generate_password(row["user_id"]),
            "user_age": row["age"],
            "user_job": row["job_status"],
            "user_gender": row["gender"],
            "user_plays_music": row["plays_music"],
            "user_instruments": row["instruments"],
            "user_music_contexts": row["listening_contexts"]
        })

    with open("./user_data_clean/user.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=user_rows[0].keys())
        writer.writeheader()
        writer.writerows(user_rows)
    print("user.csv créé")


    # ---------------------------------------------------------
    # 2) TABLE USER PROFILE
    # ---------------------------------------------------------

    user_profile_rows = []

    for _, row in df.iterrows():
        user_profile_rows.append({
            "user_profile_id": row["user_id"],
            "music_envy_today": row["music_mood_today"],
            "feeling": transform_fealing(row["current_feeling"]),
            "music_preference": transform_music_preference(row["music_preference"]),
            "music_style_preference": transform_music_style_preference(row["music_style_preference"]),
            "music_reason": row["music_reason"],
            "listening_context": row["listening_contexts"],
            "current_music_type": transform_current_music_type(row["current_music_type"]),
            "usual_listening_mode": transform_usual_listening_mode(row["usual_listening_mode"]),
            "likes_discovery": row["likes_discovery"],
            "attend_live_concert": row["attend_live_concert"],
            "repeat_listening": row["repeat_listening"],
            "explicit_ok": row["explicit_ok"],
            "avg_song_length": row["avg_song_length"],
            "avg_daily_listen_time": row["avg_daily_listen_time"],
            "recommended_artists": row["recommended_artists"]
        })

    with open("./user_data_clean/user_profile.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=user_profile_rows[0].keys())
        writer.writeheader()
        writer.writerows(user_profile_rows)
    print("user_profile.csv créé")


    # ---------------------------------------------------------
    # 3) TABLE AJOUTE GENRE FAVORIS
    # ---------------------------------------------------------

    genre_rows = []

    for _, row in df.iterrows():
        user_id = row["user_id"]
        genres = row["current_genres"]

        try:
            genres_list = json.loads(genres)        # ex: '["Rock", "Pop"]'
        except:
            try:
                genres_list = ast.literal_eval(genres)  # ex: "['Rock', 'Pop']"
            except:
                genres_list = [g.strip() for g in genres.split(",")]  # ex: "Rock, Pop"

        # S'assurer que c'est une liste
        if not isinstance(genres_list, list):
            genres_list = [genres_list]

        # Convertir en IDs
        genre_ids = transform_genres(genres_list)

        for gid in genre_ids:
            genre_rows.append({"user_id": user_id, "genre_id": gid})

    with open("./user_data_clean/user_genres_favoris.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "genre_id"])
        writer.writeheader()
        writer.writerows(genre_rows)
    print("user_genres_favoris.csv créé")


    # ---------------------------------------------------------
    # 4) TABLE PARLE (langues)
    # ---------------------------------------------------------

    language_rows = []

    for _, row in df.iterrows():
        user_id = row["user_id"]

        # lire la liste de langues proprement
        raw = row["song_languages"]
        if raw is None or (isinstance(raw, float) and math.isnan(raw)):
            continue

        try:
            languages = json.loads(raw)
        except:
            languages = ast.literal_eval(raw)

        languages_ids = transform_languages(languages)

        for lid in languages_ids:
            language_rows.append({"user_id": user_id, "language_id": lid})

    with open("./user_data_clean/parle.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "language_id"])
        writer.writeheader()
        writer.writerows(language_rows)
    print("parle.csv créé")

if __name__ == "__main__":
    main()
