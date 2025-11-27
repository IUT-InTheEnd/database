INSERT
	INTO
	sae5_6.artist
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
	artist_favorites::int,
	artist_comments::int,
	(
		SELECT
			sum(track_listens::int)
		FROM
			sae5_6.import_track it
		WHERE
			it.artist_id = ia.artist_id
	) AS artist_listens,
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
	DATE(artist_date_created) AS artist_date_created,
	artist_image_file
FROM
	sae5_6.import_artist ia;


INSERT
	INTO
	sae5_6.album
SELECT
	album_id::int,
	album_title,
	TO_DATE(album_date_release, 'DD-MM-YYYY') AS album_date_release,
	TO_DATE(album_date_created, 'DD-MM-YYYY') AS album_date_created,
	album_listens::int,
	album_favorites::int,
	album_comments::int,
	album_type,
	album_url,
	album_handle,
	album_information,
	album_tracks::int,
	album_producer,
	album_engineer
FROM
	sae5_6.import_album;

INSERT
	INTO
	sae5_6.license
SELECT
	license_id::int,
	license_title,
	license_url
FROM
	sae5_6.import_license;

INSERT
	INTO
	sae5_6.track
SELECT
	track_id::int,
	track_title,
	track_duration::int,
	to_date(track_date_created, 'DD-MM-YYYY') AS track_date_created,
	to_date(track_date_recorded, 'DD-MM-YYYY') AS track_date_recorded,
	track_composer,
	track_lyricist,
	track_publisher,
	track_listens::int,
	track_favorites::int,
	track_comments::int,
	track_interest::int,
	track_copyright_c,
	track_copyright_p,
	CASE
		WHEN track_explicit = 'Radio-Unsafe' THEN FALSE
		ELSE TRUE
	END AS track_explicit,
	track_explicit_note,
	track_instrumental::bool,
	track_language_code,
	track_url,
	track_file,
	track_image_file,
	license_id::int
FROM
	sae5_6.import_track it;

INSERT
	INTO
	sae5_6.genre
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
	sae5_6.import_genre
WHERE
	top_level = 'true';

INSERT
	INTO
	sae5_6.genre
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
	sae5_6.import_genre
WHERE
	top_level != 'true';

INSERT
	INTO
	sae5_6.track_echonest
SELECT
	acousticness::float,
	energy::float,
	instrumentalness::float,
	liveness::float,
	speechiness::float,
	valence::float,
	danceability::float,
	tempo::float,
	artist_discovery::float,
	artist_hottness::float,
	artist_familiarity::float,
	track_hottness::float,
	track_currency::float,
	track_id::int
FROM
	sae5_6.import_echonest;

INSERT
	INTO
	sae5_6.contient_genres
SELECT
	track_id::int,
	genre_id::int
FROM
	sae5_6.import_track_genre;

-- track sans album mais album_id pk donc not null
-- jvais me tirer une balle c'est quoi ce dataset de con

-- _                _ _    _ _   _         _ _    _               
--| |__   __ _ _ __(_) | _(_) |_| |_ ___  (_) | _| | _____  _   _ 
--| '_ \ / _` | '__| | |/ / | __| __/ _ \ | | |/ / |/ / _ \| | | |
--| | | | (_| | |  | |   <| | |_| ||  __/ | |   <|   < (_) | |_| |
--|_| |_|\__,_|_|  |_|_|\_\_|\__|\__\___| |_|_|\_\_|\_\___/ \__,_|

--INSERT
--	INTO
--	sae5_6.realiser
--SELECT
--	CASE
--		WHEN album_id = '' THEN NULL
--		ELSE album_id::int
--	END AS album_id,
--	track_id::int,
--	artist_id::int
--FROM
--	sae5_6.import_track;

--______________________
--< Wallah jvais me tuer >
-- ----------------------
--          \
--            \             .:---------:.
--              \        .:               :.
--                    .· __..~~       ~~..__ ·.
--               ___________________________________
--                |  :   ---     | |     ---   :  |
--           __   | :   / @ \    | |    / @ \   : |
--          /  \   \:   \___/   /   \   \___/   :/
--  _  _  _ |  |    \          /     \          /
-- / \/ \/ \|  |    : --------         -------- :
-- |  |  | _|_ |    :    o   __________    o    :
-- \_/\_/\|    |     :  。 0 |   ||   |  0  。 :
-- |       \_  |      :-     \___/\___/      -:
-- |   _____   |       .-                   -.
--  \     /   /          .-               -.
--   \______ /              :-----------:
