-- run once per database manually

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