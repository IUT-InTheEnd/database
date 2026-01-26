-- Tables d'import pour charger les CSV présents dans le dossier `dataset/`.
-- Chaque table contient les colonnes provenant des fichiers "clean_*.csv"
-- ainsi que des colonnes de métadonnées pour tracer l'importation.

DROP TABLE IF EXISTS import_artist;
DROP TABLE IF EXISTS import_album;
DROP TABLE IF EXISTS import_track;
DROP TABLE IF EXISTS import_genre;
DROP TABLE IF EXISTS import_echonest;
DROP TABLE IF EXISTS import_license;
DROP TABLE IF EXISTS import_language;
DROP TABLE IF EXISTS import_track_genre;

CREATE TABLE IF NOT EXISTS import_artist (
    artist_id TEXT,
    artist_name TEXT,
    artist_location TEXT,
    artist_latitude TEXT,
    artist_longitude TEXT,
    artist_favorites TEXT,
    artist_comments TEXT,
    artist_listens TEXT,
    artist_active_year_begin TEXT,
    artist_active_year_end TEXT,
    artist_url TEXT,
    artist_website TEXT,
    artist_wikipedia_page TEXT,
    artist_handle VARCHAR(100),
    artist_bio TEXT,
    artist_members TEXT,
    artist_associated_labels TEXT,
    artist_related_projects TEXT,
    artist_contact TEXT,
    artist_donation_url TEXT,
    artist_paypal_name TEXT,
    artist_flattr_name TEXT,
    artist_date_created TEXT,
    artist_image_file TEXT
);

CREATE TABLE IF NOT EXISTS import_album (
	album_id TEXT,
	album_title TEXT,
	album_date_release TEXT,
	album_date_created TEXT,
	album_listens TEXT,
	album_favorites TEXT,
	album_comments TEXT,
	album_type TEXT,
	album_url TEXT,
	album_handle TEXT,
	album_information TEXT,
	album_tracks TEXT,
	album_producer TEXT,
	album_engineer TEXT,
	album_image_file TEXT
);

CREATE TABLE IF NOT EXISTS import_track (
    track_id TEXT,
    track_title TEXT,
    track_duration TEXT,
    track_date_created TEXT,
    track_date_recorded TEXT,
    track_composer TEXT,
    track_lyricist TEXT,
    track_publisher TEXT,
    track_listens TEXT,
    track_favorites TEXT,
    track_comments TEXT,
    track_interest TEXT,
    track_copyright_c TEXT,
    track_copyright_p TEXT,
    track_explicit TEXT,
    track_explicit_note TEXT,
    track_instrumental TEXT,
    track_language_code TEXT,
    track_url TEXT,
    track_file TEXT,
    track_image_file TEXT,
    license_id TEXT,
    artist_id TEXT,
    album_id TEXT,
    language_id TEXT
);

CREATE TABLE IF NOT EXISTS import_genre (
	genre_id TEXT,
	genre_parent_id TEXT,
	genre_title TEXT,
	genre_handle TEXT,
	genre_color TEXT,
	top_level TEXT
);

CREATE TABLE IF NOT EXISTS import_echonest (
	track_id TEXT,
	acousticness TEXT,
	energy TEXT,
	instrumentalness TEXT,
	liveness TEXT,
	speechiness TEXT,
	valence TEXT,
	danceability TEXT,
	tempo TEXT,
	artist_discovery TEXT,
	artist_hottness TEXT,
	artist_familiarity TEXT,
	track_hottness TEXT,
	track_currency TEXT
);

CREATE TABLE IF NOT EXISTS import_license (
	license_id TEXT,
	license_title TEXT,
	license_url TEXT
);

CREATE TABLE IF NOT EXISTS import_language (
    language_id TEXT,
	language_code TEXT,
	language_name TEXT,
	language_handle TEXT
);

CREATE TABLE IF NOT EXISTS import_track_genre (
    track_id TEXT,
    genre_id TEXT
);
