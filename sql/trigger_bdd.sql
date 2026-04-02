-- permet l'obtention d'une distribution gaussienne
CREATE OR REPLACE 
FUNCTION gauss(max integer)
 RETURNS double PRECISION
 LANGUAGE plpgsql AS $$
	DECLARE
		rng float;
	BEGIN
		rng := 0;
		FOR i IN 0.. max LOOP
			rng := rng + random();
		END LOOP;
		RETURN rng;
	END;
$$;


CREATE OR REPLACE FUNCTION assign_playlist_track_position()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.position IS NULL OR NEW.position < 1 THEN
        SELECT COALESCE(MAX(position), 0) + 1
        INTO NEW.position
        FROM playlist_contient_track
        WHERE playlist_id = NEW.playlist_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_assign_playlist_track_position
BEFORE INSERT ON playlist_contient_track
FOR EACH ROW
EXECUTE FUNCTION assign_playlist_track_position();


-- Calcul echonest à partir des musiques favoris du user
CREATE OR REPLACE FUNCTION calc_echonest_favoris()
RETURNS TRIGGER AS $$
BEGIN
    -- Update si le user existe déjà
    IF EXISTS (SELECT 1 FROM user_preference_echonest WHERE user_id = NEW.user_id) THEN
        UPDATE user_preference_echonest
        SET acousticness = (SELECT AVG(te.acousticness)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            energy = (SELECT AVG(te.energy)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            instrumentalness = (SELECT AVG(te.instrumentalness)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            liveness = (SELECT AVG(te.liveness)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            speechiness = (SELECT AVG(te.speechiness)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            valence = (SELECT AVG(te.valence)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            danceability = (SELECT AVG(te.danceability)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            tempo = (SELECT AVG(te.tempo)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id)
        WHERE user_id = NEW.user_id;
    ELSE
        -- Insert new data
        INSERT INTO user_preference_echonest (acousticness, energy, instrumentalness, liveness, speechiness, valence, danceability, tempo, user_id)
        VALUES (
            (SELECT AVG(te.acousticness)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.energy)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.instrumentalness)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.liveness)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.speechiness)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.valence)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.danceability)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.tempo)
                FROM ajoute_favori af
                JOIN track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            NEW.user_id
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calc_echonest_favoris
AFTER INSERT OR DELETE ON ajoute_favori
FOR EACH ROW
EXECUTE FUNCTION calc_echonest_favoris();


CREATE OR REPLACE FUNCTION incr_listens()
RETURNS TRIGGER AS $$
DECLARE
    v_album_id INT;
    v_artist_ID INT;
BEGIN
    SELECT album_id, artist_id
    INTO v_album_id, v_artist_ID
    FROM realiser
    WHERE track_id = NEW.track_id;

    UPDATE track
    set track_listens = track_listens + 1
    WHERE track_id = NEW.track_id;

    UPDATE album
    set album_listens = album_listens + 1
    WHERE album_id = v_album_id;

    UPDATE artist
    set artist_listens = artist_listens + 1
    WHERE artist_id = v_artist_ID;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calc_listens
AFTER INSERT on user_ecoute
FOR EACH ROW
EXECUTE FUNCTION incr_listens();
