# Utilisation

## Pré-requis

Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

Démarrer PostgreSQL avec Docker :

```bash
docker compose up
```

Placer les datasets source dans `dataset/` :

- `raw_albums.csv`
- `raw_artists.csv`
- `raw_tracks.csv`
- `raw_genres.csv`
- `clean_echonest.csv`
- `clean_answers.csv`

## Nouveau pipeline

Le seeding est maintenant séparé en deux étapes :

1. `source -> CSV préparés`
   Produit des artefacts réutilisables dans `prepared_seed_data/` pour les données musique et dans `user_data_clean/` pour les données utilisateur.
2. `CSV préparés -> base de données`
   Charge uniquement les artefacts déjà préparés dans PostgreSQL.

Cette séparation permet de reseed rapidement la base quand les datasets source n'ont pas changé.

## Commandes

Rebuild complet des artefacts puis import base :

```bash
python3 main.py --rebuild
```

Import rapide à partir des CSV déjà préparés :

```bash
python3 main.py
```

Si les fichiers préparés n'existent pas encore, `main.py` demande d'exécuter `--rebuild` d'abord.

## Détails

- `prepare_seed_data.py` reconstruit les CSV préparés pour les tables d'import.
- `user.py` reconstruit les CSV utilisateurs nettoyés.
- `peuplement.py` reste disponible comme alias vers `prepare_seed_data.py`.
- `artist_listens` est désormais pré-calculé pendant la préparation des CSV, ce qui évite la sous-requête coûteuse dans `sql/import_tables.sql`.
- Les valeurs manquantes et `NaN` sont nettoyées avant l'écriture des CSV préparés pour éviter leur insertion en base.
