# utilisation

Si vous ne souhaitez pas utiliser git lfs, suivez les instructions "Sinon" plus bas.
Installer git lfs pour obtenir les datasets complets depuis le repo.
ce repo utilise [git lfs](https://git-lfs.com/) pour stocker les csv,
pour cloner le repo utilisez :  
`git clone https://github.com/IUT-InTheEnd/analyse.git`  
et pour cloner les csv complets utilisez :  
`git lfs checkout`  

## Sinon
Cloner le repo :
```
git clone https://github.com/IUT-InTheEnd/database.git
```

Récupérer le clean_echonest venant de la partie analyse du repo :
En clonant le repo  :
```
git clone https://github.com/IUT-InTheEnd/analyse.git
```
Puis lancer main.py dans le dossier analyse.
Et récupérer le dataset clean_echonest.csv dans le dossier cleaned_dataset le mettre dans le dossier dataset de ce repo.

Récupérer les autres datasets depuis le Teams qui sont :
raw_genres.csv
raw_albums.csv
rtaw_artists.csv
raw_tracks.csv

Récupérer aussi le dataset clean_answers.csv depuis :
https://github.com/IUT-InTheEnd/analyse-questions/tree/main/src/analyse_questions/cleanup/out

**TOUT LES DATASETS DOIVENT ETRE PLACES DANS LE DOSSIER dataset**


**Il y a un bouton dans l'interface pour installer les dépendances.**
**Attention** : si les dépendances ne s'installent pas, il faut les installer manuellement avec pip ou crée un environnement. Un fichier requirements.txt est fourni.

Lancer le docker avec la commande :
```
docker compose up
```

Une fois lancer, lancer le script main.py depuis la root du projet tel que :
```
python3 main.py
```

Une fois que le script a terminé vous pouvez accéder à la base de donnée via votre client préféré.



