# Babbler
Homemade twitter-like web application

# Installation

Sur la racine du projet, exécuter les commandes suivantes en ordre.

```bash
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p < data/dump.sql
```

Par la suite, exécuter le fichier ```data/populate.py``` dans votre IDE. Celui-ci s'occupera d'ajouter des données au projet.

Finalement, il suffit de lancer l'application avec le fichier ```src/app.py```.

(le main se trouve à la fin des deux fichiers)

# FAQ
- Lors de l'exécution du projet, si la page d'accueil retourne une erreur 500, c'est parce qu'il faut configurer le sql_mode ainsi:
```bash
STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```
![](doc/sql_mode.png?raw=true)

# Diagramme entité relation
![](doc/ERDiag.png?raw=true) 
