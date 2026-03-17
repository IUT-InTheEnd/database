drop schema public cascade;
create schema public;
set schema 'public';

CREATE TABLE user_profile (
    user_profile_id SERIAL PRIMARY KEY,
    music_envy_today TEXT NOT NULL,
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

CREATE TABLE "user" (
    -- Laravel colonnes obligatoires
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified_at TIMESTAMP NULL,
    password VARCHAR(255) NOT NULL,
    remember_token VARCHAR(100) NULL,
    two_factor_secret TEXT NULL,
    two_factor_recovery_codes TEXT NULL,
    two_factor_confirmed_at TIMESTAMP NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Colonnes personnalisées
    user_image_file VARCHAR(512),
    user_age FLOAT,
    user_job VARCHAR(100),
    user_plays_music TEXT,
    user_gender VARCHAR(100),
    user_instruments TEXT,
    user_music_contexts TEXT,
    profile_id INT,
    FOREIGN KEY (profile_id) REFERENCES user_profile(user_profile_id)
);

CREATE TABLE user_privacy (
    id INT,
    public_profile_visibility BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id) REFERENCES "user"(id)
);

-- Recalcule avec trigger moyenne des musiques d'une playlist ou des playlist
CREATE TABLE user_preference_echonest (
    user_id BIGINT PRIMARY KEY,
    acousticness FLOAT,
    energy FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    speechiness FLOAT,
    valence FLOAT,
    danceability FLOAT,
    tempo FLOAT,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE TABLE album (
    album_id SERIAL PRIMARY KEY,
    album_title VARCHAR(255) NOT NULL,
    album_date_release DATE,
    album_date_created DATE,
    album_listens INT DEFAULT 0,
    album_favorites INT DEFAULT 0,
    album_likes INT DEFAULT 0,
    album_dislikes INT DEFAULT 0,
    album_comments INT DEFAULT 0,
    album_type VARCHAR(50),
    album_url VARCHAR(512),
    album_handle VARCHAR(100),
    album_information TEXT,
    album_tracks INT DEFAULT 0,
    album_producer VARCHAR(510),
    album_engineer VARCHAR(510),
    album_image_file VARCHAR(512)
);

CREATE TABLE genre (
    genre_id SERIAL PRIMARY KEY,
    genre_parent_id INT,
    genre_title VARCHAR(100) NOT NULL,
    genre_handle VARCHAR(100),
    genre_color VARCHAR(10),
    top_level BOOLEAN DEFAULT TRUE
);

CREATE TABLE license (
    license_id SERIAL PRIMARY KEY,
    license_title VARCHAR(100),
    license_url VARCHAR(512)
);

CREATE TABLE track (
    track_id SERIAL PRIMARY KEY,
    track_title VARCHAR(255),
    track_duration INT,
    track_date_created DATE,
    track_date_recorded DATE,
    track_composer VARCHAR(255),
    track_lyricist VARCHAR(255),
    track_publisher VARCHAR(255),
    track_listens INT DEFAULT 0,
    track_favorites INT DEFAULT 0,
    track_likes INT DEFAULT 0,
    track_dislikes INT DEFAULT 0,
    track_comments INT DEFAULT 0,
    track_interest INT DEFAULT 0,
    track_copyright_c VARCHAR(255),
    track_copyright_p VARCHAR(255),
    track_explicit BOOLEAN DEFAULT FALSE,
    track_explicit_note TEXT,
    track_instrumental BOOLEAN DEFAULT FALSE,
    track_language_code VARCHAR(10),
    track_url VARCHAR(1023),
    track_file VARCHAR(512),
    track_image_file VARCHAR(512),
    license_id INT,
    FOREIGN KEY (license_id) REFERENCES license(license_id)
);

CREATE TABLE track_echonest (
    track_id SERIAL PRIMARY KEY,
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
    FOREIGN KEY (track_id) REFERENCES track(track_id)
);

CREATE TABLE artist (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    artist_location VARCHAR(511),
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_favorites INT DEFAULT 0,
    artist_comments INT DEFAULT 0,
    artist_listens INT DEFAULT 0,
    artist_active_year_begin INT,
    artist_active_year_end INT,
    artist_url VARCHAR(512),
    artist_website VARCHAR(512),
    artist_wikipedia_page VARCHAR(512),
    artist_handle VARCHAR(100),
    artist_bio TEXT,
    artist_members TEXT,
    artist_associated_labels TEXT,
    artist_related_projects TEXT,
    artist_contact TEXT,
    artist_donation_url VARCHAR(512),
    artist_paypal_name VARCHAR(100),
    artist_flattr_name VARCHAR(100),
    artist_date_created DATE,
    artist_image_file VARCHAR(512)
);

CREATE TABLE language (
    language_id SERIAL PRIMARY KEY,
    language_label VARCHAR(100) NOT NULL,
    language_handle VARCHAR(50)
);

CREATE TABLE playlist (
    user_id BIGINT REFERENCES "user"(id),
    playlist_id SERIAL PRIMARY KEY,
    playlist_name VARCHAR(255) NOT NULL,
    playlist_description TEXT,
    playlist_date_created DATE,
    playlist_date_updated DATE,
    playlist_listens INT DEFAULT 0,
    playlist_favorites INT DEFAULT 0,
    playlist_public BOOLEAN DEFAULT TRUE,
    playlist_image_file VARCHAR(512),
    playlist_deletable BOOLEAN DEFAULT TRUE
);

-- Relation Tables

CREATE TABLE playlist_contient_track (
    playlist_id INT REFERENCES playlist(playlist_id),
    track_id INT REFERENCES track(track_id),
    PRIMARY KEY (playlist_id, track_id)
);

CREATE TABLE represente (
    user_id BIGINT REFERENCES "user"(id),
    user_id_echonest BIGINT REFERENCES user_preference_echonest(user_id),
    PRIMARY KEY (user_id, user_id_echonest)
);

CREATE TABLE user_parle (
    user_id BIGINT REFERENCES "user"(id),
    language_id INT REFERENCES language(language_id),
    PRIMARY KEY (user_id, language_id)
);

CREATE TABLE artiste_chante (
    artist_id INT REFERENCES artist(artist_id),
    language_id INT REFERENCES language(language_id),
    PRIMARY KEY (artist_id, language_id)
);

CREATE TABLE track_chanter_en (
    track_id INT REFERENCES track(track_id),
    language_id INT REFERENCES language(language_id),
    PRIMARY KEY (track_id, language_id)
);

CREATE TABLE realiser (
    album_id INT NOT NULL REFERENCES album(album_id),
    track_id INT REFERENCES track(track_id),
    artist_id INT NOT NULL REFERENCES artist(artist_id),
    PRIMARY KEY (album_id, track_id, artist_id)
);

CREATE TABLE user_prefere_artiste (
    artist_id INT REFERENCES artist(artist_id),
    user_id BIGINT REFERENCES "user"(id),
    PRIMARY KEY (artist_id, user_id)
);

CREATE TABLE contient_genres (
    track_id INT REFERENCES track(track_id),
    genre_id INT REFERENCES genre(genre_id),
    PRIMARY KEY (track_id, genre_id)
);

CREATE TABLE supervise(
    parent_id INT REFERENCES genre(genre_id),
    child_id INT REFERENCES genre(genre_id),
    PRIMARY KEY (parent_id, child_id)
);

CREATE TABLE ajoute_favori (
    user_id BIGINT REFERENCES "user"(id),
    track_id INT REFERENCES track(track_id),
    PRIMARY KEY (user_id, track_id)
);

CREATE TABLE ajoute_genre_favoris (
    user_id BIGINT REFERENCES "user"(id),
    genre_id INT REFERENCES genre(genre_id),
    PRIMARY KEY (user_id, genre_id)
);

CREATE TABLE user_ajoute_album_favoris (
    user_id BIGINT REFERENCES "user"(id),
    album_id INT REFERENCES album(album_id),
    PRIMARY KEY (user_id, album_id)
);

CREATE TABLE track_reaction (
    reaction_id SERIAL PRIMARY KEY,
    track_id INT NOT NULL REFERENCES track(track_id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES "user"(id) ON DELETE CASCADE,
    visitor_id UUID,
    reaction VARCHAR(16) NOT NULL CHECK (reaction IN ('like', 'dislike')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (((user_id IS NOT NULL)::INT + (visitor_id IS NOT NULL)::INT) = 1)
);

CREATE UNIQUE INDEX track_reaction_track_user_unique
    ON track_reaction (track_id, user_id)
    WHERE user_id IS NOT NULL;

CREATE UNIQUE INDEX track_reaction_track_visitor_unique
    ON track_reaction (track_id, visitor_id)
    WHERE visitor_id IS NOT NULL;

CREATE TABLE album_reaction (
    reaction_id SERIAL PRIMARY KEY,
    album_id INT NOT NULL REFERENCES album(album_id) ON DELETE CASCADE,
    user_id BIGINT REFERENCES "user"(id) ON DELETE CASCADE,
    visitor_id UUID,
    reaction VARCHAR(16) NOT NULL CHECK (reaction IN ('like', 'dislike')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (((user_id IS NOT NULL)::INT + (visitor_id IS NOT NULL)::INT) = 1)
);

CREATE UNIQUE INDEX album_reaction_album_user_unique
    ON album_reaction (album_id, user_id)
    WHERE user_id IS NOT NULL;

CREATE UNIQUE INDEX album_reaction_album_visitor_unique
    ON album_reaction (album_id, visitor_id)
    WHERE visitor_id IS NOT NULL;

CREATE TABLE user_ecoute (
    user_id BIGINT REFERENCES "user"(id),
    track_id INT REFERENCES track(track_id),
    nb_ecoute INT DEFAULT 0,
    last_listen DATE,
    PRIMARY KEY (user_id, track_id)
);

CREATE TABLE personal_access_tokens (
    id BIGSERIAL PRIMARY KEY,
    tokenable_type VARCHAR(255) NOT NULL,
    tokenable_id BIGINT NOT NULL,
    name TEXT NOT NULL,
    token VARCHAR(64) NOT NULL UNIQUE,
    abilities TEXT,
    last_used_at TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    expires_at TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    created_at TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    updated_at TIMESTAMP(0) WITHOUT TIME ZONE NULL
);

CREATE INDEX personal_access_tokens_tokenable_type_tokenable_id_index
ON personal_access_tokens (tokenable_type, tokenable_id);

CREATE INDEX personal_access_tokens_expires_at_index
ON personal_access_tokens (expires_at);
