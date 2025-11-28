-- Calcul echonest à partir des musiques favoris du user
CREATE OR REPLACE FUNCTION sae5_6.calc_echonest_favoris()
RETURNS TRIGGER AS $$
BEGIN
    -- Update si le user existe déjà
    IF EXISTS (SELECT 1 FROM sae5_6.user_preference_echonest WHERE user_id = NEW.user_id) THEN
        UPDATE sae5_6.user_preference_echonest
        SET acousticness = (SELECT AVG(te.acousticness)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            energy = (SELECT AVG(te.energy)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            instrumentalness = (SELECT AVG(te.instrumentalness)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            liveness = (SELECT AVG(te.liveness)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            speechiness = (SELECT AVG(te.speechiness)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            valence = (SELECT AVG(te.valence)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            danceability = (SELECT AVG(te.danceability)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            tempo = (SELECT AVG(te.tempo)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id)
        WHERE user_id = NEW.user_id;
    ELSE
        -- Insert new data
        INSERT INTO sae5_6.user_preference_echonest (acousticness, energy, instrumentalness, liveness, speechiness, valence, danceability, tempo, user_id)
        VALUES (
            (SELECT AVG(te.acousticness)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.energy)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.instrumentalness)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.liveness)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.speechiness)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.valence)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.danceability)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            (SELECT AVG(te.tempo)
                FROM sae5_6.ajoute_favori af
                JOIN sae5_6.track_echonest te ON af.track_id = te.track_id
                WHERE af.user_id = NEW.user_id),
            NEW.user_id
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calc_echonest_favoris
AFTER INSERT OR DELETE ON sae5_6.ajoute_favori
FOR EACH ROW
EXECUTE FUNCTION sae5_6.calc_echonest_favoris();


CREATE OR REPLACE FUNCTION sae5_6.incr_listens()
RETURNS TRIGGER AS $$
DECLARE
    v_album_id INT;
    v_artist_ID INT;
BEGIN
    SELECT sae5_6.album_id, sae5_6.artist_id
    INTO v_album_id, v_artist_ID
    FROM sae5_6.track
    WHERE track_id = NEW.track_id;

    UPDATE sae5_6.track
    set track_listens = track_listens + 1
    WHERE track_id = NEW.track_id;


    UPDATE sae5_6.album
    set album_listens = track_listens + 1
    WHERE album_id = v_album_id;

    UPDATE sae5_6.artist
    set artist_listens = artist_listens + 1
    WHERE artist_id = v_album_id;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calc_listens
AFTER INSERT on sae5_6.user_ecoute
FOR EACH ROW
EXECUTE FUNCTION sae5_6.incr_listens();
