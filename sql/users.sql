-- 1. APP USER — InTheEnd_User (existant, créé lors de l'installation)
--    Rôle : application Laravel principale (web + migrations)
--    Droits : SELECT / INSERT / UPDATE / DELETE sur toutes les tables

GRANT CONNECT ON DATABASE "InTheEnd_DB" TO "InTheEnd_User";
GRANT USAGE ON SCHEMA public TO "InTheEnd_User";

-- Droits sur toutes les tables existantes
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "InTheEnd_User";

-- Droits sur les séquences (nécessaires pour les INSERT sur colonnes BIGSERIAL/SERIAL)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO "InTheEnd_User";

-- Propagation automatique aux futures tables/séquences créées par cet utilisateur
-- (les migrations Laravel sont exécutées avec ce compte)
ALTER DEFAULT PRIVILEGES FOR ROLE "InTheEnd_User" IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO "InTheEnd_User";
ALTER DEFAULT PRIVILEGES FOR ROLE "InTheEnd_User" IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO "InTheEnd_User";


-- 2. ADMIN USER — InTheEnd_Admin
--    Rôle : administration de la base (DBA, import de données, maintenance)
--    Droits : tous les droits sur toutes les tables + DDL (CREATE, DROP, ALTER, TRUNCATE, INDEX...) via CREATE ON SCHEMA
--    Ne pas utiliser en production

CREATE USER "InTheEnd_Admin" WITH
    PASSWORD 'change_me_admin'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    LOGIN;

GRANT CONNECT ON DATABASE "InTheEnd_DB" TO "InTheEnd_Admin";

-- CREATE ON SCHEMA = peut créer/modifier/supprimer des tables
GRANT USAGE, CREATE ON SCHEMA public TO "InTheEnd_Admin";

-- Tous les droits sur les tables et séquences existantes
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "InTheEnd_Admin";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "InTheEnd_Admin";

-- Propagation automatique aux futures tables/séquences créées par InTheEnd_User
ALTER DEFAULT PRIVILEGES FOR ROLE "InTheEnd_User" IN SCHEMA public
    GRANT ALL PRIVILEGES ON TABLES TO "InTheEnd_Admin";
ALTER DEFAULT PRIVILEGES FOR ROLE "InTheEnd_User" IN SCHEMA public
    GRANT ALL PRIVILEGES ON SEQUENCES TO "InTheEnd_Admin";


-- 3. API USER — InTheEnd_API
--    Rôle : endpoints REST (Laravel Sanctum) — accès externe limité
--
--    Lecture seule :
--      - Catalogue musical (track, artist, album, genre, language, license…)
--      - Données de base des utilisateurs (authentification des tokens)
--
--    Lecture + écriture :
--      - Interactions utilisateur (historique, favoris, playlists, préférences)
--      - Tokens Sanctum (personal_access_tokens)

CREATE USER "InTheEnd_API" WITH
    PASSWORD 'change_me_api'
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    LOGIN;

GRANT CONNECT ON DATABASE "InTheEnd_DB" TO "InTheEnd_API";
GRANT USAGE ON SCHEMA public TO "InTheEnd_API";

-- Donnée générales - lecture seul
GRANT SELECT ON
    track,
    artist,
    album,
    genre,
    language,
    license,
    track_echonest,
    artiste_chante,
    contient_genres,
    track_chanter_en,
    realiser,
    represente,
    supervise
TO "InTheEnd_API";

-- Données de base des utilisateurs — lecture seule (pour l'authentification des tokens)
GRANT SELECT ON
    "user",
    user_profile,
    user_privacy,
    user_parle
TO "InTheEnd_API";

-- Intéractions utilisateur — lecture + écriture (CRUD)
GRANT SELECT, INSERT, UPDATE, DELETE ON
    user_ecoute,
    user_prefere_artiste,
    user_ajoute_album_favoris,
    ajoute_genre_favoris,
    user_preference_echonest,
    playlist,
    playlist_contient_track
TO "InTheEnd_API";

-- Token Sanctum - lecture avec écriture pour gérer les tokens d'authentification de l'API
GRANT SELECT, INSERT, UPDATE, DELETE ON
    personal_access_tokens
TO "InTheEnd_API";

-- Séquence des playlists et tokens d'accès personnels (pour les INSERT)
GRANT USAGE, SELECT ON SEQUENCE
    playlist_playlist_id_seq,
    personal_access_tokens_id_seq
TO "InTheEnd_API";

-- Propagation automatique en lecture seule pour les futures tables du catalogue
ALTER DEFAULT PRIVILEGES FOR ROLE "InTheEnd_User" IN SCHEMA public
    GRANT SELECT ON TABLES TO "InTheEnd_API";

ALTER USER "InTheEnd_API" WITH PASSWORD 'MdpApi!!!!!!!!!';

--  Table Accès                | InTheEnd_User | InTheEnd_Admin | InTheEnd_API
-- ___________________________________________________________________________
--  track / artist / album     | CRUD          | ALL      | SELECT
--  genre / language / license | CRUD          | ALL      | SELECT
--  track_echonest             | CRUD          | ALL      | SELECT
--  artiste_chante / realiser  | CRUD          | ALL      | SELECT
--  contient_genres / etc.     | CRUD          | ALL      | SELECT
--  "user"                     | CRUD          | ALL      | SELECT
--  user_profile / _privacy    | CRUD          | ALL      | SELECT
--  user_parle                 | CRUD          | ALL      | SELECT
--  user_ecoute                | CRUD          | ALL      | CRUD
--  user_prefere_artiste       | CRUD          | ALL      | CRUD
--  user_ajoute_album_favoris  | CRUD          | ALL      | CRUD
--  ajoute_genre_favoris       | CRUD          | ALL      | CRUD
--  user_preference_echonest   | CRUD          | ALL      | CRUD
--  playlist                   | CRUD          | ALL      | CRUD
--  playlist_contient_track    | CRUD          | ALL      | CRUD
--  personal_access_tokens     | CRUD          | ALL      | CRUD
--  password_reset_tokens      | CRUD          | ALL      | --
--  sessions                   | CRUD          | ALL      | --
--  cache / cache_locks        | CRUD          | ALL      | --
--  jobs / job_batches / etc.  | CRUD          | ALL      | --
--  import_*                   | CRUD          | ALL      | --
--  migrations                 | CRUD          | ALL      | --
