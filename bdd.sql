DROP SCHEMA IF EXISTS sae5_6 CASCADE;
CREATE SCHEMA sae5_6;

CREATE TABLE sae5_6.image (
    image_id SERIAL PRIMARY KEY,
    image_url VARCHAR(255) NOT NULL,
    image_name VARCHAR(100)
);

CREATE TABLE sae5_6.user (
    user_id SERIAL PRIMARY KEY,
    user_age_range VARCHAR(50),
    user_job VARCHAR(100),
    user_explicit_content BOOLEAN DEFAULT FALSE,
    user_track_duration_range VARCHAR(50),
    user_time_listening_day VARCHAR(50),
    user_pseudo VARCHAR(100) NOT NULL,
    user_password TEXT NOT NULL
);

CREATE TABLE sae5_6.user_profile (
    profile_id SERIAL PRIMARY KEY,
    instrument_name VARCHAR(100) NOT NULL,
    mood_label VARCHAR(100) NOT NULL,
    envy_label VARCHAR(100) NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES sae5_6.user(user_id)
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
    FOREIGN KEY (user_preference_echonest_id) REFERENCES sae5_6.user(user_id)
);

CREATE TABLE sae5_6.user_preference_artist (
    user_preference_artist_id SERIAL PRIMARY KEY,
    artist_id INT REFERENCES sae5_6.artist(artist_id),
    FOREIGN KEY (user_preference_artist_id) REFERENCES sae5_6.user(user_id)
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
    track_image_file VARCHAR(255)
);

CREATE TABLE sae5_6.license (
    license_id SERIAL PRIMARY KEY,
    license_title VARCHAR(100) NOT NULL,
    license_url VARCHAR(255),
    parent_id INT
);
    
CREATE TABLE sae5_6.genre (
    genre_id SERIAL PRIMARY KEY,
    genre_parent_id INT,
    genre_title VARCHAR(100) NOT NULL,
    genre_handle VARCHAR(100),
    genre_color VARCHAR(10),
    top_level BOOLEAN DEFAULT TRUE
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

CREATE TABLE sae5_6.echonest (
    echonest_id SERIAL PRIMARY KEY,
    acousticness FLOAT,
    energy FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    speechiness FLOAT,
    valence FLOAT,
    danceability FLOAT,
    tempo FLOAT
);

CREATE TABLE sae5_6.tag (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(100) NOT NULL
)

CREATE TABLE sae5_6.language (
    language_id SERIAL PRIMARY KEY,
    language_label VARCHAR(100) NOT NULL,
    language_handle VARCHAR(50)
);

CREATE TABLE sae5_6.playlist (
    playlist_id SERIAL PRIMARY KEY,
    playlist_name VARCHAR(255) NOT NULL
);

-- Relation Tables

CREATE TABLE sae5_6.track_echonest (
    track_id INT REFERENCES sae5_6.track(track_id),
    echonest_id INT REFERENCES sae5_6.echonest(echonest_id),
    PRIMARY KEY (track_id, echonest_id)
);

CREATE TABLE sae5_6.playlist_contient_track (
    playlist_id INT REFERENCES sae5_6.playlist(playlist_id),
    track_id INT REFERENCES sae5_6.track(track_id),
    PRIMARY KEY (playlist_id, track_id)
);

CREATE TABLE sae5_6.user_playlist (
    user_id INT REFERENCES sae5_6.users(user_id),
    playlist_id INT REFERENCES sae5_6.playlist(playlist_id),
    PRIMARY KEY (user_id, playlist_id)
);

CREATE TABLE sae5_6.user_envy (
    user_id INT REFERENCES sae5_6.users(user_id),
    envy_id INT REFERENCES sae5_6.envy(envy_id),
    PRIMARY KEY (user_id, envy_id)
);

CREATE TABLE sae5_6.user_mood (
    user_id INT REFERENCES sae5_6.users(user_id),
    mood_id INT REFERENCES sae5_6.mood(mood_id),
    PRIMARY KEY (user_id, mood_id)
);

CREATE TABLE sae5_6.user_instrument (
    user_id INT REFERENCES sae5_6.users(user_id),
    instrument_id INT REFERENCES sae5_6.instrument(instrument_id),
    PRIMARY KEY (user_id, instrument_id)
);

CREATE TABLE sae5_6.user_language (
    user_id INT REFERENCES sae5_6.users(user_id),
    language_id INT REFERENCES sae5_6.language(language_id),
    PRIMARY KEY (user_id, language_id)
);

CREATE TABLE sae5_6.artist_image (
    artist_id INT REFERENCES sae5_6.artist(artist_id),
    image_id INT REFERENCES sae5_6.image(image_id),
    PRIMARY KEY (artist_id, image_id)
);

CREATE TABLE sae5_6.artist_tag (
    artist_id INT REFERENCES sae5_6.artist(artist_id),
    tag_id INT REFERENCES sae5_6.tag(tag_id),
    PRIMARY KEY (artist_id, tag_id)
);

CREATE TABLE sae5_6.artist_language (
    artist_id INT REFERENCES sae5_6.artist(artist_id),
    language_id INT REFERENCES sae5_6.language(language_id),
    PRIMARY KEY (artist_id, language_id)
);

CREATE TABLE sae5_6.album_image (
    album_id INT REFERENCES sae5_6.album(album_id),
    image_id INT REFERENCES sae5_6.image(image_id),
    PRIMARY KEY (album_id, image_id)
);

CREATE TABLE sae5_6.album_tag (
    album_id INT REFERENCES sae5_6.album(album_id),
    tag_id INT REFERENCES sae5_6.tag(tag_id),
    PRIMARY KEY (album_id, tag_id)
);

CREATE TABLE sae5_6.track_license (
    track_id INT REFERENCES sae5_6.track(track_id),
    license_id INT REFERENCES sae5_6.license(license_id),
    PRIMARY KEY (track_id, license_id)
);

CREATE TABLE sae5_6.track_language (
    track_id INT REFERENCES sae5_6.track(track_id),
    language_id INT REFERENCES sae5_6.language(language_id),
    PRIMARY KEY (track_id, language_id)
);

CREATE TABLE sae5_6.genre_tag (
    genre_id INT REFERENCES sae5_6.genre(genre_id),
    tag_id INT REFERENCES sae5_6.tag(tag_id),
    PRIMARY KEY (genre_id, tag_id)
);

CREATE TABLE sae5_6.album_track_genre_artist (
    album_id INT REFERENCES sae5_6.album(album_id),
    track_id INT REFERENCES sae5_6.track(track_id),
    genre_id INT REFERENCES sae5_6.genre(genre_id),
    artist_id INT REFERENCES sae5_6.artist(artist_id),
    PRIMARY KEY (album_id, track_id, genre_id, artist_id)
);

CREATE TABLE sae5_6.user_artist_pref_user (
    user_preference_artist_id INT REFERENCES sae5_6.user_preference_artist(user_preference_artist_id),
    user_id INT REFERENCES sae5_6.user(user_id),
    PRIMARY KEY (user_preference_artist_id, user_id)
);