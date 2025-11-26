import os
import csv
import psycopg2
import psycopg2.extras
import re
import calendar
import pycountry_convert 

def process_language_code(code):
    # on passe de en à Anglais etc...
    try:
        language_name = pycountry_convert.country_alpha2_to_country_name(code.upper())
    except KeyError:
        language_name = 'Unknown'
    return language_name

def process_date(date_str):
    # Convertit format : "" en DD-MM-YYYY
    return

def connection_db():
    return psycopg2.connect(
        dbname="InTheEnd_DB",
        user="InTheEnd_User",
        password="InTheEnd_Password",
        host="localhost",
        port="25000"
    )

def import_csv_to_db(csv_file_path):
    conn = connection_db()
    cursor = conn.cursor()
    match csv_file_path:
        case 'raw_artists':
            table_name = ['sae5_6.import_artist']
            table_attributes = ['artist_id, artist_name, artist_location, artist_latitude, artist_longitude, artist_favorites, artist_comments, artist_active_year_begin, artist_active_year_end, artist_url, artist_website, artist_wikipedia_page, artist_handle, artist_bio, artist_members, artist_associated_labels, artist_related_projects, artist_contact, artist_donation_url, artist_paypal_name, artist_flattr_name, artist_date_created, artist_image_file']
        case 'raw_tracks':        
            table_name = ['sae5_6.import_track', 'sae5_6.import_license', 'sae5_6.import_language']
            table_attributes = ['track_id, track_title, track_duration, track_date_created, track_date_recorded, track_composer, track_lyricist, track_publisher, track_listens, track_favorites, track_comments, track_interest, track_copyright_c, track_copyright_p, track_explicit, track_explicit_note, track_instrumental, track_language_code, track_url, track_file, track_image_file', 'license_id, license_title, license_url', 'language_code, language_name, language_handle']
        case 'clean_echonest':       
            table_name = ['sae5_6.import_echonest']
            table_attributes = ['track_id, acousticness, energy, instrumentalness, liveness, speechiness, valence, danceability, tempo, artist_discovery, artist_hottness, artist_familiarity, track_hottness, track_currency']
        case 'raw_genres':
            table_name = ['sae5_6.import_genre']
            table_attributes = ['genre_id, genre_parent_id, genre_title, genre_handle, genre_color, top_level']
        case 'raw_albums':
            table_name = ['sae5_6.import_album']
            table_attributes = ['album_id, album_title, album_date_release, album_date_created, album_listens, album_favorites, album_comments, album_type, album_url, album_handle, album_information, album_tracks, album_producer, album_engineer']
        case _:
            raise ValueError("Unknown CSV file path")

    for i in range(len(table_name)):
        csv_file_path_full = f"dataset/{csv_file_path}.csv"
        with open(csv_file_path_full, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # On suppose que la première ligne contient les en-têtes
            match table_name[i]:
                case 'sae5_6.import_artist':
                    if headers:
                        for row in reader:
                            artist_id = row[headers.index('artist_id')]
                            artist_name = row[headers.index('artist_name')]
                            artist_location = row[headers.index('artist_location')]
                            artist_latitude = row[headers.index('artist_latitude')]
                            artist_longitude = row[headers.index('artist_longitude')]
                            artist_favorites = row[headers.index('artist_favorites')]
                            artist_comments = row[headers.index('artist_comments')]
                            artist_active_year_begin = row[headers.index('artist_active_year_begin')]
                            artist_active_year_end = row[headers.index('artist_active_year_end')]
                            artist_url = row[headers.index('artist_url')]
                            artist_website = row[headers.index('artist_website')]
                            artist_wikipedia_page = row[headers.index('artist_wikipedia_page')]
                            artist_handle = row[headers.index('artist_handle')]
                            artist_bio = row[headers.index('artist_bio')]
                            artist_members = row[headers.index('artist_members')]
                            artist_associated_labels = row[headers.index('artist_associated_labels')]
                            artist_related_projects = row[headers.index('artist_related_projects')]
                            artist_contact = row[headers.index('artist_contact')]
                            artist_donation_url = row[headers.index('artist_donation_url')]
                            artist_paypal_name = row[headers.index('artist_paypal_name')]
                            artist_flattr_name = row[headers.index('artist_flattr_name')]
                            artist_date_created = row[headers.index('artist_date_created')]
                            artist_image_file = row[headers.index('artist_image_file')]
                            insert_query = f"INSERT INTO {table_name[i]} ({table_attributes[i]}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(insert_query, (artist_id, artist_name, artist_location, artist_latitude, artist_longitude, artist_favorites, artist_comments, artist_active_year_begin, artist_active_year_end, artist_url, artist_website, artist_wikipedia_page, artist_handle, artist_bio, artist_members, artist_associated_labels, artist_related_projects, artist_contact, artist_donation_url, artist_paypal_name, artist_flattr_name, artist_date_created, artist_image_file))
                
                case 'sae5_6.import_track':
                    if headers:
                        for row in reader:
                            track_id = row[headers.index('track_id')]
                            track_title = row[headers.index('track_title')]
                            track_duration = row[headers.index('track_duration')]
                            track_date_created = row[headers.index('track_date_created')]
                            track_date_recorded = row[headers.index('track_date_recorded')]
                            track_composer = row[headers.index('track_composer')]
                            track_lyricist = row[headers.index('track_lyricist')]
                            track_publisher = row[headers.index('track_publisher')]
                            track_listens = row[headers.index('track_listens')]
                            track_favorites = row[headers.index('track_favorites')]
                            track_comments = row[headers.index('track_comments')]
                            track_interest = row[headers.index('track_interest')]
                            track_copyright_c = row[headers.index('track_copyright_c')]
                            track_copyright_p = row[headers.index('track_copyright_p')]
                            track_explicit = row[headers.index('track_explicit')]
                            track_explicit_note = row[headers.index('track_explicit_notes')]
                            track_instrumental = row[headers.index('track_instrumental')]
                            track_language_code = row[headers.index('track_language_code')]
                            track_url = row[headers.index('track_url')]
                            track_file = row[headers.index('track_file')]
                            track_image_file = row[headers.index('track_image_file')]
                            insert_query = f"INSERT INTO {table_name[i]} ({table_attributes[i]}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(insert_query, (track_id, track_title, track_duration, track_date_created, track_date_recorded, track_composer, track_lyricist, track_publisher, track_listens, track_favorites, track_comments, track_interest, track_copyright_c, track_copyright_p, track_explicit, track_explicit_note, track_instrumental, track_language_code, track_url, track_file, track_image_file))
                    
                case 'sae5_6.import_echonest':
                    if headers:
                        for row in reader:
                            track_id = row[headers.index('track_id')]
                            acousticness = row[headers.index('echonest_audio_features_acousticness')]
                            energy = row[headers.index('echonest_audio_features_energy')]
                            instrumentalness = row[headers.index('echonest_audio_features_instrumentalness')]
                            liveness = row[headers.index('echonest_audio_features_liveness')]
                            speechiness = row[headers.index('echonest_audio_features_speechiness')]
                            valence = row[headers.index('echonest_audio_features_valence')]
                            danceability = row[headers.index('echonest_audio_features_danceability')]
                            tempo = row[headers.index('echonest_audio_features_tempo')]
                            artist_discovery = row[headers.index('echonest_social_features_artist_discovery')]
                            artist_hottness = row[headers.index('echonest_social_features_artist_hotttnesss')]
                            artist_familiarity = row[headers.index('echonest_social_features_artist_familiarity')]
                            track_hottness = row[headers.index('echonest_social_features_song_hotttnesss')]
                            track_currency = row[headers.index('echonest_social_features_song_currency')]
                            insert_query = f"INSERT INTO {table_name[i]} ({table_attributes[i]}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(insert_query, (track_id, acousticness, energy, instrumentalness, liveness, speechiness, valence, danceability, tempo, artist_discovery, artist_hottness, artist_familiarity, track_hottness, track_currency))
                    
                case 'sae5_6.import_genre':
                    if headers:
                        for row in reader:
                            genre_id = row[headers.index('genre_id')]
                            genre_parent_id = row[headers.index('genre_parent_id')]
                            genre_title = row[headers.index('genre_title')]
                            genre_handle = row[headers.index('genre_handle')]
                            genre_color = row[headers.index('genre_color')]
                            top_level = True if row[headers.index('genre_parent_id')] == '' else False
                            insert_query = f"INSERT INTO {table_name[i]} ({table_attributes[i]}) VALUES (%s, %s, %s, %s, %s, %s)"
                            cursor.execute(insert_query, (genre_id, genre_parent_id, genre_title, genre_handle, genre_color, top_level))
                    
                case 'sae5_6.import_album':
                    if headers:
                        for row in reader:
                            album_id = row[headers.index('album_id')]
                            album_title = row[headers.index('album_title')]
                            album_date_release = row[headers.index('album_date_released')]
                            album_date_created = row[headers.index('album_date_created')]
                            album_listens = row[headers.index('album_listens')]
                            album_favorites = row[headers.index('album_favorites')]
                            album_comments = row[headers.index('album_comments')]
                            album_type = row[headers.index('album_type')]
                            album_url = row[headers.index('album_url')]
                            album_handle = row[headers.index('album_handle')]
                            album_information = row[headers.index('album_information')]
                            album_tracks = row[headers.index('album_tracks')]
                            album_producer = row[headers.index('album_producer')]
                            album_engineer = row[headers.index('album_engineer')]
                            insert_query = f"INSERT INTO {table_name[i]} ({table_attributes[i]}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(insert_query, (album_id, album_title, album_date_release, album_date_created, album_listens, album_favorites, album_comments, album_type, album_url, album_handle, album_information, album_tracks, album_producer, album_engineer))
                
                case 'sae5_6.import_license':
                    license_id_counter = 1
                    license_id_map = {}
                    if headers:
                        for row in reader:
                            license_title = row[headers.index('license_title')]
                            license_url = row[headers.index('license_url')]
                            if license_title not in license_id_map:
                                license_id_map[license_title] = license_id_counter
                                insert_query = f"INSERT INTO {table_name[i]} ({table_attributes[i]}) VALUES (%s, %s, %s)"
                                cursor.execute(insert_query, (license_id_counter, license_title, license_url))
                                license_id_counter += 1
                case 'sae5_6.import_language':
                    country_code_list = []
                    if headers:
                        for row in reader:
                            language_code = row[headers.index('track_language_code')]
                            if language_code not in country_code_list:
                                country_code_list.append(language_code)
                                language_name = process_language_code(language_code)
                                language_handle = language_name.lower().replace(" ", "_")
                                insert_query = f"INSERT INTO {table_name[i]} ({table_attributes[i]}) VALUES (%s, %s, %s)"
                                cursor.execute(insert_query, (language_code, language_name, language_handle))
                case _:
                    print("No matching table found.")
                    
            
            
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data imported into {table_name} from {csv_file_path}")

if __name__ == "__main__":
    csvs = ['raw_artists', 'raw_tracks', 'clean_echonest', 'raw_genres', 'raw_albums']
    for csv_file in csvs:
        import_csv_to_db(csv_file)