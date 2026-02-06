-- user_profile table
SELECT setval('user_profile_user_profile_id_seq', COALESCE((SELECT MAX(user_profile_id) FROM user_profile), 1));

-- user table
SELECT setval('user_id_seq', COALESCE((SELECT MAX(id) FROM "user"), 1));

-- album table
SELECT setval('album_album_id_seq', COALESCE((SELECT MAX(album_id) FROM album), 1));

-- genre table
SELECT setval('genre_genre_id_seq', COALESCE((SELECT MAX(genre_id) FROM genre), 1));

-- license table
SELECT setval('license_license_id_seq', COALESCE((SELECT MAX(license_id) FROM license), 1));

-- track table
SELECT setval('track_track_id_seq', COALESCE((SELECT MAX(track_id) FROM track), 1));

-- track_echonest table (note: track_id is SERIAL but also FK, sequence still exists)
SELECT setval('track_echonest_track_id_seq', COALESCE((SELECT MAX(track_id) FROM track_echonest), 1));

-- artist table
SELECT setval('artist_artist_id_seq', COALESCE((SELECT MAX(artist_id) FROM artist), 1));

-- language table
SELECT setval('language_language_id_seq', COALESCE((SELECT MAX(language_id) FROM language), 1));

-- playlist table
SELECT setval('playlist_playlist_id_seq', COALESCE((SELECT MAX(playlist_id) FROM playlist), 1));
