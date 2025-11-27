DROP SCHEMA IF EXISTS sae5_6 CASCADE;
CREATE SCHEMA sae5_6;

CREATE TABLE sae5_6.image (
    image_id SERIAL PRIMARY KEY,
    image_url VARCHAR(255) NOT NULL,
    image_name VARCHAR(100)
);

CREATE TABLE sae5_6.user_profile (
    user_profile_id SERIAL PRIMARY KEY,
    music_envy_today TEXT NOT NULL
    feeling INT NOT NULL,
    music_preference INT NOT NULL,
    music_style_preference INT NOT NULL,
    music_reason TEXT NOT NULL,
    listening_context TEXT NOT NULL,
    current_music_type INT,
    usual_listening_mode INT NOT NULL,
    likes_discovery INT NOT NULL,
    attend_live_concert INT NOT NULL,
    repeat_listening INT NOT NULL,
    explicit_ok INT NOT NULL,
    avg_song_length FLOAT NOT NULL,
    avg_daily_listen_time FLOAT NOT NULL,
    recommanded_artists TEXT    
);

CREATE TABLE sae5_6.user (
    user_id SERIAL PRIMARY KEY,
    user_age FLOAT NOT NULL,
    user_job VARCHAR(100),
    user_plays_music BOOLEAN DEFAULT FALSE,
    user_pseudo VARCHAR(100) NOT NULL,
    user_password TEXT NOT NULL,
    user_gender VARCHAR(100),
    user_instruments TEXT,
    user_music_contexts FLOAT,
    profile_id INT NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES sae5_6.user_profile(profile_id)
);

-- Recalcule avec trigger moyenne des musiques d'une playlist ou des playlist
CREATE TABLE sae5_6.user_preference_echonest (
    user_preference_echonest_id SERIAL PRIMARY KEY,
    acousticness FLOAT,
    energy FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    speechiness FLOAT,
    valence FLOAT,
    danceability FLOAT,
    tempo FLOAT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES sae5_6.user(user_id)
);

CREATE TABLE sae5_6.album (
    album_id SERIAL PRIMARY KEY,
    album_title VARCHAR(255) NOT NULL,
    album_date_release DATE,
    album_date_created DATE,
    album_listens INT DEFAULT 0,
    album_favorites INT DEFAULT 0,
    album_comments INT DEFAULT 0,
    album_type VARCHAR(50),
    album_url VARCHAR(255),
    album_handle VARCHAR(100),
    album_information TEXT,
    album_tracks INT DEFAULT 0,
    album_producer VARCHAR(255),
    album_engineer VARCHAR(255)
);

CREATE TABLE sae5_6.genre (
    genre_id SERIAL PRIMARY KEY,
    genre_parent_id INT,
    genre_title VARCHAR(100) NOT NULL,
    genre_handle VARCHAR(100),
    genre_color VARCHAR(10),
    top_level BOOLEAN DEFAULT TRUE
);

CREATE TABLE sae5_6.track (
    track_id SERIAL PRIMARY KEY,
    track_title VARCHAR(255) NOT NULL,
    track_duration INT,
    track_date_created DATE,
    track_date_recorded DATE,
    track_composer VARCHAR(255),
    track_lyricist VARCHAR(255),
    track_publisher VARCHAR(255),
    track_listens INT DEFAULT 0,
    track_favorites INT DEFAULT 0,
    track_comments INT DEFAULT 0,
    track_interest INT DEFAULT 0,
    track_copyright_c VARCHAR(255),
    track_copyright_p VARCHAR(255),
    track_explicit BOOLEAN DEFAULT FALSE,
    track_explicit_note TEXT,
    track_instrumental BOOLEAN DEFAULT FALSE,
    track_language_code VARCHAR(10),
    track_url VARCHAR(255),
    track_file VARCHAR(255),
    track_image_file VARCHAR(255),
    genre_id INT NOT NULL,
    FOREIGN KEY (genre_id) REFERENCES sae5_6.genre(genre_id)
);

CREATE TABLE sae5_6.track_echonest (
    track_echonest_id SERIAL PRIMARY KEY,
    acousticness FLOAT,
    energy FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    speechiness FLOAT,
    valence FLOAT,
    danceability FLOAT,
    tempo FLOAT, 
    artist_discovery FLOAT,
    artist_hottness FLOAT,
    artist_familiarity FLOAT,
    track_hottness FLOAT,
    track_currency FLOAT,
    track_id INT NOT NULL,
    FOREIGN KEY (track_id) REFERENCES sae5_6.track(track_id)
);

CREATE TABLE sae5_6.license (
    license_id SERIAL PRIMARY KEY,
    license_title VARCHAR(100) NOT NULL,
    license_url VARCHAR(255),
    parent_id INT,
    track_id INT NOT NULL,
    FOREIGN KEY (track_id) REFERENCES sae5_6.track(track_id),
    FOREIGN KEY (parent_id) REFERENCES sae5_6.license(license_id)
);

