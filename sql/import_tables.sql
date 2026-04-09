INSERT INTO role (nom) VALUES ('admin'), ('user');

INSERT
	INTO
	artist (artist_id,artist_name,artist_location,artist_latitude,artist_longitude,artist_favorites,artist_comments,artist_listens,artist_active_year_begin,artist_active_year_end,artist_url,artist_website,artist_wikipedia_page,artist_handle,artist_bio,artist_members,artist_associated_labels,artist_related_projects,artist_contact,artist_donation_url,artist_paypal_name,artist_flattr_name,artist_date_created,artist_image_file)
SELECT
	artist_id::int,
	artist_name,
	artist_location,
	CASE
		WHEN artist_latitude = '' THEN NULL
		ELSE artist_latitude::float
	END AS artist_latitude,
	CASE
		WHEN artist_longitude = '' THEN NULL
		ELSE artist_longitude::float
	END AS artist_longitude,
	COALESCE(NULLIF(artist_favorites, ''), '0')::int,
	COALESCE(NULLIF(artist_comments, ''), '0')::int,
	COALESCE(NULLIF(artist_listens, ''), '0')::int AS artist_listens,
	CASE
		WHEN artist_active_year_begin = '' THEN NULL
		ELSE artist_active_year_begin::int
	END AS artist_active_year_begin,
	CASE
		WHEN artist_active_year_end = '' THEN NULL
		ELSE artist_active_year_end::int
	END AS artist_active_year_end,
	artist_url,
	artist_website,
	artist_wikipedia_page,
	artist_handle,
	artist_bio,
	artist_members,
	artist_associated_labels,
	artist_related_projects,
	artist_contact,
	artist_donation_url ,
	artist_paypal_name ,
	artist_flattr_name ,
	TO_DATE(artist_date_created, 'DD-MM-YYYY') AS artist_date_created,
	artist_image_file
FROM
	import_artist;


INSERT
	INTO
	album (album_id,album_title,album_date_release,album_date_created,album_listens,album_favorites,album_comments,album_type,album_url,album_handle,album_information,album_tracks,album_producer,album_engineer,album_image_file)
SELECT
	album_id::int,
	album_title,
	TO_DATE(album_date_release, 'DD-MM-YYYY') AS album_date_release,
	TO_DATE(album_date_created, 'DD-MM-YYYY') AS album_date_created,
	COALESCE(NULLIF(album_listens, ''), '0')::int,
	COALESCE(NULLIF(album_favorites, ''), '0')::int,
	COALESCE(NULLIF(album_comments, ''), '0')::int,
	album_type,
	album_url,
	album_handle,
	album_information,
	COALESCE(NULLIF(album_tracks, ''), '0')::int,
	album_producer,
	album_engineer,
	album_image_file
FROM
	import_album;

INSERT
	INTO
	license
SELECT
	license_id::int,
	license_title,
	license_url
FROM
	import_license;

INSERT
	INTO
	track (track_id,track_title,track_duration,track_date_created,track_date_recorded,track_composer,track_lyricist,track_publisher,track_listens,track_favorites,track_comments,track_interest,track_copyright_c,track_copyright_p,track_explicit,track_explicit_note,track_instrumental,track_language_code,track_url,track_file,track_image_file,license_id)
SELECT
	track_id::int,
	track_title,
	COALESCE(NULLIF(track_duration, ''), '0')::int,
	to_date(track_date_created, 'DD-MM-YYYY') AS track_date_created,
	to_date(track_date_recorded, 'DD-MM-YYYY') AS track_date_recorded,
	track_composer,
	track_lyricist,
	track_publisher,
	COALESCE(NULLIF(track_listens, ''), '0')::int,
	COALESCE(NULLIF(track_favorites, ''), '0')::int,
	COALESCE(NULLIF(track_comments, ''), '0')::int,
	COALESCE(NULLIF(track_interest, ''), '0')::int,
	track_copyright_c,
	track_copyright_p,
	CASE
		WHEN track_explicit = 'Radio-Unsafe' THEN FALSE
		ELSE TRUE
	END AS track_explicit,
	track_explicit_note,
	COALESCE(NULLIF(track_instrumental, ''), '0')::bool,
	track_language_code,
	track_url,
	track_file,
	track_image_file,
	license_id::int
FROM
	import_track it;

INSERT
	INTO
	genre
SELECT
	genre_id::int,
	CASE
		WHEN genre_parent_id = '' THEN NULL
		ELSE genre_parent_id::int
	END AS genre_parent_id,
	genre_title,
	genre_handle,
	genre_color,
	top_level::bool
FROM
	import_genre
WHERE
	top_level = 'true';

INSERT
	INTO
	genre (genre_id,genre_parent_id,genre_title,genre_handle,genre_color,top_level)
SELECT
	genre_id::int,
	CASE
		WHEN genre_parent_id = '' THEN NULL
		ELSE genre_parent_id::int
	END AS genre_parent_id,
	genre_title,
	genre_handle,
	genre_color,
	top_level::bool
FROM
	import_genre
WHERE
	top_level != 'true';

INSERT
	INTO
	track_echonest (track_id,acousticness,energy,instrumentalness,liveness,speechiness,valence,danceability,tempo,artist_discovery,artist_hottness,artist_familiarity,track_hottness,track_currency)
SELECT
	track_id::int,
	NULLIF(acousticness, '')::float,
	NULLIF(energy, '')::float,
	NULLIF(instrumentalness, '')::float,
	NULLIF(liveness, '')::float,
	NULLIF(speechiness, '')::float,
	NULLIF(valence, '')::float,
	NULLIF(danceability, '')::float,
	NULLIF(tempo, '')::float,
	NULLIF(artist_discovery, '')::float,
	NULLIF(artist_hottness, '')::float,
	NULLIF(artist_familiarity, '')::float,
	NULLIF(track_hottness, '')::float,
	NULLIF(track_currency, '')::float
FROM
	import_echonest;

INSERT
	INTO
	contient_genres (track_id, genre_id)
SELECT
	track_id::int,
	genre_id::int
FROM
	import_track_genre;

INSERT
	INTO
	realiser (album_id,track_id,artist_id)
SELECT
	album_id::int,
	track_id::int,
	artist_id::int
FROM
	import_track;

INSERT
	INTO
	language (language_id, language_code, language_label, language_handle)
SELECT
	language_id::int,
	language_code,
	language_name,
	language_handle
FROM
	import_language;

INSERT
	INTO
	track_chanter_en (track_id, language_id)
SELECT
	track_id::int,
	language_id::int
FROM
	import_track;

INSERT
	INTO
	artiste_chante (artist_id, language_id)
SELECT
	DISTINCT artist_id::int,
	language_id::int
FROM
	import_track;
