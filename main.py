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

    # Execute le script population.py
    print("Populating temp database...")
    import population
    population.main()
    print("Temp Database populated.")

    # Crée les triggers et fonctions à pour le sgbd
    print("Creating triggers and functions for the DBMS...")
    with open('sql/trigger_bdd.sql', 'r') as file:
        trigger_commands = file.read()
    cursor.execute(trigger_commands)
    conn.commit()
    print("Triggers and functions created.")

    # Execute le script sql import_tables.sql qui importe les données dans les tables
    """
    print("Importing tables...")
    with open('sql/import_tables.sql', 'r') as file:
        import_commands = file.read()
    cursor.execute(import_commands)
    conn.commit()
    print("Tables imported.")
    """

    # Lancement du script qui crée les csv nettoyés pour l'import des users
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
        insert_query = """INSERT INTO sae5_6.user_profile (user_profile_id, music_envy_today, feeling, music_preference, music_style_preference, music_reason, listening_context, current_music_type, usual_listening_mode, likes_discovery, attend_live_concert, repeat_listening, explicit_ok, avg_song_length, avg_daily_listen_time, recommended_artists) VALUES %s"""
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
            recommended_artists = row[headers.index('recommended_artists')]
            buffer.append((user_profile_id, music_envy_today, feeling, music_preference, music_style_preference, music_reason, listening_context, current_music_type, usual_listening_mode, likes_discovery, attend_live_concert, repeat_listening, explicit_ok, avg_song_length, avg_daily_listen_time, recommended_artists))
            if len(buffer) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query, buffer)
                buffer.clear()
        # Insère les restants
        if buffer:
            psycopg2.extras.execute_values(cursor, insert_query, buffer)
            buffer.clear()
    conn.commit()
    print("User profile data imported.")

    # Import des users
    with open('user_data_clean/user.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Passe l'entête
        insert_query = """INSERT INTO sae5_6.user (user_id, user_age, user_job, user_plays_music, user_pseudo, user_password, user_gender, user_instruments, user_music_contexts, profile_id) VALUES %s"""
        buffer = []
        for row in reader:
            # user_id,user_pseudo,user_password,user_age,user_job,user_gender,user_plays_music,user_instruments,user_music_contexts
            # 1,user_1,pass_1,21.0,Employé(e) à plein temps,Homme,1.0,['Guitare / Basse / Banjo'],"['Travail / études', 'Trajet', 'Détente', 'Jeu vidéo']"
            user_id = int(row[headers.index('user_id')])
            user_age = float(row[headers.index('user_age')])
            user_job = row[headers.index('user_job')]
            user_plays_music = bool(int(row[headers.index('user_plays_music')]))
            user_pseudo = row[headers.index('user_pseudo')]
            user_password = row[headers.index('user_password')]
            user_gender = row[headers.index('user_gender')]
            user_instruments = row[headers.index('user_instruments')]
            user_music_contexts = float(row[headers.index('user_music_contexts')])
            profile_id = user_id  # Même id que le profil
            buffer.append((user_id, user_age, user_job, user_plays_music, user_pseudo, user_password, user_gender, user_instruments, user_music_contexts, profile_id))
            if len(buffer) >= BATCH_SIZE:
                psycopg2.extras.execute_values(cursor, insert_query, buffer)
                buffer.clear()
        # Insère les restants
        if buffer:
            psycopg2.extras.execute_values(cursor, insert_query, buffer)
            buffer.clear()
    conn.commit()
    print("User data imported.")

    # Import des genres favoris des users
    with open('user_data_clean/user_genres_favoris.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Passe l'entête
        insert_query = """INSERT INTO sae5_6.ajoute_genre_favoris (user_id, genre_id) VALUES %s"""
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

    # Import de la langue préférée des users
    with open('user_data_clean/parle.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Passe l'entête
        insert_query = """INSERT INTO sae5_6.user_parle (user_id, language_id) VALUES %s"""
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
    cursor.close()
    conn.close()

    print("All data imported successfully.")


if __name__ == "__main__":
    main()