CREATE TABLE sae5_6.artist (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    artist_location VARCHAR(255),
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_favorites INT DEFAULT 0,
    artist_comments INT DEFAULT 0,
    artist_listens INT DEFAULT 0,
    artist_active_year_begin INT,
    artist_active_year_end INT,
    artist_url VARCHAR(255),
    artist_website VARCHAR(255),
    artist_wikipedia_page VARCHAR(255),
    artist_handle VARCHAR(100),
    artist_bio TEXT,
    artist_members TEXT,
    artist_associated_labels TEXT,
    artist_related_projects TEXT,
    artist_contact TEXT,
    artist_donation_url VARCHAR(255),
    artist_paypal_name VARCHAR(100),
    artist_flattr_name VARCHAR(100),
    artist_date_created DATE,
    artist_image_file VARCHAR(255)
);

CREATE TABLE sae5_6.language (
    language_id SERIAL PRIMARY KEY,
    language_label VARCHAR(100) NOT NULL,
    language_handle VARCHAR(50)
);

CREATE TABLE sae5_6.playlist (
    playlist_id SERIAL PRIMARY KEY,
    playlist_name VARCHAR(255) NOT NULL,
    track_id INT,
    FOREIGN KEY (track_id) REFERENCES sae5_6.track(track_id)
);

-- Relation Tables

CREATE TABLE sae5_6.quantifie (
    track_id INT NOT NULL REFERENCES sae5_6.track(track_id),
    echonest_id INT NOT NULL REFERENCES sae5_6.track_echonest(track_echonest_id),
    PRIMARY KEY (track_id, echonest_id)
);

CREATE TABLE sae5_6.playlist_contient_track (
    playlist_id INT REFERENCES sae5_6.playlist(playlist_id),
    track_id INT REFERENCES sae5_6.track(track_id),
    PRIMARY KEY (playlist_id, track_id)
);

CREATE TABLE sae5_6.possede_playlist (
    user_id INT REFERENCES sae5_6.user(user_id),
    playlist_id INT REFERENCES sae5_6.playlist(playlist_id),
    PRIMARY KEY (user_id, playlist_id)
);

CREATE TABLE sae5_6.represente (
    user_id INT REFERENCES sae5_6.user(user_id),
    user_preference_echonest_id INT REFERENCES sae5_6.user_preference_echonest(user_preference_echonest_id),
    PRIMARY KEY (user_id, user_preference_echonest_id)
);

CREATE TABLE sae5_6.user_parle (
    user_id INT REFERENCES sae5_6.user(user_id),
    language_id INT REFERENCES sae5_6.language(language_id),
    PRIMARY KEY (user_id, language_id)
);

CREATE TABLE sae5_6.provient_artist (
    artist_id INT NOT NULL REFERENCES sae5_6.artist(artist_id),
    image_id INT NOT NULL REFERENCES sae5_6.image(image_id),
    PRIMARY KEY (artist_id, image_id)
);

CREATE TABLE sae5_6.artiste_chante (
    artist_id INT REFERENCES sae5_6.artist(artist_id),
    language_id INT REFERENCES sae5_6.language(language_id),
    PRIMARY KEY (artist_id, language_id)
);

CREATE TABLE sae5_6.provient_album (
    album_id INT NOT NULL REFERENCES sae5_6.album(album_id),
    image_id INT NOT NULL REFERENCES sae5_6.image(image_id),
    PRIMARY KEY (album_id, image_id)
);

CREATE TABLE sae5_6.provient_license (
    license_id INT NOT NULL REFERENCES sae5_6.license(license_id),
    image_id INT NOT NULL REFERENCES sae5_6.image(image_id),
    PRIMARY KEY (license_id, image_id)
);

CREATE TABLE sae5_6.track_chanter_en (
    track_id INT REFERENCES sae5_6.track(track_id),
    language_id INT REFERENCES sae5_6.language(language_id),
    PRIMARY KEY (track_id, language_id)
);

CREATE TABLE sae5_6.realiser (
    album_id INT NOT NULL REFERENCES sae5_6.album(album_id),
    track_id INT REFERENCES sae5_6.track(track_id),
    artist_id INT NOT NULL REFERENCES sae5_6.artist(artist_id),
    PRIMARY KEY (album_id, track_id, artist_id)
);

CREATE TABLE sae5_6.user_prefere_artiste (
    artist_id INT REFERENCES sae5_6.artist(artist_id),
    user_id INT REFERENCES sae5_6.user(user_id),
    PRIMARY KEY (artist_id, user_id)
);

CREATE TABLE sae5_6.contient_genres (
    track_id INT REFERENCES sae5_6.track(track_id),
    genre_id INT REFERENCES sae5_6.genre(genre_id),
    PRIMARY KEY (track_id, genre_id)
);

CREATE TABLE sae5_6.supervise(
    parent_id INT REFERENCES sae5_6.genre(genre_id),
    child_id INT REFERENCES sae5_6.genre(genre_id),
    PRIMARY KEY (parent_id, child_id)
);

CREATE TABLE sae5_6.ajoute_favori (
    user_id INT REFERENCES sae5_6.user(user_id),
    track_id INT REFERENCES sae5_6.track(track_id),
    PRIMARY KEY (user_id, track_id)
);

