import psycopg2
import psycopg2.extras
import csv

def connection_db():
    return psycopg2.connect(
        dbname="InTheEnd_DB",
        user="InTheEnd_User",
        password="InTheEnd_Password",
        host="localhost",
        port="25000"
    )

def main():
    # Execute la création de la base de données
    print("Creating database...")
    with open('sql/bdd.sql', 'r') as file:
        sql_commands = file.read()
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute(sql_commands)
    conn.commit()
    print("Database created.")

    # Execute le script peuplement.py
    print("Populating temp database...")
    import peuplement
    peuplement.main()
    print("Temp Database populated.")

    # Crée les triggers et fonctions à pour le sgbd
    print("Creating triggers and functions for the DBMS...")
    with open('sql/trigger_bdd.sql', 'r') as file:
        trigger_commands = file.read()
    cursor.execute(trigger_commands)
    conn.commit()
    print("Triggers and functions created.")

    # Execute le script sql import_tables.sql qui importe les données dans les tables
    print("Importing tables...")
    with open('sql/import_tables.sql', 'r') as file:
        import_commands = file.read()
    cursor.execute(import_commands)
    conn.commit()
    print("Tables imported.")

    # Lancement du script qui crée les csv nettoyés pour l'import des user
    print("Generating cleaned CSV files for user data...")
    import user
    user.main()
    print("Cleaned CSV files generated.")
    
    # Import des données utilisateurs depuis les fichiers csv
    print("Importing user data from CSV files...")
    BATCH_SIZE = 1000


    # Import des profils utilisateurs
    with open('user_data_clean/user_profile.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Passe l'entête
        insert_query = """INSERT INTO user_profile (user_profile_id, music_envy_today, feeling, music_preference, music_style_preference, music_reason, listening_context, current_music_type, usual_listening_mode, likes_discovery, attend_live_concert, repeat_listening, explicit_ok, avg_song_length, avg_daily_listen_time, recommanded_artists) VALUES %s"""
        buffer = []
        for row in reader:
            user_profile_id = int(row[headers.index('user_profile_id')])
            music_envy_today = row[headers.index('music_envy_today')]
            feeling = int(row[headers.index('feeling')])
            music_preference = int(row[headers.index('music_preference')])
            music_style_preference = int(row[headers.index('music_style_preference')])
            music_reason = row[headers.index('music_reason')]
            listening_context = row[headers.index('listening_context')]
            current_music_type = int(row[headers.index('current_music_type')]) if row[headers.index('current_music_type')] != '' else None
            usual_listening_mode = int(row[headers.index('usual_listening_mode')])
            likes_discovery = int(row[headers.index('likes_discovery')])
            attend_live_concert = int(row[headers.index('attend_live_concert')])
            repeat_listening = int(row[headers.index('repeat_listening')])
            explicit_ok = int(row[headers.index('explicit_ok')])
            avg_song_length = float(row[headers.index('avg_song_length')])
            avg_daily_listen_time = float(row[headers.index('avg_daily_listen_time')])
            recommanded_artists = row[headers.index('recommended_artists')]
            buffer.append((user_profile_id, music_envy_today, feeling, music_preference, music_style_preference, music_reason, listening_context, current_music_type, usual_listening_mode, likes_discovery, attend_live_concert, repeat_listening, explicit_ok, avg_song_length, avg_daily_listen_time, recommanded_artists))
            if len(buffer) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query, buffer)
                buffer.clear()
        # Insère les restants
        if buffer:
            psycopg2.extras.execute_values(cursor, insert_query, buffer)
            buffer.clear()
    conn.commit()
    print("User profile data imported.")

    # Import des user (compatible Laravel)
    with open('user_data_clean/user.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Passe l'entête
        insert_query = """INSERT INTO "user" (id, name, email, email_verified_at, password, remember_token, created_at, updated_at, user_age, user_job, user_plays_music, user_gender, user_instruments, user_music_contexts, profile_id) VALUES %s"""
        buffer = []
        for row in reader:
            # id,name,email,email_verified_at,password,remember_token,created_at,updated_at,user_age,user_job,user_gender,user_plays_music,user_instruments,user_music_contexts,profile_id
            user_id = int(row[headers.index('id')])
            name = row[headers.index('name')]
            email = row[headers.index('email')]
            email_verified_at = row[headers.index('email_verified_at')] if row[headers.index('email_verified_at')] else None
            password = row[headers.index('password')]
            remember_token = row[headers.index('remember_token')] if row[headers.index('remember_token')] else None
            created_at = row[headers.index('created_at')] if row[headers.index('created_at')] else None
            updated_at = row[headers.index('updated_at')] if row[headers.index('updated_at')] else None
            user_age = float(row[headers.index('user_age')])
            user_job = row[headers.index('user_job')]
            user_plays_music = 1 if row[headers.index('user_plays_music')] == '1.0' else 0
            user_gender = row[headers.index('user_gender')]
            user_instruments = row[headers.index('user_instruments')]
            user_music_contexts = row[headers.index('user_music_contexts')]
            profile_id = int(row[headers.index('profile_id')])
            buffer.append((user_id, name, email, email_verified_at, password, remember_token, created_at, updated_at, user_age, user_job, user_plays_music, user_gender, user_instruments, user_music_contexts, profile_id))
            if len(buffer) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query, buffer)
                buffer.clear()
        # Insère les restants
        if buffer:
            psycopg2.extras.execute_values(cursor, insert_query, buffer)
            buffer.clear()
    conn.commit()
    print("User data imported.")

    # Import des genres favoris des user
    with open('user_data_clean/user_genres_favoris.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Passe l'entête
        insert_query = """INSERT INTO ajoute_genre_favoris (user_id, genre_id) VALUES %s"""
        buffer = []
        for row in reader:
            user_id = int(row[headers.index('user_id')])
            genre_id = int(row[headers.index('genre_id')])
            buffer.append((user_id, genre_id))
            if len(buffer) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query, buffer)
                buffer.clear()
        # Insère les restants
        if buffer:
            psycopg2.extras.execute_values(cursor, insert_query, buffer)
            buffer.clear()
    conn.commit()
    print("User favorite genre data imported.")

    # Import de la langue préférée des user
    with open('user_data_clean/parle.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Passe l'entête
        insert_query = """INSERT INTO user_parle (user_id, language_id) VALUES %s"""
        buffer = []
        for row in reader:
            user_id = int(row[headers.index('user_id')])
            language_id = int(row[headers.index('language_id')])
            buffer.append((user_id, language_id))
            if len(buffer) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query, buffer)
                buffer.clear()
        # Insère les restants
        if buffer:
            psycopg2.extras.execute_values(cursor, insert_query, buffer)
            buffer.clear()
    conn.commit()
    print("User language preference data imported.")

    print("User favorite music data import completed.")
    with open('user_data_clean/user_pref.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Passe l'entête
        insert_query = """INSERT INTO ajoute_favori (user_id, track_id) VALUES %s ON CONFLICT DO NOTHING"""
        insert_query2 = """INSERT INTO user_prefere_artiste (user_id, artist_id) VALUES %s ON CONFLICT DO NOTHING"""
        insert_query3 = """INSERT INTO user_ajoute_album_favoris (user_id, album_id) VALUES %s ON CONFLICT DO NOTHING"""
        buffer = []
        buffer2 = []
        buffer3 = []
        for row in reader:
            user_id = int(row[headers.index('user_id')])
            track_id = int(row[headers.index('track_id')])
            album_id = int(row[headers.index('album_id')])
            artist_id = int(row[headers.index('artist_id')])
            buffer.append((user_id, track_id))
            buffer2.append((user_id, artist_id))
            buffer3.append((user_id, album_id))
            if len(buffer) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query, buffer)
                buffer.clear()
            if len(buffer2) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query2, buffer2)
                buffer2.clear()
            if len(buffer3) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query3, buffer3)
                buffer3.clear()
        # Insère les restants
        if buffer:
            psycopg2.extras.execute_values(cursor, insert_query, buffer)
            buffer.clear()
        if buffer2:
            psycopg2.extras.execute_values(cursor, insert_query2, buffer2)
            buffer2.clear()
        if buffer3:
            psycopg2.extras.execute_values(cursor, insert_query3, buffer3)
            buffer3.clear()
    conn.commit()
    print("User favorite music data imported.")
        
    print("All data imported successfully.")

    print("Delete import tables...")
    
    query = """
        DROP TABLE IF EXISTS import_artist;
        DROP TABLE IF EXISTS import_album;
        DROP TABLE IF EXISTS import_track;
        DROP TABLE IF EXISTS import_genre;
        DROP TABLE IF EXISTS import_echonest;
        DROP TABLE IF EXISTS import_license;
        DROP TABLE IF EXISTS import_language;
        DROP TABLE IF EXISTS import_track_genre;
    """
    cursor.execute(query)
    conn.commit()
    print("Import tables deleted.")

    cursor.close()
    conn.close()
    print("End.")


if __name__ == "__main__":
    main()


